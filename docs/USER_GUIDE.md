---
id: user-guide
title: "User guide"
---

# User guide

This guide describes the current app workflows and their limits. Akatsubaki Emu is experimental; library, file-import and configuration interfaces do not prove that guest software can run.

## Install and open

1. Download the iOS IPA from the [releases page](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases).
2. Sign the unsigned IPA with a compatible sideloading method.
3. Install it using your signing tool.
4. If installation fails, follow the [installation guide](/docs/installation) and [troubleshooting guide](/docs/troubleshooting).

## Import files

Use the document picker to select files from Files or another provider. iOS file-picker access is security-scoped; selecting a file does not guarantee that it can be reopened indefinitely. Persistent access depends on creating and resolving a security-scoped bookmark.

Imported executables can be inspected for bounded PE/ELF metadata. Metadata inspection is not execution, and an imported EXE is not a working Windows game.

## Library and profiles

The library stores local metadata, favorites, tags and per-game configuration. Backup/restore uses versioned JSON metadata. Restored paths are not automatically trusted or reconnected to executable files. Artwork caching and controller/touch UI are works in progress; not every stored setting is consumed by a runtime path.

## Launching a guest

A complete full-system guest boot has not yet been verified on physical Apple hardware. QEMU is the planned full-system route; user-mode x86-64 execution and Windows compatibility are separate projects. Before treating a guest as usable, test a packaged runtime with a known-good image, display, input, shutdown, repeat launch and persistent disk state.

## Save data and external storage

VM/session configuration and save-slot metadata are prototypes. File-level access through Files is not raw USB block-device passthrough. Keep independent backups of important files and guest images.

## Controllers and keyboard

Early controller mappings and touch keyboard/gamepad interfaces exist, but complete guest input-device integration is not established. Report the device, OS version, controller model and exact input path when reporting an issue.

## Next steps

- [Installation](/docs/installation)
- [Compatibility and feature status](/docs/compatibility)
- [Troubleshooting](/docs/troubleshooting)
- [Kenran Butō architecture](/docs/hybrid-runtime-architecture)
