# Phase 2 open questions

> **Status:** Phase 1 output · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This register records the architecture questions that Phase 1 identified but deliberately **did not answer**. It is the input to Phase 2 (architecture). Each question lists:

- the requirements any answer must satisfy;
- candidate approaches to evaluate. The lists are non-exhaustive and in no particular order; listing an approach is not a recommendation;
- the expected decision vehicle.

Phase 2 decisions that affect language semantics, runtime architecture, compatibility or public APIs are made through RFCs in [`Cretes-lang/rfcs`](https://github.com/Cretes-lang/rfcs), per [GOVERNANCE.md](https://github.com/Cretes-lang/.github/blob/main/GOVERNANCE.md). When an RFC resolves a question, record the RFC link here and mark the question **Resolved**. Do not delete it.

Identifiers use the form `P2Q-NNN` and are never reused.

## Summary

| ID | Question | Area | Status |
| --- | --- | --- | --- |
| [P2Q-001](#p2q-001--static-dynamic-or-gradual-typing) | Static, dynamic or gradual typing | Types | Open |
| [P2Q-002](#p2q-002--type-inference-scope) | Type inference scope | Types | Open |
| [P2Q-003](#p2q-003--generics-model) | Generics model | Types | Open |
| [P2Q-004](#p2q-004--memory-management-architecture) | Memory-management architecture | Memory | Open |
| [P2Q-005](#p2q-005--mutability-aliasing-and-ownership-model) | Mutability, aliasing and ownership model | Memory | Open |
| [P2Q-006](#p2q-006--value-and-reference-semantics) | Value and reference semantics | Memory | Open |
| [P2Q-007](#p2q-007--error-model) | Error model | Semantics | Open |
| [P2Q-008](#p2q-008--nullability-representation) | Nullability representation | Semantics | Open |
| [P2Q-009](#p2q-009--default-integer-overflow-behavior) | Default integer overflow behavior | Semantics | Open |
| [P2Q-010](#p2q-010--execution-model-and-backend) | Execution model and backend | Compiler | Open |
| [P2Q-011](#p2q-011--concurrency-runtime-architecture) | Concurrency runtime architecture | Concurrency | Open |
| [P2Q-012](#p2q-012--asynchronous-execution-model-and-api-coloring) | Asynchronous execution model and API coloring | Concurrency | Open |
| [P2Q-013](#p2q-013--ffi-architecture) | FFI architecture | Interop | Open |
| [P2Q-014](#p2q-014--abi-stability-policy) | ABI stability policy | Interop | Open |
| [P2Q-015](#p2q-015--debug-information-strategy) | Debug information strategy | Tooling | Open |
| [P2Q-016](#p2q-016--package-and-build-architecture) | Package and build architecture | Ecosystem | Open |
| [P2Q-017](#p2q-017--standard-library-scope-and-first-party-packages) | Standard-library scope and first-party packages | Library | Open |
| [P2Q-018](#p2q-018--cryptography-and-tls-implementation-strategy) | Cryptography and TLS implementation strategy | Security | Open |
| [P2Q-019](#p2q-019--numerical-and-accelerator-architecture) | Numerical and accelerator architecture | AI/ML | Open |
| [P2Q-020](#p2q-020--constant-time-code-and-compiler-guarantees) | Constant-time code and compiler guarantees | Security | Open |
| [P2Q-021](#p2q-021--secret-lifetime-under-the-memory-model) | Secret lifetime under the memory model | Security | Open |
| [P2Q-022](#p2q-022--intermediate-representation) | Intermediate representation | Compiler | Open |
| [P2Q-023](#p2q-023--implementation-language-and-bootstrapping) | Implementation language and bootstrapping | Compiler | Open |
| [P2Q-024](#p2q-024--unsafe-code-model) | Unsafe-code model | Safety | Open |
| [P2Q-025](#p2q-025--compile-time-code-execution-and-metaprogramming) | Compile-time code execution and metaprogramming | Language | Open |
| [P2Q-026](#p2q-026--module-and-package-identity) | Module and package identity | Language | Open |
| [P2Q-027](#p2q-027--syntax-design-process) | Syntax design process | Language | Open |
| [P2Q-028](#p2q-028--specification-method-and-conformance-suite) | Specification method and conformance suite | Process | Open |

---

## Types

### P2Q-001 — Static, dynamic or gradual typing

- **Question:** What typing discipline does Cretes use, and how much checking happens before execution?
- **Must satisfy:** [CORE-017](requirements/CORE.md#core-017--errors-detected-before-execution) (MUST detect certain errors pre-execution; SHOULD detect type mismatches), [CORE-009](requirements/CORE.md#core-009--name-resolution-without-execution), [SAFE-015](requirements/SAFETY.md#safe-015--type-safety), [PERF-009](requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput), [DX-012](requirements/CORE.md#dx-012--language-server).
- **Candidates:** Static typing. Static typing with local inference. Gradual typing. Dynamic typing with optional static analysis.
- **Decision vehicle:** RFC.

### P2Q-002 — Type inference scope

- **Question:** Where are type annotations required and where are they inferred? Examples are function signatures, locals, closures and generic arguments.
- **Must satisfy:** [CORE-020](requirements/CORE.md#core-020--reduced-annotation-burden), [DX-005](requirements/CORE.md#dx-005--diagnostic-content), [Principle 6](principles/DESIGN-PRINCIPLES.md#6-excellent-diagnostics), [Principle 11](principles/DESIGN-PRINCIPLES.md#11-readability).
- **Candidates:** Local-only inference. Bidirectional inference. Whole-function inference. Global inference.
- **Decision vehicle:** RFC (may be combined with P2Q-001).

### P2Q-003 — Generics model

- **Question:** How is parametric abstraction expressed, constrained and compiled?
- **Must satisfy:** [CORE-019](requirements/CORE.md#core-019--parametric-abstraction), [PERF-009](requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput), [PERF-005](requirements/PERFORMANCE.md#perf-005--toolchain-responsiveness), [PERF-012](requirements/PERFORMANCE.md#perf-012--artifact-size), [Principle 14](principles/DESIGN-PRINCIPLES.md#14-zero-cost-or-low-cost-abstractions-where-practical).
- **Candidates:**
  - Constraints: interfaces, traits, type classes or structural constraints.
  - Compilation: monomorphization, dictionary passing, or a hybrid.
- **Decision vehicle:** RFC.

## Memory

### P2Q-004 — Memory-management architecture

- **Question:** How is memory allocated and reclaimed?
- **Must satisfy:** [SAFE-023](requirements/SAFETY.md#safe-023--memory-management-evaluation-criteria) (the full evaluation list), including SAFE-001 to SAFE-007, SAFE-012, SAFE-013, [PERF-010](requirements/PERFORMANCE.md#perf-010--memory-footprint-and-control), [INTOP-005](requirements/INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary) and [SEC-005](requirements/domains/cybersecurity.md#sec-005--secret-zeroization).
- **Candidates:**
  - Ownership and borrowing.
  - Tracing garbage collection (non-moving or moving).
  - Reference counting (with or without cycle collection).
  - Regions or arenas.
  - Hybrid combinations.
- **Decision vehicle:** RFC. This is the most consequential Phase 2 decision.

### P2Q-005 — Mutability, aliasing and ownership model

- **Question:** How does the language control aliasing of mutable data, and what is the default mutability?
- **Must satisfy:** [CORE-011](requirements/CORE.md#core-011--mutable-and-immutable-bindings), [SAFE-005](requirements/SAFETY.md#safe-005--valid-references), [SAFE-012](requirements/SAFETY.md#safe-012--data-race-freedom), [CONC-013](requirements/CONCURRENCY.md#conc-013--diagnosing-unsafe-sharing).
- **Candidates:**
  - Exclusive-or-shared borrowing.
  - Immutable-by-default with explicit mutation.
  - Reference capabilities.
  - Actor or isolation domains.
  - Copy-on-write values.
- **Decision vehicle:** RFC (tightly coupled to P2Q-004).

### P2Q-006 — Value and reference semantics

- **Question:** Which types have value semantics and which have reference semantics? When are copies implicit?
- **Must satisfy:** [PERF-003](requirements/PERFORMANCE.md#perf-003--visible-expensive-operations), [PERF-011](requirements/PERFORMANCE.md#perf-011--allocation-free-values), [AI-003](requirements/domains/ai-ml.md#ai-003--packed-value-layout), [INTOP-003](requirements/INTEROPERABILITY.md#intop-003--c-compatible-data-layout).
- **Candidates:** All values. Programmer-chosen per type. Language-defined categories.
- **Decision vehicle:** RFC.

## Semantics

### P2Q-007 — Error model

- **Question:** How are recoverable errors represented and propagated? Do faults unwind or abort?
- **Must satisfy:** [CORE-022](requirements/CORE.md#core-022--explicit-recoverable-errors), [CORE-023](requirements/CORE.md#core-023--recoverable-errors-versus-faults), [SAFE-020](requirements/SAFETY.md#safe-020--defined-fault-behavior), [CONC-008](requirements/CONCURRENCY.md#conc-008--error-propagation), [INTOP-007](requirements/INTEROPERABILITY.md#intop-007--error-propagation-across-the-boundary), [AUTO-002](requirements/domains/automation.md#auto-002--error-context-for-operational-failures).
- **Candidates:**
  - Result-style values with a propagation construct.
  - Checked exceptions.
  - Effect-typed errors.
  - For faults: abort-only, or unwinding to boundaries.
- **Decision vehicle:** RFC.

### P2Q-008 — Nullability representation

- **Question:** How is absence represented and handled?
- **Must satisfy:** [SAFE-006](requirements/SAFETY.md#safe-006--null-safety), [CORE-012](requirements/CORE.md#core-012--user-defined-data-types), [INTOP-003](requirements/INTEROPERABILITY.md#intop-003--c-compatible-data-layout) (C null pointers at the boundary).
- **Candidates:** An option-type alternative. Nullable type annotations with flow typing. Both.
- **Decision vehicle:** RFC (may be combined with P2Q-007).

### P2Q-009 — Default integer overflow behavior

- **Question:** What does default integer arithmetic do on overflow, and does the behavior differ between build profiles?
- **Must satisfy:** [SAFE-008](requirements/SAFETY.md#safe-008--defined-integer-overflow), [SAFE-009](requirements/SAFETY.md#safe-009--explicit-overflow-handling-operations), [SAFE-010](requirements/SAFETY.md#safe-010--overflow-detection-during-development), [PERF-008](requirements/PERFORMANCE.md#perf-008--development-and-optimized-profiles), [SEC-003](requirements/domains/cybersecurity.md#sec-003--checked-length-arithmetic-in-parsers).
- **Candidates:** Always trap. Trap in development and wrap in optimized builds. Always wrap. Arbitrary-precision default integers.
- **Security note:** Profile-dependent behavior means tested and deployed programs can differ. The RFC must address this explicitly.
- **Decision vehicle:** RFC.

## Compiler and execution

### P2Q-010 — Execution model and backend

- **Question:** How are Cretes programs executed, and which backend generates code?
- **Must satisfy:** [DX-003](requirements/CORE.md#dx-003--cretes-build), [PERF-001](requirements/PERFORMANCE.md#perf-001--self-contained-executables), [PERF-004](requirements/PERFORMANCE.md#perf-004--program-startup-latency), [PERF-005](requirements/PERFORMANCE.md#perf-005--toolchain-responsiveness), [PERF-009](requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput), [DX-014](requirements/CORE.md#dx-014--debugger-support), [PLAT-002](requirements/PLATFORMS.md#plat-002--tier-1-candidates), [SEC-027](requirements/domains/cybersecurity.md#sec-027--reproducible-builds).
- **Candidates:**
  - Ahead-of-time native compilation via LLVM, Cranelift, GCC or a custom backend.
  - Bytecode VM, with or without a JIT.
  - Transpilation to another language.
  - Different backends per profile.
- **Decision vehicle:** RFC.

### P2Q-022 — Intermediate representation

- **Question:** What intermediate representations does the compiler use for checking, optimization, incremental compilation and tooling?
- **Must satisfy:** [CORE-029](requirements/CORE.md#core-029--separate-and-incremental-compilation), [DX-017](requirements/CORE.md#dx-017--consistent-semantics-across-tools), [DX-005](requirements/CORE.md#dx-005--diagnostic-content) (preserving spans).
- **Decision vehicle:** Architecture RFC (after P2Q-010).

### P2Q-023 — Implementation language and bootstrapping

- **Question:** In which language is the initial compiler written? Is self-hosting a goal, and if so, when?
- **Must satisfy:** [CORE-025](requirements/CORE.md#core-025--deterministic-compilation), [SEC-027](requirements/domains/cybersecurity.md#sec-027--reproducible-builds), [SEC-032](requirements/domains/cybersecurity.md#sec-032--toolchain-release-integrity), [PLAT-002](requirements/PLATFORMS.md#plat-002--tier-1-candidates). Also consider contributor accessibility and the auditability of the bootstrap chain.
- **Decision vehicle:** RFC.

## Concurrency

### P2Q-011 — Concurrency runtime architecture

- **Question:** What executes tasks, and how are they scheduled?
- **Must satisfy:** [CONC-001](requirements/CONCURRENCY.md#conc-001--concurrent-tasks) to [CONC-020](requirements/CONCURRENCY.md#conc-020--concurrency-and-foreign-code), [NET-002](requirements/domains/networking.md#net-002--scalable-asynchronous-io), [NET-003](requirements/domains/networking.md#net-003--connection-scale-design-target), [PERF-014](requirements/PERFORMANCE.md#perf-014--concurrency-overhead).
- **Candidates:**
  - OS threads.
  - Green threads or fibers.
  - Stackless coroutines or async state machines.
  - Event loops.
  - Work-stealing schedulers.
  - Hybrid designs.
- **Decision vehicle:** RFC.

### P2Q-012 — Asynchronous execution model and API coloring

- **Question:** Do asynchronous and synchronous functions differ in type or calling convention? If they do, how does the ecosystem avoid splitting?
- **Must satisfy:** [CONC-019](requirements/CONCURRENCY.md#conc-019--unified-concurrency-model), [CONC-015](requirements/CONCURRENCY.md#conc-015--blocking-and-cpu-intensive-work), [PERF-003](requirements/PERFORMANCE.md#perf-003--visible-expensive-operations), [Principle 3](principles/DESIGN-PRINCIPLES.md#3-simple-common-cases).
- **Decision vehicle:** RFC (coupled to P2Q-011).

## Interoperability

### P2Q-013 — FFI architecture

- **Question:** How are foreign functions and types declared, how are bindings generated, and how is memory shared?
- **Must satisfy:** [INTOP-001](requirements/INTEROPERABILITY.md#intop-001--calling-c-abi-functions) to [INTOP-009](requirements/INTEROPERABILITY.md#intop-009--binding-generation), [INTOP-017](requirements/INTEROPERABILITY.md#intop-017--unsafe-ffi-declarations-are-not-trusted-by-default), [INTOP-019](requirements/INTEROPERABILITY.md#intop-019--declared-native-dependencies), [SAFE-018](requirements/SAFETY.md#safe-018--ffi-is-an-unsafe-boundary), [CONC-020](requirements/CONCURRENCY.md#conc-020--concurrency-and-foreign-code), [PERF-016](requirements/PERFORMANCE.md#perf-016--ffi-call-overhead).
- **Decision vehicle:** RFC (after P2Q-004).

### P2Q-014 — ABI stability policy

- **Question:** Will Cretes ever define a stable native ABI? If so, when, and for what surface?
- **Must satisfy:** [INTOP-018](requirements/INTEROPERABILITY.md#intop-018--abi-stability-policy), [CORE-030](requirements/CORE.md#core-030--language-evolution-mechanism), [Principle 13](principles/DESIGN-PRINCIPLES.md#13-stability-must-be-earned).
- **Decision vehicle:** RFC before 1.0.

## Tooling and ecosystem

### P2Q-015 — Debug information strategy

- **Question:** Which debug-information formats are emitted per platform, and how are language-specific constructs presented in debuggers?
- **Must satisfy:** [DX-014](requirements/CORE.md#dx-014--debugger-support), [SEC-027](requirements/domains/cybersecurity.md#sec-027--reproducible-builds) (for example path remapping).
- **Decision vehicle:** Architecture RFC (after P2Q-010).

### P2Q-016 — Package and build architecture

- **Question:** What is the manifest format, the resolution algorithm, the lock-file format, the build-script model, the registry protocol and the provenance mechanism?
- **Must satisfy:** [CORE-028](requirements/CORE.md#core-028--declarative-package-manifest), [DX-015](requirements/CORE.md#dx-015--package-manager-and-registry), [SEC-023](requirements/domains/cybersecurity.md#sec-023--dependency-integrity) to [SEC-029](requirements/domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting), [SEC-034](requirements/domains/cybersecurity.md#sec-034--registry-account-and-namespace-protection).
- **Decision vehicle:** RFC series.

### P2Q-017 — Standard-library scope and first-party packages

- **Question:** Which "First-party library" capabilities ship in the standard library, and which ship as separately versioned official packages? Examples are TLS, HTTP, cryptography, n-dimensional arrays and serialization formats.
- **Must satisfy:** The [layer model](requirements/README.md#layers), [Principle 3](principles/DESIGN-PRINCIPLES.md#3-simple-common-cases), [Principle 13](principles/DESIGN-PRINCIPLES.md#13-stability-must-be-earned), [SEC-018](requirements/domains/cybersecurity.md#sec-018--tls-security-policy) (updatable security defaults).
- **Decision vehicle:** RFC.

### P2Q-026 — Module and package identity

- **Question:** How are modules named, located, versioned and made visible? How do they map to files and packages?
- **Must satisfy:** [CORE-007](requirements/CORE.md#core-007--modules), [CORE-008](requirements/CORE.md#core-008--visibility-control), [CORE-009](requirements/CORE.md#core-009--name-resolution-without-execution), [CORE-010](requirements/CORE.md#core-010--controlled-module-initialization), [SEC-034](requirements/domains/cybersecurity.md#sec-034--registry-account-and-namespace-protection).
- **Decision vehicle:** RFC.

## Security

### P2Q-018 — Cryptography and TLS implementation strategy

- **Question:** Does Cretes bind to platform cryptography and TLS, bind to an external audited library, port audited implementations, or write its own? How are the chosen implementations kept updated?
- **Must satisfy:** [SEC-006](requirements/domains/cybersecurity.md#sec-006--secure-randomness) to [SEC-019](requirements/domains/cybersecurity.md#sec-019--certificate-handling), [SEC-015](requirements/domains/cybersecurity.md#sec-015--cryptographic-implementation-assurance), [NET-017](requirements/domains/networking.md#net-017--tls), [PLAT-005](requirements/PLATFORMS.md#plat-005--criteria-for-official-support), [PLAT-012](requirements/PLATFORMS.md#plat-012--minimal-external-runtime-dependencies).
- **Decision vehicle:** RFC, with security review.

### P2Q-020 — Constant-time code and compiler guarantees

- **Question:** Can the compiler guarantee that designated code keeps constant-time properties through optimization, or must constant-time primitives rely on vetted implementations outside the optimizer's reach?
- **Must satisfy:** [SEC-004](requirements/domains/cybersecurity.md#sec-004--constant-time-operations), [SEC-009](requirements/domains/cybersecurity.md#sec-009--message-authentication).
- **Decision vehicle:** RFC, with security review (after P2Q-010).

### P2Q-021 — Secret lifetime under the memory model

- **Question:** How can secret zeroization be guaranteed under the chosen memory model?
- **Background:** A moving collector, implicit copies or reference sharing can leave copies of secrets that zeroization cannot reach.
- **Must satisfy:** [SEC-005](requirements/domains/cybersecurity.md#sec-005--secret-zeroization), [SEC-017](requirements/domains/cybersecurity.md#sec-017--key-and-credential-handling), [SAFE-023](requirements/SAFETY.md#safe-023--memory-management-evaluation-criteria).
- **Decision vehicle:** Part of the P2Q-004 RFC, with security review.

### P2Q-024 — Unsafe-code model

- **Question:** What exactly constitutes an unsafe operation? How are unsafe regions scoped? How are proof obligations specified? How do package-level unsafe policies work?
- **Must satisfy:** [SAFE-016](requirements/SAFETY.md#safe-016--explicit-and-auditable-unsafe-code) to [SAFE-019](requirements/SAFETY.md#safe-019--package-level-unsafe-policy), [SAFE-022](requirements/SAFETY.md#safe-022--checked-builds-for-unsafe-code), [SEC-029](requirements/domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting).
- **Decision vehicle:** RFC.

## AI/ML

### P2Q-019 — Numerical and accelerator architecture

- **Question:** Where does the n-dimensional array abstraction live? How are SIMD operations exposed? How should buffer and memory designs be kept open to future device memory spaces?
- **Must satisfy:** [AI-003](requirements/domains/ai-ml.md#ai-003--packed-value-layout) to [AI-011](requirements/domains/ai-ml.md#ai-011--parallel-numerical-computation), [AI-018](requirements/domains/ai-ml.md#ai-018--cpu-execution-first), [AI-019](requirements/domains/ai-ml.md#ai-019--accelerator-ready-architecture-future-architecture). No vendor-specific concept may become language-level.
- **Decision vehicle:** RFC (accelerator aspects remain exploratory).

## Language design process

### P2Q-025 — Compile-time code execution and metaprogramming

- **Question:** Does Cretes support macros, compile-time evaluation or code generation? If so, with what limits?
- **Must satisfy:** [CORE-009](requirements/CORE.md#core-009--name-resolution-without-execution), [SEC-025](requirements/domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation), [DX-005](requirements/CORE.md#dx-005--diagnostic-content), [Principle 10](principles/DESIGN-PRINCIPLES.md#10-consistency-over-excessive-syntax).
- **Security note:** Compile-time execution of dependency code is a supply-chain risk. It must be sandboxed or auditable.
- **Decision vehicle:** RFC.

### P2Q-027 — Syntax design process

- **Question:** How will the surface syntax be decided?
- **Scope:** Block structure (braces or indentation), statement termination, declaration forms, generics notation, error-propagation notation, async notation and module syntax.
- **Must satisfy:** [Principle 10](principles/DESIGN-PRINCIPLES.md#10-consistency-over-excessive-syntax), [Principle 11](principles/DESIGN-PRINCIPLES.md#11-readability), [CORE-002](requirements/CORE.md#core-002--source-encoding) to [CORE-005](requirements/CORE.md#core-005--protection-against-deceptive-source-text), [DX-009](requirements/CORE.md#dx-009--canonical-formatter).
- **Note:** Syntax follows the semantic decisions above. Syntax is not frozen before those decisions are made.
- **Decision vehicle:** RFC series.

### P2Q-028 — Specification method and conformance suite

- **Question:** How formal is the specification? For example, prose, formal grammar, formal semantics for selected areas, or an executable reference. How are conformance tests organized and linked to requirement IDs?
- **Must satisfy:** [CORE-031](requirements/CORE.md#core-031--specification-coverage-of-shipped-features), and the [traceability model](requirements/README.md#traceability).
- **Decision vehicle:** RFC.

## Related documents

- [Requirements framework](requirements/README.md)
- [Design principles](principles/DESIGN-PRINCIPLES.md)
- [Phase 1 review](reviews/PHASE-1-REVIEW.md)
- [RFC process](https://github.com/Cretes-lang/rfcs)
