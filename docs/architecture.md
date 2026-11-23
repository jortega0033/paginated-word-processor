# Implementer map

Status: **only the scaffold exists, no product behaviour.** The modules are stubs with one-line responsibilities. This page maps the boundaries that [PROJECT-PLAN.md](PROJECT-PLAN.md) requires onto a module layout so that parallel tickets do not collide. It adds no requirement; the plan wins where they differ. The names are the orchestrator's proposal, fixed by the scaffold; a ticket that changes one corrects this page in the same pull request.

## Planned module map

| Boundary | Module | Owns | Parent ticket |
|---|---|---|---|
| Command line | `word_processor/cli.py`, `word_processor/__main__.py` | Help, version, `serve` and the report-only `preflight` | #2, #3 |
| Document model | `word_processor/model.py` | Blocks, runs, caps, normalisation, canonical equality, schema version | #2 |
| HTTP | `word_processor/server.py` | Loopback bind, guards, the four routes, static assets | #2, then each route with its ticket |
| Editor | `word_processor/static/ (editor)` | Block editor, keyboard, focus, status text | #2 |
| Layout planner | `word_processor/static/layout.mjs` | Line fragments, vertical position, page manifest | #3 |
| Preview and print | `word_processor/static/ (preview, print)` | A4 pages from the manifest, print CSS | #3 |
| Storage | `word_processor/storage.py` | Data folder, lock, atomic publication, revisions | #4 |
| DOCX writer | `word_processor/docx_write.py` | Package, relationships, main document, manual breaks | #5 |
| DOCX reader | `word_processor/docx_read.py` | Bounded package reading, subset check, typed errors, candidate | #6 |
| Fixtures | `word_processor/fixtures/, tests/fixtures/` | Lantern Inventory and Tally Rows; independent packages | #2, #3, #5, #6 |
| Records | `docs/architecture.md`, `docs/docx-profile.md`, `docs/verification.md` (the last two are written by their tickets) | Contracts, DOCX profile and typed errors, verification record | #2, #5, #7 |
| Tests | `tests/` | `unittest` for Python, `node --test` for the planner | every ticket |

Dependency direction: `cli` depends on `server`; `server` depends on `model`, `storage`, `docx_write` and `docx_read`; those depend on `model` only. `model` imports nothing from the package. The planner imports nothing from the editor.

## Freeze points

Parallel tickets rely on these shapes. A ticket that changes a frozen shape updates this page and every dependent ticket in the same pull request.

- **Document model version 1**, normalisation and the four API shapes with their error types: ticket #2.
- **Geometry profile and page manifest** (pages, lines, positions, fragments): #2 writes the profile, #3 the manifest.
- **DOCX package and XML subset**, and the typed error list: #5 documents it before #6 starts.

## What is verified where

Python tests run locally and in CI on Linux and Windows; planner tests run under `node --test`. Print checks use Chrome (`--headless --print-to-pdf` or a manual print, the pull request says which). Writer checks run where LibreOffice is installed and are owner checks otherwise.
