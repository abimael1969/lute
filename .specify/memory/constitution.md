<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Template principle 1 -> I. Reader Experience Comes First
- Template principle 2 -> II. Preserve Lute Domain Semantics
- Template principle 3 -> III. Risk-Based Testing Is Required
- Template principle 4 -> IV. Existing Architecture First
- Template principle 5 -> V. Safe Data and Configuration Handling
Added sections:
- Technical Constraints
- Development Workflow
Removed sections:
- Template placeholder sections
Templates requiring updates:
- .specify/templates/plan-template.md: updated
- .specify/templates/spec-template.md: updated
- .specify/templates/tasks-template.md: updated
Follow-up TODOs: none
-->

# Lute v3 Constitution

## Core Principles

### I. Reader Experience Comes First

Changes that affect reading, token selection, term popups, term editing,
navigation, audio controls, paging, or text rendering MUST preserve the reading
flow for existing users. Desktop reading behavior MUST remain stable unless the
feature explicitly changes it. Mobile interactions MUST avoid relying on native
browser text-selection handles when Lute-owned selection state can provide a
more predictable experience.

Rationale: Lute's core value is learning through uninterrupted reading, so the
reader UI is the highest-risk surface.

### II. Preserve Lute Domain Semantics

Features MUST respect existing semantics for texts, languages, terms, term
statuses, word identifiers, token ordering, parser output, and rendered
`span.textitem` data attributes. Multi-word term creation MUST continue to use
the existing reader flow unless a feature explicitly replaces it. Rendering
changes MUST account for both backend domain behavior and frontend token
interaction behavior.

Rationale: Small changes to term or token semantics can silently damage reading,
review, import, and editing workflows.

### III. Risk-Based Testing Is Required

Every change MUST include verification proportional to its risk. Backend,
parser, rendering, and model changes require focused pytest coverage or
`inv test`. Reader UI changes require focused acceptance coverage in
`tests/acceptance/reading.feature` or an equivalent existing acceptance suite.
Mobile reader changes involving selection, scrolling, long-press behavior, or
touch flows require `inv acceptmobile -k "<scenario name>"` or a documented
reason when the test cannot be run.

Rationale: Lute has both domain-heavy backend behavior and fragile browser
interaction surfaces; testing must match the affected surface.

### IV. Existing Architecture First

Implementation MUST prefer the current Flask templates, Python helpers,
SQLAlchemy-backed models, jQuery-style JavaScript, and local CSS/JS patterns.
New frontend frameworks, broad abstractions, or large styling rewrites are NOT
allowed unless the feature explicitly requires them and the implementation plan
justifies the added complexity.

Rationale: Lute is an established Flask application, and isolated changes are
safer than architectural churn.

### V. Safe Data and Configuration Handling

Commands that reset, migrate, or mutate application data MUST only run against
test databases when the Invoke task requires it. The configured database name
MUST start with `test_` before running DB-resetting test tasks. User-local
configuration, private data, imported books, and generated user assets MUST NOT
be modified unless the feature explicitly targets them and includes a recovery
or verification path.

Rationale: Lute manages personal language-learning data, so local data safety is
part of correctness.

## Technical Constraints

Lute v3 is a Python/Flask application using SQLAlchemy-backed models and
server-rendered templates. Flask app code lives under `lute/`, reader templates
under `lute/templates/read/`, reader interaction JavaScript in
`lute/static/js/lute.js`, and the main stylesheet in
`lute/static/css/styles.css`.

Read/render domain logic lives under `lute/read/` and `lute/read/render/`.
Tests live under `tests/`, with slower browser flows under `tests/acceptance/`
and Playwright smoke coverage under `tests/playwright/`.

Development commands MUST use the repo's Invoke tasks where available:
`inv test`, `inv accept`, `inv acceptmobile`, `inv playwright`, `inv lint`, and
`inv black`.

## Development Workflow

Spec Kit features MUST move from specification to plan to tasks to
implementation. Each feature plan MUST declare whether it affects desktop
reader behavior, mobile reader behavior, domain/rendering semantics, data
safety, and architecture fit.

Generated tasks MUST identify the expected verification command for each
affected surface. If a feature touches reader UI behavior, tasks MUST include
acceptance coverage or explicitly document why existing coverage is sufficient.
If a feature touches mobile reader behavior, tasks MUST include mobile
acceptance coverage or an explicit reason it cannot be run.

Implementation MUST keep edits scoped to the requested behavior and avoid
unrelated formatting churn, especially in large CSS and JavaScript files.

## Governance

This constitution supersedes Spec Kit templates, generated plans, generated
tasks, and `AGENTS.md` when they conflict. `AGENTS.md` remains the practical
runtime guide for commands and repository layout, but feature decisions MUST
satisfy this constitution.

Amendments MUST include a Sync Impact Report, update dependent Spec Kit
templates when needed, and use semantic versioning:

- MAJOR: Removes or redefines a core principle in a backward-incompatible way.
- MINOR: Adds a principle, required workflow, or materially expands governance.
- PATCH: Clarifies wording without changing required behavior.

Plans and code reviews MUST check compliance with the core principles before
implementation work begins and again before delivery.

**Version**: 1.0.0 | **Ratified**: 2026-05-01 | **Last Amended**: 2026-05-01
