# Platform requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

> **No platform is currently supported.** No compiler or runtime exists. The platforms below are **candidates**, meaning target requirements. A platform may be described as supported only after it meets the criteria in [PLAT-005](#plat-005--criteria-for-official-support).

Terminology, layers and targets are defined in the [requirements framework](README.md).

## Contents

- [Tier model](#tier-model)
- [Candidate platforms](#candidate-platforms)
- [Support policy requirements](#support-policy-requirements)
- [Portability requirements](#portability-requirements)

## Tier model

| Tier | Meaning once support is claimed |
| --- | --- |
| **Tier 1** | The full toolchain, runtime and standard library are built and tested on every change, in CI on the real platform. Release artifacts are published. Failures block releases. |
| **Tier 2** | Built in CI and released. Tests run at least before each release. Failures are documented and fixed on a best-effort basis. They do not automatically block a release. |
| **Tier 3 / Exploratory** | May build. No testing or artifact commitments. Community-maintained where applicable. |

## Candidate platforms

| Platform | Candidate tier | Rationale |
| --- | --- | --- |
| Linux x86-64 | Tier 1 | Dominant server, CI and container platform. Primary platform for networking and DevOps. |
| Windows x86-64 | Tier 1 | Major developer and enterprise automation platform. |
| macOS ARM64 (Apple silicon) | Tier 1 | Major developer workstation platform. |
| Linux ARM64 | Tier 2 | Growing cloud-server and edge platform. |
| macOS x86-64 | Tier 2 | Older Mac developer hardware still in use. |
| WebAssembly | Future | Sandboxed plugins, edge compute, playground ([INTOP-016](INTEROPERABILITY.md#intop-016--webassembly-modules)). |
| RISC-V 64-bit | Future | Emerging open ISA. |
| Embedded / bare metal | Future | Requires a freestanding library subset. Not an initial goal ([NON-GOALS.md](NON-GOALS.md)). |

## Support policy requirements

### PLAT-001 — Published tier policy

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** The project must publish, and keep current, a platform support table. The table must state each platform's tier and the date and release in which the tier was last verified.
- **Rationale:** Users need to know what "supported" means before they depend on it.
- **Verification:** Inspection at release review.

### PLAT-002 — Tier 1 candidates

- **Priority:** MUST · **Layer:** Process · **Target:** Before 1.0
- **Requirement:** Linux x86-64, Windows x86-64 and macOS ARM64 must reach Tier 1 before a 1.0 release. The v0.1 milestone must meet the support criteria on at least one of them, and SHOULD meet them on all three. Only platforms that meet the criteria may be described as supported.
- **Rationale:** These three cover most developer workstations and servers for the [target developers](../vision/TARGET-USERS.md). Early portability prevents platform assumptions from becoming entrenched.
- **Verification:** Platform CI.

### PLAT-003 — Tier 2 candidates

- **Priority:** SHOULD · **Layer:** Process · **Target:** Before 1.0
- **Requirement:** Linux ARM64 and macOS x86-64 should reach Tier 2 before a 1.0 release.
- **Rationale:** Significant user bases with low incremental cost once Tier 1 works.
- **Verification:** Platform CI.

### PLAT-004 — Future platform candidates

- **Priority:** MAY · **Layer:** Process · **Target:** Exploratory
- **Requirement:** WebAssembly, RISC-V 64-bit and embedded targets may be pursued once Tier 1 platforms are established. The Phase 2 architecture should record whether each is precluded.
- **Rationale:** Keeps options open without diluting early effort.
- **Verification:** Design review.

### PLAT-005 — Criteria for official support

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** A platform may be described as officially supported at a given tier only when all of the following hold:
  1. The compiler builds for, or runs on, the platform as applicable.
  2. The runtime builds for the platform.
  3. The standard-library test suite passes on the platform.
  4. The language conformance test suite passes on the platform.
  5. CI runs these checks on the real platform, or on an emulator documented as equivalent.
  6. Release artifacts with checksums are published for the platform.
  7. Known limitations are documented.
  8. A maintainer or team is responsible for the platform.
- **Rationale:** Required by [ENGINEERING.md](https://github.com/Cretes-lang/.github/blob/main/ENGINEERING.md) and [VERSIONING.md](https://github.com/Cretes-lang/.github/blob/main/VERSIONING.md). Prevents claiming support that does not exist.
- **Verification:** Inspection at release review.

### PLAT-010 — Documented minimum OS versions

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** For each supported platform, the minimum operating-system version and required system libraries must be documented.
- **Rationale:** Automation and DevOps users deploy to heterogeneous fleets.
- **Verification:** Inspection.

### PLAT-011 — Tier changes

- **Priority:** MUST · **Layer:** Process · **Target:** v0.1
- **Requirement:** Promoting or demoting a platform's tier must be recorded publicly with its rationale. A demotion must be announced in release notes.
- **Rationale:** Users need warning when a platform's support level changes.
- **Verification:** Inspection.

## Portability requirements

### PLAT-006 — Portable behavior

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Programs that use only portable standard-library interfaces must behave consistently on all supported platforms, except for platform differences that the documentation explicitly enumerates ([CORE-026](CORE.md#core-026--platform-independent-semantics)).
- **Rationale:** Portability is a design principle ([Principle 8](../principles/DESIGN-PRINCIPLES.md#8-cross-platform-design)).
- **Verification:** Conformance tests and unit tests under Platform CI.

### PLAT-007 — Explicit platform-specific code

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Code that applies only to certain target platforms must be explicitly marked. The toolchain must be able to include or exclude it based on the target. Platform-specific standard-library interfaces must be separate from portable interfaces.
- **Rationale:** Prevents accidental non-portability while keeping platform features accessible ([INTOP-010](INTEROPERABILITY.md#intop-010--operating-system-api-access)).
- **Verification:** Conformance tests.

### PLAT-008 — Cross-compilation

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** The toolchain should be able to produce artifacts for a target platform different from the host, given the target's required libraries.
- **Rationale:** DevOps pipelines build for many targets from one CI environment.
- **Verification:** Platform CI.

### PLAT-009 — Filesystem and path portability

- **Priority:** MUST · **Layer:** Standard library · **Target:** v0.1
- **Requirement:** Standard-library path handling must account for each platform's path separators, roots and drive letters, case sensitivity, and paths that are not valid Unicode. It must do so without loss or corruption ([AUTO-008](domains/automation.md#auto-008--path-abstraction)).
- **Rationale:** Path handling is the most common source of cross-platform bugs in automation code.
- **Verification:** Unit tests under Platform CI.

### PLAT-012 — Minimal external runtime dependencies

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** Post-v0.1
- **Requirement:** Built executables should depend only on system libraries that are present by default on the documented minimum OS version. Where the platform permits, a fully self-contained build should be possible.
- **Rationale:** Simplifies deployment to servers, containers and air-gapped environments.
- **Verification:** Platform CI.

### PLAT-013 — Toolchain installation

- **Priority:** MUST · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** For each supported platform, there must be a documented installation method that verifies artifact integrity using published checksums or signatures ([SEC-032](domains/cybersecurity.md#sec-032--toolchain-release-integrity)).
- **Rationale:** The toolchain is the root of trust for every program built with it.
- **Verification:** Inspection; Integration tests.

### PLAT-014 — Consistent toolchain behavior across hosts

- **Priority:** SHOULD · **Layer:** Toolchain · **Target:** v0.1
- **Requirement:** For the same target, the toolchain should produce the same diagnostics and program behavior regardless of which supported host platform runs it.
- **Rationale:** Teams working on mixed operating systems need consistent results. This supports [CORE-025](CORE.md#core-025--deterministic-compilation).
- **Verification:** Platform CI.

## Related documents

- [Interoperability requirements](INTEROPERABILITY.md)
- [Non-goals](NON-GOALS.md)
- [v0.1 requirements](V0.1-REQUIREMENTS.md)
- [Engineering standards](https://github.com/Cretes-lang/.github/blob/main/ENGINEERING.md)
