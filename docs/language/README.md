# Cretes Phase 3 — language surface candidate

**Version: 0.1 Draft · Status: PROPOSED / UNACCEPTED · Implementation: Not started**

Prepared 2026-10-02; validation and publication review 2026-10-03.

Phase 3 defines a reviewable syntax, grammar and surface-semantics candidate against the published Phase 2 proposal. It is not a frozen language specification or installable release. Phase 2 RFC acceptance remains pending; its announced final-comment period ends 2026-10-09 UTC, with a decision no earlier than 2026-10-10 00:00 UTC. The syntax candidate also requires its own RFC decision. Publication does not change either status.

[Specification](SPEC.md) · [Design rationale](DECISIONS.md) · [v0.1 scope](V0.1-SYNTAX.md) · [Grammar](cretes.ebnf) · [Lexical definitions](lexical.ebnf) · [Examples](EXAMPLES.md) · [Traceability](TRACEABILITY.md) · [Review](REVIEW.md) · [Validation](VALIDATION.md) · [Report](COMPLETION.md)

All Phase 3 files live together in `docs/language/` to keep the candidate, grammar, examples and isolated validator reviewable as one package. There is no duplicate normative grammar elsewhere. The validator is experimental and has no production AST, type checker, execution, backend or runtime.

## Sections 3.1–3.40

| Section | Topic | Feature ID | Classification |
| --- | --- | --- | --- |
| 3.1 | [Source and positions](SPEC.md#31-source-and-positions--lang-source-001) | LANG-SOURCE-001 | V0.1 REQUIRED |
| 3.2 | [Lexical structure](SPEC.md#32-lexical-structure--lang-lex-001) | LANG-LEX-001 | V0.1 REQUIRED |
| 3.3 | [Whitespace and lines](SPEC.md#33-whitespace-and-lines--lang-space-001) | LANG-SPACE-001 | V0.1 REQUIRED |
| 3.4 | [Comments](SPEC.md#34-comments--lang-comment-001) | LANG-COMMENT-001 | V0.1 REQUIRED |
| 3.5 | [Identifiers and source security](SPEC.md#35-identifiers-and-source-security--lang-ident-001) | LANG-IDENT-001 | V0.1 REQUIRED |
| 3.6 | [Keywords](SPEC.md#36-keywords--lang-keyword-001) | LANG-KEYWORD-001 | V0.1 REQUIRED |
| 3.7 | [Literals](SPEC.md#37-literals--lang-literal-001) | LANG-LITERAL-001 | V0.1 REQUIRED |
| 3.8 | [Type surface](SPEC.md#38-type-surface--lang-type-001) | LANG-TYPE-001 | V0.1 REQUIRED |
| 3.9 | [Operators](SPEC.md#39-operators--lang-op-001) | LANG-OP-001 | V0.1 REQUIRED |
| 3.10 | [Precedence](SPEC.md#310-precedence--lang-prec-001) | LANG-PREC-001 | V0.1 REQUIRED |
| 3.11 | [Expressions and places](SPEC.md#311-expressions-and-places--lang-expr-001) | LANG-EXPR-001 | V0.1 REQUIRED |
| 3.12 | [Bindings and constants](SPEC.md#312-bindings-and-constants--lang-decl-001) | LANG-DECL-001 | V0.1 REQUIRED |
| 3.13 | [Mutability and borrowing](SPEC.md#313-mutability-and-borrowing--lang-mut-001) | LANG-MUT-001 | V0.1 REQUIRED |
| 3.14 | [Functions](SPEC.md#314-functions--lang-func-001) | LANG-FUNC-001 | V0.1 REQUIRED |
| 3.15 | [Parameters and returned references](SPEC.md#315-parameters-and-returned-references--lang-param-001) | LANG-PARAM-001 | V0.1 REQUIRED |
| 3.16 | [Blocks and scopes](SPEC.md#316-blocks-and-scopes--lang-scope-001) | LANG-SCOPE-001 | V0.1 REQUIRED |
| 3.17 | [Conditionals](SPEC.md#317-conditionals--lang-if-001) | LANG-IF-001 | V0.1 REQUIRED |
| 3.18 | [Loops](SPEC.md#318-loops--lang-loop-001) | LANG-LOOP-001 | V0.1 REQUIRED |
| 3.19 | [Patterns](SPEC.md#319-patterns--lang-pattern-001) | LANG-PATTERN-001 | V0.1 REQUIRED |
| 3.20 | [Records and aliases](SPEC.md#320-records-and-aliases--lang-record-001) | LANG-RECORD-001 | V0.1 REQUIRED |
| 3.21 | [Tagged sums](SPEC.md#321-tagged-sums--lang-sum-001) | LANG-SUM-001 | V0.1 REQUIRED |
| 3.22 | [Methods](SPEC.md#322-methods--lang-method-001) | LANG-METHOD-001 | DEFERRED |
| 3.23 | [Generics](SPEC.md#323-generics--lang-generic-001) | LANG-GENERIC-001 | POST-V0.1 |
| 3.24 | [Interfaces](SPEC.md#324-interfaces--lang-interface-001) | LANG-INTERFACE-001 | POST-V0.1 |
| 3.25 | [Modules, imports and visibility](SPEC.md#325-modules-imports-and-visibility--lang-module-001) | LANG-MODULE-001 | V0.1 REQUIRED |
| 3.26 | [Errors](SPEC.md#326-errors--lang-error-001) | LANG-ERROR-001 | V0.1 REQUIRED |
| 3.27 | [Absence](SPEC.md#327-absence--lang-option-001) | LANG-OPTION-001 | V0.1 REQUIRED |
| 3.28 | [Concurrency](SPEC.md#328-concurrency--lang-conc-001) | LANG-CONC-001 | POST-V0.1 |
| 3.29 | [Async](SPEC.md#329-async--lang-async-001) | LANG-ASYNC-001 | POST-V0.1 |
| 3.30 | [Resource surface](SPEC.md#330-resource-surface--lang-resource-001) | LANG-RESOURCE-001 | V0.1 REQUIRED |
| 3.31 | [Unsafe](SPEC.md#331-unsafe--lang-unsafe-001) | LANG-UNSAFE-001 | POST-V0.1 |
| 3.32 | [FFI](SPEC.md#332-ffi--lang-ffi-001) | LANG-FFI-001 | POST-V0.1 |
| 3.33 | [Attributes](SPEC.md#333-attributes--lang-attr-001) | LANG-ATTR-001 | DEFERRED |
| 3.34 | [Grammar](SPEC.md#334-grammar--lang-grammar-001) | LANG-GRAMMAR-001 | V0.1 REQUIRED |
| 3.35 | [Formatting](SPEC.md#335-formatting--lang-format-001) | LANG-FORMAT-001 | V0.1 REQUIRED |
| 3.36 | [Diagnostics](SPEC.md#336-diagnostics--lang-diag-001) | LANG-DIAG-001 | V0.1 REQUIRED |
| 3.37 | [Canonical examples](SPEC.md#337-canonical-examples--lang-example-001) | LANG-EXAMPLE-001 | V0.1 REQUIRED |
| 3.38 | [Four-domain validation](SPEC.md#338-four-domain-validation--lang-domain-001) | LANG-DOMAIN-001 | V0.1 REQUIRED |
| 3.39 | [Consistency review](SPEC.md#339-consistency-review--lang-review-001) | LANG-REVIEW-001 | V0.1 REQUIRED |
| 3.40 | [v0.1 freeze candidate](SPEC.md#340-v01-freeze-candidate--lang-baseline-001) | LANG-BASELINE-001 | V0.1 REQUIRED |

## Authority and next steps

Proposed normative rules are explicitly labeled NORMATIVE CANDIDATE in SPEC.md. Explanations, examples, reviews and conceptual API contracts are non-normative. The token/character grammar defines syntax only; semantic restrictions remain in the prose. On conflict, fix the candidate before freeze rather than assuming a validator is authoritative over the specification.

1. Resolve Phase 2 review and record a dated architecture outcome.
2. Review the syntax RFC, including ownership restrictions, source security, grammar and examples.
3. Announce the required final-comment period with intended outcome, dispose of objections, and record the exact accepted revisions.
4. Update candidate statuses together only after acceptance. Implementation, conformance and release gates remain separate.

The administrative closure of spec issue #4 is not architecture acceptance. Phase 4 remains unstarted. Do not present conceptual standard-library calls as delivered APIs.

## Validation command

Run `python3 docs/language/validate.py` from the repository root using Python 3.10 or newer. It uses only the standard library. See VALIDATION.md for what was actually checked and what remains future work.
