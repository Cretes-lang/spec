# Phase 3 review record

Status: **DRAFT self-review**, 2026-10-02. [Specification](SPEC.md), [decision rationale](DECISIONS.md), [validation](VALIDATION.md).

## Source inspection

The baseline was downloaded through GitHub from spec main at `77079abc6458a96dddd1d2faa66edc7a17803fcb`. It contains Phase 1 requirements and all 35 architecture documents, no existing grammar or language chapter. The organization, spec, rfcs, governance, contribution guide, version policy, cretes and website scopes were inspected. There were no open spec issues or pull requests at inspection. No implementation repository or website app is changed by this candidate.

Phase 2 is PROPOSED despite merged publication; its comment window ends 2026-10-09 UTC and cannot yield acceptance before 2026-10-10 00:00 UTC. Spec issue #4 was closed administratively at the owner's request; its closure explicitly deferred acceptance. This draft work is authorized separately, without representing the architecture as already accepted. Historic Phase 2 statements that Phase 3 had not started describe the earlier milestone; the new index records the current candidate work.

## Consistency matrix

| Check | Resolution | Evidence/remaining boundary |
| --- | --- | --- |
| Declaration ordering | keyword then name, colon type, mandatory initialization | fn/let/var/const grammar and fixtures |
| Type surface | fixed names, [type] only for built-in constructors | no generic declarations; arity is semantic |
| Blocks/statements | braces; explicit semicolons; no tail values | missing-semicolon/unbraced negative fixtures |
| Mutability | var for binding, &mut for exclusive referent | two meanings explained with reference examples |
| Visibility | pub items/fields; private default | module provenance and visibility remain checker work |
| Errors and absence | Result ? versus Option match | Option propagation semantic-negative fixture |
| Ownership | moves, no partial moves, explicit reborrows/from | semantic-negative cases are future checker tests |
| Deferred features | no async/concurrency/FFI/unsafe/attributes | negative syntax fixtures and scope table |
| Keywords | 26 exact reserved words; no speculative reservations | validator compares grammar terminals to inventory |
| Punctuation | every terminal accounted for; no @/#/$ or range | grammar and fixed operator list |
| Numeric semantics | no implicit coercions; checked default arithmetic | semantic-negative conversion and boundary source |
| Initialization | module constants only; no import-time effects | top-level-let and constant-call fixtures |

## Parser review

The 45 named syntax productions are reachable and all references are defined. Token-level grammar has no left-recursive production. Postfix repetition binds tighter than prefix and binary tiers. Comparison/equality are non-chainable. Braces eliminate dangling else. `new` prevents a condition's following block from being mistaken for record construction. Built-in type arguments use brackets, avoiding angle/shift conflicts. Tuple/group parsing uses the comma; unit and singleton tuple are distinct. Literal categories are lexically disjoint after longest-match/base/byte-prefix rules. Qualified nullary variant patterns use parentheses; bare names bind.

The recognizer checks corpus acceptance but does not prove global grammar unambiguity. Manual lookahead analysis found no unresolved syntactic ambiguity in the candidate. Production error recovery, source limits, AST construction and parsing performance remain Phase 4 work. Manifest/schema readiness remains Phase 2 risk R-11 and is outside this source grammar.

## Security review

UTF-8 errors, raw bidi controls, selected invisibles, numeric suffixes and malformed escapes are rejected. ASCII identifiers avoid a versioned normalization table, with international names explicitly deferred. Raw text data remains UTF-8. Escaped runtime control data is distinct from deceptive raw source. Terminals cannot trigger shell/API execution. Standard-library sketch names cannot be treated as a safe implementation.

Unsafe and FFI source constructs are excluded; checked references do not expose pointers. Resource cleanup follows normal/Result exits; faults have no cleanup guarantee. No diagnostic fix may remove checks or add expensive cloning silently. Ownership soundness, compiler fuzzing, target stack behavior, native audits and constant-time guarantees remain unproven. Grammar acceptance is not a security certification.

## Tooling and readability review

Tokens and original byte spans support syntax highlighting and future LSP coordinate conversion. No context-sensitive keyword table depends on symbol lookup. Required return contracts aid hover/completion and refactoring. Documentation comments attach as trivia, with no execution. Canonical formatting is deterministic at the rules level, but a formatter is not implemented. Rename must distinguish module/type/value scopes; byte offsets must never be confused with UTF-16 editor positions.

Common examples were manually walked through for ownership, errors and readability. No external novice study or independent reviewer approval occurred. Keywords and punctuation remain a teaching cost; no claim of superior readability over other languages is made.

## Review outcome

Candidate ready for public RFC review after local grammar/corpus/link checks. Formal freeze is pending architecture acceptance and the syntax RFC decision. No production compiler, runtime, standard library, release, benchmark or Phase 4 implementation was created. Major source-rule changes require reviewed RFC/specification/fixture updates together.
