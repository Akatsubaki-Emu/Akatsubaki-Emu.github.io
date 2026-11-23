---
id: introduction
title: Akatsubaki Emu documentation
slug: /
---

# Akatsubaki Emu documentation

Welcome to the official Akatsubaki Emu wiki. This is the central, searchable guide to installing and using the app, understanding platform support, learning the Kenran Butō runtime architecture, building the project and contributing.

> **Development status:** Akatsubaki Emu is experimental and is not yet a complete PC emulator. It does not currently promise to boot arbitrary Windows/Linux images or run Steam games. A successful build or IPA package is not proof of guest execution on a physical Apple device.

## Start here

- **[Install Akatsubaki Emu](/docs/installation)** — download, sign and install the iOS build.
- **[User guide](/docs/user-guide)** — understand file import, the library, profiles and current launch boundaries.
- **[Compatibility](/docs/compatibility)** — see what is implemented, experimental, planned or unsupported.
- **[Frequently asked questions](/docs/faq)** — answers about emulation, JIT, platforms and contributing.
- **[Troubleshooting](/docs/troubleshooting)** — diagnose installation, file access, JIT and build issues.

## Documentation sections

### User guides

Installation, file import, library workflows, platform support, signing and JIT setup.

### Architecture and runtime

Kenran Butō, host-device services, Windows x64 static-translation research, and the DroidDeck feature-port inventory.

### Build and maintenance

QEMU/UTM build integration, release automation, repository synchronization, contributing and third-party notices.

## Important terminology

- **Kenran Butō (絢爛舞踏):** Akatsubaki Emu's hybrid emulation architecture.
- **AOT:** ahead-of-time translation, which translates guest instructions before execution.
- **TCI:** QEMU's tiny code generator interpreter, a possible no-JIT execution path when a compatible runtime is built and packaged.
- **Physical-device verification:** tests performed on real Apple hardware. Simulator builds and source-level tests do not replace them.

## Project links

- [Source repository](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu)
- [GitHub releases](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases)
- [GitLab website source](https://gitlab.com/chantinlongxthrx/i-steam.github.io)
- [AltStore source](https://akatsubaki-emu.github.io/AltSource.json)
