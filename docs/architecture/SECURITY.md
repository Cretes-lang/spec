# 2.19 — Security and trust architecture

> Decision: **ARCH-SECURITY-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[SEC-001](../requirements/domains/cybersecurity.md#sec-001--memory-safe-development-objective), [SEC-002](../requirements/domains/cybersecurity.md#sec-002--bounds-checked-binary-parsing), [SEC-003](../requirements/domains/cybersecurity.md#sec-003--checked-length-arithmetic-in-parsers), [SEC-004](../requirements/domains/cybersecurity.md#sec-004--constant-time-operations), [SEC-005](../requirements/domains/cybersecurity.md#sec-005--secret-zeroization), [SEC-006](../requirements/domains/cybersecurity.md#sec-006--secure-randomness), [SEC-015](../requirements/domains/cybersecurity.md#sec-015--cryptographic-implementation-assurance), [SEC-018](../requirements/domains/cybersecurity.md#sec-018--tls-security-policy), [SEC-023](../requirements/domains/cybersecurity.md#sec-023--dependency-integrity), [SEC-024](../requirements/domains/cybersecurity.md#sec-024--package-provenance-and-signing), [SEC-025](../requirements/domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation), [SEC-026](../requirements/domains/cybersecurity.md#sec-026--vulnerability-advisories-and-audit), [SEC-027](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds), [SEC-028](../requirements/domains/cybersecurity.md#sec-028--software-bill-of-materials), [SEC-029](../requirements/domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting), [SEC-030](../requirements/domains/cybersecurity.md#sec-030--fuzzing-support), [SEC-031](../requirements/domains/cybersecurity.md#sec-031--security-focused-static-analysis), [SEC-032](../requirements/domains/cybersecurity.md#sec-032--toolchain-release-integrity), [SEC-033](../requirements/domains/cybersecurity.md#sec-033--scope-of-defensive-utilities), [SEC-034](../requirements/domains/cybersecurity.md#sec-034--registry-account-and-namespace-protection)

## Proposed decision and rationale

**Explicit trust boundaries, constrained build inputs and independently updateable security providers.**

| Boundary | Threat | Architectural control |
| --- | --- | --- |
| Source/config to compiler | Malformed or adversarial input | Parsing limits, fuzzing, no import-time execution, deterministic errors |
| Safe source to trusted code | Incorrect wrapper/optimizer assumptions | Typed contracts, narrow unsafe regions, conformance and sanitizer tests |
| Dependency to build | Substitution or install-time code execution | Locked identities/digests, no implicit scripts, explicit source origins |
| Build to native tool | Shell injection or ambient tool substitution | Argument arrays, resolved executable paths, recorded versions |
| Runtime to OS/native library | Invalid handles/buffers and retained pointers | Ownership, checked wrappers, completion-aware lifetimes |
| Secret to logs/storage | Accidental disclosure | Secret types, redaction, opt-in diagnostics and bounded context |
| Release to user | Tampered artifacts or stale vulnerable provider | Checksums, provenance, signing plan and documented update policy |

The native program is not a capability sandbox. Compiling or running untrusted programs requires an external sandbox with OS-enforced resource/permission controls. Memory-safe source may still read allowed files or consume resources. No claim of complete vulnerability elimination follows from the language model.

Security primitives come from reviewed providers, not ad hoc algorithms written for Phase 2. High-level misuse-resistant APIs are separate from expert primitives. Provider versions and security updates are visible independently from language versions. Constant-time behavior is scoped to reviewed primitives, compilation settings and hardware assumptions; arbitrary source receives no such guarantee.

Compiler hardening includes bounded recursion/work, fuzzing and validated caches. Runtime/binary hardening uses supported platform defenses with recorded settings; defenses do not repair unsound language lowering. Package management later separates content integrity from publisher authenticity and registry authorization; a hash is not a signature. Advisories and SBOMs describe actual shipped dependencies.

## Options, advantages, disadvantages and rejected alternatives

A compiler-owned crypto/TLS stack was rejected for maintenance and audit burden. Trusting every installed package to run scripts was rejected. Universal language sandboxing was rejected as an unsupported guarantee. Explicit boundaries and separately reviewable providers are proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: provider selection, unsafe wrappers and supply-chain identity remain residual risks. Performance: validation and redaction have costs to measure. DX: safe defaults and specific failure categories avoid implicit insecure fallbacks. Implementation: threat model accompanies each native integration and release.

## Future verification

Later fuzz parser/serialization boundaries, test malicious dependency metadata, tampered digests, secret redaction, provider-policy rejection, binary hardening and release provenance.

## Risks and open questions

Crypto/TLS provider choice, signing trust root and registry identity protocol need dedicated security review before those capabilities ship; mark them DEFERRED rather than accepted.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
