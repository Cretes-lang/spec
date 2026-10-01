# 2.20 — Toolchain and developer tools

> Decision: **ARCH-TOOLCHAIN-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AUTO-001](../requirements/domains/automation.md#auto-001--single-file-programs), [DX-001](../requirements/CORE.md#dx-001--single-toolchain-entry-point), [DX-002](../requirements/CORE.md#dx-002--cretes-check), [DX-003](../requirements/CORE.md#dx-003--cretes-build), [DX-004](../requirements/CORE.md#dx-004--cretes-run), [DX-005](../requirements/CORE.md#dx-005--diagnostic-content), [DX-006](../requirements/CORE.md#dx-006--machine-readable-diagnostics), [DX-007](../requirements/CORE.md#dx-007--error-recovery), [DX-008](../requirements/CORE.md#dx-008--robustness-on-malformed-input), [DX-009](../requirements/CORE.md#dx-009--canonical-formatter), [DX-010](../requirements/CORE.md#dx-010--linter), [DX-011](../requirements/CORE.md#dx-011--integrated-test-runner), [DX-012](../requirements/CORE.md#dx-012--language-server), [DX-013](../requirements/CORE.md#dx-013--documentation-generator), [DX-014](../requirements/CORE.md#dx-014--debugger-support), [DX-015](../requirements/CORE.md#dx-015--package-manager-and-registry), [DX-016](../requirements/CORE.md#dx-016--online-playground), [DX-017](../requirements/CORE.md#dx-017--consistent-semantics-across-tools), [DX-018](../requirements/CORE.md#dx-018--release-documentation), [DX-019](../requirements/CORE.md#dx-019--scriptable-command-line-behavior)

## Proposed decision and rationale

**One public cretes driver with reusable compiler services and explicitly staged future commands.**

| Command family | Responsibility | Milestone |
| --- | --- | --- |
| check | Resolve/type/safety analysis; no artifact execution | v0.1 |
| build | Check, lower, generate and link declared target | v0.1 |
| run | Build/cache then launch, preserving program argument boundary | v0.1 |
| test / bench | Discover/run tests and reproducible measurements | Later |
| fmt / lint / doc | Syntax-preserving formatting, analysis and reference generation | Later, after grammar |
| add / remove / update | Explicit dependency graph changes | Later package-manager milestone |
| clean | Remove only owned build/cache artifacts | Later; safe path validation required |

The driver shares configuration, diagnostics and target selection. It separates compiler output from program stdout; diagnostics go to stderr or a chosen machine-readable stream. Exit statuses distinguish tool failure from child program results. Run forwards signals/termination consistently and reports whether failure occurred during compilation or execution.

Single-file use has a documented implicit project and requires no registry access. Multi-module use consumes a declarative manifest. Version output identifies compiler/runtime/backend provenance. CLI help and release documentation describe only implemented commands; future command names here are architecture intentions, not a promise that executable tools exist.

The future LSP, formatter and documentation tools share source and semantic services but can recover from incomplete code. They must not implement a second type system. Formatting cannot execute code or normalize source in a way that changes meaning. Tool plugins cannot implicitly run through configuration discovery.

## Options, advantages, disadvantages and rejected alternatives

Independent unrelated executables/configuration were rejected because they fragment semantics. A monolithic driver implementation was rejected; one user entry point can delegate to modular services. Implementing every command now is explicitly rejected as out of phase.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: no implicit network/install actions from check/build. Performance: persistent analysis can reuse snapshots after v0.1. DX: consistent options, diagnostics and command boundaries. Implementation: CLI parsing, session setup, service APIs and child supervision are separate units.

## Future verification

Later test CLI exit/status streams, argument forwarding, cancellation, machine output, cache invalidation, offline builds and help matching shipped capabilities.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
