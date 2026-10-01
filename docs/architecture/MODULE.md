# 2.15 — Modules and initialization

> Decision: **ARCH-MODULE-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-007](../requirements/CORE.md#core-007--modules), [CORE-008](../requirements/CORE.md#core-008--visibility-control), [CORE-009](../requirements/CORE.md#core-009--name-resolution-without-execution), [CORE-010](../requirements/CORE.md#core-010--controlled-module-initialization), [CORE-026](../requirements/CORE.md#core-026--platform-independent-semantics), [CORE-028](../requirements/CORE.md#core-028--declarative-package-manifest), [SEC-034](../requirements/domains/cybersecurity.md#sec-034--registry-account-and-namespace-protection)

## Proposed decision and rationale

**Package-qualified module identities, explicit visibility, acyclic imports and declarative initialization.**

A project manifest maps stable module identities to source files under a package root. Identity is the package identity plus a logical module path, not an absolute machine path. File mapping is validated for duplicate names, case collisions and traversal outside allowed roots. Phase 3 defines the import spelling. A source file belongs to one module initially; splitting a module across arbitrary files is deferred.

Visibility defaults to private. Exports form the module interface and imports resolve against that interface without executing code. Import cycles are rejected with a cycle diagnostic in v0.1. Mutually recursive declarations within one module are handled by collecting declarations before checking bodies. Recursive value layout still follows TYPE.md restrictions.

Top-level initialization is limited to declarative, side-effect-free constant evaluation. File I/O, environment access, network access and user process execution do not occur during import or checking. Runtime setup belongs in explicit functions called from the program entry point. This makes initialization order independent of incidental filesystem enumeration.

Constants are evaluated by a restricted typed evaluator with fuel/depth limits, not by running host-language or dependency code. Invalid constant arithmetic is a compile-time diagnostic. Package identity later includes registry origin and immutable version/content identity, preventing two similarly named sources from silently becoming interchangeable.

## Options, advantages, disadvantages and rejected alternatives

Path-only identity was rejected because relocation and case differences change behavior. Arbitrary import-time execution was rejected for reproducibility/security. Cyclic module initialization was rejected for v0.1 complexity. Explicit acyclic modules allow later extension through RFC.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: canonical root validation and symlink handling must prevent unintended file reads. Performance: interfaces give future incremental invalidation boundaries. DX: cycle diagnostics show the path; small single-file projects have an implicit local package. Implementation: deterministic module graph and restricted constant evaluator.

## Future verification

Later test case collisions, symlink escapes, visibility failures, cycles, declaration recursion and identical results under randomized directory order.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
