# Host-device bridge

## Purpose

`src/Runtime/HostDeviceBridge.swift` exposes limited host-side file and device metadata services to the app. It separates iOS APIs from the guest CPU implementation.

## Current interfaces

- `deviceInfo()`: reports public UIDevice model/system values and Low Power Mode state. It does not expose serial numbers or private hardware identifiers.
- `sharedDirectoryURL`: creates the app's Documents/GuestShared directory.
- `receiveFile(from:relativePath:)`: copies a selected source file into the shared directory after validating a relative path and using security-scoped, coordinated access.
- `readSharedFile(relativePath:)` and `writeSharedFile(_:relativePath:)`: access files under the shared directory. Each transfer is limited to 64 MiB; imports are checked both before and after copying, and reads stop after 64 MiB plus one byte.

## Security boundaries

Paths reject absolute paths, backslashes, and dot/dot-dot components. The final path is resolved through symlinks and checked against the resolved shared-directory root. This is a defense against accidental traversal and symlink escapes; callers should still avoid sharing attacker-controlled writable directories and should not treat path checks as a substitute for OS sandboxing.

Files-provider URLs may require security-scoped access. A URL selected once is not guaranteed to remain available indefinitely; bookmarks can become stale or providers can disconnect. Oversized files are rejected before they can consume unbounded app storage or memory.

## What is not implemented

The bridge is host-side only. No guest-visible virtio-serial, virtio-fs, 9p, or virtual-NIC RPC transport currently connects guest code to these methods. It does not expose raw USB devices or physical block devices to a guest. `GuestBlockDevice` is a host-side random-access file abstraction and is not yet attached to a QEMU guest storage controller.

## Validation

Source checks cover path resolution, security-scope use, and transfer limits. Physical-device testing must include Files-provider import/export, provider removal, stale bookmark recovery, symlink traversal attempts, and app relaunch.
