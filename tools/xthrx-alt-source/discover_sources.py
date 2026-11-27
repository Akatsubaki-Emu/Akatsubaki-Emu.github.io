#!/usr/bin/env python3
"""Discover distinct public AltStore/PAL source manifests from GitHub code search.

Only actual repository files returned by GitHub code search are added. These are
candidate feeds; the normal builder independently validates compatibility.
"""
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

import requests

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "sources.json"
API = "https://api.github.com/search/code"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Xthrx-AltSource-Discovery/2.0",
}
TOKEN = os.environ.get("GITHUB_TOKEN", "")
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

MAX_TOTAL = 6000
MAX_NEW = MAX_TOTAL
QUERIES = (
    '"bundleIdentifier" "downloadURL" extension:json',
    '"bundleIdentifier" "versions" extension:json',
    '"apps" "bundleIdentifier" "iconURL" extension:json',
    '"appPermissions" "bundleIdentifier" extension:json',
    '"sourceURL" "bundleIdentifier" extension:json',
    '"developerName" "bundleIdentifier" extension:json',
    '"minOSVersion" "downloadURL" extension:json',
    '"versionDate" "bundleIdentifier" extension:json',
    '"appID" "downloadURL" extension:json',
    '"apps" "downloadURL" "version" extension:json',
    'AltStore source extension:json',
    'AltStore apps.json',
    'SideStore source extension:json',
    'SideStore apps.json',
    'PALSource extension:json',
    'Feather repo extension:json',
    'esign repo extension:json',
    'AltStore repository iOS extension:json',
    'iOS app repo bundleIdentifier extension:json',
    'AltStore source repo.json',
)
TIMEOUT = (10, 30)
SEARCH_RETRIES = 8


def normalized_url(owner, repo, branch, path):
    if not all(isinstance(value, str) and value for value in (owner, repo, branch, path)):
        return ""
    if not (path.lower().endswith(".json") or re.search(r"(source|repo|apps|altstore|pal)", path, re.I)):
        return ""
    return (
        f"https://raw.githubusercontent.com/{owner}/{repo}/"
        f"{quote(branch, safe='')}/{quote(path, safe='/')}"
    )


def canonical_key(url):
    parts = urlsplit(str(url).strip())
    if parts.scheme.lower() not in ("http", "https") or not parts.netloc:
        return ""
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def search_page(session, query, page):
    params = {"q": query, "per_page": 100, "page": page}
    for attempt in range(SEARCH_RETRIES):
        response = session.get(API, params=params, timeout=TIMEOUT)
        if response.status_code not in (403, 429):
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("GitHub code search returned a non-object response")
            return payload.get("items", [])
        reset = response.headers.get("X-RateLimit-Reset")
        wait = 65
        if reset:
            try:
                wait = max(5, min(180, int(reset) - int(time.time()) + 2))
            except ValueError:
                pass
        print(f"GitHub search rate limit; waiting {wait}s (attempt {attempt + 1}/{SEARCH_RETRIES}).")
        time.sleep(wait)
    raise RuntimeError("GitHub code-search rate limit did not clear within retry budget")


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = manifest.setdefault("sources", [])
    seen = {
        key for item in sources
        if isinstance(item, dict) and (key := canonical_key(item.get("url", "")))
    }
    initial = len(seen)
    if initial >= MAX_TOTAL:
        print(f"Already at {initial} unique configured source URLs; target is {MAX_TOTAL}.")
        return 0

    added = 0
    session = requests.Session()
    session.headers.update(HEADERS)
    for query in QUERIES:
        for page in range(1, 11):
            if added >= MAX_NEW or len(seen) >= MAX_TOTAL:
                break
            results = search_page(session, query, page)
            if not results:
                break
            for result in results:
                repository = result.get("repository") or {}
                owner = (repository.get("owner") or {}).get("login", "")
                repo = repository.get("name", "")
                branch = repository.get("default_branch", "main")
                path = result.get("path", "")
                url = normalized_url(owner, repo, branch, path)
                key = canonical_key(url)
                if not key or key in seen:
                    continue
                seen.add(key)
                sources.append({
                    "name": f"GitHub discovery: {owner}/{repo}/{path}",
                    "url": url,
                    "verification": "discovered-candidate",
                    "discovered_by": "github-code-search",
                })
                added += 1
                if added >= MAX_NEW or len(seen) >= MAX_TOTAL:
                    break
            if len(results) < 100:
                break
            # Code search has a separate, low request budget; stay below it.
            time.sleep(6)
        if added >= MAX_NEW or len(seen) >= MAX_TOTAL:
            break

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Unique source URLs: {initial} -> {len(seen)}; added {added}; target {MAX_TOTAL}.")
    print("Discovered candidates are not described as working until the feed validator accepts them.")
    if len(seen) < MAX_TOTAL:
        print(f"Discovery stopped below target: {MAX_TOTAL - len(seen)} additional unique manifests are still needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
