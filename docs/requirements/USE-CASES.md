# Core use cases

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This document describes concrete scenarios that Cretes is intended to serve. Each use case names its [persona](../vision/TARGET-USERS.md), describes the scenario, and traces to the requirements it depends on. Use cases justify requirements. A requirement that no use case, principle or policy needs should be questioned.

The requirement ID system, the MUST/SHOULD/MAY terminology and the traceability model are defined in the [requirements framework](README.md). Use-case identifiers (`UC-<DOMAIN>-NN`) are not requirements.

> Scenarios describe what developers will want to accomplish. They do not describe existing functionality and do not imply syntax.

## Contents

- [Automation](#automation)
- [Networking](#networking)
- [AI/ML Applications](#aiml-applications)
- [Cybersecurity](#cybersecurity)
- [Cross-cutting](#cross-cutting)
- [Coverage summary](#coverage-summary)

## Automation

### UC-AUTO-01 — File housekeeping script

| Field | Value |
| --- | --- |
| Persona | [Automation Engineer](../vision/TARGET-USERS.md#automation-engineers) |
| Scenario | Write one file that scans a directory tree, selects files by age and extension, archives them and deletes the originals. Run it on Linux and Windows with `cretes run`. |
| Success looks like | No project setup. Clear errors naming the failing path. Identical behavior on both platforms. Non-UTF-8 file names handled. |
| Key requirements | [AUTO-001](domains/automation.md#auto-001--single-file-programs), [AUTO-006](domains/automation.md#auto-006--file-operations), [AUTO-007](domains/automation.md#auto-007--file-metadata), [AUTO-008](domains/automation.md#auto-008--path-abstraction), [AUTO-022](domains/automation.md#auto-022--archives-and-compression), [AUTO-024](domains/automation.md#auto-024--cross-platform-os-abstractions), [CORE-022](CORE.md#core-022--explicit-recoverable-errors), [PLAT-009](PLATFORMS.md#plat-009--filesystem-and-path-portability) |
| First milestone | Partially v0.1 (files, paths). Metadata and archives come after v0.1. |

### UC-AUTO-02 — Build and release orchestration

| Field | Value |
| --- | --- |
| Persona | [DevOps / Platform Engineer](../vision/TARGET-USERS.md#devops--platform-engineers) |
| Scenario | A tool runs compilers, test suites and packaging commands as subprocesses, several in parallel. It streams their output with prefixes, stops everything on first failure or Ctrl-C, and returns a meaningful exit status. |
| Success looks like | No shell-injection risk from file names. No zombie processes. Output is not interleaved mid-line. Cancellation cleans up. |
| Key requirements | [AUTO-004](domains/automation.md#auto-004--exit-status-and-termination-signals), [AUTO-009](domains/automation.md#auto-009--structured-process-creation), [AUTO-010](domains/automation.md#auto-010--explicit-shell-invocation), [AUTO-011](domains/automation.md#auto-011--process-supervision), [AUTO-012](domains/automation.md#auto-012--standard-streams-and-pipes), [AUTO-023](domains/automation.md#auto-023--concurrent-job-execution), [CONC-004](CONCURRENCY.md#conc-004--structured-concurrency), [CONC-006](CONCURRENCY.md#conc-006--cancellation) |
| First milestone | After v0.1 |

### UC-AUTO-03 — Infrastructure API automation

| Field | Value |
| --- | --- |
| Persona | [DevOps / Platform Engineer](../vision/TARGET-USERS.md#devops--platform-engineers) |
| Scenario | Read a typed configuration file and credentials from the environment. Call a cloud provider's HTTP API with retries and timeouts. Reconcile desired and actual state. Log structured results. |
| Success looks like | The credential never appears in logs. Malformed configuration yields a precise error. Hung API calls time out. |
| Key requirements | [AUTO-013](domains/automation.md#auto-013--environment-variables), [AUTO-016](domains/automation.md#auto-016--json), [AUTO-018](domains/automation.md#auto-018--structured-configuration), [AUTO-020](domains/automation.md#auto-020--logging), [AUTO-021](domains/automation.md#auto-021--http-and-api-automation), [NET-010](domains/networking.md#net-010--timeouts-on-every-network-operation), [SEC-017](domains/cybersecurity.md#sec-017--key-and-credential-handling), [SEC-022](domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs) |
| First milestone | After v0.1 |

### UC-AUTO-04 — Distributable command-line tool

| Field | Value |
| --- | --- |
| Persona | [Systems / Tooling Developer](../vision/TARGET-USERS.md#systems--tooling-developers) |
| Scenario | Grow a script into a CLI tool with subcommands, help text and tests. Build self-contained executables for three platforms and publish it as a package. |
| Success looks like | The same source grows without a rewrite. Artifacts need no installed runtime. Startup is fast enough for shell use. |
| Key requirements | [AUTO-019](domains/automation.md#auto-019--command-line-application-support), [AUTO-028](domains/automation.md#auto-028--distributing-command-line-tools), [DX-003](CORE.md#dx-003--cretes-build), [DX-011](CORE.md#dx-011--integrated-test-runner), [PERF-001](PERFORMANCE.md#perf-001--self-contained-executables), [PERF-004](PERFORMANCE.md#perf-004--program-startup-latency), [PLAT-008](PLATFORMS.md#plat-008--cross-compilation) |
| First milestone | Partially v0.1 (arguments, build). Packaging and cross-compilation come after v0.1. |

## Networking

### UC-NET-01 — Concurrent TCP service

| Field | Value |
| --- | --- |
| Persona | [Backend / Network Engineer](../vision/TARGET-USERS.md#backend--network-engineers) |
| Scenario | Implement a line-based TCP service that serves thousands of concurrent clients, one task per connection. It enforces idle timeouts and shuts down gracefully on SIGTERM. |
| Success looks like | Straightforward per-connection code. Bounded memory under slow clients. No leaked sockets. |
| Key requirements | [NET-002](domains/networking.md#net-002--scalable-asynchronous-io), [NET-003](domains/networking.md#net-003--connection-scale-design-target), [NET-006](domains/networking.md#net-006--tcp-clients-and-servers), [NET-010](domains/networking.md#net-010--timeouts-on-every-network-operation), [NET-013](domains/networking.md#net-013--backpressure), [NET-022](domains/networking.md#net-022--concurrent-server-foundation), [CONC-004](CONCURRENCY.md#conc-004--structured-concurrency), [SAFE-013](SAFETY.md#safe-013--deterministic-resource-release) |
| First milestone | After v0.1 |

### UC-NET-02 — HTTPS API client

| Field | Value |
| --- | --- |
| Persona | [Backend / Network Engineer](../vision/TARGET-USERS.md#backend--network-engineers) |
| Scenario | Call a remote JSON API over HTTPS with connection reuse, timeouts and structured error handling that distinguishes DNS, TLS, timeout and HTTP-status failures. |
| Success looks like | Certificate verification is on by default. Retries can branch on error kind. |
| Key requirements | [NET-009](domains/networking.md#net-009--name-resolution), [NET-014](domains/networking.md#net-014--structured-network-errors), [NET-017](domains/networking.md#net-017--tls), [NET-018](domains/networking.md#net-018--http-client), [NET-021](domains/networking.md#net-021--connection-management-and-pooling), [NET-023](domains/networking.md#net-023--secure-network-defaults), [SEC-018](domains/cybersecurity.md#sec-018--tls-security-policy) |
| First milestone | After v0.1 |

### UC-NET-03 — Binary protocol implementation

| Field | Value |
| --- | --- |
| Persona | [Backend / Network Engineer](../vision/TARGET-USERS.md#backend--network-engineers) |
| Scenario | Implement a custom length-prefixed binary protocol over TCP and UDP. The parser must be incremental and must reject malformed frames. |
| Success looks like | Truncated or hostile input produces errors, never crashes. The parser is fuzz-tested. |
| Key requirements | [NET-001](domains/networking.md#net-001--byte-oriented-data), [NET-007](domains/networking.md#net-007--udp), [NET-012](domains/networking.md#net-012--streaming), [NET-015](domains/networking.md#net-015--binary-data-encoding), [NET-016](domains/networking.md#net-016--incremental-protocol-parsing), [SEC-002](domains/cybersecurity.md#sec-002--bounds-checked-binary-parsing), [SEC-030](domains/cybersecurity.md#sec-030--fuzzing-support) |
| First milestone | After v0.1 (byte types are in v0.1) |

### UC-NET-04 — Real-time streaming gateway

| Field | Value |
| --- | --- |
| Persona | [Backend / Network Engineer](../vision/TARGET-USERS.md#backend--network-engineers) |
| Scenario | Relay messages from an upstream stream to many WebSocket clients. Slow clients must not exhaust memory. |
| Success looks like | Backpressure or bounded buffering per client, and observable metrics. |
| Key requirements | [NET-013](domains/networking.md#net-013--backpressure), [NET-020](domains/networking.md#net-020--websockets), [NET-024](domains/networking.md#net-024--network-observability-hooks), [CONC-011](CONCURRENCY.md#conc-011--message-passing), [CONC-012](CONCURRENCY.md#conc-012--backpressure) |
| First milestone | After v0.1 |

## AI/ML Applications

### UC-AI-01 — Inference service

| Field | Value |
| --- | --- |
| Persona | [AI/ML Application Developer](../vision/TARGET-USERS.md#aiml-application-developers) |
| Scenario | Load an exported model with an established inference runtime. Serve predictions over HTTP. Batch concurrent requests and pass tensors to the runtime without copying. |
| Success looks like | Predictable latency, memory ownership that is clear at the FFI boundary, and CPU execution everywhere. |
| Key requirements | [AI-008](domains/ai-ml.md#ai-008--tensor-compatible-layout-descriptors), [AI-012](domains/ai-ml.md#ai-012--model-inference-through-established-runtimes), [AI-018](domains/ai-ml.md#ai-018--cpu-execution-first), [INTOP-001](INTEROPERABILITY.md#intop-001--calling-c-abi-functions), [INTOP-005](INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary), [NET-018](domains/networking.md#net-018--http-client), [NET-019](domains/networking.md#net-019--http-server-foundation), [PERF-010](PERFORMANCE.md#perf-010--memory-footprint-and-control) |
| First milestone | After v0.1 |

### UC-AI-02 — Data preprocessing pipeline

| Field | Value |
| --- | --- |
| Persona | [AI/ML Application Developer](../vision/TARGET-USERS.md#aiml-application-developers) |
| Scenario | Stream a multi-gigabyte dataset from disk. Decode and normalize records in parallel on all cores. Write contiguous numeric arrays in a format readable by established tools. |
| Success looks like | Constant memory use, all cores busy, vectorized kernels and reproducible output. |
| Key requirements | [AI-005](domains/ai-ml.md#ai-005--contiguous-arrays), [AI-006](domains/ai-ml.md#ai-006--buffer-views), [AI-010](domains/ai-ml.md#ai-010--vectorized-computation), [AI-011](domains/ai-ml.md#ai-011--parallel-numerical-computation), [AI-014](domains/ai-ml.md#ai-014--memory-efficient-data-handling), [AI-016](domains/ai-ml.md#ai-016--tensor-and-model-serialization), [AI-022](domains/ai-ml.md#ai-022--reproducible-numerical-results), [PERF-015](PERFORMANCE.md#perf-015--numerical-throughput) |
| First milestone | After v0.1 |

### UC-AI-03 — Model-calling agent tool

| Field | Value |
| --- | --- |
| Persona | [AI/ML Application Developer](../vision/TARGET-USERS.md#aiml-application-developers) |
| Scenario | A command-line tool calls a hosted model API with streaming responses. It executes the tool actions the model requests, such as file reads and HTTP calls, under explicit allow-lists, and logs its actions. |
| Success looks like | API keys are protected. Subprocesses cannot be shell-injected. Timeouts and cancellation are reliable. |
| Key requirements | [AI-023](domains/ai-ml.md#ai-023--hosted-model-api-clients), [AUTO-009](domains/automation.md#auto-009--structured-process-creation), [AUTO-010](domains/automation.md#auto-010--explicit-shell-invocation), [AUTO-020](domains/automation.md#auto-020--logging), [CONC-007](CONCURRENCY.md#conc-007--deadlines-and-timeouts), [SEC-017](domains/cybersecurity.md#sec-017--key-and-credential-handling), [SEC-022](domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs) |
| First milestone | After v0.1 |

### UC-AI-04 — Loading model weights safely

| Field | Value |
| --- | --- |
| Persona | [AI/ML Application Developer](../vision/TARGET-USERS.md#aiml-application-developers) |
| Scenario | Memory-map a large weight file from an untrusted source and validate its header before use. |
| Success looks like | No code execution from the file. Size and shape mismatches are rejected. Memory use is bounded. |
| Key requirements | [AI-014](domains/ai-ml.md#ai-014--memory-efficient-data-handling), [AI-016](domains/ai-ml.md#ai-016--tensor-and-model-serialization), [AI-017](domains/ai-ml.md#ai-017--safe-model-and-data-loading), [SEC-003](domains/cybersecurity.md#sec-003--checked-length-arithmetic-in-parsers), [SEC-021](domains/cybersecurity.md#sec-021--resource-limits-for-untrusted-input) |
| First milestone | After v0.1 |

## Cybersecurity

### UC-SEC-01 — Secure file encryption utility

| Field | Value |
| --- | --- |
| Persona | [Cybersecurity Engineer](../vision/TARGET-USERS.md#cybersecurity-engineers) |
| Scenario | Encrypt and decrypt files with a password. Derive the key with a memory-hard function and encrypt with an AEAD. Keys are wiped after use. |
| Success looks like | The developer never chooses a nonce or a cipher mode. Keys never reach logs. Tampered files are rejected. |
| Key requirements | [SEC-005](domains/cybersecurity.md#sec-005--secret-zeroization), [SEC-006](domains/cybersecurity.md#sec-006--secure-randomness), [SEC-010](domains/cybersecurity.md#sec-010--authenticated-encryption), [SEC-013](domains/cybersecurity.md#sec-013--key-derivation-and-password-hashing), [SEC-014](domains/cybersecurity.md#sec-014--misuse-resistant-api-layering), [SEC-022](domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs) |
| First milestone | After v0.1 |

### UC-SEC-02 — Packet and protocol analyzer

| Field | Value |
| --- | --- |
| Persona | [Cybersecurity Engineer](../vision/TARGET-USERS.md#cybersecurity-engineers) |
| Scenario | Parse captured network traffic, including hostile and malformed packets, to extract protocol fields for defensive monitoring. |
| Success looks like | The parser cannot be exploited by crafted packets. It achieves high throughput. Privileged capture is platform-specific and explicit. |
| Key requirements | [SEC-001](domains/cybersecurity.md#sec-001--memory-safe-development-objective), [SEC-002](domains/cybersecurity.md#sec-002--bounds-checked-binary-parsing), [SEC-003](domains/cybersecurity.md#sec-003--checked-length-arithmetic-in-parsers), [NET-008](domains/networking.md#net-008--local-and-low-level-sockets), [NET-015](domains/networking.md#net-015--binary-data-encoding), [NET-016](domains/networking.md#net-016--incremental-protocol-parsing), [SAFE-002](SAFETY.md#safe-002--spatial-memory-safety), [PERF-013](PERFORMANCE.md#perf-013--efficient-io-buffers) |
| First milestone | After v0.1 |

### UC-SEC-03 — Certificate and TLS configuration auditor

| Field | Value |
| --- | --- |
| Persona | [Cybersecurity Engineer](../vision/TARGET-USERS.md#cybersecurity-engineers) |
| Scenario | Connect to an organization's own endpoints, retrieve certificate chains, validate them and report expiring certificates and weak configurations. |
| Success looks like | Correct chain validation. Legacy algorithms can be detected without being enabled as defaults. |
| Key requirements | [SEC-016](domains/cybersecurity.md#sec-016--algorithm-agility-and-legacy-algorithms), [SEC-018](domains/cybersecurity.md#sec-018--tls-security-policy), [SEC-019](domains/cybersecurity.md#sec-019--certificate-handling), [NET-017](domains/networking.md#net-017--tls), [NET-023](domains/networking.md#net-023--secure-network-defaults), [AUTO-023](domains/automation.md#auto-023--concurrent-job-execution) |
| First milestone | After v0.1 |

### UC-SEC-04 — Dependency supply-chain audit

| Field | Value |
| --- | --- |
| Persona | [Cybersecurity Engineer](../vision/TARGET-USERS.md#cybersecurity-engineers) |
| Scenario | Before deployment, verify dependency integrity. List every unsafe region, FFI declaration and build-time code execution in the dependency tree. Check advisories and emit an SBOM. |
| Success looks like | All information is available from the toolchain without executing dependency code. |
| Key requirements | [SEC-023](domains/cybersecurity.md#sec-023--dependency-integrity), [SEC-025](domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation), [SEC-026](domains/cybersecurity.md#sec-026--vulnerability-advisories-and-audit), [SEC-028](domains/cybersecurity.md#sec-028--software-bill-of-materials), [SEC-029](domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting), [CORE-028](CORE.md#core-028--declarative-package-manifest) |
| First milestone | After v0.1 |

## Cross-cutting

### UC-X-01 — First program

| Field | Value |
| --- | --- |
| Persona | Any newcomer to Cretes |
| Scenario | Install the toolchain and verify its checksum. Write a small program that reads a file and counts words. Check it, run it and fix a mistake guided by diagnostics. |
| Success looks like | Installation is verifiable. Diagnostics point to the exact span and suggest a fix. The program runs identically on each supported platform. |
| Key requirements | [PLAT-013](PLATFORMS.md#plat-013--toolchain-installation), [DX-002](CORE.md#dx-002--cretes-check), [DX-004](CORE.md#dx-004--cretes-run), [DX-005](CORE.md#dx-005--diagnostic-content), [CORE-032](CORE.md#core-032--text-operations), [CORE-033](CORE.md#core-033--core-collections), [AUTO-006](domains/automation.md#auto-006--file-operations) |
| First milestone | **v0.1** |

### UC-X-02 — Wrapping a native C library

| Field | Value |
| --- | --- |
| Persona | [Systems / Tooling Developer](../vision/TARGET-USERS.md#systems--tooling-developers) |
| Scenario | Generate bindings for a C compression library. Wrap them in a safe interface that owns buffers correctly, and publish a package that declares its native dependency. |
| Success looks like | Unsafe code is confined to the wrapper. Errors from C are translated. Audit tools list the native dependency. |
| Key requirements | [INTOP-001](INTEROPERABILITY.md#intop-001--calling-c-abi-functions), [INTOP-003](INTEROPERABILITY.md#intop-003--c-compatible-data-layout), [INTOP-005](INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary), [INTOP-006](INTEROPERABILITY.md#intop-006--safe-wrappers), [INTOP-007](INTEROPERABILITY.md#intop-007--error-propagation-across-the-boundary), [INTOP-009](INTEROPERABILITY.md#intop-009--binding-generation), [INTOP-019](INTEROPERABILITY.md#intop-019--declared-native-dependencies), [SAFE-016](SAFETY.md#safe-016--explicit-and-auditable-unsafe-code), [SAFE-017](SAFETY.md#safe-017--safe-abstractions-over-unsafe-code) |
| First milestone | After v0.1 |

### UC-X-03 — Editor-driven development

| Field | Value |
| --- | --- |
| Persona | All personas |
| Scenario | Work in an editor with live diagnostics, navigation, formatting and debugging, on a project with many modules. |
| Success looks like | Feedback is fast. Tools agree with the compiler. Breakpoints work on each Tier 1 platform. |
| Key requirements | [DX-006](CORE.md#dx-006--machine-readable-diagnostics), [DX-009](CORE.md#dx-009--canonical-formatter), [DX-012](CORE.md#dx-012--language-server), [DX-014](CORE.md#dx-014--debugger-support), [DX-017](CORE.md#dx-017--consistent-semantics-across-tools), [CORE-009](CORE.md#core-009--name-resolution-without-execution), [PERF-005](PERFORMANCE.md#perf-005--toolchain-responsiveness), [PERF-007](PERFORMANCE.md#perf-007--incremental-builds) |
| First milestone | Partially v0.1 (diagnostics). Editor tooling comes after v0.1. |

## Coverage summary

| Domain | Use cases | Earliest milestone touched |
| --- | ---: | --- |
| Automation | 4 | v0.1 (UC-AUTO-01, UC-AUTO-04 partially) |
| Networking | 4 | After v0.1 |
| AI/ML Applications | 4 | After v0.1 |
| Cybersecurity | 4 | After v0.1 |
| Cross-cutting | 3 | v0.1 (UC-X-01) |

v0.1 directly serves UC-X-01 and parts of UC-AUTO-01, UC-AUTO-04 and UC-X-03. The other use cases depend on post-v0.1 milestones, which are enabled by the architecture obligations in [V0.1-REQUIREMENTS.md](V0.1-REQUIREMENTS.md#architecture-obligations-beyond-v01).

## Related documents

- [Target developers](../vision/TARGET-USERS.md)
- [Requirements framework](README.md)
- [v0.1 requirements](V0.1-REQUIREMENTS.md)
