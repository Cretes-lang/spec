# 2.26 — Automation architecture

> Decision: **ARCH-AUTO-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AUTO-001](../requirements/domains/automation.md#auto-001--single-file-programs), [AUTO-002](../requirements/domains/automation.md#auto-002--error-context-for-operational-failures), [AUTO-003](../requirements/domains/automation.md#auto-003--direct-execution-on-posix-systems), [AUTO-004](../requirements/domains/automation.md#auto-004--exit-status-and-termination-signals), [AUTO-005](../requirements/domains/automation.md#auto-005--timers), [AUTO-006](../requirements/domains/automation.md#auto-006--file-operations), [AUTO-007](../requirements/domains/automation.md#auto-007--file-metadata), [AUTO-008](../requirements/domains/automation.md#auto-008--path-abstraction), [AUTO-009](../requirements/domains/automation.md#auto-009--structured-process-creation), [AUTO-010](../requirements/domains/automation.md#auto-010--explicit-shell-invocation), [AUTO-011](../requirements/domains/automation.md#auto-011--process-supervision), [AUTO-012](../requirements/domains/automation.md#auto-012--standard-streams-and-pipes), [AUTO-013](../requirements/domains/automation.md#auto-013--environment-variables), [AUTO-014](../requirements/domains/automation.md#auto-014--shared-stream-abstractions), [AUTO-015](../requirements/domains/automation.md#auto-015--in-process-scheduling), [AUTO-016](../requirements/domains/automation.md#auto-016--json), [AUTO-017](../requirements/domains/automation.md#auto-017--structured-serialization), [AUTO-018](../requirements/domains/automation.md#auto-018--structured-configuration), [AUTO-019](../requirements/domains/automation.md#auto-019--command-line-application-support), [AUTO-020](../requirements/domains/automation.md#auto-020--logging), [AUTO-021](../requirements/domains/automation.md#auto-021--http-and-api-automation), [AUTO-022](../requirements/domains/automation.md#auto-022--archives-and-compression), [AUTO-023](../requirements/domains/automation.md#auto-023--concurrent-job-execution), [AUTO-024](../requirements/domains/automation.md#auto-024--cross-platform-os-abstractions), [AUTO-025](../requirements/domains/automation.md#auto-025--clocks-and-time), [AUTO-026](../requirements/domains/automation.md#auto-026--secure-temporary-files), [AUTO-027](../requirements/domains/automation.md#auto-027--filesystem-change-notification), [AUTO-028](../requirements/domains/automation.md#auto-028--distributing-command-line-tools)

## Proposed decision and rationale

**Synchronous safe helpers for small scripts, growing into structured jobs with the same data/error/resource model.**

v0.1 supports single-file run, raw arguments/exit status, files/directories, lossless paths, own standard streams, environment reads and monotonic/wall clocks. Text and bytes are distinct; stream adapters decode text explicitly and report invalid encoding. Environment mutation is excluded from the initial public API to avoid process-global races when concurrency arrives.

Later process creation takes executable plus an argument vector, explicit working directory/environment and inherited-handle policy. It never implicitly invokes a shell. Shell evaluation is a separate named operation with a clear injection boundary. Windows command-line encoding and POSIX argument vectors require platform-specific adapters and tests. Process handles are supervised: drain stdout/stderr concurrently, cap capture size, propagate cancellation/deadlines, preserve exit/signal information and reap children. Large output can stream to a consumer instead of being buffered entirely.

Filesystem metadata, secure temporary files and change notifications are separate OS-aware APIs. Temporary creation is atomic with restrictive permissions; archive extraction defends against path traversal, symlink escape and decompression bombs. Recursive traversal declares symlink policy and resource limits. Watcher events may coalesce or be lost; callers can rescan after overflow rather than assuming a perfect event log.

JSON, serialization, configuration, compression and HTTP clients are first-party packages after v0.1, sharing bounded parsing and structured errors. Configuration validation is separate from executing actions. Logging is structured and redacts secrets. In-process scheduling uses monotonic deadlines for durations and explicit timezone/calendar policy for wall-clock schedules; it is not a persistent distributed scheduler.

Approachability is a release criterion: copying a file, filtering text and reporting an error must not require explicit executor setup or user-written lifetime parameters. Higher-level helpers own temporary resources internally; expensive copies are explicit. Concurrency is opt-in task groups with bounded job counts. POSIX direct-execution launcher support is later, without freezing lexical shebang handling now.

## Options, advantages, disadvantages and rejected alternatives

Implicit shell-based execution was rejected for injection/portability. Async-only filesystem APIs were rejected for small-script complexity. Hidden unbounded process capture was rejected for memory risk. Synchronous helpers plus explicit structured concurrency are proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: default no-shell, restricted inheritance, secret redaction and safe temp/archive behavior. Performance: streaming avoids mandatory whole-file/process buffering. DX: direct single-file flow with actionable operation/resource errors. Implementation: portable helpers over the same platform/resource layer, not a second runtime.

## Future verification

Later walk through file-copy/log-filter/config tasks with new users; test quoting, large output, inherited handles, child termination, archive traversal and watcher overflow.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
