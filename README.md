# Akatsubaki Emu Website

Static project website for Akatsubaki Emu, published through GitHub Pages.

## Pages

- Home: https://akatsubaki-emu.github.io/
- Xthrx's Repo: https://akatsubaki-emu.github.io/altsource/
- Combined AltStore / SideStore source: https://akatsubaki-emu.github.io/altsource/Xthrx%27s%20repo.json
- Feed health report: https://akatsubaki-emu.github.io/altsource/xthrx-source-report.json
- Main project source: https://github.com/Akatsubaki-Emu/Akatsubaki-Emu

## Site files

- `index.html` — project landing page, navigation, development status, and links to source/builds.
- `altsource/index.html` — Xthrx's Repo landing page and source-install instructions.
- `AltSource.json` — the project's own app source.
- `altsource/` — generated combined catalogue and feed-health report.
- `tools/xthrx-alt-source/` — configured candidate feeds, catalogue builder, regression tests, and maintenance notes.
- `docs/PAGES_SYNC.md` — GitLab-to-GitHub Pages mirror workflow and validation notes.

The site uses static HTML and CSS only; it has no JavaScript runtime, framework, external font, or build dependency. Layouts are responsive and keep the public source URLs unchanged.

## AltSource maintenance

The candidate feed catalogue is maintained in `tools/xthrx-alt-source/sources.json`. The builder and offline tests live beside it. GitHub Actions validates the builder, fetches upstream feeds every six hours, normalises app/version records for AltStore and SideStore, and publishes the aggregate plus a health report under `altsource/`.

The configured feed URLs are candidates, not a guarantee of availability or compatibility. Only validated records enter the published source. See [altsource/README.md](altsource/README.md) for details.
