# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Answer each Lute v3 constitution gate before design work begins, then re-check
after Phase 1 design:

- **Reader experience**: Does this affect reading, token selection, term popups,
  term editing, navigation, audio controls, paging, or text rendering? If yes,
  describe how desktop behavior remains stable.
- **Domain semantics**: Does this affect texts, languages, terms, term statuses,
  word identifiers, token ordering, parser output, or rendered `span.textitem`
  data attributes? If yes, describe the compatibility expectation.
- **Testing**: List the focused verification command(s), choosing from pytest,
  `inv test`, `inv accept`, `inv acceptmobile`, `inv playwright`, or a documented
  reason a required command cannot be run.
- **Mobile impact**: Does this affect selection, scrolling, long-press behavior,
  or touch flows? If yes, include mobile acceptance coverage.
- **Architecture fit**: Confirm the plan uses existing Flask templates, Python
  helpers, jQuery-style JavaScript, and local CSS/JS patterns unless explicitly
  justified.
- **Data safety**: Confirm no user-local data/config is mutated unexpectedly and
  DB-resetting tasks only run against databases whose names start with `test_`.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Keep the tree focused on real Lute paths affected by this
  feature. Delete unaffected paths and add specific modules/templates/tests as
  needed. Do not introduce a new frontend/backend project split unless the
  feature explicitly requires and justifies it.
-->

```text
lute/
├── read/
├── read/render/
├── templates/read/
├── static/js/lute.js
└── static/css/styles.css

tests/
├── unit/
├── acceptance/
└── playwright/
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
