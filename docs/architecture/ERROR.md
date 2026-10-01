# 2.8 — Error-handling architecture

> Decision: **ARCH-ERROR-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AUTO-002](../requirements/domains/automation.md#auto-002--error-context-for-operational-failures), [CONC-008](../requirements/CONCURRENCY.md#conc-008--error-propagation), [CORE-022](../requirements/CORE.md#core-022--explicit-recoverable-errors), [CORE-023](../requirements/CORE.md#core-023--recoverable-errors-versus-faults), [CORE-024](../requirements/CORE.md#core-024--structured-error-information), [INTOP-007](../requirements/INTEROPERABILITY.md#intop-007--error-propagation-across-the-boundary), [SAFE-020](../requirements/SAFETY.md#safe-020--defined-fault-behavior), [SAFE-021](../requirements/SAFETY.md#safe-021--defined-behavior-on-resource-exhaustion)

## Proposed decision and rationale

**Explicit algebraic result values for recoverable errors, with abort-only unrecoverable faults in v0.1.**

An operation either returns its success value or a typed error alternative. Ignoring a fallible result produces a diagnostic; callers explicitly handle, propagate or intentionally discard it with a visible rationale-bearing action. The exact notation is a Phase 3 task. Propagation follows normal control-flow cleanup; it is not exception unwinding.

File, network, process, model-runtime and credential failures are external/recoverable conditions unless their API declares an unrecoverable precondition. Structured errors carry a stable category, operation, optional OS/provider code and a causal chain. Human text may vary; machine consumers must use categories. Context attachment redacts sensitive values and caps chain depth/size.

Programmer faults (bounds/assertion failure, default arithmetic overflow) and runtime invariant violations invoke a minimal fault reporter and terminate. No catchable panic or cross-frame unwinding exists in v0.1. Allocation may be fallible through explicit reserve/allocate APIs; ordinary allocation failure uses the defined fault path. Fault reports identify source location when available without allocating or dumping process memory.

After concurrency is introduced, task groups return explicit completion/error/cancellation outcomes; a runtime-corruption fault still terminates the process. A library cannot silently convert all programming faults into ordinary network errors. Foreign exceptions or unwinding must not cross a Cretes boundary; wrappers translate documented error codes/results and contain native exceptions where the foreign ABI permits it.

## Options, advantages, disadvantages and rejected alternatives

Unchecked exceptions hide effects and complicate cleanup/FFI. Checked exceptions or full effect rows could express errors but add complexity before there is an ecosystem. Bare integer codes lose type/context information. Result values with abort-only faults are proposed; catchable unwinding requires a later RFC and ABI review.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: avoid continuing after invariant corruption and redact contextual secrets. Performance: explicit branches and no unwind tables required by Cretes semantics; cost still needs measurement. DX: concise propagation is required of Phase 3, not prescribed notation. Implementation: result-type checking, cleanup on propagation and allocation-independent fault reporting.

## Future verification

Later test nested propagation cleanup, unused errors, context redaction, resource exhaustion, task error aggregation and FFI boundary containment.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
