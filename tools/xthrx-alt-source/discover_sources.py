#!/usr/bin/env python3
"""Discover distinct public AltStore/PAL source manifests from GitHub code search.

Only real repository files returned by GitHub's search API are added. The normal
feed builder remains responsible for validating compatibility before publication.
"""
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "sources.json"
API = "https://api.github.com/search/code"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Xthrx-AltSource-Discovery/1.0",
}
TOKEN = os.environ.get("GITHUB_TOKEN", "")
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

MAX_TOTAL = 6000
MAX_NEW = 1000
QUERIES = (
    '"bundleIdentifier" "downloadURL" extension:json',
    'AltStore source extension:json',
    'PALSource extension:json',
    'AltStore apps.json',
    'SideStore source extension:json',
)
TIMEOUT = (10, 30)


def normalized_url(owner, repo, branch, path):
    if not all(isinstance(value, str) and value for value in (owner, repo, branch, path)):
        return ""
    if not (path.lower().endswith(".json") or re.search(r"(source|repo|apps|altstore|pal)", path, re.I)):
        return ""
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(branch, safe='')}/{quote(path, safe='/')}"


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = manifest.setdefault("sources", [])
    seen = {
        str(item.get("url", "")).strip().rstrip("/")
        for item in sources if isinstance(item, dict) and item.get("url")
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
            response = session.get(API, params={"q": query, "per_page": 100, "page": page}, timeout=TIMEOUT)
            if response.status_code in (403, 429):
                print(f"GitHub search rate limit reached; keeping {added} discoveries from this run.")
                break
            response.raise_for_status()
            payload = response.json()
            results = payload.get("items", [])
            if not results:
                break
            for result in results:
                repository = result.get("repository") or {}
                owner = (repository.get("owner") or {}).get("login", "")
                repo = repository.get("name", "")
                branch = repository.get("default_branch", "main")
                path = result.get("path", "")
                url = normalized_url(owner, repo, branch, path)
                key = url.rstrip("/")
                if not url or key in seen:
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
            time.sleep(1)
        if added >= MAX_NEW or len(seen) >= MAX_TOTAL:
            break

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Unique source URLs: {initial} -> {len(seen)}; added {added}; target {MAX_TOTAL}.")
    print("Discovered candidates are not described as working until the feed validator accepts them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
