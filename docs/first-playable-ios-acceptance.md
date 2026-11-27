# First playable iOS acceptance and remaining feature backlog

**Last audited:** 2026-11-27 13:55 UTC  

**Scope:** Kenran Butō's first reproducible iOS guest-execution milestone. This is a checklist, not a claim that the full-system milestone has shipped. See [Legacy feature parity and remaining requirements](LEGACY_FEATURE_PARITY.md) for the older cross-chat feature requests and their current implementation status.


## Current verified snapshot — 2026-11-27 13:55 UTC

**Application main:** `9ef6bc0df9706fee50793bd5fbeeca2d9eb53388` (GitHub-to-GitLab synchronization succeeded; GitLab main was read back at the same SHA). The core-only app artifact was built from `bdcc78dafe6bcc826272fa9120826f2cc538d1b1`; the only later change to `9ef6bc0d` is FEXCore audit documentation, so the app/runtime source is identical.

- **Core-only iOS IPA: VERIFIED BUILT.** GitHub Actions run `46007119592` succeeded; artifact `15203941246` (`Akatsubaki-Emu-CoreOnly-iOS-125`, 25,434,755 bytes). IPA SHA-256: `97370b540eb2f44334db1aa51d46f8e46deebe8636c509d2977a1daa6337e5c1`; artifact ZIP SHA-256: `96fa908cde4965c5df19034cfcea1b1917729397c2e678fcc0362cb1e2740b60`. The workflow reported `BUILD SUCCEEDED` and `Core-only IPA validation: PASS`.
- **IPA inspection: VERIFIED.** Mach-O arm64; iPhoneOS SDK 27.1; `LC_BUILD_VERSION` minimum iOS 16.0; bundle ID `com.xthrx.isteam`; iPhone/iPad device families; unsigned by design; no embedded provisioning profile, code signature, QEMU, UTM or EFI payload. SideStore or another permitted signer is required.
- The artifact includes three static x86-64 Linux ELF guests: `hybrid_xchg_smoke.elf`, `hybrid_runtime_smoke.elf`, and `hybrid_stdin_smoke.elf`, with builders, tests, checksums, README and the Xcode build log. The app UI imports ELF through Library → Import Game / Executable and launches it in the diagnostic Console.
- **Kenran Butō ARM64 execution: VERIFIED ON HOSTED ARM64.** AOT run `46006971732` passed all 16 steps, including a real static ELF guest through the hybrid AOT/interpreter path and native GuestMachine stop/pause/resume smoke. Repository validation run `46007119597` also completed successfully, including Swift guest-runtime regression tests.
- **FEXCore iOS ARM64 libraries: VERIFIED BUILT, NOT INTEGRATED.** Run `46002145212`, artifact `15199106936`, pinned fork commit `1dc6ed4932bd231df1c53dd7b8043ffdee0ac34a`; seven static archives, all 154 object members independently verified as Mach-O arm64 with iOS `LC_BUILD_VERSION`. Artifact SHA-256: `8183ad9c600c3182dab7280d997567755a8479a51c09e8ada692432044f3df58`. No FEXCore bridge, syscall adapter or guest-memory integration is yet linked into the app.
- **QEMU full-system build: IN PROGRESS.** Build & Release run `46007119653` is compiling UTM dependencies for physical iOS arm64. No TCI runtime artifact or QEMU-enabled IPA is yet available. The QEMU distribution gate remains closed pending qualified file-level and combined-work licensing approval.
- **Physical iPad execution: NOT YET VERIFIED.** The unsigned IPA is ready for SideStore installation and the three ELF guests are packaged, but no on-device install/launch/interactive result is claimed. Full-system Linux boot, Windows execution, guest graphics/input/audio, persistent disk and repeat-launch device evidence remain open.

The current diagnostic build makes Akatsubaki theoretically usable for the bounded static x86-64 Linux ELF subset. It is not a full PC/OS emulator and does not satisfy the first-playable QEMU TCI physical-device acceptance gate.

## Validation automation

Changes to this acceptance checklist trigger both the QEMU-free core-only iOS build and the Kenran Butō AOT validation workflow. The AOT workflow uses matching `push` and `pull_request` path filters; a regression test checks that those lists stay identical and that the allocation hot-path test is included in both.

These hosted checks validate source contracts, native/Swift execution harnesses, and the unsigned physical-device ARM64 build. They do **not** prove signing, installation, JIT activation, or guest execution on a physical iPad; those remain explicit device acceptance gates below.

## Selected first-playable route: QEMU TCTI (no JIT; legacy profile name TCI)

The first playable physical-iOS guest is a known-good x86-64 Linux image booted through the full-system QEMU TCTI (threaded-dispatch TCG bytecode) interpreter. The project retains the historical TCI profile and directory identifiers for compatibility, but the pinned physical iOS arm64 build selects `--enable-tcg-threaded-interpreter`. This no-JIT route does not require StikDebug, TXM, executable-memory entitlements, or a JIT pairing. The app's automatic acceleration mode may use JIT when available and fall back to TCTI; the explicit QEMU interpreter mode selects the no-JIT variant directly.

The custom `LinuxELFRuntime` and its two static ELF guests are diagnostic user-mode tests for Kenran Butō's interpreter/GuestMachine path. They are valuable regression tests, but they are **not** a bootable Linux OS and do not satisfy the first-playable emulator milestone. The separate core-only IPA workflow intentionally excludes QEMU and is diagnostic only.

The repository has a manual QEMU runtime build workflow for JIT and TCI variants and a release workflow that embeds the combined runtime. The release workflow is gated by `QEMU_GPL_COMPATIBILITY_REVIEW_APPROVED=true`; do not set this variable until qualified file-level and combined-work licensing review is complete. Without approval, the workflow may compile/validate but does not publish the QEMU runtime artifact or QEMU-enabled IPA.

## Current implementation boundary

The repository now contains:

- A bounded static x86-64 Linux ELF loader and Linux initial-stack builder.
- A bounded Linux syscall subset including `uname`, `write`, `exit`, memory-management calls and an interruptible 64 KiB guest-stdin queue for `read(0, ...)`, surfaced by the diagnostic console input field.
- \`GuestMachine\` orchestration with the x86-64 interpreter and native C-backed guest memory, including non-destructive pause/resume of blocked stdin reads without clearing guest state.
- A partial x86-64-to-ARM64 AOT translator, translated-code cache, backend routing, and interpreter fallback.
- Atomic memory-form XCHG for 1-, 4-, and 8-byte operands through a mutex-serialized native guest-memory API, including cross-page accesses and permission checks.
- Conservative CPUID feature reporting and a monotonic 1 GHz virtual RDTSC counter; unsupported instructions still fall back to the interpreter.
- A 96 MiB process-lifetime TXM executable arena for StikDebug-backed AOT memory, with exact-allocation tracking, coalescing, and concurrency regression tests. The shared dual-map allocator API is exposed for a future FEXCore bridge; FEXCore's seven iOS ARM64 static libraries are now built and verified, but they are not linked or operational.
- An application import-to-launch route through \`LibraryViewController\`, \`ConsoleViewController\`, \`GameLauncher\`, \`LinuxELFRuntime\`, and \`GuestMachine\`.

This is a real, bounded execution path, not a complete PC emulator. It does not yet provide dynamic ELF linking, arbitrary Linux userland, a bootable Linux/Windows OS, a production graphics pipeline, or complete guest input.

### Historical source snapshot (2026-11-27 13:35 UTC; superseded by the current verified snapshot above)

- GitLab `main` was verified at `4596d94561b6182700dd9b8c0f5fd43d0de4d529`. At the last cross-remote comparison, GitHub `main` was a two-commit fast-forward descendant; the intervening changes were limited to the validation assertion and GuestMachine comments. GitLab API rate limiting prevented confirmation of mirror synchronization after that comparison.
- The native GuestMachine smoke harness now covers repeated static-ELF execution, asynchronous stdin, stop while blocked in `read(0)`, and pause/resume while preserving guest memory and retrying the same syscall. The harness is wired into the Kenran Butō AOT validation workflow, but no current-head Xcode-runner result or physical-iPad result is recorded.
- The latest recorded GitLab pipeline 1347 failed before runner allocation with `ci_quota_exceeded` on the preceding `76c4011d` commit; it did not validate `4596d945`. The native C/Swift smoke source and the executable-arena stress harness therefore remain unverified on the current head.
- No current-head IPA, physical iPad installation, physical AOT/JIT execution, QEMU TCI runtime package, or full-system guest boot is claimed. The QEMU distribution gate remains closed pending qualified file-level and combined-work licensing review.


## Acceptance gates

### Gate 1 — Reproducible QEMU-free core-only diagnostic iOS build

- [ ] Run the core-only iOS workflow against the current GitLab \`main\` source.
- [ ] Confirm the workflow compiles the physical-device ARM64 target and produces the expected unsigned IPA.
- [ ] Record the source commit, workflow run, IPA checksum, bundle identifier, and effective entitlements.
- [ ] Sign and install the IPA on a physical iPad using a supported signing path.
- [ ] Confirm the app launches repeatedly without a simulator-only dependency.

This QEMU-free IPA validates the custom ELF/interpreter path only. It is a diagnostic build, not the first playable VM or a full-system guest.

### Gate 2 — Physical static-ELF diagnostic (not first playable)

Use the two diagnostic guests produced by \`scripts/build_hybrid_xchg_smoke_elf.py\` and \`scripts/build_hybrid_runtime_smoke_elf.py\`.

- [ ] Import \`hybrid_xchg_smoke.elf\` through Files and launch it through the application UI.
- [ ] Confirm \`KENRAN_BUTO_XCHG_OK\` and exit status 0.
- [ ] Import \`hybrid_runtime_smoke.elf\` through Files and launch it through the application UI.
- [ ] Confirm \`Linux\`, \`x86_64\`, and \`KENRAN_BUTO_RUNTIME_OK\`, followed by exit status 0.
- [ ] Repeat both launches after returning to the library and after restarting the app.
- [ ] Confirm stopping a guest releases guest-memory pages and does not leave stale runtime state.
- [ ] Record device model, iPadOS version, app build, guest checksums, logs, and a short screen recording.

Host-side ELF execution, Swift regression tests, and IPA packaging are not substitutes for this physical-device gate.

### Gate 3 — AOT/JIT correctness on device

- [ ] Use StikDebug 3.2.2 or newer for TXM/AOT validation. On iOS/iPadOS 27+, pair on-device through Settings → Pair a Device → Pair iPhone or iPad and complete the Developer Mode prompt; no computer or manual `RPPairing` import is required. On older supported versions, generate/import a fresh `RPPairing` file.
- [ ] Verify the installed app has the required effective \`get-task-allow\` entitlement.
- [ ] Verify the JIT protocol mode and TXM arena are available on a supported physical device.
- [ ] Execute representative AOT blocks and compare register, memory, flag, and exit results against the interpreter.
- [ ] Revoke JIT readiness during execution and confirm AOT fails closed and interpreter fallback continues safely.
- [ ] Verify repeated arena allocation, eviction, and reuse without stale executable mappings.

The AOT path is optional for the first QEMU TCI guest. TCI does not require StikDebug or JIT. StikDebug pairing and JIT are required only to validate the optional accelerated user-mode path.

### Gate 4 — QEMU TCTI display and input validation

- [ ] Connect the guest execution path to a guest framebuffer and a Metal-backed display.
- [ ] Route touch, hardware keyboard, and controller input into guest input events.
- [ ] Verify pause/resume, focus changes, orientation, and clean shutdown.
- [ ] Verify the Power Off action sends an ACPI power-button event and that a supported guest OS completes shutdown cleanly.
- [ ] Apply guest resolution and frame-rate settings to the actual renderer rather than only storing UI preferences.

For QEMU TCTI, validate the existing VNC-to-Metal display and keyboard/controller event path on the physical device. The iOS display exposes a Power Off action that sends QMP `system_powerdown`. The QEMU command line omits `-no-shutdown` so a guest that completes ACPI shutdown exits QEMU and triggers native cleanup; if the guest ignores ACPI, a 120-second QMP `quit` fallback requests native cleanup; an unsaved guest state may be lost after the forced exit. Both paths still require physical validation. Hardware-keyboard key-down/up/cancel forwarding and F-key/HID mappings are implemented in main; physical focus, key-up and guest delivery still need verification. The separate static ELF console remains text-only and has no independent framebuffer; it now has a bounded, interruptible guest-stdin queue and a text input field for diagnostic programs.

### Gate 5 — Persistent QEMU guest disk state

- [ ] Implement a guest disk/block-device path with documented image formats.
- [ ] Persist guest writes across app restarts.
- [ ] Add save slots/snapshots with corruption-safe writes and recovery.
- [ ] Verify cleanup and repeat launches do not erase persistent guest data.

QEMU has a disk-image path, but write persistence across physical-device restarts, crash-safe snapshots, USB passthrough, and external-drive controller semantics still require device validation.

### Gate 6 — First playable: QEMU TCTI full-system Linux boot (P0)

- [ ] Complete the qualified file-level and combined-work QEMU/UTM licensing review.
- [ ] Run the manual QEMU runtime build workflow and verify the `ios-tci` / `iOS-SE` TCI variant and its runtime manifest.
- [ ] Only after the licensing review, set `QEMU_GPL_COMPATIBILITY_REVIEW_APPROVED=true` and run the release workflow that embeds the QEMU TCI runtime into the iOS app.
- [ ] Confirm the resulting device IPA contains the TCI runtime, passes the runtime manifest and IPA validators, and has a recorded SHA-256.
- [ ] Sign/install the IPA on a physical iPad through SideStore or another supported path.
- [ ] Boot a known-good x86-64 Linux image through QEMU TCI with JIT disabled.
- [ ] Verify VNC-to-Metal display, keyboard/controller input, virtual-disk writes, clean shutdown, and repeat boots.
- [ ] Confirm ACPI shutdown waits for native QEMU cleanup, releases security-scoped disk/firmware URLs, reports the guest as powered off, and requires an app restart before another guest can start.
- [ ] Record device model, iPadOS version, app/TCI runtime versions, image checksums, logs, and a short screen recording.

QEMU TCI is the selected first playable no-JIT route. The manual build workflow can compile and validate TCI/JIT variants, but the release workflow intentionally withholds QEMU runtime artifacts and QEMU-enabled IPA packaging until the licensing approval variable is set after review. Bochs remains a research alternative, not an integrated or verified replacement.

## iOS signing and JIT prerequisites

- The interpreter smoke path must work without JIT and must size guest memory using available host memory.
- SideStore free-team signing may omit optional increased-memory entitlements from the effective installed signature; enabling an App ID capability is not proof that the installed app received it. Inspect effective entitlements after reinstall.
- \`get-task-allow\` is a separate requirement for StikDebug JIT. Missing JIT must disable AOT execution safely and preserve interpreter fallback.
- See [iOS memory entitlements](IOS_ENTITLEMENTS.md), [JIT activation](JIT_ACTIVATION.md), and [core-only iOS test build](CORE_ONLY_IOS_TEST_BUILD.md).

## Remaining features from older project requests

These items remain outside the first QEMU TCI Linux-boot milestone and should be implemented only after the physical guest path is stable.

| Area | Requested capability | Current boundary / missing work |
|---|---|---|
| Windows | Windows 10 guest, EXE installation and execution | PE metadata inspection is not a Windows kernel, Win32 API, dynamic translator, Wine, or Proton runtime |
| Linux | General Linux applications and dynamic ELF files | Dynamic loader, shared libraries, broader syscall/ABI coverage, and full-system boot are missing |
| Steam | In-app Steam Store and library/game launch integration | The tvOS Store action is an explanatory prototype; a functional Steam client/session is not integrated |
| Storage | Persistent VM disks, save slots, external drives and USB | Needs a real block-device layer, image management, snapshots, and device passthrough |
| Graphics | Guest framebuffer, Metal rendering, 3D translation | Current display experiments are not a complete guest graphics backend |
| Input | Touch gamepad, movable/resizable controls, pointer lock, motion, hardware keyboard and F-key bar | Touch and hardware-keyboard routing exist in source; physical focus/guest delivery, pointer lock, motion mapping and per-game profiles still need verification |
| Display | Custom resolution, FPS limits, 60/120 Hz selection | Must be connected to the real renderer and guest timing, not only UI settings |
| Controllers | Physical gamepads, sticks, buttons and controller mapping | Needs a tested host-to-guest input translation layer |
| Android | Android guest experiment | UI selection only; no Android execution backend |
| VR / visionOS | VR mode, motion input, visionOS support | Prototype/build-target work; no verified guest VR rendering or interaction |
| tvOS | Apple TV guest launch and controller support | Interface prototype; no verified OS boot or game launch |
| Dynamic translation | FEXCore/Box64 or another general x86-64 dynamic backend | FEXCore iOS ARM64 static libraries now build and are verified; no integrated, benchmarked runtime backend yet; interpreter remains correctness fallback |
| UTM/QEMU | Full-system emulation backend | QEMU TCI is the selected no-JIT first-playable route; current UTM/QEMU iOS arm64 build is in progress, but the GPL compatibility gate, distributable TCI artifact, QEMU-enabled IPA and physical Linux boot remain unverified |
| Vapour Emu | Evaluate after its expected release | Date and availability are unverified; development must not wait for it |

## Historical repository/CI coordination snapshot (2026-11-26; superseded by the current verified snapshot above)

GitLab `main` is `bd6b9207768cf38990f554563c13545ad59e84a7`; GitHub `main` is `71ee9407bb4cc491e6d0d2188c00574d183c2a67`, three commits behind. The GitLab-only commits update GitHub CI coverage and refresh these acceptance/feature documents. No reverse sync or force-push has been attempted.

### Current source changes (2026-11-26)

- `efbdf480` — reload the AOT guest-register-array pointer from preserved `x17` after using `x16` as scratch; byte-register AL/AH/R8B preservation regression coverage.
- `c095723d` and `158481af` — iOS 17 keyboard-layout API availability guard for the iOS 16 deployment target and guest stdin lock-scope assertion.
- `b26079cc` — preserve the iOS/tvOS SteamOS 2 GiB / 2-vCPU profile; keep desktop 4 GiB / 4-vCPU defaults and add platform-specific UI/test coverage.
- `fdc4c21c` — align QEMU BIOS fixture paths and release-channel source-contract assertions with the current packaging layout.
- `e1660af8` — isolate the complete TCI framework/dependency closure under `Frameworks/TCI`, rewrite loader-relative runpaths, re-sign modified Mach-O files and test versioned frameworks/symlinks.
- `3418baa0` — correct the AOT byte-XCHG hybrid test to expect the supported MOV prefix to execute in AOT before interpreter side-exit.
- `033c62d8` and `08ab0ae0` — route hardware keyboard key-down/up/cancel events to QEMU/VNC with HID mappings, F-keys, modifiers and key cleanup.
- `7a151691` — historical project-authored GPL-2.0-or-later declaration; superseded on 2026-11-27 by GPL-3.0-or-later for files listed in `.reuse/dep5`.
- `71ee9407` — enforce strict JIT/TCI callback-export parity in native validation and startup; add a fake JIT-library rejection test for TCI and run native bridge tests in GitLab CI.
- `e9cf8f87` — add the TCI mismatch case to GitHub's native bridge workflow and assert both CI definitions remain aligned.

### Historical hosted and local validation evidence (2026-11-26; superseded by the current verified snapshot above)

- Native ARM64 AOT validation completed successfully after the byte-XCHG hybrid block-count assertion was corrected in `3418baa0`. This verifies the hosted ARM64 test path, not physical iOS JIT/AOT execution.
- The QEMU TCI dependency-isolation synthetic suite was recorded as 17/17 passing locally after `e1660af8`. It does not replace `otool -L`/load-command closure checks, `codesign --verify`, on-device `dlopen`, or a guest boot.
- The native QEMU bridge now rejects a JIT callback export when TCI is requested and rejects a missing callback when JIT is requested. The C harness covers JIT success, TCI success and TCI-with-JIT-export rejection. GitLab CI and the GitHub validation workflow are wired to run these cases.
- GitLab pipeline IID 1303 (commit `71ee9407`), IID 1304 (same commit) and IID 1305 (commit `e9cf8f87`) all failed before runner assignment with `ci_quota_exceeded`; no tests ran on the new bridge-parity changes.
- GitHub repository validation run `45842731799`, platform compile run `45842731803` and core-only IPA run `45842731853` are pending without assigned runners. Build & Release run `45842732055` is queued. No IPA artifact or platform build result is available.
- GitLab `main` is `bd6b9207768cf38990f554563c13545ad59e84a7`; GitHub `main` is `71ee9407bb4cc491e6d0d2188c00574d183c2a67`, three commits behind. The GitLab-only commit updates the GitHub validation workflow and its source-contract test; no reverse sync or force-push has been attempted.
- The project-authored source files listed in `.reuse/dep5` are GPL-3.0-or-later (commit `7f85bbb8`). The QEMU file-level and combined-work audit remains incomplete; `QEMU_GPL_COMPATIBILITY_REVIEW_APPROVED=true` must remain unset until qualified review.
- No current QEMU TCI runtime artifact, QEMU-enabled IPA, SideStore installation or physical iPad Linux boot is verified.

### Runtime and older-feature boundary

The custom `LinuxELFRuntime` is a bounded diagnostic user-mode path. It is not a full-system OS emulator: `read(0, ...)` is backed by a bounded, interruptible stdin queue and ConsoleViewController text input, but it has no independent framebuffer contract.

FEXCore and Box64 are not operational iOS dynamic backends. Dynamic ELF/PT_TLS, broad Linux syscall/thread/signal support, Windows PE/EXE execution, Wine/Proton, full-system graphics/audio beyond the QEMU display path, save snapshots, USB passthrough, and Android/VR/tvOS/visionOS guest execution remain separate milestones.

### Required next actions

1. Run the manual QEMU runtime build workflow and validate the no-JIT TCI variant. It can compile/validate without publishing the runtime artifact.
2. Complete a qualified file-level and combined-work QEMU/UTM licensing review. Do not set `QEMU_GPL_COMPATIBILITY_REVIEW_APPROVED=true` before that review.
3. After approval, run the release workflow to embed the TCI runtime and produce a current physical-device iOS IPA.
4. Sign/install on a physical iPad and boot a known-good x86-64 Linux image through QEMU TCI with JIT disabled.
5. Verify VNC-to-Metal display, keyboard/controller input, disk persistence, clean stop, repeat boot, and cleanup; record logs and checksums.
6. Keep the QEMU-free core-only IPA and static ELF guests as separate diagnostic coverage for Kenran Butō's interpreter, guest memory, syscall and AOT paths.
7. After the first physical TCI boot, continue broader dynamic translation, Windows, Steam, snapshots, audio, and additional platform work.

A core-only IPA, static ELF host execution, simulator build, or QEMU compile alone does not satisfy the first-playable physical-device acceptance gate.

## Definition of done

The first playable physical iOS milestone is complete only when a reproducible current-source IPA containing the approved QEMU TCI runtime is installed on a physical iPad, a known-good x86-64 Linux image boots through TCI with JIT disabled, guest display and keyboard/controller input work, guest disk state survives restarts, repeat boots and cleanup are reliable, and build/test/device evidence is recorded. A QEMU-free core-only IPA, static ELF diagnostic, host execution, simulator run, or successful QEMU compilation alone is insufficient.

## Historical source status (2026-11-26)

QEMU TCTI is the selected first-playable no-JIT full-system route (legacy internal profile name TCI). It does not require StikDebug or TXM. The custom interpreter/static-ELF path is diagnostic coverage and remains useful as a correctness fallback. The 32 MiB TXM/SPTM arena and JIT path are optional acceleration work after TCI boot is proven; StikDebug 3.2.2+ is required for the iOS/iPadOS 27+ TXM/AOT pairing tests. No physical TCI boot or physical JIT/AOT execution is verified.



## Historical source and packaging status (2026-11-26)

GitLab `main` is `bd6b9207768cf38990f554563c13545ad59e84a7`; GitHub `main` is `71ee9407bb4cc491e6d0d2188c00574d183c2a67`, three commits behind. No force-push or reverse sync has been attempted.

- The AOT guest-register-pointer correction and byte-XCHG hybrid block-count test correction are in main; hosted ARM64 AOT validation passed. Physical iOS JIT/AOT execution remains unverified.
- QEMU TCI dependency isolation is in main: the complete TCI framework tree is packaged separately, loader-relative runpaths are rewritten, modified Mach-O files are re-signed, and versioned framework/symlink cases are tested. Local synthetic merger tests were recorded 17/17 passing.
- Hardware keyboard key-down/up/cancel forwarding and F-key/HID mappings are in main. Physical keyboard focus and guest delivery remain unverified.
- Native QEMU bridge parity is in GitLab main: JIT must export the StikJIT callback and TCI must not. The GitLab C-test job covers both valid modes and the TCI-with-JIT-export rejection case. GitHub's workflow invocation is updated in the GitLab-only follow-up commit.
- GitLab pipelines IID 1303–1305 failed before runner assignment with `ci_quota_exceeded`. GitHub validation/platform/core-only IPA runs remain pending without assigned runners. No current IPA or QEMU runtime artifact exists.
- The QEMU publication gate remains closed. The project-authored GPL-3.0-or-later grant does not establish compatibility of GPL-2.0-only QEMU files or every bundled dependency in the combined distribution. Complete the qualified file-level and combined-work audit before enabling the gate.
- First physical-device target remains a 1 GiB x86-64 Linux guest through QEMU TCI with JIT disabled, VNC-to-Metal display, keyboard/controller/touch input, persistent disk, clean shutdown and repeat boot. No physical iPad guest boot is verified.

