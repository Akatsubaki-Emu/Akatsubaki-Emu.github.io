#!/usr/bin/env python3
"""Refresh the official Akatsubaki Emu AltStore source from published GitHub releases."""
import json
import re
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
API_URL = "https://api.github.com/repos/Akatsubaki-Emu/Akatsubaki-Emu/releases?per_page=30"
ICON_URLS = {
    "main": "https://akatsubaki-emu.github.io/img/akatsubaki-icon-default.png",
    "nightly": "https://akatsubaki-emu.github.io/img/akatsubaki-icon-simple.png",
}
BUNDLE_IDS = {
    "main": "com.xthrx.isteam",
    "nightly": "com.xthrx.isteam.nightly",
}
APP_NAMES = {
    "main": "Akatsubaki Emu",
    "nightly": "Akatsubaki Emu Nightly",
}
DESCRIPTION = (
    "Experimental iOS game-library and guest-runtime project. It is not yet a working PC emulator "
    "and does not guarantee Windows/Linux guest boot or Steam game compatibility. This development "
    "build is unsigned; sign it with a compatible installer before use."
)


def release_version(release):
    text = " ".join((release.get("name") or "", release.get("body") or ""))
    match = re.search(r"(?<![0-9])([0-9]+\.[0-9]+\.[0-9]+)(?![0-9])", text)
    return match.group(1) if match else ""


def app_from_release(release, channel):
    if release.get("draft") or release.get("tag_name") != channel:
        return None
    if bool(release.get("prerelease")) != (channel == "nightly"):
        return None
    version = release_version(release)
    if not version:
        return None
    asset = next(
        (item for item in release.get("assets", []) if item.get("name") == "iSteam-ios.ipa"),
        None,
    )
    if not asset:
        return None
    download_url = asset.get("browser_download_url", "")
    if not download_url.startswith("https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases/download/"):
        return None
    published = release.get("published_at") or release.get("created_at") or ""
    if not published:
        return None
    try:
        size = max(0, int(asset.get("size", 0)))
    except (TypeError, ValueError, OverflowError):
        size = 0
    channel_label = "Nightly" if channel == "nightly" else "Main"
    version_entry = {
        "version": version,
        "buildVersion": str(int(version.rsplit(".", 1)[1])),
        "date": published,
        "downloadURL": download_url,
        "size": size,
        "localizedDescription": f"{channel_label} iOS build {version}. Unsigned development build; signing required.",
        "minOSVersion": "16.0",
    }
    digest = asset.get("digest", "")
    if isinstance(digest, str) and digest.startswith("sha256:"):
        version_entry["sha256"] = digest.split(":", 1)[1].lower()
    return {
        "name": APP_NAMES[channel],
        "bundleIdentifier": BUNDLE_IDS[channel],
        "developerName": "Xthrx",
        "subtitle": f"Experimental iOS {channel_label.lower()}",
        "localizedDescription": DESCRIPTION,
        "iconURL": ICON_URLS[channel],
        "tintColor": "#7A263A",
        "versions": [version_entry],
    }


def build_sources(releases, existing):
    existing_apps = {
        app.get("bundleIdentifier"): app
        for app in existing.get("apps", [])
        if isinstance(app, dict) and app.get("bundleIdentifier")
    }
    apps = []
    for channel in ("main", "nightly"):
        latest = next(
            (app for release in releases if (app := app_from_release(release, channel))),
            None,
        )
        fallback = existing_apps.get(BUNDLE_IDS[channel])
        if fallback is None:
            fallback = next(
                (
                    app for bundle, app in existing_apps.items()
                    if bundle.casefold() == BUNDLE_IDS[channel].casefold()
                ),
                None,
            )
        if latest:
            apps.append(latest)
        elif fallback and fallback.get("versions"):
            preserved = dict(fallback)
            preserved["bundleIdentifier"] = BUNDLE_IDS[channel]
            preserved["iconURL"] = ICON_URLS[channel]
            apps.append(preserved)

    source = {
        "name": "Akatsubaki Emu",
        "subtitle": "Experimental iOS emulation project",
        "description": (
            "Official Akatsubaki Emu iOS builds. Experimental and unstable; not yet a working PC "
            "emulator. Unsigned IPAs require a compatible signing method."
        ),
        "iconURL": ICON_URLS["main"],
        "website": "https://akatsubaki-emu.github.io/",
        "tintColor": "#7A263A",
        "apps": apps,
        "featuredApps": [app["bundleIdentifier"] for app in apps],
    }

    pal_apps = []
    for app in apps:
        version = app["versions"][0]
        pal_apps.append({
            "name": app.get("name", "Akatsubaki Emu"),
            "bundleIdentifier": app["bundleIdentifier"],
            "developerName": app.get("developerName", "Xthrx"),
            "subtitle": app.get("subtitle", "Experimental iOS build"),
            "localizedDescription": app.get("localizedDescription", DESCRIPTION),
            "tintColor": app.get("tintColor", "#7A263A").lstrip("#"),
            "category": "utilities",
            "iconURL": app.get("iconURL", ICON_URL),
            "downloadURL": version["downloadURL"],
            "version": version["version"],
            "buildVersion": version.get("buildVersion", ""),
            "date": version.get("date", ""),
            "size": version.get("size", 0),
            "minOSVersion": version.get("minOSVersion", "16.0"),
            **({"sha256": version["sha256"]} if version.get("sha256") else {}),
        })
    pal = {
        "name": "Akatsubaki Emu",
        "identifier": "com.xthrx.akatsubaki-emu.source",
        "subtitle": source["subtitle"],
        "description": source["description"],
        "website": source["website"],
        "apps": pal_apps,
    }
    return source, pal


def main():
    response = requests.get(
        API_URL,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "Akatsubaki-Emu-AltSource/1.0"},
        timeout=(5, 20),
    )
    response.raise_for_status()
    releases = response.json()
    if not isinstance(releases, list):
        raise ValueError("GitHub releases API returned an unexpected response")

    alt_path = ROOT / "AltSource.json"
    pal_path = ROOT / "alt" / "source.json"
    existing = json.loads(alt_path.read_text(encoding="utf-8"))
    source, pal = build_sources(releases, existing)
    alt_path.write_text(json.dumps(source, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pal_path.parent.mkdir(parents=True, exist_ok=True)
    pal_path.write_text(json.dumps(pal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Akatsubaki Emu source refreshed: {len(source['apps'])} iOS app channels; "
        f"{sum(len(app['versions']) for app in source['apps'])} published versions."
    )


if __name__ == "__main__":
    main()
