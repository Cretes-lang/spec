# 2.11 — Backend strategy

> Decision: **ARCH-BACKEND-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[DX-014](../requirements/CORE.md#dx-014--debugger-support), [PERF-001](../requirements/PERFORMANCE.md#perf-001--self-contained-executables), [PERF-005](../requirements/PERFORMANCE.md#perf-005--toolchain-responsiveness), [PERF-009](../requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput), [PERF-012](../requirements/PERFORMANCE.md#perf-012--artifact-size), [PLAT-002](../requirements/PLATFORMS.md#plat-002--tier-1-candidates), [SEC-027](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds)

## Proposed decision and rationale

**One initial LLVM native backend behind a target-neutral MIR adapter; alternate backends require later evidence.**

Use the backend for instruction selection, register allocation, object emission and established target optimizations. Cretes retains ownership of language semantics, layout decisions, checks, cleanup and diagnostic identity. The adapter consumes verified MIR plus an explicit target description and emits objects/debug data; it does not expose backend objects in frontend APIs.

LLVM is proposed because the long-term requirements combine native platform coverage, optimized numerical loops, C ABI integration and source debugging. This is an architectural judgment, not a measured claim that LLVM is fastest for Cretes. Its compile time, dependency footprint and release churn are costs. Select and pin a supported release only at implementation readiness; test each upgrade with the conformance suite.

Lower default arithmetic through overflow checks; never add no-overflow or aliasing attributes merely because a source program is safe. Prove the specific operation's preconditions. Guard division, shifts and conversions before backend operations that can produce poison or undefined behavior. Language-defined faults must remain observable under optimization.

Initially use the platform linker with explicit argument arrays and declared inputs. Do not download linkers/SDKs during a build. Target runtime and standard-library objects carry matching compiler/runtime metadata. Keep debug information and source-path remapping in the backend contract. Dependency notices and the exact bundled license inventory are release gates.

## Options, advantages, disadvantages and rejected alternatives

| Backend | Potential benefit | Cost and decision |
| --- | --- | --- |
| LLVM | Broad optimization, native tooling/debug integration | Build footprint and semantic-lowering hazards; proposed |
| Cranelift | Compilation-speed and correctness-oriented design | Different optimization/debug tradeoffs; strong future fast-build candidate |
| GCC infrastructure | Mature native code generation | Integration API, distribution/license and maintenance assessment needed; not initial |
| Custom codegen | Complete control | Register allocation, ABI, debugging, optimization and ports all become project work; rejected initially |
| C output | Accessible toolchain | Two compilation layers and semantic/debug mapping; fallback research only |
| WebAssembly | Portable VM target | Not a native backend replacement; deferred platform adapter |
| LLVM plus Cranelift immediately | Separate throughput/edit-loop strategies | Doubles backend equivalence work too early; deferred |

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: backend correctness and flags are in the trusted base. Performance: measure compilation latency, throughput and binary size before adding a second backend. DX: backend failures report a compiler defect with version details, not a user type error. Implementation: keep the adapter narrow and add golden lowering tests for dangerous arithmetic.

## Future verification

Later verify object ABI, debug mapping, checked arithmetic under optimization, target feature baselines and release license inventory. See SOURCES.md for LLVM and Cranelift primary references.

## Risks and open questions

Exact backend version, binding crate and link packaging are implementation-readiness choices; no third-party dependency is installed or licensed by this document.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
