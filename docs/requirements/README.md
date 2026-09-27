# Cretes requirements framework

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This document explains how Cretes requirements are written, identified, prioritized and traced. Read it before the individual requirement documents.

Phase 1 defines **what** Cretes must accomplish. Phase 2 and later phases decide **how** it is accomplished. A requirement here does not describe existing functionality. No compiler, runtime, standard library or toolchain exists yet.

## Contents

- [Requirement terminology](#requirement-terminology)
- [Requirement identifiers](#requirement-identifiers)
- [Requirement record format](#requirement-record-format)
- [Layers](#layers)
- [Targets](#targets)
- [Verification approaches](#verification-approaches)
- [Requirement register](#requirement-register)
- [Changing requirements](#changing-requirements)

## Requirement terminology

Cretes uses the key words MUST, SHOULD and MAY in the spirit of [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174). They carry these meanings in the Cretes project **only when written in capitals**:

| Term | Meaning in Cretes |
| --- | --- |
| **MUST** | A fundamental requirement. The architecture and the implementation that ships the requirement's target milestone must satisfy it. You may only drop or weaken a MUST through a documented decision (see [Changing requirements](#changing-requirements)). |
| **MUST NOT** | An absolute prohibition, with the same weight as MUST. |
| **SHOULD** | Strongly desirable. It is expected to be satisfied unless a documented technical reason prevents it. The reason must be recorded in an RFC or in the relevant design record. |
| **SHOULD NOT** | Strongly undesirable, with the same weight as SHOULD. |
| **MAY** | Optional, or a future capability. Not required for any milestone. Recorded so that architecture does not accidentally rule it out. |
| **NON-GOAL** | Explicitly outside the current project scope. See [NON-GOALS.md](NON-GOALS.md). |

A requirement's priority applies to its **target milestone**. For example, a MUST requirement with target `Post-v0.1` is not required in v0.1. However, the v0.1 architecture must not make it impractical to satisfy later.

Lower-case "must", "should" and "may" in explanatory prose carry their ordinary English meaning.

## Requirement identifiers

Every requirement has a permanent identifier of the form `NAMESPACE-NNN`. Identifiers are never reused or renumbered. A withdrawn requirement keeps its identifier and is marked **Withdrawn** with a link to the decision.

| Namespace | Category | Document |
| --- | --- | --- |
| `CORE` | Cross-cutting language and foundational library requirements | [CORE.md](CORE.md) |
| `DX` | Developer experience, diagnostics and tooling | [CORE.md](CORE.md#developer-experience-and-tooling) |
| `AUTO` | Automation domain | [domains/automation.md](domains/automation.md) |
| `NET` | Networking domain | [domains/networking.md](domains/networking.md) |
| `AI` | AI/ML Applications domain | [domains/ai-ml.md](domains/ai-ml.md) |
| `SEC` | Cybersecurity domain | [domains/cybersecurity.md](domains/cybersecurity.md) |
| `SAFE` | Safety outcomes | [SAFETY.md](SAFETY.md) |
| `PERF` | Performance | [PERFORMANCE.md](PERFORMANCE.md) |
| `CONC` | Concurrency | [CONCURRENCY.md](CONCURRENCY.md) |
| `INTOP` | Interoperability | [INTEROPERABILITY.md](INTEROPERABILITY.md) |
| `PLAT` | Platforms | [PLATFORMS.md](PLATFORMS.md) |

Three related identifier series are **not** requirements:

- `UC-<DOMAIN>-NN` identifies a use case in [USE-CASES.md](USE-CASES.md).
- `P2Q-NNN` identifies an open architecture question in [PHASE-2-OPEN-QUESTIONS.md](../PHASE-2-OPEN-QUESTIONS.md).
- `NG-NN` identifies a non-goal in [NON-GOALS.md](NON-GOALS.md).

## Requirement record format

Each requirement is written as a level-3 heading followed by a fixed set of fields:

```markdown
### NET-006 — TCP clients and servers

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide TCP client and server facilities ...
- **Rationale:** Why the requirement exists.
- **Verification:** How conformance will eventually be demonstrated.
```

| Field | Meaning |
| --- | --- |
| ID | Permanent identifier (see above). |
| Title | Short human-readable name. |
| Priority | MUST, SHOULD or MAY. |
| Category | Implied by the namespace and document. |
| Layer | Which part of the system is responsible (see [Layers](#layers)). |
| Target | Earliest milestone where the requirement applies (see [Targets](#targets)). |
| Requirement | The testable statement. |
| Rationale | Why the requirement exists and which need it serves. |
| Verification | How satisfaction will be demonstrated once an implementation exists. |

Requirements are written to be implementation-neutral. Where a requirement mentions an existing technology, such as a protocol, file format or operating-system facility, the reference identifies a compatibility need. It does not select an implementation strategy.

## Layers

Requirements are assigned to the layer that is responsible for satisfying them. This prevents every capability from being pushed into language syntax.

| Layer | Responsibility |
| --- | --- |
| **Language** | Semantics that the specification must define and every conforming implementation must provide: types, evaluation, modules, safety rules. |
| **Runtime** | Execution support that compiled programs rely on: scheduling, I/O readiness, memory reclamation, fault handling. Whether a separate runtime component exists at all is a Phase 2 question. |
| **Standard library** | Interfaces distributed with every conforming toolchain. |
| **First-party library** | Maintained by the Cretes project. Whether it ships inside the standard library or as a separately versioned official package is a Phase 2+ decision. |
| **Toolchain** | The `cretes` command and associated tools: compiler, formatter, test runner, language server. |
| **Ecosystem** | Packages, registry and third-party libraries. The project provides infrastructure and policy but not necessarily the functionality. |
| **Process** | Project governance, release and review obligations. |

## Targets

Targets describe **when** a requirement applies. They are milestones, not dates. [VERSIONING.md](https://github.com/Cretes-lang/.github/blob/main/VERSIONING.md) governs version numbers. No release date is implied.

| Target | Meaning |
| --- | --- |
| `v0.1` | Required for the first usable language milestone. See [V0.1-REQUIREMENTS.md](V0.1-REQUIREMENTS.md). |
| `Post-v0.1` | Required in a later capability milestone that is not yet scheduled. The v0.1 architecture must leave room for it. |
| `Before 1.0` | Must be satisfied before any 1.0 stability commitment. |
| `Long-term` | Intended direction with no milestone commitment. |
| `Exploratory` | Worth investigating. May be abandoned without an RFC. |

Every MUST requirement, whatever its target, is an **input to Phase 2 architecture**. Phase 2 designs must show that they can satisfy it, even when implementation is later.

## Verification approaches

| Approach | Meaning |
| --- | --- |
| Design review | Checked when the relevant architecture RFC is reviewed. |
| Specification review | Checked when the relevant specification chapter is reviewed. |
| Conformance tests | Positive and negative language tests tied to the specification. |
| Unit / integration tests | Tests of toolchain, runtime or library behavior. |
| Diagnostic tests | Tests that verify diagnostic content, location and codes. |
| Fuzzing | Coverage-guided or grammar-based testing with malformed input. |
| Benchmark | Reproducible measurement under the strategy in [PERFORMANCE.md](PERFORMANCE.md#benchmarking-strategy). |
| Platform CI | Automated checks running on the real target platform. |
| Security review | Focused review by someone with relevant security expertise. |
| Inspection | Manual review of documentation, policy or configuration. |

## Requirement register

| Namespace | Count | MUST | SHOULD | MAY |
| --- | ---: | ---: | ---: | ---: |
| CORE | 33 | 28 | 5 | 0 |
| DX | 19 | 13 | 5 | 1 |
| AUTO | 28 | 19 | 8 | 1 |
| NET | 26 | 17 | 8 | 1 |
| AI | 23 | 10 | 10 | 3 |
| SEC | 34 | 27 | 7 | 0 |
| SAFE | 23 | 19 | 4 | 0 |
| PERF | 18 | 5 | 13 | 0 |
| CONC | 20 | 14 | 6 | 0 |
| INTOP | 19 | 12 | 4 | 3 |
| PLAT | 14 | 9 | 4 | 1 |
| **Total** | **257** | **173** | **74** | **10** |

The register was produced by extracting every requirement heading from the documents listed above. Recount it whenever requirements are added or withdrawn.

## Traceability

The documents form a chain. Each link can be followed in both directions.

```text
VISION.md ─► TARGET-USERS.md ─► DESIGN-PRINCIPLES.md
                  │
                  ▼
            USE-CASES.md  (UC-* ─► requirement IDs)
                  │
      ┌───────────┼──────────────────────────┐
      ▼           ▼                          ▼
 domains/*.md   cross-cutting documents   CORE.md
 (AUTO, NET,    (SAFE, PERF, CONC,        (CORE, DX)
  AI, SEC)       INTOP, PLAT)
      └───────────┼──────────────────────────┘
                  ▼
        V0.1-REQUIREMENTS.md  ─►  PHASE-2-OPEN-QUESTIONS.md
```

- [USE-CASES.md](USE-CASES.md) maps each use case to the requirements it depends on.
- [DESIGN-PRINCIPLES.md](../principles/DESIGN-PRINCIPLES.md) lists representative requirements that implement each principle.
- [V0.1-REQUIREMENTS.md](V0.1-REQUIREMENTS.md) lists every requirement whose target is `v0.1`.
- [PHASE-2-OPEN-QUESTIONS.md](../PHASE-2-OPEN-QUESTIONS.md) lists the requirements each open question must satisfy.

Once implementation begins, specification chapters, conformance tests and release notes should cite requirement IDs. This lets coverage be measured instead of asserted.

## Changing requirements

1. Open an issue in this repository describing the change, affected IDs and motivation.
2. Editorial changes and new SHOULD/MAY requirements use an ordinary reviewed pull request.
3. Adding, weakening or removing a **MUST** requirement, or changing the four official domains, requires an RFC in [`Cretes-lang/rfcs`](https://github.com/Cretes-lang/rfcs). This follows [GOVERNANCE.md](https://github.com/Cretes-lang/.github/blob/main/GOVERNANCE.md).
4. Never renumber. Mark withdrawn requirements **Withdrawn** in place, with a link to the decision.
5. Update the [requirement register](#requirement-register), the [v0.1 list](V0.1-REQUIREMENTS.md) and [use-case mappings](USE-CASES.md) in the same pull request.
