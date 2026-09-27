# Cybersecurity requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

Cybersecurity is one of the four official Cretes domains. It covers **secure software development** and **defensive security engineering**:

- building secure applications and services;
- cryptographic applications;
- protocol and binary analysis;
- security analysis tooling;
- defensive utilities.

The primary persona is the [Cybersecurity Engineer](../../vision/TARGET-USERS.md#cybersecurity-engineers).

Offensive tooling distributions are not a project deliverable ([NON-GOALS.md](../NON-GOALS.md)). Cretes is a general-purpose language, and its use is governed by its license and applicable law.

This document separates three concerns that are often confused:

| Part | Concern | Question it answers |
| --- | --- | --- |
| [A. Language safety](#part-a--language-safety) | Properties of the language and compiler | Can Cretes code be written without memory-corruption and type-confusion vulnerabilities? |
| [B. Security libraries](#part-b--security-libraries) | Cryptography, TLS, encoding, secrets | Can developers build secure systems without misusing primitives? |
| [C. Security tooling and supply chain](#part-c--security-tooling-and-supply-chain) | Toolchain, packages, analysis | Can users trust what they build and depend on? |

Security-sensitive interfaces must be **misuse-resistant**. The easy path must be the secure path, and dangerous operations must be explicit ([Principle 1](../../principles/DESIGN-PRINCIPLES.md#1-safety-by-default), [Principle 9](../../principles/DESIGN-PRINCIPLES.md#9-secure-ecosystem)).

Terminology, layers and targets are defined in the [requirements framework](../README.md).

## Part A — Language safety

Most language-safety outcomes are defined in [SAFETY.md](../SAFETY.md). The requirements below add the security-specific aspects.

### SEC-001 — Memory-safe development objective

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** It must be possible to write complete security-sensitive programs, such as parsers, network services and cryptographic protocol logic, entirely in safe code. Any unsafe code required must be confined to audited standard or first-party libraries. The safety outcomes of [SAFE-001](../SAFETY.md#safe-001--no-undefined-behavior-in-safe-code) to [SAFE-007](../SAFETY.md#safe-007--no-use-of-uninitialized-values) apply.
- **Rationale:** Memory-safety defects account for a large share of severe vulnerabilities in software written in memory-unsafe languages.
- **Verification:** Security review; Inspection of standard-library unsafe usage.

### SEC-002 — Bounds-checked binary parsing

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Standard-library facilities for reading binary data must report truncated or malformed input as recoverable errors. They must never fault, read out of bounds or return uninitialized data ([NET-015](networking.md#net-015--binary-data-encoding)).
- **Rationale:** Parsing untrusted binary input, such as packets, file formats and certificates, is the primary attack surface of security tools.
- **Verification:** Unit tests; Fuzzing.

### SEC-003 — Checked length arithmetic in parsers

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Standard and first-party parsers and decoders must use checked arithmetic ([SAFE-009](../SAFETY.md#safe-009--explicit-overflow-handling-operations)) for all length, offset and size computations derived from input.
- **Rationale:** Integer overflow in length computation is a classic prelude to buffer overflows and allocation attacks.
- **Verification:** Security review; Fuzzing.

### SEC-004 — Constant-time operations

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library should provide constant-time comparison and selection primitives for secret data. The documentation should state exactly what timing guarantees are provided and under which build configurations. How the compiler preserves constant-time properties is a Phase 2 question ([P2Q-020](../../PHASE-2-OPEN-QUESTIONS.md#p2q-020--constant-time-code-and-compiler-guarantees)).
- **Rationale:** Timing side channels leak secrets, such as MAC tags, tokens and keys.
- **Verification:** Security review; Statistical timing tests.

### SEC-005 — Secret zeroization

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide types for holding secrets that:
  - are erased from memory when released, with an erasure the compiler cannot optimize away;
  - are excluded from debug formatting and logging by default ([SEC-022](#sec-022--secret-redaction-in-diagnostics-and-logs));
  - avoid unintended copies, as far as the memory-management model allows.

  The interaction with the memory-management model is a Phase 2 question ([P2Q-021](../../PHASE-2-OPEN-QUESTIONS.md#p2q-021--secret-lifetime-under-the-memory-model)).
- **Rationale:** Secrets that linger in memory can be exposed through crash dumps, swap or memory-disclosure bugs.
- **Verification:** Security review; Integration tests.

## Part B — Security libraries

The cryptographic requirements below are satisfied by the standard library or first-party packages. The choice between them is a Phase 2+ decision ([P2Q-018](../../PHASE-2-OPEN-QUESTIONS.md#p2q-018--cryptography-and-tls-implementation-strategy)). Naming an algorithm identifies an interoperability need. It is not a mandate to implement the algorithm from scratch ([SEC-015](#sec-015--cryptographic-implementation-assurance)).

### SEC-006 — Secure randomness

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide cryptographically secure random bytes and values, sourced from the operating system's secure generator. This must be the default, most discoverable random facility. Any non-cryptographic generator, used for simulations or sampling for example, must be clearly and distinctly named as unsuitable for security purposes.
- **Rationale:** Using non-cryptographic generators for tokens and keys is a frequent vulnerability.
- **Verification:** Unit tests; Security review.

### SEC-007 — Cryptographic hashing

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must provide the SHA-256 and SHA-512 hash functions (SHA-2 family). SHA-3 and BLAKE2 or BLAKE3 SHOULD be provided. Hash interfaces must support streaming input. Non-cryptographic hashes must be clearly distinguished by name.
- **Rationale:** Integrity checks, content addressing and signatures rely on standard hashes.
- **Verification:** Unit tests against published test vectors.

### SEC-008 — Collision-resistant hash tables by default

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** The default hashing used by the standard key-value map and set ([CORE-033](../CORE.md#core-033--core-collections)) must resist algorithmic-complexity attacks from attacker-chosen keys, for example through keyed or randomized hashing. Faster, unkeyed hashing may be available as an explicit choice. Because keyed hashing can make iteration order vary between runs, the documentation must state the iteration-order guarantees of these collections. Code that needs reproducible output ([CORE-025](../CORE.md#core-025--deterministic-compilation), [AI-022](ai-ml.md#ai-022--reproducible-numerical-results)) must be able to obtain a deterministic order explicitly.
- **Rationale:** Hash-flooding denial-of-service attacks target servers that insert request data into hash tables.
- **Verification:** Security review; Unit tests.

### SEC-009 — Message authentication

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must provide HMAC with SHA-2 hashes. Tag verification must use constant-time comparison.
- **Rationale:** Webhooks, API signatures and token formats depend on MACs.
- **Verification:** Unit tests against published test vectors.

### SEC-010 — Authenticated encryption

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must provide authenticated encryption with associated data (AEAD), including AES-GCM and ChaCha20-Poly1305. The high-level encryption interface must only offer authenticated modes, and must generate nonces safely by default. Unauthenticated modes, if offered at all, must be confined to the explicitly hazardous layer ([SEC-014](#sec-014--misuse-resistant-api-layering)).
- **Rationale:** Unauthenticated encryption and nonce reuse are among the most common cryptographic misuse bugs.
- **Verification:** Unit tests against published test vectors; Security review.

### SEC-011 — Digital signatures

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must provide Ed25519 signing and verification. ECDSA over P-256 SHOULD be provided. RSA-PSS and RSA PKCS#1 v1.5 signature verification SHOULD be provided for interoperability.
- **Rationale:** Package signing, software updates, tokens and protocols rely on signatures.
- **Verification:** Unit tests against published test vectors.

### SEC-012 — Key agreement

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should provide X25519 key agreement and ECDH over P-256. The project should track standardized post-quantum key-encapsulation mechanisms and plan their adoption.
- **Rationale:** Needed for protocol implementation beyond TLS. Post-quantum migration is under way across the industry.
- **Verification:** Unit tests against published test vectors.

### SEC-013 — Key derivation and password hashing

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must provide HKDF for key derivation. It SHOULD provide a memory-hard password-hashing function, such as Argon2id or scrypt, with secure default parameters. Password hashing must be clearly separated from general-purpose hashing.
- **Rationale:** Storing passwords with fast hashes is a persistent vulnerability.
- **Verification:** Unit tests against published test vectors.

### SEC-014 — Misuse-resistant API layering

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cryptographic interfaces must be layered:
  - a **high-level** layer that performs complete tasks, such as encrypting a message, signing data or hashing a password, with secure defaults and no algorithm-selection burden;
  - a **low-level** layer that exposes individual primitives. This layer must be clearly labeled as requiring expertise and must be separated from the high-level interface.

  Keys, nonces, tags and plaintexts must have distinct types where that prevents confusion.
- **Rationale:** Most cryptographic vulnerabilities come from misusing correct primitives, not from broken primitives.
- **Verification:** Security review.

### SEC-015 — Cryptographic implementation assurance

- **Priority:** MUST · **Layer:** Process · **Target:** Post-v0.1
- **Requirement:** No cryptographic implementation may be labeled stable until it has passed published test vectors and independent security review. The project must prefer established, audited implementations over new ones. Any original implementation requires an RFC that justifies it.
- **Rationale:** Cryptographic code is exceptionally hard to get right. [GOVERNANCE.md](https://github.com/Cretes-lang/.github/blob/main/GOVERNANCE.md) already calls for extra review of security-sensitive changes.
- **Verification:** Inspection; Security review.

### SEC-016 — Algorithm agility and legacy algorithms

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** The cryptographic libraries must have a documented process for deprecating algorithms. Weak or broken algorithms, such as MD5, SHA-1 for signatures, DES and RC4, must not be used by any default. If they are provided for interoperability or forensic analysis, they must be available only through interfaces explicitly labeled as legacy or insecure.
- **Rationale:** Security tools need to read legacy formats. That need must not leak weak algorithms into new designs.
- **Verification:** Security review.

### SEC-017 — Key and credential handling

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Keys and credentials must be represented by dedicated types, not plain byte or text values. These types must satisfy [SEC-005](#sec-005--secret-zeroization). Import and export in standard encodings, such as PEM, DER and JWK, SHOULD be supported. The standard library SHOULD allow credentials to be read from environment variables and files directly into secret types, so that they never exist as ordinary text values. Integration with operating-system credential stores MAY be provided.
- **Rationale:** Dedicated types prevent accidental logging, comparison with non-constant-time equality and confusion between key kinds.
- **Verification:** Unit tests; Security review.

### SEC-018 — TLS security policy

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** The TLS implementation ([NET-017](networking.md#net-017--tls)) must default to:
  - TLS 1.3 preferred, with TLS 1.2 as the minimum;
  - only cipher suites with forward secrecy and authenticated encryption;
  - certificate-chain validation against the platform or configured trust store;
  - hostname verification.

  Relaxing any default must be explicit ([NET-023](networking.md#net-023--secure-network-defaults)). Defaults must be updatable in patch releases as guidance evolves.
- **Rationale:** Secure defaults protect developers who never change configuration.
- **Verification:** Integration tests; Security review.

### SEC-019 — Certificate handling

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must parse X.509 certificates and validate certificate chains, including name constraints, validity periods and key usage. Use of the platform trust store must be the default. Custom trust anchors must be configured explicitly. Revocation checking SHOULD be supported. Certificate pinning MAY be supported.
- **Rationale:** Certificate validation errors are a recurring class of severe vulnerabilities.
- **Verification:** Integration tests against public certificate-validation test suites; Fuzzing.

### SEC-020 — Encoding and decoding

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide hexadecimal and Base64 encoding and decoding, both standard and URL-safe. Validation must be strict by default. Any lenient decoding must be explicitly selected.
- **Rationale:** Lenient decoders create ambiguity that attackers exploit to bypass validation.
- **Verification:** Unit tests; Fuzzing.

### SEC-021 — Resource limits for untrusted input

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Every standard and first-party parser or decoder that may process untrusted input must enforce configurable limits with safe defaults. Such parsers include JSON, HTTP, archives, certificates, compressed data and model files. The limits must cover input size, nesting depth, element counts and decompressed size.
- **Rationale:** Resource-exhaustion attacks exploit parsers that trust declared sizes.
- **Verification:** Unit tests; Fuzzing.

### SEC-022 — Secret redaction in diagnostics and logs

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Values of secret-holding types must be redacted by default when formatted for logs, debug output, error messages or fault reports. Revealing a secret must require an explicit operation. Standard-library error messages must not embed secret values.
- **Rationale:** Credentials in logs are a common cause of breaches ([AUTO-020](automation.md#auto-020--logging)).
- **Verification:** Unit tests; Security review.

## Part C — Security tooling and supply chain

### SEC-023 — Dependency integrity

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The package manager must record the exact resolved version and a cryptographic hash of every dependency in a lock file. It must verify those hashes on every fetch and fail on mismatch.
- **Rationale:** Prevents tampering in transit, at mirrors or at the registry from altering a build silently.
- **Verification:** Integration tests; Security review.

### SEC-024 — Package provenance and signing

- **Priority:** MUST · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** Before the package registry is opened for public publishing, packages must carry verifiable provenance or signatures that link them to their publisher and, where possible, to their source. The mechanism is a Phase 2+ decision.
- **Rationale:** Registry compromise and account takeover are established supply-chain attack vectors.
- **Verification:** Security review.

### SEC-025 — No implicit code execution during dependency installation

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** Resolving, fetching and installing dependencies must not execute code from those dependencies. Any build-time code execution by dependencies, such as code generation or native builds, must be declared in the manifest, visible to auditing tools, and subject to a project-level policy that can deny it.
- **Rationale:** Install-time scripts are a primary mechanism of malicious packages ([CORE-028](../CORE.md#core-028--declarative-package-manifest)).
- **Verification:** Integration tests; Security review.

### SEC-026 — Vulnerability advisories and audit

- **Priority:** MUST · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** The project must maintain a public vulnerability advisory database for Cretes packages. The toolchain must be able to report when a project's locked dependencies are affected by a published advisory.
- **Rationale:** Users need to know when their dependencies are vulnerable. This complements [SECURITY.md](https://github.com/Cretes-lang/.github/blob/main/SECURITY.md).
- **Verification:** Integration tests.

### SEC-027 — Reproducible builds

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Before 1.0
- **Requirement:** Building the same source with the same toolchain, dependencies, target and configuration must be able to produce bit-for-bit identical artifacts. This applies to toolchain releases and to user builds ([CORE-025](../CORE.md#core-025--deterministic-compilation)).
- **Rationale:** Reproducibility allows independent verification that binaries match source.
- **Verification:** Integration tests (independent rebuilds compared).

### SEC-028 — Software bill of materials

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain should be able to emit a software bill of materials (SBOM) for a build in a standard format, such as SPDX or CycloneDX. The SBOM should include native library dependencies.
- **Rationale:** SBOMs are increasingly required for procurement and incident response.
- **Verification:** Integration tests.

### SEC-029 — Unsafe and FFI audit reporting

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain must be able to report, for a project and all its dependencies:
  - every unsafe region ([SAFE-016](../SAFETY.md#safe-016--explicit-and-auditable-unsafe-code));
  - every foreign declaration and native library dependency ([INTOP-019](../INTEROPERABILITY.md#intop-019--declared-native-dependencies));
  - every build-time code execution ([SEC-025](#sec-025--no-implicit-code-execution-during-dependency-installation)).
- **Rationale:** Reviewers need to find where the language's guarantees stop.
- **Verification:** Integration tests.

### SEC-030 — Fuzzing support

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain should support coverage-guided fuzz testing of Cretes functions, integrated with the test runner ([DX-011](../CORE.md#dx-011--integrated-test-runner)).
- **Rationale:** Fuzzing is the most effective way to find parser bugs. Built-in support increases adoption.
- **Verification:** Integration tests.

### SEC-031 — Security-focused static analysis

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The linter ([DX-010](../CORE.md#dx-010--linter)) should include security rules. Examples are use of legacy cryptography, disabled certificate verification, shell invocation with interpolated input, discarded secret-type values and confusable identifiers. The analysis interfaces should allow third-party security analyzers.
- **Rationale:** Catches security anti-patterns early and supports security review.
- **Verification:** Diagnostic tests.

### SEC-032 — Toolchain release integrity

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** Every toolchain release artifact must be published with checksums. From the first release, artifacts SHOULD also be signed or carry verifiable build provenance. Release workflows must use least-privilege credentials and must not run untrusted pull-request code with secrets ([ENGINEERING.md](https://github.com/Cretes-lang/.github/blob/main/ENGINEERING.md)).
- **Rationale:** A compromised compiler compromises every program built with it.
- **Verification:** Inspection at release review; Security review.

### SEC-033 — Scope of defensive utilities

- **Priority:** SHOULD · **Layer:** Ecosystem · **Target:** Long-term
- **Requirement:** The standard and first-party libraries should provide the **building blocks** for defensive security tools:
  - parsing;
  - cryptography;
  - networking, including platform-specific raw access ([NET-008](networking.md#net-008--local-and-low-level-sockets));
  - encoding;
  - structured logging.

  Complete security products, such as scanners, intrusion detection, forensics suites and malware analysis frameworks, are left to the ecosystem.
- **Rationale:** Keeps the project focused while enabling the security ecosystem.
- **Verification:** Inspection.

### SEC-034 — Registry account and namespace protection

- **Priority:** SHOULD · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** The package registry should require multi-factor authentication for publishers of widely used packages. It should also mitigate typosquatting and name confusion, and should support yanking compromised versions with a public record.
- **Rationale:** Account takeover and typosquatting are common registry attacks.
- **Verification:** Security review.

## Related documents

- [Safety requirements](../SAFETY.md)
- [Interoperability requirements](../INTEROPERABILITY.md)
- [Networking requirements](networking.md)
- [Security policy](https://github.com/Cretes-lang/.github/blob/main/SECURITY.md)
- [Phase 1 review](../../reviews/PHASE-1-REVIEW.md)
