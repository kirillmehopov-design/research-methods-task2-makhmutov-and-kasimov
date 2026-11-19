# Task 4 IEEE paper

This paper examines automatic versus manually invoked Copilot suggestions across
experience groups using the published 33-participant dataset. Task 3 analysis,
the executed notebook, and scientific figures are integrated in this branch.

## Contributions

The first contribution completes Introduction, implemented Methodology, the
pipeline diagram, analysis settings, and a 12-source cited bibliography based on
Task 1. It adds build checks, defense notes, and a handoff for the second contributor.

The second contribution completes Results and Discussion, Limitations and
Conclusion, a 172-word results Abstract, the baseline table, two compact vector
plots, and the verified four-page PDF. The final package is ready for submission.

- Final PDF: [task4_paper.pdf](task4_paper.pdf)
- Standalone source/PDF archive: [task4_submission.zip](../outputs/task4_submission.zip)
- Verification and Zotero status: [task4_checklist.md](../docs/task4_checklist.md)
- Standalone compilation: [SUBMISSION_README.md](SUBMISSION_README.md)

## Build and validation

`main.tex` uses IEEEtran conference mode and four section files. Only
`references.bib` is compiled; `library/` preserves the original Task 1 file.

From the repository root with Tectonic available:

```powershell
./paper/build.ps1
./paper/build.ps1 -Compiler 'C:/path/to/tectonic.exe'
```

Output: `paper/build/main.pdf` and compilation logs. Tectonic downloads standard
packages on first use and runs bibliography passes. A compiler downloaded locally
is at `outputs/tectonic/tectonic.exe` (ignored by Git).

For Overleaf, upload the contents of `paper/`, choose `main.tex`, and select
pdfLaTeX. For a local TeX installation, run inside `paper/`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

From the repository root:

```sh
python -m src.check_paper
python -m unittest discover -s tests -v
python -m src.check_submission
```

Final verification (19 November 2026): all 20 tests and both submission checkers
passed. The final PDF has exactly four pages; all four pages were rendered and
visually inspected. No undefined references or overfull boxes remain. The last
page is balanced using the standard balance package. Remaining underfull-box
messages concern bibliography line justification; reviewed entries are readable.
All fonts are embedded. The 12 publisher DOI links and repository link are present
as PDF URI annotations, and internal cross-references resolve.

Linux/macOS build: `sh paper/build.sh`. Official unmodified IEEEtran.cls and
IEEEtran.bst are included for standalone compilation. Run `python paper/make_figures.py`
from the full repository to regenerate paper-specific vector figures from the
saved JSON (requires Matplotlib). The standard IEEE sizes and margins are unchanged.

```sh
python -m src.check_paper --final --pdf paper/build/main.pdf
```

## Bibliography and Zotero

Ten sources retain their Task 1 keys; the dataset paper and Ziegler et al. come
from the earlier draft. All twelve are cited. See [source verification](bibliography_audit.md).

For Zotero/Overleaf synchronization, import `references.bib` into a dedicated
collection, preserve the keys (pin with Better BibTeX if used), then export that
collection back to the same `.bib`. Rebuild after export and record completion
in the checklist. Repository setup alone does not establish a live Zotero connection.

Actual status: no Zotero connector or executable is available here. Import/export
and account synchronization were not performed. The exact remaining optional
steps are in SUBMISSION_README.md; the paper builds independently of Zotero.
Keep author/title/year, venue, DOI, and available volume/issue/pages. Remove
local file paths, abstracts, and duplicate DOI URLs.

## Evidence and wording

Use `data/processed/results.json` for numbers and `reports/task3_report.md` for
interpretation. Copy selected vector plots from `reports/figures/` into
`paper/figures/` for a self-contained Overleaf project. The parser runtime plot
is supplementary. Manual invocation is the Copilot baseline; changes are
automatic minus manual. Keep validity considerations concise in the final section.
