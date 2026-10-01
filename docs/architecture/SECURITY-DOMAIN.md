# 2.27 — Defensive cybersecurity libraries

> Decision: **ARCH-SECURITY-DOMAIN-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[SEC-001](../requirements/domains/cybersecurity.md#sec-001--memory-safe-development-objective), [SEC-002](../requirements/domains/cybersecurity.md#sec-002--bounds-checked-binary-parsing), [SEC-003](../requirements/domains/cybersecurity.md#sec-003--checked-length-arithmetic-in-parsers), [SEC-004](../requirements/domains/cybersecurity.md#sec-004--constant-time-operations), [SEC-005](../requirements/domains/cybersecurity.md#sec-005--secret-zeroization), [SEC-006](../requirements/domains/cybersecurity.md#sec-006--secure-randomness), [SEC-007](../requirements/domains/cybersecurity.md#sec-007--cryptographic-hashing), [SEC-008](../requirements/domains/cybersecurity.md#sec-008--collision-resistant-hash-tables-by-default), [SEC-009](../requirements/domains/cybersecurity.md#sec-009--message-authentication), [SEC-010](../requirements/domains/cybersecurity.md#sec-010--authenticated-encryption), [SEC-011](../requirements/domains/cybersecurity.md#sec-011--digital-signatures), [SEC-012](../requirements/domains/cybersecurity.md#sec-012--key-agreement), [SEC-013](../requirements/domains/cybersecurity.md#sec-013--key-derivation-and-password-hashing), [SEC-014](../requirements/domains/cybersecurity.md#sec-014--misuse-resistant-api-layering), [SEC-015](../requirements/domains/cybersecurity.md#sec-015--cryptographic-implementation-assurance), [SEC-016](../requirements/domains/cybersecurity.md#sec-016--algorithm-agility-and-legacy-algorithms), [SEC-017](../requirements/domains/cybersecurity.md#sec-017--key-and-credential-handling), [SEC-018](../requirements/domains/cybersecurity.md#sec-018--tls-security-policy), [SEC-019](../requirements/domains/cybersecurity.md#sec-019--certificate-handling), [SEC-020](../requirements/domains/cybersecurity.md#sec-020--encoding-and-decoding), [SEC-021](../requirements/domains/cybersecurity.md#sec-021--resource-limits-for-untrusted-input), [SEC-022](../requirements/domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs), [SEC-033](../requirements/domains/cybersecurity.md#sec-033--scope-of-defensive-utilities)

## Proposed decision and rationale

**Checked binary processing, uniquely owned secrets and reviewed cryptographic providers behind misuse-resistant APIs.**

Binary parsers use bounds-checked byte views and checked length/offset arithmetic. Decoders distinguish invalid input from incomplete input and cap nesting, allocation and work. Packet representation contains validated lengths and explicit byte order; raw capture or privileged sockets are opt-in external/OS facilities, not offensive tooling bundled with the compiler.

Secure randomness is separate from deterministic pseudorandom generators. It uses an OS/provider entropy source and fails closed if unavailable. v0.1 hash tables use per-process unpredictable seeding from the OS and an appropriate collision-resistant keyed strategy; deterministic iteration is requested explicitly through sorting/ordered containers. No silent deterministic fallback is allowed when security seed initialization fails.

Later crypto APIs cover hashing, MAC, authenticated encryption, signatures, key agreement, KDF/password hashing and certificates through vetted providers. High-level encryption owns nonce-generation/state policy and does not release unauthenticated plaintext. Expert primitives are visibly separate. Legacy algorithms are opt-in and policy-gated. Keys have types describing purpose/algorithm; formats validate parameters before costly operations. Certificate validation includes hostname, chain, time and policy; disabling checks is never a silent fallback.

Secret storage is uniquely owned, non-copyable, non-formatting and non-serializing by default. Read credentials directly into that storage when APIs permit; exposure to ordinary text/bytes is explicit. Release invokes a provider/OS-supported non-elidable zeroization operation. The compiler must not introduce implicit secret copies. Register spills, swap, dumps, backups and foreign copies remain documented limitations; locked memory is optional and fallible, not a universal guarantee. Abort does not promise zeroization.

Constant-time guarantees are limited to identified reviewed primitives and documented hardware/compiler conditions. Do not label arbitrary Cretes code constant-time from source shape alone. Keep such provider calls outside transformations that invalidate their reviewed assumptions. Protocol, credential and key errors redact sensitive material.

## Options, advantages, disadvantages and rejected alternatives

Writing novel cryptography was rejected. One low-level byte API for all users was rejected for misuse risk. Secret strings with ordinary copying were rejected. Vetted providers plus typed high-level wrappers are proposed, with exact providers deferred.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: native provider bugs and secret copies outside controlled storage remain risks. Performance: constant-time/zeroization checks and parser limits need targeted validation; no blanket speed claims. DX: secure defaults and clear expert boundaries. Implementation: wrapper contracts, test vectors, timing assessment and provider-update process.

## Future verification

Later run known-answer/negative tests, authentication-failure tests, seed failure, parser fuzzing, redaction checks, optimized zeroization inspection and provider-specific constant-time review.

## Risks and open questions

Provider/algorithm selection and their security assessment remain DEFERRED before release; no implementation guarantee is claimed by this proposal.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
