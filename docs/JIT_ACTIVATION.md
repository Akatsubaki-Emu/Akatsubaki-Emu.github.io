---
id: jit-activation
title: "Automatic QEMU JIT activation"
---

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
7. Before `qemu_init`, the native bridge resolves QEMU's exported `isteam_qemu_set_jit_callbacks` and registers three direct host callbacks: `iSteamJITIsReady`, `iSteamJITPrepareRegion`, and `iSteamJITDetach`. QEMU separately resolves only `iSteamJITIsSupported` to choose the iOS 26+ TXM path. The QEMU allocator uses the registered callbacks to prepare the executable region and detach after the writable/executable aliases are established.

## First-time setup

- Install [StikDebug](https://github.com/StikDebug/StikDebug) and [LocalDevVPN](https://github.com/jkcoxson/LocalDevVPN) separately.
- Open LocalDevVPN once and approve its VPN configuration.
- Import the device pairing file into StikDebug.
- When StikDebug shows its external JIT request confirmation, approve it; cancelling the request leaves QEMU stopped.
- Enable iOS Developer Mode.
- Sign Akatsubaki with a profile that preserves `get-task-allow`.
- When running inside LiveContainer, enable StikDebug's **Use LiveContainer's Bundle ID** option.

The helper apps are not embedded in Akatsubaki. They remain external dependencies and must be installed/configured by the user. The app uses LocalDevVPN's URL activation interface and StikDebug's documented JIT request interface; it does not redistribute either helper. TXM hardware classification independently follows the public model/version rules in [StikDebug's ProcessInfo+TXM implementation](https://github.com/StikDebug/StikDebug/blob/main/StikDebug/Support/ProcessInfo+TXM.swift).
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
- `scripts/patch_qemu_stikjit_ios.py` — selects the breakpoint allocator only on TXM devices; non-TXM iOS 26 devices retain the upstream split-W^X allocator.
- `scripts/tests/test_jit_protocol.py` — source-contract regression coverage for TXM model detection, live-debugger gating, and QEMU allocator routing.
- `scripts/tests/test_jit_coordinator.py` — source-contract regression coverage.

## Validation status

- **Source readback:** completed for all changed implementation, project, settings and test files.
- **Static contract checks:** passed for the physical-device guards, entitlement lookup, LocalDevVPN and StikDebug URL construction, iOS 26 script gate, callback registration, Security linker flags, VM launch gate and source-validator contract.
- **Historical, pre-migration:** GitLab pipeline `3099547557` failed before runner startup with `failure_reason=ci_quota_exceeded`; its `python-source-contracts` job had `started_at=null` and no runner assigned. GitLab CI has since been retired. Current Python source-contract and regression tests run through [GitHub Actions validation](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/actions/workflows/validate-repository.yml), while Apple-platform compilation runs through [platform validation](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/actions/workflows/validate-ios-build.yml).
- **Not tested:** Python unittest execution, Xcode compilation, IPA packaging, installation, JIT activation on hardware, QEMU guest boot or persistent guest state.

Do not treat source-level integration as proof of a working JIT session until a physical-device build and VM launch have been tested.


## Fail-closed TXM detection

On physical iOS 26+ devices, Akatsubaki reads `IODeviceTree:/chosen/memory-map` through IOKit, matching StikJIT's protocol detection. A valid registry result without `TXM` selects standard attach-only JIT; `TXM` selects the StikDebug breakpoint allocator; unreadable, malformed, or empty registry data is UNKNOWN and blocks launch. The QEMU patcher uses the tri-state protocol export and refuses unknown devices.
