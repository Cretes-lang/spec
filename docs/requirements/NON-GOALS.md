# Scope and non-goals

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This document states what Cretes is deliberately **not** trying to be. Its purpose is to prevent uncontrolled scope expansion in a young project with limited maintainer capacity.

## Building versus containing

Cretes is a general-purpose language. In time, Cretes **may be capable of building** software in almost any category. That is different from making such software part of the core language, its standard library or the project's deliverables.

A non-goal here means:

- the project will not build, bundle or maintain it as part of the Cretes language, standard library or official toolchain in the initial project scope;
- requirements, RFCs and pull requests that assume it should be declined, or deferred, with a reference to this document;
- the ecosystem is free to build it with Cretes.

Changing a non-goal into a goal requires an RFC ([requirements framework](README.md#changing-requirements)).

## Product non-goals

| ID | Cretes is not trying to become… | Clarification |
| --- | --- | --- |
| NG-01 | **An operating system** | Cretes needs excellent OS integration ([INTOP-010](INTEROPERABILITY.md#intop-010--operating-system-api-access)). Kernel development and bare-metal targets are not initial goals ([PLAT-004](PLATFORMS.md#plat-004--future-platform-candidates)). |
| NG-02 | **A database** | Drivers and embedded storage engines belong in the ecosystem. The standard library will not include a database engine. |
| NG-03 | **A browser** | No rendering engine or browser runtime. WebAssembly output is a long-term platform question, not a browser project. |
| NG-04 | **A complete AI framework** | Cretes targets AI/ML *applications* and interop with established frameworks and runtimes ([ai-ml.md](domains/ai-ml.md)). It does not aim to replace PyTorch, TensorFlow, JAX or their model ecosystems, or to ship a training framework. |
| NG-05 | **A game engine** | Graphics, audio, physics and asset pipelines are ecosystem concerns. |
| NG-06 | **A mobile UI framework** | Mobile platforms are not candidate targets ([PLATFORMS.md](PLATFORMS.md)). No UI toolkit, mobile or desktop, is part of the standard library. |
| NG-07 | **A penetration-testing distribution** | The Cybersecurity domain covers secure development and defensive engineering ([cybersecurity.md](domains/cybersecurity.md)). The project does not ship exploit collections, attack frameworks or offensive tool bundles. |
| NG-08 | **A web framework** | HTTP foundations are in scope ([networking.md](domains/networking.md)). Application frameworks, templating and ORMs belong in the ecosystem. |
| NG-09 | **A cloud platform or deployment service** | Automation and DevOps capabilities are libraries and tools. The project does not operate hosting, CI or deployment services for users. |

## Language-identity non-goals

Cretes learns from existing languages. It does not attempt to be a copy of any of them. No design is justified solely by "language X does it this way". Equally, no design is rejected solely because another language uses it. Each decision is evaluated against the [design principles](../principles/DESIGN-PRINCIPLES.md) and the requirements.

| ID | Cretes is not… | Meaning |
| --- | --- | --- |
| NG-10 | **A clone of Python** | Approachability for automation and AI/ML users is a goal. Source compatibility with Python, its object model or its dynamic semantics is not. |
| NG-11 | **A clone of Rust** | Memory safety without undefined behavior is a goal. Adopting Rust's specific ownership and borrowing model is not presumed. It is one candidate for Phase 2 ([P2Q-004](../PHASE-2-OPEN-QUESTIONS.md#p2q-004--memory-management-architecture)). |
| NG-12 | **A clone of Go** | Simple, first-class concurrency and fast builds are goals. Go's specific runtime design, and its choices on error handling and generics, are not presumed. |
| NG-13 | **A clone of Java** | Portability, tooling and a large ecosystem are goals. A mandatory virtual machine, class-centric design or JVM compatibility are not presumed. |
| NG-14 | **A superset or dialect of an existing language** | Cretes is not required to accept existing source code from another language. Interoperability happens at the ABI and data level ([INTEROPERABILITY.md](INTEROPERABILITY.md)), not through source compatibility. |

These statements do not disparage any language. Each of the languages named is successful because it serves its own goals well.

## Initial-scope non-goals

The following are out of scope **for the initial project**, through v0.1 and until an RFC changes that. They may become goals later.

| ID | Out of initial scope | Rationale |
| --- | --- | --- |
| NG-15 | 32-bit platforms | Focus on the 64-bit [Tier 1 candidates](PLATFORMS.md#candidate-platforms). |
| NG-16 | Mobile operating systems (iOS, Android) as targets | Requires platform toolchains and UI integration beyond initial capacity. |
| NG-17 | Embedded and bare-metal targets | Requires a freestanding library design. Recorded as a future candidate ([PLAT-004](PLATFORMS.md#plat-004--future-platform-candidates)). |
| NG-18 | Language-level GPU or accelerator programming | Future architecture only ([AI-019](domains/ai-ml.md#ai-019--accelerator-ready-architecture-future-architecture), [AI-021](domains/ai-ml.md#ai-021--heterogeneous-compute-future-architecture)). |
| NG-19 | Source compatibility guarantees during `0.x` | [VERSIONING.md](https://github.com/Cretes-lang/.github/blob/main/VERSIONING.md) allows breaking changes before 1.0. Stability must be earned ([Principle 13](../principles/DESIGN-PRINCIPLES.md#13-stability-must-be-earned)). |
| NG-20 | A stable Cretes-native ABI | The C ABI is the stable boundary ([INTOP-018](INTEROPERABILITY.md#intop-018--abi-stability-policy)). |
| NG-21 | Implementing every protocol, file format and algorithm named in the requirements | Requirements name interoperability needs. Delivery is prioritized per milestone, and much is left to the ecosystem. |
| NG-22 | Hot code reloading, live images and metaprogramming beyond Phase 2 needs | Not required by any domain use case. They can be proposed through RFCs with evidence. |

## Process non-goals for Phase 1

Phase 1 itself deliberately does not:

- define syntax or grammar;
- select a type system, memory-management model, error model, concurrency runtime or compiler backend;
- start compiler, runtime, standard-library, package-manager or tooling implementation;
- set numeric performance targets without measurements.

These are recorded as inputs to Phase 2 in [PHASE-2-OPEN-QUESTIONS.md](../PHASE-2-OPEN-QUESTIONS.md).

## Related documents

- [Vision](../vision/VISION.md)
- [v0.1 requirements](V0.1-REQUIREMENTS.md)
- [Design principles](../principles/DESIGN-PRINCIPLES.md)
