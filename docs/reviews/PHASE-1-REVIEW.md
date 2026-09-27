# Phase 1 review record

> **Status:** Phase 1 output · **Review date:** 2026-09-27

This record documents the security, consistency and scope reviews performed on the Phase 1 requirements baseline, and the Phase 1 completion checklist. Under the single-maintainer policy in [GOVERNANCE.md](https://github.com/Cretes-lang/.github/blob/main/GOVERNANCE.md), this is a documented self-review. It is not an independent review. An independent security review of the cryptography and supply-chain requirements is recommended once a qualified reviewer is available.

Tracking issue: [Cretes-lang/spec#1](https://github.com/Cretes-lang/spec/issues/1).

## Contents

- [Scope of review](#scope-of-review)
- [Security review](#security-review)
- [Consistency review](#consistency-review)
- [Scope review](#scope-review)
- [Completion checklist](#completion-checklist)

## Scope of review

All documents under `docs/` and the repository README:

| Document | Phase 1 section |
| --- | --- |
| [vision/VISION.md](../vision/VISION.md) | 1.1 Language mission |
| [vision/TARGET-USERS.md](../vision/TARGET-USERS.md) | 1.2 Target developers |
| [requirements/USE-CASES.md](../requirements/USE-CASES.md) | 1.3 Core use cases |
| [principles/DESIGN-PRINCIPLES.md](../principles/DESIGN-PRINCIPLES.md) | 1.4 Design principles |
| [requirements/domains/automation.md](../requirements/domains/automation.md) | 1.5 Automation |
| [requirements/domains/networking.md](../requirements/domains/networking.md) | 1.6 Networking |
| [requirements/domains/ai-ml.md](../requirements/domains/ai-ml.md) | 1.7 AI/ML Applications |
| [requirements/domains/cybersecurity.md](../requirements/domains/cybersecurity.md) | 1.8 Cybersecurity |
| [requirements/SAFETY.md](../requirements/SAFETY.md) | 1.9 Safety |
| [requirements/PERFORMANCE.md](../requirements/PERFORMANCE.md) | 1.10 Performance |
| [requirements/CONCURRENCY.md](../requirements/CONCURRENCY.md) | 1.11 Concurrency |
| [requirements/INTEROPERABILITY.md](../requirements/INTEROPERABILITY.md) | 1.12 Interoperability |
| [requirements/PLATFORMS.md](../requirements/PLATFORMS.md) | 1.13 Platforms |
| [requirements/NON-GOALS.md](../requirements/NON-GOALS.md) | 1.14 Scope and non-goals |
| [requirements/V0.1-REQUIREMENTS.md](../requirements/V0.1-REQUIREMENTS.md) | 1.15 v0.1 requirements |
| [requirements/CORE.md](../requirements/CORE.md) | Cross-cutting core and DX requirements |
| [requirements/README.md](../requirements/README.md) | Terminology, IDs, traceability |
| [PHASE-2-OPEN-QUESTIONS.md](../PHASE-2-OPEN-QUESTIONS.md) | Phase 2 question register |

## Security review

The requirements were reviewed for internal contradictions and weaknesses that would undermine security. Each finding is listed with its resolution.

| # | Potential issue | Finding | Resolution |
| --- | --- | --- | --- |
| S1 | Claiming memory safety while allowing unrestricted unsafe memory access | Low-level control ([Principle 15](../principles/DESIGN-PRINCIPLES.md#15-clear-escape-hatches-for-expert-low-level-development)), FFI and raw sockets could be read as unrestricted access. | Safety guarantees are scoped to **safe code** ([SAFETY.md definitions](../requirements/SAFETY.md#definitions)). Unsafe operations must be explicit, scoped and enumerable ([SAFE-016](../requirements/SAFETY.md#safe-016--explicit-and-auditable-unsafe-code)), with package-level policies ([SAFE-019](../requirements/SAFETY.md#safe-019--package-level-unsafe-policy)) and audit reporting ([SEC-029](../requirements/domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting)). v0.1 has no user-visible unsafe code. |
| S2 | Unclear FFI trust boundary | The compiler cannot verify foreign code or foreign declarations. | FFI is an unsafe boundary ([SAFE-018](../requirements/SAFETY.md#safe-018--ffi-is-an-unsafe-boundary)). Foreign declarations are not trusted ([INTOP-017](../requirements/INTEROPERABILITY.md#intop-017--unsafe-ffi-declarations-are-not-trusted-by-default)). Ownership must be explicit ([INTOP-005](../requirements/INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary)). Unwinding across foreign frames is constrained ([INTOP-007](../requirements/INTEROPERABILITY.md#intop-007--error-propagation-across-the-boundary)). Native dependencies must be declared ([INTOP-019](../requirements/INTEROPERABILITY.md#intop-019--declared-native-dependencies)). |
| S3 | Insecure cryptographic defaults | Legacy algorithms are needed for interoperability and forensics. | Legacy algorithms are never defaults and are available only through explicitly labeled interfaces ([SEC-016](../requirements/domains/cybersecurity.md#sec-016--algorithm-agility-and-legacy-algorithms)). High-level APIs expose only authenticated encryption with safe nonce handling ([SEC-010](../requirements/domains/cybersecurity.md#sec-010--authenticated-encryption), [SEC-014](../requirements/domains/cybersecurity.md#sec-014--misuse-resistant-api-layering)). Implementations need independent review before being labeled stable ([SEC-015](../requirements/domains/cybersecurity.md#sec-015--cryptographic-implementation-assurance)). |
| S4 | Insecure TLS defaults, or silent downgrade | An option to disable verification is a known source of defects. | Verification is on by default, and disabling it must be explicit, distinctly named and should warn ([NET-023](../requirements/domains/networking.md#net-023--secure-network-defaults), [SEC-018](../requirements/domains/cybersecurity.md#sec-018--tls-security-policy)). There is no silent plaintext fallback. |
| S5 | Secrets exposed through logging, debug output or faults | Logging, diagnostics and fault reports could print secrets. | Secret types are redacted by default everywhere ([SEC-022](../requirements/domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs), [AUTO-020](../requirements/domains/automation.md#auto-020--logging)). **Residual risk:** secrets held as plain text are not detectable. **Mitigation added during review:** [SEC-017](../requirements/domains/cybersecurity.md#sec-017--key-and-credential-handling) now asks that credentials can be read directly into secret types. A linter rule is proposed in [SEC-031](../requirements/domains/cybersecurity.md#sec-031--security-focused-static-analysis). |
| S6 | Secrets lingering in memory | Zeroization may be defeated by the memory model, for example by moving collectors or implicit copies. | Recorded as open question [P2Q-021](../PHASE-2-OPEN-QUESTIONS.md#p2q-021--secret-lifetime-under-the-memory-model). The memory-model evaluation must include zeroization ([SAFE-023](../requirements/SAFETY.md#safe-023--memory-management-evaluation-criteria)). |
| S7 | Constant-time guarantees undermined by optimization | An optimizing backend may transform constant-time code. | Recorded as [P2Q-020](../PHASE-2-OPEN-QUESTIONS.md#p2q-020--constant-time-code-and-compiler-guarantees). [SEC-004](../requirements/domains/cybersecurity.md#sec-004--constant-time-operations) requires the documentation to state the actual guarantees. |
| S8 | Unsafe dependency assumptions | Install-time scripts, unverified downloads and registry takeover. | Hash-locked dependencies ([SEC-023](../requirements/domains/cybersecurity.md#sec-023--dependency-integrity)). No code execution during installation ([SEC-025](../requirements/domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation)). Declarative manifests ([CORE-028](../requirements/CORE.md#core-028--declarative-package-manifest)). Provenance before a public registry ([SEC-024](../requirements/domains/cybersecurity.md#sec-024--package-provenance-and-signing)). Registry account protections ([SEC-034](../requirements/domains/cybersecurity.md#sec-034--registry-account-and-namespace-protection)). |
| S9 | Compile-time code execution | Macros or compile-time evaluation of dependency code would reintroduce the risk addressed in S8. | Recorded as [P2Q-025](../PHASE-2-OPEN-QUESTIONS.md#p2q-025--compile-time-code-execution-and-metaprogramming), with a security note. Name resolution must not require execution ([CORE-009](../requirements/CORE.md#core-009--name-resolution-without-execution)). |
| S10 | Command injection in automation | Shell execution is a common automation pattern. | Argument-vector process creation is the default ([AUTO-009](../requirements/domains/automation.md#auto-009--structured-process-creation)). Shell execution is separate and explicit ([AUTO-010](../requirements/domains/automation.md#auto-010--explicit-shell-invocation)). |
| S11 | Path traversal and decompression bombs | Archive extraction and path handling. | Extraction must reject escaping entries and enforce size limits ([AUTO-022](../requirements/domains/automation.md#auto-022--archives-and-compression)). Paths use a dedicated abstraction ([AUTO-008](../requirements/domains/automation.md#auto-008--path-abstraction)). |
| S12 | Unsafe deserialization | Pickle-style model loading executes code. | Prohibited in standard and first-party libraries ([AI-017](../requirements/domains/ai-ml.md#ai-017--safe-model-and-data-loading), [AUTO-017](../requirements/domains/automation.md#auto-017--structured-serialization)). |
| S13 | Denial of service through untrusted input | Unbounded parsers, queues and buffers. | Resource limits on all parsers of untrusted input ([SEC-021](../requirements/domains/cybersecurity.md#sec-021--resource-limits-for-untrusted-input)). Bounded queues by default ([CONC-012](../requirements/CONCURRENCY.md#conc-012--backpressure), [NET-013](../requirements/domains/networking.md#net-013--backpressure)). Finite network timeouts ([NET-010](../requirements/domains/networking.md#net-010--timeouts-on-every-network-operation)). Hash-flooding resistance ([SEC-008](../requirements/domains/cybersecurity.md#sec-008--collision-resistant-hash-tables-by-default)). |
| S14 | Randomized hashing versus reproducibility | Keyed hashing (SEC-008) can make map iteration order vary between runs. This conflicts with reproducible output. | **Clarified during review:** SEC-008 now requires documented iteration-order guarantees and an explicit way to obtain deterministic order. |
| S15 | Deceptive source text | Bidirectional-control characters can hide code from reviewers. | Detected by default from v0.1 ([CORE-005](../requirements/CORE.md#core-005--protection-against-deceptive-source-text)). |
| S16 | Environment mutation races | `setenv`-style mutation is not thread-safe on several platforms. | [AUTO-013](../requirements/domains/automation.md#auto-013--environment-variables) requires a design that cannot cause data races in safe code. |
| S17 | Profile-dependent overflow behavior | Tested behavior could differ from deployed behavior. | Documented as a security note in [P2Q-009](../PHASE-2-OPEN-QUESTIONS.md#p2q-009--default-integer-overflow-behavior). The overflow behavior is never undefined ([SAFE-008](../requirements/SAFETY.md#safe-008--defined-integer-overflow)). |
| S18 | Raw sockets and privileged operations | Could be misused, or used implicitly. | MAY-level, platform-specific, subject to OS privileges and never implicit ([NET-008](../requirements/domains/networking.md#net-008--local-and-low-level-sockets)). Offensive tooling bundles are a non-goal (NG-07). |
| S19 | Playground executing untrusted code | Long-term service risk. | Sandbox and credential isolation are required if a playground is operated ([DX-016](../requirements/CORE.md#dx-016--online-playground)). |
| S20 | Toolchain compromise | A compromised compiler compromises all output. | Checksums from v0.1, and signatures or provenance SHOULD be provided ([SEC-032](../requirements/domains/cybersecurity.md#sec-032--toolchain-release-integrity)). Reproducible builds before 1.0 ([SEC-027](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds)). Bootstrap auditability is included in [P2Q-023](../PHASE-2-OPEN-QUESTIONS.md#p2q-023--implementation-language-and-bootstrapping). |
| S21 | Memory-mapped files and external modification | Concurrent external writes can break safety assumptions. | [AI-014](../requirements/domains/ai-ml.md#ai-014--memory-efficient-data-handling) requires such cases to be unsafe or documented. |

**Unresolved security architecture questions for Phase 2:** P2Q-004, P2Q-009, P2Q-018, P2Q-020, P2Q-021, P2Q-024 and P2Q-025.

## Consistency review

| Check | Method | Result |
| --- | --- | --- |
| Requirement record format | Every requirement heading was parsed to confirm it has Priority, Layer, Target, Requirement, Rationale and Verification. Layer and Target values were checked against the vocabularies in the [requirements framework](../requirements/README.md). | Passed. 257 requirements. |
| Requirement ID uniqueness | All requirement headings were extracted, and duplicates were checked. | Passed. No duplicates. |
| Requirement ID gaps | Numbering was checked for gaps in each namespace. | Passed. One numbering gap in the `AI` namespace was closed during drafting, before any external reference existed. |
| Cross-references | Every `NAMESPACE-NNN` and `P2Q-NNN` mention was checked to confirm it resolves to a defined item. | Passed. |
| Relative links and anchors | Every relative Markdown link, and every `#anchor` against GitHub-style heading slugs, was checked. Link text naming an ID was checked to point at that ID's anchor. | Passed. |
| v0.1 list | The set of requirements with target `v0.1` was compared with the rows in [V0.1-REQUIREMENTS.md](../requirements/V0.1-REQUIREMENTS.md), including their priorities. | Passed. 86 requirements (77 MUST, 9 SHOULD). |
| Register counts | Counts in the [requirement register](../requirements/README.md#requirement-register) were recomputed from the documents. | Passed. The counts were corrected during review. |
| Naming | The language is referred to as "Cretes", the source extension as `.cretes`, and the domains as Automation, Networking, AI/ML Applications and Cybersecurity. | Passed. "AI/ML" is used as a short form inside the AI/ML Applications domain document. |
| Terminology | MUST/SHOULD/MAY/NON-GOAL are used as defined. Lower-case modal verbs appear in explanatory prose only. | Passed. |
| Heading hierarchy | One H1 per document. Requirements at H3 under H2 section headings. | Passed. |
| Duplicated documents | Checked for overlapping documents with slightly different names. | Passed. One canonical document per topic. The Phase 0 [spec README](../../README.md) was extended, not duplicated. |
| Duplicate or contradictory requirements | Overlaps were reviewed manually. [NET-001](../requirements/domains/networking.md#net-001--byte-oriented-data) (byte views) and [AI-006](../requirements/domains/ai-ml.md#ai-006--buffer-views) (general buffer views) overlap intentionally: NET-001 is the v0.1 subset. [SAFE-012](../requirements/SAFETY.md#safe-012--data-race-freedom) (MUST, outcome) and [CONC-013](../requirements/CONCURRENCY.md#conc-013--diagnosing-unsafe-sharing) (SHOULD, early diagnosis) are complementary. | No contradictions remain after the S14 clarification. |
| Unsupported claims | Checked for performance comparisons, capability claims and fabricated statistics. | Passed. No claim that any capability exists. Performance targets are deferred to measurement. The connection-scale figure in NET-003 is labeled a design target. |

The automated checks were run with a local script against the working tree. They are not a CI check, following the [ENGINEERING.md](https://github.com/Cretes-lang/.github/blob/main/ENGINEERING.md) rule against placeholder checks.

## Scope review

| Check | Result |
| --- | --- |
| No compiler, lexer, parser, AST, IR, runtime, standard library or package-manager implementation started | Confirmed. The pull request contains Markdown documentation only. |
| No syntax frozen | Confirmed. No declaration, block, termination, generic, ownership, async, error-propagation, module or type-definition syntax is defined. The command names `cretes run`, `cretes build` and `cretes check` are toolchain interface requirements, not language syntax. The optional interpreter-directive line (AUTO-003) is MAY-level and explicitly deferred to Phase 2. |
| No memory model selected | Confirmed. Candidates are listed only in [P2Q-004](../PHASE-2-OPEN-QUESTIONS.md#p2q-004--memory-management-architecture). [SAFETY.md](../requirements/SAFETY.md) defines outcomes only. |
| No compiler backend selected | Confirmed. Candidates are listed only in [PERFORMANCE.md](../requirements/PERFORMANCE.md) and [P2Q-010](../PHASE-2-OPEN-QUESTIONS.md#p2q-010--execution-model-and-backend). |
| No concurrency implementation selected | Confirmed. See [P2Q-011](../PHASE-2-OPEN-QUESTIONS.md#p2q-011--concurrency-runtime-architecture). |
| v0.1 does not require the full domain ecosystems | Confirmed. See the [exclusions](../requirements/V0.1-REQUIREMENTS.md#what-v01-deliberately-excludes). |
| Scope creep in domains | Ecosystem-level items, such as web frameworks, gRPC, training frameworks, dataframes and security products, are assigned to the Ecosystem layer or listed as [non-goals](../requirements/NON-GOALS.md). Protocol and algorithm names identify interoperability needs, not delivery promises (NG-21). |
| GPU and accelerators | Labeled future architecture. No vendor-specific concept is required at language level ([AI-019](../requirements/domains/ai-ml.md#ai-019--accelerator-ready-architecture-future-architecture) to [AI-021](../requirements/domains/ai-ml.md#ai-021--heterogeneous-compute-future-architecture)). |
| Platform support claims | None. All platforms are candidates ([PLATFORMS.md](../requirements/PLATFORMS.md)). |

## Completion checklist

- [x] 1.1 Language mission
- [x] 1.2 Target developers
- [x] 1.3 Core use cases
- [x] 1.4 Design principles
- [x] 1.5 Automation requirements
- [x] 1.6 Networking requirements
- [x] 1.7 AI/ML requirements
- [x] 1.8 Cybersecurity requirements
- [x] 1.9 Safety requirements
- [x] 1.10 Performance requirements
- [x] 1.11 Concurrency requirements
- [x] 1.12 Interoperability requirements
- [x] 1.13 Platform requirements
- [x] 1.14 Non-goals
- [x] 1.15 v0.1 requirements
- [x] CORE requirements completed
- [x] Requirement IDs reviewed
- [x] MUST/SHOULD/MAY terminology documented
- [x] Cross-document links checked
- [x] README documentation index updated
- [x] Security review completed (self-review; independent review recommended)
- [x] Scope review completed
- [x] Contradictions reviewed
- [x] Phase 2 questions recorded
- [x] No compiler implementation started
- [x] No syntax prematurely frozen
- [x] No memory model prematurely selected
- [x] No compiler backend prematurely selected
- [x] Final GitHub diff reviewed (recorded in the pull request)

## Follow-up items outside this repository

- The `.github` repository records Phase 1 acceptance in `PHASE_1.md`, mirroring `PHASE_0.md`.
- The Phase 0 open dependencies recorded in `PHASE_0.md` remain the responsibility of the maintainer and are not changed by Phase 1. These are CODEOWNERS restoration, organization 2FA enforcement, publication of the profile email and domain verification.
