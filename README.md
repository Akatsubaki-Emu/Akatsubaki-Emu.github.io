# I-Steam Pages

Source repository for the I-Steam website and AltStore / SideStore source.

## Repository synchronization

GitLab `chantinlongxthrx/i-steam.github.io` on `main` is the canonical source. GitHub `I-Steam/I-steam.github.io` is the public mirror.

GitHub Actions performs the recurring GitLab-to-GitHub sync. The workflow source is `.github/workflows/main.yml`; setup, permissions, reconciliation behavior, and validation notes are documented in [docs/PAGES_SYNC.md](docs/PAGES_SYNC.md).

The mirror workflow reads public GitLab without a GitLab token. It uses the repository Actions secret `MIRROR_TOKEN` (a fine-grained token with Contents and Workflows read/write access) because GitHub's built-in `GITHUB_TOKEN` cannot push updates to `.github/workflows/`. The workflow never force-pushes or writes back to GitLab. GitLab CI runners are not needed for this synchronization.

## Website contents

- `index.html` — website landing page.
- `AltSource.json`, `alt/`, and `altsource/` — AltStore / SideStore source metadata and pages.
- `downloads/` — published i-Steam IPA and checksum.
- `tools/xthrx-alt-source/` — helper for building the Xthrx AltStore source.
- `.github/workflows/` — GitHub Actions workflow sources and related automation.

See [docs/PAGES_SYNC.md](docs/PAGES_SYNC.md) before changing the mirror configuration.
