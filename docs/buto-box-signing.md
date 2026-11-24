---
id: buto-box-signing
title: Butō Box signing and installation
description: Separate IPA packaging, Apple code signing, sideloading and JIT preparation.
---

# Signing, installation and JIT preparation

Packaging, signing, installation and guest execution are separate steps. A valid IPA archive is not automatically installable, and an installed host app is not proof that its guest executable can run.

> Butō Box is in early development. Its README lists signing support as roadmap work; this page explains the surrounding concepts and does not claim that Butō Box currently performs these operations.

## Packaging does not equal signing

The planned Butō Box output is an IPA assembled from a host app and a guest payload. Apple-platform installation still requires an acceptable signing and provisioning arrangement for the target device and distribution method.

The repository lists optional support for:

- `ldid`-based signing.
- Provisioning-profile signing.

Both are roadmap items in the current README. No supported signing command, certificate workflow, entitlement set, or provisioning automation is documented yet.

## Sideloading

The Butō Box README names AltStore, SideStore and Sideloadly as examples of IPA installation tools. Availability and signing behavior depend on the tool, account, certificate, device and OS version. Consult the current documentation for the tool you use.

Installing an IPA does not add missing runtime components or make an unsupported guest executable compatible.

## JIT and runtime attachment

The project README lists a compatible JIT enabler or debugger attachment, with StikDebug, SideStore and Xcode as examples. JIT availability is dependent on the device, OS, signing context and the chosen host/runtime implementation.

Do not assume that installing a JIT utility automatically enables JIT for every app. Follow the relevant tool's current instructions and confirm that the host process actually receives the execution capability it needs.

## Troubleshooting checklist

- **App will not install:** inspect the signing/provisioning status and confirm the IPA contains a valid `Payload/*.app` bundle.
- **App installs but closes immediately:** check host compatibility, required frameworks, entitlements and device logs.
- **Host opens but guest does not:** verify the guest executable path, launch arguments, working directory and payload files.
- **Guest reports missing DLLs or libraries:** check the complete application directory and dynamically loaded dependencies.
- **Guest starts only when attached to a debugger:** record the JIT/debugger setup and confirm whether the runtime requires it for that execution path.

These checks are diagnostic suggestions. They do not imply that the corresponding Butō Box features are already implemented.
