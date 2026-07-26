# Security Policy

## Supported Versions

Featuresmith is currently in active development (Phase 1). Security fixes are applied to the latest development version only.

| Version | Supported |
|---------|-----------|
| `0.1.0` (current) | ✅ Supported |
| Earlier versions | ❌ Not maintained |

---

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Featuresmith, please **do not open a public GitHub issue**. Instead, follow the responsible disclosure process below.

### How to Report

1. **Email or private GitHub issue** — contact the maintainer privately via:
   - GitHub: Open a [private security advisory](https://github.com/adityagangwani30/FeatureSmith/security/advisories/new) (preferred — keeps the report confidential and tracked)
   - If GitHub security advisories are unavailable, contact the repository owner directly via GitHub profile.

2. **Include in your report:**
   - A description of the vulnerability and its potential impact
   - Steps to reproduce the issue
   - Affected version(s)
   - Any suggested mitigations or patches (optional but appreciated)

3. **What to expect:**
   - Acknowledgement within **48 hours**
   - An initial assessment within **7 days**
   - A patch or mitigation timeline communicated within **14 days** for confirmed vulnerabilities
   - Credit in the changelog and release notes (unless you prefer to remain anonymous)

---

## Security Design Considerations

Featuresmith is designed with several security properties in mind:

### Data Privacy

- **No raw data ever sent to cloud AI providers by default.** The AI layer (Phase 2+) only receives precomputed, structured `ProfileResult` and `RuleFinding[]` objects — never raw rows, column values, or PII. This is an architectural contract enforced in `Architecture.md §7.2` and tested structurally.
- **Cloud AI is opt-in.** The default is local-only analysis (no network calls required). OpenAI/Anthropic integration requires an explicit `ai.provider: openai` config value.
- **API keys are never logged or exported.** Keys are read from environment variables referenced by name in `.featuresmith.yml` — never written into config files, reports, or generated notebooks.

### SQL Connectors (Phase 5+)

- SQL connectors will use parameterized queries exclusively. No string-interpolated SQL is permitted — enforced via code review and documented in `Rules.md §13`.

### Dependency Security

- Dependencies are scanned for known vulnerabilities via `pip-audit` in CI on every PR that touches a `pyproject.toml` file in the workspace.
- New third-party dependencies require an Architecture Decision Record (ADR) in `docs/adr/` before being added.

### Telemetry

- Featuresmith does not collect telemetry by default. Any future opt-in telemetry will be documented in a public `TELEMETRY.md`, will be aggregate-only, and will never include column names, data values, or AI chat content.

---

## Scope

The following are **in scope** for security reports:

- Vulnerabilities in `featuresmith-core`, `featuresmith-cli`, or `featuresmith-dashboard`
- Data leakage paths that could expose raw data to unintended destinations
- Dependency vulnerabilities with a realistic exploitation path
- Authentication/authorization issues in future hosted-tier components

The following are **out of scope:**

- Vulnerabilities in third-party dependencies without a realistic exploitation path in Featuresmith
- Issues requiring physical access to a user's machine
- Social engineering attacks

---

## Disclosure Policy

Once a fix is available and deployed, we will:

1. Publish a GitHub Security Advisory
2. Reference the CVE (if applicable)
3. Include a summary in `CHANGELOG.md`
4. Credit the reporter (unless anonymity is requested)

We follow a **coordinated disclosure** model — please give us reasonable time to prepare and release a fix before any public disclosure.
