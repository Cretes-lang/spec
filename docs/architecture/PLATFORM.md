# 2.17 — Platform architecture

> Decision: **ARCH-PLATFORM-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-026](../requirements/CORE.md#core-026--platform-independent-semantics), [PLAT-001](../requirements/PLATFORMS.md#plat-001--published-tier-policy), [PLAT-002](../requirements/PLATFORMS.md#plat-002--tier-1-candidates), [PLAT-003](../requirements/PLATFORMS.md#plat-003--tier-2-candidates), [PLAT-004](../requirements/PLATFORMS.md#plat-004--future-platform-candidates), [PLAT-005](../requirements/PLATFORMS.md#plat-005--criteria-for-official-support), [PLAT-006](../requirements/PLATFORMS.md#plat-006--portable-behavior), [PLAT-007](../requirements/PLATFORMS.md#plat-007--explicit-platform-specific-code), [PLAT-008](../requirements/PLATFORMS.md#plat-008--cross-compilation), [PLAT-009](../requirements/PLATFORMS.md#plat-009--filesystem-and-path-portability), [PLAT-010](../requirements/PLATFORMS.md#plat-010--documented-minimum-os-versions), [PLAT-011](../requirements/PLATFORMS.md#plat-011--tier-changes), [PLAT-012](../requirements/PLATFORMS.md#plat-012--minimal-external-runtime-dependencies), [PLAT-013](../requirements/PLATFORMS.md#plat-013--toolchain-installation), [PLAT-014](../requirements/PLATFORMS.md#plat-014--consistent-toolchain-behavior-across-hosts)

## Proposed decision and rationale

**Linux x86-64 as the first proposed v0.1 target; Windows x86-64 and macOS ARM64 are subsequent Tier 1 candidates, not declared supported today.**

A target descriptor contains architecture, OS, ABI, object format, data layout, baseline CPU features, system-library requirements and minimum OS version. Host and target are distinct. Cross-compilation requires a matching sysroot/linker; the driver reports missing inputs instead of silently using host libraries.

| Candidate | Object/link/debug direction | Platform boundary |
| --- | --- | --- |
| Linux x86-64 first | ELF, system linker, DWARF | POSIX byte paths, file descriptors, epoll when async arrives |
| Windows x86-64 later | PE/COFF, compatible linker, CodeView/PDB investigation | UTF-16 OS paths, handles, process quoting, IOCP |
| macOS ARM64 later | Mach-O, system SDK/linker, DWARF | macOS path/process conventions, kqueue |
| Linux ARM64 / macOS x86-64 | Same OS adapter with target ABI validation | Later evidence-driven tier selection |
| WebAssembly / RISC-V | Dedicated host/runtime and ABI evaluation | Deferred; not implicit native compatibility |

Paths are OS-aware values, distinct from Unicode text. Preserve native path data losslessly; conversion to display text may be escaped/lossy only when labeled. Case sensitivity and normalization are filesystem properties. Environment access, file permissions, process handles, signals and terminal behavior are adapted explicitly. Portable APIs expose unsupported operations as structured errors.

A target earns support only after release builds, conformance, fault/exhaustion handling, installation/uninstallation, diagnostics and documented minimum OS versions pass on that target. Merely generating its object format is insufficient. 32-bit, mobile and bare-metal targets stay outside initial scope.

## Options, advantages, disadvantages and rejected alternatives

Simultaneous three-OS v0.1 delivery was rejected as an unvalidated capacity commitment. Linux-first reduces initial integration burden while explicit adapters preserve later portability. A portable VM-first strategy was rejected as the primary execution model. Tier promotions require evidence, not backend target listings.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: path traversal, inherited handles and target SDK provenance need validation. Performance: platform-specific fast paths may optimize but not alter semantics. DX: errors state host/target and missing SDKs. Implementation: isolate OS types at adapters and test target descriptions.

## Future verification

Later run target CI and installer tests, non-UTF paths, case collisions, process quoting, baseline CPUs, stack probes and shared-library dependency inspection.

## Risks and open questions

Minimum OS/kernel/libc versions remain unset until a tested release baseline exists. This is a release gate, not permission to claim broad support.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
