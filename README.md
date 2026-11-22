# Akatsubaki Emu Website

Official project website and documentation wiki for Akatsubaki Emu.

- Website: https://akatsubaki-emu.github.io/
- **Documentation wiki:** https://akatsubaki-emu.github.io/docs/
- Official app source: https://akatsubaki-emu.github.io/AltSource.json
- Xthrx's Repo: https://akatsubaki-emu.github.io/altsource/
- Emulator source: https://github.com/Akatsubaki-Emu/Akatsubaki-Emu

## Documentation

The wiki is built with Docusaurus and follows the information architecture of SideStore Docs: searchable documentation, collapsible section sidebar, responsive navigation, code highlighting, and previous/next page navigation.

The complete app documentation is mirrored from the canonical application repository: installation, contribution and third-party notices; Kenran Butō hybrid runtime architecture; host-device bridge and Windows x64 → ARM64 translation research; DroidDeck port plan and status; iOS entitlements, JIT activation and tvOS guidance; QEMU/UTM build workflow, releases and Git synchronization.

The docs source lives in `docs/`; navigation is defined in `sidebars.js`; theme configuration is in `docusaurus.config.js`; custom styling and the homepage are in `src/`.

## Local development

Requires Node.js 20 or newer.

```sh
npm install
npm run start
```

Build the static website:

```sh
npm run build
npm run serve
```

The build output is generated in `build/`. The existing GitLab-to-GitHub mirror workflow builds and deploys GitHub Pages after canonical GitLab updates. The website repository remains GitLab-canonical; the application source remains GitHub-canonical.

## AltStore feeds and downloads

The static asset configuration preserves `/AltSource.json`, `/alt/`, `/altsource/`, and `/downloads/`. The release-driven feed updater remains the single writer for the official app manifests and Xthrx catalogue.

## Maintenance

Keep documentation claims aligned with verified source and device evidence. Mark prototypes, planned features and unverified runtime behavior accurately. Update the relevant wiki page whenever user-facing behavior or build steps change. Do not remove or alter the existing feed updater, mirror policy, or repository ownership.
