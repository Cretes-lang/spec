# 2.3 — Compilation pipeline and invariants

> Decision: **ARCH-PIPELINE-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-001](../requirements/CORE.md#core-001--source-file-extension), [CORE-002](../requirements/CORE.md#core-002--source-encoding), [CORE-003](../requirements/CORE.md#core-003--platform-independent-line-structure), [CORE-004](../requirements/CORE.md#core-004--unicode-identifiers-policy), [CORE-005](../requirements/CORE.md#core-005--protection-against-deceptive-source-text), [CORE-009](../requirements/CORE.md#core-009--name-resolution-without-execution), [CORE-017](../requirements/CORE.md#core-017--errors-detected-before-execution), [DX-005](../requirements/CORE.md#dx-005--diagnostic-content), [DX-008](../requirements/CORE.md#dx-008--robustness-on-malformed-input), [SAFE-001](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code)

## Proposed decision and rationale

**A staged pipeline preserves original source spans and verifies safety before backend optimization.**

| Stage | Input | Output and required invariant |
| --- | --- | --- |
| Source manager | File bytes and project map | Immutable original bytes, validated UTF-8 and line index; no silent source rewriting |
| Lexer | Source snapshot | Tokens/trivia with byte spans, invalid-token diagnostics |
| Parser | Tokens | Recoverable AST with explicit error nodes; no invented valid program |
| Resolution | AST and module graph | Symbol IDs and import/export visibility; no user-code execution |
| Type analysis | Resolved AST | Typed HIR, explicit conversions, exhaustive sum handling |
| Safety analysis | Typed HIR and control flow | Initialization, move and loan checks; rejection of unsafe safe-code paths |
| MIR construction | Checked HIR | Typed blocks, explicit checks, cleanup edges and source origins |
| MIR validation/optimization | MIR | Preserved behavior and cleanup; verifier after transformations |
| Backend lowering | Verified MIR and target | Backend IR with explicit layout and checked operations |
| Object generation | Verified backend IR | Target object and optional debug metadata |
| Link | Objects and declared native dependencies | Artifact plus provenance and dependency manifest |

Source locations remain file ID plus byte range into the original snapshot. CRLF may be interpreted as a line boundary without shifting offsets. Diagnostics carry presentation columns separately, preventing Unicode display width from corrupting byte offsets.

If parsing recovers, later stages may analyze unaffected regions for more errors, but no artifact is emitted while error-severity diagnostics remain. Parser recovery has a token-progress invariant. Limit nesting, diagnostic count and pathological resource use. Safety analysis is not optional in optimized builds.

## Options, advantages, disadvantages and rejected alternatives

An AST-only compiler was rejected because cleanup, borrow checking and diagnostics need explicit control flow. Running optimization before semantic validation was rejected because it could hide invalid source. A single untyped IR was rejected because it loses invariants between stages.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: malformed input must produce bounded errors rather than a compiler crash. Performance: stop check before backend work. DX: retain precise origin spans through lowering. Implementation: define pass contracts and verifiers; external linker diagnostics are translated without pretending they originated in source.

## Future verification

Later test stage snapshots, malformed input, Unicode/CRLF offsets, diagnostic ordering, and equivalence of optimized and unoptimized valid programs.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
