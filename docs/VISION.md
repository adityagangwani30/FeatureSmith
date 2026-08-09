# VISION.md

> This is the highest-level document in the Featuresmith repository. Every other document — `PRD.md` (what we build), `Architecture.md` (how it's built), `Phases.md` (in what order), `Design-Principles.md` (how we decide), and everything under `features/` — exists to serve one of the four answers below. When a decision is ambiguous anywhere else in this repository, it resolves here first.

---

## 1. Why does Featuresmith exist?

Software engineering spent decades building discipline into the *development loop*: tests, linters, formatters, code review, CI gates. Underneath all of it sits something even more basic — version control and lockfiles, which make the *state* of a codebase provable, diffable, and reproducible, not just its logic testable. None of that was ever controversial. It's just how software gets built now.

Datasets never got any of this. A column can go 40% missing, a categorical can silently leak the target, a distribution can drift out from under a production model — and nothing stops it the way a failing test stops a bad commit, because nothing is watching. Worse, nothing *remembers*: six months after a model ships, "what exactly was this dataset, and was it safe" is a question a team re-derives from scratch, if they can answer it at all.

This isn't because the problem is unrecognized. It's because the tooling that exists is fragmented by design: one tool profiles, another validates, another detects drift, another engineers features, another monitors quality in production. Each is usually good at its one job. None of them talk to each other, and none of them leave behind a record. A team stitches together a workflow instead of using one, and the moment the last person who understood a dataset's history leaves, that history leaves with them.

**Featuresmith exists to close that gap — to give the dataset the same engineering discipline the codebase around it already has.** Not as five separate tools bolted together, but as one continuous, deterministic loop: a dataset is reviewed the way a pull request is reviewed, a fix is planned and applied through the tools a team already trusts, the result is proven to have worked, and the whole thing is recorded into something a team can commit, diff, and gate on — permanently, not just for the duration of one notebook session.

"Every dataset deserves a code review" is how Featuresmith introduces itself — five words that borrow a mental model every engineer already trusts to explain a problem most teams have stopped noticing they have. It's the true, honest entry point. It is not the whole of why Featuresmith exists.

## 2. What category is Featuresmith creating?

Featuresmith is not a better EDA report generator, and it should not be evaluated as one. Tools like `ydata-profiling`, `sweetviz`, and `autoviz` *describe* a dataset. Great Expectations *validates* a pipeline's output against rules someone already wrote. Feature-engineering libraries generate transformations. Each is a single station on an assembly line; none of them is the line itself, and none of them leave behind a record another tool — or another person — can trust later without re-checking everything by hand.

**Featuresmith is building the Dataset Contract layer: the state-management layer for structured data.** Not a feature-engineering framework, not a data-quality dashboard, not another EDA tool with a chat window bolted on — the layer that makes a dataset's *state* a first-class, versioned, provable thing, the way git made a codebase's state a first-class thing and a lockfile made a dependency tree's resolved state a first-class thing.

The clearest way to say what that means concretely: a dataset that has gone through Featuresmith has been **reviewed** (its problems are known), **planned against** (there's an inspectable record of what should change and why), **validated** (a proposed fix was proven, not assumed, to work), and **locked** (its state — schema, quality, leakage, transformation history — is a versioned artifact a team can commit next to their code). Feature engineering is one capability that lives inside this loop, not the reason the loop exists. A team that never uses Featuresmith's transformation-planning capability at all still gets the full value of the category: a dataset whose state is provable instead of assumed.

The right peer set, for calibrating ambition, is not other profiling tools — it's the category-defining developer tools that made an invisible discipline visible and automatic: **git** (state and diff, applied to data instead of code), **Terraform** (plan → apply → state, applied to dataset transformations instead of infrastructure), **dbt** (turning a pile of scripts into a documented, tested, versioned artifact, applied to dataset state instead of SQL models), and **Ruff** or **uv** (the bar for "zero-config, fast, and trusted enough to just run"). None of those tools are impressive because of their feature count. They're impressive because they made something that used to be tribal knowledge and manual discipline into something a machine just handles, silently, every time.

## 3. What will Featuresmith intentionally NOT become?

Every one of these is a permanent boundary, not a phase-limited caveat — each exists because it's a category Featuresmith has no structural advantage in, and reaching into it would dilute the one advantage Featuresmith is actually building: **being trusted to tell the truth about a dataset's state.**

- **Not an orchestrator.** Featuresmith plans and validates a transformation; it does not schedule, retry, or run a DAG. That's Airflow, Dagster, and Prefect's job, and an exported pipeline is simply a step they can call.
- **Not an execution engine.** No Featuresmith-owned runtime, ever — not for a single machine, and not distributed. Every transformation Featuresmith recommends compiles to real, readable code for an ecosystem a team already runs — Polars, pandas, scikit-learn, dbt — that a person can read, run, and own entirely outside Featuresmith. The moment Featuresmith needs its own scheduler or its own execution state, something has gone wrong.
- **Not a feature store.** Featuresmith does not serve features online or manage serving-time versioning. It exports to feature stores that already do that job well.
- **Not an AutoML or model-training system.** Featuresmith's recommendations are about the data. The instant a suggestion is about a hyperparameter instead of a dataset, it's out of scope — that's a different job entirely, done by different tools, for a different kind of trust.
- **Not a no-code platform.** Every capability is developer-first — importable, scriptable, pipeable — before it ever has a UI. A dashboard that could be operated by someone who's never seen the underlying code is a different product than this one.
- **Not a data warehouse.** Featuresmith certifies data wherever it lives; it doesn't ask a team to move it somewhere else first.
- **Not a replacement for judgment.** Every recommendation, every plan, is advisory — reviewable, editable, rejectable — right up until a human explicitly accepts it. Featuresmith proves what happened; it never decides unilaterally what should.

The shape of all seven: Featuresmith owns the loop of *understanding, planning, validating, and proving* — and stops, deliberately, at the edge of *executing*. That boundary is what keeps this a lockfile, not an operating system.

## 4. What is the long-term North Star?

> **No dataset should silently break a pipeline, a model, or a decision — Featuresmith makes the state of a dataset as versioned, provable, and reviewable as the state of code.**

Everything in this repository is in service of that sentence. A phase on the roadmap that doesn't move Featuresmith closer to it is worth questioning, no matter how useful it looks in isolation. Success, at any point in this project's life, looks the same way: a team can answer *"what exactly was this dataset, and is it safe to build on"* in one command, backed by a record they trust — instead of an afternoon, a Slack thread, and a guess.
