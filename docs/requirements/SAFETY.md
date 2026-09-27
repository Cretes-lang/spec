# Safety requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This document defines the **safety outcomes** Cretes must deliver. It deliberately does **not** choose how they are achieved.

> **No memory-management model is selected.** Ownership and borrowing, tracing garbage collection, reference counting, regions, arenas, manual allocation and hybrid designs remain candidates. Phase 2 evaluates them against these outcomes ([P2Q-004](../PHASE-2-OPEN-QUESTIONS.md#p2q-004--memory-management-architecture)). An outcome that no candidate can satisfy must be revisited by RFC. It must not be silently dropped.

Terminology, layers and targets are defined in the [requirements framework](README.md).

## Contents

- [Definitions](#definitions)
- [Foundational outcome](#foundational-outcome)
- [Memory safety](#memory-safety)
- [Value and type safety](#value-and-type-safety)
- [Concurrency safety](#concurrency-safety)
- [Resource safety](#resource-safety)
- [Unsafe operations and FFI boundaries](#unsafe-operations-and-ffi-boundaries)
- [Failure behavior](#failure-behavior)
- [Evaluation criteria for Phase 2](#evaluation-criteria-for-phase-2)

## Definitions

| Term | Meaning in this document |
| --- | --- |
| **Safe code** | Cretes code that does not use any operation the language designates as unsafe. By default, all code is safe code. |
| **Unsafe operation** | An operation whose correctness the implementation cannot check. Examples include dereferencing a raw address, calling foreign code, reinterpreting memory, or asserting an invariant the compiler cannot prove. |
| **Undefined behavior** | Behavior for which the specification imposes no requirements. |
| **Defined failure** | A specified, observable outcome such as a reported error or a controlled program termination. It never includes memory corruption or continued execution in an inconsistent state. |

## Foundational outcome

### SAFE-001 — No undefined behavior in safe code

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Every program that the toolchain accepts and that contains only safe code must have behavior fully defined by the specification. That behavior may include defined failure.
- **Rationale:** This is the root safety property. Every other requirement in this document elaborates a way undefined behavior commonly arises.
- **Verification:** Specification review; Conformance tests; Fuzzing; Security review.

## Memory safety

### SAFE-002 — Spatial memory safety

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Safe code must not be able to read or write outside the bounds of an object, array or buffer. Each potential out-of-bounds access must either be rejected before execution or be checked at run time with a defined failure. The implementation may remove checks it can prove unnecessary.
- **Rationale:** Out-of-bounds access is among the most exploited vulnerability classes.
- **Verification:** Conformance tests; Fuzzing.

### SAFE-003 — Temporal memory safety

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Safe code must not be able to access memory after the object it belonged to has been reclaimed. This excludes use-after-free and dangling references.
- **Rationale:** Use-after-free is a leading cause of exploitable memory corruption.
- **Verification:** Conformance tests; Fuzzing; Design review.

### SAFE-004 — No double release

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Safe code must not be able to release the same memory or resource more than once.
- **Rationale:** Double-free corrupts allocator state and is exploitable.
- **Verification:** Conformance tests; Design review.

### SAFE-005 — Valid references

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** In safe code, every reference or handle that can be dereferenced must refer to a live value of the expected type.
- **Rationale:** Generalizes SAFE-003 and SAFE-006 to all indirections, including those into collections that may be resized.
- **Verification:** Conformance tests; Design review.

### SAFE-006 — Null safety

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The possible absence of a value must be expressed in the type of that value. Safe code must not be able to use a possibly absent value as present without first handling the absent case.
- **Rationale:** Null dereferences are a pervasive source of crashes. Making absence visible moves the check to where it is meaningful. The nullability design is [P2Q-008](../PHASE-2-OPEN-QUESTIONS.md#p2q-008--nullability-representation).
- **Verification:** Conformance tests; Diagnostic tests.

### SAFE-007 — No use of uninitialized values

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Safe code must not be able to observe the contents of uninitialized memory. Use of a variable or field before initialization must be rejected before execution, or the value must be defined by the specification.
- **Rationale:** Reading uninitialized memory leaks data, including secrets, and causes nondeterminism.
- **Verification:** Conformance tests; Diagnostic tests.

## Value and type safety

### SAFE-008 — Defined integer overflow

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Integer arithmetic overflow must never be undefined behavior. The default behavior on overflow is a Phase 2 decision ([P2Q-009](../PHASE-2-OPEN-QUESTIONS.md#p2q-009--default-integer-overflow-behavior)). Candidates include a defined failure or another fully specified result. The behavior must be documented, including any difference between build profiles.
- **Rationale:** Overflow in size and length computations is a common prelude to memory corruption.
- **Verification:** Conformance tests.

### SAFE-009 — Explicit overflow-handling operations

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language or standard library must provide explicit checked, wrapping and saturating integer operations, whatever the default behavior.
- **Rationale:** Hashing, checksums and cryptography need wrapping. Parsers need checked arithmetic. Signal processing needs saturation.
- **Verification:** Conformance tests; Unit tests.

### SAFE-010 — Overflow detection during development

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** At least one supported build profile should detect unintended integer overflow in default arithmetic and report it as a defined failure.
- **Rationale:** Surfaces overflow bugs during testing, even if a different default is chosen for optimized builds.
- **Verification:** Conformance tests.

### SAFE-011 — Defined arithmetic edge cases

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The following must have defined behavior:
  - integer division by zero;
  - the minimum signed value divided by −1;
  - shifts by an amount greater than or equal to the operand width;
  - conversion of out-of-range or NaN floating-point values to integers.
- **Rationale:** These cases are undefined in several established languages and are sources of portability bugs.
- **Verification:** Conformance tests.

### SAFE-015 — Type safety

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Safe code must not be able to reinterpret a value's memory as a different type, except through conversions the specification defines as valid for all bit patterns. Unchecked reinterpretation must be an unsafe operation.
- **Rationale:** Type confusion is a major vulnerability class.
- **Verification:** Conformance tests; Security review.

## Concurrency safety

### SAFE-012 — Data-race freedom

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Safe code must not be able to cause a data race: unsynchronized concurrent access to the same memory location where at least one access is a write. Race conditions at a higher level, such as logic races, are not covered by this requirement. The target is the first milestone that introduces concurrency. The v0.1 design must not preclude it.
- **Rationale:** Concurrency is foundational ([CONCURRENCY.md](CONCURRENCY.md)). Data races produce memory unsafety and nondeterminism that testing rarely catches.
- **Verification:** Design review; Conformance tests; Security review.

## Resource safety

### SAFE-013 — Deterministic resource release

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The language must provide a way to guarantee that non-memory resources, such as files, sockets, locks and handles, are released at a predictable program point. This must hold on every exit path, including error propagation, faults that permit cleanup, and cancellation ([CONC-006](CONCURRENCY.md#conc-006--cancellation)). The guarantee must not depend on when memory is reclaimed.
- **Rationale:** Resource leaks cause outages in long-running automation and network services. Deferred memory reclamation must not delay closing a socket.
- **Verification:** Conformance tests; Integration tests.

### SAFE-014 — Resource-leak diagnostics

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain or runtime should be able to report resources that were not released, or that were retained beyond their expected scope, at least in a diagnostic build profile.
- **Rationale:** Aids detection of leaks that the language model cannot rule out statically.
- **Verification:** Integration tests.

## Unsafe operations and FFI boundaries

### SAFE-016 — Explicit and auditable unsafe code

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Every unsafe operation must be explicitly marked in source. The marking must be scoped to the smallest practical region. Tools must be able to enumerate all unsafe regions in a package and its dependencies.
- **Rationale:** Expert low-level control is a design principle ([Principle 15](../principles/DESIGN-PRINCIPLES.md#15-clear-escape-hatches-for-expert-low-level-development)). It must remain visible and reviewable ([SEC-029](domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting)).
- **Verification:** Conformance tests; Integration tests.

### SAFE-017 — Safe abstractions over unsafe code

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Unsafe code must be able to implement interfaces that safe code uses. The language must make it possible for such interfaces to prevent safe callers from violating the invariants the unsafe code relies on. The proof obligations of each unsafe operation must be documented in the specification.
- **Rationale:** Allows performance-critical and FFI code to be encapsulated once and reused safely.
- **Verification:** Specification review; Security review.

### SAFE-018 — FFI is an unsafe boundary

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Calling foreign code, and accepting calls or data from foreign code, must be treated as unsafe unless a safe wrapper has encapsulated the boundary. Safety guarantees must not be claimed for behavior that occurs in foreign code. See [INTEROPERABILITY.md](INTEROPERABILITY.md).
- **Rationale:** The compiler cannot verify foreign code. Pretending otherwise would misstate the safety guarantee.
- **Verification:** Specification review; Security review.

### SAFE-019 — Package-level unsafe policy

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** A project should be able to declare that a package must not contain unsafe code, and the toolchain should enforce that declaration.
- **Rationale:** Lets security-sensitive projects constrain their own code and choose dependencies accordingly.
- **Verification:** Integration tests.

### SAFE-022 — Checked builds for unsafe code

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain should support a build profile that adds run-time checking to unsafe and foreign-boundary code, for example by integrating with platform address and undefined-behavior sanitizers where available.
- **Rationale:** Unsafe code is where memory-safety bugs will remain. Tooling should help find them.
- **Verification:** Integration tests.

## Failure behavior

### SAFE-020 — Defined fault behavior

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** When an unrecoverable fault occurs, such as a failed bounds check or a violated assertion, the program must behave as the specification defines. It must report the fault with source location where available, then either terminate or unwind to a defined boundary. Whether unwinding exists is a Phase 2 decision ([P2Q-007](../PHASE-2-OPEN-QUESTIONS.md#p2q-007--error-model)). Execution must never continue silently past a fault.
- **Rationale:** A detected violation that is then ignored provides no safety.
- **Verification:** Conformance tests.

### SAFE-021 — Defined behavior on resource exhaustion

- **Priority:** MUST · **Layer:** Runtime · **Target:** v0.1
- **Requirement:** Stack exhaustion must result in defined failure rather than memory corruption. Memory-allocation failure must also result in defined failure, or in a recoverable error where the API offers one.
- **Rationale:** Unbounded recursion on attacker-controlled input must not become a memory-corruption primitive.
- **Verification:** Conformance tests; Fuzzing.

## Evaluation criteria for Phase 2

### SAFE-023 — Memory-management evaluation criteria

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** The Phase 2 memory-management decision must be recorded in an accepted RFC. The RFC must evaluate every candidate against at least:
  - SAFE-001 to SAFE-007 and SAFE-012;
  - [SAFE-013](#safe-013--deterministic-resource-release);
  - latency predictability for network services ([PERF-010](PERFORMANCE.md#perf-010--memory-footprint-and-control));
  - FFI compatibility, including passing and pinning memory for foreign code ([INTOP-005](INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary));
  - secret zeroization ([SEC-005](domains/cybersecurity.md#sec-005--secret-zeroization));
  - concurrency ([CONC-013](CONCURRENCY.md#conc-013--diagnosing-unsafe-sharing));
  - learning cost for the [target developers](../vision/TARGET-USERS.md).
- **Rationale:** Makes the Phase 2 decision traceable to Phase 1 outcomes, rather than to preference.
- **Verification:** Design review.

## Related documents

- [Concurrency requirements](CONCURRENCY.md)
- [Interoperability requirements](INTEROPERABILITY.md)
- [Cybersecurity requirements](domains/cybersecurity.md)
- [Design principles](../principles/DESIGN-PRINCIPLES.md)
- [Phase 2 open questions](../PHASE-2-OPEN-QUESTIONS.md)
