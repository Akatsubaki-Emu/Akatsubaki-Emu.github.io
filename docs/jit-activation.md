# Automatic QEMU JIT activation

- **Status:** Implemented at source level; not yet verified on a physical device.
- **Scope:** General StikDebug JIT acquisition supports physical iOS 17.4+ devices. QEMU TCG specifically requires iOS 26+ and a recognised protocol (standard split-WX or TXM); simulator and Mac Catalyst are excluded from the device activation path.
- **Owner:** `JITCoordinator` coordinates helper apps and readiness; `VMDisplayViewController` gates QEMU startup; the existing QEMU native bridge and allocator own executable-region preparation.

## Startup lifecycle

1. When the user launches a VM, `LaunchSetupViewController` requests JIT through `JITCoordinator` before presenting the VM screen. It passes success/failure callbacks; `VMDisplayViewController` repeats the readiness check defensively before starting QEMU.
2. `JITCoordinator` checks the running process's actual `get-task-allow` entitlement using `SecTaskCreateFromSelf` and `SecTaskCopyValueForEntitlement` resolved from Security at runtime. If the entitlement is missing, the VM is not started.
3. The coordinator opens LocalDevVPN with `localdevvpn://enable?scheme=<bundle-id>`. The bundle ID is also registered as Akatsubaki's callback URL scheme, so stable and nightly builds can return to their own app instance.
4. LocalDevVPN submits its tunnel-start request and calls back to Akatsubaki after its own one-second delay. Akatsubaki waits a further two seconds, then opens StikDebug with the current bundle identifier and process ID using `stikdebug://enable-jit`.
5. On iOS 26+ devices with TXM/SPTM, the StikDebug request includes `script-name=universal.js`. The QEMU allocator selects the breakpoint-based executable-region protocol only when the host's hardware check reports TXM; non-TXM devices omit the script and retain QEMU's normal Darwin split-W^X allocator.
6. When Akatsubaki becomes active again, it polls the process debugger/JIT status. QEMU starts only after that state is confirmed. If the request fails or times out, QEMU remains stopped.
7. Before `qemu_init`, the native bridge resolves QEMU's exported `isteam_qemu_set_jit_callbacks` and registers three direct host callbacks: `iSteamJITIsReady`, `iSteamJITPrepareRegion`, and `iSteamJITDetach`. QEMU separately resolves only `iSteamJITIsSupported` to choose the iOS 26+ TXM path. The QEMU allocator uses the registered callbacks to prepare the executable region and invokes the detach callback after aliases are established. QEMU's detach callback remains a no-op on TXM because QEMU may request executable regions lazily throughout its lifetime. Kenran Butō AOT uses a separate one-shot 32 MiB arena: it prepares one region, creates a writable alias, then issues iSteamJITDetachPreparedArena exactly once. The AOT executor requires a live StikDebug attachment for that initial prepare; after the detach breakpoint returns, the prepared-arena state permits subsequent AOT allocations without keeping the debugger attached. The two allocators do not share arena state. This lifecycle remains unverified on a physical iPad.

## First-time setup

- Install [StikDebug](https://github.com/StikDebug/StikDebug) and [LocalDevVPN](https://github.com/jkcoxson/LocalDevVPN) separately.
- Open LocalDevVPN once and approve its VPN configuration.
- On iOS/iPadOS 27+, use StikDebug 3.2.2 or newer to pair on-device: Settings → Pair a Device → Pair iPhone or iPad, then complete the system Developer Mode pairing prompt. StikDebug saves the device-specific pairing identity automatically; no computer or manual `RPPairing` import is needed on 27+.
- On older supported iOS versions, generate a fresh device-specific `RPPairing` file with iloader and import it into StikDebug.
- When StikDebug shows its external JIT request confirmation, approve it; cancelling the request leaves QEMU stopped.
- Enable iOS Developer Mode.
- Sign Akatsubaki with a profile that preserves `get-task-allow`.
- When running inside LiveContainer, enable StikDebug's **Use LiveContainer's Bundle ID** option.

The helper apps are not embedded in Akatsubaki. They remain external dependencies and must be installed/configured by the user. The app uses LocalDevVPN's URL activation interface and StikDebug's documented JIT request interface; it does not redistribute either helper. TXM classification reads the keys at `IODeviceTree:/chosen/memory-map` through IOKit, matching StikJIT's protocol detection. A valid registry result containing `TXM` selects the StikDebug breakpoint allocator; a valid result without `TXM` selects standard split-WX. Missing, malformed, empty, or unreadable registry data is UNKNOWN and blocks QEMU startup; it is never treated as a standard device.
The **Increased Memory Limit** capability is separate from `get-task-allow`. Requesting that memory capability does not grant `get-task-allow` or make the process debuggable; the development provisioning profile must still provide `get-task-allow=true`.

The helper apps are not embedded in Akatsubaki. They remain external dependencies and must be installed/configured by the user.

## Failure handling and security

- Missing LocalDevVPN, missing StikDebug, an unavailable callback, or a missing `get-task-allow` entitlement prevents QEMU startup. The LocalDevVPN activation callback has a five-minute timeout; only one JIT acquisition may be active per process, and delayed callbacks from an expired request are ignored.
- LocalDevVPN's callback confirms that the tunnel-start request was submitted; it does **not** confirm that the VPN is connected. The readiness check is separate. If acquisition fails, verify the VPN is connected, StikDebug pairing is valid, Developer Mode is enabled, and the signing entitlement is present.
- The entitlement query uses Security task SPI. This is a sideload/developer workflow and is not suitable for App Store submission.
- The coordinator owns one foreground readiness poll and reports completion through callbacks; Launch Setup does not run a second polling loop. Every supported JIT path requires `CS_DEBUGGED`. On iOS 26+ TXM/SPTM devices, readiness additionally requires a live `P_TRACED` debugger because QEMU must complete the universal breakpoint protocol before detaching. Non-TXM devices use the normal split-W^X allocator and do not require a live debugger after JIT is enabled. A successful helper handoff alone is not treated as proof of a usable VM session.

## Build integration

- `iSteam/JITCoordinator.swift` — helper orchestration, entitlement gate, callback handling and readiness polling.
- `iSteam/JIT26Protocol.c` / `.h` — runtime signing-entitlement inspection, StikDebug TXM hardware detection, version-aware readiness, and iOS 26 breakpoint protocol entry points.
- `iSteam/Info.plist` — LocalDevVPN query permission and per-bundle callback URL scheme.
- `iSteam/AppDelegate.swift` — callback dispatch and app-activation readiness polling.
- `iSteam/LaunchSetupViewController.swift` — waits for the coordinator's success/failure callback before presenting the VM.
- `src/Display/VMDisplayViewController.swift` — repeats the readiness gate and starts QEMU only once.
- `iSteam/SettingsViewController.swift` — describes the automatic helper sequence.
- `project.yml` — links Security for the stable and nightly iOS targets.
- `scripts/patch_qemu_stikjit_ios.py` — selects the breakpoint allocator only on TXM/SPTM devices; non-TXM iOS 26 devices retain the upstream split-W^X allocator.
- `scripts/tests/test_jit_protocol.py` — source-contract regression coverage for TXM model detection, live-debugger gating, and QEMU allocator routing.
- `scripts/tests/test_jit_coordinator.py` — source-contract regression coverage.

## Validation status

- **Source readback:** completed for all changed implementation, project, settings and test files.
- **Static contract checks:** passed for the physical-device guards, entitlement lookup, LocalDevVPN and StikDebug URL construction, iOS 26 script gate, callback registration, Security linker flags, VM launch gate and source-validator contract.
- **Current validation state (2026-11-25):** GitLab main `7a06b230` and GitHub main `f2bcd957` diverge at common ancestor `8cce0419`. GitHub AOT #224, core-only IPA #10 and platform validation #861 ran on `8cce0419`. The iOS device ARM64 compile and tvOS/visionOS simulator builds passed in earlier platform run #860; AOT/core-only #224/#10 then failed at the stale Linux `exit(0)` expectation, while platform #861 failed at the unmapped mmap-hint assertion. Those test assertions are corrected on GitLab main (`bc3eab67`, `55996e0c`, `e97b25e1`) but have not been rerun. GitLab pipeline IID 1221 (ID `3112427618`) against the current main also failed before runner assignment with `ci_quota_exceeded`; earlier IID 1220, manual retries #1217/#1219 and retry #1216 were quota-blocked. No current-main IPA or physical guest execution is verified. Commit `7a06b230` makes the metrics workflow artifact-only to prevent new GitHub-only commits; it does not reconcile existing history. Do not force-push; the existing safe reconciliation workflow requires explicit owner approval.
- **Not validated on current GitLab main:** rerun of the Python/Swift suites and Xcode compilation after the GitLab-only test fixes, IPA packaging, installation, JIT activation on hardware, QEMU guest boot or persistent guest state. The earlier common-ancestor CI run passed 415 Python tests, AOT decoder/cache/arena checks and an iOS device ARM64 compile, but stopped on test assertions later corrected on GitLab main.

Do not treat source-level integration as proof of a working JIT session until a physical-device build and VM launch have been tested.


## Fail-closed TXM detection

On physical iOS 26+ devices, Akatsubaki reads `IODeviceTree:/chosen/memory-map` through IOKit, matching StikJIT's protocol detection. A valid registry result containing either `TXM` or `SPTM` selects StikDebug’s `universal.js` breakpoint protocol; a valid result containing neither selects standard JIT; unreadable, malformed, or empty registry data is UNKNOWN and blocks launch. The QEMU patcher uses the tri-state protocol export and refuses unknown devices.


## Kenran Butō AOT executable memory on TXM/SPTM devices

The iOS TXM/StikDebug AOT path now prepares one 32 MiB split-WX executable arena on first use. A single `iSteamJITPrepareRegion` request is followed by one writable `vm_remap` alias; translated blocks are allocated as host-page-aligned subranges. The current translation cache is capped at 16 MiB/64 blocks, leaving headroom for a candidate block while eviction runs. Eviction returns subranges to a coalescing, thread-safe free list; the process-lifetime arena itself is retained until process exit.

This avoids asking StikDebug to prepare a new executable region for every translated block and respects 16 KiB host-page alignment. The allocator has standalone C regression coverage for alignment, fragmentation/coalescing, exhaustion, invalid frees, overflow and concurrent allocation.

**JIT session policy:** QEMU continues to use `iSteamJITDetach` as a no-op so StikDebug remains attached for lazily created QEMU regions. Kenran Butō’s fixed 32 MiB arena uses the separate `iSteamJITDetachPreparedArena` breakpoint after its RX region and writable alias are ready. `sTXMArenaReady` records that the preallocated arena remains usable after the debugger detaches; `KenranButoAOTExecution` checks this arena-specific state rather than QEMU’s attached-session readiness. This implements the prepare/alias/detach sequence, but remains unverified on physical iPad hardware. Do not claim device-ready JIT until that test is recorded. Use StikDebug 3.2.2 or newer for TXM/JIT26 testing. On iOS/iPadOS 27+, pair on-device through Settings → Pair a Device → Pair iPhone or iPad and complete the Developer Mode prompt; StikDebug saves the pairing identity automatically. On older supported versions, create/import a fresh `RPPairing` file. Older 3.1.x sessions are not accepted as proof.

The standard non-TXM split-WX allocator remains unchanged. If the TXM arena cannot be prepared or becomes exhausted, AOT allocation fails closed and the x86-64 interpreter remains the fallback.


## StikDebug pairing recovery for iOS 26/27

Use the current [StikDebug 3.2.2 release](https://github.com/StikDebug/StikDebug/releases/tag/3.2.2) or newer for the TXM/JIT26 integration. On iOS/iPadOS 27+, pair directly on-device through Settings → Pair a Device → Pair iPhone or iPad and complete the system Developer Mode prompt; StikDebug saves the pairing identity automatically, so no computer or manual `RPPairing` import is required. On older supported versions, generate a fresh `RPPairing` file with iloader and import it into StikDebug. A passcode change or reset invalidates the pairing; repeat pairing. See the [official StikDebug pairing guide](https://github.com/StikDebug/StikDebug/blob/main/PAIRING.md).

If LocalDevVPN/StikDebug pairing still fails on older supported iOS versions with a missing `public_key` field or TLS tunnel timeout, [StikDebug issue #471](https://github.com/StikDebug/StikDebug/issues/471) records a user-reported recovery: delete StikDebug completely (do not offload it), restart the device, reinstall StikDebug, create a new pairing file, and import that file. This is a reported workaround, not a guarantee. On iOS/iPadOS 27+, use the built-in on-device pairing flow first. The interpreter smoke guest does not require JIT; this setup is only needed to validate AOT acceleration.


## Kenran Butō post-detach readiness

The 32 MiB arena is a single prepared executable region. Kenran Butō prepares that region once, creates the writable alias, then calls `iSteamJITDetachPreparedArena`. The generic `iSteamJITIsReady` and QEMU callback remain attached-session checks; the Kenran Butō allocator has its own `sTXMArenaReady` state and remains available after successful detach. If preparation or detach does not complete, AOT allocation fails closed and the interpreter remains the fallback. Physical iPadOS 27.2 validation is still required.
