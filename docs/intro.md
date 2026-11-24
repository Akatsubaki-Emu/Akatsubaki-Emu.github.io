---
id: introduction
title: Introduction
slug: /
---

# Akatsubaki Emu

Akatsubaki Emu is an experimental emulator for Apple platforms. Its hybrid runtime, **Kenran Butō**, combines ahead-of-time translation with interpreter fallbacks.

This site covers installation, using the app, platform compatibility, runtime internals and development.

:::warning Development build
Akatsubaki Emu is still under development. It is not yet a general-purpose PC emulator, and support for arbitrary Windows or Linux images and Steam games is not established. Installing the app successfully does not mean guest software will run. See [Compatibility](/docs/compatibility) for the current status.
:::

## Getting started

- [Installation](/docs/installation) — install and set up the iOS app.
- [User guide](/docs/user-guide) — learn about importing files and using the library.
- [Compatibility](/docs/compatibility) — check implemented, experimental and planned features.
- [Troubleshooting](/docs/troubleshooting) — resolve common setup and runtime problems.

## About Kenran Butō

Kenran Butō is the hybrid execution architecture used by Akatsubaki Emu. It is designed to combine translated code for suitable guest instructions with interpreter execution when translation is unavailable or unsuitable.

Read the [runtime architecture guide](/docs/hybrid-runtime-architecture) for the current design and implementation status.

## Project

- [Source code](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu)
- [Releases](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases)
- [Contributing](/docs/contributing)
- [Third-party notices](/docs/third-party-notices)
