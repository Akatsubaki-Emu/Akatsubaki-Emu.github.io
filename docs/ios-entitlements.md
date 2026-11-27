# iOS memory entitlements

Akatsubaki Emu declares `com.apple.developer.kernel.increased-memory-limit` and `com.apple.developer.kernel.extended-virtual-addressing` in `iSteam/iSteam.entitlements`. A declaration in that file is only a request: the final code signature and provisioning profile must also authorize the entitlement.

## Enabling Increased Memory Limit

The iOS Settings screen includes an **Entitlements** page based on the Apple Developer Services flow used by [GetMoreRam](https://github.com/hugeBlack/GetMoreRam):

1. Set a compatible HTTPS Anisette server. The default is `https://ani.sidestore.io`.
2. Sign in with the Apple account and developer team that own the installed app's App ID.
3. Complete Apple's two-factor verification if requested.
4. Select the team containing the exact bundle ID shown by the current build (`com.xthrx.isteam` or `com.xthrx.isteam.nightly`).
5. Choose **Enable Increased Memory Limit for Akatsubaki Emu**.
6. Reinstall the app through SideStore or AltStore using the same Apple account so the installer can obtain and apply a refreshed provisioning profile.

The integration lists the selected team's App IDs to locate the exact bundle identifier of the running build, then reads that App ID's current capability list and settings. It preserves every existing capability and its settings while adding `INCREASED_MEMORY_LIMIT`. If Apple does not return a complete, readable capability list, the app stops without changing the App ID. It does not create or modify unrelated App IDs. The Anisette device identifier and provisioning data are stored in the iOS Keychain; the Apple account password is held only in memory for authentication and cleared when sign-in finishes.

## Custom capability requests

The iOS Settings → **Experiments** → **Add Anything** screen accepts a capability identifier and submits it through the same authenticated Apple Developer Services session used by the Entitlements page. The request is restricted to the App ID whose bundle identifier exactly matches the running build. Existing capability records and their settings are fetched and preserved; the requested capability is added only if it is not already present.

Apple remains the authority: unsupported, unavailable, or account-ineligible identifiers can be rejected. The input sends an empty settings array for the new capability, so capabilities requiring additional capability-specific settings may be rejected. This is not an entitlement bypass and does not change the running installation's signature. After Apple accepts a request, reinstall/re-provision through SideStore or AltStore and inspect the effective signed entitlements.

## Important limits

- The app cannot grant itself a privileged entitlement at runtime, rewrite its own code signature, or replace its installed provisioning profile from inside its sandbox.
- Apple invalidates provisioning profiles when an App ID's capabilities change. Reinstallation/re-provisioning is therefore required; see [Apple's capability guidance](https://developer.apple.com/help/account/identifiers/enable-app-capabilities).
- The account must have permission to modify the App ID, and the App ID must already exist in the selected team. This does not bypass Apple's eligibility rules for free or paid developer accounts.
- `get-task-allow` is a development-signing entitlement and is not granted by the Increased Memory Limit capability request.
- Extended Virtual Addressing remains declared in the entitlements file, but this GetMoreRam-compatible flow does not request it. Do not assume it is active until the signed app's effective entitlements and provisioning profile are inspected.
- Apple Developer Services authentication is controlled by Apple and StosSign. Authentication failures (including Apple's `-80045` response) must be surfaced rather than treated as a successful capability update.

## Validation

The source-contract test is `scripts/tests/test_entitlement_management.py`. A successful API response means Apple accepted the App ID update; it is not proof that a later installed build carries the entitlement. Verify the effective entitlements in the reinstalled app's code signature and test memory headroom on a supported physical device.


## SideStore free-team signing caveat (checked 2026-11-24)

[SideStore issue #1616](https://github.com/SideStore/SideStore/issues/1616) reports that SideStore 0.7.0 free-team signing can omit `com.apple.developer.kernel.increased-memory-limit` from the effective signed app, even after the App ID capability is enabled. The proposed [SideSign PR #4](https://github.com/SideStore/SideSign/pull/4) remains open and unmerged as of this check. The PR does not cover `com.apple.developer.kernel.extended-virtual-addressing`. If the installed SideStore build uses the affected signer, enabling the App ID capability in this screen is not proof that the installed app received it; inspect the effective signed entitlements after reinstall.

This is **not a launch blocker** for the diagnostic interpreter path. `VMConfiguration` reads `os_proc_available_memory()`, reserves host headroom and caps the Linux guest budget at 1,024 MB. Missing optional memory entitlements therefore reduces the available budget rather than making the interpreter depend on a capability the signer may drop. The JIT `get-task-allow` entitlement is separate and must still be present for StikDebug; AOT falls back to the interpreter when JIT is unavailable.
