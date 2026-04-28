# Repository Guidelines

## Project Shape

This repository is a copy of Lute v3, a Python/Flask app for reading texts and managing language-learning terms.

- Flask app code lives under `lute/`.
- Reading UI templates live under `lute/templates/read/`.
- The main reading interaction JavaScript is `lute/static/js/lute.js`.
- The main stylesheet is `lute/static/css/styles.css`.
- Read/render domain logic lives under `lute/read/` and `lute/read/render/`.
- Tests live under `tests/`, with slower browser flows under `tests/acceptance/` and `tests/playwright/`.

## Development Commands

Use Invoke tasks from the repo root:

- `inv start --port 5001` starts the dev server.
- `inv test` runs non-acceptance tests.
- `inv accept` runs desktop acceptance tests.
- `inv acceptmobile` runs mobile-emulated acceptance tests marked `@mobile`.
- `inv playwright` runs the recorded Playwright smoke test.
- `inv lint` runs pylint.
- `inv black` formats Python code.

Important: most Invoke test tasks first verify that the configured DB name starts with `test_`. Do not run DB-resetting tasks against a non-test database.

## Coding Notes

- Prefer existing Flask templates, jQuery-style JavaScript, and local helper functions over introducing a new frontend framework.
- Keep desktop reading behavior stable when changing mobile interactions.
- Multi-word term creation already uses `/read/termform/<langid>/<text>`.
- Single-term editing already uses `/read/edit_term/<term_id>`.
- Text tokens in the reader are rendered as `span.textitem` elements with useful `data-*` attributes such as `data-order`, `data-lang-id`, `data-wid`, and status classes.
- On mobile, be careful with native browser text selection, scrolling, and long-press behavior. Prefer Lute-owned visual selection state over relying on OS selection handles.

## Testing Guidance

- For backend/rendering changes, start with focused `pytest` or `inv test`.
- For reader UI changes, add or update acceptance scenarios in `tests/acceptance/reading.feature`.
- For mobile reader changes, use `inv acceptmobile -k "<scenario name>"` and verify the flow under iPhone emulation.
- Browser tests can be slow and flaky; keep new scenarios narrow and behavior-focused.

## Git Hygiene

- Do not revert user changes unless explicitly asked.
- Keep edits scoped to the requested behavior.
- Avoid unrelated formatting churn, especially in large CSS/JS files.
