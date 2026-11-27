# tvOS status and roadmap

## Current target

The XcodeGen target `iSteamTV` is a separate tvOS application using `tvOSApp/` and `iSteam/Info-tvOS.plist`. It is a Siri Remote-friendly interface prototype, not the iOS VM runtime.

The current `project.yml` declares tvOS 17.0 as its deployment target. The tvOS app does not currently share the iOS VM runtime source set, and its Launch session, Steam Store, and Settings actions present explanatory prototype notices.

## Current limitations

- No QEMU guest boot is wired into the tvOS target.
- No Windows/Linux game execution is integrated.
- The current tvOS UI is not a Steam client and does not authenticate with Valve.
- iOS signing, JIT, file-provider access, controller APIs, and display behavior cannot be assumed to work identically on tvOS.
- A tvOS IPA package is not proof of installability on every Apple TV model or installer.

## Build and validation

Generate the project with XcodeGen:

```sh
bash scripts/prepare-app-icons.sh
xcodegen generate --spec project.yml
```

Select the `iSteamTV` target/scheme in Xcode or use the GitHub Actions platform compile workflow. Verify the deployment target and entitlements in the generated project before release.

## Next milestones

1. Keep the tvOS prototype clearly separated from unsupported runtime controls.
2. Add UI tests for Siri Remote focus and navigation.
3. Verify app lifecycle, storage and network permission behavior on a physical Apple TV.
4. Only integrate QEMU after the iOS runtime has a proven boot/display/input/shutdown lifecycle and a separate tvOS feasibility review.
