# Xthrx's Repo

Combined AltStore / SideStore source built from public feeds listed in
[tools/xthrx-alt-source/sources.json](../tools/xthrx-alt-source/sources.json).

- Website: https://akatsubaki-emu.github.io/altsource/
- Source JSON: https://akatsubaki-emu.github.io/altsource/Xthrx%27s%20repo.json
- Feed health: https://akatsubaki-emu.github.io/altsource/xthrx-source-report.json
- Configured inputs: 125 unique HTTP(S) candidate feeds

The six-hour GitHub Actions job fetches each candidate independently, accepts
recognised AltStore / SideStore / PAL JSON layouts, normalises app and version
metadata, deduplicates by exact bundle identifier, and retains distinct version
downloads. It publishes a health report showing accepted and failed feeds,
valid and rejected app counts, and per-feed errors.

The configured count is not a live-feed claim. A candidate contributes apps only
when it returns parseable JSON containing compatible app records. The builder
will not overwrite the published catalogue with an empty result.

## Maintenance

Edit \`tools/xthrx-alt-source/sources.json\` to add, remove or rename feed inputs.
Run offline tests with:

\`\`\`sh
cd tools/xthrx-alt-source
python -m unittest -v
\`\`\`

The workflow installs the only runtime dependency (\`requests\`) and runs tests
before contacting upstream feeds. Generated output is written under
\`tools/xthrx-alt-source/docs/\` and copied into this Pages directory.

Upstream app metadata and downloads remain controlled by their publishers.
Review each app, its signing requirements and permissions before installing it.
