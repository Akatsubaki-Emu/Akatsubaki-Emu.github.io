# QEMU iOS distribution — qualified review checklist

**Purpose:** assemble the exact technical facts and questions for a qualified licensing reviewer. This document is not a legal opinion and does not approve distribution.

## Pinned source and project licensing
- Akatsubaki Emu project license: GPL-3.0-or-later (`LICENSE`).
- UTM source used by the current runtime build: UTM 5.0.9, commit `3d4b8d8cb1ce93a8b1a9610695c12487685f0c15`, project license Apache-2.0.
- QEMU source used by the runtime workflow: UTM release archive `qemu-10.0.12-utm.tar.xz`, QEMU 10.0.12-utm. The project-level QEMU license is recorded as GPL-2.0-only; individual files can have separate SPDX exceptions and must be checked individually.
- The active QEMU native bridge currently records adaptation of UTM lifecycle/launcher material, including `Services/UTMQemuSystem.m`, `Configuration/UTMQemuConfiguration+Arguments.swift` and `QEMULauncher/Bootstrap.c`. The exact scope of that adaptation and whether it is a derivative work requires qualified review.
- The build workflow uses UTM's iOS dependency/build scripts and extracts the QEMU runtime framework plus required dependency frameworks, firmware/data. The packaged app does not include UTM's Swift VM UI. Verify the exact contents of the final app bundle rather than relying on the workflow description.

## Dependencies and distribution obligations to verify
- Produce a file-level SPDX/license inventory for every object in the QEMU framework and every embedded framework in both JIT and TCI variants. The project-level QEMU license is not sufficient to classify every source file.
- Verify the exact licenses and versions of SPICE, GStreamer, pixman, libslirp, GLib, zlib, libffi, crypto/TLS libraries and every transitive iOS-SE framework actually retained by the package.
- Inventory firmware and data shipped with the runtime (UEFI/EDK2, BIOS/VGA BIOS, device firmware, keymaps and related data) and record each source, version and license.
- Confirm source availability for the exact QEMU fork, UTM patches, project patches, build scripts and corresponding dependency sources. Record the source offer/location and the process for providing corresponding source to recipients.
- Review LGPL obligations for dynamically linked frameworks, including replacement/relinking rights and whether iOS code-signing/sideloading workflows satisfy those obligations.
- Review attribution, copyright notices, license texts, patent notices, modification notices and redistribution conditions for every component.
- Confirm whether the QEMU dynamic framework and GPL-3.0-or-later host app form one combined work for distribution purposes, and identify the license that can legally cover the combined binary.

## Specific compatibility questions
1. Does the exact QEMU linked source/object closure contain GPL-2.0-only files that are incompatible with GPL-3.0-or-later project code in the combined iOS app?
2. Do the UTM QEMU fork patches or retained iOS frameworks contain Apache-2.0-only or other terms that create additional incompatibility with GPL-2.0-only components?
3. Can the app/runtime be distributed under GPL-3.0-or-later with the exact QEMU file-level licence closure, or must particular GPL-2.0-only QEMU files be excluded/replaced or separately licensed?
4. Do any dependency or firmware licenses impose additional source, relinking, notice, patent or installation-information obligations for this sideloaded iOS distribution?
5. Does the final packaging process preserve the required notices and make the corresponding source and build instructions available to every recipient?

## Possible engineering paths — reviewer to decide
- Obtain explicit permission/relicensing from the relevant UTM copyright holders for the adapted portions, if needed.
- Replace UTM-derived app-side bridge/argument code with independently authored code based only on QEMU public APIs and command-line documentation, preserving the historical source and its Apache attribution outside the compiled target. This would not by itself clear the gate; the QEMU fork and dependency closure still require review.
- Use a runtime/source combination whose exact file-level licenses are demonstrably compatible with the project and its distribution model.
- Do not remove the gate or distribute a QEMU-enabled IPA until the reviewer has approved the exact source revision, embedded frameworks, firmware and packaging output.

## Build evidence and gate
- QEMU manual build #57, run `45969687780`, source `b8164935`: JIT/TCI dependency builds, UTM iOS archive, iOS-SE/TCTI archive and package validation succeeded. The runtime artifact upload was intentionally skipped by the licensing gate. This is compile/package validation, not a downloadable runtime or physical-device boot.
- The workflow requires `QEMU_GPL_COMPATIBILITY_REVIEW_APPROVED=true` before uploading a QEMU runtime artifact. Keep this value false/unset until the qualified review is complete. Never bypass the gate to obtain an IPA.
- Core-Only IPA Build 100, run `45970545143`, artifact `15185346993`, is unsigned and QEMU-free. It is a diagnostic guest-core build, not evidence that QEMU distribution is approved.

## Reviewer sign-off
| Field | Required record |
|---|---|
| Reviewer / organisation | Name and qualifications |
| Date and reviewed revision | Exact Git commit and source archive hashes |
| Embedded binary manifest | SHA-256 for every framework, dylib, firmware and data file |
| File-level license report | SPDX identifiers and exception/notice list |
| Combined-work conclusion | Written conclusion and permitted distribution license |
| Source/notice obligations | Exact source archive, offer, notices and delivery process |
| Conditions / exclusions | Any components or distribution channels not approved |
| Gate decision | Explicit approve / reject / needs remediation |

**Current decision: NOT APPROVED.** This is the conservative engineering gate state, not a legal conclusion about compatibility.
