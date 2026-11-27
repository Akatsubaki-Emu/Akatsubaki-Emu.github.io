# DroidDeck port status

This status reflects the source-level readiness inventory in `src/Steam/DroidDeckFeatureServices.swift`. It is not a physical-device test report.

## Partial

- Library management: local metadata, favorites and query are present; game execution is not implied.
- Per-game profiles: settings can be persisted; active runtime consumption is incomplete.
- Library backup: versioned JSON import/export exists; executable paths are metadata and are not reconnected automatically.
- Document-picker import: file selection/copy flows exist; persistent provider access can still fail.
- Controller input: GameController callbacks and mappings exist; complete guest-device input is not established.
- Touch gamepad: host UI prototype; not a complete guest HID device.
- Performance targets: resolution/FPS preferences and diagnostics exist; guest rendering may not honor them.
- External storage bookmarks: file-level security-scoped access exists; raw USB block-device passthrough does not.
- SteamOS gaming profile: profile/configuration exists; no SteamOS image is bundled.

## Unavailable

- Linux desktop boot and Flatpak/AppImage execution.
- Wine/Proton Windows compatibility.
- FEXCore runtime on iOS.
- Turnip Vulkan driver integration.
- Frame generation.
- SteamVR.
- Vendor-specific glasses pose tracking.
- Raw USB block-device passthrough.
- Verified full-system QEMU guest boot.

## Verification required

1. Build the iOS target and install on a physical supported device.
2. Test library import, backup/restore and artwork replacement.
3. Test controller connect/disconnect and touch-control transitions.
4. Boot a known-good Linux image through the packaged QEMU runtime.
5. Verify display protocol, keyboard, pointer and controller input.
6. Verify stop/cleanup, relaunch constraints and persistent disk state.
7. Update this page only with linked commit, CI and device-test evidence.

Do not describe Akatsubaki Emu as a working Windows/Steam game emulator until the Windows runtime, compatibility layers, and physical game tests exist.
