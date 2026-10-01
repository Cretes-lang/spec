# Phase 2 question disposition

The Phase 1 question register is preserved as historical input. None of its questions is marked resolved before RFC acceptance. This table records proposed answers and explicitly deferred details. No grammar work is performed here.

| Question | Architectural response | Current disposition |
| --- | --- | --- |
| [P2Q-001 — Static, dynamic or gradual typing](../PHASE-2-OPEN-QUESTIONS.md#p2q-001--static-dynamic-or-gradual-typing) | [ARCH-TYPE-001](TYPE.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-002 — Type inference scope](../PHASE-2-OPEN-QUESTIONS.md#p2q-002--type-inference-scope) | [ARCH-TYPE-001](TYPE.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-003 — Generics model](../PHASE-2-OPEN-QUESTIONS.md#p2q-003--generics-model) | [ARCH-TYPE-001](TYPE.md) | PROPOSED strategy; generic coherence/details DEFERRED |
| [P2Q-004 — Memory-management architecture](../PHASE-2-OPEN-QUESTIONS.md#p2q-004--memory-management-architecture) | [ARCH-MEM-001](MEM.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-005 — Mutability, aliasing and ownership model](../PHASE-2-OPEN-QUESTIONS.md#p2q-005--mutability-aliasing-and-ownership-model) | [ARCH-MEM-001](MEM.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-006 — Value and reference semantics](../PHASE-2-OPEN-QUESTIONS.md#p2q-006--value-and-reference-semantics) | [ARCH-MEM-001](MEM.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-007 — Error model](../PHASE-2-OPEN-QUESTIONS.md#p2q-007--error-model) | [ARCH-ERROR-001](ERROR.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-008 — Nullability representation](../PHASE-2-OPEN-QUESTIONS.md#p2q-008--nullability-representation) | [ARCH-NULL-001](NULL.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-009 — Default integer overflow behavior](../PHASE-2-OPEN-QUESTIONS.md#p2q-009--default-integer-overflow-behavior) | [ARCH-TYPE-001](TYPE.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-010 — Execution model and backend](../PHASE-2-OPEN-QUESTIONS.md#p2q-010--execution-model-and-backend) | [ARCH-EXEC-001](EXEC.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-011 — Concurrency runtime architecture](../PHASE-2-OPEN-QUESTIONS.md#p2q-011--concurrency-runtime-architecture) | [ARCH-CONC-001](CONC.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-012 — Asynchronous execution model and API coloring](../PHASE-2-OPEN-QUESTIONS.md#p2q-012--asynchronous-execution-model-and-api-coloring) | [ARCH-ASYNC-001](ASYNC.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-013 — FFI architecture](../PHASE-2-OPEN-QUESTIONS.md#p2q-013--ffi-architecture) | [ARCH-FFI-001](FFI.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-014 — ABI stability policy](../PHASE-2-OPEN-QUESTIONS.md#p2q-014--abi-stability-policy) | [ARCH-COMPAT-001](COMPAT.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-015 — Debug information strategy](../PHASE-2-OPEN-QUESTIONS.md#p2q-015--debug-information-strategy) | [ARCH-DEBUG-001](DEBUG.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-016 — Package and build architecture](../PHASE-2-OPEN-QUESTIONS.md#p2q-016--package-and-build-architecture) | [ARCH-BUILD-001](BUILD.md) | PROPOSED boundaries; manifest/lock/resolver/registry formats DEFERRED |
| [P2Q-017 — Standard-library scope and first-party packages](../PHASE-2-OPEN-QUESTIONS.md#p2q-017--standard-library-scope-and-first-party-packages) | [ARCH-RUNTIME-001](RUNTIME.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-018 — Cryptography and TLS implementation strategy](../PHASE-2-OPEN-QUESTIONS.md#p2q-018--cryptography-and-tls-implementation-strategy) | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) | PROPOSED provider boundary; provider selection DEFERRED |
| [P2Q-019 — Numerical and accelerator architecture](../PHASE-2-OPEN-QUESTIONS.md#p2q-019--numerical-and-accelerator-architecture) | [ARCH-AI-001](AI.md) | PROPOSED CPU/buffer boundary; accelerator contracts DEFERRED |
| [P2Q-020 — Constant-time code and compiler guarantees](../PHASE-2-OPEN-QUESTIONS.md#p2q-020--constant-time-code-and-compiler-guarantees) | [ARCH-SECURITY-DOMAIN-001](SECURITY-DOMAIN.md) | PROPOSED scoped provider guarantee; primitive assurance DEFERRED |
| [P2Q-021 — Secret lifetime under the memory model](../PHASE-2-OPEN-QUESTIONS.md#p2q-021--secret-lifetime-under-the-memory-model) | [ARCH-MEM-001](MEM.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-022 — Intermediate representation](../PHASE-2-OPEN-QUESTIONS.md#p2q-022--intermediate-representation) | [ARCH-IR-001](IR.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-023 — Implementation language and bootstrapping](../PHASE-2-OPEN-QUESTIONS.md#p2q-023--implementation-language-and-bootstrapping) | [ARCH-COMPILER-001](COMPILER.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-024 — Unsafe-code model](../PHASE-2-OPEN-QUESTIONS.md#p2q-024--unsafe-code-model) | [ARCH-SAFETY-001](SAFETY.md) | PROPOSED boundary; user-facing unsafe specification post-v0.1 |
| [P2Q-025 — Compile-time code execution and metaprogramming](../PHASE-2-OPEN-QUESTIONS.md#p2q-025--compile-time-code-execution-and-metaprogramming) | [ARCH-MODULE-001](MODULE.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-026 — Module and package identity](../PHASE-2-OPEN-QUESTIONS.md#p2q-026--module-and-package-identity) | [ARCH-MODULE-001](MODULE.md) | PROPOSED; awaiting RFC acceptance |
| [P2Q-027 — Syntax design process](../PHASE-2-OPEN-QUESTIONS.md#p2q-027--syntax-design-process) | [ARCH-REVIEW-001](REVIEW.md) | DEFERRED to Phase 3 after acceptance; process documented |
| [P2Q-028 — Specification method and conformance suite](../PHASE-2-OPEN-QUESTIONS.md#p2q-028--specification-method-and-conformance-suite) | [ARCH-COMPAT-001](COMPAT.md) | PROPOSED specification/conformance method |
