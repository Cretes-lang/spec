# Core language and developer-experience requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This document consolidates cross-cutting requirements. Every Cretes program depends on them, whichever domain it serves. It covers source representation, modules, declarations, expressions, functions, types, errors, determinism, the build model, foundational library facilities (`CORE`), and developer experience and tooling (`DX`).

Terminology, layers and targets are defined in the [requirements framework](README.md).

> **No syntax is defined here.** Requirements describe capabilities and outcomes. Keywords, punctuation, block structure, declaration forms and operator spellings are Phase 2+ decisions. See [PHASE-2-OPEN-QUESTIONS.md](../PHASE-2-OPEN-QUESTIONS.md).

## Contents

- [Source representation](#source-representation)
- [Modules and names](#modules-and-names)
- [Declarations and bindings](#declarations-and-bindings)
- [Expressions and control flow](#expressions-and-control-flow)
- [Functions](#functions)
- [Types](#types)
- [Error handling](#error-handling)
- [Determinism and portability of meaning](#determinism-and-portability-of-meaning)
- [Build model and evolution](#build-model-and-evolution)
- [Foundational standard library](#foundational-standard-library)
- [Developer experience and tooling](#developer-experience-and-tooling)

## Source representation

### CORE-001 — Source file extension

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** Cretes source files must use the `.cretes` file extension. The toolchain must recognize `.cretes` files as Cretes source.
- **Rationale:** Recorded in [IDENTITY.md](https://github.com/Cretes-lang/.github/blob/main/IDENTITY.md). Editors, build tools and repositories rely on a single, stable extension.
- **Verification:** Integration tests.

### CORE-002 — Source encoding

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Source text must be interpreted as Unicode encoded in UTF-8. Input that is not valid UTF-8 must be rejected with a diagnostic that identifies the location of the invalid bytes. A leading byte-order mark, if permitted, must not change program meaning.
- **Rationale:** A single encoding removes platform- and locale-dependent interpretation of source code.
- **Verification:** Conformance tests; Fuzzing.

### CORE-003 — Platform-independent line structure

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The meaning of a program must not depend on whether its line terminators are LF or CRLF.
- **Rationale:** Source is shared between Linux, macOS and Windows developers and checked out with differing line-ending conventions.
- **Verification:** Conformance tests.

### CORE-004 — Unicode identifiers policy

- **Priority:** SHOULD · **Layer:** Language · **Target:** Before 1.0
- **Requirement:** If identifiers may contain non-ASCII characters, the permitted characters and normalization rules should be defined by reference to a published Unicode standard, such as Unicode Standard Annex #31. They should also be stable across Unicode versions.
- **Rationale:** Supports developers who do not write in English, while keeping identifier comparison well defined.
- **Verification:** Specification review; Conformance tests.

### CORE-005 — Protection against deceptive source text

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** The toolchain must reject, or diagnose by default, source text where the displayed form can differ from the compiled meaning. This covers unpaired or unexpected bidirectional control characters and invisible formatting characters outside comments and string content. SHOULD: warn about confusable identifiers.
- **Rationale:** "Trojan Source" attacks (CVE-2021-42574) hide malicious logic from reviewers. Code review is a security control and must see what the compiler sees.
- **Verification:** Conformance tests; Diagnostic tests; Security review.

### CORE-006 — Text distinct from bytes

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language and standard library must distinguish text values, which are guaranteed valid Unicode, from arbitrary byte sequences. Conversion from bytes to text must be explicit and must report invalid input.
- **Rationale:** Networking, file formats, binary parsing and security code handle raw bytes. User-facing code handles text. Silently conflating them causes corruption and injection bugs.
- **Verification:** Conformance tests; Unit tests.

## Modules and names

### CORE-007 — Modules

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Code must be organizable into modules with explicitly declared dependencies on other modules. A module's identity must not depend on the absolute filesystem location of the build machine.
- **Rationale:** Programs larger than one file need structure. Location-independent identity is required for reproducible builds ([SEC-027](domains/cybersecurity.md#sec-027--reproducible-builds)).
- **Verification:** Conformance tests; Integration tests.

### CORE-008 — Visibility control

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** A module must be able to expose a public interface while keeping other declarations inaccessible to other modules.
- **Rationale:** Encapsulation allows libraries to evolve without breaking users and lets safe interfaces protect internal invariants ([SAFE-017](SAFETY.md#safe-017--safe-abstractions-over-unsafe-code)).
- **Verification:** Conformance tests.

### CORE-009 — Name resolution without execution

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The specification must define name resolution so that a tool can resolve every name reference in a well-formed program without executing any part of that program.
- **Rationale:** Required for reliable diagnostics, editor navigation, refactoring and security review ([DX-012](#dx-012--language-server)). Executing untrusted code to analyze it is unacceptable.
- **Verification:** Specification review; Conformance tests.

### CORE-010 — Controlled module initialization

- **Priority:** SHOULD · **Layer:** Language · **Target:** v0.1
- **Requirement:** Importing a module should not implicitly execute arbitrary side effects. If module-level initialization exists, its ordering must be specified and deterministic, and initialization failures must be reported.
- **Rationale:** Implicit import-time execution makes programs hard to reason about and is a supply-chain attack vector.
- **Verification:** Specification review; Conformance tests.

## Declarations and bindings

### CORE-011 — Mutable and immutable bindings

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language must allow a programmer to state whether a named binding can be reassigned or its value mutated. Violations must be diagnosed before execution. Which form is the default is a Phase 2 decision.
- **Rationale:** Explicit mutability aids reasoning, enables optimization and supports data-race freedom ([SAFE-012](SAFETY.md#safe-012--data-race-freedom)).
- **Verification:** Conformance tests; Diagnostic tests.

### CORE-012 — User-defined data types

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Programmers must be able to define aggregate types that group named fields. They must also be able to define types whose value is exactly one of a closed set of alternatives, each optionally carrying data. Tools must be able to check that code handling such a type covers every alternative.
- **Rationale:** Structured data modeling is essential in every domain. Closed alternatives are a foundation for safe absence handling ([SAFE-006](SAFETY.md#safe-006--null-safety)) and explicit errors ([CORE-022](#core-022--explicit-recoverable-errors)).
- **Verification:** Conformance tests.

## Expressions and control flow

### CORE-013 — Specified evaluation order

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The order of evaluation of operands, arguments and side effects must be fully specified. No well-formed program may have unspecified evaluation order.
- **Rationale:** Unspecified evaluation order is a source of portability bugs and undefined behavior in other languages. It conflicts with [SAFE-001](SAFETY.md#safe-001--no-undefined-behavior-in-safe-code).
- **Verification:** Specification review; Conformance tests.

### CORE-014 — Control flow

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language must provide:
  - conditional execution;
  - bounded and unbounded loops;
  - early exit from loops and functions;
  - selection among the alternatives of a closed type, with exhaustiveness checking.
- **Rationale:** Minimum control flow for general-purpose programming.
- **Verification:** Conformance tests.

## Functions

### CORE-015 — Functions

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language must support named functions with parameters and results, including recursion.
- **Rationale:** The fundamental unit of abstraction.
- **Verification:** Conformance tests.

### CORE-016 — Functions as values

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Functions, including functions that capture values from their defining scope, should be usable as values: passed as arguments, returned and stored.
- **Rationale:** Needed for callbacks, iteration, concurrency APIs ([CONC-001](CONCURRENCY.md#conc-001--concurrent-tasks)) and data-processing pipelines.
- **Verification:** Conformance tests.

## Types

### CORE-017 — Errors detected before execution

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The toolchain must detect before execution:
  - references to undefined names;
  - calls with the wrong number of arguments;
  - non-exhaustive handling of closed alternatives.

  It SHOULD also detect before execution value-type mismatches in operations and calls. The degree of static checking is decided in Phase 2 ([P2Q-001](../PHASE-2-OPEN-QUESTIONS.md#p2q-001--static-dynamic-or-gradual-typing)).
- **Rationale:** Early error detection underpins safety, tooling and large-codebase maintenance.
- **Verification:** Conformance tests; Diagnostic tests.

### CORE-018 — Primitive types with defined representation

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language must provide:
  - a boolean type;
  - signed and unsigned integer types of explicit widths, at least 8, 16, 32 and 64 bits;
  - IEEE 754 binary32 and binary64 floating-point types;
  - a Unicode scalar value type;
  - a text type ([CORE-006](#core-006--text-distinct-from-bytes)).

  The width and value range of each fixed-width type must be identical on every supported platform.
- **Rationale:** Networking, binary parsing, FFI and numerical work require exact representations.
- **Verification:** Conformance tests; Platform CI.

### CORE-019 — Parametric abstraction

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** The language must allow collections, algorithms and interfaces to be written once and used with many element types, while retaining the type checking of [CORE-017](#core-017--errors-detected-before-execution). v0.1 may provide built-in collections without exposing user-defined parametric types.
- **Rationale:** Reusable libraries in all four domains depend on generic containers and algorithms.
- **Verification:** Conformance tests; Design review.

### CORE-020 — Reduced annotation burden

- **Priority:** SHOULD · **Layer:** Language · **Target:** v0.1
- **Requirement:** Where the type of a local value can be determined unambiguously, the language should not require the programmer to state it. The inference model is a Phase 2 decision ([P2Q-002](../PHASE-2-OPEN-QUESTIONS.md#p2q-002--type-inference-scope)).
- **Rationale:** Keeps common automation and application code concise ([Principle 3](../principles/DESIGN-PRINCIPLES.md#3-simple-common-cases)).
- **Verification:** Conformance tests.

### CORE-021 — No implicit lossy conversions

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** A conversion that can lose information, change a numeric value, or change signedness must require explicit programmer intent.
- **Rationale:** Implicit narrowing conversions are a recurring source of security bugs in length and size calculations.
- **Verification:** Conformance tests; Diagnostic tests.

## Error handling

### CORE-022 — Explicit recoverable errors

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Whether an operation can fail with a recoverable error must be discoverable from its declared interface. A caller must not be able to ignore a recoverable error silently. Discarding an error must be a deliberate act that the source makes visible.
- **Rationale:** Automation scripts, network services and security code fail in production when errors are dropped unnoticed. The error-propagation mechanism is a Phase 2 decision ([P2Q-007](../PHASE-2-OPEN-QUESTIONS.md#p2q-007--error-model)).
- **Verification:** Conformance tests; Diagnostic tests.

### CORE-023 — Recoverable errors versus faults

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language must distinguish recoverable errors, which are expected failures such as a missing file, from unrecoverable faults, which are violated invariants or bugs. An unrecoverable fault must lead to defined behavior (see [SAFE-020](SAFETY.md#safe-020--defined-fault-behavior)), never to undefined behavior.
- **Rationale:** The two categories need different handling. Mixing them either hides bugs or makes routine failures fatal.
- **Verification:** Specification review; Conformance tests.

### CORE-024 — Structured error information

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Standard-library errors must expose a programmatically inspectable kind, a human-readable message, and, where applicable, an underlying cause. Programs must be able to attach context while propagating an error.
- **Rationale:** Callers must be able to branch on error kind without parsing messages. Operators need contextual chains to diagnose failures.
- **Verification:** Unit tests.

## Determinism and portability of meaning

### CORE-025 — Deterministic compilation

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** Given identical source, dependencies, toolchain version, target and configuration, the toolchain must produce identical diagnostics and semantically identical output. Compilation must not depend on timestamps, hash-map iteration order, absolute paths or environment state, except where explicitly configured. Bit-for-bit reproducibility is covered by [SEC-027](domains/cybersecurity.md#sec-027--reproducible-builds).
- **Rationale:** Non-determinism undermines testing, caching, CI and supply-chain verification.
- **Verification:** Integration tests (repeated and relocated builds compared).

### CORE-026 — Platform-independent semantics

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The meaning of a program that uses only portable language features and portable standard-library interfaces must be the same on every supported platform. The only exception is behavior that the specification explicitly defines as platform-dependent, such as pointer-sized integers or filesystem case sensitivity.
- **Rationale:** Portability ([Principle 8](../principles/DESIGN-PRINCIPLES.md#8-cross-platform-design)) requires that differences are enumerated rather than accidental.
- **Verification:** Conformance tests run under Platform CI.

### CORE-027 — Program entry and exit

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** An executable program must have a defined entry point. It must be able to access its command-line arguments and set its process exit status. An unhandled recoverable error or fault reaching the entry point must produce a non-zero exit status and a diagnostic on standard error.
- **Rationale:** Required for command-line tools and automation ([AUTO-019](domains/automation.md#auto-019--command-line-application-support)).
- **Verification:** Integration tests.

## Build model and evolution

### CORE-028 — Declarative package manifest

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** A multi-module Cretes project must be described by a manifest that declares its identity, its dependencies and its build targets. Tools must be able to determine a project's dependency graph without executing code from the project or its dependencies. The manifest format is a Phase 2+ decision.
- **Rationale:** Build tools, IDEs and security scanners need the graph. Code execution during resolution is a supply-chain risk ([SEC-025](domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation)).
- **Verification:** Integration tests; Security review.

### CORE-029 — Separate and incremental compilation

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The compilation model should allow unchanged modules and dependencies to be reused between builds, so that the work needed after a local change is proportionate to that change.
- **Rationale:** Build latency dominates developer experience in large projects ([PERF-007](PERFORMANCE.md#perf-007--incremental-builds)).
- **Verification:** Benchmark.

### CORE-030 — Language evolution mechanism

- **Priority:** MUST · **Layer:** Language · **Target:** Before 1.0
- **Requirement:** Before 1.0, the project must define how a package declares the language version or edition it targets. The mechanism must let the language evolve without silently changing the meaning of existing code.
- **Rationale:** Stability must be earned ([Principle 13](../principles/DESIGN-PRINCIPLES.md#13-stability-must-be-earned)). Once earned, it must be preserved without freezing the language.
- **Verification:** Design review.

### CORE-031 — Specification coverage of shipped features

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** Every language feature included in a release must be described in the specification, marked with its stability status and covered by positive and negative conformance tests.
- **Rationale:** Implements the documentation hierarchy in [ENGINEERING.md](https://github.com/Cretes-lang/.github/blob/main/ENGINEERING.md). The implementation must not become the de facto specification.
- **Verification:** Inspection at release review.

## Foundational standard library

### CORE-032 — Text operations

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** The standard library must provide text operations: construction, concatenation, length (with a documented unit), comparison, searching, slicing on valid boundaries, splitting, trimming, formatting of primitive values and parsing of numbers with error reporting.
- **Rationale:** Text handling is universal across automation, networking and application code.
- **Verification:** Unit tests.

### CORE-033 — Core collections

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** The standard library must provide:
  - a growable ordered sequence;
  - a key-value map;
  - a set.

  Each must have documented complexity for its principal operations and bounds-checked access ([SAFE-002](SAFETY.md#safe-002--spatial-memory-safety)).
- **Rationale:** Minimum collections for useful programs. Documented complexity supports predictable performance ([PERF-002](PERFORMANCE.md#perf-002--documented-cost-model)).
- **Verification:** Unit tests.

## Developer experience and tooling

### DX-001 — Single toolchain entry point

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** The toolchain must be invoked through a single `cretes` command with subcommands. Additional tools should be reachable through it.
- **Rationale:** One discoverable entry point lowers the barrier to entry ([Principle 12](../principles/DESIGN-PRINCIPLES.md#12-tooling-is-part-of-the-language-experience)).
- **Verification:** Integration tests.

### DX-002 — `cretes check`

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** `cretes check` must perform all analysis needed to report compile-time diagnostics for a file or project, without producing an executable artifact.
- **Rationale:** A fast analysis-only command supports editing loops, CI and pre-commit validation.
- **Verification:** Integration tests; Diagnostic tests.

### DX-003 — `cretes build`

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** `cretes build` must compile a file or project into an executable artifact that runs on the same platform without the Cretes source. The artifact's form, such as a native executable or another format, is decided in Phase 2 ([P2Q-010](../PHASE-2-OPEN-QUESTIONS.md#p2q-010--execution-model-and-backend)).
- **Rationale:** Distributable artifacts are needed for tools and services.
- **Verification:** Integration tests.

### DX-004 — `cretes run`

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** `cretes run` must build if necessary and then execute a file or project. It must forward program arguments, standard streams and exit status.
- **Rationale:** The shortest path from source to result, essential for automation and learning ([AUTO-001](domains/automation.md#auto-001--single-file-programs)).
- **Verification:** Integration tests.

### DX-005 — Diagnostic content

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** Every compile-time diagnostic must include:
  - a severity;
  - a stable diagnostic code;
  - the file and a precise source span (line and column);
  - a primary message stating what is wrong.

  Diagnostics SHOULD include an explanation and a suggested correction where one can be derived reliably.
- **Rationale:** Excellent diagnostics are a design principle ([Principle 6](../principles/DESIGN-PRINCIPLES.md#6-excellent-diagnostics)). Stable codes allow documentation and suppression policies.
- **Verification:** Diagnostic tests.

### DX-006 — Machine-readable diagnostics

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** The toolchain must be able to emit diagnostics in a documented, versioned, machine-readable format, in addition to human-readable output.
- **Rationale:** Editors, CI annotations and the language server consume diagnostics programmatically.
- **Verification:** Integration tests.

### DX-007 — Error recovery

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** The compiler should report multiple independent errors in one run and should avoid cascades of follow-on errors caused by a single mistake.
- **Rationale:** One-error-per-run workflows are slow. Cascades obscure the real problem.
- **Verification:** Diagnostic tests.

### DX-008 — Robustness on malformed input

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** For any input, the compiler must either succeed or report diagnostics and exit with a failure status. It must never crash, hang indefinitely or corrupt memory. An internal compiler error must be reported as such, distinctly from user errors.
- **Rationale:** Compilers process untrusted input, for example in CI and playgrounds. Crashes erode trust.
- **Verification:** Fuzzing; Integration tests.

### DX-009 — Canonical formatter

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain must include a formatter that produces a single canonical layout. It must preserve program meaning and be idempotent.
- **Rationale:** Removes style debates and makes diffs reviewable.
- **Verification:** Unit tests (idempotence and meaning preservation).

### DX-010 — Linter

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain should provide configurable lints for likely bugs, security hazards, such as confusable identifiers and discarded secrets, and maintainability issues.
- **Rationale:** Catches problems that are legal but probably wrong, without making them language errors.
- **Verification:** Diagnostic tests.

### DX-011 — Integrated test runner

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain must provide a test runner that discovers and executes tests, reports results in human- and machine-readable form, and supports filtering.
- **Rationale:** Testing should need no third-party setup ([Principle 12](../principles/DESIGN-PRINCIPLES.md#12-tooling-is-part-of-the-language-experience)).
- **Verification:** Integration tests.

### DX-012 — Language server

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The project should provide a Language Server Protocol implementation offering at least diagnostics, go-to-definition, find references, hover information and completion.
- **Rationale:** Editor integration across many editors through one standard protocol.
- **Verification:** Integration tests.

### DX-013 — Documentation generator

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain should generate browsable API documentation from source declarations and documentation comments.
- **Rationale:** Consistent library documentation across the ecosystem.
- **Verification:** Integration tests.

### DX-014 — Debugger support

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** Built artifacts must be able to carry debug information that allows established platform debuggers to set breakpoints by source line, step and inspect values on Tier 1 platforms. Tier 1 platforms are defined in [PLATFORMS.md](PLATFORMS.md).
- **Rationale:** Debuggability is essential for production systems and native interop. The debug-information strategy is [P2Q-015](../PHASE-2-OPEN-QUESTIONS.md#p2q-015--debug-information-strategy).
- **Verification:** Platform CI.

### DX-015 — Package manager and registry

- **Priority:** MUST · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** The project must provide a package manager integrated into the `cretes` command. It must resolve, fetch, verify and build dependencies, and it must be supported by a package registry. Supply-chain requirements [SEC-023](domains/cybersecurity.md#sec-023--dependency-integrity) to [SEC-026](domains/cybersecurity.md#sec-026--vulnerability-advisories-and-audit) apply.
- **Rationale:** An ecosystem is necessary for all four domains. A fragmented package story harms security.
- **Verification:** Integration tests; Security review.

### DX-016 — Online playground

- **Priority:** MAY · **Layer:** Ecosystem · **Target:** Long-term
- **Requirement:** The project may operate an online playground. If it does, untrusted programs must be executed in a sandbox with resource limits and no access to project infrastructure credentials.
- **Rationale:** Lowers the barrier to trying Cretes. It is a security-sensitive service.
- **Verification:** Security review.

### DX-017 — Consistent semantics across tools

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The compiler, formatter, linter, documentation generator and language server should share language analysis. This ensures they never disagree about whether a program is valid or what a name refers to.
- **Rationale:** Tools that disagree with the compiler destroy trust in the tooling.
- **Verification:** Design review.

### DX-018 — Release documentation

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** Each toolchain release must ship with installation instructions, a getting-started guide, reference documentation for the included language features and standard library, and a list of known limitations that matches actual behavior.
- **Rationale:** Required by [VERSIONING.md](https://github.com/Cretes-lang/.github/blob/main/VERSIONING.md). Documentation must not imply unimplemented features.
- **Verification:** Inspection at release review.

### DX-019 — Scriptable command-line behavior

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** `cretes` subcommands must use documented, distinct exit statuses for success, user-program errors (compile errors), and internal toolchain failures. Output intended for machines must be separable from human-oriented output.
- **Rationale:** The toolchain itself is used in automation and CI.
- **Verification:** Integration tests.

## Related documents

- [Requirements framework](README.md)
- [Safety requirements](SAFETY.md)
- [v0.1 requirements](V0.1-REQUIREMENTS.md)
- [Design principles](../principles/DESIGN-PRINCIPLES.md)
- [Phase 2 open questions](../PHASE-2-OPEN-QUESTIONS.md)
