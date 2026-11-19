# Task 4 IEEE paper

This paper examines automatic versus manually invoked Copilot suggestions across
experience groups using the published 33-participant dataset. Task 3 analysis,
the executed notebook, and scientific figures are integrated in this branch.

## Contributions

The first contribution completes Introduction, implemented Methodology, the
pipeline diagram, analysis settings, and a 12-source cited bibliography based on
Task 1. It adds build checks, defense notes, and a handoff for the second contributor.

The second contribution completes Results and Discussion, Limitations and
Conclusion, results sentences in the Abstract, and final four-page layout.
See [the handoff](../docs/task4_handoff.md). The unfinished section files carry
`TASK4_PENDING` comments. This intermediate draft is not the submission PDF.

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

After the second contribution, install `pypdf` in the validation environment:

```sh
python -m src.check_paper --final --pdf paper/build/main.pdf
```

Or use `./paper/build.ps1 -Final`. This requires four pages, no pending sections,
and a compiler log beside the PDF without unresolved references or overfull boxes.
Inspect every page visually, then copy the final PDF to `paper/task4_paper.pdf`.

First-contribution verification: Tectonic 0.17.0 successfully compiled the
two-page foundation preview; both pages were rendered and inspected. The log
has no unresolved references or overfull boxes. The final two sections remain
for the second contribution, so this preview does not meet final submission scope.

## Bibliography and Zotero

Ten sources retain their Task 1 keys; the dataset paper and Ziegler et al. come
from the earlier draft. All twelve are cited. See [source verification](bibliography_audit.md).

For Zotero/Overleaf synchronization, import `references.bib` into a dedicated
collection, preserve the keys (pin with Better BibTeX if used), then export that
collection back to the same `.bib`. Rebuild after export and record completion
in the handoff. Repository setup alone does not establish a live Zotero connection.
Keep author/title/year, venue, DOI, and available volume/issue/pages. Remove
local file paths, abstracts, and duplicate DOI URLs.

## Evidence and wording

Use `data/processed/results.json` for numbers and `reports/task3_report.md` for
interpretation. Copy selected vector plots from `reports/figures/` into
`paper/figures/` for a self-contained Overleaf project. The parser runtime plot
is supplementary. Manual invocation is the Copilot baseline; changes are
automatic minus manual. Keep validity considerations concise in the final section.
