---
id: troubleshooting
title: "Troubleshooting"
---

# Troubleshooting

## The IPA will not install

- Confirm that you downloaded the iOS IPA, not the tvOS package or outer workflow artifact ZIP.
- The release IPA is unsigned. Sign it with a compatible method before installation.
- Confirm the signing method supports the device, OS version, bundle metadata and required entitlements.
- If signing fails, include the exact error from your signing tool.

## The app installs but crashes

Record the app release/commit and iOS/iPadOS version, capture the full device crash report, and note whether the failure occurs at launch or after opening a particular screen. A successful compile or package validation does not prove that the app runs on hardware.

## An imported file cannot be reopened

iOS document-picker URLs can be security-scoped. Persistent access depends on creating and resolving a security-scoped bookmark. Re-select the file in Files if access has expired, and report the provider/app if bookmark creation or resolution fails.

## A guest does not boot

A file being imported, parsed or selected does not mean a runtime is available. Confirm that a compatible QEMU runtime is packaged and that the guest image/firmware matches the selected machine configuration. A verified physical-device guest boot is not yet established.

When reporting a boot failure, include device model and OS version, app commit/release and runtime mode (TCI or JIT), guest image format and firmware source, and the first QEMU error with relevant redacted logs.

## JIT activation fails

The JIT flow depends on external LocalDevVPN and StikDebug installations, pairing, Developer Mode, a signing profile that preserves get-task-allow, and a supported device protocol.

- Verify LocalDevVPN is installed and its VPN configuration is approved.
- Verify the device pairing file is valid in StikDebug.
- Verify Developer Mode is enabled.
- Verify the installed app has the required get-task-allow entitlement.
- Approve the external JIT request and return to Akatsubaki.
- Do not treat the LocalDevVPN callback alone as proof that the tunnel is connected or JIT is ready.

QEMU's no-JIT TCI route is separate from JIT. See [automatic JIT activation](/docs/jit-activation) and [QEMU build workflow](/docs/qemu-build-workflow).

## A build or release workflow fails

Open the [GitHub Actions run](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/actions). Start with the first failed step and retain the exact compiler/linker error. A skipped, queued, cancelled or failed job is not a passing validation result.

## File a useful report

Use the [GitHub issue tracker](https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/issues). Include expected vs actual behavior, reproduction steps, device/OS, app commit, and redacted logs. Remove Apple IDs, signing credentials, private URLs, certificates and tokens before attaching files.
