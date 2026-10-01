# 2.30 — Architecture review and acceptance gates

> Decision: **ARCH-REVIEW-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-031](../requirements/CORE.md#core-031--specification-coverage-of-shipped-features), [PERF-017](../requirements/PERFORMANCE.md#perf-017--evidence-before-claims), [PERF-018](../requirements/PERFORMANCE.md#perf-018--benchmark-methodology), [SAFE-023](../requirements/SAFETY.md#safe-023--memory-management-evaluation-criteria), [SEC-015](../requirements/domains/cybersecurity.md#sec-015--cryptographic-implementation-assurance)

## Proposed decision and rationale

**Publish a reviewable proposal, preserve objections and keep Phase 2 open until the RFC process records acceptance.**

This is an architectural self-review, not independent approval, a proof of soundness or executable validation. No compiler/runtime exists and no performance benchmark or security test has run. The review evaluates internal consistency, plausible implementation and explicit risk ownership.

| Perspective | Finding | Required follow-through |
| --- | --- | --- |
| Language | Ownership, option/result, checked arithmetic and explicit initialization form a coherent proposed core | Formalize loan/move and evaluation semantics before implementation |
| Compiler | Typed HIR/MIR separate checking from backend codegen; one backend limits equivalence burden | Pass verifiers and safe lowering tests, especially poison/overflow |
| Security | Safe-source contract depends on trusted wrappers/backend; cancellation must retain I/O buffers | Independent expert review when available; fuzz/sanitizer and provider gates |
| Performance | AOT/unboxed data avoid mandatory VM/boxing, but compilation and destruction can be costly | Measure cold builds, tail latency, memory, code size and numerical throughput |
| Developer experience | Synchronous helpers and local inference support scripts; ownership adds learning cost | Novice task walkthroughs and diagnostic quality review |

Consistency checks: fatal faults do not promise cleanup; result errors do. Cancellation is cooperative and waits for terminal I/O completion. v0.1 has no scheduler or user FFI. Native ABI stability is not promised. Crypto/accelerator/provider details remain deferred. Phase 1 obligations retain their original priority and milestone; a proposal mapping does not claim implementation.

Acceptance sequence: publish all sections and traceability; conduct public RFC review; address objections; announce at least seven calendar days of final comment with intended outcome; after the period, record dated acceptance/rejection/deferral and rationale; only then update decision statuses and mark covered Phase 1 architecture questions resolved. Do not backdate the period or infer approval from silence. Material design changes restart appropriate review.

Phase 3 inputs are the accepted semantic model, numeric/error/ownership contracts, module and concurrency boundaries, plus an explicit grammar worklist. Phase 3 must decide identifiers, keywords, literals, comments, declaration/type/function/import/generic/error/async notation, operator precedence, formal grammar and parser recovery examples. Those tasks have not started here.

## Options, advantages, disadvantages and rejected alternatives

Immediate acceptance on document creation was rejected because the RFC process requires review and elapsed final-comment time. Inventing independent reviewer approvals was rejected. Published proposed documents plus an open RFC are the correct current state.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: no audit/benchmark claims are fabricated. Performance: hypotheses stay separate from results. DX: index, decision records and traceability make review navigable. Implementation: blocked on accepted architecture and subsequent syntax specification.

## Future verification

Current validation is documentation-only: ID uniqueness, required record fields, all requirement mappings, relative links/anchors, question coverage, milestone consistency and diff inspection. Later executable verification belongs to implementation.

## Risks and open questions

RFC acceptance, formal ownership/concurrency details, provider/security decisions and implementation evidence remain open. See RISKS.md for owners and closure criteria.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
