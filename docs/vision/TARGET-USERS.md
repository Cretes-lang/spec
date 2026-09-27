# Target developers

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This document defines the developer personas Cretes is designed for. Personas keep requirements grounded in real work. Each persona lists common tasks, current pain points, required Cretes capabilities, and expectations for developer experience, performance and security.

Pain points describe common engineering challenges in these roles. They are not criticisms of any particular language or tool. Every established ecosystem has strengths that Cretes should learn from.

Personas are linked from the [use cases](../requirements/USE-CASES.md) and from domain requirement documents.

## Contents

- [Automation Engineers](#automation-engineers)
- [Backend / Network Engineers](#backend--network-engineers)
- [AI/ML Application Developers](#aiml-application-developers)
- [Cybersecurity Engineers](#cybersecurity-engineers)
- [Systems / Tooling Developers](#systems--tooling-developers)
- [DevOps / Platform Engineers](#devops--platform-engineers)
- [Persona-to-domain matrix](#persona-to-domain-matrix)

## Automation Engineers

Engineers who automate repetitive work, including file processing, system administration, report generation, data movement and integration between tools and APIs.

| Aspect | Description |
| --- | --- |
| **Common tasks** | Filesystem traversal and manipulation. Running and chaining commands. Calling REST APIs. Parsing JSON, CSV and logs. Scheduling jobs. Writing small CLI tools. Administering Linux and Windows systems. |
| **Current pain points** | Scripts that grow beyond their original scope become hard to maintain. Errors are silently ignored, or surface late with unclear context. Shell quoting leads to injection bugs. Scripts written on one OS fail on another. Distributing a script often means distributing an interpreter and dependencies too. |
| **Required Cretes capabilities** | Single-file execution, structured process APIs without implicit shells, path handling that works across platforms, explicit and concise error propagation, JSON and configuration handling, timers and scheduling, logging. |
| **Developer experience** | Write and run a file with one command. Scripts grow into tested tools without a rewrite. Errors name the operation and the resource that failed. |
| **Performance expectations** | Fast program startup for tools invoked many times. Throughput adequate for processing large logs and files. |
| **Security expectations** | No shell interpretation by default. Secrets from the environment are not logged. Temporary files are created securely. |
| **Key requirements** | [automation.md](../requirements/domains/automation.md), [AUTO-001](../requirements/domains/automation.md#auto-001--single-file-programs), [AUTO-009](../requirements/domains/automation.md#auto-009--structured-process-creation), [AUTO-010](../requirements/domains/automation.md#auto-010--explicit-shell-invocation) |

## Backend / Network Engineers

Engineers who build services, proxies, gateways, protocol implementations and streaming systems.

| Aspect | Description |
| --- | --- |
| **Common tasks** | TCP and UDP servers and clients. HTTP APIs. TLS termination. WebSocket and streaming services. Implementing binary and text protocols. Connection pooling. Graceful shutdown. |
| **Current pain points** | Timeouts, cancellation and backpressure are easy to omit and hard to retrofit. Concurrency bugs, such as races and leaked tasks, show up only under production load. Async code can split an ecosystem into incompatible halves. Parsing binary protocols safely requires constant vigilance. |
| **Required Cretes capabilities** | Scalable asynchronous I/O, structured concurrency with cancellation and deadlines, bounded channels, IPv4/IPv6 parity, TLS with secure defaults, HTTP foundations, structured network errors, bounds-checked binary parsing. |
| **Developer experience** | The per-connection code reads sequentially. The safe pattern is the default one. Timeouts are always available and never forgotten silently. |
| **Performance expectations** | Many concurrent connections per process. Low, predictable latency without long pauses. Efficient buffer reuse. |
| **Security expectations** | Certificate verification on by default. Parsers resist malformed input. Resource limits guard against slow-client and memory-exhaustion attacks. |
| **Key requirements** | [networking.md](../requirements/domains/networking.md), [CONCURRENCY.md](../requirements/CONCURRENCY.md), [NET-022](../requirements/domains/networking.md#net-022--concurrent-server-foundation) |

## AI/ML Application Developers

Developers who build applications that use machine learning: inference services, data pipelines, model-calling agents and edge deployments. They are not necessarily researchers training new models.

| Aspect | Description |
| --- | --- |
| **Common tasks** | Numerical computation. Transforming and batching data. Working with arrays and tensors. Running inference with established runtimes. Integrating native AI libraries. Calling hosted model APIs. Deploying models to servers and edge devices. |
| **Current pain points** | Moving from a prototype to a production service often requires rewriting code or crossing language boundaries. Data copies between runtimes waste memory. Native library integration is fragile. Preprocessing can become a CPU bottleneck. Loading untrusted model files can be dangerous. |
| **Required Cretes capabilities** | Exact numeric types, including reduced precision, contiguous arrays and zero-copy views, tensor-compatible layouts, SIMD and parallel computation, safe FFI to inference runtimes, memory-mapped data, safe model loading, HTTP and streaming clients. |
| **Developer experience** | Numerical code readable close to mathematical form. Straightforward integration with the runtimes they already use. The same code on laptop and server. |
| **Performance expectations** | Vectorized, parallel CPU execution. Zero-copy tensor exchange. Accelerator support later, through interop. |
| **Security expectations** | Model and data loading never executes embedded code. API keys are handled as secrets. |
| **Key requirements** | [ai-ml.md](../requirements/domains/ai-ml.md), [INTEROPERABILITY.md](../requirements/INTEROPERABILITY.md), [AI-008](../requirements/domains/ai-ml.md#ai-008--tensor-compatible-layout-descriptors) |

## Cybersecurity Engineers

Engineers who build secure software and **defensive** security tooling: cryptographic applications, protocol and binary analysis, security scanners for their own infrastructure, monitoring and incident-response utilities.

| Aspect | Description |
| --- | --- |
| **Common tasks** | Building secure applications. Using cryptographic primitives correctly. Parsing untrusted binary data, such as packets, file formats and certificates. Analyzing protocols. Auditing TLS configurations and dependencies. Writing defensive monitoring tools. |
| **Current pain points** | Memory-corruption bugs in parsers of untrusted input. Cryptographic APIs that make misuse, such as nonce reuse or unauthenticated encryption, easy. Secrets leaking into logs or lingering in memory. Opaque dependency trees and install-time code execution. |
| **Required Cretes capabilities** | Memory safety without undefined behavior, bounds-checked binary parsing, misuse-resistant cryptography, secure randomness, secret types with zeroization and redaction, TLS and certificate validation, auditing of unsafe code and FFI, reproducible builds, SBOM generation. |
| **Developer experience** | Secure choices are the default ones. Dangerous operations are explicit and searchable. Tooling shows where guarantees end. |
| **Performance expectations** | High-throughput parsing. Predictable, constant-time behavior where secrets are involved. |
| **Security expectations** | The strongest of any persona. Security-sensitive APIs must be hard to misuse, and the supply chain must be verifiable. |
| **Key requirements** | [cybersecurity.md](../requirements/domains/cybersecurity.md), [SAFETY.md](../requirements/SAFETY.md), [SEC-014](../requirements/domains/cybersecurity.md#sec-014--misuse-resistant-api-layering) |

## Systems / Tooling Developers

Developers who build native command-line tools, developer tooling, libraries and system utilities.

| Aspect | Description |
| --- | --- |
| **Common tasks** | Producing native binaries. Integrating with operating-system APIs. Wrapping C libraries. Building compilers, linters, formatters and build tools. Writing performance-sensitive libraries. |
| **Current pain points** | Choosing between low-level control and memory safety. Binding to C libraries by hand. Unpredictable performance from hidden allocations or pauses. Complex cross-platform builds. |
| **Required Cretes capabilities** | Self-contained executables, a documented cost model, C-ABI interop in both directions, clearly scoped unsafe code, debugger support, cross-compilation. |
| **Developer experience** | Low-level control is available when needed and clearly marked. Otherwise, safe high-level code is the default. |
| **Performance expectations** | Throughput comparable to established native languages, measured by benchmark. Small binaries. Fast startup. Low FFI overhead. |
| **Security expectations** | Unsafe code is auditable. Native dependencies are declared. |
| **Key requirements** | [INTEROPERABILITY.md](../requirements/INTEROPERABILITY.md), [PERFORMANCE.md](../requirements/PERFORMANCE.md), [SAFE-016](../requirements/SAFETY.md#safe-016--explicit-and-auditable-unsafe-code) |

## DevOps / Platform Engineers

Engineers who build and operate deployment pipelines, infrastructure automation, internal platforms and observability tooling.

| Aspect | Description |
| --- | --- |
| **Common tasks** | Infrastructure automation through cloud APIs. Deployment and release tooling. Configuration management. Orchestrating processes and containers. Health checks and agents. Metrics, logs and traces. |
| **Current pain points** | Tools that need a specific runtime version on every host. Inconsistent behavior between CI and production environments. Configuration errors discovered late. Poor error messages from failed automation. Supply-chain risk from sprawling dependencies. |
| **Required Cretes capabilities** | Self-contained binaries, cross-compilation, structured configuration, HTTP/API clients, process management, structured logging with redaction, observability hooks, reproducible builds, dependency integrity. |
| **Developer experience** | Build once and deploy anywhere. Clear configuration validation errors. Predictable resource usage. |
| **Performance expectations** | Low memory footprint for agents. Fast startup for CLI invocations. Efficient concurrent API calls. |
| **Security expectations** | Credentials never logged. Artifacts verifiable. Dependencies locked and hashed. |
| **Key requirements** | [automation.md](../requirements/domains/automation.md), [PLATFORMS.md](../requirements/PLATFORMS.md), [SEC-023](../requirements/domains/cybersecurity.md#sec-023--dependency-integrity) |

## Persona-to-domain matrix

| Persona | Automation | Networking | AI/ML Applications | Cybersecurity |
| --- | :---: | :---: | :---: | :---: |
| Automation Engineers | ●●● | ● | ● | ● |
| Backend / Network Engineers | ● | ●●● | ● | ●● |
| AI/ML Application Developers | ●● | ●● | ●●● | ● |
| Cybersecurity Engineers | ●● | ●●● | ● | ●●● |
| Systems / Tooling Developers | ●● | ●● | ●● | ●● |
| DevOps / Platform Engineers | ●●● | ●● | ● | ●● |

●●● primary · ●● significant · ● occasional

## Related documents

- [Vision](VISION.md)
- [Use cases](../requirements/USE-CASES.md)
- [Design principles](../principles/DESIGN-PRINCIPLES.md)
