---
id: introduction
title: Akatsubaki Emu documentation
slug: /
---

# Akatsubaki Emu documentation

Welcome to the official Akatsubaki Emu wiki. This is the central reference for installing the app, understanding its current capabilities, building it, contributing, and following the Kenran Butō hybrid runtime.

> **Development status:** Akatsubaki Emu is experimental and is not yet a complete PC emulator. A successful build or IPA package does not prove that a guest operating system boots. See [the current runtime architecture](./HYBRID_RUNTIME_ARCHITECTURE.md) and [QEMU build status](./QEMU_BUILD_WORKFLOW.md) for verified boundaries and remaining work.

## Start here

- **[Install Akatsubaki Emu](./INSTALL.md)** — download and sign the iOS IPA, use SideStore, and troubleshoot installation.
- **[Current capabilities and port status](./DROIDDECK_PORT_STATUS.md)** — what is partial, unavailable, and still needs physical-device verification.
- **[Kenran Butō architecture](./HYBRID_RUNTIME_ARCHITECTURE.md)** — AOT, dynamic translation, routing, runtime and graphics responsibilities.
- **[Build and release channels](./RELEASES.md)** — GitHub Actions, Main/Nightly releases and artifact requirements.
- **[Contributing](./CONTRIBUTING.md)** — development setup, tests, bug reports and review expectations.

## Documentation sections

### User guides
Installation, signing, JIT setup, supported platforms, and known limitations.

### Architecture and runtime
Kenran Butō, host-device services, Windows x64 static-translation research, and the DroidDeck feature-port inventory.

### Build and maintenance
QEMU/UTM build integration, release automation, repository synchronization, and third-party notices.

## Important terminology

- **Kenran Butō (絢爛舞踏):** Akatsubaki Emu's hybrid emulation architecture.
- **AOT:** ahead-of-time translation, which translates guest instructions before execution.
- **TCI:** QEMU's tiny code generator interpreter, a possible no-JIT execution path when a compatible runtime is built and packaged.
- **Physical-device verification:** tests performed on real Apple hardware. Simulator builds and source-level tests are useful but do not replace them.

## Project links

- [Source repository](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu)
- [GitHub releases](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases)
- [GitLab website source](https://gitlab.com/chantinlongxthrx/i-steam.github.io)
- [AltStore source](https://akatsubaki-emu.github.io/AltSource.json)
