# 2.2 — Compiler architecture and bootstrapping

> Decision: **ARCH-COMPILER-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-025](../requirements/CORE.md#core-025--deterministic-compilation), [CORE-029](../requirements/CORE.md#core-029--separate-and-incremental-compilation), [CORE-031](../requirements/CORE.md#core-031--specification-coverage-of-shipped-features), [DX-005](../requirements/CORE.md#dx-005--diagnostic-content), [DX-008](../requirements/CORE.md#dx-008--robustness-on-malformed-input), [DX-017](../requirements/CORE.md#dx-017--consistent-semantics-across-tools), [PERF-007](../requirements/PERFORMANCE.md#perf-007--incremental-builds), [SEC-027](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds), [SEC-032](../requirements/domains/cybersecurity.md#sec-032--toolchain-release-integrity)

## Proposed decision and rationale

**A library-oriented compiler with an initially Rust-hosted implementation and a narrow native backend boundary.**

Organize source management, parsing, semantic analysis, diagnostics, intermediate representations and code generation as independently testable libraries behind the driver. A compilation session owns an immutable source snapshot, target configuration and intern tables. Stable IDs connect entities; source pointers or parser objects must not escape their session lifetime.

The initial implementation language proposal is Rust, chosen for typed data modeling, explicit error handling and memory-safety support in code that processes untrusted source. This does not select Cretes syntax or require users to learn Rust. It also does not prove the compiler correct. Native backend bindings and OS operations remain audited trust boundaries.

Bootstrap with a pinned released host compiler and dependency lockfile. Record source provenance, compiler version, backend version, patches and build inputs in release metadata. Avoid self-hosting until Cretes has a stable-enough frontend, conformance suite and reproducible bootstrap plan. No bootstrap code is created in Phase 2.

Incremental compilation is an architectural boundary, not a v0.1 delivery promise: queries take explicit inputs and return immutable results with dependency fingerprints. Start with whole-project analysis. Later caching must invalidate transitive dependents and reject schema/version mismatches. The checker and eventual language server share semantic analysis rather than reimplement it.

## Options, advantages, disadvantages and rejected alternatives

| Option | Evaluation |
| --- | --- |
| Monolithic command | Easiest initial assembly but couples tooling, testing and backend; rejected |
| Compiler libraries plus thin driver | Proposed; enables reuse and explicit test boundaries |
| Rust host | Proposed; additional learning and native-build integration cost acknowledged |
| C/C++ host | Direct backend integration but larger manual memory-safety burden; not selected |
| Python host | Accessible experimentation but deployment and performance constraints; not primary |
| Immediate self-hosting | Circular bootstrap and immature-toolchain risk; deferred |

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: untrusted source and malformed cache files receive limits and validation. Performance: arena allocation and interning are implementation opportunities, not semantic requirements. DX: one diagnostic schema across tools. Implementation: define library interfaces and versioned internal schemas before caching; pin dependencies only when implementation begins.

## Future verification

Later fuzz each input boundary, compare cached and clean builds, test deterministic diagnostics and artifacts, and record bootstrap provenance.

## Risks and open questions

The exact Rust and backend versions must be selected and pinned during implementation readiness; no current-version dependency is silently promised.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
