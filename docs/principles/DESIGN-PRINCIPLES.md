# Cretes design principles

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

These principles guide every future Cretes design decision: language features, runtime architecture, standard-library APIs, tooling and ecosystem policy. They are the criteria that RFCs are evaluated against. They do **not** define syntax, and they do not select a memory model, type system or backend.

Each principle states its **rationale**, its **consequences**, the **trade-offs** it accepts, and **examples of future decisions** it should influence. Representative requirements that put the principle into effect are linked.

## Contents

1. [Safety by default](#1-safety-by-default)
2. [Predictable performance](#2-predictable-performance)
3. [Simple common cases](#3-simple-common-cases)
4. [Explicit low-level operations](#4-explicit-low-level-operations)
5. [Concurrency as a foundational capability](#5-concurrency-as-a-foundational-capability)
6. [Excellent diagnostics](#6-excellent-diagnostics)
7. [Interoperability over isolation](#7-interoperability-over-isolation)
8. [Cross-platform design](#8-cross-platform-design)
9. [Secure ecosystem](#9-secure-ecosystem)
10. [Consistency over excessive syntax](#10-consistency-over-excessive-syntax)
11. [Readability](#11-readability)
12. [Tooling is part of the language experience](#12-tooling-is-part-of-the-language-experience)
13. [Stability must be earned](#13-stability-must-be-earned)
14. [Zero-cost or low-cost abstractions where practical](#14-zero-cost-or-low-cost-abstractions-where-practical)
15. [Clear escape hatches for expert low-level development](#15-clear-escape-hatches-for-expert-low-level-development)

[Resolving conflicts between principles](#resolving-conflicts-between-principles) · [Using the principles in RFCs](#using-the-principles-in-rfcs)

---

## 1. Safety by default

**Statement.** The default way to write Cretes code must be safe: free of undefined behavior, memory corruption, data races and silently ignored errors. Unsafe capabilities exist, but they must be requested explicitly.

- **Rationale:** Most severe vulnerabilities and many production incidents come from a small set of bug classes that a language can rule out. Defaults determine what most code does, because most developers never change them.
- **Consequences:**
  - Bounds checks, initialization checks, null handling and overflow semantics are part of the language.
  - Standard-library APIs choose the safe behavior by default: argument vectors, not shells; verified, not unverified, TLS.
  - Unsafe operations are marked and auditable.
- **Trade-offs:** Some run-time checks cost performance. Some safe patterns are more verbose than their unsafe equivalents. Some programs are harder to express. Cretes accepts these costs and mitigates them through optimization ([Principle 14](#14-zero-cost-or-low-cost-abstractions-where-practical)) and escape hatches ([Principle 15](#15-clear-escape-hatches-for-expert-low-level-development)).
- **Future decisions influenced:**
  - Selection of the memory-management model ([P2Q-004](../PHASE-2-OPEN-QUESTIONS.md#p2q-004--memory-management-architecture)).
  - The default integer-overflow behavior.
  - The design of process-creation and TLS APIs.
  - Whether unsafe code may be disallowed per package.
- **Representative requirements:** [SAFE-001](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code), [SAFE-006](../requirements/SAFETY.md#safe-006--null-safety), [CORE-022](../requirements/CORE.md#core-022--explicit-recoverable-errors), [AUTO-010](../requirements/domains/automation.md#auto-010--explicit-shell-invocation), [NET-023](../requirements/domains/networking.md#net-023--secure-network-defaults)

## 2. Predictable performance

**Statement.** A competent Cretes developer should be able to anticipate the cost of their code, and performance should not vary surprisingly between runs, inputs or releases.

- **Rationale:** Network services need stable latency. CLI tools need fast startup. Numerical code needs steady throughput. Predictability matters more than peak benchmark numbers.
- **Consequences:** A documented cost model. Operations that are expensive or that block are visible in source or documentation. Memory management with bounded, documented pauses. Performance is tracked by benchmarks.
- **Trade-offs:** Some convenient abstractions that hide costs, such as implicit copying, invisible allocation and implicit dynamic dispatch, are avoided or made explicit. This may add verbosity.
- **Future decisions influenced:**
  - Memory-management evaluation ([SAFE-023](../requirements/SAFETY.md#safe-023--memory-management-evaluation-criteria)).
  - Whether value copies are implicit.
  - Collection API design.
  - Concurrency runtime design.
- **Representative requirements:** [PERF-002](../requirements/PERFORMANCE.md#perf-002--documented-cost-model), [PERF-003](../requirements/PERFORMANCE.md#perf-003--visible-expensive-operations), [PERF-010](../requirements/PERFORMANCE.md#perf-010--memory-footprint-and-control), [PERF-017](../requirements/PERFORMANCE.md#perf-017--evidence-before-claims)

## 3. Simple common cases

**Statement.** Common tasks should be simple to express, and learning Cretes should start small. Complexity should appear only when a problem needs it.

- **Rationale:** Automation engineers and application developers need to be productive quickly. A language that requires mastering advanced concepts before writing a useful script will not be adopted in those domains.
- **Consequences:**
  - Single-file programs run directly.
  - Type annotations can be omitted where they are unambiguous.
  - Error propagation is concise.
  - The standard library covers everyday needs without third-party packages.
- **Trade-offs:** Simplicity for common cases can conflict with explicitness ([Principle 4](#4-explicit-low-level-operations)) and with performance control. Where they conflict, the simple path must still be safe. Additional control is opt-in.
- **Future decisions influenced:**
  - Type-inference scope ([P2Q-002](../PHASE-2-OPEN-QUESTIONS.md#p2q-002--type-inference-scope)).
  - The error-propagation mechanism.
  - The breadth of the standard library.
  - Project scaffolding requirements.
- **Representative requirements:** [AUTO-001](../requirements/domains/automation.md#auto-001--single-file-programs), [AUTO-002](../requirements/domains/automation.md#auto-002--error-context-for-operational-failures), [CORE-020](../requirements/CORE.md#core-020--reduced-annotation-burden)

## 4. Explicit low-level operations

**Statement.** Operations that bypass safety checks, reinterpret memory, cross into foreign code, or have significant hidden cost must be explicit in source.

- **Rationale:** Readers and reviewers must be able to find where guarantees end and where costs arise. Implicit low-level behavior makes code review and security audit impractical.
- **Consequences:**
  - Unsafe regions are marked and tool-enumerable.
  - Foreign declarations are distinct.
  - Lossy conversions are explicit.
  - Blocking operations are identifiable.
- **Trade-offs:** More ceremony for low-level code. Cretes accepts this because low-level code is a minority of most programs and deserves extra scrutiny.
- **Future decisions influenced:**
  - Unsafe-region design.
  - FFI declaration forms.
  - Conversion rules.
  - Layout-control attributes.
- **Representative requirements:** [SAFE-016](../requirements/SAFETY.md#safe-016--explicit-and-auditable-unsafe-code), [CORE-021](../requirements/CORE.md#core-021--no-implicit-lossy-conversions), [INTOP-006](../requirements/INTEROPERABILITY.md#intop-006--safe-wrappers)

## 5. Concurrency as a foundational capability

**Statement.** Concurrency is designed into the language, runtime and standard library from the start. It is not added later as a library.

- **Rationale:** All four domains are concurrent by nature. Retrofitting concurrency tends to produce split ecosystems, unsafe shared state and inconsistent cancellation.
- **Consequences:**
  - Structured concurrency, cancellation, deadlines and backpressure are standard.
  - Data-race freedom is a safety requirement.
  - Standard-library APIs are designed for concurrent use.
  - v0.1 architecture must leave room for concurrency, even though v0.1 does not ship it.
- **Trade-offs:** Concurrency safety constrains the memory and type systems. Designing concurrency early delays some features and adds up-front design work.
- **Future decisions influenced:**
  - Concurrency runtime architecture ([P2Q-011](../PHASE-2-OPEN-QUESTIONS.md#p2q-011--concurrency-runtime-architecture)).
  - How the async model affects API design ([P2Q-012](../PHASE-2-OPEN-QUESTIONS.md#p2q-012--asynchronous-execution-model-and-api-coloring)).
  - How sharing is checked.
- **Representative requirements:** [CONC-004](../requirements/CONCURRENCY.md#conc-004--structured-concurrency), [CONC-006](../requirements/CONCURRENCY.md#conc-006--cancellation), [SAFE-012](../requirements/SAFETY.md#safe-012--data-race-freedom), [CONC-019](../requirements/CONCURRENCY.md#conc-019--unified-concurrency-model)

## 6. Excellent diagnostics

**Statement.** Every diagnostic should explain what is wrong, where, and — when it can be reliably determined — how to fix it.

- **Rationale:** Diagnostics are the language's primary teaching interface. Good diagnostics reduce learning cost, support cost and frustration more than almost any feature.
- **Consequences:**
  - Precise spans, stable codes, suggestions and machine-readable output.
  - Error recovery that reports several problems in one run.
  - Diagnostic quality is tested like any other feature.
  - Language designs are evaluated for their diagnostic impact.
- **Trade-offs:** Some expressive features make good diagnostics very hard, such as unrestricted overloading or complex inference. Cretes may reject such features, or limit them, for diagnostic reasons.
- **Future decisions influenced:**
  - Inference scope.
  - The design of generics and overloading.
  - The macro or metaprogramming facilities, if any.
  - Compiler architecture that preserves source spans.
- **Representative requirements:** [DX-005](../requirements/CORE.md#dx-005--diagnostic-content), [DX-006](../requirements/CORE.md#dx-006--machine-readable-diagnostics), [DX-007](../requirements/CORE.md#dx-007--error-recovery)

## 7. Interoperability over isolation

**Statement.** Cretes should work with the existing software world rather than requiring it to be rewritten.

- **Rationale:** Operating systems, cryptographic libraries, AI runtimes and decades of native code cannot be replaced, and should not be. Adoption depends on incremental integration.
- **Consequences:**
  - The C ABI is the initial interoperability target in both directions.
  - Data layouts are compatible with C and with established tensor formats.
  - Ownership across boundaries is explicit.
  - Integration with Python, WebAssembly and other ecosystems is planned in stages.
- **Trade-offs:** Interop constrains memory management, for example through pinning and ownership transfer, and ABI decisions. FFI is also where safety ends, so it demands careful boundary design.
- **Future decisions influenced:**
  - FFI architecture ([P2Q-013](../PHASE-2-OPEN-QUESTIONS.md#p2q-013--ffi-architecture)).
  - How memory management is evaluated for pinning.
  - The design of the tensor layout descriptor.
- **Representative requirements:** [INTOP-001](../requirements/INTEROPERABILITY.md#intop-001--calling-c-abi-functions), [INTOP-005](../requirements/INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary), [AI-008](../requirements/domains/ai-ml.md#ai-008--tensor-compatible-layout-descriptors)

## 8. Cross-platform design

**Statement.** Cretes programs should behave identically across supported platforms, except where differences are explicitly specified.

- **Rationale:** Automation, DevOps and security tools run on Linux, Windows and macOS. Platform surprises cost more than slightly less idiomatic abstractions.
- **Consequences:**
  - Fixed-width primitives.
  - Platform-independent evaluation rules.
  - Path and process abstractions that handle platform differences.
  - Platform-specific APIs are separated and marked.
  - Platform support is claimed only when tested in CI.
- **Trade-offs:** The portable interface cannot expose every platform feature directly. Some platform-specific behavior must be reached through explicit extensions.
- **Future decisions influenced:**
  - Standard-library design.
  - The conditional-compilation model.
  - The CI matrix.
  - Promotion of platforms between tiers.
- **Representative requirements:** [CORE-026](../requirements/CORE.md#core-026--platform-independent-semantics), [PLAT-005](../requirements/PLATFORMS.md#plat-005--criteria-for-official-support), [PLAT-007](../requirements/PLATFORMS.md#plat-007--explicit-platform-specific-code)

## 9. Secure ecosystem

**Statement.** Security extends beyond the language to the toolchain, packages, registry and release process.

- **Rationale:** A memory-safe language with an insecure supply chain is not secure. Attackers increasingly target build systems and package registries.
- **Consequences:**
  - Lock files with hashes.
  - No code execution at install time.
  - Package provenance.
  - Advisories and auditing.
  - Reproducible builds and signed releases.
  - Audited cryptography with misuse-resistant APIs.
- **Trade-offs:** Security policy adds friction for publishers and build-script authors, and it costs maintainer effort. Cretes accepts this friction for widely used packages.
- **Future decisions influenced:**
  - Package manager and registry architecture ([P2Q-016](../PHASE-2-OPEN-QUESTIONS.md#p2q-016--package-and-build-architecture)).
  - The build-script model.
  - The cryptography implementation strategy.
- **Representative requirements:** [SEC-023](../requirements/domains/cybersecurity.md#sec-023--dependency-integrity), [SEC-025](../requirements/domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation), [SEC-027](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds), [SEC-014](../requirements/domains/cybersecurity.md#sec-014--misuse-resistant-api-layering)

## 10. Consistency over excessive syntax

**Statement.** Prefer a small set of general, consistent mechanisms to many special-case constructs.

- **Rationale:** Each additional construct increases learning cost, tooling cost and the number of interactions that must be specified and tested. Consistency makes code predictable to read and tools simpler to build.
- **Consequences:**
  - New syntax needs strong justification in an RFC.
  - Library solutions are preferred to language features when they are adequate.
  - Similar concepts look similar.
- **Trade-offs:** Some domain-specific conveniences are rejected or delayed. General mechanisms can sometimes be less concise than special cases.
- **Future decisions influenced:**
  - Whether a capability belongs in the language or the library.
  - Operator overloading.
  - The number of declaration forms.
  - Macro facilities.
- **Representative requirements:** [AI-004](../requirements/domains/ai-ml.md#ai-004--readable-numerical-notation), and the [layer model](../requirements/README.md#layers) used throughout the requirements.

## 11. Readability

**Statement.** Code is read far more often than it is written. Cretes optimizes for the reader.

- **Rationale:** Automation scripts, network services and security tools are maintained for years by people other than their authors. Security review depends on readable code.
- **Consequences:**
  - Explicit intent where it matters: mutability, fallibility, unsafe code and blocking.
  - A canonical formatter.
  - No semantics that depend on invisible characters.
  - Names and APIs that describe behavior.
- **Trade-offs:** Readability can mean more words. Terseness is not a goal in itself.
- **Future decisions influenced:**
  - Keyword and punctuation choices in later syntax phases.
  - Visibility of error propagation.
  - Formatter style.
  - Standard-library naming conventions.
- **Representative requirements:** [CORE-005](../requirements/CORE.md#core-005--protection-against-deceptive-source-text), [CORE-011](../requirements/CORE.md#core-011--mutable-and-immutable-bindings), [DX-009](../requirements/CORE.md#dx-009--canonical-formatter)

## 12. Tooling is part of the language experience

**Statement.** The compiler, formatter, test runner, package manager, language server, documentation generator and debugger integration are designed as part of Cretes. They are not left entirely to third parties.

- **Rationale:** Developers experience a language through its tools. Consistent official tooling prevents fragmentation and lowers the barrier to entry.
- **Consequences:**
  - A single `cretes` command.
  - Language designs are evaluated for their impact on tooling, for example name resolution without execution.
  - Tools share compiler analysis.
- **Trade-offs:** Tooling takes significant maintainer effort. Some features may be delayed until the tools can support them well.
- **Future decisions influenced:**
  - Compiler architecture for incremental and IDE use.
  - The manifest format.
  - The diagnostic format.
- **Representative requirements:** [DX-001](../requirements/CORE.md#dx-001--single-toolchain-entry-point), [DX-011](../requirements/CORE.md#dx-011--integrated-test-runner), [DX-012](../requirements/CORE.md#dx-012--language-server), [CORE-009](../requirements/CORE.md#core-009--name-resolution-without-execution)

## 13. Stability must be earned

**Statement.** Cretes makes compatibility promises only after designs have been implemented, used and reviewed. Once made, promises are kept.

- **Rationale:** Premature stability freezes mistakes. Broken promises destroy trust. [VERSIONING.md](https://github.com/Cretes-lang/.github/blob/main/VERSIONING.md) already allows breaking changes during `0.x`.
- **Consequences:**
  - Features are marked experimental until proven.
  - An edition or version mechanism exists before 1.0.
  - The native ABI stays unstable until a decision is made.
  - A stability review precedes 1.0.
- **Trade-offs:** Early adopters face breaking changes. Cretes mitigates this with migration guidance and, where feasible, automated migration tooling.
- **Future decisions influenced:**
  - Feature-stability labeling.
  - The edition mechanism.
  - ABI policy.
  - Deprecation process.
- **Representative requirements:** [CORE-030](../requirements/CORE.md#core-030--language-evolution-mechanism), [CORE-031](../requirements/CORE.md#core-031--specification-coverage-of-shipped-features), [INTOP-018](../requirements/INTEROPERABILITY.md#intop-018--abi-stability-policy)

## 14. Zero-cost or low-cost abstractions where practical

**Statement.** Abstractions should not impose run-time costs beyond what an equivalent hand-written implementation would incur, where this is technically practical. Where an abstraction has inherent cost, the cost should be low and documented.

- **Rationale:** Developers should not have to choose between clean code and efficient code in performance-sensitive domains such as networking, numerical work and parsing.
- **Consequences:**
  - Semantics that permit inlining, unboxed values and elimination of redundant checks.
  - Generic code that can be specialized.
  - Iteration that compiles to efficient loops.
- **Trade-offs:** Zero-cost abstractions can increase compile time and binary size, which conflicts with [PERF-005](../requirements/PERFORMANCE.md#perf-005--toolchain-responsiveness) and [PERF-012](../requirements/PERFORMANCE.md#perf-012--artifact-size). "Where practical" means these trade-offs are weighed explicitly in RFCs. They do not always resolve in favor of run-time speed.
- **Future decisions influenced:**
  - Generics implementation strategy (specialization versus shared code).
  - Compiler backend selection.
  - Iterator design.
- **Representative requirements:** [PERF-009](../requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput), [PERF-011](../requirements/PERFORMANCE.md#perf-011--allocation-free-values), [AI-003](../requirements/domains/ai-ml.md#ai-003--packed-value-layout)

## 15. Clear escape hatches for expert low-level development

**Statement.** Experts must be able to step outside the safe subset when there is a real need: implementing data structures, binding foreign libraries, optimizing hot paths or reaching platform features. Such steps must be clearly marked and contained.

- **Rationale:** A language without escape hatches forces experts to leave it, into C for example. The unsafe code still exists, only outside Cretes' tooling and review. Controlled escape hatches keep that code auditable.
- **Consequences:**
  - Scoped unsafe regions with documented obligations.
  - Safe wrappers.
  - Package-level unsafe policies.
  - Audit tooling.
  - Checked build profiles for unsafe code.
- **Trade-offs:** Escape hatches can be overused. Cretes counters this with tooling, lints and ecosystem norms, not by removing the capability.
- **Future decisions influenced:**
  - Unsafe-region design.
  - The specification of proof obligations.
  - The design of the audit report.
- **Representative requirements:** [SAFE-016](../requirements/SAFETY.md#safe-016--explicit-and-auditable-unsafe-code), [SAFE-017](../requirements/SAFETY.md#safe-017--safe-abstractions-over-unsafe-code), [SAFE-019](../requirements/SAFETY.md#safe-019--package-level-unsafe-policy), [SEC-029](../requirements/domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting)

---

## Resolving conflicts between principles

Principles will conflict. When they do, RFC authors should weigh them with the following guidance. It is a default order, not an absolute ranking:

1. **Safety and security** (Principles 1, 9) take precedence over convenience and performance. A design that weakens safety must provide an explicit, contained escape hatch (Principle 15) rather than an unsafe default.
2. **Correctness and predictability** (Principles 2, 8) take precedence over peak performance (Principle 14).
3. **Readability and consistency** (Principles 10, 11) take precedence over brevity (Principle 3), except where brevity is essential to make the common case practical.
4. **Stability** (Principle 13) is weighed against every other principle when an existing promise is involved.

Any decision that departs from this order must explain why in its RFC.

## Using the principles in RFCs

RFCs submitted to [`Cretes-lang/rfcs`](https://github.com/Cretes-lang/rfcs) that affect language design, runtime architecture or public APIs should:

- name the principles that the proposal advances and those it trades against;
- cite the requirement IDs the proposal satisfies, or proposes to change;
- explain how the proposal affects diagnostics and tooling (Principles 6 and 12);
- identify safety and security consequences, as the RFC template already requires.

Changing a principle requires an RFC.

## Related documents

- [Vision](../vision/VISION.md)
- [Requirements framework](../requirements/README.md)
- [Phase 2 open questions](../PHASE-2-OPEN-QUESTIONS.md)
