# GitHub Repository Recommendations — Featuresmith

This document provides recommended GitHub repository settings for the first public release.
These must be applied manually through the GitHub repository settings UI.

---

## 1. Repository Description

**Suggested description (160 characters max):**

> Open-source developer-first toolkit for structured data profiling, rules validation, and improvement. Make data quality as routine as code quality. SDK+CLI.

---

## 2. Repository Topics / Tags

Apply these topics to make the repository discoverable:

```
data-quality
data-validation
profiling
tabular-data
developer-tools
python
polars
pandas
cli
rule-engine
mlops
open-source
data-science
machine-learning
```

**How to apply:** Repository → About (gear icon) → Topics

---

## 3. Repository Homepage

The documentation website is the Next.js app in `frontend/`:

```
https://featuresmith.adityagangwani.me
```

Until then, leave blank or point to the GitHub repository itself.

---

## 4. Social Preview Image

Create a 1280×640px social preview image for rich link previews (Twitter, Slack, LinkedIn).

**Suggested content:**
- Dark background (`#0F1115` from the design system)
- Featuresmith wordmark in Inter font
- Tagline: *"Deterministic feature engineering & data quality for Python"*
- Key stats: "5 connectors · 8 rules · SDK + CLI"
- Accent color highlights (`#2F6FED`)

**How to apply:** Repository → Settings → Social Preview

---

## 5. Suggested Repository Labels

Apply these labels to create a structured, contributor-friendly issue tracker:

| Label | Color | Description |
|-------|-------|-------------|
| `bug` | `#D64545` | Confirmed reproducible bug |
| `enhancement` | `#2F6FED` | New feature or improvement |
| `question` | `#5B6270` | Usage or design question |
| `good-first-issue` | `#54B384` | Ideal for first-time contributors |
| `help-wanted` | `#D98A2B` | Help from community needed |
| `core` | `#5B8DEF` | Affects featuresmith-core |
| `cli` | `#9AA1AE` | Affects featuresmith-cli |
| `dashboard` | `#9AA1AE` | Affects featuresmith-dashboard |
| `rules` | `#E3A857` | New or modified rule |
| `connectors` | `#E3A857` | New or modified connector |
| `ai-layer` | `#D64545` | AI provider / narration / chat |
| `exporters` | `#E3A857` | New or modified exporter |
| `infra` | `#5B6270` | CI, tooling, packaging |
| `docs` | `#54B384` | Documentation only |
| `needs-triage` | `#D98A2B` | Awaiting maintainer review |
| `duplicate` | `#E4E6EB` | Already reported |
| `wontfix` | `#E4E6EB` | Out of scope per PRD |
| `breaking-change` | `#D64545` | Breaking public API change |
| `performance` | `#2F6FED` | Performance regression or improvement |
| `security` | `#D64545` | Security vulnerability |
| `phase-2` | `#1B2333` | Planned for Phase 2 (AI layer) |
| `phase-3` | `#1B2333` | Planned for Phase 3 (AI Chat) |
| `phase-4` | `#1B2333` | Planned for Phase 4 (Export) |
| `phase-5` | `#1B2333` | Planned for Phase 5 (Dashboard) |

---

## 6. GitHub Discussions Categories

Enable GitHub Discussions and create these categories:

| Category | Format | Purpose |
|----------|--------|---------|
| 📣 Announcements | Announcement | Release notes, major updates (maintainer-only posting) |
| 💬 General | Open-ended discussion | General conversation about Featuresmith |
| 💡 Ideas | Open-ended discussion | Feature ideas and design discussions before formal issues |
| ❓ Q&A | Question / Answer | Usage questions (community can mark answers) |
| 🔌 Show & Tell | Open-ended discussion | Community showcases: integrations, workflows, use cases |
| 🛠️ Contributing | Open-ended discussion | Questions about contributing, PRs, extension development |

---

## 7. Branch Protection Rules

Apply to the `main` branch:

- ✅ Require a pull request before merging
- ✅ Require at least 1 approving review (2 for `featuresmith-core/core/` and `api.py` per Rules.md §6)
- ✅ Require status checks to pass before merging: `CI / test`
- ✅ Require branches to be up to date before merging
- ✅ Do not allow bypassing the above settings

---

## 8. Repository Features to Enable

- ✅ Issues
- ✅ Discussions
- ✅ Projects (for roadmap tracking per phase)
- ✅ Wiki — disabled (docs live in `docs/` and the Next.js documentation website in `frontend/`)
- ✅ Sponsorships (optional, for future sustainability)

---

## 9. Suggested GitHub Projects Boards

Create one project board per active phase:

| Board | Status |
|-------|--------|
| v0.1 Launch (Phase 1 complete) | Archive after release |
| v0.3 AI Layer (Phase 2) | Active next |

Use the **Roadmap layout** for high-level phase views and **Board layout** for sprint work.

---

## 10. Repository Insights / Community Health

After publishing, check the **Community** tab in GitHub Insights. The following files will satisfy all community health requirements:

- ✅ `README.md`
- ✅ `CODE_OF_CONDUCT.md`
- ✅ `CONTRIBUTING.md`
- ✅ `LICENSE`
- ✅ `SECURITY.md`
- ✅ `.github/ISSUE_TEMPLATE/`
- ✅ `.github/PULL_REQUEST_TEMPLATE.md`
