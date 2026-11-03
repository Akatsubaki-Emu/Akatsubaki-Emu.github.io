# Xthrx's Repo on I-Steam Pages

- Page: https://i-steam.github.io/altsource/
- Source JSON: https://i-steam.github.io/altsource/Xthrx%27s%20repo.json
- Feed health report: https://i-steam.github.io/altsource/xthrx-source-report.json

The GitHub Actions workflow checks 48 candidate feeds every six hours, merges valid `apps[]` arrays, deduplicates apps by bundle identifier, and commits refreshed JSON here. Failed or incompatible feeds are listed in the report.

Edit `tools/xthrx-alt-source/sources.json` to add or remove upstream feeds.
