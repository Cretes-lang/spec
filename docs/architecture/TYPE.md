# 2.4 — Type and numeric architecture

> Decision: **ARCH-TYPE-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AI-001](../requirements/domains/ai-ml.md#ai-001--exact-numeric-semantics), [CORE-006](../requirements/CORE.md#core-006--text-distinct-from-bytes), [CORE-011](../requirements/CORE.md#core-011--mutable-and-immutable-bindings), [CORE-012](../requirements/CORE.md#core-012--user-defined-data-types), [CORE-014](../requirements/CORE.md#core-014--control-flow), [CORE-015](../requirements/CORE.md#core-015--functions), [CORE-016](../requirements/CORE.md#core-016--functions-as-values), [CORE-017](../requirements/CORE.md#core-017--errors-detected-before-execution), [CORE-018](../requirements/CORE.md#core-018--primitive-types-with-defined-representation), [CORE-019](../requirements/CORE.md#core-019--parametric-abstraction), [CORE-020](../requirements/CORE.md#core-020--reduced-annotation-burden), [CORE-021](../requirements/CORE.md#core-021--no-implicit-lossy-conversions), [SAFE-006](../requirements/SAFETY.md#safe-006--null-safety), [SAFE-008](../requirements/SAFETY.md#safe-008--defined-integer-overflow), [SAFE-009](../requirements/SAFETY.md#safe-009--explicit-overflow-handling-operations), [SAFE-010](../requirements/SAFETY.md#safe-010--overflow-detection-during-development), [SAFE-011](../requirements/SAFETY.md#safe-011--defined-arithmetic-edge-cases), [SAFE-015](../requirements/SAFETY.md#safe-015--type-safety)

## Proposed decision and rationale

**Static typing with local bidirectional inference, nominal aggregates and explicit algebraic absence/error values.**

Require explicit public function parameter/return contracts; infer local bindings and closure expressions from surrounding types. Do not infer a public API by searching callers across packages. v0.1 has booleans, Unicode scalar values, UTF-8 text, bytes, fixed-width numbers, tuples, records and tagged sum types. Ordinary references are non-null. Mutable bindings are explicit; mutation permission is distinct from ownership.

Signed and unsigned 8/16/32/64-bit integers have defined ranges. Numeric names and literal notation are left to Phase 3. Unsuffixed integer literals use contextual type if representable; otherwise use signed 64-bit, diagnosing out-of-range values. Default floating literals are binary64 unless context supplies binary32. No implicit numeric conversions between typed values, including signed/unsigned mixing. Conversions that may lose range or precision are explicit; checked conversion reports a result. Float-to-int conversion truncates toward zero and rejects NaN, infinity or out-of-range results.

Default integer overflow, division by zero, minimum-signed divided by minus one, and negative/out-of-width shift counts cause a defined fault in every profile. Explicit checked, wrapping and saturating operations are available. Floating arithmetic follows binary32/binary64 round-to-nearest ties-to-even; no implicit fast-math, reassociation or contraction. Signed zero and NaN behavior are specified; NaN payload bit preservation is not promised. Serialization never assumes native byte order. An address-sized unsigned index type is target metadata, not a portable serialized representation.

User-defined generics are post-v0.1. Reserve nominal interface constraints and monomorphization for statically known concrete instantiations; explicit dynamic dispatch is a distinct later facility. Built-in option, result and collection families may be compiler-known type constructors in v0.1; this does not open user generic declarations. Recursive by-value layout is rejected; recursion needs an owning indirection. Type aliases do not create new nominal identity.

## Evaluation and future callable values

All operand and argument evaluation is left-to-right, with explicit short-circuit boolean evaluation. Future first-class functions use typed parameter/result contracts; closures capture by move or a checked borrow and cannot escape captured lifetimes. Function representation and callable-interface dispatch remain post-v0.1 details. A future generic interface design must define coherence, orphan/overlap rules and recursive instantiation limits before exposure; this proposal does not silently authorize arbitrary specialization.

## Options, advantages, disadvantages and rejected alternatives

| Discipline | Fit | Disposition |
| --- | --- | --- |
| Static with local inference | Early errors, unboxed data, bounded API analysis | Proposed |
| Fully annotated static | Predictable but burdens small automation | Rejected as default |
| Dynamic | Easy heterogeneous scripting; runtime errors and boxing | Rejected as primary |
| Gradual/hybrid | Interop flexibility; complex casts and guarantee boundaries | Deferred; foreign dynamic values need explicit wrappers |
| Global inference | Fewer annotations; distant edits change contracts/errors | Rejected |

For generics, universal boxing/dictionary dispatch was not selected as the only strategy because numerical loops need concrete layouts. Monomorphization trades code size and compile time for specialization; measure both before stabilization.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: all numeric edge cases are checked before emitting backend operations with narrower validity domains. Performance: checks may be removed only by proof; specialization can increase artifact size. DX: contextual inference handles locals while public annotations explain contracts. Implementation: constraint solving with bounded recursion, typed constants, layout recursion checks and exhaustive sum analysis.

## Future verification

Later test every integer width at boundaries, NaN/infinity conversion, signed zero, cross-profile equivalence, invalid recursive layout, inference diagnostics and exhaustive handling.

## Risks and open questions

Post-v0.1 generic coherence, trait-object layout and specialization limits need a follow-up RFC. Phase 3 specifies spellings and grammar, not different overflow semantics.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
