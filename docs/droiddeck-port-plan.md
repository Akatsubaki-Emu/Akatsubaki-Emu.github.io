# DroidDeck feature-port plan

## Porting rule

DroidDeck is an Android/Linux-oriented project. Its FEX/Proton, Turnip, Gamescope, package-manager, raw USB, and Android device-access assumptions are not drop-in iOS implementations. Port features by preserving their user-facing purpose while replacing platform-specific services with Apple-platform APIs and explicitly documenting unavailable features.

## Planned feature areas

| Area | iOS approach | Current boundary |
|---|---|---|
| Library management | Local `GameStore`, query, favorites and tags | Metadata only; entries are not necessarily executable |
| Per-game profiles | Codable profile files under Application Support | Preferences persist; runtime consumption is incomplete |
| Backup/restore | Versioned JSON via Files document picker | Import validates metadata; executable paths remain untrusted |
| Artwork | App-sandboxed ImageIO cache | Local image import only; no implicit remote fetching |
| Controller input | GameController API and mapping profiles | Host callbacks and partial VNC key mapping |
| Touch gamepad/keyboard | UIKit overlays | Prototype controls; not a complete virtual HID device |
| External storage | Security-scoped URLs and bookmarks | File-level access, not raw USB block devices |
| Linux/Windows | QEMU full-system route; process translators only after integration | No complete Linux desktop or Windows game runtime |
| Graphics | Metal presentation and future translation adapters | DirectX→Vulkan→Metal not integrated |
| VR/glasses | Apple motion/display APIs where available | Prototype only; no SteamVR or vendor pose stack |

## Implementation locations

- `src/Steam/GameStore.swift`, `GameLibraryQuery.swift`, `GameRuntimeProfile.swift`, `GameArtworkStore.swift`, `DroidDeckFeatureServices.swift`
- `src/Display/ControllerInputManager.swift`, `ControllerMappingStore.swift`, `TouchGamepadView.swift`, `KeyboardOverlayView.swift`
- `src/Runtime/ExternalDriveStore.swift`, `HostDeviceBridge.swift`, `GuestBlockDevice.swift`
- `src/QEMU/` and `src/GPU/` for guest execution/display integration.

## Acceptance criteria

A feature is not marked implemented solely because a model, enum, settings row, or source file exists. Require a concrete adapter, target-platform build, and relevant device test. See [DroidDeck port status](DROIDDECK_PORT_STATUS.md).
