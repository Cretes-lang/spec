# 2.1 — Execution model

> Decision: **ARCH-EXEC-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AUTO-001](../requirements/domains/automation.md#auto-001--single-file-programs), [DX-001](../requirements/CORE.md#dx-001--single-toolchain-entry-point), [DX-002](../requirements/CORE.md#dx-002--cretes-check), [DX-003](../requirements/CORE.md#dx-003--cretes-build), [DX-004](../requirements/CORE.md#dx-004--cretes-run), [PERF-001](../requirements/PERFORMANCE.md#perf-001--self-contained-executables), [PERF-004](../requirements/PERFORMANCE.md#perf-004--program-startup-latency), [PERF-005](../requirements/PERFORMANCE.md#perf-005--toolchain-responsiveness), [PERF-006](../requirements/PERFORMANCE.md#perf-006--analysis-faster-than-full-builds), [PERF-017](../requirements/PERFORMANCE.md#perf-017--evidence-before-claims)

## Proposed decision and rationale

**Native ahead-of-time compilation is the proposed primary execution model; run compiles and executes a cached native artifact.**

The same frontend checks a single .cretes file and a multi-module project. `cretes check` stops before code generation; `cretes build` produces an artifact; `cretes run` checks its cache and launches the matching artifact. Run must rebuild after any semantic input changes. It must never interpret stale source through a different language engine.

The v0.1 executable includes required Cretes runtime support but may depend on documented system libraries. A self-contained Cretes artifact does not imply a completely statically linked operating-system image. The loader, OS ABI and minimum OS version remain deployment constraints.

A cache key includes source content, dependency identities, compiler/runtime versions, target description, profile and semantic flags. The cache is private to the user, uses atomic replacement and rejects untrusted or mismatched entries. Running source is execution with the user's privileges; it is not a sandbox.

The proposal deliberately has one semantic engine and one initial backend. WebAssembly remains a later target; an interpreter could eventually serve teaching or testing, but is not required to define current behavior. JIT execution and live images remain outside the initial scope.

## Options, advantages, disadvantages and rejected alternatives

| Candidate | Benefits for Cretes | Cost and disposition |
| --- | --- | --- |
| Native AOT | Deployable tools, direct C boundary, no warm-up requirement | Linker/distribution complexity; proposed primary |
| Interpreter | Simple interactive experimentation | Separate execution engine and runtime distribution; deferred |
| Bytecode VM | Portable executable format | VM maintenance and interpreter/JIT performance work; rejected as primary |
| JIT | Runtime specialization | Startup, executable-memory policy and debugging complexity; deferred |
| C transpilation | Reuses installed C toolchains | Source/debug mapping and C undefined-behavior hazards; rejected as primary |
| Hybrid profiles | Potentially faster edit loop | Two engines require semantic equivalence testing; deferred |
| WebAssembly | Portable constrained deployment | Host APIs and OS facilities need adapters; future target, not native replacement |

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: compilation does not authorize dependency code execution; only explicit run launches a program. Performance: cached runs avoid repeated backend work, but cold compile latency may be noticeable. Developer experience: one command for small programs, with clear build versus execution errors. Implementation: separate driver, semantic service, code generator and launcher; no interpreter is needed for v0.1.

## Future verification

Later measure cold/warm run, check/build latency, startup, executable dependencies and cache invalidation; compare exit behavior between build-then-run and run.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
