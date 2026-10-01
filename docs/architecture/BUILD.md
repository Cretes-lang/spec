# 2.21 — Build and package architecture

> Decision: **ARCH-BUILD-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CORE-025](../requirements/CORE.md#core-025--deterministic-compilation), [CORE-028](../requirements/CORE.md#core-028--declarative-package-manifest), [CORE-029](../requirements/CORE.md#core-029--separate-and-incremental-compilation), [DX-015](../requirements/CORE.md#dx-015--package-manager-and-registry), [SEC-023](../requirements/domains/cybersecurity.md#sec-023--dependency-integrity), [SEC-024](../requirements/domains/cybersecurity.md#sec-024--package-provenance-and-signing), [SEC-025](../requirements/domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation), [SEC-026](../requirements/domains/cybersecurity.md#sec-026--vulnerability-advisories-and-audit), [SEC-027](../requirements/domains/cybersecurity.md#sec-027--reproducible-builds), [SEC-028](../requirements/domains/cybersecurity.md#sec-028--software-bill-of-materials), [SEC-034](../requirements/domains/cybersecurity.md#sec-034--registry-account-and-namespace-protection)

## Proposed decision and rationale

**Declarative local projects in v0.1; a future locked dependency graph with explicit origins and no implicit executable hooks.**

The v0.1 manifest describes project/package identity, source root, module map and executable/library targets. The filename and concrete serialization format are left to a focused format decision before implementation; they are not language grammar. The manifest is parsed as data with a versioned schema, rejects duplicate/unknown critical keys and cannot execute scripts. v0.1 has no remote dependency resolver or package registry.

Future packages have a canonical identity consisting of source origin, namespace/name and immutable version/content identity. A workspace coordinates local packages but cannot silently override a locked registry package. Registry, Git and local dependencies are explicit source kinds. Git resolves to an immutable commit plus content verification; a branch name alone is not a reproducible lock. Local path dependencies are root-checked and recorded as non-publishable until packaged reproducibly.

Resolution runs only for an explicit dependency update. A normal build consumes the lockfile and fails when metadata or content differs. The lock records the complete transitive graph, source origins, versions, digests, target conditions and resolver version. Deterministic tie-breaking and conflict explanations are required; exact version-constraint grammar and solver algorithm remain a later package RFC. Multiple versions may coexist only with distinct type/package identity; no accidental type unification.

Install/resolve/check do not run arbitrary build hooks. Native tool invocation is declared and surfaced to the caller. Any future executable hook needs a separate opt-in policy and OS-enforced sandbox design; configuration alone is not a sandbox. Fetching and execution are separate stages. Archive extraction enforces root containment, link policy and size limits. Registry identity, signing/provenance, revocation and advisory metadata require dedicated review.

Reproducibility records compiler/backend/runtime, target/sysroot, source inputs and semantic flags; paths/timestamps/random seeds must be controlled when bit-for-bit builds become a supported claim. SBOMs derive from the actual graph and native dependencies, not only manifest names.

## Options, advantages, disadvantages and rejected alternatives

Implicit latest-version resolution was rejected for reproducibility. Arbitrary install-time scripts were rejected for supply-chain risk. Designing a hosted registry in Phase 2 was rejected as implementation scope. A local-first schema plus future locked graph is proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: integrity, provenance and publisher identity are distinct checks. Performance: content-addressed caches reduce repeated work but must validate inputs. DX: dependency updates are explicit and conflicts explain the chain. Implementation: schema/resolver/cache interfaces are separate from registry hosting.

## Future verification

Later test offline locked builds, tampered artifacts, cyclic/conflicting dependencies, malicious archives, path traversal, source substitution and clean-vs-cached reproducibility.

## Risks and open questions

Manifest/lock syntax, resolver algorithm, signing trust roots and registry protocol are DEFERRED follow-up decisions; their security properties above constrain those decisions.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
