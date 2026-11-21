# Xthrx AltSource builder

- \`sources.json\` — 125 unique candidate feed URLs; not a live-feed guarantee.
- \`build_xthrx_repo.py\` — concurrent fetcher, JSON parser, SideStore-compatible normaliser, deduplicator and report generator.
- \`test_build_xthrx_repo.py\` — offline regression tests; no upstream network calls.
- \`docs/\` — generated catalogue and health report, copied into \`/altsource/\` by GitHub Actions.

## Run locally

\`\`\`sh
python -m pip install requests
python -m unittest -v
python build_xthrx_repo.py
\`\`\`

Set \`XTHRX_SOURCE_URL\` only when publishing at a different URL. The builder
rejects malformed download URLs, skips records without a bundle identifier or
usable version, fills SideStore's required version \`size\` with zero when
upstream omits it, and never writes an empty catalogue.
