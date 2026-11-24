---
id: buto-box-bundle-layout
title: Butō Box app bundle layout
description: Understand the planned IPA structure and metadata that Butō Box needs to assemble.
---

# App bundle layout and metadata

An IPA is an archive containing an iOS-family app bundle under a top-level `Payload/` directory. Butō Box intends to prepare this structure around a host app that includes Kenran Butō.

## Conceptual structure

The following is an illustrative layout, not a specification of the current Butō Box implementation:

```text
Application.ipa
└── Payload/
    └── HostApplication.app/
        ├── Info.plist
        ├── [host executable and bundled frameworks]
        ├── [app icon and resources]
        └── [guest payload directory]
            ├── application.exe
            ├── required.dll
            ├── data/
            └── assets/
```

The repository README does not yet define the final guest-payload directory name, manifest schema, or exact runtime lookup rules. Those details must be agreed between Butō Box and the Kenran Butō host before a stable package format can be considered complete.

## Preserve the guest directory tree

Do not assume that every file can be placed in one flat directory. Desktop programs often use relative paths for assets, plugins, language files and configuration. Keep the original directory structure unless the application is known to support a different layout.

## Metadata to configure

The README specifically identifies four app metadata values:

| Value | Purpose |
|---|---|
| Bundle identifier | Uniquely identifies the installed Apple app |
| Display name | Name shown by the device's launcher |
| Icon | App icon presented by the operating system |
| Launch arguments | Arguments passed to the guest launch configuration |

A future profile format should also document how it selects the guest executable, sets the working directory, and locates the payload. Those additional fields are sensible design requirements, but they are not specified in the current README.

## Signing is a separate stage

The repository lists optional `ldid` and provisioning-profile signing support on its roadmap. Until implemented and tested, do not assume Butō Box signs the resulting IPA. An unsigned or incorrectly signed archive may fail to install or launch even when its ZIP structure is valid.

See [Signing, installation and JIT preparation](./buto-box-signing).
