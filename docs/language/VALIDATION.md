# Candidate validation report

Date: 2026-10-03. Status: local self-validation, **not independent approval**.

Command: `python3 docs/language/validate.py` (Python standard library only).

| Check | Result |
| --- | --- |
| Canonical `.cretes` corpus | 14 files recognized |
| Valid syntax fixtures | 32 accepted |
| Invalid syntax fixtures | 31 rejected |
| Invalid lexical fixtures | 22 rejected |
| Semantic-negative source fixtures | 16 recognized as syntax; semantic rejection intentionally NOT tested |
| Token grammar | 45 named productions; references defined and reachable |
| Keywords | 26; exact match to grammar word terminals |
| Invalid UTF-8 bytes | rejected |
| UTF-8 plus CRLF source spans | asserted against original byte offsets |
| Candidate local Markdown targets | checked by validator |
| Baseline-relative targets and anchors | checked during publication preparation against downloaded repository |

The recognizer expands token-level EBNF to BNF and uses a generic Earley algorithm. It does not emit an AST, resolve names, infer types, check ownership, execute programs or produce artifacts. The handwritten lexical scanner is a small validation spike implementing the lexical prose; lexical.ebnf is reviewed rather than independently compiled. There are no third-party package dependencies.

The 16 semantic-negative fixtures explicitly state the future expected failure. Their successful recognition must never be reported as successful program conformance. The library API sketches in EXAMPLES.md likewise cannot be executed today.

Manual checks cover tier/associativity grouping, record/control disambiguation, bracket type arguments, nullable grammar cases, enum/binding pattern distinction, deferred feature exclusions and source-security rules. Recognition of a finite corpus is not a proof of unambiguity or completeness. No generated parser, production lexer, runtime, benchmark, fuzz campaign, independent reviewer or soundness proof is claimed.

Future Phase 4 work: token snapshots; malformed-source recovery/progress tests; parser performance/resource-limit tests; AST conformance; and subsequent semantic/move/loan/cleanup tests. Preserve the exact source span contract and run the full published v0.1 requirements before any release claim.
