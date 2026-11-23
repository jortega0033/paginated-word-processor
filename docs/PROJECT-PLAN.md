# Paginated Word Processor

## Product requirements

A writer preparing a short report needs to see where pages end while editing, resume a local draft, and hand over an editable document that opens in LibreOffice Writer. This local workbench combines an ordered block editor, an A4 preview derived from the same draft, and specific feedback when an imported document is outside the supported format.

The first release supports one draft, fixed A4 portrait margins, headings, paragraphs with plain and bold runs, small two-column tables, and intentional page breaks. The writer can insert, edit, delete and reorder blocks by keyboard, preview pages, save, restart, print a PDF, export an editable DOCX, and import a supported DOCX into an unsaved draft. The writer explicitly decides whether to save an imported draft. Cancelled or rejected imports leave the previous draft and revision intact.

### First usable workflow

Open the sample report at localhost. Edit the title, add a paragraph and table, and insert a break before an appendix. Preview, save and restart. Print a two-page A4 PDF in Chrome. Open the DOCX output in LibreOffice Writer and inspect the text, bold run, table rows and explicit break. Reimport that DOCX and compare its editable content to the saved draft.

The first epic uses a block editor beside a read-only preview. Later milestones cover lists and images, editable page settings, headers and footers, a broader independent DOCX corpus, and tracked changes and comments. General Word compatibility, arbitrary pagination fidelity, collaboration, floating objects and tables spanning pages are outside this release. The long-term bar is to quantify line and page-break agreement with LibreOffice on a legally reusable corpus. The first release makes no large-document performance claims.

## Technical design

Use Python 3 standard-library HTTP, JSON, ZIP and XML modules for the loopback server. Serve local HTML, CSS and JavaScript to Chrome with zero runtime downloads. Use installed LibreOffice Writer for a separate interoperability check. Preflight Python, Chrome, Writer and locally installed Liberation Serif, and record their versions with layout results. Show a setup error if the required font cannot be loaded. Check the applicable license before bundling any font.

Use a versioned model with document title, ordered blocks, fixed page-profile ID and a saved revision. A block is a heading, paragraph, a table with exactly two equal-width columns and up to twelve rows, or a manual break. Text consists of ordered plain or bold runs. Each table cell contains one paragraph. Preserve stable editor block IDs. Canonical equality covers title, text, run formatting, table grid, block order and manual breaks. Adjacent compatible runs can merge. IDs, preview geometry and ZIP metadata do not participate. Set hard caps of 200 blocks and 80,000 Unicode scalar values. The reference layout supports left-to-right Latin letters and common punctuation. Identify unsupported characters without destroying a working draft. Escape document text in the app and DOCX construction.

### Local API and storage

| Endpoint | Behavior |
| --- | --- |
| GET /api/document | Return the saved model and revision or a blank revision zero. |
| PUT /api/document | Validate a captured draft and base revision and publish the next revision. Return a typed conflict if the revision differs. |
| POST /api/import-docx | Decode a bounded upload to an unsaved candidate or a typed error. |
| POST /api/export-docx | Serialize a validated draft and return the editable file without writing a saved revision. |

Bind only to 127.0.0.1. Require the exact app origin for browser writes and validate content types. Keep one local writer, lock its data directory and serialize writes. Validate, write a same-directory temporary file, flush and sync it, rename it, and sync the directory. Refuse to overwrite a malformed prior revision. For a post-publication sync error, ask the user to reload the persisted revision before retrying. Exercise restart and interrupted temporary writes using disposable fixtures. Physical power-loss durability remains unmeasured.

### Layout and print

Use A4 11,906 × 16,838 twips with 1,440-twip margins on each edge. This gives 9,026 × 13,958 twips of content. Body text is 12 pt with 360-twip lines and 120 twips after a paragraph. Headings are 18 pt with 480-twip lines and 120 twips after. Measure locally loaded faces with their specified weights and turn off discretionary kerning and ligatures in the reference profile. One flow planner computes line fragments, vertical position and page assignment. Break lines at spaces, split oversized tokens at supported character boundaries and retain the exact original text in the model.

Charge after-spacing with the last line of a paragraph. Keep a heading with the following body line when the pair fits on a fresh page. Size table rows by their tallest cell and move the full table to the next page when necessary. Flag a table too tall for an empty page. Reject leading, trailing and consecutive explicit breaks without removing user edits. Use the same page manifest in preview and print. Apply A4 physical dimensions without app chrome and one print break between pages. Disable browser-generated page headers and footers during verification. Compare screenshots or PDF markers on the documented local font and browser profile.

### DOCX subset

Build a bounded OPC package with a manifest, relationships, main document, title metadata and one fixed section profile, using the Transitional WordprocessingML markup consumed by Writer. Preserve explicit geometry, run bold, significant spaces, table cells and manual breaks. Write explicit breaks before eligible headings and paragraphs, with a dedicated break-only paragraph when a break precedes a table. The importer normalizes the documented representations to manual-break blocks. Preview-only automatic page breaks are recomputed. Use independent package sketches and compare model equality plus the visible Writer result. [ECMA-376](https://ecma-international.org/publications-and-standards/standards/ecma-376/) · [WordprocessingML document structure](https://learn.microsoft.com/en-us/office/open-xml/word/structure-of-a-wordprocessingml-document)

Cap uploads at 4 MiB, inflated parts at 8 MiB total, with up to 32 entries and 2 MiB per XML part. Read permitted parts into bounded buffers without disk extraction. Reject duplicate or noncanonical part names, unsuitable ZIP methods, encrypted entries, external targets, macros, embedded resources, non-UTF-8 XML, DTD or entity declarations and unsupported content-bearing XML. Cap XML depth and node count. Document the harmless package metadata the importer can ignore, and report it on success. Lists, images, comments or tracked changes cause specific rejection instead of losing content. Open fixture outputs in Writer with a disposable user profile, and measure forced pages using PDF export and whichever PDF tools pass preflight. [LibreOffice command-line parameters](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html)

### Original fixtures and expected results

- **Tally Rows.** Thirty short one-line paragraphs, Row 01 through Row 30. Each occupies 480 twips. The first page holds rows 01–29 with 38 twips remaining. Row 30 goes on page two. Moving row 30 before row 29 puts row 30 at the end of page one and row 29 first on page two.
- **Lantern Inventory.** A heading, paragraph with bold “Six,” a table with rows “Supply / Count,” “Wicks / 6” and “Cases / 2,” one manual break, heading “Appendix,” and paragraph “Recheck on Monday.” Exactly six ordered blocks. The inventory and all cells appear on page one, and Appendix and its text appear on page two in preview, Chrome print and Writer.
- **Wrapped Lines.** A sample paragraph and a table close to a natural page boundary. Compare ordered line positions to an independently authored fixed-width fixture. Test an oversized token and an atomic table larger than one page.
- **Unsupported Features.** Import separate independently authored packages containing one numbered paragraph and one inline image. Check different errors and unchanged draft and revision for each.
- **Save Conflict.** Open revision 4 in tabs A and B. A saves its title as revision 5. B receives a revision conflict and retains its edits. After restart the title from A remains.

## Epic · Author and hand over a paginated report offline

Deliver an ordered editor, repeatable A4 pagination, a resumable draft, a defined DOCX import/export profile and proof in independently rendered original sample reports. Estimated total effort is 20–31 engineering hours including verification. Start WP-01 and run WP-02, WP-03 and WP-04 in parallel against the stable model and geometry contract. WP-05 follows the package format established by WP-04. WP-06 integrates the branches and proves the scope end to end.

### WP-01 · Build a validated document model and keyboard editor

Estimate 3–4 hours. Dependencies none.

- Build a localhost shell that opens Lantern Inventory and lets a keyboard user add, move, edit and remove headings, paragraphs, rows and manual breaks with predictable focus.
- Verify normalization is idempotent, adjacent compatible runs merge without text loss, and the sample retains all six ordered blocks. Invalid text or size reports the relevant block and preserves the editable draft.
- Publish stable API, model, geometry and fixture contracts for the parallel tickets.

### WP-02 · Calculate line and page layout and print the same pages

Estimate 4–6 hours. Depends on WP-01.

- Share a single line and page manifest between Chrome preview and print. Tally Rows produces the precise 29/1 split and reorder result.
- Verify the Wrapped Lines fixture, including a heading pair near the edge, a moving table and rejection of a table that exceeds a fresh page.
- Print Lantern Inventory and verify A4 geometry, page count and marker positions in Chrome. Record the font and browser version and confirm there are no external page requests.

### WP-03 · Save and recover the latest local draft revision

Estimate 2–4 hours. Depends on WP-01.

- Add explicit save, atomic file publication and a single writer. Save, restart both server and browser, and confirm the same normalized content and revision.
- Run Save Conflict. Keep unsaved changes in the rejected tab and the winning title on disk.
- Simulate an unpublished partial temporary file and a malformed saved revision separately. Ignore the former, report the latter and refuse to overwrite it.

### WP-04 · Write the supported editable DOCX profile

Estimate 4–6 hours. Depends on WP-01.

- Document the package, schema subset and typed errors before WP-05. Inspect relationships, sizes and main XML in independent tests.
- Open Lantern Inventory in Writer without a repair prompt. Verify text, bold, table and explicit appendix break. Independently verify a break before a table.
- Test significant spaces, ampersands, angle brackets and accents in a separate fixture. Verify exact values after opening the output. Reject invalid export data before sending any file bytes.

### WP-05 · Import supported DOCX with explicit format limits

Estimate 4–6 hours. Depends on WP-01 and WP-04.

- Import an independent package into a candidate without replacing an existing draft. Export and reimport it and verify text, formatting, cells, positions of explicit breaks and block order.
- Reject unsupported content with typed errors, and enforce declared and observed package limits. Check no failed case changes editor content or persisted revision.
- Confirm cancel restores the original editing state. An accepted candidate still uses the same revision rules when explicitly saved.

### WP-06 · Verify the complete offline workflow in Chrome and LibreOffice

Estimate 3–5 hours. Depends on WP-02, WP-03 and WP-05.

- In a clean offline checkout, edit, save, restart and reopen Lantern Inventory. Print from Chrome and open its DOCX in Writer. Record page counts and section markers in both renderers.
- Reimport the exact output, compare with the saved model, edit one cell and save. Confirm the changed cell and unchanged section order after restart.
- Complete the workflow using keyboard navigation, including clear recovery from an unsupported file. Record commands, observed evidence, tested boundaries and the broader compatibility goals still pending.
