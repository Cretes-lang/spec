# AI/ML Applications requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

AI/ML Applications is one of the four official Cretes domains. The primary persona is the [AI/ML Application Developer](../../vision/TARGET-USERS.md#aiml-application-developers).

## Positioning

Cretes aims first to be an excellent language for **building applications that use AI/ML**, and for **interoperating with established AI/ML frameworks and runtimes**. Typical applications include:

- inference services;
- data preprocessing pipelines;
- agents and tools that call models;
- edge deployments;
- glue code around native inference engines.

Cretes does **not** aim to replace established training frameworks such as PyTorch, TensorFlow or JAX, or their model ecosystems ([NON-GOALS.md](../NON-GOALS.md)). Whether first-party training capabilities are ever pursued is a long-term question, not a Phase 1 commitment.

> **Future accelerator work is not designed.** GPU and other accelerator support below is labeled **future architecture**. No vendor-specific programming model, including CUDA, is a language-level concept in Phase 1. Phase 2 must only ensure the architecture does not preclude accelerator support ([P2Q-019](../../PHASE-2-OPEN-QUESTIONS.md#p2q-019--numerical-and-accelerator-architecture)).

Terminology, layers and targets are defined in the [requirements framework](../README.md).

## Contents

- [Layer allocation](#layer-allocation)
- [Language requirements](#language-requirements)
- [Standard-library requirements](#standard-library-requirements)
- [Interoperability and inference](#interoperability-and-inference)
- [Data handling](#data-handling)
- [Execution targets](#execution-targets)
- [Ecosystem](#ecosystem)

## Layer allocation

| Layer | AI/ML responsibilities |
| --- | --- |
| Language | Numeric primitives with exact semantics, packed value layout, parallel-safe data access, notation for numeric code. |
| Runtime | Parallel execution on CPU cores. Future: device memory spaces. |
| Standard library | Contiguous arrays, buffer views, alignment, memory-mapped files, SIMD primitives. |
| First-party library | N-dimensional arrays and tensor layout descriptors, inference-runtime bindings (decided in Phase 2+). |
| Ecosystem | Model formats, tokenizers, image and audio codecs, dataframes, hosted-model API clients, framework bindings. |

## Language requirements

### AI-001 — Exact numeric semantics

- **Priority:** MUST · **Layer:** Language · **Target:** v0.1
- **Requirement:** Floating-point types must follow IEEE 754 semantics for their operations. This covers NaN and infinities, signed zero and round-to-nearest-even by default. Any permitted deviation, such as fused multiply-add contraction or relaxed-precision modes, must be explicit and opt-in.
- **Rationale:** Numerical reproducibility and cross-platform consistency ([CORE-026](../CORE.md#core-026--platform-independent-semantics)).
- **Verification:** Conformance tests under Platform CI.

### AI-002 — Reduced-precision numeric types

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Cretes should support 16-bit IEEE binary16 and bfloat16 values, at least as storage types with conversion. It should also support 8-bit integer types suitable for quantized model data.
- **Rationale:** Modern inference relies on reduced-precision weights and activations.
- **Verification:** Conformance tests.

### AI-003 — Packed value layout

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Arrays of primitive values and of user-defined value aggregates must be storable contiguously, element after element, without per-element indirection or headers ([PERF-011](../PERFORMANCE.md#perf-011--allocation-free-values)).
- **Rationale:** Numerical performance and zero-copy interop depend on dense layout.
- **Verification:** Design review; Integration tests inspecting layout.

### AI-004 — Readable numerical notation

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Numerical code on library-defined numeric types, such as vectors, matrices and complex numbers, should be expressible in notation close to its mathematical form. The mechanism, such as operator overloading, is a Phase 2+ decision.
- **Rationale:** Readability of numerical code reduces errors. The mechanism must be balanced against [Principle 10](../../principles/DESIGN-PRINCIPLES.md#10-consistency-over-excessive-syntax).
- **Verification:** Design review.

## Standard-library requirements

### AI-005 — Contiguous arrays

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** The standard library must provide fixed-size and growable one-dimensional arrays whose elements are stored contiguously. Their layout must be documented, and they must provide bounds-checked access. For v0.1 this is satisfied by the growable sequence of [CORE-033](../CORE.md#core-033--core-collections), provided that it guarantees contiguous storage of primitive elements.
- **Rationale:** The building block for all numerical data.
- **Verification:** Unit tests.

### AI-006 — Buffer views

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Programs must be able to create non-owning, bounds-checked views of sub-ranges of contiguous memory without copying. Views must not be able to outlive or invalidate the underlying storage in safe code ([SAFE-003](../SAFETY.md#safe-003--temporal-memory-safety)).
- **Rationale:** Batching, windowing and parsing operate on slices of large buffers.
- **Verification:** Conformance tests; Unit tests.

### AI-007 — Multidimensional arrays

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes should provide an n-dimensional array abstraction with:
  - element type, shape and strides;
  - row-major and column-major layouts;
  - views such as slicing, transposition and reshaping, without copying where possible;
  - element-wise operations with bounds safety.
- **Rationale:** Tensors are the lingua franca of AI/ML data.
- **Verification:** Unit tests; Benchmark (`numerical/`).

### AI-009 — Alignment control

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Programs must be able to allocate buffers with specified alignment and to query the alignment of existing buffers.
- **Rationale:** SIMD instructions, DMA and many native runtimes require specific alignment.
- **Verification:** Unit tests.

### AI-010 — Vectorized computation

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Cretes should support vectorized computation through both of the following:
  - compiler optimization of straightforward loops over contiguous data;
  - an explicit, portable SIMD interface with a documented fallback on platforms that lack particular instructions.
- **Rationale:** Vector units provide large speedups for preprocessing and CPU inference kernels ([PERF-015](../PERFORMANCE.md#perf-015--numerical-throughput)).
- **Verification:** Benchmark (`numerical/`); Unit tests under Platform CI.

### AI-011 — Parallel numerical computation

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Cretes should provide data-parallel operations over arrays, such as parallel map, reduction and chunked iteration. They should use the concurrency model ([CONC-003](../CONCURRENCY.md#conc-003--parallel-execution)) and be free of data races in safe code ([SAFE-012](../SAFETY.md#safe-012--data-race-freedom)).
- **Rationale:** Using all CPU cores is the first step in accelerating numerical work.
- **Verification:** Unit tests; Benchmark (`numerical/`).

## Interoperability and inference

### AI-008 — Tensor-compatible layout descriptors

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes must be able to describe a buffer's element type, shape, strides, alignment and memory location in a form that can be converted to and from widely used exchange conventions. Examples are DLPack, the NumPy array interface and the Apache Arrow columnar format. Conversion must not copy data when layouts are compatible.
- **Rationale:** Zero-copy exchange with existing runtimes is the core of Cretes' AI/ML interop strategy ([INTOP-012](../INTEROPERABILITY.md#intop-012--ai-runtime-integration)).
- **Verification:** Integration tests.

### AI-012 — Model inference through established runtimes

- **Priority:** MUST · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** Cretes programs must be able to run inference through established inference runtimes that expose C APIs ([INTOP-001](../INTEROPERABILITY.md#intop-001--calling-c-abi-functions)), passing input and output tensors without unnecessary copies. The ownership of memory shared with the runtime must be explicit ([INTOP-005](../INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary)).
- **Rationale:** Inference is the most common AI capability in applications. Established runtimes already provide optimized kernels.
- **Verification:** Integration tests.

### AI-013 — First-party inference bindings

- **Priority:** SHOULD · **Layer:** First-party library · **Target:** Post-v0.1
- **Requirement:** The project should maintain safe bindings to at least one widely used, openly licensed inference runtime. Which runtime is a later decision, based on licensing, portability and C-API stability.
- **Rationale:** A maintained reference integration demonstrates the interop story and sets the pattern for others.
- **Verification:** Integration tests under Platform CI.

### AI-023 — Hosted-model API clients

- **Priority:** SHOULD · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** The networking foundation should make it straightforward to build clients for hosted model APIs. This includes streaming responses, for example server-sent events over HTTP ([NET-018](networking.md#net-018--http-client)), and handling credentials safely ([SEC-017](cybersecurity.md#sec-017--key-and-credential-handling)).
- **Rationale:** Many AI applications consume hosted models over HTTP rather than running inference locally.
- **Verification:** Integration tests (example client).

## Data handling

### AI-014 — Memory-efficient data handling

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must support memory-mapped file access through a safe interface. Where safety cannot be guaranteed, for example with concurrent external modification, the operation must be unsafe or documented as such. The standard library must also support streaming, chunked processing of datasets larger than memory.
- **Rationale:** Models and datasets are frequently larger than comfortable RAM budgets.
- **Verification:** Unit tests; Security review.

### AI-015 — Data preprocessing

- **Priority:** SHOULD · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** The standard and first-party libraries should provide the primitives that preprocessing libraries need. These include efficient text and byte processing, JSON ([AUTO-016](automation.md#auto-016--json)), CSV reading and conversion between numeric types. Specialized preprocessing, such as tokenizers and image and audio decoding, is expected from the ecosystem.
- **Rationale:** Preprocessing is where much AI application code is written.
- **Verification:** Unit tests.

### AI-016 — Tensor and model serialization

- **Priority:** SHOULD · **Layer:** Ecosystem · **Target:** Post-v0.1
- **Requirement:** It should be possible to read and write common tensor and model storage formats that do not embed executable code, using memory-mapping where the format allows. The safetensors and NumPy `.npy` formats are examples.
- **Rationale:** Applications must load model weights and datasets produced by established tools.
- **Verification:** Integration tests; Fuzzing.

### AI-017 — Safe model and data loading

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Standard and first-party libraries must not provide deserialization that can execute code, or instantiate arbitrary types, chosen by the input data. An example of such deserialization is Python-pickle-style object loading. Loaders must validate declared sizes against actual data and resource limits ([SEC-021](cybersecurity.md#sec-021--resource-limits-for-untrusted-input)).
- **Rationale:** Malicious model files are a real supply-chain attack vector.
- **Verification:** Security review; Fuzzing.

### AI-022 — Reproducible numerical results

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Parallel and vectorized numerical operations should offer a mode with deterministic results across runs on the same platform, for example with a fixed reduction order. They should document when results may differ.
- **Rationale:** Debugging and testing numerical pipelines requires reproducibility.
- **Verification:** Unit tests.

## Execution targets

### AI-018 — CPU execution first

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Every numerical facility in this document must work on the CPU on all supported platforms. Accelerator support must be an addition, never a prerequisite.
- **Rationale:** Portability, testability and a reliable baseline everywhere.
- **Verification:** Unit tests under Platform CI.

### AI-019 — Accelerator-ready architecture (future architecture)

- **Priority:** MAY · **Layer:** Language · **Target:** Long-term
- **Requirement:** The Phase 2 design of buffers and memory should record whether it can later express memory residing in distinct memory spaces, such as device memory, and asynchronous transfer between them. It should not require vendor-specific concepts.
- **Rationale:** Keeps future accelerator support possible without committing to a design now.
- **Verification:** Design review.

### AI-020 — GPU support through interop (future architecture)

- **Priority:** MAY · **Layer:** Ecosystem · **Target:** Long-term
- **Requirement:** GPU computation may be supported through libraries that bind vendor or cross-vendor compute APIs, such as CUDA, ROCm/HIP, Metal, Vulkan compute, SYCL or OpenCL, using the FFI. No such API is a language-level concept.
- **Rationale:** Enables GPU use without coupling the language to one vendor.
- **Verification:** Integration tests (when pursued).

### AI-021 — Heterogeneous compute (future architecture)

- **Priority:** MAY · **Layer:** Language · **Target:** Exploratory
- **Requirement:** Language-level support for writing kernels that run on accelerators, or for heterogeneous scheduling across CPU and accelerator devices, may be explored in the future through RFCs.
- **Rationale:** A long-term research direction, only after CPU and interop foundations are proven.
- **Verification:** Inspection (research RFC).

## Ecosystem

Expected from the ecosystem, not the Cretes project:

- dataframes;
- tokenizers;
- image, audio and video codecs;
- model-format converters;
- bindings to training frameworks;
- experiment tracking;
- vector-database clients;
- higher-level agent frameworks.

## Related documents

- [Interoperability requirements](../INTEROPERABILITY.md)
- [Performance requirements](../PERFORMANCE.md)
- [Concurrency requirements](../CONCURRENCY.md)
- [Non-goals](../NON-GOALS.md)
