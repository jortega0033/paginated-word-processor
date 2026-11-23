# CLAUDE.md

Working instructions for this repository. Read this file first, then the documents it links to. It does not repeat them.

## What this is

A local workbench for a writer of a short report: edit ordered blocks with an A4 preview, save and resume one draft, print a PDF, and exchange a small DOCX profile that opens in LibreOffice Writer. Python 3 standard library, `127.0.0.1` only, bundled browser assets, original sample reports.

**Nothing is implemented yet.** The repository holds the plan, the delivery tooling and the backlog in epic #1. Commands marked planned below do not work yet. Do not describe a planned thing as working, and do not claim a passing baseline: there is none.

## Sources of truth

| Topic | Document |
|---|---|
| Product scope, design, fixtures with expected values | [docs/PROJECT-PLAN.md](docs/PROJECT-PLAN.md) |
| Planned module map, freeze points, planned versus implemented | [docs/architecture.md](docs/architecture.md) |
| Backlog | Epic issue #1 and its child tickets on GitHub. The epic's table is authoritative for order, dependencies and estimates; tickets state their own owner-decision defaults. |
| Loop setup and its limits | [LOOP.md](LOOP.md), [loop-constraints.md](loop-constraints.md) |
| Project subagents, origin and local changes | [.claude/agency-agents/README.md](.claude/agency-agents/README.md) |
| Ticket workflow and the step at which each role runs | [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md), section "Agent roles" below |
| How a ticket goes from the queue to a ready pull request, who may do what | "Delivery workflow" below |
| UI and copy rules | [docs/ui-quality.md](docs/ui-quality.md) |
| Decisions the owner made, with dates | [docs/owner-decisions.md](docs/owner-decisions.md) |

The plan wins for product design; the epic and tickets win for order and scope. A ticket that changes a contract fixes the plan in the same pull request.

## Stack and constraints

- Python 3.12, **standard library only**, in the application and in the tests. Browser code is plain modules without a build step.
- Serves bundled HTML, CSS and JavaScript and four JSON or DOCX routes on `127.0.0.1`.
- One draft, fixed A4 portrait, headings, paragraphs with plain and bold runs, two-column tables, manual breaks.
- Offline: same-origin assets only. No CDN, web font, script or telemetry from another host.
- Original sample reports and independently authored packages only.
- Lists, images, headers and footers, tracked changes, collaboration, tables across pages, general Word compatibility and large-document claims are later work.
- A runtime version change, a dependency, an external request or a non-loopback listener needs the owner's approval first, not a pull request.

## Commands

Python 3.12 or 3.13; Node 22 for the planner tests. No install step is needed.

| Purpose | Command | Status |
|---|---|---|
| Tests | `python -m unittest discover -s tests` | planned: real with the scaffold |
| Planner tests | `node --test` | planned: real with the scaffold |
| Help and version | `python -m word_processor --help` | planned: real with the scaffold |
| Run the app | `python -m word_processor serve --port 8766 --data-dir ./data` | planned: #2 |

## Architecture boundaries

The planned module map is in [docs/architecture.md](docs/architecture.md). Invariants every change must keep (the plan is the source):

- Document model, layout planner, storage, DOCX writer, DOCX reader and page stay separate. The planner is a pure module with an injected text measure.
- One flow planner produces one page manifest, used by preview and print. Automatic page breaks are never stored in the model or the DOCX.
- Canonical equality covers title, text, run formatting, table grid, block order and manual breaks; block IDs, geometry and ZIP metadata do not count. Normalising is idempotent and loses no text.
- Caps: 200 blocks, 80,000 Unicode scalar values, tables of two equal columns and up to 12 rows with one paragraph per cell. A violation names the block and keeps the editable draft.
- Geometry in twips: A4 11,906 × 16,838, margins 1,440, content 9,026 × 13,958. Body 12 pt, 360 lines, 120 after. Headings 18 pt, 480 lines, 120 after. Tally Rows splits 29 and 1.
- Lines break at spaces, oversized tokens at supported character boundaries, the stored text never changes. A heading stays with its next body line when the pair fits a fresh page; a table moves as a whole, and one taller than an empty page is flagged.
- PUT carries the base revision. A different saved revision is a typed conflict and the losing tab keeps its edits. Export and import never write a saved revision.
- Save: validate, write a temporary file in the same directory, flush and sync, rename, sync the directory, one writer with a directory lock. A malformed prior revision is reported and never overwritten.
- DOCX import reads into bounded buffers without disk extraction: upload 4 MiB, 32 entries, 2 MiB per XML part, 8 MiB inflated, XML depth and node caps, enforced on declared and observed sizes.
- Reject duplicate or noncanonical part names, unsuitable ZIP methods, encryption, external targets, macros, embedded resources, non-UTF-8 XML, DTD or entity declarations, and unsupported content-bearing XML, each with a specific error. Nothing is dropped silently.
- Export validates first and sends no byte of an invalid document. Text is escaped in XML and in the page; significant spaces survive.
- The server binds `127.0.0.1` only, requires the exact app origin and the documented content type for writes, and builds no path from an HTTP value.
- Every edit, move, insert and delete works by keyboard with predictable focus. Errors, conflicts and unsaved state are text. The preview is read-only.
- Layout results are recorded with the font, Chrome and Writer versions. A missing Liberation Serif is a setup error, and no font is bundled without a licence check and an owner decision.

## Git workflow

- `main` is the default branch. Work on one branch per ticket: `<issue-number>-<short-slug>`. Never commit to `main`.
- Small commits with imperative subjects and a type prefix (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- Order for every ticket: local evidence, Code Reviewer, Reality Checker, then a draft pull request that says `Part of epic #1` and `Closes #<ticket>`, then CI on that draft, then `gh pr ready` only when CI is green.
- Do not push or open a pull request unless the owner asked in the current session; starting `/next-ticket` is that request for one ticket. Only the owner merges and releases. Do not push to `main`, force-push, or merge your own pull request.
- Never commit a data folder (`data/`), `.env*`, or build output.
- Do not change `.claude/agents/`, `LOOP.md`, `loop-constraints.md` or `loop-budget.md` as part of a feature ticket.
- Open owner decisions on a ticket are settled with the ticket's stated default. Where a ticket states none, take the conservative option and say so in the pull request.

## Evidence before a ticket is called done

Paste real output into the pull request; never summarise a run you did not make.

1. For each acceptance criterion of the issue: the name of the test that proves it, or the exact step and what was observed.
2. The full output of `python -m unittest discover -s tests` and `node --test` locally, and the link to the green CI run on the draft pull request (Linux and Windows, Python 3.12 and 3.13).
3. For a layout or print change: the fixture, page count and marker positions, the font and the Chrome version.
4. For an import or export change: the packages run, the rejected cases with their error, and that draft and saved revision were unchanged.
5. For a UI change: the Chrome version, the keyboard path walked and what was observed, and that the page made no external request.
6. `git status` shows no stray files, and no dependency, external URL or non-loopback listener was added.
7. Anything not verified, said plainly.

## Agent roles

Project subagents are in `.claude/agents/`: eight Agency Agents roles and `loop-verifier`, which belongs to the Loop setup. Each Agency Agents role file starts with a section "In this repository", written for this project. That section and this file override the generic text below it. Sources, licence, local changes and the name collision with a user-level install are in [.claude/agency-agents/README.md](.claude/agency-agents/README.md).

When asked to implement, continue or finish a GitHub issue, follow the playbook [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Claude Code loads it on its own for ticket work; `/implement-ticket <issue number>` starts it by hand. Delegate to the roles without waiting to be asked: each role's `description` ends with a "Use proactively ..." sentence, which is what makes Claude Code delegate. The playbook gives the exact trigger of each role.

| When | Roles | Access |
|---|---|---|
| Before coding | Software Architect | `Read, Grep, Glob` |
| While coding | Backend Architect, Frontend Developer | can edit |
| After coding, when the trigger matches | Application Security Engineer, Accessibility Auditor | `Read, Grep, Glob` |
| After coding, when the trigger matches | API Tester | can edit |
| Gate on every ticket | Code Reviewer on the full diff, until no material finding is left | `Read, Grep, Glob` |
| Acceptance gate on every ticket, after Code Reviewer | Reality Checker on each acceptance criterion and the recorded evidence, and that CI is configured to run the checks (no CI result is needed yet) | `Read, Grep, Glob` |

- The two gates run on every ticket, whatever its size. A ticket is not called done before both have passed.
- Roles limited to `Read, Grep, Glob` cannot run commands. Give them the diff, the acceptance criteria and whatever command output exists.
- The session or role that wrote a change does not count as its reviewer.
- If a role is missing or cannot be delegated to, the session does the before-coding, while-coding and specialist steps itself and says so. It cannot pass the two gates on its own change: do not push or open the pull request. Stop, report that the gates could not run, and leave the run for the owner. This overrides the playbook's sentence "do that step yourself" for the two gates.
- In the pull request description, list under "Agent roles run" each role that ran, what it was asked and its verdict, and any step done without a role.

## Delivery workflow

How a ticket reaches the owner. Each piece is described in its own file; this part only links them.

- **Start:** the owner runs `/next-ticket` ([`.claude/skills/next-ticket/SKILL.md`](.claude/skills/next-ticket/SKILL.md)); it picks one leaf ticket (never a `tracking` parent or a ticket with open sub-issues; the last sub-issue's pull request also closes the parent), creates the branch and worktree, and runs the playbook [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Nothing is scheduled.
- **Gate hook:** [`.claude/hooks/role_gate.py`](.claude/hooks/role_gate.py) blocks `gh pr create` and `gh pr ready` until Code Reviewer and Reality Checker ran after the last code edit. `ROLE_GATE=off` in the environment Claude Code is started from switches it off for that session; only the owner does that.
- **Permissions:** [`.claude/settings.json`](.claude/settings.json). Agent configuration edits ask in the main checkout and in ticket worktrees; CI, `CLAUDE.md`, `AGENTS.md` and Loop-file edits ask only in the main checkout; in a ticket worktree they are limited by the playbook's scope rule and reviewed by the owner at merge (shell-made edits are not covered, so a ticket never changes agent configuration); force pushes, pushes to `main`, `gh pr merge`, releases and reads of `.env` are denied.
- **CI:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Every job must be green on the current diff before a pull request is marked ready. The agent does not poll: it ends its turn with "Draft pull request #N is waiting for CI" and reads `gh pr checks` once when woken. Reviewers read the diff and evidence from `.claude/state/review/`. An acceptance step that needs a person is listed under "Owner checks" in the pull request.
- **Pull request:** [`.github/pull_request_template.md`](.github/pull_request_template.md). Tickets use [`.github/ISSUE_TEMPLATE/implementation-ticket.md`](.github/ISSUE_TEMPLATE/implementation-ticket.md).
- **Labels:** `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`, `tracking` (parent container, never worked; its sub-issues are the work items).
- **Changelog:** every ticket pull request adds one line under Unreleased in [CHANGELOG.md](CHANGELOG.md).
- **UI and copy:** [docs/ui-quality.md](docs/ui-quality.md); the `ui-ux-pro-max` and `unslop` skills are in `.claude/skills/`.
- **Decisions:** [docs/owner-decisions.md](docs/owner-decisions.md). Security reports: [SECURITY.md](SECURITY.md).
- **Merge and release:** only the owner merges and releases ([docs/RELEASING.md](docs/RELEASING.md)). An agent stops at a ready pull request.

## Loop

Issue triage runs at L1: report-only, started by hand, no scheduler, no GitHub writes. See [LOOP.md](LOOP.md).
