# 2.23 — Debugging and observability

> Decision: **ARCH-DEBUG-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[DX-014](../requirements/CORE.md#dx-014--debugger-support), [NET-024](../requirements/domains/networking.md#net-024--network-observability-hooks), [PERF-017](../requirements/PERFORMANCE.md#perf-017--evidence-before-claims), [PERF-018](../requirements/PERFORMANCE.md#perf-018--benchmark-methodology), [SEC-022](../requirements/domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs), [SEC-027](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds)

## Proposed decision and rationale

**Preserve source/type origins through lowering and expose opt-in, bounded observability; use platform debug formats.**

For Linux/macOS investigate DWARF emission through the native backend; for Windows use the compatible CodeView/PDB toolchain path after validation. The compiler maps source functions, lexical scopes, variables and inlined calls through HIR/MIR to machine locations. Optimized-out values are reported unavailable rather than fabricated. Private ownership metadata must not be mistaken for a stable public ABI.

v0.1 requires source-located faults and useful diagnostics; full debugger integration remains post-v0.1 per Phase 1. Development artifacts may include debug metadata and frame information, but debugger support is claimed only after stepping, breakpoints and value inspection pass on a target. Remap build paths for privacy and reproducibility.

Later async traces identify task/group parents and suspension points separately from native stack frames. Runtime events include queue pressure, task lifecycle, I/O completion and cancellation, using bounded buffers and explicit opt-in sampling. Logging and metrics must not become a hidden unbounded allocation path. No automatic telemetry upload or crash report transmission is enabled.

Fault reporting uses a minimal allocation-independent path; rich stack symbolization may happen out of process. Core dumps, traces and profile files can contain secrets, so collection and retention are opt-in policies. Compiler debug dumps also disclose source and paths and must be treated as user data.

## Options, advantages, disadvantages and rejected alternatives

A custom debugger protocol was rejected initially in favor of platform tools. Always-on detailed tracing was rejected for overhead/privacy. Full-fidelity optimized variable recovery cannot be promised. Source metadata plus staged platform validation is proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: debug artifacts and traces are sensitive; use path remapping and redaction. Performance: sampling/buffering overhead must be measured. DX: distinguish native stacks, logical tasks and unavailable values. Implementation: origin metadata, target debug adapters and bounded event schemas.

## Future verification

Later verify stepping and breakpoints across inlining, optimized-out values, remapped paths, task traces, crash reporting under exhaustion and trace backpressure.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
