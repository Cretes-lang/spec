# Phase 1 to Phase 2 traceability

> Status: PROPOSED responses · Implementation: Not started · Baseline: spec d5f0f2b, with editorial corrections through 36d709e · Date: 2026-09-27

Every one of the 257 Phase 1 requirements appears exactly once below, including all 173 MUST requirements. A row assigns an architectural response and future verification obligation; it does not claim the requirement is implemented or verified. The original milestone remains unchanged. Later-milestone responses constrain foundations without adding features to v0.1.

All architecture decisions are PROPOSED pending RFC acceptance. Detailed follow-ups marked DEFERRED in RISKS.md remain explicit release gates. In particular, SAFE-023 requires an accepted memory RFC and is not satisfied by this proposed mapping.

[Architecture index](README.md) · [Question disposition](QUESTIONS.md)

## CORE

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [CORE-001 — Source file extension](../requirements/CORE.md#core-001--source-file-extension) | MUST | v0.1 | [ARCH-PIPELINE-001](PIPELINE.md) — Compilation pipeline and invariants; PROPOSED | Integration tests. |
| [CORE-002 — Source encoding](../requirements/CORE.md#core-002--source-encoding) | MUST | v0.1 | [ARCH-PIPELINE-001](PIPELINE.md) — Compilation pipeline and invariants; PROPOSED | Conformance tests; Fuzzing. |
| [CORE-003 — Platform-independent line structure](../requirements/CORE.md#core-003--platform-independent-line-structure) | MUST | v0.1 | [ARCH-PIPELINE-001](PIPELINE.md) — Compilation pipeline and invariants; PROPOSED | Conformance tests. |
| [CORE-004 — Unicode identifiers policy](../requirements/CORE.md#core-004--unicode-identifiers-policy) | SHOULD | Before 1.0 | [ARCH-PIPELINE-001](PIPELINE.md) — Compilation pipeline and invariants; PROPOSED | Specification review; Conformance tests. |
| [CORE-005 — Protection against deceptive source text](../requirements/CORE.md#core-005--protection-against-deceptive-source-text) | MUST | v0.1 | [ARCH-PIPELINE-001](PIPELINE.md) — Compilation pipeline and invariants; PROPOSED | Conformance tests; Diagnostic tests; Security review. |
| [CORE-006 — Text distinct from bytes](../requirements/CORE.md#core-006--text-distinct-from-bytes) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests; Unit tests. |
| [CORE-007 — Modules](../requirements/CORE.md#core-007--modules) | MUST | v0.1 | [ARCH-MODULE-001](MODULE.md) — Modules and initialization; PROPOSED | Conformance tests; Integration tests. |
| [CORE-008 — Visibility control](../requirements/CORE.md#core-008--visibility-control) | MUST | v0.1 | [ARCH-MODULE-001](MODULE.md) — Modules and initialization; PROPOSED | Conformance tests. |
| [CORE-009 — Name resolution without execution](../requirements/CORE.md#core-009--name-resolution-without-execution) | MUST | v0.1 | [ARCH-MODULE-001](MODULE.md) — Modules and initialization; PROPOSED | Specification review; Conformance tests. |
| [CORE-010 — Controlled module initialization](../requirements/CORE.md#core-010--controlled-module-initialization) | SHOULD | v0.1 | [ARCH-MODULE-001](MODULE.md) — Modules and initialization; PROPOSED | Specification review; Conformance tests. |
| [CORE-011 — Mutable and immutable bindings](../requirements/CORE.md#core-011--mutable-and-immutable-bindings) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests; Diagnostic tests. |
| [CORE-012 — User-defined data types](../requirements/CORE.md#core-012--user-defined-data-types) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [CORE-013 — Specified evaluation order](../requirements/CORE.md#core-013--specified-evaluation-order) | MUST | v0.1 | [ARCH-V0.1-ARCHITECTURE-001](V0.1-ARCHITECTURE.md) — v0.1 implementation blueprint; PROPOSED | Specification review; Conformance tests. |
| [CORE-014 — Control flow](../requirements/CORE.md#core-014--control-flow) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [CORE-015 — Functions](../requirements/CORE.md#core-015--functions) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [CORE-016 — Functions as values](../requirements/CORE.md#core-016--functions-as-values) | SHOULD | Post-v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [CORE-017 — Errors detected before execution](../requirements/CORE.md#core-017--errors-detected-before-execution) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests; Diagnostic tests. |
| [CORE-018 — Primitive types with defined representation](../requirements/CORE.md#core-018--primitive-types-with-defined-representation) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests; Platform CI. |
| [CORE-019 — Parametric abstraction](../requirements/CORE.md#core-019--parametric-abstraction) | MUST | Post-v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests; Design review. |
| [CORE-020 — Reduced annotation burden](../requirements/CORE.md#core-020--reduced-annotation-burden) | SHOULD | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [CORE-021 — No implicit lossy conversions](../requirements/CORE.md#core-021--no-implicit-lossy-conversions) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests; Diagnostic tests. |
| [CORE-022 — Explicit recoverable errors](../requirements/CORE.md#core-022--explicit-recoverable-errors) | MUST | v0.1 | [ARCH-ERROR-001](ERROR.md) — Error-handling architecture; PROPOSED | Conformance tests; Diagnostic tests. |
| [CORE-023 — Recoverable errors versus faults](../requirements/CORE.md#core-023--recoverable-errors-versus-faults) | MUST | v0.1 | [ARCH-ERROR-001](ERROR.md) — Error-handling architecture; PROPOSED | Specification review; Conformance tests. |
| [CORE-024 — Structured error information](../requirements/CORE.md#core-024--structured-error-information) | MUST | v0.1 | [ARCH-ERROR-001](ERROR.md) — Error-handling architecture; PROPOSED | Unit tests. |
| [CORE-025 — Deterministic compilation](../requirements/CORE.md#core-025--deterministic-compilation) | MUST | v0.1 | [ARCH-COMPILER-001](COMPILER.md) — Compiler architecture and bootstrapping; PROPOSED | Integration tests (repeated and relocated builds compared). |
| [CORE-026 — Platform-independent semantics](../requirements/CORE.md#core-026--platform-independent-semantics) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Conformance tests run under Platform CI. |
| [CORE-027 — Program entry and exit](../requirements/CORE.md#core-027--program-entry-and-exit) | MUST | v0.1 | [ARCH-V0.1-ARCHITECTURE-001](V0.1-ARCHITECTURE.md) — v0.1 implementation blueprint; PROPOSED | Integration tests. |
| [CORE-028 — Declarative package manifest](../requirements/CORE.md#core-028--declarative-package-manifest) | MUST | v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Integration tests; Security review. |
| [CORE-029 — Separate and incremental compilation](../requirements/CORE.md#core-029--separate-and-incremental-compilation) | SHOULD | Post-v0.1 | [ARCH-COMPILER-001](COMPILER.md) — Compiler architecture and bootstrapping; PROPOSED | Benchmark. |
| [CORE-030 — Language evolution mechanism](../requirements/CORE.md#core-030--language-evolution-mechanism) | MUST | Before 1.0 | [ARCH-COMPAT-001](COMPAT.md) — Compatibility and stability; PROPOSED | Design review. |
| [CORE-031 — Specification coverage of shipped features](../requirements/CORE.md#core-031--specification-coverage-of-shipped-features) | MUST | v0.1 | [ARCH-COMPAT-001](COMPAT.md) — Compatibility and stability; PROPOSED | Inspection at release review. |
| [CORE-032 — Text operations](../requirements/CORE.md#core-032--text-operations) | MUST | v0.1 | [ARCH-V0.1-ARCHITECTURE-001](V0.1-ARCHITECTURE.md) — v0.1 implementation blueprint; PROPOSED | Unit tests. |
| [CORE-033 — Core collections](../requirements/CORE.md#core-033--core-collections) | MUST | v0.1 | [ARCH-V0.1-ARCHITECTURE-001](V0.1-ARCHITECTURE.md) — v0.1 implementation blueprint; PROPOSED | Unit tests. |

## DX

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [DX-001 — Single toolchain entry point](../requirements/CORE.md#dx-001--single-toolchain-entry-point) | MUST | v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Integration tests. |
| [DX-002 — `cretes check`](../requirements/CORE.md#dx-002--cretes-check) | MUST | v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Integration tests; Diagnostic tests. |
| [DX-003 — `cretes build`](../requirements/CORE.md#dx-003--cretes-build) | MUST | v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Integration tests. |
| [DX-004 — `cretes run`](../requirements/CORE.md#dx-004--cretes-run) | MUST | v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Integration tests. |
| [DX-005 — Diagnostic content](../requirements/CORE.md#dx-005--diagnostic-content) | MUST | v0.1 | [ARCH-DIAGNOSTIC-001](DIAGNOSTIC.md) — Diagnostics architecture; PROPOSED | Diagnostic tests. |
| [DX-006 — Machine-readable diagnostics](../requirements/CORE.md#dx-006--machine-readable-diagnostics) | MUST | v0.1 | [ARCH-DIAGNOSTIC-001](DIAGNOSTIC.md) — Diagnostics architecture; PROPOSED | Integration tests. |
| [DX-007 — Error recovery](../requirements/CORE.md#dx-007--error-recovery) | SHOULD | v0.1 | [ARCH-DIAGNOSTIC-001](DIAGNOSTIC.md) — Diagnostics architecture; PROPOSED | Diagnostic tests. |
| [DX-008 — Robustness on malformed input](../requirements/CORE.md#dx-008--robustness-on-malformed-input) | MUST | v0.1 | [ARCH-DIAGNOSTIC-001](DIAGNOSTIC.md) — Diagnostics architecture; PROPOSED | Fuzzing; Integration tests. |
| [DX-009 — Canonical formatter](../requirements/CORE.md#dx-009--canonical-formatter) | MUST | Post-v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Unit tests (idempotence and meaning preservation). |
| [DX-010 — Linter](../requirements/CORE.md#dx-010--linter) | SHOULD | Post-v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Diagnostic tests. |
| [DX-011 — Integrated test runner](../requirements/CORE.md#dx-011--integrated-test-runner) | MUST | Post-v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Integration tests. |
| [DX-012 — Language server](../requirements/CORE.md#dx-012--language-server) | SHOULD | Post-v0.1 | [ARCH-DIAGNOSTIC-001](DIAGNOSTIC.md) — Diagnostics architecture; PROPOSED | Integration tests. |
| [DX-013 — Documentation generator](../requirements/CORE.md#dx-013--documentation-generator) | SHOULD | Post-v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Integration tests. |
| [DX-014 — Debugger support](../requirements/CORE.md#dx-014--debugger-support) | MUST | Post-v0.1 | [ARCH-DEBUG-001](DEBUG.md) — Debugging and observability; PROPOSED | Platform CI. |
| [DX-015 — Package manager and registry](../requirements/CORE.md#dx-015--package-manager-and-registry) | MUST | Post-v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Integration tests; Security review. |
| [DX-016 — Online playground](../requirements/CORE.md#dx-016--online-playground) | MAY | Long-term | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Security review. |
| [DX-017 — Consistent semantics across tools](../requirements/CORE.md#dx-017--consistent-semantics-across-tools) | SHOULD | Post-v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Design review. |
| [DX-018 — Release documentation](../requirements/CORE.md#dx-018--release-documentation) | MUST | v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Inspection at release review. |
| [DX-019 — Scriptable command-line behavior](../requirements/CORE.md#dx-019--scriptable-command-line-behavior) | MUST | v0.1 | [ARCH-TOOLCHAIN-001](TOOLCHAIN.md) — Toolchain and developer tools; PROPOSED | Integration tests. |

## AUTO

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [AUTO-001 — Single-file programs](../requirements/domains/automation.md#auto-001--single-file-programs) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests. |
| [AUTO-002 — Error context for operational failures](../requirements/domains/automation.md#auto-002--error-context-for-operational-failures) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Conformance tests; Inspection of examples. |
| [AUTO-003 — Direct execution on POSIX systems](../requirements/domains/automation.md#auto-003--direct-execution-on-posix-systems) | MAY | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests. |
| [AUTO-004 — Exit status and termination signals](../requirements/domains/automation.md#auto-004--exit-status-and-termination-signals) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests under Platform CI. |
| [AUTO-005 — Timers](../requirements/domains/automation.md#auto-005--timers) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests. |
| [AUTO-006 — File operations](../requirements/domains/automation.md#auto-006--file-operations) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests under Platform CI. |
| [AUTO-007 — File metadata](../requirements/domains/automation.md#auto-007--file-metadata) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests under Platform CI. |
| [AUTO-008 — Path abstraction](../requirements/domains/automation.md#auto-008--path-abstraction) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests under Platform CI. |
| [AUTO-009 — Structured process creation](../requirements/domains/automation.md#auto-009--structured-process-creation) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests under Platform CI; Security review. |
| [AUTO-010 — Explicit shell invocation](../requirements/domains/automation.md#auto-010--explicit-shell-invocation) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Inspection; Security review. |
| [AUTO-011 — Process supervision](../requirements/domains/automation.md#auto-011--process-supervision) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests under Platform CI. |
| [AUTO-012 — Standard streams and pipes](../requirements/domains/automation.md#auto-012--standard-streams-and-pipes) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests. |
| [AUTO-013 — Environment variables](../requirements/domains/automation.md#auto-013--environment-variables) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests; Security review. |
| [AUTO-014 — Shared stream abstractions](../requirements/domains/automation.md#auto-014--shared-stream-abstractions) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests. |
| [AUTO-015 — In-process scheduling](../requirements/domains/automation.md#auto-015--in-process-scheduling) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests. |
| [AUTO-016 — JSON](../requirements/domains/automation.md#auto-016--json) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests; Fuzzing; Conformance against published JSON test suites. |
| [AUTO-017 — Structured serialization](../requirements/domains/automation.md#auto-017--structured-serialization) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests; Security review. |
| [AUTO-018 — Structured configuration](../requirements/domains/automation.md#auto-018--structured-configuration) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests. |
| [AUTO-019 — Command-line application support](../requirements/domains/automation.md#auto-019--command-line-application-support) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests. |
| [AUTO-020 — Logging](../requirements/domains/automation.md#auto-020--logging) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests; Security review. |
| [AUTO-021 — HTTP and API automation](../requirements/domains/automation.md#auto-021--http-and-api-automation) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests. |
| [AUTO-022 — Archives and compression](../requirements/domains/automation.md#auto-022--archives-and-compression) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests; Fuzzing; Security review. |
| [AUTO-023 — Concurrent job execution](../requirements/domains/automation.md#auto-023--concurrent-job-execution) | MUST | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests. |
| [AUTO-024 — Cross-platform OS abstractions](../requirements/domains/automation.md#auto-024--cross-platform-os-abstractions) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests under Platform CI. |
| [AUTO-025 — Clocks and time](../requirements/domains/automation.md#auto-025--clocks-and-time) | MUST | v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests. |
| [AUTO-026 — Secure temporary files](../requirements/domains/automation.md#auto-026--secure-temporary-files) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Unit tests; Security review. |
| [AUTO-027 — Filesystem change notification](../requirements/domains/automation.md#auto-027--filesystem-change-notification) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests under Platform CI. |
| [AUTO-028 — Distributing command-line tools](../requirements/domains/automation.md#auto-028--distributing-command-line-tools) | SHOULD | Post-v0.1 | [ARCH-AUTO-001](AUTO.md) — Automation architecture; PROPOSED | Integration tests. |

## NET

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [NET-001 — Byte-oriented data](../requirements/domains/networking.md#net-001--byte-oriented-data) | MUST | v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Conformance tests. |
| [NET-002 — Scalable asynchronous I/O](../requirements/domains/networking.md#net-002--scalable-asynchronous-io) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests; Benchmark (`networking/`). |
| [NET-003 — Connection-scale design target](../requirements/domains/networking.md#net-003--connection-scale-design-target) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Benchmark (`networking/`, `concurrency/`). |
| [NET-004 — IP address types](../requirements/domains/networking.md#net-004--ip-address-types) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests; Fuzzing. |
| [NET-005 — IPv6 parity](../requirements/domains/networking.md#net-005--ipv6-parity) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests under Platform CI. |
| [NET-006 — TCP clients and servers](../requirements/domains/networking.md#net-006--tcp-clients-and-servers) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests under Platform CI. |
| [NET-007 — UDP](../requirements/domains/networking.md#net-007--udp) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests. |
| [NET-008 — Local and low-level sockets](../requirements/domains/networking.md#net-008--local-and-low-level-sockets) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests under Platform CI. |
| [NET-009 — Name resolution](../requirements/domains/networking.md#net-009--name-resolution) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests. |
| [NET-010 — Timeouts on every network operation](../requirements/domains/networking.md#net-010--timeouts-on-every-network-operation) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests. |
| [NET-011 — Cancellation of network operations](../requirements/domains/networking.md#net-011--cancellation-of-network-operations) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests. |
| [NET-012 — Streaming](../requirements/domains/networking.md#net-012--streaming) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests. |
| [NET-013 — Backpressure](../requirements/domains/networking.md#net-013--backpressure) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests. |
| [NET-014 — Structured network errors](../requirements/domains/networking.md#net-014--structured-network-errors) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests. |
| [NET-015 — Binary data encoding](../requirements/domains/networking.md#net-015--binary-data-encoding) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests; Fuzzing. |
| [NET-016 — Incremental protocol parsing](../requirements/domains/networking.md#net-016--incremental-protocol-parsing) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests; Fuzzing. |
| [NET-017 — TLS](../requirements/domains/networking.md#net-017--tls) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests against independent TLS implementations; Security review. |
| [NET-018 — HTTP client](../requirements/domains/networking.md#net-018--http-client) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests; Fuzzing of response parsing. |
| [NET-019 — HTTP server foundation](../requirements/domains/networking.md#net-019--http-server-foundation) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests; Fuzzing. |
| [NET-020 — WebSockets](../requirements/domains/networking.md#net-020--websockets) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests against an independent conformance suite. |
| [NET-021 — Connection management and pooling](../requirements/domains/networking.md#net-021--connection-management-and-pooling) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests; Benchmark (`networking/`). |
| [NET-022 — Concurrent server foundation](../requirements/domains/networking.md#net-022--concurrent-server-foundation) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Integration tests. |
| [NET-023 — Secure network defaults](../requirements/domains/networking.md#net-023--secure-network-defaults) | MUST | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests; Security review. |
| [NET-024 — Network observability hooks](../requirements/domains/networking.md#net-024--network-observability-hooks) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests. |
| [NET-025 — URL handling](../requirements/domains/networking.md#net-025--url-handling) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Unit tests; Fuzzing. |
| [NET-026 — Protocol ecosystem support](../requirements/domains/networking.md#net-026--protocol-ecosystem-support) | MAY | Long-term | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Inspection. |

## AI

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [AI-001 — Exact numeric semantics](../requirements/domains/ai-ml.md#ai-001--exact-numeric-semantics) | MUST | v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Conformance tests under Platform CI. |
| [AI-002 — Reduced-precision numeric types](../requirements/domains/ai-ml.md#ai-002--reduced-precision-numeric-types) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Conformance tests. |
| [AI-003 — Packed value layout](../requirements/domains/ai-ml.md#ai-003--packed-value-layout) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Design review; Integration tests inspecting layout. |
| [AI-004 — Readable numerical notation](../requirements/domains/ai-ml.md#ai-004--readable-numerical-notation) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Design review. |
| [AI-005 — Contiguous arrays](../requirements/domains/ai-ml.md#ai-005--contiguous-arrays) | MUST | v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests. |
| [AI-006 — Buffer views](../requirements/domains/ai-ml.md#ai-006--buffer-views) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Conformance tests; Unit tests. |
| [AI-007 — Multidimensional arrays](../requirements/domains/ai-ml.md#ai-007--multidimensional-arrays) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests; Benchmark (`numerical/`). |
| [AI-008 — Tensor-compatible layout descriptors](../requirements/domains/ai-ml.md#ai-008--tensor-compatible-layout-descriptors) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Integration tests. |
| [AI-009 — Alignment control](../requirements/domains/ai-ml.md#ai-009--alignment-control) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests. |
| [AI-010 — Vectorized computation](../requirements/domains/ai-ml.md#ai-010--vectorized-computation) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Benchmark (`numerical/`); Unit tests under Platform CI. |
| [AI-011 — Parallel numerical computation](../requirements/domains/ai-ml.md#ai-011--parallel-numerical-computation) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests; Benchmark (`numerical/`). |
| [AI-012 — Model inference through established runtimes](../requirements/domains/ai-ml.md#ai-012--model-inference-through-established-runtimes) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Integration tests. |
| [AI-013 — First-party inference bindings](../requirements/domains/ai-ml.md#ai-013--first-party-inference-bindings) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Integration tests under Platform CI. |
| [AI-014 — Memory-efficient data handling](../requirements/domains/ai-ml.md#ai-014--memory-efficient-data-handling) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests; Security review. |
| [AI-015 — Data preprocessing](../requirements/domains/ai-ml.md#ai-015--data-preprocessing) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests. |
| [AI-016 — Tensor and model serialization](../requirements/domains/ai-ml.md#ai-016--tensor-and-model-serialization) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Integration tests; Fuzzing. |
| [AI-017 — Safe model and data loading](../requirements/domains/ai-ml.md#ai-017--safe-model-and-data-loading) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Security review; Fuzzing. |
| [AI-018 — CPU execution first](../requirements/domains/ai-ml.md#ai-018--cpu-execution-first) | MUST | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests under Platform CI. |
| [AI-019 — Accelerator-ready architecture (future architecture)](../requirements/domains/ai-ml.md#ai-019--accelerator-ready-architecture-future-architecture) | MAY | Long-term | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Design review. |
| [AI-020 — GPU support through interop (future architecture)](../requirements/domains/ai-ml.md#ai-020--gpu-support-through-interop-future-architecture) | MAY | Long-term | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Integration tests (when pursued). |
| [AI-021 — Heterogeneous compute (future architecture)](../requirements/domains/ai-ml.md#ai-021--heterogeneous-compute-future-architecture) | MAY | Exploratory | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Inspection (research RFC). |
| [AI-022 — Reproducible numerical results](../requirements/domains/ai-ml.md#ai-022--reproducible-numerical-results) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Unit tests. |
| [AI-023 — Hosted-model API clients](../requirements/domains/ai-ml.md#ai-023--hosted-model-api-clients) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Integration tests (example client). |

## SEC

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [SEC-001 — Memory-safe development objective](../requirements/domains/cybersecurity.md#sec-001--memory-safe-development-objective) | MUST | v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Security review; Inspection of standard-library unsafe usage. |
| [SEC-002 — Bounds-checked binary parsing](../requirements/domains/cybersecurity.md#sec-002--bounds-checked-binary-parsing) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests; Fuzzing. |
| [SEC-003 — Checked length arithmetic in parsers](../requirements/domains/cybersecurity.md#sec-003--checked-length-arithmetic-in-parsers) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Security review; Fuzzing. |
| [SEC-004 — Constant-time operations](../requirements/domains/cybersecurity.md#sec-004--constant-time-operations) | SHOULD | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Security review; Statistical timing tests. |
| [SEC-005 — Secret zeroization](../requirements/domains/cybersecurity.md#sec-005--secret-zeroization) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Security review; Integration tests. |
| [SEC-006 — Secure randomness](../requirements/domains/cybersecurity.md#sec-006--secure-randomness) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests; Security review. |
| [SEC-007 — Cryptographic hashing](../requirements/domains/cybersecurity.md#sec-007--cryptographic-hashing) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests against published test vectors. |
| [SEC-008 — Collision-resistant hash tables by default](../requirements/domains/cybersecurity.md#sec-008--collision-resistant-hash-tables-by-default) | MUST | v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Security review; Unit tests. |
| [SEC-009 — Message authentication](../requirements/domains/cybersecurity.md#sec-009--message-authentication) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests against published test vectors. |
| [SEC-010 — Authenticated encryption](../requirements/domains/cybersecurity.md#sec-010--authenticated-encryption) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests against published test vectors; Security review. |
| [SEC-011 — Digital signatures](../requirements/domains/cybersecurity.md#sec-011--digital-signatures) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests against published test vectors. |
| [SEC-012 — Key agreement](../requirements/domains/cybersecurity.md#sec-012--key-agreement) | SHOULD | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests against published test vectors. |
| [SEC-013 — Key derivation and password hashing](../requirements/domains/cybersecurity.md#sec-013--key-derivation-and-password-hashing) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests against published test vectors. |
| [SEC-014 — Misuse-resistant API layering](../requirements/domains/cybersecurity.md#sec-014--misuse-resistant-api-layering) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Security review. |
| [SEC-015 — Cryptographic implementation assurance](../requirements/domains/cybersecurity.md#sec-015--cryptographic-implementation-assurance) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Inspection; Security review. |
| [SEC-016 — Algorithm agility and legacy algorithms](../requirements/domains/cybersecurity.md#sec-016--algorithm-agility-and-legacy-algorithms) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Security review. |
| [SEC-017 — Key and credential handling](../requirements/domains/cybersecurity.md#sec-017--key-and-credential-handling) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests; Security review. |
| [SEC-018 — TLS security policy](../requirements/domains/cybersecurity.md#sec-018--tls-security-policy) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Integration tests; Security review. |
| [SEC-019 — Certificate handling](../requirements/domains/cybersecurity.md#sec-019--certificate-handling) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Integration tests against public certificate-validation test suites; Fuzzing. |
| [SEC-020 — Encoding and decoding](../requirements/domains/cybersecurity.md#sec-020--encoding-and-decoding) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests; Fuzzing. |
| [SEC-021 — Resource limits for untrusted input](../requirements/domains/cybersecurity.md#sec-021--resource-limits-for-untrusted-input) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests; Fuzzing. |
| [SEC-022 — Secret redaction in diagnostics and logs](../requirements/domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs) | MUST | Post-v0.1 | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) — Defensive cybersecurity libraries; PROPOSED | Unit tests; Security review. |
| [SEC-023 — Dependency integrity](../requirements/domains/cybersecurity.md#sec-023--dependency-integrity) | MUST | Post-v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Integration tests; Security review. |
| [SEC-024 — Package provenance and signing](../requirements/domains/cybersecurity.md#sec-024--package-provenance-and-signing) | MUST | Post-v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Security review. |
| [SEC-025 — No implicit code execution during dependency installation](../requirements/domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation) | MUST | Post-v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Integration tests; Security review. |
| [SEC-026 — Vulnerability advisories and audit](../requirements/domains/cybersecurity.md#sec-026--vulnerability-advisories-and-audit) | MUST | Post-v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Integration tests. |
| [SEC-027 — Reproducible builds](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds) | MUST | Before 1.0 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Integration tests (independent rebuilds compared). |
| [SEC-028 — Software bill of materials](../requirements/domains/cybersecurity.md#sec-028--software-bill-of-materials) | SHOULD | Post-v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Integration tests. |
| [SEC-029 — Unsafe and FFI audit reporting](../requirements/domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting) | MUST | Post-v0.1 | [ARCH-SECURITY-001](SECURITY.md) — Security and trust architecture; PROPOSED | Integration tests. |
| [SEC-030 — Fuzzing support](../requirements/domains/cybersecurity.md#sec-030--fuzzing-support) | SHOULD | Post-v0.1 | [ARCH-SECURITY-001](SECURITY.md) — Security and trust architecture; PROPOSED | Integration tests. |
| [SEC-031 — Security-focused static analysis](../requirements/domains/cybersecurity.md#sec-031--security-focused-static-analysis) | SHOULD | Post-v0.1 | [ARCH-SECURITY-001](SECURITY.md) — Security and trust architecture; PROPOSED | Diagnostic tests. |
| [SEC-032 — Toolchain release integrity](../requirements/domains/cybersecurity.md#sec-032--toolchain-release-integrity) | MUST | v0.1 | [ARCH-SECURITY-001](SECURITY.md) — Security and trust architecture; PROPOSED | Inspection at release review; Security review. |
| [SEC-033 — Scope of defensive utilities](../requirements/domains/cybersecurity.md#sec-033--scope-of-defensive-utilities) | SHOULD | Long-term | [ARCH-SECURITY-001](SECURITY.md) — Security and trust architecture; PROPOSED | Inspection. |
| [SEC-034 — Registry account and namespace protection](../requirements/domains/cybersecurity.md#sec-034--registry-account-and-namespace-protection) | SHOULD | Post-v0.1 | [ARCH-BUILD-001](BUILD.md) — Build and package architecture; PROPOSED | Security review. |

## SAFE

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [SAFE-001 — No undefined behavior in safe code](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code) | MUST | v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Specification review; Conformance tests; Fuzzing; Security review. |
| [SAFE-002 — Spatial memory safety](../requirements/SAFETY.md#safe-002--spatial-memory-safety) | MUST | v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Conformance tests; Fuzzing. |
| [SAFE-003 — Temporal memory safety](../requirements/SAFETY.md#safe-003--temporal-memory-safety) | MUST | v0.1 | [ARCH-MEM-001](MEM.md) — Memory-management model; PROPOSED | Conformance tests; Fuzzing; Design review. |
| [SAFE-004 — No double release](../requirements/SAFETY.md#safe-004--no-double-release) | MUST | v0.1 | [ARCH-MEM-001](MEM.md) — Memory-management model; PROPOSED | Conformance tests; Design review. |
| [SAFE-005 — Valid references](../requirements/SAFETY.md#safe-005--valid-references) | MUST | v0.1 | [ARCH-MEM-001](MEM.md) — Memory-management model; PROPOSED | Conformance tests; Design review. |
| [SAFE-006 — Null safety](../requirements/SAFETY.md#safe-006--null-safety) | MUST | v0.1 | [ARCH-NULL-001](NULL.md) — Nullability architecture; PROPOSED | Conformance tests; Diagnostic tests. |
| [SAFE-007 — No use of uninitialized values](../requirements/SAFETY.md#safe-007--no-use-of-uninitialized-values) | MUST | v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Conformance tests; Diagnostic tests. |
| [SAFE-008 — Defined integer overflow](../requirements/SAFETY.md#safe-008--defined-integer-overflow) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [SAFE-009 — Explicit overflow-handling operations](../requirements/SAFETY.md#safe-009--explicit-overflow-handling-operations) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests; Unit tests. |
| [SAFE-010 — Overflow detection during development](../requirements/SAFETY.md#safe-010--overflow-detection-during-development) | SHOULD | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [SAFE-011 — Defined arithmetic edge cases](../requirements/SAFETY.md#safe-011--defined-arithmetic-edge-cases) | MUST | v0.1 | [ARCH-TYPE-001](TYPE.md) — Type and numeric architecture; PROPOSED | Conformance tests. |
| [SAFE-012 — Data-race freedom](../requirements/SAFETY.md#safe-012--data-race-freedom) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Design review; Conformance tests; Security review. |
| [SAFE-013 — Deterministic resource release](../requirements/SAFETY.md#safe-013--deterministic-resource-release) | MUST | v0.1 | [ARCH-RESOURCE-001](RESOURCE.md) — Resource and lifetime management; PROPOSED | Conformance tests; Integration tests. |
| [SAFE-014 — Resource-leak diagnostics](../requirements/SAFETY.md#safe-014--resource-leak-diagnostics) | SHOULD | Post-v0.1 | [ARCH-RESOURCE-001](RESOURCE.md) — Resource and lifetime management; PROPOSED | Integration tests. |
| [SAFE-015 — Type safety](../requirements/SAFETY.md#safe-015--type-safety) | MUST | v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Conformance tests; Security review. |
| [SAFE-016 — Explicit and auditable unsafe code](../requirements/SAFETY.md#safe-016--explicit-and-auditable-unsafe-code) | MUST | Post-v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Conformance tests; Integration tests. |
| [SAFE-017 — Safe abstractions over unsafe code](../requirements/SAFETY.md#safe-017--safe-abstractions-over-unsafe-code) | MUST | Post-v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Specification review; Security review. |
| [SAFE-018 — FFI is an unsafe boundary](../requirements/SAFETY.md#safe-018--ffi-is-an-unsafe-boundary) | MUST | Post-v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Specification review; Security review. |
| [SAFE-019 — Package-level unsafe policy](../requirements/SAFETY.md#safe-019--package-level-unsafe-policy) | SHOULD | Post-v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Integration tests. |
| [SAFE-020 — Defined fault behavior](../requirements/SAFETY.md#safe-020--defined-fault-behavior) | MUST | v0.1 | [ARCH-ERROR-001](ERROR.md) — Error-handling architecture; PROPOSED | Conformance tests. |
| [SAFE-021 — Defined behavior on resource exhaustion](../requirements/SAFETY.md#safe-021--defined-behavior-on-resource-exhaustion) | MUST | v0.1 | [ARCH-ERROR-001](ERROR.md) — Error-handling architecture; PROPOSED | Conformance tests; Fuzzing. |
| [SAFE-022 — Checked builds for unsafe code](../requirements/SAFETY.md#safe-022--checked-builds-for-unsafe-code) | SHOULD | Post-v0.1 | [ARCH-SAFETY-001](SAFETY.md) — Safety architecture; PROPOSED | Integration tests. |
| [SAFE-023 — Memory-management evaluation criteria](../requirements/SAFETY.md#safe-023--memory-management-evaluation-criteria) | MUST | v0.1 | [ARCH-MEM-001](MEM.md) — Memory-management model; PROPOSED | Design review. |

## PERF

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [PERF-001 — Self-contained executables](../requirements/PERFORMANCE.md#perf-001--self-contained-executables) | MUST | Post-v0.1 | [ARCH-EXEC-001](EXEC.md) — Execution model; PROPOSED | Platform CI. |
| [PERF-002 — Documented cost model](../requirements/PERFORMANCE.md#perf-002--documented-cost-model) | MUST | v0.1 | [ARCH-OPT-001](OPT.md) — Optimization architecture; PROPOSED | Inspection. |
| [PERF-003 — Visible expensive operations](../requirements/PERFORMANCE.md#perf-003--visible-expensive-operations) | SHOULD | Post-v0.1 | [ARCH-OPT-001](OPT.md) — Optimization architecture; PROPOSED | Design review. |
| [PERF-004 — Program startup latency](../requirements/PERFORMANCE.md#perf-004--program-startup-latency) | SHOULD | v0.1 | [ARCH-EXEC-001](EXEC.md) — Execution model; PROPOSED | Benchmark (`startup/`). |
| [PERF-005 — Toolchain responsiveness](../requirements/PERFORMANCE.md#perf-005--toolchain-responsiveness) | SHOULD | v0.1 | [ARCH-EXEC-001](EXEC.md) — Execution model; PROPOSED | Benchmark (`startup/`, `compile/`). |
| [PERF-006 — Analysis faster than full builds](../requirements/PERFORMANCE.md#perf-006--analysis-faster-than-full-builds) | SHOULD | v0.1 | [ARCH-EXEC-001](EXEC.md) — Execution model; PROPOSED | Benchmark (`compile/`). |
| [PERF-007 — Incremental builds](../requirements/PERFORMANCE.md#perf-007--incremental-builds) | SHOULD | Post-v0.1 | [ARCH-COMPILER-001](COMPILER.md) — Compiler architecture and bootstrapping; PROPOSED | Benchmark (`compile/`). |
| [PERF-008 — Development and optimized profiles](../requirements/PERFORMANCE.md#perf-008--development-and-optimized-profiles) | MUST | v0.1 | [ARCH-OPT-001](OPT.md) — Optimization architecture; PROPOSED | Conformance tests run under both profiles. |
| [PERF-009 — Optimizable compute throughput](../requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput) | SHOULD | Post-v0.1 | [ARCH-OPT-001](OPT.md) — Optimization architecture; PROPOSED | Benchmark (`compute/`). |
| [PERF-010 — Memory footprint and control](../requirements/PERFORMANCE.md#perf-010--memory-footprint-and-control) | SHOULD | Post-v0.1 | [ARCH-MEM-001](MEM.md) — Memory-management model; PROPOSED | Benchmark (`memory/`). |
| [PERF-011 — Allocation-free values](../requirements/PERFORMANCE.md#perf-011--allocation-free-values) | SHOULD | v0.1 | [ARCH-MEM-001](MEM.md) — Memory-management model; PROPOSED | Design review; Benchmark (`memory/`). |
| [PERF-012 — Artifact size](../requirements/PERFORMANCE.md#perf-012--artifact-size) | SHOULD | Post-v0.1 | [ARCH-OPT-001](OPT.md) — Optimization architecture; PROPOSED | Benchmark (`startup/`). |
| [PERF-013 — Efficient I/O buffers](../requirements/PERFORMANCE.md#perf-013--efficient-io-buffers) | SHOULD | Post-v0.1 | [ARCH-NET-001](NET.md) — Networking architecture; PROPOSED | Benchmark (`networking/`). |
| [PERF-014 — Concurrency overhead](../requirements/PERFORMANCE.md#perf-014--concurrency-overhead) | SHOULD | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Benchmark (`concurrency/`). |
| [PERF-015 — Numerical throughput](../requirements/PERFORMANCE.md#perf-015--numerical-throughput) | SHOULD | Post-v0.1 | [ARCH-AI-001](AI.md) — AI/ML architecture; PROPOSED | Benchmark (`numerical/`). |
| [PERF-016 — FFI call overhead](../requirements/PERFORMANCE.md#perf-016--ffi-call-overhead) | SHOULD | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Benchmark (`compute/`). |
| [PERF-017 — Evidence before claims](../requirements/PERFORMANCE.md#perf-017--evidence-before-claims) | MUST | v0.1 | [ARCH-REVIEW-001](REVIEW.md) — Architecture review and acceptance gates; PROPOSED | Inspection at release review. |
| [PERF-018 — Benchmark methodology](../requirements/PERFORMANCE.md#perf-018--benchmark-methodology) | MUST | Post-v0.1 | [ARCH-REVIEW-001](REVIEW.md) — Architecture review and acceptance gates; PROPOSED | Inspection; Platform CI. |

## CONC

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [CONC-001 — Concurrent tasks](../requirements/CONCURRENCY.md#conc-001--concurrent-tasks) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Conformance tests. |
| [CONC-002 — Non-blocking waiting](../requirements/CONCURRENCY.md#conc-002--non-blocking-waiting) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Integration tests; Benchmark (`concurrency/`). |
| [CONC-003 — Parallel execution](../requirements/CONCURRENCY.md#conc-003--parallel-execution) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Benchmark (`concurrency/`, `numerical/`). |
| [CONC-004 — Structured concurrency](../requirements/CONCURRENCY.md#conc-004--structured-concurrency) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Conformance tests. |
| [CONC-005 — Explicit detached tasks](../requirements/CONCURRENCY.md#conc-005--explicit-detached-tasks) | SHOULD | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Conformance tests. |
| [CONC-006 — Cancellation](../requirements/CONCURRENCY.md#conc-006--cancellation) | MUST | Post-v0.1 | [ARCH-ASYNC-001](ASYNC.md) — Async and cancellation architecture; PROPOSED | Conformance tests; Integration tests. |
| [CONC-007 — Deadlines and timeouts](../requirements/CONCURRENCY.md#conc-007--deadlines-and-timeouts) | MUST | Post-v0.1 | [ARCH-ASYNC-001](ASYNC.md) — Async and cancellation architecture; PROPOSED | Integration tests. |
| [CONC-008 — Error propagation](../requirements/CONCURRENCY.md#conc-008--error-propagation) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Conformance tests. |
| [CONC-009 — Synchronization primitives](../requirements/CONCURRENCY.md#conc-009--synchronization-primitives) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Unit tests; Integration tests. |
| [CONC-010 — Memory model](../requirements/CONCURRENCY.md#conc-010--memory-model) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Specification review. |
| [CONC-011 — Message passing](../requirements/CONCURRENCY.md#conc-011--message-passing) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Unit tests. |
| [CONC-012 — Backpressure](../requirements/CONCURRENCY.md#conc-012--backpressure) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Unit tests. |
| [CONC-013 — Diagnosing unsafe sharing](../requirements/CONCURRENCY.md#conc-013--diagnosing-unsafe-sharing) | SHOULD | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Conformance tests; Diagnostic tests. |
| [CONC-014 — Task lifecycle observation](../requirements/CONCURRENCY.md#conc-014--task-lifecycle-observation) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Unit tests. |
| [CONC-015 — Blocking and CPU-intensive work](../requirements/CONCURRENCY.md#conc-015--blocking-and-cpu-intensive-work) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Integration tests. |
| [CONC-016 — Waiting on multiple operations](../requirements/CONCURRENCY.md#conc-016--waiting-on-multiple-operations) | SHOULD | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Unit tests. |
| [CONC-017 — Concurrency observability](../requirements/CONCURRENCY.md#conc-017--concurrency-observability) | SHOULD | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Integration tests. |
| [CONC-018 — Deterministic concurrency testing](../requirements/CONCURRENCY.md#conc-018--deterministic-concurrency-testing) | SHOULD | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Unit tests. |
| [CONC-019 — Unified concurrency model](../requirements/CONCURRENCY.md#conc-019--unified-concurrency-model) | SHOULD | Post-v0.1 | [ARCH-ASYNC-001](ASYNC.md) — Async and cancellation architecture; PROPOSED | Design review. |
| [CONC-020 — Concurrency and foreign code](../requirements/CONCURRENCY.md#conc-020--concurrency-and-foreign-code) | MUST | Post-v0.1 | [ARCH-CONC-001](CONC.md) — Concurrency architecture; PROPOSED | Integration tests; Design review. |

## INTOP

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [INTOP-001 — Calling C-ABI functions](../requirements/INTEROPERABILITY.md#intop-001--calling-c-abi-functions) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests under Platform CI. |
| [INTOP-002 — Exposing Cretes functions through the C ABI](../requirements/INTEROPERABILITY.md#intop-002--exposing-cretes-functions-through-the-c-abi) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests under Platform CI. |
| [INTOP-003 — C-compatible data layout](../requirements/INTEROPERABILITY.md#intop-003--c-compatible-data-layout) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests comparing layouts with the platform C compiler. |
| [INTOP-004 — Linking and loading native libraries](../requirements/INTEROPERABILITY.md#intop-004--linking-and-loading-native-libraries) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests under Platform CI. |
| [INTOP-005 — Memory ownership across the boundary](../requirements/INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Design review; Integration tests; Security review. |
| [INTOP-006 — Safe wrappers](../requirements/INTEROPERABILITY.md#intop-006--safe-wrappers) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Conformance tests; Security review. |
| [INTOP-007 — Error propagation across the boundary](../requirements/INTEROPERABILITY.md#intop-007--error-propagation-across-the-boundary) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests; Specification review. |
| [INTOP-008 — Callbacks from foreign code](../requirements/INTEROPERABILITY.md#intop-008--callbacks-from-foreign-code) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests. |
| [INTOP-009 — Binding generation](../requirements/INTEROPERABILITY.md#intop-009--binding-generation) | SHOULD | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests. |
| [INTOP-010 — Operating-system API access](../requirements/INTEROPERABILITY.md#intop-010--operating-system-api-access) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests under Platform CI. |
| [INTOP-011 — C++ interoperability](../requirements/INTEROPERABILITY.md#intop-011--c-interoperability) | SHOULD | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests (example project). |
| [INTOP-012 — AI runtime integration](../requirements/INTEROPERABILITY.md#intop-012--ai-runtime-integration) | SHOULD | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests. |
| [INTOP-013 — Python interoperability](../requirements/INTEROPERABILITY.md#intop-013--python-interoperability) | MAY | Long-term | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests. |
| [INTOP-014 — JavaScript interoperability](../requirements/INTEROPERABILITY.md#intop-014--javascript-interoperability) | MAY | Long-term | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests. |
| [INTOP-015 — JVM interoperability](../requirements/INTEROPERABILITY.md#intop-015--jvm-interoperability) | MAY | Exploratory | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Inspection (feasibility report). |
| [INTOP-016 — WebAssembly modules](../requirements/INTEROPERABILITY.md#intop-016--webassembly-modules) | SHOULD | Long-term | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Design review. |
| [INTOP-017 — Unsafe FFI declarations are not trusted by default](../requirements/INTEROPERABILITY.md#intop-017--unsafe-ffi-declarations-are-not-trusted-by-default) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Inspection; Integration tests. |
| [INTOP-018 — ABI stability policy](../requirements/INTEROPERABILITY.md#intop-018--abi-stability-policy) | MUST | v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Inspection at release review. |
| [INTOP-019 — Declared native dependencies](../requirements/INTEROPERABILITY.md#intop-019--declared-native-dependencies) | MUST | Post-v0.1 | [ARCH-FFI-001](FFI.md) — FFI and ABI architecture; PROPOSED | Integration tests. |

## PLAT

| Requirement | Priority | Phase 1 target | Proposed response | Future evidence |
| --- | --- | --- | --- | --- |
| [PLAT-001 — Published tier policy](../requirements/PLATFORMS.md#plat-001--published-tier-policy) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Inspection at release review. |
| [PLAT-002 — Tier 1 candidates](../requirements/PLATFORMS.md#plat-002--tier-1-candidates) | MUST | Before 1.0 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Platform CI. |
| [PLAT-003 — Tier 2 candidates](../requirements/PLATFORMS.md#plat-003--tier-2-candidates) | SHOULD | Before 1.0 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Platform CI. |
| [PLAT-004 — Future platform candidates](../requirements/PLATFORMS.md#plat-004--future-platform-candidates) | MAY | Exploratory | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Design review. |
| [PLAT-005 — Criteria for official support](../requirements/PLATFORMS.md#plat-005--criteria-for-official-support) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Inspection at release review. |
| [PLAT-006 — Portable behavior](../requirements/PLATFORMS.md#plat-006--portable-behavior) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Conformance tests and unit tests under Platform CI. |
| [PLAT-007 — Explicit platform-specific code](../requirements/PLATFORMS.md#plat-007--explicit-platform-specific-code) | MUST | Post-v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Conformance tests. |
| [PLAT-008 — Cross-compilation](../requirements/PLATFORMS.md#plat-008--cross-compilation) | SHOULD | Post-v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Platform CI. |
| [PLAT-009 — Filesystem and path portability](../requirements/PLATFORMS.md#plat-009--filesystem-and-path-portability) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Unit tests under Platform CI. |
| [PLAT-010 — Documented minimum OS versions](../requirements/PLATFORMS.md#plat-010--documented-minimum-os-versions) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Inspection. |
| [PLAT-011 — Tier changes](../requirements/PLATFORMS.md#plat-011--tier-changes) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Inspection. |
| [PLAT-012 — Minimal external runtime dependencies](../requirements/PLATFORMS.md#plat-012--minimal-external-runtime-dependencies) | SHOULD | Post-v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Platform CI. |
| [PLAT-013 — Toolchain installation](../requirements/PLATFORMS.md#plat-013--toolchain-installation) | MUST | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Inspection; Integration tests. |
| [PLAT-014 — Consistent toolchain behavior across hosts](../requirements/PLATFORMS.md#plat-014--consistent-toolchain-behavior-across-hosts) | SHOULD | v0.1 | [ARCH-PLATFORM-001](PLATFORM.md) — Platform architecture; PROPOSED | Platform CI. |

