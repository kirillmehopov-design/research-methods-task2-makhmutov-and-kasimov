# Task 4 paper and laboratory 9

This directory contains an English IEEE conference draft for laboratory 9:
the Introduction and Methodology are written against the existing Task 2 code.
Results integration and the final four-page Task 4 submission remain pending.

## Open in Overleaf

Upload the contents of this directory as an Overleaf project, select `main.tex`
as the main document, and use pdfLaTeX with BibTeX. The document class is
`IEEEtran` in conference mode; use the IEEE template available in Overleaf.
The source uses `amsmath`, `amssymb`, `booktabs`, `graphicx`, and `hyperref`.
Sections are included through `\input` and the reference style is `IEEEtran`.

For a local TeX installation, run from this directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Use `text~\cite{key}` for numeric IEEE citations. Do not add `natbib` or mix
`\citep`/author-year conventions into this IEEE draft. Use `\label` and `\ref`
for references; place table labels after captions. The pipeline figure is native
LaTeX, so it needs no external image or shell-escape support.

## Bibliography and Zotero

`references.bib` is a manually curated, DOI-verified starter bibliography of
three peer-reviewed publications, not a claimed export from your Zotero library.
All three entries are cited. The source paper supports dataset attribution;
Barke et al. support the interaction context; Ziegler et al. support the
distinction between perceived productivity and usage measures.

To establish a Zotero workflow:

1. Import `references.bib` into a dedicated Zotero collection and inspect records.
2. If Better BibTeX is installed, retain/pin the existing citation keys.
3. Export that collection as BibTeX (or Better BibTeX), retaining these keys,
   then replace `references.bib` in Overleaf. A normal Zotero BibTeX export also works.
4. Keep author, title, year, journal/booktitle, DOI, and available volume/pages.
   Remove local `file`, `abstract`, and `bdsk-url` fields. Retain URLs when they
   are essential for datasets or web-only resources; DOI records need no duplicate URL.
5. Recompile and check that no citation is undefined. Zotero synchronization
   and an Overleaf account project have not been configured by this file setup.

Verification sources, checked on 5 November 2026:

- Source study: https://doi.org/10.1007/s10664-026-10965-6
- Barke et al., author-hosted paper: https://shraddhabarke.github.io/raw/copilot.pdf
- Ziegler et al., author manuscript: https://arxiv.org/abs/2205.06537
- Dataset provenance: `../data/raw/provenance.json` and `../data/README.md`.

The source study appeared online on 3 November 2026, but its publisher's
recommended citation assigns volume 32, article 42 to 2027. The BibTeX entry
uses that citation year and the author spelling on the publisher page; its
existing key `guglielmi2026copilot` is intentionally kept stable.

## Validation status

All citation keys and cross-reference targets were checked in the source.
All 12 existing analysis tests pass. No local TeX distribution was available;
attempts to obtain a portable compiler stalled during download. Consequently,
PDF compilation, rendered layout, and the absence of compilation warnings have
not been verified. Compile in Overleaf before treating the draft as ready to submit.

## Before the final Task 4 submission

- Complete Task 3 notebook, figures, summaries, and sensitivity checks.
- Replace the results integration note with verified results and discussion.
- Update the abstract and conclusion to reflect those results.
- Expand and cite the literature to the required 10--12 peer-reviewed sources;
  three starter sources do not meet the final Task 4 bibliography requirement.
- Check exactly four PDF pages including figures, tables, and references.
- Review every page visually and resolve all compilation/reference warnings.

The current analysis is a secondary analysis, not a new participant experiment.
Technical runtime benchmarks, if added for laboratory 6, must not be described
as new Copilot productivity evidence or mixed into the participant sample.
