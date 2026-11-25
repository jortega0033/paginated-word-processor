# Paginated Word Processor

An offline editor for structured documents with predictable pagination, print and bounded DOCX round-trips.

Only a runnable scaffold exists (help, version and smoke tests); the product is planned. The scope, architecture and acceptance criteria are in [the project plan](docs/PROJECT-PLAN.md). The plan includes a reproducible verification strategy for the future build.

- [Product requirements](docs/PROJECT-PLAN.md#product-requirements)
- [Technical design](docs/PROJECT-PLAN.md#technical-design)
- [Implementation backlog and epic](https://github.com/jortega0033/paginated-word-processor/issues)

The first plan of phase 1 said 20–31 engineering hours. Its open tickets, with tests and review, add up to 66 to 96 hours; the whole program is larger and is described below. All figures are estimates.

## Program goal

Build a word processor that can replace an office suite for real documents: full DOCX in and out, page layout measured against other word processors, editing by many people at once, and 1,000-page documents, with no document or layout library.

The program is planned ([#40](https://github.com/jortega0033/paginated-word-processor/issues/40)). Phase 1 is the current epic [#1](https://github.com/jortega0033/paginated-word-processor/issues/1) and the only phase with tickets.

**Score.** Share of pages in a licence-clean DOCX corpus whose line and page breaks agree with LibreOffice, and the share of documents that round-trip without loss.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 66 to 96 | [#1](https://github.com/jortega0033/paginated-word-processor/issues/1) |
| 2 | Full document model | 170 to 300 | [#41](https://github.com/jortega0033/paginated-word-processor/issues/41) |
| 3 | Layout engine | 180 to 320 | [#42](https://github.com/jortega0033/paginated-word-processor/issues/42) |
| 4 | Real editing | 150 to 260 | [#43](https://github.com/jortega0033/paginated-word-processor/issues/43) |
| 5 | Collaboration | 130 to 230 | [#44](https://github.com/jortega0033/paginated-word-processor/issues/44) |
| 6 | Formats and automation | 150 to 260 | [#45](https://github.com/jortega0033/paginated-word-processor/issues/45) |

About 850 to 1470 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.

## License

[MIT](LICENSE) © 2026 Jake Ortega.
