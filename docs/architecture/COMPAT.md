# 2.28 — Compatibility and stability

> Decision: **ARCH-COMPAT-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-030](../requirements/CORE.md#core-030--language-evolution-mechanism), [CORE-031](../requirements/CORE.md#core-031--specification-coverage-of-shipped-features), [DX-018](../requirements/CORE.md#dx-018--release-documentation), [INTOP-018](../requirements/INTEROPERABILITY.md#intop-018--abi-stability-policy), [PLAT-011](../requirements/PLATFORMS.md#plat-011--tier-changes)

## Proposed decision and rationale

**Explicit feature maturity and versioned artifacts, following existing pre-1.0 policy without premature editions.**

| State | Meaning |
| --- | --- |
| Experimental | Research-only behavior; no compatibility promise |
| Unstable | Specified enough for testing but may change under RFC |
| Stable | Meets documented source/API commitments for its release series |
| Deprecated | Supported temporarily with migration guidance and removal policy |
| Removed | No longer supported; diagnostic/migration reference retained |

Architecture status (PROPOSED/ACCEPTED/DEFERRED/REJECTED/SUPERSEDED) is separate from feature maturity and implementation status. An accepted RFC can describe an unimplemented unstable feature. A merged draft document cannot claim accepted semantics.

During 0.x, breaking source changes require recorded rationale, migration notes and updated conformance tests; they must follow VERSIONING.md rather than inventing new version arithmetic here. Compiler, standard-library and runtime artifacts identify compatible versions. The private Cretes ABI may change; mix-and-match linking is rejected unless a supported boundary exists. A versioned C interface is the external stability boundary when delivered.

Manifests eventually state supported language/toolchain versions; an older compiler diagnoses unsupported features rather than guessing. Experimental flags are recorded in artifact/cache identity. Avoid editions until a concrete migration problem justifies their cost. Deprecation identifies replacement, affected versions and release policy. Platform tier changes also receive explicit notice and evidence.

The specification uses precise prose plus later formal grammar, executable conformance tests and focused formalization of ownership/concurrency invariants. Tests link requirement and decision IDs. No reference implementation silently overrides the written specification; discrepancies become issues.

## Options, advantages, disadvantages and rejected alternatives

Permanent compatibility from the first prototype was rejected as unrealistic. Unversioned private ABI mixing was rejected. Immediate edition machinery was rejected as unnecessary. Explicit maturity/version metadata with RFC-controlled evolution is proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: unsupported/incompatible artifacts fail closed. Performance: compatibility choices may constrain future optimizations and need review. DX: migrations are documented; old features fail with actionable diagnostics. Implementation: artifact metadata, conformance mapping and release-note discipline.

## Future verification

Later test version mismatch, feature flags in caches, deprecation diagnostics, migration examples and source/API/ABI distinctions in release documentation.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
