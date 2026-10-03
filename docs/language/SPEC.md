# Cretes language surface — 0.1 Draft

Status: **DRAFT CANDIDATE, UNACCEPTED, UNIMPLEMENTED**. Date: 2026-10-02.

[Index](README.md) · [Grammar](cretes.ebnf) · [Decisions](DECISIONS.md) · [Traceability](TRACEABILITY.md)

Rules marked **NORMATIVE CANDIDATE** describe proposed behavior only. They become normative only after architecture acceptance, syntax RFC acceptance, and a reviewed status update. All examples and rationale are **NON-NORMATIVE**. No compiler behavior is claimed. Phase 1 priorities and the 86-requirement v0.1 scope are unchanged.

## 3.1 Source and positions — LANG-SOURCE-001

**NORMATIVE CANDIDATE.** Sources use `.cretes` and strict UTF-8. Reject malformed UTF-8, surrogate encodings, overlong forms, and U+FEFF including a leading BOM. No shebang is accepted in v0.1. LF and CRLF each count as one line boundary; bare CR is an error. Preserve original bytes. Locations are a file snapshot identity plus zero-based half-open byte offsets `[start,end)`. Human line and Unicode-scalar column numbers start at one; a tab counts as one scalar column, while display width is a rendering concern. EOF has a zero-width span. Final newline is recommended, not syntactically required. Do not normalize Unicode or line endings before recording spans.

Implementations must support at least 1 MiB of source per module and 128 levels of syntax nesting, or diagnose resource limits without crashing. They may support more; resource-limit diagnostics are distinct from invalid syntax. No source-length limit can be interpreted as permission for unsafe memory access.

## 3.2 Lexical structure — LANG-LEX-001

**NORMATIVE CANDIDATE.** Token categories are IDENT, INT, FLOAT, STRING, CHAR, BYTES, keywords, operators and delimiters. Comments/whitespace are trivia, preserved for tooling and excluded from grammar recognition. Lex longest valid operator. Scan an identifier before testing exact keyword membership. `letter` is ASCII only. An identifier-like suffix directly following a number is an invalid numeric token, not a new identifier: `12foo`, `0b102`, `1__0`, `0x` fail. A decimal point belongs to a float only when followed by a decimal digit. Therefore `1.foo` is integer, dot, identifier (then a type error), while `1.2` is FLOAT. Comments start outside literals only. `b"..."` has priority over IDENT `b` followed by STRING. EOF is the end condition, not a source spelling.

Unrecognized characters get a non-empty span and a diagnostic; a recovering lexer must advance. Token spans include delimiters and escape spellings; decoded values do not replace original spans. Lexical definitions are in [lexical.ebnf](lexical.ebnf).

## 3.3 Whitespace and lines — LANG-SPACE-001

**NORMATIVE CANDIDATE.** Only ASCII space, horizontal tab, LF and CRLF are whitespace. Indentation is not semantic. Blocks use braces. Semicolons terminate bindings, constants, aliases, imports, module declarations, return/break/continue, assignment and expression statements. No implicit semicolon insertion exists. Newlines can appear between any tokens; a newline cannot split a token. Empty statements (`;`) are rejected. Control statements and declaration bodies have no trailing semicolon. This gives pasted/generated code the same parse regardless of indentation.

## 3.4 Comments — LANG-COMMENT-001

**NORMATIVE CANDIDATE.** `//` ends before LF/CRLF or EOF. `/* ... */` nests; unmatched termination outside a comment is ordinary punctuation and then a syntax error. Unterminated block comments report the opening span. Strings inside comments do not inhibit nesting. `///` starts documentation trivia attached to the immediately following item/field when no blank line or intervening non-doc comment occurs. Documentation trivia does not alter program semantics. Future documentation tools may render it as data, never execute it. Block documentation notation is deferred.

## 3.5 Identifiers and source security — LANG-IDENT-001

**NORMATIVE CANDIDATE.** Identifiers match `[A-Za-z_][A-Za-z0-9_]*` and are case-sensitive. A sole `_` is the wildcard pattern, never a binding or expression name. Names beginning `__` are reserved for implementations and rejected in user declarations and references. Other underscore-prefixed names are ordinary. Unicode identifiers are deferred; UTF-8 text, character literals and comments remain available. ASCII-only names are a deliberate initial security/usability tradeoff, not a claim that all source spoofing is eliminated.

Reject literal bidi controls U+061C, U+200E–200F, U+202A–202E and U+2066–2069 everywhere, including comments/strings. Reject raw C0 controls except HT/LF/CRLF, DEL/C1 controls, U+200B–200D, U+2060, U+FEFF and U+2028–2029. Other non-ASCII whitespace is permitted in strings/comments but is invalid between tokens; render suspicious characters escaped in diagnostics. A Unicode escape inside a literal may intentionally produce these scalars at runtime; diagnostics render the source escape rather than executing terminal controls. Do not silently repair or normalize source. Confusable ASCII names such as `l` and `I` remain a review/lint concern.

## 3.6 Keywords — LANG-KEYWORD-001

**NORMATIVE CANDIDATE.** Exact reserved inventory:

`as break const continue else enum false fn for from if import in let loop match module mut new pub return struct true type var while`

All are required by the grammar. `from` is reserved to make return-borrow provenance visible; `as` is solely an import alias marker, never a cast. There are no contextual or future-reserved keywords in this candidate. Future words such as `async`, `await`, `trait`, `unsafe`, `extern` are ordinary identifiers today; adding syntax later requires the 0.x migration process. Built-in type names and `discard` occupy predeclared namespaces and cannot be redeclared, but lex as IDENT. The wildcard `_` is a grammar terminal, not a declaration name.

## 3.7 Literals — LANG-LITERAL-001

**NORMATIVE CANDIDATE.** Integers: decimal and lowercase-prefixed `0b`, `0o`, `0x`; hexadecimal digits may be uppercase. Leading decimal zero has no octal meaning. A single underscore may separate digits, never precede/follow the digits or touch a radix prefix, decimal point, exponent marker or sign. Floats require digits on both sides of a decimal point, or an exponent (`1e3`, `1.0e-3`). No numeric suffix, hexadecimal float, leading/trailing decimal point or infinity/NaN literal exists. Unary minus is separate from a literal.

An untyped integer adopts a representable contextual integer type, otherwise i64. The directly negated magnitude may represent the minimum signed value (`-9223372036854775808` for i64); type-check this pair before rejecting its positive magnitude. Default float type is f64, context may choose f32. Decimal-to-binary conversion rounds once to the destination, nearest ties-to-even; diagnose a finite spelling whose rounded magnitude overflows to infinity. Underflow follows that rounding mode.

Double-quoted text literals decode to valid UTF-8 `text`. Single-quoted character literals decode to exactly one Unicode scalar `char`, not a grapheme cluster. Allowed escapes: `\n`, `\r`, `\t`, `\0`, `\\`, `\"`, `\'`, `\u{H…}` with 1–6 hex digits representing a scalar through U+10FFFF excluding surrogates. No raw newline or tab in literals; escape them. Unknown/incomplete escapes are errors. No interpolation, implicit adjacent-string concatenation, raw or multiline string syntax in v0.1.

Byte literals `b"..."` produce `Bytes` (owning bytes), permit printable ASCII plus the simple escapes above and `\xHH`; Unicode escapes and raw non-ASCII are rejected. Text is never implicitly converted to bytes. `true` and `false` have type bool. There is no `null` literal; it is an ordinary unresolved identifier unless declared. Absence uses `Option::None()`.

## 3.8 Type surface — LANG-TYPE-001

**NORMATIVE CANDIDATE.** Predeclared types: `bool`, `char`, `text`, `i8 i16 i32 i64`, `u8 u16 u32 u64`, `f32 f64`, `usize`, `Bytes`, `Seq[T]`, `Map[K,V]`, `Set[T]`, `Option[T]`, `Result[T,E]`, `Box[T]`. `()` is the unit type/value; `(T,)` is a singleton tuple type; `(T,U)` is a tuple type; `(T)` is not a type grouping in v0.1. `byte`/`void` aliases are not predefined. `Bytes` is nominally distinct from `Seq[u8]`; conversion is explicit.

Signed integers use ranges -2^(n-1) through 2^(n-1)-1, unsigned 0 through 2^n-1. `usize` is the target pointer-width unsigned integer and is not a portable serialization type. char is a Unicode scalar independent of encoded byte width. f32/f64 use binary32/binary64 semantics from ARCH-TYPE-001. text/Bytes/collections/Box own storage and are not implicitly copyable. Map/Set keys initially require built-in hash/equality support (integer, bool, char, text, Bytes and tuples thereof); user-defined hashing is deferred. Maps/sets have unspecified iteration order and preserve Phase 2 randomized hashing requirements.

Built-in type constructors have exact arities above; user nominal types have zero type arguments. Qualified imported types may be named with `::`. No implicit conversion between typed numbers. Narrowing, float/integer conversion and text encoding require explicit fallible library calls. Cast punctuation is absent. Comparison operators do not perform numeric coercion.

## 3.9 Operators — LANG-OP-001

**NORMATIVE CANDIDATE.** Binary arithmetic `+ - * / %` takes same-type numbers; `%` is integer-only. Integer division truncates toward zero; remainder has dividend sign and satisfies the corresponding division identity. Division by zero, signed-minimum/-1 (including `%`), overflow, and invalid shifts fault in every profile. Bitwise `& | ^ ~` operate on integers; shifts require both operands of the same integer type and counts 0 through bit-width-1. Signed right shift sign-extends. Left shift computes multiplication by 2^count and faults when the mathematical result is outside the operand type; count validation also applies. Explicit checked/wrapping/saturating arithmetic is library surface, never implicit mode changes.

`== !=` accept equal types with built-in equality: numbers, bool, char, text, Bytes and recursively copyable tuples/records/sums whose fields support equality. Collections/Box/references have no generic identity/equality operator. Ordered comparisons accept numbers, char and text; text compares Unicode scalar sequences lexicographically. NaN compares unequal to every value including itself, and all ordered comparisons with NaN are false. `&& || !` require bool and short-circuit as usual. No truthiness. Unary `-` accepts signed integers/floats, `~` integers. Unary `*` dereferences checked references; `&`/`&mut` borrow places. No pointer arithmetic.

`=` is assignment statement syntax, not an expression. No compound assignment, increment/decrement, range, exponentiation, custom operators or operator overloading. Member access `.`, calls `()`, indexing `[]`, propagation `?`, and qualification `::` have the meanings below. Delimiters `{} [] () , ; :` and arrows `-> =>` are structural. `@ # $` have no token meaning.

## 3.10 Precedence — LANG-PREC-001

**NORMATIVE CANDIDATE.** High to low; grammar is authoritative for grouping and prose for typing:

| Level | Operators/forms | Associativity |
| --- | --- | --- |
| 12 | call, member, index, postfix `?` | left, in written order |
| 11 | unary `- ! ~ * & &mut` | right |
| 10 | `* / %` | left |
| 9 | `+ -` | left |
| 8 | `<< >>` | left |
| 7 | `< <= > >=` | non-associative |
| 6 | `== !=` | non-associative |
| 5 | bitwise `&` | left |
| 4 | `^` | left |
| 3 | bitwise `|` | left |
| 2 | `&&` | left |
| 1 | `||` | left |

Assignment is outside the table. Qualification belongs inside a primary path. `a < b < c` and `a == b == c` are syntax errors; write separate boolean comparisons. `a & b == c` groups as `a & (b == c)` and usually fails typing; prefer explicit parentheses. `a + b * c` groups `a + (b * c)`; `a-b-c` groups `(a-b)-c`. `&x?` groups `&(x?)`, then place checking determines validity. Parentheses always override grouping.

## 3.11 Expressions and places — LANG-EXPR-001

**NORMATIVE CANDIDATE.** Expressions include literals, names, grouped/tuple/sequence values, record construction, calls, member/index access, unary/binary operations and propagation. Blocks, if, loops and match are statements, never values. No closures/function values in v0.1. A function identifier is valid only as a direct call target; calls cannot return callable values.

Operands and arguments evaluate left-to-right; `&&`/`||` may skip the right operand. A call evaluates its argument expressions once in written order. Record field values evaluate in written order, independent of declaration order. Index receivers evaluate before indices. Assignment resolves its place (including indices) once before evaluating the right side, then releases the old initialized value and installs the new one; live conflicting loans make assignment illegal.

Places are locals/parameters, dereferenced references, and record fields or Seq/Bytes elements reached from places. Moving a non-copyable field/element out of an aggregate by value is rejected in v0.1; use whole-value moves or library removal operations. Read-only indexing of a non-copyable element requires borrowing. Numeric tuple selection is via library functions in this initial candidate; `.0` is not grammar. Borrowing a temporary is rejected; bind it first. Calls returning references produce reference values that can be dereferenced, with declared provenance.

An expression statement must have unit type. A non-unit value must be bound, returned, matched, or explicitly passed to `discard(value, "non-empty reason")`. This predeclared operation returns unit and deliberately drops its value; the second argument must be a non-empty literal STRING. Discarding a Result therefore remains visible. A bound Result must eventually be handled/returned/propagated or explicitly discarded before normal scope exit; moving into an aggregate only transfers that obligation. No bare ignored fallible call passes checking.

## 3.12 Bindings and constants — LANG-DECL-001

**NORMATIVE CANDIDATE.** `let name [: Type] = expression;` introduces an immutable binding; `var` introduces a mutable binding. Initialization is mandatory. Type inference is local and must determine one type without looking at other modules' callers. Empty sequences and option/result constructors may require an expected type. Bindings exist after their initializer; a use in its own initializer resolves an outer declaration if one exists.

`const name: Type = expression;` requires an explicit type and a constant expression. Constants may occur at module or block scope. Allowed constant values are scalar numbers, bool, char, unit and recursively such tuples. Constant expressions use their literals, earlier or module-scope constants, grouping and scalar unary/binary operations; no calls, borrows, text/byte allocation, collections, record construction or I/O. A dependency cycle is an error. Invalid arithmetic is a compile-time error, never a host-language overflow. Evaluation limits produce a dedicated diagnostic. Top-level let/var or arbitrary statements are disallowed.

## 3.13 Mutability and borrowing — LANG-MUT-001

**NORMATIVE CANDIDATE.** `var` permits replacing a binding and mutating owned fields/elements. `let` forbids these operations. Moving a value from an immutable binding is permitted. Mutability is separate from ownership. `&T` permits shared read access; `&mut T` permits exclusive mutation of its referent even if the reference binding is immutable. `var r: &T` permits rebinding r, not writing through r. Parameter `var` permits local rebinding and mutation of an owned parameter; it does not give a caller's owned variable implicit by-reference mutation.

`&place` and `&mut place` create loans. `&mut` requires a writable place. Reference lifetime is bounded by the owner, control-flow uses and reborrow ancestry; multiple shared loans or one exclusive loan may be live. A parent exclusive reference is suspended while a reborrow is live. Owners cannot move, resize, be destroyed or be incompatibly accessed while a loan is live. Shared references copy; exclusive references move. Aggregates may not store references, even nested through Option/Seq/Box. References can be locals/parameters or direct function results only in v0.1. Reference-to-reference types are excluded. These restrictions are semantic checks even when the grammar can recognize the spelling.

At a branch join, a value is usable only if initialized and unmoved on every incoming reachable edge. Loop analysis must include back edges: an owner moved in one iteration cannot be used by the next without reinitialization. Reassignment to a moved `var` restores initialization; immutable bindings cannot be reinitialized. Whole aggregates of copyable fields copy implicitly, with no allocation; other values move. Partial field moves are excluded. This candidate specifies analysis obligations, not a soundness proof.

## 3.14 Functions — LANG-FUNC-001

**NORMATIVE CANDIDATE.** `fn name(parameters) -> Type { statements }`. All parameters and returns are annotated, including private functions; local bindings carry the inference benefit. Unit-returning functions write `-> ()`. Functions are module items; nested functions, overloads, defaults, callable values and closures are deferred. All module function declarations are collected before bodies, allowing recursion and mutual recursion. Duplicate names in a module are errors.

Every reachable path of a non-unit function returns a value or diverges. A unit function may fall through; `return;` is equivalent to returning unit. There is no implicit tail-expression return. The selected entry module has exactly one `fn main() -> i32` or `fn main() -> Result[i32, E]`; E must be a concrete accessible error type. Zero signals success, 1–125 are explicit portable application failures; values outside 0–125 produce a defined entry-contract fault. An entry Err is reported through bounded redacted error output and exits 1. Arguments come from a conceptual standard-library API. Libraries need no main.

## 3.15 Parameters and returned references — LANG-PARAM-001

**NORMATIVE CANDIDATE.** Calls use positional arguments, exact arity and no default, named or variadic arguments. Each owned argument moves unless copyable. Shared/exclusive borrowing is explicit at the call site; there is no automatic receiver borrowing. Parameter order is evaluation order. Multiple values are returned as a tuple.

A direct reference return must declare `from parameter`, for example `fn first(xs: &Seq[i64]) -> &i64 from xs`. The named parameter must be a compatible reference; every returned reference must derive from that loan and cannot refer to local storage. Shared output may derive from shared/exclusive input; mutable output only from exclusive input. The returned loan remains bounded by the actual argument owner and reborrow ancestry. A from clause on a non-reference result is an error. Only one source parameter may be named in v0.1; borrowing from alternative owners or storing borrowed fields needs a later RFC. References never escape as nested return fields.

## 3.16 Blocks and scopes — LANG-SCOPE-001

**NORMATIVE CANDIDATE.** Each block introduces lexical scope. A name cannot be redeclared in the same scope. Inner blocks may shadow outer local bindings, but must not shadow predeclared type names, imported module aliases or `discard`. A shadowing initializer resolves the outer binding. Parameters share the outer function-body scope. Function/item names are resolved lexically, not by declaration execution. Cleanup runs when leaving a block along normal control flow. Unreachable code is diagnosed as a warning where reliable; it is still parsed and type checked.

## 3.17 Conditionals — LANG-IF-001

**NORMATIVE CANDIDATE.** `if condition { ... } else if condition { ... } else { ... }`. Conditions are bool. Parentheses are legal grouped expressions but optional and omitted by canonical formatting unless needed. Braces are mandatory. The grammar attaches else to the immediately preceding if of the nested structure; there is no unbraced dangling-else case. No ternary operator, implicit truthiness, conditional binding or value-yielding if exists.

## 3.18 Loops — LANG-LOOP-001

**NORMATIVE CANDIDATE.** `while condition { ... }`, `loop { ... }`, `for name in expression { ... }`, `break;`, `continue;`. While checks a bool before each iteration. Loop repeats until control exits. Break/continue target the nearest loop and are invalid outside loops; labels/value-carrying break are deferred. They execute scope cleanup for scopes exited, with continue preserving the loop's outer scope.

For evaluates its iterable once and accepts an owned Seq/Bytes, or a shared/exclusive reference to Seq/Bytes. Owned iteration consumes the container and moves elements; shared iteration binds a shared element reference; exclusive iteration binds an exclusive element reference that may not survive into the next iteration. Iteration proceeds in index order; the loop binding is immutable. Breaking drops remaining owned elements once. User iterator protocols, range syntax, map/set iteration and C-style loops are deferred; index-based while loops and explicit library operations express initial requirements.

## 3.19 Patterns — LANG-PATTERN-001

**NORMATIVE CANDIDATE.** Patterns are match-only: wildcard `_`, immutable binding, tuple, literal, or qualified variant `Type::Variant(patterns)`. A zero-field variant is spelled with empty parentheses. A bare name always binds; it does not test a constant or nullary variant. No or-pattern, guard, range, field destructuring, rest, reference or nested mutability pattern. Literal patterns are integer/char/bool/text/bytes; floating patterns are rejected semantically. Tuple arity and variant field counts must match. Bindings in one pattern must be distinct.

Match evaluates its subject once. An owned subject is consumed, and payload bindings receive moved/copied values. A reference subject inspects the referent and binds payload references of the same access mode, avoiding consumption. Literal/wildcard tests do not move fields. This is the only implicit pattern borrowing; ordinary expressions require explicit borrows. Wildcard drops an unmatched owned payload at arm completion; it cannot silently discard a Result obligation (use an explicit discard action). A binding pattern receives the whole subject. Patterns are tried in source order. An unconditional wildcard/binding makes later arms unreachable and is an error.

## 3.20 Records and aliases — LANG-RECORD-001

**NORMATIVE CANDIDATE.** `struct Point { pub x: i64, pub y: i64, }` declares a nominal record. Every field ends with a comma, including the last, to keep grammar/formatting deterministic. Construct with `new Point { x: 1, y: 2 }`; every field occurs once, no shorthand/default/spread. Empty records are allowed. Field names are ordinary identifiers; fields are private unless pub. Construction outside the declaring module requires the type and every supplied field to be accessible. `value.field` accesses a field; mutation requires a writable place. Field order defines logical storage order but no stable ABI or packed layout is promised.

`type Name = Type;` is a transparent alias, without new identity. Alias cycles and recursive by-value record/sum layouts fail checking. Owning Box indirection breaks a recursive layout cycle. No classes, inheritance, opaque-type declarations, custom destructors or user-defined copy behavior in v0.1.

## 3.21 Tagged sums — LANG-SUM-001

**NORMATIVE CANDIDATE.** `enum Status { Idle, Busy(i64), }` declares a non-empty nominal sum. Payloads are positional types; nullary variants omit parentheses in the declaration but use parentheses in construction/patterns: `Status::Idle()`. Fields/variants of a public enum are public; private representation uses a private type rather than selectively hidden variants. Constructors require exact payload types/arity. No numeric discriminants or implicit integer conversion.

`match value { Status::Idle() => { ... } Status::Busy(n) => { ... } }` is a statement. Every possible value must be covered; a wildcard/binding is required for unbounded scalar domains. Finite bool/enums and product patterns may be checked recursively. An empty match is invalid for inhabited types. Type checking must reject missing variants and unreachable arms. New public variants are source compatibility changes even during 0.x and require migration notes.

## 3.22 Methods — LANG-METHOD-001

**DEFERRED.** ARCH-TYPE-001 does not require a v0.1 method system. Module functions with explicit receiver parameters (`geom::area(&shape)`) express the needed operations. `x.name` denotes a field; calling a field is a semantic error because function values are deferred. No impl/self/static receiver syntax is reserved. A later RFC must define method resolution, borrowing, visibility and coherence before adding methods.

## 3.23 Generics — LANG-GENERIC-001

**POST-V0.1.** User generic declarations, constraints, specialization and generic call arguments are absent. Square brackets in a type instantiate only compiler-known constructors. Expression brackets mean indexing/sequence construction, never generic specialization. No token splitting is required for `>>` in nested type arguments. Built-in constructor operations infer their type arguments from annotated bindings/returns and payloads. An unsolved empty collection is a type error, not dynamic typing. Later generic syntax requires its own RFC and migration review.

## 3.24 Interfaces — LANG-INTERFACE-001

**POST-V0.1.** Nominal interface constraints and explicit dynamic dispatch remain architecture directions, not current grammar. No trait/interface/protocol/implementation keyword, inheritance, default implementation or dispatch layout is selected here. The later RFC must resolve coherence, overlap, object safety and code-size costs. Required map-key operations are compiler-defined for the initial built-in set.

## 3.25 Modules, imports and visibility — LANG-MODULE-001

**NORMATIVE CANDIDATE.** Optional first declaration `module package::logical::path;` must match the manifest's module identity. It may be omitted when the manifest or single-file driver supplies the identity. Imports precede items: `import package::module as alias;`. Without as, the last component is the alias. Imports name modules, not files or values; qualified uses are `alias::item`. Duplicate/conflicting aliases are errors. Wildcards, selective imports, re-exports and relative path escapes are absent. `pub` applies to module-level functions, constants, aliases, records and sums, not local declarations or imports. A pub API cannot expose a private type.

Module imports are acyclic and resolved without executing code. Module-level constants use the restricted evaluator. A single-file program has an implicit local package and entry module; the standard package is provided by the toolchain. Manifest filename/schema is an existing Phase 2 follow-up, outside source grammar. The eventual manifest maps module IDs to source and an entry target; file layout never silently changes symbol identity.

## 3.26 Errors — LANG-ERROR-001

**NORMATIVE CANDIDATE.** `Result[T,E]` has `Result::Ok(T)` and `Result::Err(E)`. Constructors infer missing type arguments from context. `value?` accepts Result only: evaluate once, yield T on Ok, or return Err with the exact same E from the enclosing Result-returning function. No implicit error conversion. Cleanup is identical to explicit return. Parenthesized propagation composes with postfix calls/indexing in written order. There is no throw/catch, unwinding or catchable fault. Match provides explicit recovery.

Error values may be user sums/records or standard structured errors. Standard API errors must expose stable category, operation, optional provider code and bounded/redacted cause chain per ARCH-ERROR-001; those library member names are not frozen by this grammar. `discard(result, "reason")` is the explicit opt-out. A simple `let ignored = fallible();` does not satisfy the handling obligation if ignored at scope exit.

## 3.27 Absence — LANG-OPTION-001

**NORMATIVE CANDIDATE.** `Option[T]` has `Option::Some(T)` and `Option::None()`. Option differs from Result and uninitialized storage. Match performs exhaustive extraction. Postfix `?` on Option is a type error; optional chaining/coalescing and unchecked extraction syntax are deferred. Ordinary references cannot be null. An empty Option is a fully initialized value. No pointer representation/niche is exposed by source syntax.

## 3.28 Concurrency — LANG-CONC-001

**POST-V0.1.** No spawn, task group, thread, channel, select or atomic syntax exists in this grammar. ARCH-CONC-001 calls for structured ownership and bounded tasks later. Future syntax must preserve join-before-release, transfer/share checks, cancellation outcomes and bounded queues. The absence of a concurrency example is intentional; see [domain review](DOMAINS.md). A word such as `spawn` can be a user function name but has no language effect.

## 3.29 Async — LANG-ASYNC-001

**POST-V0.1.** No async function or await operator is accepted. Future surface design must distinguish cold operations from scheduled tasks, make suspension explicit and retain I/O buffers until terminal completion. Adding only keywords now would falsely freeze a runtime contract. Deferred requirements retain their original milestone and are not claimed fulfilled by synchronous examples.

## 3.30 Resource surface — LANG-RESOURCE-001

**NORMATIVE CANDIDATE.** Owning values release on normal scope exit in reverse binding-declaration order, including return, propagation, break and continue. Within records/tuples, release initialized components in reverse construction order. A move transfers release responsibility; an uninitialized/moved slot is never released twice. Replacing a live var releases the old value after RHS evaluation succeeds. Construction failure releases only initialized components. Fallback release cannot throw or suspend; explicit fallible library close/finish must be checked for durability. Fatal faults terminate without a cleanup guarantee. No defer/finally/using/custom destructor syntax is introduced. Borrow rules prevent closing an owner with live views.

## 3.31 Unsafe — LANG-UNSAFE-001

**POST-V0.1.** Raw addresses, unchecked casts, pointer arithmetic and unsafe blocks are absent. `*` dereferences valid checked references only. Trusted compiler/runtime implementation remains a later audit obligation. No safe-language claim is proved by grammar validation. A later unsafe RFC must define audit visibility without disabling ordinary type checks.

## 3.32 FFI — LANG-FFI-001

**POST-V0.1.** No extern declaration, ABI string, callback export, foreign pointer or C-layout attribute is defined. The eventual C boundary must specify calling convention, layout, ownership, nullability, retained lifetimes and unwinding containment. Cretes-native ABI remains unstable. Domain sketches do not create callable foreign APIs.

## 3.33 Attributes — LANG-ATTR-001

**DEFERRED.** Documentation comments are the only metadata-like surface. No `@`, `#[...]`, annotation, macro, conditional-compilation or plugin syntax is accepted. Tests and deprecation attributes need later toolchain/API decisions. No executable compile-time hooks are introduced.

## 3.34 Grammar — LANG-GRAMMAR-001

**NORMATIVE CANDIDATE.** [cretes.ebnf](cretes.ebnf) specifies token-level syntax; [lexical.ebnf](lexical.ebnf) specifies character-level tokens with explicitly described special sequences. `=` defines, `;` ends a rule, juxtaposition concatenates, `|` alternates, parentheses group, square brackets mean optional, braces mean zero-or-more. Quoted strings are exact terminals; uppercase token categories are supplied by the lexer. Comments use `(* ... *)` in EBNF only. Source delimiters are quoted and cannot be confused with notation.

The start rule is program. All input must be consumed. No user feature is added by accepting a syntactic shape later rejected by typing: type arity, lvalues, exhaustive patterns, return completeness, visibility, name resolution and ownership are explicit semantic checks. The grammar uses no left recursion. Declarations are keyword-dispatched; expression tiers fit the proposed recursive-descent/precedence strategy. `new` disambiguates record construction from a following control block. Pattern binding vs constructor uses following `::`/`(`; type arguments occur only in type contexts. `from` is outside the return type.

The included validator is an **EXPERIMENTAL NON-PRODUCTION recognizer**, with no AST/type checker/runtime. Its passing fixtures are evidence of recognizability, not semantic correctness or a proof of global unambiguity. See [validation](VALIDATION.md).

## 3.35 Formatting — LANG-FORMAT-001

**NORMATIVE CANDIDATE FOR FUTURE FORMATTER.** Four spaces, no tabs, UTF-8 without BOM, LF output, final newline, opening brace on the declaration/control line, closing brace on its own line. One space around binary/assignment operators, after commas and colons; no spaces inside ordinary delimiters or around `::`/member dots/postfix `?`. Write `&mut x`, `&x`, `*x`, `-x`. Imports precede declarations, separated from them by a blank line; preserve comment attachment and import order rather than reordering side-effect-free declarations unnecessarily. Separate top-level items by one blank line. Recommended width 100 columns, with long indivisible tokens exempt. Multiline argument/type/variant/initializer lists use trailing commas; record declarations always do. Preserve literal values, comments and spelling when escape changes might affect teaching/security. A formatter must not change parsing or bindings. No formatter implementation is included.

## 3.36 Diagnostics — LANG-DIAG-001

**NORMATIVE CANDIDATE.** Codes are stable within this draft family; human wording may evolve. Each diagnostic includes severity, original snapshot ID and byte span, concise explanation, secondary spans where needed, and actionable help. Machine output carries schema version and coordinate units, never requires parsing prose. Suggested fixes name applicability and must not insert cloning, remove checking or silently suppress errors.

| Code | Trigger | Guidance |
| --- | --- | --- |
| L001 | invalid UTF-8/BOM/newline/control | identify exact byte/scalar; save strict UTF-8 |
| L002 | invalid identifier/reserved internal name | show escaped source and permitted characters |
| L003 | malformed number | identify base/separator/exponent |
| L004 | invalid literal/escape | name delimiter/escape and opening span |
| L005 | unterminated nested comment | point to opening delimiter |
| P001 | unexpected token/missing delimiter | report expected category, opening delimiter |
| P002 | keyword used as declaration name | suggest a new name, not silent escaping |
| P003 | chained comparison/equality | suggest explicit boolean conjunction |
| T001 | wrong type/arity/operator/lvalue | show expected and found contracts |
| T002 | non-exhaustive or unreachable match | list missing alternatives |
| T003 | unused Result | handle, return, propagate or explicit reasoned discard |
| B001 | moved/uninitialized value | show move and subsequent use |
| B002 | conflicting/escaping loan | show owner, borrow and invalidating use |
| M001 | module cycle/private or duplicate name | show path/declaration chain |
| C001 | invalid/cyclic constant | show dependency or arithmetic operation |
| R001 | implementation resource limit | report limit without claiming valid source is malformed |

Recovery must always consume a token or finish a region, synchronize at semicolons/braces/top-level item keywords, cap cascades and never emit an executable when errors remain. Escape terminal controls, bound displayed source and redact sensitive content. The validation tool's abbreviated failures are not the future diagnostic engine.

## 3.37 Canonical examples — LANG-EXAMPLE-001

**NON-NORMATIVE.** Numbered `.cretes` files in this directory are the canonical candidate corpus. [01-hello-world.cretes](01-hello-world.cretes) imports a conceptual standard I/O module, declares main, propagates the explicit print Result, and returns zero. `fn`, name, parentheses, arrow, type tokens and braces follow function; the import follows import_decl; the call and postfix propagation follow postfix. Expected conceptual behavior is one greeting line on stdout and successful exit; I/O failure returns Err. This is not executable today. API contracts are explicitly scoped in [examples](EXAMPLES.md).

## 3.38 Four-domain validation — LANG-DOMAIN-001

**NON-NORMATIVE.** [DOMAINS.md](DOMAINS.md) records automation/file errors, network packet validation, CPU numeric preprocessing and defensive byte checks. It distinguishes grammar fixtures from conceptual APIs and deferred services. No networking, crypto, process or AI framework is implemented.

## 3.39 Consistency review — LANG-REVIEW-001

**NON-NORMATIVE.** [REVIEW.md](REVIEW.md) records declaration/type ordering, keyword/punctuation inventory, precedence, ownership, parser, security, tooling and scope review. The automated recognizer validates the published grammar/corpus and checks rule reachability. It cannot replace independent language/borrow-checker review, type checking, runtime tests or human usability studies.

## 3.40 v0.1 freeze candidate — LANG-BASELINE-001

**DRAFT FREEZE CANDIDATE, NOT FROZEN.** [V0.1-SYNTAX.md](V0.1-SYNTAX.md) identifies the proposed implementation target. Formal freeze requires acceptance of Phase 2 and the Phase 3 RFC, public comment/objection disposition and dated maintainer decision tied to exact revisions. Afterwards, major syntax changes use follow-up RFCs; spelling/behavior corrections require specification and fixture updates together. Phase 4 may use the approved files for token/AST implementation only after separately authorized. No production lexer/parser, compiler/runtime or standard library is part of this work.
