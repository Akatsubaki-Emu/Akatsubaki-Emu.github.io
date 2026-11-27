# Releases and build channels

## Source of truth

- Canonical source: [Akatsubaki-Emu/Akatsubaki-Emu](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu), branch `main`.
- GitLab mirror: [chantinlongxthrx/I-steam](https://gitlab.com/chantinlongxthrx/I-steam).
- CI/CD runs in GitHub Actions. See [Git sync policy](GIT_SYNC.md).

Do not treat a GitLab mirror commit as proof that GitHub Actions has tested the same revision. Compare commit SHAs before interpreting CI.

## Workflow layout

- `.github/workflows/validate-repository.yml`: workflow/YAML contracts, QEMU source contracts, Python regression tests, native guest-memory tests, native QEMU bridge lifecycle tests, and shell syntax.
- `.github/workflows/validate-ios-build.yml`: simulator compile validation for supported Apple platform targets.
- `.github/workflows/build-qemu-runtime.yml`: reusable/manual UTM/QEMU iOS arm64 runtime build.
- `.github/workflows/release.yml`: builds the QEMU runtime first, then app platform packages, checksums, and combined GitHub releases.
- `.github/workflows/blank.yml`: GitHub-to-GitLab synchronization. Preserve it unless the owner explicitly approves a change.

## Release channels

The release workflow supports Main and Nightly channels. Manual Main releases are accepted only when dispatched from `refs/heads/main`; Nightly remains available for test builds from other branches. Pushes to `main` are configured to produce the nightly channel; manual dispatch selects the requested channel. Nightly pushes, schedules, and manual Nightly runs share one concurrency group and queue behind an active Nightly build. Manual Main runs use a separate group, so they do not block or cancel Nightly builds. Active releases are allowed to finish before the next same-channel run starts.

The iOS app package must consume the QEMU runtime artifact produced in the same workflow run. Missing runtime artifacts, required lifecycle exports, or package contents must fail the release rather than silently producing an incomplete IPA.

## AltStore/PAL feed refresh

The official website repository owns the AltStore and PAL manifests. Its [`update-xthrx-alt-source.yml`](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu.github.io/blob/main/.github/workflows/update-xthrx-alt-source.yml) workflow reads published app releases and refreshes the official manifests and Xthrx catalogue on its schedule. The app release workflow deliberately does not write to the website repository, avoiding duplicate manifest writers and a separate cross-repository token. Feed refresh may therefore lag a newly published release until the website workflow runs.

## Required configuration

- `GITLAB_TOKEN`: used by the retained GitHub-to-GitLab sync workflow.
- GitLab-to-GitHub mirror credentials are configured in GitLab project settings and must never be committed.

## What a successful build proves

A successful YAML/source-validation job proves only the checks it runs. Simulator compilation does not prove physical-device installation. IPA packaging and checksums do not prove QEMU starts, a guest OS boots, guest input works, storage persists, or a game is compatible.

Before calling a release device-verified, record:
1. Device model and OS version.
2. Signing/install method and app version.
3. QEMU runtime revision and package checksum.
4. Known-good guest image and firmware.
5. Boot/display/keyboard/pointer/controller results.
6. Graceful stop and relaunch behavior.
7. Disk persistence after app restart.

See [QEMU build workflow](QEMU_BUILD_WORKFLOW.md) for dependency patching and link diagnostics.
