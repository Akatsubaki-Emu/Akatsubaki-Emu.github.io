#!/usr/bin/env python3
"""Merge public AltStore/SideStore feeds into Xthrx's Repo."""
import concurrent.futures, json, os, re
from pathlib import Path
from urllib.parse import urlparse
import requests

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "Xthrx-AltSource-Merger/3.0", "Accept": "application/json,text/plain,*/*"}
TIMEOUT = (5, 15)

def unpack(data):
    """Accept common AltStore, PAL, and app-catalogue JSON layouts."""
    def values(value):
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return list(value.values())
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("apps", "data", "applications"):
            if key in data:
                items = values(data[key])
                if items:
                    return items
        for key in ("source", "repo", "repository", "result"):
            nested = data.get(key)
            if isinstance(nested, dict):
                for app_key_name in ("apps", "data", "applications"):
                    items = values(nested.get(app_key_name))
                    if items:
                        return items
    return []

def app_key(app):
    bundle = app.get("bundleIdentifier") or app.get("bundleID") or app.get("bundle_id")
    if bundle:
        return ("bundle", str(bundle).strip().casefold())
    name = app.get("name") or app.get("title")
    if name:
        developer = app.get("developerName") or app.get("developer") or app.get("author") or ""
        return ("name", re.sub(r"\s+", " ", str(name)).strip().casefold(), str(developer).casefold())
    return None

def fetch(source):
    try:
        response = requests.get(source["url"], headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        body = response.text.lstrip("\ufeff \t\r\n")
        if not body or body.startswith("<"):
            raise ValueError("HTML or empty response")
        apps = [item for item in unpack(response.json()) if isinstance(item, dict)]
        if not apps:
            raise ValueError("No recognised non-empty apps[] array")
        return {"name": source["name"], "url": source["url"], "final_url": response.url,
                "status": "ok", "apps": apps}
    except Exception as error:
        return {"name": source["name"], "url": source["url"], "status": "failed",
                "error": f"{type(error).__name__}: {error}"}

def main():
    manifest = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    unique, seen = [], set()
    for source in manifest["sources"]:
        url = source["url"].strip()
        if url not in seen and urlparse(url).scheme in ("http", "https"):
            seen.add(url)
            unique.append(source)
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(fetch, unique))

    merged, report, accepted = {}, [], []
    for result in results:
        if result["status"] == "ok":
            app_count, added = len(result["apps"]), 0
            for original in result.pop("apps"):
                app = dict(original)
                key = app_key(app)
                if key and key not in merged:
                    app["xthrxSource"] = result["name"]
                    app["xthrxSourceURL"] = result["final_url"]
                    merged[key] = app
                    added += 1
            result["appCount"] = app_count
            result["uniqueAppsAdded"] = added
            accepted.append({"name": result["name"], "url": result["final_url"], "status": "ok"})
        report.append({key: value for key, value in result.items() if key != "apps"})

    ok = sum(item["status"] == "ok" for item in results)
    print(f"{ok}/{len(unique)} candidate feeds accepted; {len(merged)} unique apps")
    (OUT / "xthrx-source-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not merged:
        print("No usable feeds; refusing to overwrite the published catalogue.")
        return 2

    output = {
        "name": "Xthrx's Repo",
        "identifier": "com.xthrx.altstore.repo",
        "sourceURL": os.environ.get(
            "XTHRX_SOURCE_URL",
            "https://i-steam.github.io/altsource/Xthrx%27s%20repo.json"),
        "apps": list(merged.values()),
        "xthrxSources": accepted,
    }
    (OUT / "Xthrx's repo.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
