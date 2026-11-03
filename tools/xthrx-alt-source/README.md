# Xthrx's Repo on I-Steam Pages

- Configured source feeds: **125 unique URLs**
- Page: https://i-steam.github.io/altsource/
- Source JSON: https://i-steam.github.io/altsource/Xthrx%27s%20repo.json
- Feed health report: https://i-steam.github.io/altsource/xthrx-source-report.json

The GitHub Actions workflow checks the configured feeds every six hours, accepts supported AltStore/PAL JSON layouts, deduplicates apps by bundle identifier, and commits refreshed JSON here. Failed, offline, HTML-only, or incompatible feeds are listed in the report.

**Important:** 125 is the number of configured candidate URLs, not a claim that all 125 are currently live or compatible. The scheduled validator determines which sources actually contribute apps. Some sources may be duplicates, archived, rate-limited, or use non-standard formats.

Edit `tools/xthrx-alt-source/sources.json` to add or remove upstream feeds.
