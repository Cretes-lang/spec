# Networking requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

Networking is one of the four official Cretes domains. This document covers:

- network clients and servers;
- protocol implementations;
- streaming systems;
- connection-heavy services.

The primary personas are the [Backend / Network Engineer](../../vision/TARGET-USERS.md#backend--network-engineers) and the [Cybersecurity Engineer](../../vision/TARGET-USERS.md#cybersecurity-engineers).

> **Scope note.** No networking capability is required in v0.1 ([V0.1-REQUIREMENTS.md](../V0.1-REQUIREMENTS.md)). The one exception is the byte-oriented data types of [NET-001](#net-001--byte-oriented-data), which are a language foundation. The remaining requirements describe a post-v0.1 networking foundation. Listing a protocol here does not promise that the project will implement it in any particular milestone.

Terminology, layers and targets are defined in the [requirements framework](../README.md).

## Contents

- [Domain goals](#domain-goals)
- [Layer allocation](#layer-allocation)
- [Language requirements](#language-requirements)
- [Runtime requirements](#runtime-requirements)
- [Standard-library requirements](#standard-library-requirements)
- [First-party library requirements](#first-party-library-requirements)
- [Ecosystem](#ecosystem)

## Domain goals

1. Correct, robust network code should be the default. Timeouts, cancellation, backpressure and structured errors are built in, not bolted on.
2. Services should scale to many concurrent connections with predictable latency.
3. Encrypted communication should be the easy path, and its defaults should be secure.
4. Binary protocols should be parseable without memory-safety risk.

## Layer allocation

| Layer | Networking responsibilities |
| --- | --- |
| Language | Byte types, fixed-width integers, safe buffer access, concurrency and cancellation semantics. |
| Runtime | Efficient waiting on many sockets. Integration of network readiness with task scheduling. |
| Standard library | IP addresses, TCP, UDP, DNS resolution, byte buffers and binary codecs, timeouts, structured network errors. |
| First-party library | TLS, HTTP, WebSockets, URL handling, connection pooling. The Phase 2+ decision is whether these ship in the standard library or as official packages ([P2Q-017](../../PHASE-2-OPEN-QUESTIONS.md#p2q-017--standard-library-scope-and-first-party-packages)). |
| Ecosystem | Web frameworks, RPC systems, message brokers, QUIC/HTTP/3, database drivers, domain-specific protocols. |

## Language requirements

### NET-001 — Byte-oriented data

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language must provide immutable and mutable byte sequences, and views into them, that are distinct from text ([CORE-006](../CORE.md#core-006--text-distinct-from-bytes)) and bounds-checked ([SAFE-002](../SAFETY.md#safe-002--spatial-memory-safety)).
- **Rationale:** Every protocol operates on bytes. Treating bytes as text causes corruption and injection bugs.
- **Verification:** Conformance tests.

## Runtime requirements

### NET-002 — Scalable asynchronous I/O

- **Priority:** MUST · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** Waiting on network I/O must integrate with the concurrency model ([CONC-002](../CONCURRENCY.md#conc-002--non-blocking-waiting)). It must use scalable operating-system notification mechanisms, such as the readiness- or completion-based facilities each Tier 1 platform provides. The mechanism is selected in Phase 2.
- **Rationale:** One OS thread per connection does not scale to the connection counts of modern services.
- **Verification:** Integration tests; Benchmark (`networking/`).

### NET-003 — Connection-scale design target

- **Priority:** SHOULD · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** A single process on a Tier 1 platform should be able to hold at least 10,000 concurrent, mostly idle TCP connections, each served by its own task, within ordinary OS limits. This figure is a **design target** to validate by benchmark. It is not a measured claim.
- **Rationale:** An established reference scale for concurrent servers. It makes [PERF-014](../PERFORMANCE.md#perf-014--concurrency-overhead) concrete.
- **Verification:** Benchmark (`networking/`, `concurrency/`).

## Standard-library requirements

### NET-004 — IP address types

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide IPv4 and IPv6 address types and socket-address types. Parsing and formatting must be strict and standards-conforming. For IPv6, this includes scope identifiers and the canonical text form (RFC 5952). Ambiguous legacy IPv4 forms, such as octal or shortened notations, must not be silently accepted.
- **Rationale:** Lenient address parsing has caused access-control bypasses (server-side request forgery (SSRF) filter evasion).
- **Verification:** Unit tests; Fuzzing.

### NET-005 — IPv6 parity

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Every standard-library networking interface must support IPv6 equally with IPv4, including dual-stack listening where the platform supports it.
- **Rationale:** IPv6 is required in modern networks. Retrofitting it is costly.
- **Verification:** Integration tests under Platform CI.

### NET-006 — TCP clients and servers

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide TCP facilities to:
  - connect;
  - listen and accept;
  - read and write;
  - perform half-close and shutdown;
  - set common socket options, such as no-delay, keepalive, address reuse and buffer sizes.
- **Rationale:** TCP underlies most application protocols.
- **Verification:** Integration tests under Platform CI.

### NET-007 — UDP

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must support binding UDP sockets and sending and receiving datagrams with peer addresses. Multicast and broadcast SHOULD be supported.
- **Rationale:** DNS, service discovery, telemetry and many security tools use UDP.
- **Verification:** Integration tests.

### NET-008 — Local and low-level sockets

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library should support Unix domain sockets on platforms that provide them. Raw sockets and packet capture MAY be exposed through platform-specific interfaces ([PLAT-007](../PLATFORMS.md#plat-007--explicit-platform-specific-code)). They must require the privileges the OS demands and must never be used implicitly.
- **Rationale:** Local IPC is common in system services. Raw access supports defensive network monitoring ([SEC-033](cybersecurity.md#sec-033--scope-of-defensive-utilities)).
- **Verification:** Integration tests under Platform CI.

### NET-009 — Name resolution

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must resolve host names to addresses without blocking unrelated tasks, and must support timeouts and cancellation. It must use the platform's configured resolution by default. Connection helpers SHOULD try multiple resolved addresses using a strategy such as "Happy Eyeballs" (RFC 8305).
- **Rationale:** Blocking DNS lookups are a common cause of stalled services.
- **Verification:** Integration tests.

### NET-010 — Timeouts on every network operation

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Connect, accept, read, write, resolve and handshake operations must each be boundable by a timeout or by an enclosing deadline ([CONC-007](../CONCURRENCY.md#conc-007--deadlines-and-timeouts)). High-level clients, such as HTTP, must have finite default timeouts.
- **Rationale:** Operations with no timeout hang services and enable slow-client denial of service.
- **Verification:** Integration tests.

### NET-011 — Cancellation of network operations

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Cancelling a task must promptly interrupt its pending network operations and release the associated sockets and buffers ([CONC-006](../CONCURRENCY.md#conc-006--cancellation), [SAFE-013](../SAFETY.md#safe-013--deterministic-resource-release)).
- **Rationale:** Graceful shutdown and request abandonment depend on it.
- **Verification:** Integration tests.

### NET-012 — Streaming

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Stream sockets must implement the common stream abstractions ([AUTO-014](automation.md#auto-014--shared-stream-abstractions)). The standard library must provide framing helpers for incremental processing of data larger than memory. Examples are length-prefixed and delimiter-based framing.
- **Rationale:** Streaming allows constant-memory processing of large transfers.
- **Verification:** Unit tests.

### NET-013 — Backpressure

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Writes must wait, or report, when the peer or the local buffers cannot accept more data. Standard-library servers and clients must use bounded buffers by default ([CONC-012](../CONCURRENCY.md#conc-012--backpressure)).
- **Rationale:** A fast producer and slow consumer without backpressure leads to unbounded memory growth.
- **Verification:** Integration tests.

### NET-014 — Structured network errors

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Network errors must be distinguishable programmatically by kind. Kinds include connection refused, connection reset, timed out, host unreachable, name resolution failure, address in use, and TLS or certificate failure. Programs must not need to parse message text.
- **Rationale:** Retry and failover logic depends on error kind ([CORE-024](../CORE.md#core-024--structured-error-information)).
- **Verification:** Unit tests.

### NET-015 — Binary data encoding

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide bounds-checked readers and writers over byte buffers. They must handle fixed-width integers in explicit byte orders, variable-length integers and bit fields. Truncated input must produce errors, never faults or out-of-bounds access ([SEC-002](cybersecurity.md#sec-002--bounds-checked-binary-parsing)).
- **Rationale:** Binary protocol implementation is a core networking and security task.
- **Verification:** Unit tests; Fuzzing.

### NET-016 — Incremental protocol parsing

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library should support writing parsers that consume input incrementally, resume after partial reads and report how much input was consumed.
- **Rationale:** Network data arrives in arbitrary fragments. Buffering whole messages before parsing enables memory-exhaustion attacks.
- **Verification:** Unit tests; Fuzzing.

### NET-022 — Concurrent server foundation

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must make it straightforward to accept connections and serve each in its own task within a structured scope ([CONC-004](../CONCURRENCY.md#conc-004--structured-concurrency)). The server must be able to limit concurrent connections and to shut down gracefully by draining in-flight work within a deadline.
- **Rationale:** The dominant server pattern must be safe and simple by default.
- **Verification:** Integration tests.

### NET-023 — Secure network defaults

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Standard and first-party network clients must never silently fall back from an encrypted to an unencrypted connection. Disabling certificate or hostname verification must require an explicit, distinctly named, documented operation, and should produce a warning at build or run time ([SEC-018](cybersecurity.md#sec-018--tls-security-policy)).
- **Rationale:** Disabled verification is one of the most common security defects in network code.
- **Verification:** Unit tests; Security review.

## First-party library requirements

### NET-017 — TLS

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must provide TLS client and server support. It must support TLS 1.3, and TLS 1.2 where needed for interoperability. It must support server name indication (SNI) and ALPN, and it must verify certificates and hostnames by default. Security policy is defined in [SEC-018](cybersecurity.md#sec-018--tls-security-policy). Whether TLS uses platform libraries, a bound external library or a Cretes implementation is a Phase 2+ decision ([P2Q-018](../../PHASE-2-OPEN-QUESTIONS.md#p2q-018--cryptography-and-tls-implementation-strategy)).
- **Rationale:** Encrypted transport is mandatory for modern networked software.
- **Verification:** Integration tests against independent TLS implementations; Security review.

### NET-018 — HTTP client

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must provide an HTTP client that supports HTTP/1.1 and HTTPS, with finite default timeouts, limited redirects, streaming bodies and header-size limits. HTTP/2 SHOULD be supported. HTTP/3 MAY be supported.
- **Rationale:** HTTP is the most widely used application protocol for automation, AI services and APIs.
- **Verification:** Integration tests; Fuzzing of response parsing.

### NET-019 — HTTP server foundation

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should provide HTTP/1.1 server primitives with limits on header size, body size, request rate per connection and idle and read time. The limits exist to resist slow-client and resource-exhaustion attacks. Full web frameworks are left to the ecosystem.
- **Rationale:** Services, webhooks and health endpoints need a secure baseline server.
- **Verification:** Integration tests; Fuzzing.

### NET-020 — WebSockets

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should support WebSocket clients and servers (RFC 6455) with message-size limits and backpressure.
- **Rationale:** Real-time dashboards, streaming AI responses and control channels commonly use WebSockets.
- **Verification:** Integration tests against an independent conformance suite.

### NET-021 — Connection management and pooling

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** HTTP and similar clients should reuse connections through pools. Pools should have per-host and total limits, idle timeouts and detection of broken connections.
- **Rationale:** Connection reuse is critical for throughput and for avoiding port exhaustion.
- **Verification:** Integration tests; Benchmark (`networking/`).

### NET-024 — Network observability hooks

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Network clients and servers should expose hooks for metrics and tracing without requiring modification of library code. Examples of metrics are connection counts, latency and bytes transferred.
- **Rationale:** Operability of production services ([DevOps persona](../../vision/TARGET-USERS.md#devops--platform-engineers)).
- **Verification:** Unit tests.

### NET-025 — URL handling

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should provide URL parsing and construction that follows a documented standard (RFC 3986 or the WHATWG URL Standard) and states which one. Parsing should be consistent across all first-party libraries.
- **Rationale:** Inconsistent URL parsing between components is a known source of SSRF and request-smuggling vulnerabilities.
- **Verification:** Unit tests; Fuzzing.

## Ecosystem

The following are expected to be provided by the ecosystem and are **not** Cretes project commitments, although first-party support may be proposed through RFCs:

- web application frameworks;
- gRPC and other RPC systems;
- QUIC and HTTP/3 servers;
- message-broker clients (for example MQTT, AMQP, Kafka);
- database drivers;
- SSH, SNMP, BGP and other domain-specific protocols.

### NET-026 — Protocol ecosystem support

- **Priority:** MAY · **Layer:** Ecosystem · **Target:** Long-term
- **Requirement:** The project may publish guidance and shared building blocks, such as framing, codecs and test harnesses, for ecosystem protocol libraries.
- **Rationale:** Encourages consistent quality without making the project responsible for every protocol.
- **Verification:** Inspection.

## Related documents

- [Concurrency requirements](../CONCURRENCY.md)
- [Cybersecurity requirements](cybersecurity.md)
- [Performance requirements](../PERFORMANCE.md)
- [Use cases](../USE-CASES.md)
