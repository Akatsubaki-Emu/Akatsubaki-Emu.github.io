# Kenran Butō AOT execution ABI v1

## Scope

ABI v1 is a deliberately small x86-64-to-AArch64 execution path. It is not a general x86-64 JIT, a Linux ABI implementation, or proof that arbitrary Linux software can run.

The current translator emits only operations whose semantics are fully modelled:

- NOP
- MOV r8, imm8 (B0–B7), including AH/CH/DH/BH without REX and REX.B-extended low-byte registers
- MOV r32/r64, imm32/imm64
- register-only MOV r/m32/r/m64, r32/r64 and the reverse direction
- C7 /0 register-only MOV r/m32, imm32 and MOV r/m64, sign-extended imm32
- LEA r32/r64 with base/index/SIB addressing, scales 1/2/4/8 and signed combined displacement in the range -4095...4095
- LEA r32/r64 with no base and no index using a sign-extended disp32 constant
- RIP-relative LEA r32/r64 using the next guest instruction address plus signed disp32
- accumulator/register XCHG forms (0x90–0x97), 32/64-bit including REX.B register extension
- Register-only MOVZX/MOVSX r32/r64, r/m8/r/m16 (0F B6/B7/BE/BF with ModRM mod=3), including legacy high-byte selection without REX
- Register-only MOVSXD r64,r/m32 (0x63 with REX.W and ModRM mod=3)
- CWDE/CDQE and CDQ/CQO (0x98/0x99), including 16→32, 32→64 and sign-derived EDX/RDX results
- Register-only XCHG r/m32,r/m64 (0x87 with ModRM mod=3), including REX.R/REX.B extensions
- BSWAP r32/r64 (0F C8–CF), including REX.B-extended registers; emitted as AArch64 REV W/X

The translator stops before the first unsupported instruction and reports the exact guest-byte offset. Version 11 added MOV r8, imm8 (B0-B7), including AH/CH/DH/BH selection without REX and REX.B-extended low-byte registers; the ARM64 BFI sequence preserves all bits outside the selected byte. Version 12 adds BSWAP (0F C8–CF), mapped to AArch64 REV W/X with REX.B register extension. Version 10 added CWDE/CDQE and CDQ/CQO; 16-bit CBW/CWD forms remain interpreter-only. It does not currently emit guest memory accesses, arithmetic, branches, syscalls, privileged instructions, or SIMD. RIP-relative LEA uses the guest block RIP and signed disp32; address-size/segment overrides, memory-form XCHG, and base/index LEA displacements outside the bounded immediate subset still side-exit to the interpreter. Arithmetic flags therefore remain unchanged by translated blocks. ENDBR64 remains an interpreter side-exit until guest CET policy is explicitly implemented.

## ABI layout

All fields use the host's native little-endian layout. The C provider contains compile-time assertions for the structure sizes and the guest-register pointer offset.

### Guest state — 96 bytes on arm64

| Offset | Type | Field |
|---:|---|---|
| 0 | u32 | abi_version (must be 1) |
| 4 | u32 | struct_size (at least 96) |
| 8 | u64 pointer | gpr (16 guest registers) |
| 16 | u64 | rip |
| 24 | u64 | rflags |
| 32 | u64 | fs_base |
| 40 | u64 | gs_base |
| 48 | pointer | memory callback table |
| 56 | u64 | instruction_budget |
| 64 | u64 | instructions_executed |
| 72 | u64 | exit_rip |
| 80 | u64 | exit_address |
| 88 | u32 | exit_reason |
| 92 | u32 | reserved |

### Memory callbacks — 32 bytes on arm64

| Offset | Type | Field |
|---:|---|---|
| 0 | u32 | abi_version |
| 4 | u32 | struct_size |
| 8 | pointer | opaque guest-memory context |
| 16 | function pointer | bounded read callback |
| 24 | function pointer | bounded write callback |

The callbacks are part of the stable ABI, but the current translator does not emit guest memory operations. A callback must validate its complete range and return failure rather than exposing host pointers to guest code.

### Exit reasons

| Value | Meaning |
|---:|---|
| 0 | no exit recorded by generated code |
| 1 | unsupported guest instruction |
| 2 | truncated guest instruction |
| 3 | guest input window limit |
| 4 | instruction budget exhausted |
| 5 | translated output budget exhausted |
| 6 | end of supplied guest bytes |
| 7 | guest memory read fault |
| 8 | guest memory write fault |
| 9 | invalid ABI state |

The Swift adapter converts a normal generated-code return into the translator's stop reason, verifies exact RIP accounting, checks register/state pointers and restores the original guest registers if native invocation or validation fails.

## ARM64 block entry

The generated block is an ARM64 function receiving a pointer to KenranButoAOTGuestState in x0. Its prologue emits a BTI C landing instruction, saves the state pointer, loads the guest-register array, and maps guest registers 0–15 to host x0–x15. The epilogue stores all 16 guest registers back and returns. The translator is constrained not to use x16/x17 as guest registers.

The generated block may not call host functions or retain pointers into the Swift runtime. Memory callbacks are retained only for the synchronous invocation.

## Executable memory and JIT policy

iSteamAOTExecutableMemoryCreate accepts non-empty, four-byte-aligned code no larger than 1 MiB. It rounds the allocation to the system page size and reports the mapped size so the Swift cache accounts for real page-rounded allocations.

- Standard iOS JIT mode uses separate writable and executable aliases. The executable alias is sealed read/execute after code is copied.
- StikDebug/TXM mode obtains the executable region through the existing JIT breakpoint allocator and creates a separate writable alias.
- The provider rejects unknown protocols and unsupported platforms.
- iSteamAOTExecutableMemoryInvoke rechecks live JIT readiness immediately before every native block invocation. A failed check returns to the interpreter.
- Non-ARM64 and simulator builds report executable memory unavailable.

No writable-and-executable mapping is intentionally retained. Cache eviction and reset destroy the region through the matching VM or mmap release path.

## Interpreter cooperation

The interpreter probes the first instruction using its architectural 15-byte fetch window before it reads a larger block. A translated block is limited to the current guest page and the remaining run budget. After a normal side exit, the interpreter resumes at the exact reported RIP. Unsupported instructions are decoded by the interpreter; they are not skipped.

AOT is injected only at the Linux ELF launch boundary. Other guest-machine users keep the interpreter unless they explicitly provide an executor. When JIT is absent, the interpreter does not build or copy the AOT window.

## Cache and resource limits

The translation identity includes guest-code SHA-256, guest ABI, guest block RIP, translator version (currently 12), host architecture, CPU features, ABI version, and the instruction/input/output budgets. Cached artifacts are structurally validated and compared with a canonical translation before reuse. Cache I/O failure is an optimization miss, not an execution failure.

The executor is capped at 64 executable blocks and 16 MiB of page-rounded executable mappings. Translation is capped at 4,096 instructions, 65,536 guest bytes, and 1 MiB of emitted code. The interpreter currently supplies at most one 4 KiB guest page to a block.

## Verification

The ARM64 validation workflow compiles the C provider with warnings as errors, executes the ABI and register-preservation tests, verifies exact-RIP side exits, checks cache limits, and runs a static ELF through the hybrid interpreter/AOT path. These hosted tests are necessary but do not replace a signed physical-iPad build and a real guest boot.

Until physical-device evidence exists, the AOT path is classified as a validated implementation subset, not a complete operational emulator backend.
