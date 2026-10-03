# Candidate example corpus

All examples are **NON-NORMATIVE, UNIMPLEMENTED**. Their syntax is recognized by the experimental grammar tool. This is not execution or type-checker evidence. Library-only files deliberately have no main.

| File | Purpose | Conceptual result |
| --- | --- | --- |
| [01-hello-world.cretes](01-hello-world.cretes) | canonical greeting, explicit I/O errors | greeting plus LF, exit 0; error exit 1 |
| [02-variables.cretes](02-variables.cretes) | const, let, var, assignment | count becomes 12 |
| [03-functions.cretes](03-functions.cretes) | annotated positional functions | computes 42 |
| [04-conditionals.cretes](04-conditionals.cretes) | library sign function | -1, 0 or 1 |
| [05-loops.cretes](05-loops.cretes) | for/while/loop and control exits | total returns 6 |
| [06-collections.cretes](06-collections.cretes) | Seq/Map/Set construction and borrowing | four sequence elements, empty map/set |
| [07-user-types.cretes](07-user-types.cretes) | record, alias, sum and exhaustive match | handles both variants |
| [08-errors.cretes](08-errors.cretes) | Result propagation and Option handling | nonnegative path returns Ok(0) |
| [09-modules.cretes](09-modules.cretes) | exported library function | demo::math identity, twice operation |
| [10-borrowing.cretes](10-borrowing.cretes) | mutable argument and return provenance | count becomes 1; view stays within owner |
| [11-automation.cretes](11-automation.cretes) | file copy through conceptual helpers | copies bytes or returns I/O error |
| [12-packet-validation.cretes](12-packet-validation.cretes) | synchronous packet header validation | typed truncation/version errors |
| [13-numeric-preprocessing.cretes](13-numeric-preprocessing.cretes) | sequential CPU numeric reduction | left-to-right f64 additions |
| [14-defensive-bytes.cretes](14-defensive-bytes.cretes) | bounds-first magic check | true for initial bytes 0x43,0x52 |

There is deliberately no concurrency `.cretes` example: ARCH-CONC-001 excludes concurrency from v0.1. File 10 demonstrates supported borrowing instead. Async, FFI, generic functions and methods are neither silently implemented nor illustrated as accepted syntax.

## Conceptual standard API contracts

These contracts make the examples reviewable, but **do not freeze a standard-library API**. A later library specification must record allocation, failure and OS details before executing them. No referenced module exists as a delivered implementation.

| Name | Assumed contract for illustration |
| --- | --- |
| io::println | consumes text; returns Result[(),io::Error]; writes text and LF; reports output failure |
| seq::push | exclusive Seq[T] reference plus owned T; returns unit; ordinary allocation failure follows defined fault path |
| map::empty / set::empty | no arguments; returns inferred empty Map[K,V] / Set[T]; type context mandatory |
| bytes::len | shared Bytes reference; returns usize, no mutation |
| fs::read_bytes | consumes text path convenience input; returns Result[Bytes,fs::Error]; conversion to native Path must be explicit inside the helper and fail on unrepresentable input |
| fs::write_bytes | text path plus shared Bytes reference; returns Result[(),fs::Error]; owns/finishes resources internally and reports write/close failures |

The path convenience contract does not replace the required lossless Path abstraction. Production APIs must support native paths that cannot be represented in text. File copy examples use fixed teaching filenames; they are not instructions to run against user files.

## Canonical Hello World explanation

`import std::io;` resolves a module without executing it. `fn main() -> Result[i32, io::Error]` exposes entry success/failure. The body calls println once, then `?` either produces unit or returns the exact error type. `Result::Ok(0)` requests successful exit. It uses only the declared import/function/type/call/propagation/return productions. No macro, interpolation, async runtime or implicit I/O exception is assumed.

## Conformance fixture classes

[fixtures.json](fixtures.json) stores valid syntax, invalid syntax, invalid lexical input and **semantic-negative** cases. Semantic-negative sources MUST parse and MUST later fail type/ownership/context checking for the stated reason. The current recognizer intentionally cannot assert those future semantic failures. Examples are reviewed by hand against the prose; this is self-review, not independent approval.
