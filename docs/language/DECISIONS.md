# Syntax decision record

Status: **PROPOSED**, 2026-10-02. All selections below are conditional on Phase 2 acceptance and the syntax RFC. They are not accepted design decisions.

[Reference](SPEC.md) · [Review](REVIEW.md)

| Family | Alternatives evaluated | Selection and rationale | Architecture source | Parser, tooling and teaching consequence |
| --- | --- | --- | --- | --- |
| Encoding | UTF-8, locale-dependent text, UTF-16 | Strict UTF-8, original byte spans; portable input and stable diagnostics | ARCH-PIPELINE-001 | One decoding policy; editor coordinate conversion remains explicit |
| Block structure | indentation, braces, begin/end | Braces and required statement semicolons; robust copying/generated code and no newline insertion rules | ARCH-PIPELINE-001 | Small lookahead; beginners learn punctuation once |
| Identifiers | Unicode XID with versioned tables, ASCII initial subset | ASCII names initially, Unicode literal/comment data; avoids silent normalization and dependency on mutable Unicode tables | ARCH-DIAGNOSTIC-001 | Less international naming flexibility; explicit diagnostics; later RFC may extend |
| Comments | # lines, // lines, nonnested/nested blocks | //, /// docs, nested /* */; no conflict with attributes or shell launcher | ARCH-PIPELINE-001 | Stateful comment lexer; formatter preserves trivia |
| Literals | suffix types, constructor types, contextual literals | Contextual integers/floats with explicit annotations; base prefixes and strict separators | ARCH-TYPE-001 | Lexing independent from type inference; overflow is a semantic check |
| Type names | Int64/UInt64, int/float target dependence, fixed-width short names | i8–i64/u8–u64/f32/f64, explicit usize, text/char/Bytes | ARCH-TYPE-001 | Compact numerical code without hidden width; text and bytes stay distinct |
| Type arguments | angle brackets, square brackets, parentheses | Built-in constructors use [T]; expression brackets remain index/sequence contexts | ARCH-TYPE-001 | No > versus >> splitting; user generics still deferred |
| Bindings | let plus modifier, implicit declarations, let/var | let immutable, var mutable, const compile-time; keywords expose the distinction | ARCH-TYPE-001, ARCH-MEM-001 | Slightly larger inventory; straightforward completion and diagnostics |
| Functions | function, fun, fn, arrow-only definitions | fn with colon parameter types and mandatory -> return; terse but structurally explicit | ARCH-TYPE-001 | Uniform public/private contracts; locals remain inferred; no accidental callable ABI |
| Return values | tail expressions, return statement, expression bodies | Explicit return, statements in blocks; a single model for early exits/cleanup | ARCH-RESOURCE-001 | More words, fewer value/statement ambiguities |
| Operators | word-based logic, punctuation logic, custom operators | Fixed familiar punctuation tiers, no overloads; typed operands and mandatory safety | ARCH-TYPE-001, ARCH-SAFETY-001 | Published precedence; chain comparisons rejected; parentheses recommended for mixed bitwise/comparison |
| Assignment | expression assignment, statement assignment | Statement-only =; excludes accidental assignment in conditions | ARCH-SAFETY-001 | Semantic writable-place check after syntax recognition |
| Records | bare Type {…}, Type(…), new Type {…} | new marker plus named fields; separates construction from if/while block | ARCH-TYPE-001 | One keyword buys unambiguous control parsing; no constructor method system |
| Sums/patterns | integer tags, switch, exhaustive match | Tagged enum and statement match; qualified constructors with parentheses even when nullary | ARCH-TYPE-001, ARCH-NULL-001 | Uniform sum/error/absence extraction; no bare-name constant-pattern ambiguity |
| Borrowing | automatic address taking, view keywords, & / &mut | Explicit checked & and &mut, * dereference, from parameter for returned loans | ARCH-MEM-001 | Visible alias permissions; one provenance source per return keeps first checker tractable |
| Errors | exceptions, explicit match everywhere, postfix propagation | Result plus ? and exhaustive match; same E on propagation | ARCH-ERROR-001 | Concise operational errors while cleanup remains explicit; no hidden coercion |
| Discard | ignored expressions, underscore bindings, reasoned operation | discard(value, "reason") predeclared operation; Result obligations remain visible | ARCH-ERROR-001 | More deliberate opt-out; diagnostic can name an actionable resolution |
| Modules | file-path imports, wildcard/selective imports, module imports | package::module with optional as; pub explicit; no import execution | ARCH-MODULE-001 | Reliable rename/resolution and straightforward module graph |
| Iteration | C loops, ranges, iterator protocol, core sequence loops | while/loop/for over sequence and bytes initially | ARCH-TYPE-001 | Achievable core; custom iterator/generic ecosystem requires later work |
| Resource cleanup | finally, defer, using, ownership scopes | Scope release plus explicit fallible library finish | ARCH-RESOURCE-001 | No new punctuation; must teach fault versus recoverable exit |
| Async/concurrency | reserve syntax now, experimental grammar, defer | No syntax until post-v0.1 RFC; retain architecture constraints | ARCH-CONC-001, ARCH-ASYNC-001 | Prevents unsupported examples and premature keyword reservations |
| FFI/unsafe/attributes | expose C-like surface now, reserve words, defer | No v0.1 source forms | ARCH-FFI-001, ARCH-SAFETY-001 | Language cannot imply trusted foreign safety; future audit design still required |

Doing nothing would leave Phase 4 inventing tokens and control structure. Copying a host language wholesale would import features outside the 86-entry scope. This candidate selects a small coherent surface; familiar spellings do not imply compatibility with another language.

Performance consequences are hypotheses: fixed tiers and keyword dispatch should simplify parsing; explicit contracts bound cross-module inference; ownership may require more teaching. No throughput, readability-study or memory benchmark is claimed. Independent review and novice walkthroughs remain valuable before stabilization.
