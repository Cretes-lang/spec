# 2.9 — Nullability architecture

> Decision: **ARCH-NULL-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-012](../requirements/CORE.md#core-012--user-defined-data-types), [INTOP-003](../requirements/INTEROPERABILITY.md#intop-003--c-compatible-data-layout), [SAFE-005](../requirements/SAFETY.md#safe-005--valid-references), [SAFE-006](../requirements/SAFETY.md#safe-006--null-safety)

## Proposed decision and rationale

**Non-null ordinary references and a distinct option type for absence.**

An absent value is an explicit sum alternative. The checker requires exhaustive handling or an explicit checked extraction whose failure has defined fault behavior. There is no implicit coercion from possibly absent to present. An initialized option with absence is distinct from uninitialized storage.

v0.1 uses this same conceptual model for missing map keys, unsuccessful searches and nullable external data. Result is distinct from option: absence is not automatically an error, and an error has context beyond missing data. Chaining optional operations may be proposed in syntax design but cannot silently bypass checking.

An internal compiler may exploit representation niches only when it proves equivalence and does not expose those assumptions across an ABI. C null pointers are raw boundary values. A wrapper validates nullability, length, alignment and lifetime, then constructs an option or error; a non-null foreign pointer alone is not evidence of validity.

Data serialization gives absence an explicit format-specific representation. It never serializes raw native pointer bits or assumes a tag layout. Generic option semantics remain stable across future optimizations even when physical representation changes.

## Options, advantages, disadvantages and rejected alternatives

Nullable-by-default weakens the common reference invariant and increases checks. Flow-sensitive nullable annotations are possible but would duplicate a sum-type model. A single explicit option abstraction is proposed; implicit null conversions and sentinel-only absence are rejected.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: null checks cannot substitute for foreign lifetime validation. Performance: representation optimization is allowed behind private boundaries. DX: absence is visible at API boundaries and handled consistently. Implementation: exhaustive sum analysis, checked extraction and wrapper validation.

## Future verification

Later test absent/present branches, nested option/result, non-null FFI pointers with invalid contracts, serialization and optimized representations.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
