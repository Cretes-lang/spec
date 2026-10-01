# Risks, deferred decisions and release gates

> Status: OPEN review register · Date: 2026-09-27

Ownership of each item is the current project lead until a qualified maintainer explicitly accepts it. This does not imply a staffed compiler or security team. Phase 2 architecture approval and later implementation readiness are separate gates.

| ID | Risk or deferred choice | Owner role | Required closure evidence | Gate |
| --- | --- | --- | --- | --- |
| R-01 | Ownership is too difficult for automation personas | Lead / language design | File-copy, log-filter and error-propagation walkthroughs; diagnostic examples; revise RFC if goals fail | Architecture review, then usability validation |
| R-02 | Borrow/move analysis is unsound or underspecified | Lead / compiler | Precise transfer/reborrow/join rules, negative conformance cases and expert review | Before compiler safety claim |
| R-03 | Destruction cascades, allocator work or blocking calls harm latency | Lead / runtime | Tail-latency/allocation measurements, documented bounds/mitigations | Before latency-sensitive milestone |
| R-04 | Backend lowering introduces poison/undefined behavior | Lead / backend | Checked-operation lowering tests across profiles and targets | Every release |
| R-05 | Stack/heap exhaustion corrupts state | Lead / platform | Stack probing/guard and allocation-independent fault tests per target | Before target support |
| R-06 | Async cancellation frees an in-use buffer | Lead / runtime | Terminal completion state-machine review and race/fault tests | Before async delivery |
| R-07 | Transfer/shared-state capabilities fail data-race freedom | Lead / language/runtime | Formal happens-before/atomic contract and compile-fail/runtime tests | Before concurrency delivery |
| R-08 | FFI wrappers trust invalid native contracts | Lead / interop | Per-provider ownership/layout/callback audit and C fixtures | Before FFI/provider delivery |
| R-09 | Crypto/TLS provider and constant-time scope not selected | Lead / security | Dedicated provider RFC, maintenance/license inventory, test vectors and expert security assessment | DEFERRED; before crypto/TLS delivery |
| R-10 | Zeroization cannot erase copies outside controlled storage | Lead / security | Explicit guarantee scope, optimized-code inspection, provider/OS constraints | Before secret API guarantees |
| R-11 | Manifest format/filename and lock/resolver protocol unspecified | Lead / toolchain | Schema/format RFC with compatibility/security fixtures | Manifest before v0.1 implementation; remote graph later |
| R-12 | Registry authenticity/provenance/revocation model unspecified | Lead / ecosystem | Threat model, trust roots, account recovery and namespace policy | DEFERRED; before registry delivery |
| R-13 | Target versions/SDKs are untested | Lead / platform | CI/release baseline, minimum OS, license/provenance and installation tests | Before claiming supported targets |
| R-14 | Generic code size, coherence and dispatch details | Lead / types | Follow-up RFC with examples and measurements | DEFERRED; before user generics |
| R-15 | Accelerator/tensor/provider interfaces | Lead / AI interop | Ownership/completion/layout contracts and CPU fallback | DEFERRED; after v0.1 |
| R-16 | Reproducibility claim exceeds actual evidence | Lead / release | Rebuild comparison including native dependencies, paths and timestamps | Before bit-for-bit claim |
| R-17 | RFC elapsed review gate not met | Project lead | Public review, at least seven calendar days final comment, objections and dated decision | Phase 2 closure |

No research spike was executed. The current qualitative proposal does not depend on invented benchmark results. If review cannot resolve a choice without experimentation, create an isolated, removable spike with one question and publish actual results before claiming that question settled.

## Phase 2 closure checklist

- [x] Sections 2.1–2.30 have proposed decisions, alternatives and consequences.
- [x] All 257 requirements, including 173 MUSTs, have proposed response mappings.
- [x] All 28 Phase 1 architecture questions have a proposed/deferred disposition.
- [x] v0.1 remains the original 86-requirement subset.
- [x] Language/compiler/security/performance/developer-experience self-review is recorded.
- [ ] Public RFC review and final-comment period completed.
- [ ] Objections addressed and dated maintainer outcome recorded.
- [ ] Accepted statuses and resolved-question links updated after that outcome.

Implementation tests, provider audits and target support tests are later gates, not tests falsely marked passed by this checklist. Phase 3 and production implementation have not started.
