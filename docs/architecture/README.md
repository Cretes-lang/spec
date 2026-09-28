# Cretes Phase 2 architecture proposal

> **Overall status: PROPOSED / IN REVIEW. Not accepted or implemented.**
> Date: 2026-09-27. Phase 1 remains the requirements authority. Phase 0 administrative dependencies remain tracked separately.

This directory covers sections 2.1–2.30. Each section is a decision record with requirements, design/rationale, qualitative alternatives, security/performance/developer/implementation consequences and future verification. Filenames use decision-area identifiers; domain documents live here alongside the other architecture boundaries to keep cross-links direct.

Publication of these documents is not acceptance of language semantics. The RFC process requires public review and at least seven calendar days of final comment before a dated maintainer decision. SAFE-023 specifically requires an accepted memory-management RFC. Phase 2 therefore remains open until that gate is met.

## Reading order

Start with [v0.1 blueprint](V0.1-ARCHITECTURE.md), then [types](TYPE.md), [memory](MEM.md), [errors](ERROR.md), [IR](IR.md), [backend](BACKEND.md), [concurrency](CONC.md) and [async](ASYNC.md). Review [all requirement mappings](TRACEABILITY.md), [question dispositions](QUESTIONS.md), [risks](RISKS.md), [architecture review](REVIEW.md) and [primary sources](SOURCES.md).

## Section and decision register

| Section | Decision | Topic | Status |
| --- | --- | --- | --- |
| 2.1 | ARCH-EXEC-001 | [Execution model](EXEC.md) | PROPOSED |
| 2.2 | ARCH-COMPILER-001 | [Compiler architecture and bootstrapping](COMPILER.md) | PROPOSED |
| 2.3 | ARCH-PIPELINE-001 | [Compilation pipeline and invariants](PIPELINE.md) | PROPOSED |
| 2.4 | ARCH-TYPE-001 | [Type and numeric architecture](TYPE.md) | PROPOSED |
| 2.5 | ARCH-MEM-001 | [Memory-management model](MEM.md) | PROPOSED |
| 2.6 | ARCH-RESOURCE-001 | [Resource and lifetime management](RESOURCE.md) | PROPOSED |
| 2.7 | ARCH-SAFETY-001 | [Safety architecture](SAFETY.md) | PROPOSED |
| 2.8 | ARCH-ERROR-001 | [Error-handling architecture](ERROR.md) | PROPOSED |
| 2.9 | ARCH-NULL-001 | [Nullability architecture](NULL.md) | PROPOSED |
| 2.10 | ARCH-IR-001 | [Intermediate representations](IR.md) | PROPOSED |
| 2.11 | ARCH-BACKEND-001 | [Backend strategy](BACKEND.md) | PROPOSED |
| 2.12 | ARCH-RUNTIME-001 | [Runtime responsibilities](RUNTIME.md) | PROPOSED |
| 2.13 | ARCH-CONC-001 | [Concurrency architecture](CONC.md) | PROPOSED |
| 2.14 | ARCH-ASYNC-001 | [Async and cancellation architecture](ASYNC.md) | PROPOSED |
| 2.15 | ARCH-MODULE-001 | [Modules and initialization](MODULE.md) | PROPOSED |
| 2.16 | ARCH-FFI-001 | [FFI and ABI architecture](FFI.md) | PROPOSED |
| 2.17 | ARCH-PLATFORM-001 | [Platform architecture](PLATFORM.md) | PROPOSED |
| 2.18 | ARCH-OPT-001 | [Optimization architecture](OPT.md) | PROPOSED |
| 2.19 | ARCH-SECURITY-001 | [Security and trust architecture](SECURITY.md) | PROPOSED |
| 2.20 | ARCH-TOOLCHAIN-001 | [Toolchain and developer tools](TOOLCHAIN.md) | PROPOSED |
| 2.21 | ARCH-BUILD-001 | [Build and package architecture](BUILD.md) | PROPOSED |
| 2.22 | ARCH-DIAGNOSTIC-001 | [Diagnostics architecture](DIAGNOSTIC.md) | PROPOSED |
| 2.23 | ARCH-DEBUG-001 | [Debugging and observability](DEBUG.md) | PROPOSED |
| 2.24 | ARCH-AI-001 | [AI/ML architecture](AI.md) | PROPOSED |
| 2.25 | ARCH-NET-001 | [Networking architecture](NET.md) | PROPOSED |
| 2.26 | ARCH-AUTO-001 | [Automation architecture](AUTO.md) | PROPOSED |
| 2.27 | ARCH-SECURITY-DOMAIN-001 | [Defensive cybersecurity libraries](SECURITY-DOMAIN.md) | PROPOSED |
| 2.28 | ARCH-COMPAT-001 | [Compatibility and stability](COMPAT.md) | PROPOSED |
| 2.29 | ARCH-V0.1-ARCHITECTURE-001 | [v0.1 implementation blueprint](V0.1-ARCHITECTURE.md) | PROPOSED |
| 2.30 | ARCH-REVIEW-001 | [Architecture review and acceptance gates](REVIEW.md) | PROPOSED |

## Boundaries and status

The proposal is native AOT, static typing with local inference, move ownership/scoped loans, explicit result/option values, checked numeric behavior, typed HIR/MIR and an initial LLVM adapter. These are review candidates. No final syntax, production compiler, runtime, library, package registry, deployment or release is created here.

The original v0.1 scope remains 86 requirements (77 MUST and 9 SHOULD). Async/network protocols, user FFI/unsafe, user generics and advanced AI integration remain later milestones. All 257 Phase 1 requirements are indexed, including the 173 MUST requirements; architecture mappings do not claim implementation compliance.

## GitHub tracking

- [Phase 2 acceptance tracker](https://github.com/Cretes-lang/spec/issues/4)
- [RFC repository and process](https://github.com/Cretes-lang/rfcs)
- [Phase 1 baseline](../requirements/README.md)
- [Original open-question register](../PHASE-2-OPEN-QUESTIONS.md)

RFC and proposal pull-request links are recorded in the tracking issue. Keep the issue open until acceptance. Status vocabulary is PROPOSED, ACCEPTED, DEFERRED, REJECTED and SUPERSEDED; implementation status is tracked separately.
