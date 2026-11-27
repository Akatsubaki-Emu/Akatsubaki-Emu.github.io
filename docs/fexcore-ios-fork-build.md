# FEXCore iOS fork build and integration boundary

**Checked:** 2026-11-27  
**Purpose:** produce a reproducible arm64-apple-ios FEXCore static-library build for later Kenran Butō integration. This is a build-validation step, not an operational guest runtime.

## Pinned source

- Repository: `https://github.com/willfaust/FEX`
- Exact commit: `1dc6ed4932bd231df1c53dd7b8043ffdee0ac34a`
- This is the FEX submodule commit pinned by `willfaust/Madeira` on its `main` tree at the time of this audit. Do not follow a moving branch.
- The fork's top-level `CMakeLists.txt` explicitly accepts `CMAKE_SYSTEM_NAME=iOS` and an arm64 host. The iOS recipe builds the FEXCore library targets, not the Linux FEX frontend.
- The repository pins transitive submodules in `.gitmodules`; CI checks them out recursively and verifies that no submodule is missing or diverged.

## Build and validation

Run on a macOS host with Xcode, CMake, Ninja and Git:

```sh
mkdir -p build/third_party
git clone https://github.com/willfaust/FEX.git build/third_party/FEX
cd build/third_party/FEX
git checkout --detach 1dc6ed4932bd231df1c53dd7b8043ffdee0ac34a
git submodule update --init --recursive
cd ../../..
FEX_SOURCE_DIR="$PWD/build/third_party/FEX" bash scripts/build_fexcore_ios.sh
```

The build is configured for `arm64-apple-ios`, the iPhoneOS SDK, the app's iOS 16 deployment floor, generic ARM64 tuning and no LTO. It builds the FEXCore and required static dependency archives, verifies every archive is arm64, checks the public context/thread API symbols, and checks an object file's Mach-O load command for the iOS platform. It packages headers, hashes, pinned submodule revisions and licence texts into `build/fexcore-ios-dist/` by default.

The `FEXCore iOS ARM64 build` workflow runs this validation on main and retains a private, seven-day artifact. The artifact is not a release and is not linked into the app yet.

## Licensing and provenance

- Upstream FEX code remains MIT licensed; preserve its copyright and `LICENSE` text.
- The inspected Madeira fork marks Madeira-authored changes as GPL-3.0-or-later and includes `LICENSE-MADEIRA.md` plus the full GPL-3.0 text. Preserve both, along with the pinned submodule provenance.
- The fork's additional Apple Metal Shader Converter permission is scoped to Madeira-authored code and does not automatically relicense Akatsubaki Emu. This build step does not include the converter or DXMT.
- Do not redistribute the combined app/runtime until the exact source/object closure and notices have been reviewed. The upstream Madeira licensing document itself identifies lawyer review and a clean-machine rebuild/relink/install check as open release requirements.

## Integration boundary

The Madeira repository's `FEXBridge.mm` is a useful API reference, not production code to copy. Its inspected proof-of-concept uses a single global context, a minimal `write`/`exit` syscall handler, a hard-coded A15 feature profile and a global `longjmp` exit path. Those choices are not safe for multiple guest processes, normal signal delivery, blocking syscalls or thread lifecycle.

Kenran Butō must retain its existing AOT translator, translation cache, diagnostic interpreter and no-JIT fallback. A future FEXCore adapter must:

1. Own one FEXCore context and thread set per guest process, with deterministic teardown.
2. Reuse or extend the existing 16-KiB-aware StikDebug W^X arena through allocator hooks; handle cache invalidation, exhaustion and JIT revocation without writable-executable pages.
3. Probe the real ARM64 host features and expose only correctly implemented guest CPUID features.
4. Route Linux syscalls through a memory-safe ABI adapter; do not pass guest pointers directly to host APIs.
5. Add guest-address-space mapping, ELF relocations/dynamic loader, TLS, signals, clone/thread lifecycle, futexes, file descriptors and filesystem semantics.
6. Side-exit unsupported instructions and unavailable JIT execution to Kenran Butō's interpreter without losing guest state.
7. Pass the same ELF, syscall, memory, stop/resume, repeated-launch and cleanup tests as the interpreter before the router can advertise FEXCore as `validatedSubset`, and pass physical iPad guest execution before `operational`.

FEXCore is a Linux x86-64 user-mode translator. It does not boot a Linux/Windows kernel and cannot replace QEMU TCI for the first full-system iOS playable milestone. Windows PE execution additionally needs Wine/Proton and Win32/NT services; graphics translation remains a separate subsystem.
