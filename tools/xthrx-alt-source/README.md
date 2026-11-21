# Xthrx AltSource builder

- `sources.json` — candidate AltStore, SideStore, PAL and community feeds, including the first-party Akatsubaki Emu source. The official feed is read from the checked-out `AltSource.json` snapshot during the build, avoiding a race with GitHub Pages deployment.
- `build_xthrx_repo.py` — concurrent fetcher, JSON parser, SideStore-compatible normaliser, bounded metadata merger and report generator.
- `sync_akatsubaki_source.py` — refreshes the official Akatsubaki Emu AltStore and PAL manifests from published GitHub releases. It selects only iOS IPA assets from the canonical repository; tvOS and visionOS packages are not advertised as iOS apps. If a release channel has no valid published asset, its last known valid entry is retained rather than replaced with a broken link.
- `test_build_xthrx_repo.py` and `test_sync_akatsubaki_source.py` — offline regression tests; no upstream network calls.
- `docs/` — generated catalogue and health report, copied into `/altsource/` by GitHub Actions.

## Run locally

    python -m pip install requests
    python -m unittest -v
    python sync_akatsubaki_source.py
    python build_xthrx_repo.py

Set `XTHRX_SOURCE_URL` only when publishing at a different URL. The merger keeps only supported app/version metadata, discards arbitrary feed payloads such as embedded images, bounds descriptions and retains the 20 newest distinct versions per app. It rejects malformed download URLs, skips records without a bundle identifier or usable version, fills SideStore's required version size with zero when upstream omits it, and never writes an empty catalogue.
