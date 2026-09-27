# Automation requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

Automation is one of the four official Cretes domains. This document covers:

- task automation;
- system administration;
- build and deployment tooling;
- data processing scripts;
- command-line applications.

The primary personas are the [Automation Engineer](../../vision/TARGET-USERS.md#automation-engineers) and the [DevOps / Platform Engineer](../../vision/TARGET-USERS.md#devops--platform-engineers).

Requirements are grouped by the **layer** responsible for them, so that capabilities are not pushed into language syntax unnecessarily. Most automation capability belongs in the standard library. Terminology, layers and targets are defined in the [requirements framework](../README.md).

## Contents

- [Domain goals](#domain-goals)
- [Language requirements](#language-requirements)
- [Runtime requirements](#runtime-requirements)
- [Standard-library requirements](#standard-library-requirements)
- [Ecosystem requirements](#ecosystem-requirements)
- [Related cross-cutting requirements](#related-cross-cutting-requirements)

## Domain goals

1. Writing a small automation program should feel as direct as writing a script. It should not require project scaffolding.
2. The same program should be able to grow into a maintained, tested, distributable tool without a rewrite.
3. Interacting with processes, files and the environment should be safe by default. Shell-injection and path-traversal bugs should require deliberate effort to introduce.
4. Automation should work identically on Linux, Windows and macOS wherever the underlying capability exists.

## Language requirements

### AUTO-001 — Single-file programs

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** A single `.cretes` file must be runnable through `cretes run` ([DX-004](../CORE.md#dx-004--cretes-run)) without a manifest or project directory. It may use only the standard library.
- **Rationale:** Small automation tasks must have a near-zero setup cost ([Principle 3](../../principles/DESIGN-PRINCIPLES.md#3-simple-common-cases)).
- **Verification:** Integration tests.

### AUTO-002 — Error context for operational failures

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Propagating an error from an operation, such as opening a file or running a process, must be concise enough for everyday use. It must also allow context to be added, such as which file was being opened ([CORE-022](../CORE.md#core-022--explicit-recoverable-errors), [CORE-024](../CORE.md#core-024--structured-error-information)).
- **Rationale:** Automation code is dominated by fallible operations. If explicit error handling is too verbose, programmers will suppress errors instead.
- **Verification:** Conformance tests; Inspection of examples.

### AUTO-003 — Direct execution on POSIX systems

- **Priority:** MAY · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** The lexical design may allow a source file to begin with an interpreter directive line (`#!`) so that it can be executed directly on POSIX systems. The lexical form itself is a Phase 2 decision.
- **Rationale:** A common convenience for scripts. It must not constrain the rest of the lexical design.
- **Verification:** Integration tests.

## Runtime requirements

### AUTO-004 — Exit status and termination signals

- **Priority:** MUST · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** Programs must be able to respond to termination requests, such as SIGINT/SIGTERM on POSIX and console control events on Windows, by initiating orderly shutdown. Shutdown should use cancellation ([CONC-006](../CONCURRENCY.md#conc-006--cancellation)). The default behavior on such a request must be documented.
- **Rationale:** Long-running automation must clean up temporary files, child processes and locks on interruption.
- **Verification:** Integration tests under Platform CI.

### AUTO-005 — Timers

- **Priority:** MUST · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** Programs must be able to sleep and to schedule work after a delay or at intervals, measured with a monotonic clock. Timers must integrate with concurrency ([CONC-002](../CONCURRENCY.md#conc-002--non-blocking-waiting)).
- **Rationale:** Polling, retries with backoff and periodic jobs are basic automation patterns.
- **Verification:** Unit tests.

## Standard-library requirements

### AUTO-006 — File operations

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** The standard library must support:
  - reading and writing whole files and streams;
  - appending;
  - creating, renaming, copying and removing files;
  - creating, listing and removing directories.

  Each must report failures as structured errors. Recursive directory traversal is required after v0.1. It must not follow symbolic links unless requested.
- **Rationale:** Filesystem work is the core of most automation.
- **Verification:** Unit tests under Platform CI.

### AUTO-007 — File metadata

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must expose file type, size, modification time and permissions through a portable interface. Platform-specific metadata, such as POSIX mode bits and ownership or Windows attributes, must be available through clearly platform-specific extensions. Symbolic links must be distinguishable from their targets.
- **Rationale:** Backup, synchronization, cleanup and security-audit scripts depend on metadata.
- **Verification:** Unit tests under Platform CI.

### AUTO-008 — Path abstraction

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Paths must be represented by a dedicated abstraction, not plain text. It must support joining, splitting, extension handling and normalization. It must losslessly represent paths that are not valid Unicode ([PLAT-009](../PLATFORMS.md#plat-009--filesystem-and-path-portability)).
- **Rationale:** Building paths by concatenating strings is a source of portability and path-traversal bugs.
- **Verification:** Unit tests under Platform CI.

### AUTO-009 — Structured process creation

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must launch operating-system processes from a program path and an **argument vector** that is passed without shell interpretation. It must allow control of environment variables, working directory and standard stream redirection.
- **Rationale:** Structured arguments eliminate shell-injection vulnerabilities by construction.
- **Verification:** Unit tests under Platform CI; Security review.

### AUTO-010 — Explicit shell invocation

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Executing a command line through a system shell must be a separate, explicitly named operation. It must never be the default behavior of process creation. Its documentation must describe injection risks.
- **Rationale:** Shell pipelines are sometimes useful, but implicit shell execution is a leading cause of command injection ([Principle 1](../../principles/DESIGN-PRINCIPLES.md#1-safety-by-default)).
- **Verification:** Inspection; Security review.

### AUTO-011 — Process supervision

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Programs must be able to:
  - wait for a child process, with a timeout;
  - obtain its exit status or terminating signal;
  - request termination and force-kill it.

  Terminated children must be reaped. Child processes started within a cancelled scope must have a documented cleanup behavior.
- **Rationale:** Automation orchestrates many subprocesses. Leaked or zombie processes cause resource exhaustion.
- **Verification:** Integration tests under Platform CI.

### AUTO-012 — Standard streams and pipes

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Programs must be able to read standard input and to write standard output and standard error. For child processes (post-v0.1), programs must be able to capture or stream output, supply input and connect processes with pipes. Capturing both output streams must not risk deadlock.
- **Rationale:** Composition through streams is fundamental to CLI tools. Naive pipe handling commonly deadlocks.
- **Verification:** Integration tests.

### AUTO-013 — Environment variables

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Programs must be able to read environment variables, including values that are not valid Unicode. Modifying the current process environment must be designed so that it cannot cause data races or memory unsafety in safe code, for example with concurrently running threads or foreign code. Setting variables for child processes must not require mutating the parent's environment.
- **Rationale:** On several platforms, modifying the process environment is not thread-safe. This is a known source of memory corruption.
- **Verification:** Unit tests; Security review.

### AUTO-014 — Shared stream abstractions

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Files, standard streams, pipes and (later) sockets must share common byte-stream and text-stream abstractions. The abstractions must include buffered reading and writing, and line-oriented reading of text.
- **Rationale:** Generic code, such as a log processor, should work on any source.
- **Verification:** Unit tests.

### AUTO-015 — In-process scheduling

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library should support running jobs on intervals and at wall-clock times from within a program, with cancellation. Integration with OS schedulers, such as cron, systemd timers or Windows Task Scheduler, is left to the ecosystem.
- **Rationale:** Periodic jobs are common. System-scheduler integration is platform-specific and better served by packages.
- **Verification:** Unit tests.

### AUTO-016 — JSON

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must parse and produce JSON (RFC 8259) strictly. It must enforce configurable limits on nesting depth and input size ([SEC-021](cybersecurity.md#sec-021--resource-limits-for-untrusted-input)), and preserve numeric precision or report loss.
- **Rationale:** JSON is the lingua franca of APIs and configuration.
- **Verification:** Unit tests; Fuzzing; Conformance against published JSON test suites.

### AUTO-017 — Structured serialization

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library should provide a mechanism for mapping user-defined types to and from structured data formats, starting with JSON. The mechanism should not require hand-written conversion code for each type. Other formats, such as TOML, YAML and CSV, may be provided by first-party or ecosystem packages. Deserialization must never execute code chosen by the input ([AI-017](ai-ml.md#ai-017--safe-model-and-data-loading)).
- **Rationale:** Configuration and API handling are dominated by data mapping. Deserialization is a classic attack vector.
- **Verification:** Unit tests; Security review.

### AUTO-018 — Structured configuration

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should provide a way to load configuration from files, environment variables and command-line arguments into typed structures, with validation errors that name the offending source and key.
- **Rationale:** Every deployable tool needs configuration. Consistent handling improves operability.
- **Verification:** Unit tests.

### AUTO-019 — Command-line application support

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Programs must be able to access their raw arguments as values that support non-Unicode input, and to set their exit status ([CORE-027](../CORE.md#core-027--program-entry-and-exit)). After v0.1, the standard library SHOULD provide argument parsing with generated help and usage errors.
- **Rationale:** CLI tools are the primary deliverable of automation work.
- **Verification:** Integration tests.

### AUTO-020 — Logging

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide a logging interface with severity levels and structured key-value fields, and with pluggable output destinations. Values of secret types must be redacted by default ([SEC-022](cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs)).
- **Rationale:** A common logging interface lets libraries log without choosing a backend. Leaked credentials in logs are a frequent incident cause.
- **Verification:** Unit tests; Security review.

### AUTO-021 — HTTP and API automation

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Automation programs should be able to call HTTP APIs with JSON bodies, authentication headers, timeouts and retries, using the networking foundation ([NET-018](networking.md#net-018--http-client)).
- **Rationale:** Most modern infrastructure is controlled through HTTP APIs.
- **Verification:** Integration tests.

### AUTO-022 — Archives and compression

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should support reading and writing common archive formats, such as tar and zip, and compression formats, such as gzip. Extraction must reject entries that would escape the destination directory, including "zip slip" and symbolic-link escapes. It must also enforce limits on decompressed size.
- **Rationale:** Packaging and deployment rely on archives. Unsafe extraction and decompression bombs are well-known vulnerabilities.
- **Verification:** Unit tests; Fuzzing; Security review.

### AUTO-023 — Concurrent job execution

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Programs must be able to run many jobs, such as subprocesses, file operations or HTTP calls, concurrently. Programs must be able to limit the degree of concurrency, collect individual results and errors, and cancel remaining jobs on failure or interruption ([CONC-004](../CONCURRENCY.md#conc-004--structured-concurrency), [CONC-008](../CONCURRENCY.md#conc-008--error-propagation)).
- **Rationale:** Fan-out over hosts, files or services is a defining automation workload.
- **Verification:** Integration tests.

### AUTO-024 — Cross-platform OS abstractions

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** The automation facilities in this document must behave consistently on all supported platforms wherever the underlying capability exists. Unavoidable differences must be documented per interface ([PLAT-006](../PLATFORMS.md#plat-006--portable-behavior)).
- **Rationale:** Automation scripts are often shared between Windows and Unix-like environments.
- **Verification:** Unit tests under Platform CI.

### AUTO-025 — Clocks and time

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** The standard library must distinguish monotonic time, used for measuring durations, from wall-clock time. It must format and parse timestamps in RFC 3339 / ISO 8601 form in UTC. Time-zone database support SHOULD be available post-v0.1, from the standard library or a first-party package.
- **Rationale:** Confusing wall-clock and monotonic time causes timeout and scheduling bugs.
- **Verification:** Unit tests.

### AUTO-026 — Secure temporary files

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library should create temporary files and directories with unpredictable names, exclusive creation and restrictive permissions. Removal should be tied to scope ([SAFE-013](../SAFETY.md#safe-013--deterministic-resource-release)).
- **Rationale:** Predictable temporary files are a classic local privilege-escalation vector.
- **Verification:** Unit tests; Security review.

### AUTO-027 — Filesystem change notification

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should provide an interface for observing filesystem changes, built on platform notification facilities.
- **Rationale:** Build tools, synchronization and monitoring agents react to file changes.
- **Verification:** Integration tests under Platform CI.

## Ecosystem requirements

### AUTO-028 — Distributing command-line tools

- **Priority:** SHOULD · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** The package manager ([DX-015](../CORE.md#dx-015--package-manager-and-registry)) should support installing command-line tools published as packages, with the same integrity verification as library dependencies ([SEC-023](cybersecurity.md#sec-023--dependency-integrity)).
- **Rationale:** Sharing tools is how an automation ecosystem grows.
- **Verification:** Integration tests.

## Related cross-cutting requirements

| Topic | Requirements |
| --- | --- |
| Structured errors | [CORE-022](../CORE.md#core-022--explicit-recoverable-errors), [CORE-024](../CORE.md#core-024--structured-error-information) |
| Cancellation and timeouts | [CONC-006](../CONCURRENCY.md#conc-006--cancellation), [CONC-007](../CONCURRENCY.md#conc-007--deadlines-and-timeouts) |
| Resource cleanup | [SAFE-013](../SAFETY.md#safe-013--deterministic-resource-release) |
| Startup latency | [PERF-004](../PERFORMANCE.md#perf-004--program-startup-latency) |
| Portability | [PLAT-006](../PLATFORMS.md#plat-006--portable-behavior), [PLAT-009](../PLATFORMS.md#plat-009--filesystem-and-path-portability) |
| Secrets in logs | [SEC-022](cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs) |
