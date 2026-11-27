# Kenran Butō (絢爛舞踏) — Hybrid runtime composition

- **System name:** Kenran Butō (絢爛舞踏).
- **Status:** composable execution-policy prototype with an explicit upstream-reuse strategy. The translation-cache artifact layer, bounded x86-64 → AArch64 AOT bring-up, limited static Linux process-entry stack, and QEMU integration work exist. FEXCore, Box64, Wine, Proton and a32rt are planned reuse/port targets, not currently integrated or packaged as a working user-mode stack.
- **Component naming:** Kenran Butō AOT is a bounded static x86-64 → ARM64 translator bring-up; Kenran Butō Cache stores validated translated-code artifacts; Kenran Butō Router selects backends and fallback; Kenran Butō Runtime orchestrates execution; Kenran Butō Graphics owns graphics translation. These names do not imply that missing implementations are complete.
- **Planner:** `src/Runtime/ExecutionBackendRouter.swift`
- **Cache:** `src/Performance/TranslationCache.swift`
- **Launch entry point:** `src/Steam/GameLauncher.swift` → `src/Steam/LinuxELFRuntime` (bounded static ELF bring-up through `GuestMachine`) or `src/Runtime/WindowsRuntime.swift` (Windows path still requires a verified compatibility stack)
- **Related code:** `src/Runtime/WindowsPEImage.swift`, `src/Runtime/WindowsPELoader.swift`, `src/Runtime/X86_64Interpreter.swift`, `iSteam/Box64Bridge.*`, `src/QEMU/`, `src/Windows/`, `src/GPU/`.

## How simultaneous composition works

"Use everything simultaneously" means composing independent stages, not running every CPU emulator against the same instruction stream.

1. **AOT cache:** run validated, previously translated ARM64 code for supported guest modules/blocks.
2. **Dynamic translator:** one selected translator handles cache misses, invalidated code and runtime-generated code. FEXCore and Box64 are alternatives for a given process, not concurrent duplicate engines.
3. **Diagnostic interpreter:** only a limited bring-up fallback for instructions the translation pipeline cannot yet handle. It is not a general game compatibility engine.
4. **OS compatibility:** Windows PE loading, DLL/import handling, Win32/NT services and Wine/Proton are composed with the CPU path.
5. **Graphics:** DirectX → Vulkan → Metal is a separate pipeline and can run alongside CPU work when the required translation layers are present.
6. **Host services:** audio, input, networking and storage are orthogonal subsystems and can run alongside CPU/GPU work.
7. **Full-system fallback:** QEMU TCI/TCG remains the selected first-playable full-system route, but the current distribution gate remains closed pending qualified file-level and combined-work licensing review. Bochs 3.1 is an unselected contingency only if the QEMU gate cannot be cleared and a separate backend change is explicitly approved; its unauthenticated 8-bit RFB frontend and lack of official iOS support make it a non-drop-in port. No full-system path is verified on a physical iPad. Full-system emulation remains separate from PE process translation.
8. **Architecture-specific paths:** a32rt is only for ARM32 guests; native ARM64 is used only where the guest ABI is compatible.

## Routing policy

| Guest workload | Composition |
|---|---|
| Windows x64 PE process | AOT cache + one of Wine/Proton+FEXCore or Wine/Proton+Box64; Win32/DLL compatibility; optional DirectX→Vulkan→Metal; audio/input/network/storage services |
| Linux x64 ELF process | AOT cache + one of FEXCore or Box64; Linux syscall ABI; diagnostic interpreter only for limited bring-up |
| ARM32 Linux ELF | a32rt architecture backend; QEMU full-system where a complete OS is needed |
| Native ARM64 process | native ARM64 under a compatible ABI |
| Complete OS/kernel | QEMU TCI/TCG is the selected no-JIT first-playable path but remains distribution-gated; Bochs is an unselected contingency, not a current backend |

## Upstream reuse and porting plan

The development strategy is to reuse mature upstream implementations wherever they solve a subsystem better than a new in-house implementation. Kenran Butō owns orchestration, platform adapters, guest-state contracts, policy, validation and integration; it should not reimplement a mature CPU translator or Windows compatibility layer without a measured reason.

### Target composition

| Subsystem | Preferred upstream implementation | Role in Kenran Butō | Porting boundary |
|---|---|---|---|
| Linux x86-64 → ARM64 user-mode execution | **FEXCore** (primary candidate) | Main dynamic translation engine for Linux x86-64 processes; reuse its decoder/IR/recompiler and supported instruction implementation | FEX is designed and tested for ARM64 Linux. iOS requires a Darwin host layer, syscall/runtime boundary, signal/thread/memory integration and Apple executable-memory policy work. Do not assume upstream FEX runs unchanged on iOS. |
| Linux x86-64 compatibility alternative | **Box64** | Secondary backend for workloads where its compatibility or measured performance is better; keep behind the same process/runtime interface | Box64 is also Linux-oriented and depends on Linux process, loader, signal and library behavior. Port and package it as an alternative, not as a second translator for the same process. |
| Windows user-mode API compatibility | **Wine** | PE process environment, Win32/NT user-mode APIs, DLL loading and Windows runtime behavior | Wine is not a CPU translator. It must be paired with exactly one x86-64 execution backend and a compatible guest userspace/root filesystem. Darwin/iOS host integration and required services must be evaluated separately. |
| Windows game distribution/runtime layer | **Proton** | Optional game-focused Wine configuration, patches and components after a minimal Wine path works | Proton is built around Steam-on-Linux assumptions and a collection of separately licensed dependencies. Port only the required components; do not treat Proton as a replacement for Wine or the CPU translator. |
| ARM32 guest execution | **a32rt** | Dedicated ARM32 execution backend where the guest ABI and source project match the required workload | Verify the exact upstream repository, revision, API, supported host OS and licence before selecting or importing code. It does not replace x86-64 translation or provide a complete Linux syscall ABI by itself. |
| Whole operating system / kernel | **Bochs 3.1 (prototype candidate); QEMU TCG (license-gated)** | Full-system emulation, including booting complete guest OS images | Keep the full-system engine separate from user-mode FEX/Box64/Wine/Proton. Project-authored source is GPL-3.0-or-later; GPL-2.0-only QEMU components remain incompatible in a combined work. The UTM-derived Apache-2.0 bridge is generally compatible, but the exact bundled dependency closure still requires qualified review. Bochs needs an ARM64 iOS build and custom Metal/input frontend. |
| Static hot-block acceleration | **Kenran Butō AOT/cache** | Optional project-owned fast path for a deliberately bounded subset and validated cached translations | Avoid building a competing general-purpose translator. Keep it only where differential tests and benchmarks demonstrate value over FEXCore/Box64. |

### Execution rules

1. A process selects **one** x86-64 dynamic translator: FEXCore or Box64. Never execute the same guest thread through both.
2. Wine supplies Windows API compatibility; Proton layers game-oriented patches/configuration and selected components over Wine. Neither is a CPU emulator.
3. The selected translator, Wine/Proton layer, guest root filesystem, syscall ABI and host services must be versioned and validated as one runtime profile.
4. A full-system engine owns its complete guest machine and kernel. QEMU TCG is license-gated; Bochs is only a candidate until its iOS build and boot path are proven. Do not compose a full-system engine and FEX/Box64 as simultaneous CPU engines for the same guest process.
5. a32rt is an architecture-specific ARM32 route. Native ARM64 is used only when the guest ABI is genuinely compatible.
6. Keep the current diagnostic interpreter and bounded custom AOT translator as bring-up tools until upstream engines are built, integrated and proven. Do not silently route workloads to an unavailable backend.
7. Preserve the guest execution-context boundary so engines can be swapped without rewriting loaders, storage, display, input or application UI.

### Integration sequence — optimise for the first playable build

**Track A — first playable physical iOS guest (P0):**
1. Keep the legacy QEMU TCI/no-JIT profile as the selected no-JIT full-system route. On physical iOS arm64 this profile builds experimental TCTI via `--enable-tcg-threaded-interpreter`, not standard TCI. Do not treat the static-ELF interpreter or core-only IPA as a bootable operating system.
2. Run the pinned UTM/QEMU JIT+legacy-TCI build workflow and validate the TCI-named/TCTI runtime manifest, lifecycle exports, firmware inventory and ARM64 device binary. Verify that the arm64 build retains `--enable-tcg-threaded-interpreter`; the workflow may compile/validate internally, but runtime artifact publication remains gated.
3. Complete a qualified file-level and combined-work QEMU/UTM licensing review. Do not set `QEMU_GPL_COMPATIBILITY_REVIEW_APPROVED=true` or distribute a QEMU-linked IPA until a compatible distribution strategy is approved.
4. After approval, package the legacy TCI/TCTI runtime into a current iOS device IPA, validate its manifest and checksum, sign/install it on a physical iPad, and boot a known-good x86-64 Linux image with JIT disabled.
5. Verify VNC-to-Metal display, touch/hardware-keyboard/controller input, writable disk persistence, clean shutdown, repeat boots and cleanup. Record device/OS/build versions, image checksums, logs and a screen recording.
6. If QEMU distribution cannot be approved, evaluate Bochs 3.1 as a separate LGPL-2.1-or-later full-system alternative; first prove a headless ARM64 iOS build and Linux boot, then add Metal and input adapters. Bochs is not an integrated fallback until those tests pass.

**Track A-D — bounded Kenran Butō diagnostics (parallel, not first playable):**
1. Keep the QEMU-free core-only IPA separate from the full-system release; it must not contain QEMU libraries, firmware or manifests.
2. Import `hybrid_xchg_smoke.elf` and verify `KENRAN_BUTO_XCHG_OK` plus exit status `0`; import `hybrid_runtime_smoke.elf` and verify Linux/x86_64 output plus exit status `0`.
3. Verify deliberate XCHG failures exit nonzero, failed ELF loads clear guest memory, stop/relaunch works, and repeat launches preserve expected app/guest state.
4. Retain these tests for interpreter, GuestMemory, syscall and AOT regressions. They do not satisfy full-system OS boot acceptance.

**Track B — reusable user-mode engines (parallel after the shared interfaces are stable):**
1. Pin and audit FEXCore's upstream revision, licence and dependencies; build a minimal ARM64 host-side library harness and measure the build footprint.
2. Define the Darwin host adapter and explicit Linux guest syscall, signal, thread, memory-map, loader and filesystem contracts. Port FEXCore incrementally and run its upstream correctness tests plus differential guest tests.
3. Benchmark the existing bounded interpreter/AOT path against FEXCore before deciding which custom code remains useful.
4. Evaluate Box64 against the same Linux ELF test corpus. Integrate it only if it adds compatibility or performance that justifies a second backend.
5. Add Wine only after one x86-64 engine can run a Linux userspace reliably. Start with a small Windows console program, DLL loading and Win32 API tests before graphical applications.
6. Add Proton as an optional profile after Wine works; audit each submodule and dependency independently and port only the components that can be supported on Apple platforms.
7. Audit and integrate a32rt against a named upstream source and ARM32 test corpus; connect its Linux syscall/runtime adapter before advertising ARM32 support.

**Track C — alternate full-system backend (only if the QEMU licensing route is unavailable):**
1. Audit Bochs 3.1 source files, firmware, plugins and transitive dependencies individually; its upstream LGPL-2.1-or-later notices are promising but do not replace a complete provenance review.
2. Build an ARM64 iOS static library with `--enable-x86-64` and `--with-nogui`; prove a known-good Linux image boots headlessly before investing in UI integration.
3. Add a custom display bridge for Metal and native keyboard/gamepad/touch input. Bochs' RFB backend is diagnostic only and is not the target high-resolution display path.
4. Measure boot time, instruction throughput, guest RAM pressure, storage, suspend/resume and repeat launches on a physical iPad before selecting Bochs for Windows 10 or other full-system guests.

### Licensing, provenance and platform gates

- Project-authored source files listed in `.reuse/dep5` are GPL-3.0-or-later; upstream-derived portions and third-party components retain their own applicable licence terms. The UTM-derived QEMU bridge has Apache-2.0 provenance, generally compatible with GPL-3.0-or-later. GPL-2.0-only QEMU files remain incompatible with GPLv3 in a combined distribution. Record the exact upstream URL, commit, licence, copyright notices, modifications and transitive dependency licences for every imported component.
- FEXCore's upstream repository identifies the project as MIT-licensed and targets ARM64 Linux; Box64, Wine and Proton have their own licence terms and dependency trees. Proton's submodules must be audited individually rather than assuming the top-level licence covers every component.
- Do not copy code from an unverified project called “a32rt”: first establish the canonical repository and licence. Keep it as a candidate until that check is complete.
- Prefer linking or vendoring an unmodified upstream component with its notices where practical. Keep local iOS changes in clearly separated patch sets and preserve upstream attribution.
- A successful ARM64 compile is not proof of iOS compatibility. Each candidate must pass device-SDK compilation, dependency closure, runtime loading, guest correctness tests, memory/permission checks and physical-device validation.
- No upstream project listed in this plan is currently promoted to an operational iOS backend solely by this plan. Runtime capability registration must remain fail-closed until the concrete binary, ABI, dependencies and guest workload have been tested.

### Full-system backend licensing decision (2026-11-24)

- **QEMU:** the [official QEMU licence documentation](https://www.qemu.org/docs/master/about/license.html) identifies QEMU as GPL version 2, with individual components carrying other licences. Treat the full emulator/runtime as GPL-2.0-only unless a file-by-file audit proves a specific component is GPL-2.0-or-later or permissively licensed. The GPL-3.0-or-later project grant is generally compatible with Apache-2.0 UTM-derived material, but GPL-2.0-only QEMU components remain incompatible with GPLv3 in a combined work. Keep QEMU publication blocked until the exact source/link closure and combined-work licensing path are reviewed. The [UTM project licence](https://github.com/utmapp/UTM#license) does not relicense its QEMU source or transitive dependencies.
- **Bochs 3.1:** the [upstream licence](https://bochs.sourceforge.io/doc/docbook/user/license.html) is LGPL version 2 or later. That gives a potential GPL-3.0-compatible route by selecting a later LGPL version for files whose notices permit it; still audit every source file, firmware image and dependency before importing. The [compile guide](https://bochs.sourceforge.io/doc/docbook/user/compiling.html) requires `--enable-x86-64` for 64-bit guest support (disabled by default). The [3.1 release notes](https://bochs.sourceforge.io/get_current.html) document UEFI/OVMF support, but upstream does not document iOS as a supported host target.
- **iOS prototype boundary:** `--with-nogui` is useful for a headless ARM64 boot test but provides no production video output. A production iOS port needs a custom display frontend feeding Metal plus keyboard, gamepad and touch event adapters. Treat RFB as a diagnostic option, not the final high-resolution display path. Windows 10 boot, device compatibility and performance on an iPad remain unverified.

## What is actually integrated today

- **Translation cache:** stores versioned translated-code artifacts using a cache identity that includes guest-code SHA-256, exact guest block RIP, guest architecture, translator identity/version, host architecture, CPU features and guest ABI. Each artifact has an integrity digest, is written atomically, is rejected and removed if corrupt or mismatched, and is bounded to 8 MiB per code artifact, 512 entries and 256 MiB total. Cache entries can be explicitly invalidated. The cache itself returns validated bytes; the Linux ELF AOT execution adapter revalidates cached translations, materializes bounded ARM64 blocks through the W^X executable-memory provider, and invokes them only while live JIT readiness is present. Declined or revoked blocks fall back to the interpreter.
- **Windows PE:** `WindowsPEImage` performs bounded metadata inspection; `WindowsPELoader` is read-only inspection. No PE image mapping, executable memory, import resolver, AOT translator or Windows process execution engine is integrated.
- **Static AOT:** `X86_64AOTTranslator` currently translates a deliberately small, flag-preserving subset: NOP; MOV r8,imm8 (B0–B7, including legacy high-byte and REX.B forms); MOV r32/r64,imm32/imm64 (B8–BF); register-only MOV (89/8B); register-only C7 /0 immediate MOV; bounded base/index/SIB and guest-RIP-relative LEA; register-only MOVZX/MOVSX (0F B6/B7/BE/BF); register-only MOVSXD (0x63 with REX.W); CWDE/CDQE and CDQ/CQO (0x98/0x99); accumulator/register XCHG (0x90–0x97) and register-only XCHG (0x87); and BSWAP (0F C8–CF, including REX.B register extension). It stops at the first unsupported instruction with an exact fallback offset. `KenranButoAOTCompiler` keys and caches the validated artifact. This is not a complete decoder/IR/code generator/relinker and the executable adapter dispatches only this small subset through a versioned guest-state ABI, with exact interpreter side exits for unsupported instructions.
- **FEXCore:** not integrated or packaged.
- **Box64:** a C/Swift bridge can look for an already-loaded Box64 entry point. It does not bundle Box64, provide a Linux rootfs/syscall ABI, or prove game execution.
- **Wine/Proton:** not integrated.
- **QEMU:** `QEMURuntimeStatus.inspect(requiresJIT:)` selects the JIT or TCI library and asks the native bridge to load it with `RTLD_NOW`. Both modes require `qemu_init`, `qemu_main_loop`, `qemu_cleanup`, and `qemu_system_shutdown_request`; only JIT mode requires `isteam_qemu_set_jit_callbacks`. `RuntimeCapabilityRegistry` records a loadable library as `loadable`, not `operational`, so it cannot yet make QEMU selectable in the planner. The bridge is deliberately one-shot per app process because QEMU global-state reinitialization is not proven safe. The shared runtime uses QMP to pause and resume the same guest; generation leases prevent stale backends from stopping or resetting a newer session, and duplicate active starts are rejected. Switching configurations requires an app restart. The JIT profile uses native TCG code generation with a 128 MiB split-WX translation buffer. The legacy `TCI` profile name is retained for compatibility, but on the pinned physical iOS arm64 build UTM selects `--enable-tcg-threaded-interpreter`, so the runtime is QEMU's experimental TCTI (threaded-dispatch TCG bytecode interpreter), not standard TCI (`--enable-tcg-interpreter`). It still uses `-accel tcg` and does not require executable-memory JIT. The `QEMU/TCI` directory name alone is not evidence that standard TCI is present. The runtime workflow builds the upstream UTM `iOS` and `iOS-SE` schemes using the `ios` and `ios-tci` dependency targets, respectively; the TCI archive product is `UTM SE.app`. Both are packaged under `QEMU/JIT` and `QEMU/TCI`. A successful hosted dual-runtime build and physical guest boot remain unverified. The QEMU-free core-only diagnostic IPA always excludes QEMU. A separate full-system release IPA may embed QEMU TCI only after the full-system licensing gate above is resolved. On physical iOS 26+, the host queries `IODeviceTree:/chosen/memory-map` through IOKit and classifies the JIT protocol as UNKNOWN, STANDARD, or STIKDEBUG/TXM, matching StikJIT's query. Empty, malformed, inaccessible, or missing registry data blocks JIT launch and JIT allocation, but does not block the no-JIT TCI path. STANDARD devices retain QEMU's normal split-WX allocator; confirmed TXM devices use the exported `isteam_qemu_set_jit_callbacks` ABI to obtain the RX region, remap its RW alias, and detach the debugger. Launch Setup rejects unknown protocol modes and waits for `CS_DEBUGGED` only when the JIT profile is selected; TCI bypasses JIT readiness. `QEMUNativeRuntime` repeats the readiness check before JIT startup. Simulator, tvOS and visionOS skip the physical-iOS JIT request path. QEMU remains full-system only, not a PE process translator. Guest boot, firmware compatibility, device-level graceful stop, display/input and persistence remain unverified.
- **Linux ELF startup:** `GameLauncher` first asks `RuntimeBackendRouter` for the explicitly subset-validated interpreter route before starting `LinuxELFRuntime`, which owns a `GuestMachine`, injects the optional Kenran Butō AOT executor for the supported NOP/MOV/C7/LEA/XCHG subset, and runs bounded batches with cooperative stop; unsupported instructions side-exit to the interpreter. The capability registry labels this interpreter `validatedSubset`, not `operational`, and deliberately leaves the full `linuxSyscallABI` layer unavailable; the router permits only the bounded diagnostic subset and keeps general Linux execution false. `ELF64Loader` maps static ET_EXEC and self-contained ET_DYN PIE images, verifies program-header mapping, and applies bounded R_X86_64_RELATIVE relocations. `LinuxProcessStackBuilder` creates an aligned initial stack with argv, envp, AT_PHDR/AT_PHENT/AT_PHNUM, AT_ENTRY, AT_RANDOM and AT_EXECFN. PT_INTERP, DT_NEEDED dependencies, non-relative relocations, ELF PT_TLS initialization and a complete syscall ABI remain unsupported. Static PIE support is limited to self-contained images using R_X86_64_RELATIVE relocations; it is not a dynamic linker. The interpreter now handles ARCH_SET_FS/GS and ARCH_GET_FS/GS plus FS/GS-based memory operands; this is segment-base support, not a complete ELF TLS loader. CPUID exposes a conservative feature set (TSC, CMOV, SYSCALL, NX and long mode, without advertising unsupported SIMD), and RDTSC returns a monotonic 1 GHz virtual counter. The F3 90 PAUSE spin-wait hint is treated as a no-op. The interpreter's syscall shim currently covers stdout/stderr write and bounded writev, bounded interruptible text stdin through the console input queue, brk, anonymous mmap/munmap, mprotect/madvise validation, clock_gettime/gettimeofday, getrandom, uname (a stable virtual Linux x86-64 identity), process identity, and a small single-thread subset; it still has no guest framebuffer or guest filesystem, dynamic loader, ELF TLS initialization or full signal/thread semantics. A synthetic static ELF smoke test exercises the complete supported path from ELF loading and initial stack setup through x86-64 execution, Linux write and exit. The iOS game library now exposes imported entries and routes console launches through `GameLauncher`; this does not make dynamic ELF binaries, general Linux applications or commercial games compatible.
- **Interpreter:** diagnostic x86-64 subset with 8-bit register moves and byte memory stores with high-byte/REX semantics; byte ADD/OR/AND/SUB/XOR/CMP/TEST register/memory and immediate forms plus 32/64-bit register and memory operations; 32/64-bit memory forms of MOV/LEA/ADD/SUB/CMP/AND/OR/XOR; signed IMUL, MOVSXD and MOVZX/MOVSX byte/word extensions; ModRM/SIB base-index-scale and RIP-relative addressing (including trailing-immediate displacement bases); sign-extended immediate arithmetic; CF/PF/AF/ZF/SF/OF flags; Linux SYSCALL RCX/R11 return-state semantics; all 16 short/near conditional branches; SETcc and CMOVcc; multi-byte NOP; SHL/SHR/SAR immediate, one and CL forms; byte and wider TEST-immediate, NOT, NEG, INC and DEC; C7 immediates; direct register/immediate PUSH and register POP, LEAVE/RET-imm16, indirect CALL/JMP/PUSH, accumulator/register XCHG, and atomic memory-form XCHG 0x86/0x87 (1/4/8-byte operations through the mutex-serialized native GuestMemory API, including cross-page accesses and read/write permission checks); exact ENDBR64 (`F3 0F 1E FA`) landing-pad no-op handling for legacy execution (CET enforcement is not implemented). Other atomic read-modify-write instructions, SIMD, exceptions, paging, and most Linux syscalls remain unsupported; this is not a general game backend.
- **a32rt:** not integrated. A future Linux ARM32 ELF process route must also provide the Linux syscall ABI; the translator alone is not a launchable runtime.
- **Graphics:** Metal framebuffer presentation exists; DirectX→Vulkan→Metal guest translation is not integrated.
- **Audio/input/network/storage:** host and prototype services exist in parts, but complete guest-device adapters are not proven.

The planner's availability set must be populated only by concrete runtime probes that validate the binary, architecture, ABI, transitive libraries, required compatibility services and platform constraints. The QEMU probe now validates loadability and lifecycle exports, but the higher-level planner is not yet wired to populate availability from this probe. A source file or enum case is not proof that a backend is installed. Empty availability is deliberately safe.

## Performance policy

- Prefer native ARM64 guest code when its ABI is already compatible.
- Reuse cached AOT translations only when source hash, translator version, CPU feature set, host architecture and guest ABI match.
- Use exactly one dynamic translator per process; prefer FEX or Box64 only after compatibility and measured performance checks.
- Compile hot blocks asynchronously where permitted; never block the render/input thread for translation.
- Keep QEMU for whole-machine requirements rather than routing every simple process through it.
- Bound guest memory, translation cache growth, worker concurrency and framebuffer allocations to device capabilities.
- Keep graphics translation independent from CPU translation and use Metal-native presentation when possible.
- Record backend choice, fallback reason, cache hit/miss and startup errors in diagnostics.

## Safety and compatibility boundaries

- iOS/iPadOS sandboxing, code-signing, executable-memory/JIT entitlements, memory budgets and available APIs constrain dynamic translation.
- A Windows kernel and kernel-mode anti-cheat cannot be replaced by user-mode CPU translation. Anti-cheat support requires publisher approval for the exact environment.
- Do not disable, bypass, spoof or tamper with anti-cheat.
- A planned composition is not a working runtime. Verify physical-device boot, process launch, graphics, input/audio, shutdown and persistence before claiming compatibility.

 
## Kenran Butō AOT execution subset

The translator is now connected to a versioned ARM64 guest-state ABI, a W^X executable-memory provider, a bounded executable-block cache and interpreter side exits. ABI details and field offsets are documented in [KENRAN_BUTO_AOT_ABI.md](KENRAN_BUTO_AOT_ABI.md).

Translator version 12 emits NOP; MOV r8,imm8 (B0–B7, including AH/CH/DH/BH without REX and REX.B-extended low-byte registers); MOV r32/r64,imm32/imm64 (B8–BF); register-only MOV (89/8B); C7 /0 register-only immediate MOV (32/64-bit, including imm32 sign-extension for 64-bit destinations); bounded base/index/SIB and guest-RIP-relative LEA; register-only MOVZX/MOVSX byte/word extensions (0F B6/B7/BE/BF); register-only MOVSXD r64,r/m32 (0x63 with REX.W); CWDE/CDQE and CDQ/CQO (0x98/0x99); accumulator/register XCHG (0x90–0x97, 32/64-bit including REX.B extension); register-only XCHG (0x87, ModRM mod=3); and BSWAP (0F C8–CF, 32/64-bit including REX.B extension). XCHG uses a flag-neutral three-EOR swap without a non-guest scratch register; byte MOV preserves all unrelated register bits. ENDBR64, arithmetic, guest memory operations, branches, calls/returns, syscalls, SIMD, atomics, relocations and cross-block control flow remain interpreter fallbacks. The translated subset does not modify x86 arithmetic flags.

AOT is injected at the Linux ELF launch boundary. Generic GuestMachine instances remain interpreter-only unless an executor is explicitly supplied. The C invocation boundary rechecks JIT readiness for every block; unavailable or revoked JIT returns to the interpreter. The ARM64 workflow validates the ABI, register preservation, side-exit RIP, cache bounds and a static ELF hybrid run. This is a validated execution subset, not a general-purpose x86-64 backend or proof of physical-iPad compatibility.

## AOT decoder correctness contract

Translator version 12 enforces the x86-64 architectural 15-byte instruction limit across prefixes, opcode, ModRM and immediate. The interpreter start probe admits the full 0x90–0x97 accumulator XCHG range, including REX.B extended registers, and the flag-neutral 0x98/0x99 sign-extension forms. MOVZX/MOVSX and MOVSXD are translated inside an active AOT block; their memory forms remain interpreter fallbacks, and block-entry eligibility remains conservative. RIP-relative LEA requires the exact guest block RIP; that RIP is included in both compiler and executor cache identities so identical guest bytes at different addresses cannot alias. ENDBR64 is preserved for fallback until guest CET policy is represented. Guest-input, instruction-count and output-byte budgets stop only at instruction boundaries; unsupported and truncated instructions report the original guest offset.

The focused regression harness is scripts/tests/test_kenran_buto_aot_translator.swift. It checks AArch64 MOVZ/MOVK/BFI/REV encodings, byte-immediate MOV and high-byte preservation, C7 /0 immediates, bounded and RIP-relative LEA, 32/64-bit accumulator/register XCHG, BSWAP and REX.B high-register forms, and CWDE/CDQE/CDQ/CQO sign-extension, legal 15-byte and rejected 16-byte instructions, multi-instruction blocks, hard budget clamps, input limits, ENDBR64 fallback, unsupported/truncated boundaries and output/instruction budgets. Interpreter regressions verify XCHG block entry after an interpreter-only side exit and compare guest registers, flags and stack memory. A separate allocation-contract test guards the borrowed input buffer, fixed four-word instruction buffer and single final Data copy.

## Kenran Butō executable AOT subset

The ARM64 executable-memory provider and Swift execution adapter now connect the bounded translator to the x86-64 interpreter. The launch path injects this adapter only for Linux ELF guests; generic GuestMachine users remain interpreter-only unless they explicitly inject an executor.

The current translated subset is deliberately narrow: NOP; MOV r8,imm8 (B0–B7); MOV r32/r64,imm32/imm64 (B8–BF); register-only MOV (89/8B); C7 /0 register-immediate MOV; bounded base/index/SIB and guest-RIP-relative LEA; register-only MOVZX/MOVSX (0F B6/B7/BE/BF); register-only MOVSXD (0x63 with REX.W); accumulator/register XCHG (0x90–0x97); register-only XCHG (0x87 with ModRM mod=3); CWDE/CDQE and CDQ/CQO (0x98/0x99); and BSWAP (0F C8–CF). ENDBR64, arithmetic, guest memory operations, control flow, syscalls and all other unsupported instructions side-exit to the interpreter at the exact guest RIP. No full Linux ABI or general x86-64 compatibility is implied. Memory XCHG, arithmetic, branches, syscalls and other unsupported instructions side-exit to the interpreter.

The native ABI is versioned and size-checked. Guest registers are copied into the ARM64 call registers and written back on return. The executor validates state pointers, budgets, register state and exact byte accounting; failed native invocation restores the original registers. The C invocation boundary rechecks live JIT readiness before each block, so a revoked or unavailable JIT session falls back to interpretation.

Executable blocks use separate writable and executable mappings and are capped at 64 blocks / 16 MiB of page-rounded executable memory. The translation cache identity includes ABI and resource budgets, and cached artifacts are compared with a canonical translation before reuse. The translator uses bounded input/output budgets and a fixed four-word instruction emission buffer.

The dedicated ARM64 workflow now has ABI, memory-callback, side-exit, differential interpreter, cache-limit and static-ELF hybrid tests. These are hosted validation gates only. Physical iPad execution, JIT entitlement behavior, app signing, graphics/input, persistent guest state and repeat-launch cleanup still require device verification.

## Process-lifetime QEMU and VNC frame ownership

QEMU's native library remains a process-global, one-shot initialization. The application owns one shared QEMUNativeRuntime for the process lifetime and does not terminate the native worker when a user pauses a guest. The command line uses a private AF_UNIX QMP socket at FileManager.default.temporaryDirectory/q.sock (app-container sandbox) and intentionally omits `-no-shutdown`: when a guest completes ACPI shutdown, QEMU exits and the native worker can complete `qemu_cleanup`. The bridge allowlist accepts `stop`, `cont`, `system_reset`, `system_powerdown` and `query-status`. Stopping a VM pauses the guest; launching the same configuration resumes it with `cont` without resetting RAM. Explicit reset uses `system_reset`. Power Off sends `system_powerdown` and gives the guest 120 seconds to respond; if it does not, the runtime sends the allowlisted QMP `quit` command (falling back to the native shutdown request) so `qemu_cleanup` can release file scopes. Each successful start or resume receives a generation lease, and only the current lease can control the guest. A different VM configuration is rejected with an app-restart diagnostic rather than attempting unsafe qemu_init re-entry. Disk and firmware security scopes remain held while QEMU is active; a process-wide lifecycle monitor releases them only after the native worker has completed `qemu_cleanup`. Once QEMU exits, the one-shot runtime requires an app restart before another guest can be initialized.

VNC frames carry the QEMUVNCClient session generation from the locked framebuffer snapshot through VirtIOGPU and the Metal backend. Session replacement invalidates pending uploads, pending full-frame snapshots and published framebuffer slots. The Metal draw path rechecks both session and framebuffer generations immediately before command-buffer presentation, so work queued by an old VNC connection cannot replace the new session's frame.

The QMP and frame-generation source tests verify these lifecycle contracts. They do not replace physical iPad testing of QEMU initialization, QMP socket availability, JIT policy, guest boot, display and input, repeat launches or persistent guest state.

## iOS guest RAM and no-JIT launch budget

The iOS/tvOS Linux profile chooses a 256–1024 MB guest-RAM default from `os_proc_available_memory()`, rounded down to 256 MB steps. The budget reserves at least 512 MB or one third of the process's currently available memory for QEMU, VNC, Metal and the host UI. Windows and SteamOS profiles use a 2 GB iOS/tvOS default; non-iOS defaults remain 4 GB.

Immediately before QEMU startup, `VMConfiguration.validateForStart` rechecks current available memory. It requires guest RAM plus a host reserve of at least 512 MB or 25% of guest RAM, whichever is larger. If the budget is insufficient, launch fails with an actionable message rather than overcommitting memory and risking jetsam. The legacy TCI/TCTI no-JIT path does not require executable-memory JIT; JIT remains optional and respects the selected accelerator policy.

The available-memory API is advisory and changes during the app lifecycle; the implementation rechecks at launch rather than caching a device-wide RAM figure. See [Apple's `os_proc_available_memory` documentation](https://developer.apple.com/documentation/os/os_proc_available_memory).


## Evaluated iOS Box64 snapshot — reference only, not integrated

A third-party [BoxiOS static-library snapshot](https://github.com/cloverfield11/box64-ios-library) was inspected because Box64 is already a planned alternate user-mode backend. Its port notes identify MIT licensing, an upstream Box64 base of `2deb99ae4aa4b326819806ac2541477273244741`, and a build-126 checkpoint validated on 2026-04-27. The notes report an ARM64 static library with JIT/dynarec disabled, a MetalGL rendering bridge, and Powder Toy input/rendering at approximately 4.5–5 FPS. The port documentation reports app-linked library SHA-256 `08155073e1ac68b3dba1cd93016efbb1613b067f42576599a3e0921bbd725bbb`.

This is useful evidence that a no-JIT Box64 user-mode path can be made to execute an x86-64 ELF on iOS, but it is not a general-purpose drop-in backend:

- The tested rendering and touch path is explicitly targeted to one Powder Toy binary; the input bridge is not a generic SDL input adapter.
- The inspected iOS fork contains hard-coded guest instruction-address workarounds for that binary's LuaJIT path (including offsets around `0x69a2f5`, `0x69a31b` and `0x698c04`). These workarounds must not be transplanted into Kenran Butō.
- The CMake file defines `BOX64_EMBEDDED_IOS`, but ARM64 configuration normally enables the ARM dynarec; a reproducible interpreter-only build must explicitly disable `ARM_DYNAREC` and verify the resulting binary contains no dynarec path.
- The reported 4.5–5 FPS is a bring-up result, not a performance target. The snapshot is based on an older upstream revision and is not a substitute for an upstream-diff, dependency and physical-device audit.
- The related WiSHbox/GameHubIOS public README describes a static-ELF-on-iPhone milestone, but the inspected public repository exposed no source tree or licence file; it is a reference only and supplies no code that can be safely reused.

**Decision:** do not replace Kenran Butō or merge this game-specific fork. Keep Box64 as a secondary Linux x86-64 user-mode candidate. If evaluated further, pin and audit the full fork diff and every dependency, reproduce the no-JIT static-library build, and benchmark the same Akatsubaki smoke ELF and broader Linux test corpus on a physical iPad. FEXCore and Box64 remain alternatives for one process, never simultaneous translators for the same guest thread. This is user-mode execution, not full-system OS emulation.


Track A now includes a second static guest, hybrid_runtime_smoke.elf, which exercises uname, write and exit through the no-JIT interpreter with separate RX/RW PT_LOAD segments. Verify its Linux/x86_64 output and exit status 0 on the physical device.


See [FEXCore and Box64 iOS integration audit](FEXCORE_IOS_PORT_AUDIT.md) for the current upstream platform boundary, embedding requirements, Windows/graphics gaps and first-playable sequence.


## iOS JIT lifecycle split

On iOS 26+ hardware, either TXM or SPTM selects StikDebug `universal.js`. QEMU keeps its existing no-op detach callback because its JIT regions can be created lazily. Kenran Butō instead prepares one 32 MiB executable arena, creates its writable alias, and uses the separate `iSteamJITDetachPreparedArena` breakpoint. Its arena-ready state is independent of QEMU’s debugger-attached state. This is source-level protocol integration only; physical iPad execution, JIT revocation and interpreter fallback still require device verification.


The first TXM/SPTM prepare requires a live StikDebug attachment and a separate explicit prepare call. Availability checks are side-effect-free; after the prepared-arena detach returns, the arena-ready state is reused for subsequent AOT work.


See [Legacy feature parity and remaining requirements](LEGACY_FEATURE_PARITY.md) for the older launcher, storage, controller, keyboard, Steam, Android, VR, tvOS and visionOS requests and their current implementation boundaries.
