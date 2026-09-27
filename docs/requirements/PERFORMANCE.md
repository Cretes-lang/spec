# Performance requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This document defines the performance dimensions that matter for Cretes, the requirements that shape its architecture, and the strategy for measuring them.

> **No performance claims are made.** Cretes has no implementation, so no measurements exist. Statements such as "faster than language X" are not permitted in project documentation unless they are backed by published, reproducible benchmarks ([PERF-017](#perf-017--evidence-before-claims)). Numeric targets are set only once executable implementations exist and baselines have been measured.

> **No compiler backend or execution model is selected.** Candidates include LLVM, Cranelift, GCC, a custom native backend, a bytecode VM, a JIT and transpilation. These are Phase 2 decisions ([P2Q-010](../PHASE-2-OPEN-QUESTIONS.md#p2q-010--execution-model-and-backend)).

Terminology, layers and targets are defined in the [requirements framework](README.md).

## Contents

- [Performance dimensions](#performance-dimensions)
- [Execution and cost model](#execution-and-cost-model)
- [Toolchain performance](#toolchain-performance)
- [Runtime performance](#runtime-performance)
- [Domain performance](#domain-performance)
- [Evidence and measurement](#evidence-and-measurement)
- [Benchmarking strategy](#benchmarking-strategy)

## Performance dimensions

| Dimension | What is measured | Primary personas | Requirements |
| --- | --- | --- | --- |
| Compiler startup | Time until the toolchain begins useful work | All | [PERF-005](#perf-005--toolchain-responsiveness) |
| Compilation latency | Time for `cretes check` and `cretes build` on representative projects | All | [PERF-006](#perf-006--analysis-faster-than-full-builds) |
| Incremental builds | Rebuild time after a small change | Systems, backend | [PERF-007](#perf-007--incremental-builds) |
| Program startup | Time from process launch to the first line of user code | Automation, DevOps | [PERF-004](#perf-004--program-startup-latency) |
| Runtime throughput | Work completed per unit time on compute-bound code | Systems, AI/ML | [PERF-009](#perf-009--optimizable-compute-throughput) |
| Memory usage | Resident memory of the baseline runtime and of representative programs | Backend, systems | [PERF-010](#perf-010--memory-footprint-and-control) |
| Allocation overhead | Cost and frequency of implicit allocations | Backend, AI/ML | [PERF-011](#perf-011--allocation-free-values) |
| Binary size | Size of built artifacts | Automation, DevOps, embedded (future) | [PERF-012](#perf-012--artifact-size) |
| Network throughput | Bytes and requests per second, latency percentiles | Backend, security | [PERF-013](#perf-013--efficient-io-buffers) |
| Concurrency overhead | Cost of creating, switching and cancelling tasks | Backend | [PERF-014](#perf-014--concurrency-overhead) |
| Numerical performance | Throughput on vectorizable and parallel kernels | AI/ML | [PERF-015](#perf-015--numerical-throughput) |
| FFI overhead | Cost of a call into or out of foreign code | Systems, AI/ML | [PERF-016](#perf-016--ffi-call-overhead) |

## Execution and cost model

### PERF-001 — Self-contained executables

- **Priority:** MUST · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** For Tier 1 platforms, the toolchain must be able to produce executables that run without a separately installed Cretes interpreter, virtual machine or toolchain. Any runtime support must be included in or shipped with the artifact.
- **Rationale:** Automation, DevOps and security tools are deployed as single artifacts to machines without developer tooling. v0.1 artifacts may take a different form ([DX-003](CORE.md#dx-003--cretes-build)).
- **Verification:** Platform CI.

### PERF-002 — Documented cost model

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** The specification and standard-library documentation must describe the performance characteristics of core operations. These include allocation, copying of values, dynamic dispatch, bounds checking, and the complexity of standard collection operations.
- **Rationale:** Predictable performance ([Principle 2](../principles/DESIGN-PRINCIPLES.md#2-predictable-performance)) requires that developers can reason about costs without profiling everything.
- **Verification:** Inspection.

### PERF-003 — Visible expensive operations

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Operations with potentially large or unbounded cost should be identifiable from source, types or documentation, and should not be hidden behind syntax that looks trivially cheap. Such operations include heap allocation, deep copies of large values, blocking waits and dynamic code loading.
- **Rationale:** Hidden costs undermine predictable latency in network services and tight numerical loops.
- **Verification:** Design review.

### PERF-008 — Development and optimized profiles

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** The toolchain must provide at least a fast-to-build development profile and an optimized profile. Semantics must be identical between them, except for differences the specification explicitly permits, such as overflow detection under [SAFE-010](SAFETY.md#safe-010--overflow-detection-during-development).
- **Rationale:** Build latency and runtime speed trade off against each other. Developers need both.
- **Verification:** Conformance tests run under both profiles.

## Toolchain performance

### PERF-005 — Toolchain responsiveness

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** Toolchain startup and analysis of a single small file should be fast enough for interactive use in editors and pre-commit hooks. The numeric target is set once baselines exist.
- **Rationale:** Slow feedback discourages use of the checker and language server.
- **Verification:** Benchmark (`startup/`, `compile/`).

### PERF-006 — Analysis faster than full builds

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** `cretes check` should complete in substantially less time than `cretes build` for the same project.
- **Rationale:** The check command exists to shorten the edit–diagnose loop ([DX-002](CORE.md#dx-002--cretes-check)).
- **Verification:** Benchmark (`compile/`).

### PERF-007 — Incremental builds

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** After a change confined to one module, rebuild time should scale with the size of the change and its dependents, not with total project size ([CORE-029](CORE.md#core-029--separate-and-incremental-compilation)).
- **Rationale:** Build latency dominates developer experience on large projects.
- **Verification:** Benchmark (`compile/`).

## Runtime performance

### PERF-004 — Program startup latency

- **Priority:** SHOULD · **Layer:** Runtime · **Target:** v0.1
- **Requirement:** Built programs should start quickly enough to be practical as short-lived command-line tools invoked many times in scripts. Startup must be measured and tracked from the first release.
- **Rationale:** Automation workloads invoke small tools repeatedly. Startup cost multiplies.
- **Verification:** Benchmark (`startup/`).

### PERF-009 — Optimizable compute throughput

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** The language semantics should not prevent the optimizations needed for compute-bound code to approach the throughput of equivalent C baselines. Examples are inlining, unboxed values, bounds-check elimination and vectorization. The acceptable gap is established by benchmark.
- **Rationale:** Systems, networking and AI/ML workloads are performance-sensitive. The target is a measured ratio, not a slogan.
- **Verification:** Benchmark (`compute/`).

### PERF-010 — Memory footprint and control

- **Priority:** SHOULD · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** The baseline memory footprint of a minimal program should be small and tracked. Programs should be able to control allocation in hot paths, for example by reusing buffers. Pause times introduced by memory management should be bounded and documented, to support latency-sensitive services.
- **Rationale:** Network services, CLI tools and constrained deployments are sensitive to memory usage and latency spikes. This is an evaluation criterion in [SAFE-023](SAFETY.md#safe-023--memory-management-evaluation-criteria).
- **Verification:** Benchmark (`memory/`).

### PERF-011 — Allocation-free values

- **Priority:** SHOULD · **Layer:** Language · **Target:** v0.1
- **Requirement:** Primitive values and small user-defined aggregates should be representable without mandatory heap allocation, including when they are stored in collections and arrays.
- **Rationale:** Mandatory boxing makes numerical arrays, packet buffers and hot loops allocation-bound ([AI-003](domains/ai-ml.md#ai-003--packed-value-layout)).
- **Verification:** Design review; Benchmark (`memory/`).

### PERF-012 — Artifact size

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The size of built artifacts should be measured and tracked. Unused code should be eliminable from release builds.
- **Rationale:** Deployment in containers, CI and future constrained targets benefits from small artifacts.
- **Verification:** Benchmark (`startup/`).

## Domain performance

### PERF-013 — Efficient I/O buffers

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** File and network I/O interfaces should allow buffer reuse and should avoid mandatory intermediate copies between the operating system and application data where the platform permits.
- **Rationale:** Network throughput and log or data processing are bounded by copying costs.
- **Verification:** Benchmark (`networking/`).

### PERF-014 — Concurrency overhead

- **Priority:** SHOULD · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** Creating, scheduling and cancelling a concurrent task should be cheap enough that a design with one task per connection or per request is practical at the scale of [NET-003](domains/networking.md#net-003--connection-scale-design-target).
- **Rationale:** Structured concurrency ([CONC-004](CONCURRENCY.md#conc-004--structured-concurrency)) is only practical if tasks are inexpensive.
- **Verification:** Benchmark (`concurrency/`).

### PERF-015 — Numerical throughput

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Contiguous numerical data should be processable with vectorized and parallel execution, without per-element dynamic dispatch or allocation ([AI-010](domains/ai-ml.md#ai-010--vectorized-computation), [AI-011](domains/ai-ml.md#ai-011--parallel-numerical-computation)).
- **Rationale:** Data preprocessing and CPU inference kernels depend on it.
- **Verification:** Benchmark (`numerical/`).

### PERF-016 — FFI call overhead

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** A call to a foreign C-ABI function that takes and returns primitive values should cost no more than a comparable native call, apart from overhead required by safety or runtime-state transitions that is documented and measured.
- **Rationale:** AI runtimes, cryptographic libraries and OS APIs are reached through FFI in tight loops.
- **Verification:** Benchmark (`compute/`).

## Evidence and measurement

### PERF-017 — Evidence before claims

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** Project documentation, releases and announcements must not make comparative or absolute performance claims unless the claims are backed by published, reproducible benchmark results. The claims must name the compared versions, hardware and methodology.
- **Rationale:** Credibility with engineers depends on honest measurement. The same rule appears in the RFC template.
- **Verification:** Inspection at release review.

### PERF-018 — Benchmark methodology

- **Priority:** MUST · **Layer:** Process · **Target:** Post-v0.1
- **Requirement:** Before the first performance-focused milestone, the project must maintain a benchmark suite that records:
  - hardware, operating system and toolchain versions;
  - build profile;
  - repetition count and variance.

  Benchmarks must run regularly enough to detect regressions.
- **Rationale:** Performance requirements are only meaningful if they are measured consistently.
- **Verification:** Inspection; Platform CI.

## Benchmarking strategy

The benchmark suite will live in the implementation repository ([`Cretes-lang/cretes`](https://github.com/Cretes-lang/cretes)) once an executable implementation exists. The proposed organization is:

```text
benchmarks/
├── startup/       # process start, minimal program, artifact size
├── compile/       # check/build latency, incremental rebuilds, large synthetic projects
├── compute/       # scalar algorithms, collections, string processing, FFI calls
├── memory/        # footprint, allocation rate, reclamation pauses
├── networking/    # TCP echo, HTTP request/response, TLS handshakes, many idle connections
├── concurrency/   # task spawn/cancel, channel throughput, contention
└── numerical/     # array kernels, reductions, matrix operations, preprocessing pipelines
```

Principles for the suite:

1. **Baselines come after implementations.** Numeric targets and comparison languages are chosen once Cretes programs can be executed. The comparison set should include C, because it is the reference for FFI and systems code. It should also include one or more established languages that the [target developers](../vision/TARGET-USERS.md) currently use. Comparisons are for learning, not marketing.
2. **Equivalent programs.** Compared programs must implement the same algorithm with idiomatic, reviewed code in each language.
3. **Reproducibility.** Scripts, inputs, versions and hardware descriptions are published with results.
4. **Distributions, not single numbers.** Report medians and variance. For latency, report percentiles.
5. **Regression tracking.** Once CI exists, significant regressions block releases or are documented as known issues.
6. **No synthetic green checks.** Following [ENGINEERING.md](https://github.com/Cretes-lang/.github/blob/main/ENGINEERING.md), no benchmark job exists until it measures something real.

## Related documents

- [Concurrency requirements](CONCURRENCY.md)
- [Networking requirements](domains/networking.md)
- [AI/ML requirements](domains/ai-ml.md)
- [Phase 2 open questions](../PHASE-2-OPEN-QUESTIONS.md)
