# 2.6 — Resource and lifetime management

> Decision: **ARCH-RESOURCE-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AUTO-006](../requirements/domains/automation.md#auto-006--file-operations), [CONC-006](../requirements/CONCURRENCY.md#conc-006--cancellation), [INTOP-005](../requirements/INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary), [SAFE-004](../requirements/SAFETY.md#safe-004--no-double-release), [SAFE-013](../requirements/SAFETY.md#safe-013--deterministic-resource-release), [SAFE-014](../requirements/SAFETY.md#safe-014--resource-leak-diagnostics), [SEC-005](../requirements/domains/cybersecurity.md#sec-005--secret-zeroization)

## Proposed decision and rationale

**Affine resource guards with scope-bound cleanup and explicit fallible close/finish operations.**

Files, sockets, locks, processes, connections, mappings, GPU buffers and keys are represented by owning guards. A move transfers cleanup responsibility; copying a guard is forbidden unless a separate, documented OS duplication operation creates an independent handle. A closed guard cannot be used again. Cleanup is independent of memory reclamation.

Normal return and result-error propagation execute initialized guards in reverse declaration order. Partially constructed objects clean up only initialized fields in reverse construction order. The compiler makes each cleanup edge explicit in MIR and uses drop-state tracking to avoid double cleanup. Scope destruction cannot throw or suspend. If an operation such as buffered-file flush can fail, an explicit close/finish reports the error; fallback cleanup closes best-effort and cannot silently promise data durability.

Unrecoverable faults terminate in v0.1 and do not promise language-level cleanup. OS process termination releases many handles but does not flush application buffers or erase every secret copy. This fits SAFE-013's distinction for faults that permit cleanup; recoverable errors always follow cleanup paths. Safe code cannot rely on destructor side effects for memory-safety invariants.

Later task cancellation follows cooperative structured shutdown, not arbitrary stack interruption. Cancel an operation, await its terminal completion, then release its registered buffer/handle. Async protocol shutdown is explicit and bounded by caller policy; a non-suspending guard handles last-resort close. Child processes are reaped by a supervised owner; cancellation policy must specify wait, terminate and escalation rather than orphaning work.

## Options, advantages, disadvantages and rejected alternatives

Finalizers alone were rejected because reclamation timing does not guarantee prompt release. Manual close alone was rejected because every error path becomes a leak hazard. Unrestricted throwing/suspending destructors were rejected because cleanup can recursively fail or deadlock. Guards plus explicit fallible finish are proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: lifetime registration prevents reuse while the OS still owns an I/O buffer. Performance: close and destruction can block for documented OS operations; no universal bounded cleanup claim. DX: ordinary scope-based cleanup minimizes boilerplate; durability-sensitive operations require explicit finish. Implementation: cleanup ladders, initialization flags and resource-state diagnostics.

## Future verification

Later inject failures after each acquisition step; assert exactly-once cleanup on returns/errors, explicit flush failures, cancellation with late completion, and process reaping.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
