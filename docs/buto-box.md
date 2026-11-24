---
id: buto-box
title: Butō Box
description: Overview of the planned Windows and Linux application packager for Apple platforms.
---

# Butō Box

**Butō Box** is the application-packaging companion to Akatsubaki Emu. Its goal is to prepare Windows and Linux application files for use inside an Apple-platform app bundle, with the **Kenran Butō** runtime providing the guest execution layer.

> **Development status:** Butō Box is in early development and is not ready for building or general use. The workflow and capabilities described here are design goals, not a promise that an end-to-end packager is available today.

## What it is intended to do

A desktop application is more than its main executable. It may rely on adjacent data files, dynamically linked libraries, configuration files, assets, and launch arguments. Butō Box is intended to collect those inputs, combine them with a compatible host application, and produce an installable app archive.

The repository currently describes Windows `.exe` binaries and application/game directories as inputs, with iOS/iPadOS and tvOS as target platforms. The repository description also names visionOS as a target; actual support remains unverified.

## Where it fits

- **Butō Box:** prepares and packages the application payload and app metadata.
- **Kenran Butō:** the planned guest execution runtime used by the host application.
- **Apple host app:** the app installed on the device and responsible for launching the runtime.
- **Signing and installation tools:** handle signing and sideloading; they do not make an incompatible guest executable run by themselves.

See [Kenran Butō architecture](/docs/hybrid-runtime-architecture) and the [AOT execution ABI](/docs/kenran-buto-aot-abi) for the runtime-side design.

## Documentation

- [Planned packaging workflow](./buto-box-workflow)
- [App bundle layout and metadata](./buto-box-bundle-layout)
- [Signing, installation and JIT preparation](./buto-box-signing)
- [Compatibility and limitations](./buto-box-compatibility)

## Current repository roadmap

The Butō Box README lists these items as unfinished:

- [ ] Inject a base iOS/tvOS IPA stub and patch its `Info.plist`.
- [ ] Package a single `.exe` or a complete application/game directory.
- [ ] Scan for static `.dll` dependencies.
- [ ] Support per-app controller mappings and environment profiles.
- [ ] Add optional `ldid` or provisioning-profile signing support.

Do not treat any unchecked item as implemented.

## Requirements currently listed by the project

The README currently names iOS/iPadOS 17.4+ or tvOS 17.4+ and a compatible JIT enabler or debugger attachment (examples given are StikDebug, SideStore and Xcode). These are project-stated targets, not a verified compatibility guarantee for every device or payload.

## Source and feedback

- [Butō Box source repository](https://github.com/Akatsubaki-Emu/buto-box)
- [Report an issue](https://github.com/Akatsubaki-Emu/buto-box/issues)
- [Akatsubaki Emu](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu)

Butō Box is licensed under GPL-3.0; consult the repository's [LICENSE](https://github.com/Akatsubaki-Emu/buto-box/blob/main/LICENSE).
