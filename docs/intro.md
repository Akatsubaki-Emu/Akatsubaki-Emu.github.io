---
id: introduction
title: Akatsubaki Emu
slug: /
---

# Akatsubaki Emu

Akatsubaki Emu is an experimental emulation project for Apple platforms. Its runtime, **Kenran Butō**, combines ahead-of-time translation with interpreter fallbacks and supporting host services.

The project is under active development. Not every planned component is implemented, and building or installing the app does not prove that guest software runs on a physical device.

## What the project contains

- **Kenran Butō:** the hybrid execution architecture and its translation and interpreter paths.
- **Host-device services:** the boundary between guest execution and iOS facilities, including memory, files and process support.
- **Build tooling:** scripts and workflows used to assemble the app and its runtime dependencies.
- **Technical notes:** implementation status, compatibility limits, testing requirements and areas still being investigated.

## Getting started

- **[Installation](/docs/installation)** — install the current iOS build and review the signing requirements.
- **[User guide](/docs/user-guide)** — learn about the app's current interface and workflows.
- **[Compatibility](/docs/compatibility)** — check which parts are implemented, experimental or still planned.
- **[FAQ](/docs/faq)** — common questions about the project and its runtime.
- **[Troubleshooting](/docs/troubleshooting)** — investigate installation, file access, JIT and build problems.

## Technical documentation

### Runtime architecture

Read about [Kenran Butō](/docs/hybrid-runtime-architecture), the [host-device bridge](/docs/host-device-bridge) and the current [Windows ARM64 translation work](/docs/windows-arm64-static-translation).

### Building and releases

The [QEMU build guide](/docs/qemu-build-workflow), [release notes](/docs/releases) and [repository synchronization guide](/docs/git-sync) describe the development and distribution workflows.

## Terms used in these pages

- **AOT:** ahead-of-time translation of guest instructions.
- **TCI:** QEMU's Tiny Code Generator Interpreter, used as an interpreter-based execution path where the required runtime is available.
- **Physical-device verification:** testing on real Apple hardware. Simulator builds and source-level tests do not replace this check.

## Project links

- [Source repository](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu)
- [Releases](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases)
- [Website source on GitLab](https://gitlab.com/chantinlongxthrx/i-steam.github.io)
- [AltStore source](https://akatsubaki-emu.github.io/AltSource.json)
