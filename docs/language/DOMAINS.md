# Four-domain surface review

Status: NON-NORMATIVE self-review, 2026-10-02. [Examples](EXAMPLES.md).

| Domain | Candidate fixture | Finding | Deferred coverage |
| --- | --- | --- | --- |
| Automation | 11-automation.cretes | Synchronous read/write plus ? expresses a file operation with explicit failures; helper owns cleanup, avoiding lifetime annotations in the common case | Processes, shell invocation, HTTP, recursive jobs and scheduling are post-v0.1 |
| Networking | 12-packet-validation.cretes | Bytes and checked indexing support bounded header inspection; an error sum distinguishes malformed data | Connections, async I/O, backpressure, cancellation and concurrent servers need later syntax/runtime RFCs |
| AI/ML | 13-numeric-preprocessing.cretes | Fixed numeric types, Seq and borrowed iteration express CPU preprocessing without ownership transfer of input | Tensor shapes, user generics, inference runtimes, native adapters and accelerators remain later facilities |
| Cybersecurity | 14-defensive-bytes.cretes | Length checks precede index access and no raw pointer/implicit conversion is needed | Crypto, secret buffers, constant-time operations, native boundaries and provider assurance remain later gates |

Automation readability: the common example is seven lines of code plus spacing; its complexity is mostly a visible Result return. Literal filesystem paths are teaching data. Error detail is preserved instead of converted to a boolean. The helper contracts still require a library design review.

Networking review: parser-oriented synchronous validation is within scope. A fake `async fn` example would not demonstrate an approved v0.1 feature. Future connection examples must prove task ownership, deadline propagation, terminal I/O completion and join-before-drop; those are explicit acceptance criteria for that later work.

AI review: left-to-right accumulation follows the architecture, so reassociation/parallel reduction is not silently permitted. Empty collections need annotations; concrete numeric types avoid hidden boxing. User generic abstractions and foreign acceleration are not needed to make this syntax fixture parse.

Security review: rejecting raw deceptive controls protects source display; bounds-first examples do not prove a future implementation memory-safe. The bytes example is a defensive format check, not a cryptographic authenticity test. No native/crypto API is implemented or claimed audited.

Conclusion of this review: the synchronous surface is expressible and internally consistent in these small examples. Real usability, performance and comprehensive domain support require implementation and later domain milestones. These samples do not satisfy every long-term domain requirement.
