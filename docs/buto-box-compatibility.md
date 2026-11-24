---
id: buto-box-compatibility
title: Butō Box compatibility and limitations
description: Target platforms, guest dependencies and current development limitations.
---

# Compatibility and limitations

Butō Box is intended to package Windows and Linux application files for Apple-platform hosts. Packaging a file does not translate every operating-system API, CPU instruction, graphics interface or driver dependency. The guest runtime must implement or provide the behavior the application expects.

## Target platforms named by the project

The Butō Box README currently lists:

- iOS/iPadOS 17.4+.
- tvOS 17.4+.
- visionOS in the repository's short description.

The README's explicit minimum-version line names iOS/iPadOS and tvOS, but does not give a visionOS minimum version or a verified device compatibility matrix. Treat visionOS support as a stated project goal until a tested build and supported workflow are published.

## Guest application factors

Compatibility can vary significantly between applications. Important factors include:

- **CPU architecture:** the guest executable's instruction set must be supported by the runtime's execution or translation path.
- **Operating-system APIs:** Windows and Linux programs may depend on system calls, services, registry behavior, filesystem semantics or APIs not present on Apple platforms.
- **Libraries:** static and dynamic dependencies must be available in a compatible form. The project's DLL dependency scanner is still listed as unfinished.
- **Graphics and audio:** desktop applications may require graphics, audio or windowing interfaces that need runtime support or adaptation.
- **Input:** mouse, keyboard, touch and controller expectations differ between desktop and mobile software.
- **Resources:** large games may require substantial storage, memory and sustained CPU/GPU performance.

A successful package build would only confirm that the archive was assembled. It would not establish that the guest program is compatible or performs acceptably.

## Current status versus planned work

| Area | Public repository status |
|---|---|
| Base IPA stub injection | Roadmap / unchecked |
| `Info.plist` patching | Roadmap / unchecked |
| Single executable packaging | Roadmap / unchecked |
| Full application directory packaging | Roadmap / unchecked |
| Static DLL dependency scan | Roadmap / unchecked |
| Per-app controller mappings | Roadmap / unchecked |
| Environment profiles | Roadmap / unchecked |
| `ldid` / provisioning signing | Roadmap / unchecked |

Update this table only when the implementation and its tests demonstrate that a feature works.

## How to report a compatibility result

When testing a payload, include:

- Application name and version.
- Whether it is a Windows or Linux build.
- Executable architecture and required dependencies, if known.
- Apple device and OS version.
- Butō Box revision and Kenran Butō host/runtime revision.
- Signing and JIT/debugger setup.
- Whether the app installed, the host launched, the guest started, and which features worked.

Separate confirmed results from assumptions. A report that says only “works” is not enough to reproduce a compatibility result.
