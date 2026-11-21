#!/usr/bin/env python3
"""Build the Xthrx AltStore/SideStore aggregate catalogue."""
import concurrent.futures
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
SOURCE_URL = os.environ.get("XTHRX_SOURCE_URL", "https://akatsubaki-emu.github.io/altsource/Xthrx%27s%20repo.json")
HEADERS = {"User-Agent": "Xthrx-AltSource-Merger/4.0", "Accept": "application/json,text/plain,*/*"}
TIMEOUT = (5, 20)
MAX_BYTES = 25 * 1024 * 1024
MAX_VERSIONS_PER_APP = 20
MAX_DESCRIPTION_LENGTH = 4000


def items(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    return []


def unpack(data):
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        return []
    for key in ("apps", "data", "applications", "items"):
        found = items(data.get(key))
        if found:
            return found
    for key in ("source", "repo", "repository", "result", "catalogue", "catalog"):
        nested = data.get(key)
        if isinstance(nested, dict):
            for app_key in ("apps", "data", "applications", "items"):
                found = items(nested.get(app_key))
                if found:
                    return found
    return []


def http_url(value):
    if not isinstance(value, str):
        return ""
    value = value.strip()
    parsed = urlparse(value)
    return value if parsed.scheme in ("http", "https") and parsed.netloc else ""


def clean_text(value, limit=MAX_DESCRIPTION_LENGTH, default=""):
    if not isinstance(value, (str, int, float)):
        return default
    return str(value).strip()[:limit] or default


def normalize_app(raw):
    if not isinstance(raw, dict):
        return None
    name = clean_text(raw.get("name") or raw.get("title"), 200)
    bundle = clean_text(raw.get("bundleIdentifier") or raw.get("bundleID") or raw.get("bundle_id"), 255)
    if not name or not bundle:
        return None

    raw_versions = items(raw.get("versions")) or [raw]
    versions, seen = [], set()
    for version in raw_versions:
        if not isinstance(version, dict):
            continue
        version_name = clean_text(version.get("version") or version.get("versionString") or raw.get("version"), 100)
        download = http_url(version.get("downloadURL") or raw.get("downloadURL"))
        if not version_name or not download:
            continue
        release_date = clean_text(
            version.get("date") or version.get("versionDate") or raw.get("versionDate") or raw.get("date"),
            64,
            "1970-01-01",
        )
        try:
            size = max(0, int(version.get("size", raw.get("size", 0)) or 0))
        except (ValueError, TypeError, OverflowError):
            size = 0

        description = clean_text(
            version.get("localizedDescription")
            or version.get("versionDescription")
            or raw.get("versionDescription")
            or raw.get("localizedDescription"),
        )
        entry = {
            "version": version_name,
            "date": release_date,
            "downloadURL": download,
            "localizedDescription": description,
            "size": size,
        }
        build = clean_text(version.get("buildVersion") or raw.get("buildVersion"), 100)
        if build:
            entry["buildVersion"] = build
        for field in ("minOSVersion", "maxOSVersion"):
            value = clean_text(version.get(field), 32)
            if value:
                entry[field] = value

        key = (version_name, build, download)
        if key not in seen:
            seen.add(key)
            versions.append(entry)

    if not versions:
        return None
    versions.sort(key=lambda value: value.get("date", ""), reverse=True)
    versions = versions[:MAX_VERSIONS_PER_APP]

    app = {
        "name": name,
        "bundleIdentifier": bundle,
        "developerName": clean_text(
            raw.get("developerName") or raw.get("developer") or raw.get("author"),
            200,
            "Unknown Developer",
        ),
        "localizedDescription": clean_text(
            raw.get("localizedDescription") or raw.get("description") or raw.get("subtitle") or name,
        ),
        "versions": versions,
    }
    for field, limit in (("subtitle", 500), ("tintColor", 64), ("category", 100)):
        value = clean_text(raw.get(field), limit)
        if value:
            app[field] = value

    icon = http_url(raw.get("iconURL") or raw.get("iconUrl") or raw.get("icon"))
    if icon:
        app["iconURL"] = icon
    return app


def merge_apps(results):
    """Merge by exact bundle ID, retaining distinct recent version downloads."""
    merged = {}
    for feed in results:
        if feed.get("status") != "ok":
            continue
        for app in feed.get("apps", []):
            bundle = app["bundleIdentifier"]
            source = feed["name"]
            source_url = feed.get("final_url") or feed["url"]
            if bundle not in merged:
                item = dict(app)
                item.update({"xthrxSource": source, "xthrxSourceURL": source_url, "xthrxSources": [source]})
                merged[bundle] = item
                continue

            current = merged[bundle]
            current_latest = max((str(value.get("date", "")) for value in current["versions"]), default="")
            incoming_latest = max((str(value.get("date", "")) for value in app["versions"]), default="")
            versions = {
                (value.get("version"), value.get("buildVersion", ""), value.get("downloadURL")): value
                for value in current["versions"]
            }
            for value in app["versions"]:
                versions.setdefault(
                    (value.get("version"), value.get("buildVersion", ""), value.get("downloadURL")),
                    value,
                )
            current["versions"] = sorted(
                versions.values(),
                key=lambda value: str(value.get("date", "")),
                reverse=True,
            )[:MAX_VERSIONS_PER_APP]
            if source not in current["xthrxSources"]:
                current["xthrxSources"].append(source)
            if incoming_latest > current_latest:
                for field in ("name", "developerName", "subtitle", "localizedDescription", "iconURL", "tintColor", "category"):
                    if field in app:
                        current[field] = app[field]
                current["xthrxSource"], current["xthrxSourceURL"] = source, source_url
    return list(merged.values())


def fetch(source):
    result = {"name": source.get("name") or source["url"], "url": source["url"], "status": "failed"}
    url = http_url(source.get("url"))
    if not url:
        result["error"] = "Invalid HTTP(S) URL"
        return result
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        if len(response.content) > MAX_BYTES:
            raise ValueError("Response exceeds 25 MiB limit")
        body = response.content.decode(response.encoding or "utf-8-sig").lstrip("\ufeff \t\r\n")
        if not body or body.startswith("<"):
            raise ValueError("HTML or empty response")
        records = unpack(response.json())
        apps = [app for record in records if (app := normalize_app(record)) is not None]
        if not apps:
            raise ValueError(f"No compatible apps ({len(records)} records)")
        result.update({
            "status": "ok",
            "final_url": response.url,
            "appCount": len(records),
            "validApps": len(apps),
            "rejectedApps": len(records) - len(apps),
            "apps": apps,
        })
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
    return result


def build(manifest, fetcher=fetch):
    sources, seen = [], set()
    for source in manifest.get("sources", []):
        if not isinstance(source, dict):
            continue
        url = http_url(source.get("url"))
        if url and url not in seen:
            seen.add(url)
            sources.append({**source, "url": url})
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(fetcher, sources))
    apps = merge_apps(results)
    accepted = [
        {
            "name": feed["name"],
            "url": feed.get("final_url", feed["url"]),
            "status": "ok",
            "appCount": feed.get("appCount", 0),
            "validApps": feed.get("validApps", 0),
            "rejectedApps": feed.get("rejectedApps", 0),
        }
        for feed in results
        if feed.get("status") == "ok"
    ]
    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "configuredFeeds": len(sources),
        "acceptedFeeds": len(accepted),
        "failedFeeds": len(sources) - len(accepted),
        "uniqueApps": len(apps),
        "feeds": [{key: value for key, value in feed.items() if key != "apps"} for feed in results],
    }
    catalogue = {
        "name": "Xthrx's Repo",
        "identifier": "com.xthrx.altstore.repo",
        "sourceURL": SOURCE_URL,
        "subtitle": "A combined community catalogue for AltStore and SideStore.",
        "description": "Community index of apps from public AltStore, SideStore and PAL feeds.",
        "apps": apps,
        "xthrxSources": accepted,
    }
    return catalogue, report


def main():
    manifest = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    catalogue, report = build(manifest)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "xthrx-source-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"{report['acceptedFeeds']}/{report['configuredFeeds']} feeds accepted; "
        f"{report['uniqueApps']} unique apps"
    )
    if not catalogue["apps"]:
        print("No compatible apps; refusing to publish an empty catalogue.")
        return 2
    (OUT / "Xthrx's repo.json").write_text(
        json.dumps(catalogue, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
