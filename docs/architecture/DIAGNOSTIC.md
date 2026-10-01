# 2.22 — Diagnostics architecture

> Decision: **ARCH-DIAGNOSTIC-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-004](../requirements/CORE.md#core-004--unicode-identifiers-policy), [CORE-005](../requirements/CORE.md#core-005--protection-against-deceptive-source-text), [DX-005](../requirements/CORE.md#dx-005--diagnostic-content), [DX-006](../requirements/CORE.md#dx-006--machine-readable-diagnostics), [DX-007](../requirements/CORE.md#dx-007--error-recovery), [DX-008](../requirements/CORE.md#dx-008--robustness-on-malformed-input), [DX-012](../requirements/CORE.md#dx-012--language-server), [SEC-022](../requirements/domains/cybersecurity.md#sec-022--secret-redaction-in-diagnostics-and-logs)

## Proposed decision and rationale

**A structured versioned diagnostic model shared by terminal output and future IDE tooling.**

A diagnostic contains code, severity, message identifier/parameters, source snapshot ID, primary byte span, labeled secondary spans, notes, help, related causes and optional fixes. Machine-readable output carries a schema version and explicit byte/line coordinate units; consumers must not parse human prose. Ordering is deterministic by file identity, span and stable code tie-breaker.

Fixes have replacement spans and applicability (machine-applicable, suggestion or uncertain). Applying a fix requires matching source version and non-overlapping ranges. Never automatically insert a deep clone, remove a security check or suppress an error merely to make compilation pass. Ownership errors identify owner creation, conflicting use and the lifetime endpoint; suggest restructuring before expensive copying.

Keep original UTF-8 bytes and a line index. Render tabs, combining characters, wide characters and CRLF without changing diagnostic offsets. Flag bidirectional controls and suspicious invisible characters with an escaped representation; identifier normalization/confusable policy remains a documented Phase 3 decision, not silent normalization. Bound rendered source and diagnostic counts to avoid terminal injection or output exhaustion.

Parser error recovery must make progress and suppress cascades when an earlier error poisons a region. The checker can analyze unaffected code but cannot emit a runnable artifact with errors. LSP adapters translate coordinate conventions from the same source snapshot rather than reusing terminal display columns. Secret values and environment contents are never automatically attached.

## Options, advantages, disadvantages and rejected alternatives

Human-text-only diagnostics were rejected for tooling. Backend-origin diagnostics as the primary interface were rejected because they lose semantic context. A shared structured model is proposed; exact visual layout and code spelling are not frozen here.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: escape terminal control characters and redact secrets. Performance: cap cascades and avoid duplicating source text per error. DX: show actionable cause and location, including inferred type/loan context. Implementation: schema, source index, renderer and LSP adapter remain separate.

## Future verification

Later snapshot diagnostics on Unicode/CRLF/tabs, malformed code, stale fixes, redacted data and terminal escapes; validate machine schema and stable error ordering.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
