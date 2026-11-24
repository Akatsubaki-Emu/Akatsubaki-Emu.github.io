---
id: buto-box-workflow
title: Butō Box packaging workflow
description: The planned steps for turning a desktop application payload into an Apple app package.
---

# Planned packaging workflow

This page expands the workflow described in the Butō Box repository README. It is a design outline only: Butō Box is not currently ready for general use, and the repository does not yet document a working end-to-end command or graphical workflow.

## 1. Prepare the input payload

The intended input is either a Windows `.exe` or a complete application/game directory. For a directory-based application, the executable may depend on files stored beside it or in subdirectories.

Before packaging, identify:

- The intended executable and its relative path.
- Data files, assets, configuration files and plugins required at launch.
- Any DLLs loaded dynamically or discovered only while the program runs.
- Required command-line arguments and working-directory assumptions.
- Whether the software expects a particular Windows or Linux environment.

A successful archive operation cannot compensate for missing dependencies or unsupported operating-system behavior.

## 2. Select a compatible host stub

The planned process starts from a base iOS/tvOS host application linked against Kenran Butō. The host is not simply a renamed desktop executable: it is the Apple-platform application that launches and coordinates the guest runtime.

The current public README does not identify a downloadable, production-ready host stub or define a stable stub interface. Treat host selection and runtime compatibility as prerequisites that still need implementation and documentation.

## 3. Place the guest files

The planned packager copies the executable and its supporting files into a payload directory inside the host app bundle. The exact final directory name and manifest format have not yet been specified by the project.

Preserve relative paths where the guest application expects them. Avoid flattening a directory tree: two different folders can contain files with the same name, and programs commonly locate assets relative to their executable or working directory.

## 4. Configure app metadata

The README names these metadata fields for patching in `Info.plist`:

- Bundle identifier.
- Display name.
- App icon.
- Launch arguments.

The bundle identifier must be unique for the installed app. Launch arguments and working-directory handling must match the guest program's expectations. The exact key names and schema for Butō Box profiles are not yet documented.

## 5. Assemble the IPA

The planned output is an IPA archive containing a correctly structured `Payload/` directory and the host application bundle. Creating an archive is only the packaging stage; it does not itself sign the app, grant entitlements, enable JIT, or validate that the guest software can execute.

## 6. Validate on a test device

Once a complete implementation exists, validate one simple payload before attempting a large game or complex desktop application. Record the device model, OS version, host build, runtime revision, signing method, JIT method, and exact launch result.

A useful test sequence is:

1. Confirm the app installs and appears with the expected name and icon.
2. Confirm the host launches without immediately closing.
3. Confirm the runtime can locate the configured guest executable.
4. Confirm required data files and libraries are found.
5. Test input, display, audio and save behavior separately.
6. Repeat after reinstalling to check whether app data persists as expected.

These are recommended validation steps, not features currently claimed by Butō Box.
