# Evidence and source notes

Sources consulted on 2026-09-27. These are primary project documents used to check feasibility and known tradeoffs. They do not establish measured Cretes performance or prove its proposed safety model. Cretes design choices are inferences from its requirements and the qualitative comparisons, not endorsements by these projects.

| Source | Fact informing review | Cretes consequence |
| --- | --- | --- |
| [LLVM language reference](https://llvm.org/docs/LangRef.html) | Backend IR has poison/undefined-behavior preconditions | Checked arithmetic and careful attribute emission must preserve Cretes behavior |
| [LLVM source-level debugging](https://llvm.org/docs/SourceLevelDebugging.html) | Source/type metadata maps frontend concepts into codegen | Retain origin/type information through HIR and MIR |
| [LLVM developer policy](https://llvm.org/docs/DeveloperPolicy.html) | Project license includes LLVM exceptions and legacy components | Audit the exact shipped dependency inventory; do not assume one blanket notice |
| [Cranelift](https://cranelift.dev/) | General native backend emphasizing compilation speed and correctness, with a different optimization stance | Keep it a future measured alternative; do not claim Cretes benchmark comparisons |
| [Go GC guide](https://go.dev/doc/gc-guide) | Tracing GC entails CPU/memory/latency tradeoffs | Evaluate collector overhead and resource cleanup separately |
| [Rust ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html) | Ownership tracks memory responsibility through checked rules | Evidence that static ownership is feasible, not proof that this proposal is sound |
| [Rust references and borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html) | Aliasing/mutation restrictions contribute to data-race prevention | Cretes needs explicit transfer/share rules in addition to scoped loans |
| [Rust destructors](https://doc.rust-lang.org/reference/destructors.html) | Aborting termination does not guarantee destructors | State fault-cleanup limitations explicitly |
| [libuv design](https://docs.libuv.org/en/v1.x/design.html) | Platforms use different I/O mechanisms and handle/request lifetimes | Cancellation cannot release a buffer before terminal completion |
| [ONNX Runtime C API](https://onnxruntime.ai/docs/api/c/struct_ort_api.html) | Native inference is accessible through a C API | Library adapters can provide interop without a compiler-integrated ML framework |

No third-party source text or implementation is copied into this proposal. Backend/provider versions are not selected or installed here. Formal API/ABI validation and dependency licensing checks must use the exact version eventually chosen.
