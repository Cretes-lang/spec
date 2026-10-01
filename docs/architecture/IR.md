# 2.10 — Intermediate representations

> Decision: **ARCH-IR-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-029](../requirements/CORE.md#core-029--separate-and-incremental-compilation), [CORE-031](../requirements/CORE.md#core-031--specification-coverage-of-shipped-features), [DX-005](../requirements/CORE.md#dx-005--diagnostic-content), [DX-017](../requirements/CORE.md#dx-017--consistent-semantics-across-tools), [PERF-009](../requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput), [SAFE-001](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code)

## Proposed decision and rationale

**Typed HIR, ownership-aware control-flow MIR, then target backend IR.**

AST preserves parsed structure and recovery nodes. HIR resolves names and desugars surface constructs while keeping origin maps. Typed HIR makes conversions, effects, value categories and type identities explicit. MIR is a control-flow graph over typed places and values, with move/borrow, initialization, checks, calls and cleanup operations. Scalar temporaries may use SSA; mutable storage and cleanup state must remain explicit until their invariants are proven.

MIR is the last backend-neutral semantic checkpoint. Every block has a terminator; operands are defined and type-correct; joins agree on initialized ownership state; loans cannot outlive storage; every normal/error exit closes its live guards. Abort terminators explicitly do not execute language cleanup. Validate these properties before and after each semantics-changing pass.

Lower MIR to backend IR only after checks and cleanup are explicit. Do not reuse a backend's undefined behavior as the language's error model. Keep a source-origin chain for synthetic instructions and eliminated/inlined constructs. Serializing MIR for caches is an internal versioned format, never a package ABI.

Async lowering later transforms suspension points into explicit state machines only after ownership constraints are known. Device memory and vector types can be represented through typed library/intrinsic boundaries without adding mandatory GPU IR to the compiler. A future WebAssembly adapter consumes the same verified MIR contracts, subject to its platform limits.

## Options, advantages, disadvantages and rejected alternatives

AST-only is too implicit for ownership and cleanup. One backend-specific IR leaks target semantics into language checking. Many speculative IR levels add maintenance without proven need. Three conceptual levels are proposed, with typed HIR as a checked state rather than an unrelated second frontend.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: verifiers defend against invalid transformations but do not prove compiler correctness. Performance: explicit control flow enables inlining/check elimination; avoid repeated whole-program copies. DX: spans survive all lowerings. Implementation: document MIR operations and pass contracts before introducing optimizations.

## Future verification

Later unit-test verifier rejection, cleanup-preserving rewrites, source mappings and cross-profile behavior; fuzz serialized internal representations only as untrusted input.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
