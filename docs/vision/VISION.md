# Cretes language vision

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

This is the canonical statement of what Cretes is, why it exists and where it is heading. It extends the Phase 0 [identity record](https://github.com/Cretes-lang/.github/blob/main/IDENTITY.md).

> **Current status.** Cretes has completed its project-foundation phase (Phase 0) and is defining requirements (Phase 1). **No compiler, runtime, standard library, syntax or release exists.** Every capability described in this document is an aspiration or a requirement, not an available feature.

## Identity

| Field | Value |
| --- | --- |
| Name | Cretes |
| Type | General-purpose programming language |
| Source extension | `.cretes` |
| Primary domains | Automation · Networking · AI/ML Applications · Cybersecurity |
| License | Apache-2.0 |
| Home | [github.com/Cretes-lang](https://github.com/Cretes-lang) |

## Mission

**Cretes is a modern general-purpose programming language for building automation, networked systems, AI/ML applications and security-critical software that is safe by default, predictable in performance, and pleasant to develop and operate.**

Cretes is general-purpose. It is not a domain-specific language. The four domains are its **design drivers**: they supply the concrete requirements that shape the language, runtime, standard library and tooling. A capability exists in Cretes because the domains need it, not because other languages have it.

## Why Cretes exists

Engineers in these four domains commonly face a recurring set of trade-offs:

- **Convenience versus safety.** Languages that make quick automation and prototyping easy often leave memory safety, error handling or concurrency correctness to discipline and testing.
- **Performance versus approachability.** Languages that give predictable native performance and low-level control often demand significant expertise before a newcomer is productive.
- **Integration friction.** AI/ML runtimes, cryptographic libraries and operating-system facilities live in native code. Crossing into them is often where safety guarantees end and bugs begin.
- **Operational gaps.** Timeouts, cancellation, backpressure, structured errors and secret handling are frequently added by libraries after the fact, inconsistently.
- **Supply-chain exposure.** Package ecosystems that run arbitrary code at install time, or lack integrity verification, turn every dependency into a risk.

Cretes aims to reduce these trade-offs. It does not claim to eliminate them. Each language makes deliberate choices, and Cretes will too. Its choices are recorded in the [design principles](../principles/DESIGN-PRINCIPLES.md), and its obligations in the [requirements](../requirements/README.md).

## Design aspirations

These are aspirations. They become obligations only through specific requirements, which are linked here.

| Aspiration | What it means for Cretes | Anchoring requirements |
| --- | --- | --- |
| **Approachable development** | Small programs are short and direct. A single file runs with one command. Large programs grow without rewrites. | [AUTO-001](../requirements/domains/automation.md#auto-001--single-file-programs), [CORE-020](../requirements/CORE.md#core-020--reduced-annotation-burden) |
| **Predictable performance** | Costs are documented and visible. Performance is measured, never assumed. | [PERF-002](../requirements/PERFORMANCE.md#perf-002--documented-cost-model), [PERF-017](../requirements/PERFORMANCE.md#perf-017--evidence-before-claims) |
| **Strong safety properties** | No undefined behavior in safe code. Memory, null, type and data-race safety are required outcomes. | [SAFE-001](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code), [SAFE-012](../requirements/SAFETY.md#safe-012--data-race-freedom) |
| **Modern concurrency** | Structured tasks, cancellation, deadlines and backpressure are foundations, not add-ons. | [CONC-004](../requirements/CONCURRENCY.md#conc-004--structured-concurrency), [CONC-006](../requirements/CONCURRENCY.md#conc-006--cancellation) |
| **Portability** | The same program behaves the same on Linux, Windows and macOS. Differences are enumerated. | [CORE-026](../requirements/CORE.md#core-026--platform-independent-semantics), [PLAT-006](../requirements/PLATFORMS.md#plat-006--portable-behavior) |
| **Interoperability** | The C ABI is the bridge to operating systems, native libraries and AI runtimes. The safety boundary at that bridge is explicit. | [INTOP-001](../requirements/INTEROPERABILITY.md#intop-001--calling-c-abi-functions), [SAFE-018](../requirements/SAFETY.md#safe-018--ffi-is-an-unsafe-boundary) |
| **High-quality tooling** | Diagnostics, formatting, testing, the language server and package management are part of the language experience. | [DX-005](../requirements/CORE.md#dx-005--diagnostic-content), [DX-011](../requirements/CORE.md#dx-011--integrated-test-runner) |
| **Secure defaults** | Secure randomness, verified TLS, redacted secrets, no shell by default, and no install-time code execution. | [SEC-006](../requirements/domains/cybersecurity.md#sec-006--secure-randomness), [NET-023](../requirements/domains/networking.md#net-023--secure-network-defaults), [SEC-025](../requirements/domains/cybersecurity.md#sec-025--no-implicit-code-execution-during-dependency-installation) |

## Who Cretes is for

Cretes is designed for six developer personas, described in [TARGET-USERS.md](TARGET-USERS.md):

- Automation Engineers;
- Backend / Network Engineers;
- AI/ML Application Developers;
- Cybersecurity Engineers;
- Systems / Tooling Developers;
- DevOps / Platform Engineers.

## Long-term ecosystem

The long-term vision is a complete, coherent ecosystem. The following table describes **intended** components. None exists today.

| Component | Purpose | First expected |
| --- | --- | --- |
| Language specification | Normative definition of syntax and semantics | Incrementally, from Phase 2 |
| Compiler | Checks and builds `.cretes` programs | v0.1 |
| Runtime | Execution support, such as scheduling, I/O and fault handling, to the extent the architecture requires | v0.1 (minimal) |
| Standard library | Portable foundations for the four domains | v0.1 (basic), grows per milestone |
| Package manager | Dependency resolution, verification and building | After v0.1 |
| Package registry | Hosting and discovery of packages with provenance | After v0.1 |
| Formatter | Canonical source layout | After v0.1 |
| Linter | Correctness, security and style analysis | After v0.1 |
| Test runner | Unit, integration and fuzz testing | After v0.1 |
| Documentation generator | API documentation from source | After v0.1 |
| Language server | Editor integration through the Language Server Protocol | After v0.1 |
| Debugger integration | Source-level debugging with platform debuggers | After v0.1 |
| Editor / IDE integration | Syntax support and extensions for popular editors | After v0.1 |
| Playground | Try Cretes in a browser, sandboxed | Long-term |
| Security tooling | Audit of unsafe code and FFI, advisories, SBOM, fuzzing | After v0.1 |

"First expected" states intent only. [V0.1-REQUIREMENTS.md](../requirements/V0.1-REQUIREMENTS.md) is the authoritative scope for v0.1.

## Long-term vision versus v0.1

| | Long-term vision | v0.1 |
| --- | --- | --- |
| Language | Complete general-purpose language, with generics, concurrency and FFI | Core language: values, functions, control flow, modules, types, errors |
| Safety | Memory safety, data-race freedom, auditable unsafe code | Memory safety for all v0.1 code, with no user-visible unsafe code |
| Library | Rich standard and first-party libraries for all four domains | Text, collections, files, streams, arguments, environment, time |
| Tooling | Full toolchain, as in the table above | `cretes check`, `cretes build`, `cretes run` with high-quality diagnostics |
| Platforms | Tier 1 and Tier 2 platforms, and future targets | At least one Tier 1 candidate |
| Domains | Automation, Networking, AI/ML Applications, Cybersecurity | Foundations only. The architecture leaves room for all four. |

## How the vision becomes a language

1. **Phase 0 (complete):** identity, governance, RFC process, repositories.
2. **Phase 1 (this baseline):** vision, users, principles, requirements, scope, v0.1 definition.
3. **Phase 2:** architecture decisions through RFCs, answering the [open questions](../PHASE-2-OPEN-QUESTIONS.md). The questions cover the type system, memory management, execution model, concurrency runtime, error model and FFI.
4. **Later phases:** syntax and semantics are specified, then implemented, tested and released through milestones, starting with v0.1.

Phase ordering follows [GOVERNANCE.md](https://github.com/Cretes-lang/.github/blob/main/GOVERNANCE.md). Changes to language semantics, runtime architecture, compatibility and public APIs require an accepted RFC before implementation.

## Related documents

- [Target developers](TARGET-USERS.md)
- [Design principles](../principles/DESIGN-PRINCIPLES.md)
- [Use cases](../requirements/USE-CASES.md)
- [Requirements framework](../requirements/README.md)
- [Non-goals](../requirements/NON-GOALS.md)
