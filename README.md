# Akatsubaki Emu Website

The GitHub Pages site for Akatsubaki Emu.

## Pages

- Home: https://akatsubaki-emu.github.io/
- Xthrx's Repo: https://akatsubaki-emu.github.io/altsource/
- Combined AltStore / SideStore source: https://akatsubaki-emu.github.io/altsource/Xthrx%27s%20repo.json
- Feed health report: https://akatsubaki-emu.github.io/altsource/xthrx-source-report.json
- Project source: https://github.com/Akatsubaki-Emu/Akatsubaki-Emu

## AltSource maintenance

The candidate feed catalogue is maintained in
\`tools/xthrx-alt-source/sources.json\`. The builder and offline tests live beside
it. GitHub Actions validates the builder, fetches upstream feeds every six
hours, normalises app/version records for AltStore and SideStore, and publishes
the aggregate plus a health report under \`altsource/\`. See
[altsource/README.md](altsource/README.md) for details.

The 125 configured feed URLs are candidates, not a guarantee of availability or
compatibility. Only validated records enter the published source.
