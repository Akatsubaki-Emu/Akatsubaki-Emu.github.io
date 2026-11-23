---
id: compatibility
title: "Compatibility and feature status"
---

# Compatibility and feature status

This page separates source-level prototypes from verified runtime support. A successful compile, simulator launch, IPA package or library import does not prove that guest software runs on a physical device.

## Platform targets

| Platform | Project target | Current status |
|---|---|---|
| iOS / iPadOS | iOS 16 deployment target | Primary development target; physical guest boot is not verified |
| tvOS | tvOS 17 deployment target | Early Siri Remote-friendly interface prototype; guest launch is not implemented |
| visionOS | visionOS 1 deployment target | App target/prototype; guest execution is not verified |

Confirm actual SDK and device compatibility against current project settings and release notes.

## Guest workload status

| Workload | Status | Boundary |
|---|---|---|
| Full Linux/Windows operating system | Not verified | QEMU full-system runtime and physical guest boot remain required |
| Static Linux x86-64 ELF subset | Experimental | Bounded loader/interpreter/syscall smoke path; not general Linux compatibility |
| Dynamic Linux ELF | Unsupported | Dynamic linker, shared libraries, full syscall ABI and TLS are incomplete |
| Windows x64 PE | Inspection only / incomplete runtime | PE metadata parsing is not a Windows translator or Win32 runtime |
| Wine / Proton | Not integrated | Windows API compatibility layers, not CPU translators |
| FEXCore / Box64 | Not operational on iOS | Linux-oriented projects require Darwin/iOS host integration and validation |
| ARM32 Linux | Not integrated | a32rt remains a gated candidate and needs a Linux ABI/runtime |
| Android | UI experiment | No working Android guest runtime |
| Steam games / anti-cheat | No compatibility promise | No commercial game or anti-cheat compatibility is established |

## Runtime components

- **Kenran Butō AOT/cache:** bounded translation research and cache artifacts exist; not a general production execution backend.
- **Interpreter:** diagnostic x86-64 instruction and syscall subset; unsupported operations must fail closed.
- **QEMU:** iOS JIT and TCI build work exists, but loadability/package evidence is not guest-boot evidence.
- **Graphics:** Metal presentation work exists; DirectX-to-Vulkan-to-Metal translation is not integrated.
- **Input/storage/networking:** host-side prototypes exist; complete guest-device adapters and persistence are not verified.

## Verification labels

- **Verified:** exact feature passed a reproducible test on the named target/device.
- **Partially verified:** limited source, host, simulator or component test passed; state the scope.
- **Experimental:** implementation exists but end-to-end behavior is not established.
- **Planned:** design or integration work is not complete.
- **Unsupported:** the project does not currently provide the feature.

See [DroidDeck port status](/docs/droiddeck-port-status), [Kenran Butō architecture](/docs/hybrid-runtime-architecture) and [QEMU build workflow](/docs/qemu-build-workflow).
