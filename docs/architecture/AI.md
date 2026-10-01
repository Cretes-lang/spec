# 2.24 — AI/ML architecture

> Decision: **ARCH-AI-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AI-001](../requirements/domains/ai-ml.md#ai-001--exact-numeric-semantics), [AI-002](../requirements/domains/ai-ml.md#ai-002--reduced-precision-numeric-types), [AI-003](../requirements/domains/ai-ml.md#ai-003--packed-value-layout), [AI-004](../requirements/domains/ai-ml.md#ai-004--readable-numerical-notation), [AI-005](../requirements/domains/ai-ml.md#ai-005--contiguous-arrays), [AI-006](../requirements/domains/ai-ml.md#ai-006--buffer-views), [AI-007](../requirements/domains/ai-ml.md#ai-007--multidimensional-arrays), [AI-008](../requirements/domains/ai-ml.md#ai-008--tensor-compatible-layout-descriptors), [AI-009](../requirements/domains/ai-ml.md#ai-009--alignment-control), [AI-010](../requirements/domains/ai-ml.md#ai-010--vectorized-computation), [AI-011](../requirements/domains/ai-ml.md#ai-011--parallel-numerical-computation), [AI-012](../requirements/domains/ai-ml.md#ai-012--model-inference-through-established-runtimes), [AI-013](../requirements/domains/ai-ml.md#ai-013--first-party-inference-bindings), [AI-014](../requirements/domains/ai-ml.md#ai-014--memory-efficient-data-handling), [AI-015](../requirements/domains/ai-ml.md#ai-015--data-preprocessing), [AI-016](../requirements/domains/ai-ml.md#ai-016--tensor-and-model-serialization), [AI-017](../requirements/domains/ai-ml.md#ai-017--safe-model-and-data-loading), [AI-018](../requirements/domains/ai-ml.md#ai-018--cpu-execution-first), [AI-019](../requirements/domains/ai-ml.md#ai-019--accelerator-ready-architecture-future-architecture), [AI-020](../requirements/domains/ai-ml.md#ai-020--gpu-support-through-interop-future-architecture), [AI-021](../requirements/domains/ai-ml.md#ai-021--heterogeneous-compute-future-architecture), [AI-022](../requirements/domains/ai-ml.md#ai-022--reproducible-numerical-results), [AI-023](../requirements/domains/ai-ml.md#ai-023--hosted-model-api-clients), [PERF-015](../requirements/PERFORMANCE.md#perf-015--numerical-throughput)

## Proposed decision and rationale

**CPU-first contiguous data and provider-neutral native runtime adapters; tensor/accelerator facilities remain libraries.**

v0.1 contributes exact binary32/binary64 semantics and contiguous growable sequences. Later numerical libraries add typed strided tensor views with element type, dimensions, byte strides, alignment, address space and ownership/deleter contract. Validate dimension products and offset arithmetic for overflow before access. A view cannot outlive its owner or permit mutation through overlapping aliases without an explicit safe policy.

Packed records and arrays avoid per-element boxing. Alignment requests are validated against allocator and target support. SIMD/vectorization use backend capabilities through typed operations with scalar fallbacks; reduced-precision types require specified rounding/conversion before exposure. Numerical notation is a Phase 3 concern. Parallel operations use the same task/transfer architecture; BLAS or inference libraries may use their own threads, so adapters document and control oversubscription.

Native wrappers may integrate BLAS and ONNX Runtime through versioned C interfaces. They validate shapes, data types, retained buffers, session lifetimes and provider errors. Zero-copy is conditional on exact layout, ownership and synchronization compatibility; adapters otherwise make a visible copy. CPU execution is the default. Device memory uses explicit address-space/device/context identity and completion events; no mandatory CUDA dependency or core GPU syntax is introduced.

Streaming preprocessing uses shared stream/error abstractions and bounded batches. Memory mapping is exposed safely only when the wrapper can maintain validity despite external file changes; otherwise use a copied buffer or explicit unsafe boundary. Model/tensor loaders parse data only, validate lengths and resource budgets, and never execute embedded source/plugins by default. Hosted-model clients are ordinary authenticated HTTP packages with redaction and timeouts.

Reproducibility records hardware, provider/version, precision, seeds, thread settings and algorithm choices. Parallel reductions and provider kernels can differ; bitwise cross-device reproducibility is not asserted.

## Options, advantages, disadvantages and rejected alternatives

A compiler-integrated AI framework was rejected by non-goals. Vendor-specific accelerator semantics were rejected as mandatory language features. Universal boxed numerical objects were rejected for layout/interop cost. Typed contiguous buffers plus library adapters are proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: untrusted models and native providers remain attack surfaces; limit resources and validate contracts. Performance: copies, alignment and thread oversubscription dominate some workloads; measure them. DX: data APIs share ordinary collections/errors rather than requiring a separate language. Implementation: later tensor descriptors, adapters and CPU fallback tests.

## Future verification

Later test shape/stride overflow, aliasing, retained native buffers, malformed models, copy-vs-zero-copy equivalence, provider failures and numerical reproducibility metadata.

## Risks and open questions

Provider package selection, tensor API, reduced precision and accelerator execution contracts are DEFERRED. Architecture reserves extension points without promising those features for v0.1.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
