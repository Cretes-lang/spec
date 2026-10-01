# 2.25 — Networking architecture

> Decision: **ARCH-NET-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[NET-001](../requirements/domains/networking.md#net-001--byte-oriented-data), [NET-002](../requirements/domains/networking.md#net-002--scalable-asynchronous-io), [NET-003](../requirements/domains/networking.md#net-003--connection-scale-design-target), [NET-004](../requirements/domains/networking.md#net-004--ip-address-types), [NET-005](../requirements/domains/networking.md#net-005--ipv6-parity), [NET-006](../requirements/domains/networking.md#net-006--tcp-clients-and-servers), [NET-007](../requirements/domains/networking.md#net-007--udp), [NET-008](../requirements/domains/networking.md#net-008--local-and-low-level-sockets), [NET-009](../requirements/domains/networking.md#net-009--name-resolution), [NET-010](../requirements/domains/networking.md#net-010--timeouts-on-every-network-operation), [NET-011](../requirements/domains/networking.md#net-011--cancellation-of-network-operations), [NET-012](../requirements/domains/networking.md#net-012--streaming), [NET-013](../requirements/domains/networking.md#net-013--backpressure), [NET-014](../requirements/domains/networking.md#net-014--structured-network-errors), [NET-015](../requirements/domains/networking.md#net-015--binary-data-encoding), [NET-016](../requirements/domains/networking.md#net-016--incremental-protocol-parsing), [NET-017](../requirements/domains/networking.md#net-017--tls), [NET-018](../requirements/domains/networking.md#net-018--http-client), [NET-019](../requirements/domains/networking.md#net-019--http-server-foundation), [NET-020](../requirements/domains/networking.md#net-020--websockets), [NET-021](../requirements/domains/networking.md#net-021--connection-management-and-pooling), [NET-022](../requirements/domains/networking.md#net-022--concurrent-server-foundation), [NET-023](../requirements/domains/networking.md#net-023--secure-network-defaults), [NET-024](../requirements/domains/networking.md#net-024--network-observability-hooks), [NET-025](../requirements/domains/networking.md#net-025--url-handling), [NET-026](../requirements/domains/networking.md#net-026--protocol-ecosystem-support), [PERF-013](../requirements/PERFORMANCE.md#perf-013--efficient-io-buffers)

## Proposed decision and rationale

**OS-backed async transport primitives, structured task ownership and separately versioned protocol/security libraries.**

Language features provide bytes, ownership, typed errors and async effects. The runtime provides readiness/completion drivers, task wakeups and monotonic timers. Standard-library transport interfaces provide typed IPv4/IPv6 endpoints, TCP listeners/streams, UDP datagrams and DNS resolution. Local/raw sockets are platform-dependent opt-in capabilities with explicit privilege/availability errors. Protocols do not belong in the compiler.

A platform driver normalizes readiness systems (epoll/kqueue) and completion systems (IOCP) into terminal operation outcomes while preserving partial reads/writes and buffer ownership. DNS may use a bounded blocking pool; cancelled callers do not free buffers still used by a worker. No particular third-party event library is selected in this proposal; libuv's design is useful evidence for the platform differences, not an automatic dependency choice.

Every operation accepts a cancellation/deadline context. Streams carry demand and bounded buffering. Backpressure propagates from consumers to producers; unbounded queueing is not a default. A server owns connection groups, accepts within configured limits, and drains or cancels them on shutdown. The Phase 1 connection-scale target is a future benchmark scenario, not an achieved capacity.

First-party packages implement HTTP client/server foundations, TLS, WebSockets, URL parsing and bounded connection pooling. Pools isolate origins/security configurations, cap idle/active connections and honor deadlines; retries are explicit and limited to safe/idempotent policies. TLS verifies certificates/hostnames by default and rejects silent downgrade. Provider choice is deferred to security review.

Binary encoding specifies byte order explicitly. Incremental parsers return need-more-data, value or structured error, maintain resource limits and never advance beyond validated input. Network errors identify operation, peer where safe, provider/OS category and partial progress. Observability hooks use bounded events with credentials redacted. Framework routing, databases and application protocols remain ecosystem concerns.

## Options, advantages, disadvantages and rejected alternatives

Thread-per-connection was rejected as the default high-concurrency model. A compiler-bundled HTTP framework was rejected as scope creep. One identical OS syscall path was rejected because readiness and completion have different lifetimes. An adapter-based transport runtime is proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: authentication defaults, buffer lifetime and parser limits are critical. Performance: copies, wakeups, connection-state memory and pool pressure require measurement. DX: shared cancellation/errors across protocols. Implementation: driver conformance fixtures plus fake-clock/cancellation tests.

## Future verification

Later test IPv4/IPv6 parity, partial I/O, slow consumers, reset/EOF, timeout/cancel races, DNS saturation, TLS failures, bounded pools and high-idle-connection memory.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
