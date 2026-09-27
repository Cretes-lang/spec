# Cretes language specification

This repository is the designated home for the future normative Cretes specification and for the requirements that constrain it. **No language semantics, grammar or syntax have been approved or implemented.**

| Phase | Status | Output in this repository |
| --- | --- | --- |
| Phase 0 — Project foundation and governance | Complete | Repository scaffold and change-control policy (below) |
| Phase 1 — Language vision, requirements and design principles | Baseline published | [`docs/`](docs/) — vision, principles, requirements, v0.1 scope, Phase 2 questions |
| Phase 2 — Architecture | Not started | Decisions through [RFCs](https://github.com/Cretes-lang/rfcs), answering the [open questions](docs/PHASE-2-OPEN-QUESTIONS.md) |

Phase 1 defines **what** Cretes must accomplish. Phase 2 and later phases decide **how**. The Phase 1 documents are requirements. They are not normative language rules and do not define syntax.

## Phase 1 documentation

### Where to start

Read in this order:

1. [Vision](docs/vision/VISION.md) — what Cretes is, why it exists, the long-term ecosystem.
2. [Target developers](docs/vision/TARGET-USERS.md) — the six personas Cretes is designed for.
3. [Design principles](docs/principles/DESIGN-PRINCIPLES.md) — the fifteen principles that guide every decision.
4. [Requirements framework](docs/requirements/README.md) — MUST/SHOULD/MAY terminology, requirement IDs, layers, targets, traceability.
5. [Use cases](docs/requirements/USE-CASES.md) — concrete scenarios traced to requirements.
6. The domain and cross-cutting requirements (tables below).
7. [v0.1 requirements](docs/requirements/V0.1-REQUIREMENTS.md) — the first language milestone.
8. [Phase 2 open questions](docs/PHASE-2-OPEN-QUESTIONS.md) — architecture decisions deliberately left open.

### Index

| § | Topic | Document | IDs |
| --- | --- | --- | --- |
| 1.1 | Language mission | [docs/vision/VISION.md](docs/vision/VISION.md) | — |
| 1.2 | Target developers | [docs/vision/TARGET-USERS.md](docs/vision/TARGET-USERS.md) | — |
| 1.3 | Core use cases | [docs/requirements/USE-CASES.md](docs/requirements/USE-CASES.md) | `UC-*` |
| 1.4 | Design principles | [docs/principles/DESIGN-PRINCIPLES.md](docs/principles/DESIGN-PRINCIPLES.md) | — |
| 1.5 | Automation | [docs/requirements/domains/automation.md](docs/requirements/domains/automation.md) | `AUTO` |
| 1.6 | Networking | [docs/requirements/domains/networking.md](docs/requirements/domains/networking.md) | `NET` |
| 1.7 | AI/ML Applications | [docs/requirements/domains/ai-ml.md](docs/requirements/domains/ai-ml.md) | `AI` |
| 1.8 | Cybersecurity | [docs/requirements/domains/cybersecurity.md](docs/requirements/domains/cybersecurity.md) | `SEC` |
| 1.9 | Safety | [docs/requirements/SAFETY.md](docs/requirements/SAFETY.md) | `SAFE` |
| 1.10 | Performance | [docs/requirements/PERFORMANCE.md](docs/requirements/PERFORMANCE.md) | `PERF` |
| 1.11 | Concurrency | [docs/requirements/CONCURRENCY.md](docs/requirements/CONCURRENCY.md) | `CONC` |
| 1.12 | Interoperability | [docs/requirements/INTEROPERABILITY.md](docs/requirements/INTEROPERABILITY.md) | `INTOP` |
| 1.13 | Platforms | [docs/requirements/PLATFORMS.md](docs/requirements/PLATFORMS.md) | `PLAT` |
| 1.14 | Scope and non-goals | [docs/requirements/NON-GOALS.md](docs/requirements/NON-GOALS.md) | `NG-*` |
| 1.15 | v0.1 requirements | [docs/requirements/V0.1-REQUIREMENTS.md](docs/requirements/V0.1-REQUIREMENTS.md) | — |
| — | Core language and developer experience | [docs/requirements/CORE.md](docs/requirements/CORE.md) | `CORE`, `DX` |
| — | Requirements framework and register | [docs/requirements/README.md](docs/requirements/README.md) | — |
| — | Phase 2 open questions | [docs/PHASE-2-OPEN-QUESTIONS.md](docs/PHASE-2-OPEN-QUESTIONS.md) | `P2Q-*` |
| — | Phase 1 security, consistency and scope review | [docs/reviews/PHASE-1-REVIEW.md](docs/reviews/PHASE-1-REVIEW.md) | — |

### Layout

```text
docs/
├── vision/            VISION.md, TARGET-USERS.md
├── principles/        DESIGN-PRINCIPLES.md
├── requirements/      README.md (framework), USE-CASES.md, CORE.md, SAFETY.md,
│   │                  PERFORMANCE.md, CONCURRENCY.md, INTEROPERABILITY.md,
│   │                  PLATFORMS.md, NON-GOALS.md, V0.1-REQUIREMENTS.md
│   └── domains/       automation.md, networking.md, ai-ml.md, cybersecurity.md
├── reviews/           PHASE-1-REVIEW.md
└── PHASE-2-OPEN-QUESTIONS.md
```

## Planned reference structure

Future normative chapters will cover the areas below. They will be kept separate from the Phase 1 requirements in `docs/`, and their location will be decided when the first chapter is approved.

| Area | Future document scope |
| --- | --- |
| Lexical structure and grammar | Source encoding, tokens and formal grammar |
| Types and semantics | Values, conversions, inference and semantic constraints |
| Expressions and control flow | Evaluation, branching, loops and functions |
| Modules | Imports, visibility and module identity |
| Errors and resources | Failure behavior, memory and resource lifetime |
| Concurrency | Execution and synchronization rules |
| Standard library | Required behavior of standard interfaces |
| Conformance | Requirements and positive/negative test mappings |

These headings do not select any design. Chapters are added after approved proposals. Each chapter should cite the requirement IDs it satisfies.

## Authority and change control

An accepted RFC records a design decision. A reviewed specification change defines normative behavior. Tutorials and examples are explanatory. A compiler discrepancy is not automatically a change to the language. Resolve it in an issue with the specification reference and test evidence.

Each future chapter should declare:

- status and scope;
- terminology;
- normative rules and their rationale;
- examples, marked as normative or illustrative;
- links to accepted RFCs and conformance tests.

Drafts must remain visibly marked. Version the specification and associate it with toolchain releases before making stability claims.

Phase 1 requirements change through issues and reviewed pull requests. Adding, weakening or removing a MUST requirement requires an RFC. See [Changing requirements](docs/requirements/README.md#changing-requirements).

## Project policies

- [Contributing](https://github.com/Cretes-lang/.github/blob/main/CONTRIBUTING.md)
- [Governance](https://github.com/Cretes-lang/.github/blob/main/GOVERNANCE.md)
- [Code of Conduct](https://github.com/Cretes-lang/.github/blob/main/CODE_OF_CONDUCT.md)
- [Security reporting](https://github.com/Cretes-lang/.github/blob/main/SECURITY.md)
- [Engineering standards](https://github.com/Cretes-lang/.github/blob/main/ENGINEERING.md)
- [Versioning](https://github.com/Cretes-lang/.github/blob/main/VERSIONING.md)

Initial maintainer: @krishanth7. License: [Apache-2.0](LICENSE).
