---
id: faq
title: "Frequently asked questions"
---

# Frequently asked questions

## Is Akatsubaki Emu a working PC emulator?

Not yet. It is an experimental Apple-platform game-library and guest-runtime project. It does not currently promise to boot arbitrary Windows/Linux images or run Steam games. See [compatibility](/docs/compatibility).

## Can I install the IPA directly from Files?

No. The published IPA is unsigned. Sign it with a compatible sideloading method before iOS can install it. Follow the [installation guide](/docs/installation).

## Does importing an EXE mean I can run it?

No. Import and PE metadata inspection do not execute the file. A working Windows runtime requires a CPU translation backend, Windows API/DLL compatibility, a guest userspace and other services.

## Does the app support Linux?

There is a bounded static Linux ELF bring-up path and a planned QEMU full-system route. Neither means general Linux desktop or commercial game compatibility. A physical-device guest boot has not been established.

## What is Kenran Butō?

Kenran Butō (絢爛舞踏) is the project's hybrid execution architecture. It coordinates AOT/cache, a selected dynamic translator, interpreter fallback, OS compatibility, graphics and host services. Planned components are not automatically operational.

## Is FEXCore or Box64 included?

No operational iOS FEXCore or Box64 backend is currently advertised. They are candidates for future integration and require platform-specific porting, licensing review and correctness testing.

## Does JIT work automatically?

The app has a source-level JIT coordination flow using external LocalDevVPN and StikDebug helper apps. It is not physically verified. QEMU's JIT path has stricter platform/protocol requirements than the no-JIT TCI path. Read [automatic JIT activation](/docs/jit-activation).

## Does tvOS launch games?

No. The tvOS target is currently an interface prototype. Its session/store/settings actions do not boot an operating system or launch games.

## Where can I report a bug?

Use the [GitHub issue tracker](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/issues). Include app version/commit, device and OS version, reproduction steps, and relevant redacted logs. Never publish Apple IDs, certificates, provisioning profiles, tokens or private keys.

## How can I contribute?

Start with [Contributing](/docs/contributing). For upstream integrations, include exact revision, licence, dependencies and attribution requirements.
