# Task 4 final submission checklist

Verified on 19 November 2026 on branch task-4, based on 0c62ac2.
The checkout started clean; there were no local edits to stash. The first
contributor's separate machine-local stash was neither accessed nor applied.
The local preparation commit used Codex <codex@openai.com>. Publication uses
the connected kirillmehopov-design GitHub account; its author/committer metadata
is recorded in the published commit. Earlier remote commits are retained.

## Content and numerical verification

- [x] Results and Discussion answers RQ1, RQ2 and the direct RQ3 contrast.
- [x] Six-row booktabs table reports manual baseline / automatic means, sample
  SDs, paired changes and 95% participant-pair bootstrap CIs with explicit units.
- [x] Recomputed build_analysis output equals the complete saved results.json.
- [x] Primary contrast -0.5660084244; CI [-0.8386704834, -0.2839248256].
- [x] Leave-one-out range [-0.6232927427, -0.5200099145], explicitly a sensitivity
  range; equal task-allocation contrast -0.5772750363, not an order adjustment.
- [x] Completion and time interpreted separately; higher novice productivity
  accompanies longer sessions. Both modes provide Copilot.
- [x] Source researchers' data collection and our secondary-analysis contribution
  remain distinct. No causal effect or unmeasured security outcome is claimed.
- [x] One 72-word limitations paragraph covers sample, tasks, tool setting,
  exploratory analysis, nonrandom groups and unmodeled session-period context.
- [x] Conclusion answers RQ1-RQ3 and proposes additional tasks with explicit
  period labels and solution-quality assessment.
- [x] Abstract contains actual findings, 172 whitespace-separated words and
  five keywords. No pending section markers remain in the paper.

## Build and inspection

- [x] Standard IEEEtran conference class, two columns and original margins/fonts
  sizes; no template shrinking. Unmodified CTAN class/style included.
- [x] Exactly four US Letter pages, including 12 cited bibliography entries.
- [x] Twelve unique labels resolve; visuals/equations are introduced before use.
- [x] Pipeline diagram, three equations, settings table and results table included.
- [x] Two result figures use native vector PDF, readable 8-point plot text,
  distinct group markers and colorblind-safe colors; no raster images embedded.
- [x] All four pages rendered and visually reviewed at final layout, including
  table, captions, formulas, references and balanced last-page columns.
- [x] All PDF fonts embedded; no Type 3 fonts.
- [x] No undefined citations/references, overfull boxes or LaTeX errors.
  Remaining underfull hbox diagnostics are bibliography line justification;
  visually reviewed and accepted, not suppressed.
- [x] Twelve distinct DOI URI annotations and repository link verified in PDF.
  Internal reference destinations resolve. Publisher availability itself was
  audited in the preceding contribution, not re-certified by this link check.
- [x] Standalone source archive compiled separately and passed final PDF checks.

## Executed checks

- [x] python -m unittest discover -s tests -v: 20 tests passed.
- [x] python -m src.check_submission: 8 executed notebook cells, 4 PDF/PNG pairs,
  33 participant pairs passed.
- [x] python -m src.check_paper: 12 citations, 12 labels, 172-word Abstract passed.
- [x] python -m src.check_paper --final --pdf paper/build/main.pdf: four pages
  and clean reference/overflow checks passed.
- [x] Same final checker passed on paper/task4_paper.pdf with local sibling log.
- [x] Original Task 1 bibliography bytes match the starting commit.
- [x] ZIP integrity and required files checked; no compiler caches, environment,
  temporary files or raw datasets included.

## Zotero status and remaining actions

No Zotero connector or executable was available. No import/export, account sync
or Overleaf synchronization was performed. The BibTeX file retains all 12 keys
and metadata; compilation and PDF URI checks succeeded independently.

Optional integration step: import paper/references.bib into a dedicated Zotero
collection, retain/pin existing keys (Better BibTeX if used), export BibTeX,
compare keys/metadata, and rebuild with the documented commands. Do not describe
this prepared workflow as completed synchronization. No manual action remains
for PDF compilation; this Zotero step requires application/account access.

## Deliverables

- paper/task4_paper.pdf: final verified four-page paper.
- outputs/task4_submission.zip: final PDF and standalone LaTeX source package.
- paper/README.md: repository build and validation instructions.
- paper/SUBMISSION_README.md: standalone compilation and Zotero instructions.
- paper/build/main.log: local compiler log retained beside the build PDF.

Submission action: upload the final PDF/archive and repository link in LMS.
