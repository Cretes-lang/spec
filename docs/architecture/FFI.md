# 2.16 — FFI and ABI architecture

> Decision: **ARCH-FFI-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CONC-020](../requirements/CONCURRENCY.md#conc-020--concurrency-and-foreign-code), [INTOP-001](../requirements/INTEROPERABILITY.md#intop-001--calling-c-abi-functions), [INTOP-002](../requirements/INTEROPERABILITY.md#intop-002--exposing-cretes-functions-through-the-c-abi), [INTOP-003](../requirements/INTEROPERABILITY.md#intop-003--c-compatible-data-layout), [INTOP-004](../requirements/INTEROPERABILITY.md#intop-004--linking-and-loading-native-libraries), [INTOP-005](../requirements/INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary), [INTOP-006](../requirements/INTEROPERABILITY.md#intop-006--safe-wrappers), [INTOP-007](../requirements/INTEROPERABILITY.md#intop-007--error-propagation-across-the-boundary), [INTOP-008](../requirements/INTEROPERABILITY.md#intop-008--callbacks-from-foreign-code), [INTOP-009](../requirements/INTEROPERABILITY.md#intop-009--binding-generation), [INTOP-010](../requirements/INTEROPERABILITY.md#intop-010--operating-system-api-access), [INTOP-011](../requirements/INTEROPERABILITY.md#intop-011--c-interoperability), [INTOP-012](../requirements/INTEROPERABILITY.md#intop-012--ai-runtime-integration), [INTOP-013](../requirements/INTEROPERABILITY.md#intop-013--python-interoperability), [INTOP-014](../requirements/INTEROPERABILITY.md#intop-014--javascript-interoperability), [INTOP-015](../requirements/INTEROPERABILITY.md#intop-015--jvm-interoperability), [INTOP-016](../requirements/INTEROPERABILITY.md#intop-016--webassembly-modules), [INTOP-017](../requirements/INTEROPERABILITY.md#intop-017--unsafe-ffi-declarations-are-not-trusted-by-default), [INTOP-018](../requirements/INTEROPERABILITY.md#intop-018--abi-stability-policy), [INTOP-019](../requirements/INTEROPERABILITY.md#intop-019--declared-native-dependencies), [PERF-016](../requirements/PERFORMANCE.md#perf-016--ffi-call-overhead), [SAFE-018](../requirements/SAFETY.md#safe-018--ffi-is-an-unsafe-boundary)

## Proposed decision and rationale

**A declared C ABI boundary with explicit ownership contracts; no stable Cretes-native ABI and no user FFI in v0.1.**

Foreign declarations record calling convention, symbol, target availability, layout, nullability, length, ownership, lifetime, alignment, thread affinity and error behavior. They are unsafe assertions, not proof. Generated bindings preserve that unsafe classification until a reviewed safe wrapper validates inputs and encapsulates all obligations.

Pointers cross as raw addresses paired with documented bounds/lifetime, never as automatically trusted Cretes references. Strings specify encoding, length and termination; embedded NUL and invalid UTF-8 are handled explicitly. Buffers name who allocates and which matching allocator frees them. A caller may not resize or destroy a buffer while native code retains it. Zero-copy requires compatible layout, alignment, ownership and synchronization; otherwise copy with an explicit cost.

Callbacks use a context pointer plus lifetime registration. Foreign threads enter through a runtime attachment boundary before calling Cretes; callbacks cannot outlive their registration. Blocking foreign calls do not occupy an async scheduler worker indefinitely. Native exceptions and Cretes faults cannot unwind across the boundary. C-facing exports translate recoverable results into an explicit status plus output representation; no private sum/aggregate layout is exported by accident.

C-compatible record layout is opt-in, verified per target. Native Cretes symbols/layout remain unstable during 0.x. Version a library's C-facing interface independently, document supported target ABIs and reject mismatched artifacts. C++ uses C shims; Python/JavaScript/JVM integrations are separately versioned adapters. WebAssembly uses an explicit host/component contract, not an assumed C ABI. AI runtimes use the same wrapper rules.

## Options, advantages, disadvantages and rejected alternatives

Directly exposing internal object layouts was rejected as brittle. Automatic trust in generated headers was rejected as unsafe. Full C++/Python/JVM object-model interoperability in the core was rejected as scope expansion. A narrow C-first boundary is proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: foreign code is outside safe Cretes guarantees; wrappers and allocator matching are critical. Performance: scalar calls should avoid unnecessary marshaling, while validation/copies are documented. DX: binding generators can assist but cannot certify contracts. Implementation: target layout tables, boundary checks, callback registration and link manifests.

## Future verification

Later test C fixtures for each supported target, null/length mismatches, allocator mismatch, callbacks from foreign threads, unwinding containment and retained-buffer lifetime.

## Risks and open questions

Concrete declaration syntax, binding-tool choice and stable ABI versioning format require later specification; user-facing FFI remains post-v0.1.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
