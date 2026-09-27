# Interoperability requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

Cretes will not replace existing software ecosystems. Operating systems, cryptographic libraries, AI inference runtimes and decades of native libraries are reached through interoperability. This document defines what interoperability Cretes needs and in what order ([Principle 7](../principles/DESIGN-PRINCIPLES.md#7-interoperability-over-isolation)).

> **No ABI or FFI design is defined here.** Declaration forms, calling-convention annotations, layout attributes, binding generators and the Cretes-native ABI are Phase 2+ decisions ([P2Q-013](../PHASE-2-OPEN-QUESTIONS.md#p2q-013--ffi-architecture), [P2Q-014](../PHASE-2-OPEN-QUESTIONS.md#p2q-014--abi-stability-policy)).

Terminology, layers and targets are defined in the [requirements framework](README.md).

## Contents

- [Integration classification](#integration-classification)
- [Why the C ABI first](#why-the-c-abi-first)
- [Calling and data exchange](#calling-and-data-exchange)
- [Ownership, errors and safety boundaries](#ownership-errors-and-safety-boundaries)
- [Other ecosystems](#other-ecosystems)
- [ABI stability](#abi-stability)

## Integration classification

| Integration | Class | Notes |
| --- | --- | --- |
| C ABI: calling C functions | **Initial** | Foundation for OS APIs, native libraries, crypto and AI runtimes. |
| Native static and shared libraries | **Initial** | Linking against C-ABI libraries. |
| Operating-system APIs (POSIX, Win32, Darwin) | **Initial** | Reached through the C ABI. Wrapped by the standard library. |
| C ABI: exposing Cretes functions | **Near-term** | Lets Cretes libraries be used from other languages. |
| AI inference runtimes with C APIs | **Near-term** | Via the C ABI. See [ai-ml.md](domains/ai-ml.md). |
| C++ | **Near-term** via C-ABI shims; **Exploratory** for direct interop | Direct C++ interop requires handling templates, exceptions and name mangling. |
| WebAssembly | **Long-term** | Compiling Cretes to Wasm, and embedding. Also a [platform](PLATFORMS.md) candidate. |
| Python | **Long-term** | Extension modules or embedding, via the C ABI. |
| JavaScript | **Long-term** | Primarily through WebAssembly. |
| JVM ecosystems | **Exploratory** | Via JNI or the Java Foreign Function & Memory API, both of which consume C ABI. |

The C ABI is the only integration required before any other. The v0.1 milestone requires **no** user-visible FFI ([V0.1-REQUIREMENTS.md](V0.1-REQUIREMENTS.md)). However, its architecture must leave room for [INTOP-001](#intop-001--calling-c-abi-functions).

## Why the C ABI first

- Every Tier 1 candidate operating system exposes its system interfaces through a C-compatible ABI.
- Mature cryptographic libraries, compression libraries, databases and AI inference runtimes provide C APIs.
- Python, the JVM, .NET, Node.js and WebAssembly hosts can all consume C-ABI libraries. A Cretes C-ABI export therefore reaches many ecosystems at once.
- The C ABI is stable and documented for each platform, and is understood by existing debuggers and linkers.

The C ABI is not a safe interface. Its use is bounded by [SAFE-018](SAFETY.md#safe-018--ffi-is-an-unsafe-boundary).

## Calling and data exchange

### INTOP-001 — Calling C-ABI functions

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Cretes programs must be able to call functions that use the platform's C calling convention, including variadic functions where the platform permits. Calls must pass and return primitive values, pointers and C-compatible aggregates.
- **Rationale:** The foundation of all other interoperability.
- **Verification:** Integration tests under Platform CI.

### INTOP-002 — Exposing Cretes functions through the C ABI

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Cretes must be able to define functions callable through the C ABI. The toolchain must be able to package them as static or shared libraries.
- **Rationale:** Allows incremental adoption inside existing C, C++, Python and other codebases.
- **Verification:** Integration tests under Platform CI.

### INTOP-003 — C-compatible data layout

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Programmers must be able to declare types whose memory layout matches the platform C layout. This covers field order, size, alignment and padding for structures, unions, enumerations with a specified underlying integer type, and fixed-size arrays.
- **Rationale:** Required to exchange structures with OS APIs, network stacks and native libraries.
- **Verification:** Integration tests comparing layouts with the platform C compiler.

### INTOP-004 — Linking and loading native libraries

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain must support linking against native static and shared libraries declared by a project. The standard library should support loading shared libraries at run time.
- **Rationale:** Most native functionality is distributed as libraries. Plugin systems need run-time loading.
- **Verification:** Integration tests under Platform CI.

### INTOP-008 — Callbacks from foreign code

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Foreign code must be able to call Cretes functions through function pointers, including from threads not created by Cretes. The behavior must be defined, including that of the concurrency runtime ([CONC-020](CONCURRENCY.md#conc-020--concurrency-and-foreign-code)).
- **Rationale:** OS APIs, event libraries and inference runtimes use callbacks.
- **Verification:** Integration tests.

### INTOP-009 — Binding generation

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The project should provide a tool that generates Cretes declarations from C headers. Generated bindings are unsafe declarations to be wrapped.
- **Rationale:** Handwritten bindings are slow to produce and error-prone. Mistakes cause memory corruption.
- **Verification:** Integration tests.

### INTOP-010 — Operating-system API access

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Programs must be able to reach platform-specific OS APIs when the portable standard library is insufficient. Platform-specific interfaces must be clearly separated from portable ones ([PLAT-007](PLATFORMS.md#plat-007--explicit-platform-specific-code)).
- **Rationale:** Systems, security and automation tools inevitably need platform-specific features.
- **Verification:** Integration tests under Platform CI.

## Ownership, errors and safety boundaries

### INTOP-005 — Memory ownership across the boundary

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** The FFI design must let every binding state who allocates, owns and releases memory passed across the boundary. Memory managed by Cretes and passed to foreign code must remain valid and unmoved for a duration the programmer can control, whatever memory-management model Phase 2 selects. Foreign-owned memory must not be released by Cretes memory management.
- **Rationale:** Ownership confusion across FFI is a primary source of use-after-free and double-free. This is an evaluation criterion in [SAFE-023](SAFETY.md#safe-023--memory-management-evaluation-criteria).
- **Verification:** Design review; Integration tests; Security review.

### INTOP-006 — Safe wrappers

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Foreign declarations must be usable only through unsafe operations ([SAFE-018](SAFETY.md#safe-018--ffi-is-an-unsafe-boundary)). It must be possible to wrap them in safe interfaces that validate arguments and translate ownership ([SAFE-017](SAFETY.md#safe-017--safe-abstractions-over-unsafe-code)).
- **Rationale:** Confines unverifiable code to small, reviewable regions.
- **Verification:** Conformance tests; Security review.

### INTOP-007 — Error propagation across the boundary

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** The standard library must offer conversions from common foreign error conventions to Cretes errors ([CORE-024](CORE.md#core-024--structured-error-information)). These conventions include return codes, `errno` and `GetLastError`. Cretes faults or errors must not propagate across foreign frames in a way the target ABI leaves undefined. Behavior when a foreign call fails in a way Cretes cannot represent must be defined.
- **Rationale:** Unwinding across C frames is undefined in many ABIs. Lost `errno` values cause misdiagnosis.
- **Verification:** Integration tests; Specification review.

### INTOP-019 — Declared native dependencies

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** A package's native library dependencies and foreign declarations must be discoverable from its manifest and by tooling, so that they can be audited ([SEC-029](domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting)).
- **Rationale:** Native code is a supply-chain and safety risk that must be visible.
- **Verification:** Integration tests.

## Other ecosystems

### INTOP-011 — C++ interoperability

- **Priority:** SHOULD · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** Cretes should document and support a pattern for using C++ libraries through C-ABI shims. Direct C++ interoperability MAY be explored later.
- **Rationale:** Many AI runtimes and systems libraries are written in C++. Shims are practical now. Direct interop is a large research effort.
- **Verification:** Integration tests (example project).

### INTOP-012 — AI runtime integration

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should be able to integrate with established inference runtimes that expose C APIs, and exchange tensor buffers without copying where layouts are compatible ([AI-008](domains/ai-ml.md#ai-008--tensor-compatible-layout-descriptors)).
- **Rationale:** AI/ML Applications is a primary domain. Cretes aims to use existing runtimes, not replace them.
- **Verification:** Integration tests.

### INTOP-013 — Python interoperability

- **Priority:** MAY · **Layer:** Ecosystem · **Target:** Long-term
- **Requirement:** Cretes may support building Python extension modules or embedding a Python interpreter, through the C ABI.
- **Rationale:** Python dominates AI/ML and automation. Interop enables gradual adoption.
- **Verification:** Integration tests.

### INTOP-014 — JavaScript interoperability

- **Priority:** MAY · **Layer:** Ecosystem · **Target:** Long-term
- **Requirement:** Cretes may support interoperation with JavaScript hosts, primarily through WebAssembly ([INTOP-016](#intop-016--webassembly-modules)).
- **Rationale:** Browser and edge runtimes are JavaScript-hosted.
- **Verification:** Integration tests.

### INTOP-015 — JVM interoperability

- **Priority:** MAY · **Layer:** Ecosystem · **Target:** Exploratory
- **Requirement:** Interoperation with JVM ecosystems may be explored through their C-ABI facilities.
- **Rationale:** Enterprise automation often involves JVM systems. Demand is not yet established.
- **Verification:** Inspection (feasibility report).

### INTOP-016 — WebAssembly modules

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Long-term
- **Requirement:** The architecture should not preclude compiling Cretes programs to WebAssembly modules that interact with host interfaces, such as WASI or browser hosts ([PLAT-004](PLATFORMS.md#plat-004--future-platform-candidates)).
- **Rationale:** WebAssembly is a portable sandboxed target for plugins, edge computing and the playground.
- **Verification:** Design review.

## ABI stability

### INTOP-018 — ABI stability policy

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** Until a documented decision states otherwise, the Cretes-native ABI must be treated as unstable. Separately compiled Cretes artifacts must not be assumed compatible across toolchain versions. C-ABI exports ([INTOP-002](#intop-002--exposing-cretes-functions-through-the-c-abi)) are the stable binary boundary. Each release's documentation must state this policy.
- **Rationale:** Freezing an ABI early blocks language evolution. Clear policy prevents users from relying on accidental compatibility.
- **Verification:** Inspection at release review.

### INTOP-017 — Unsafe FFI declarations are not trusted by default

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain must not treat a foreign declaration as a verified description of foreign behavior. Mismatches between a Cretes foreign declaration and the actual foreign signature must be treated as the programmer's responsibility. Documentation must say so, and tooling SHOULD help detect such mismatches, for example by checking against headers.
- **Rationale:** Makes the trust boundary explicit and avoids overstating safety.
- **Verification:** Inspection; Integration tests.

## Related documents

- [Safety requirements](SAFETY.md)
- [Platform requirements](PLATFORMS.md)
- [AI/ML requirements](domains/ai-ml.md)
- [Phase 2 open questions](../PHASE-2-OPEN-QUESTIONS.md)
