# Task 4 submission

`task4_paper.pdf` is the verified four-page IEEE conference paper by Damir
Makhmutov and Amir Kasimov. It contains 12 cited sources, a baseline comparison,
three equations, the analysis pipeline, and two vector result plots.

## Rebuild the standalone sources

Upload main.tex, sections/, figures/, references.bib, IEEEtran.cls and
IEEEtran.bst to Overleaf. Select main.tex and pdfLaTeX. The included IEEEtran
class and bibliography style are unmodified CTAN files with their original
license notices.

With TeX Live/MiKTeX and latexmk, run `sh build.sh`. Output is build/main.pdf;
compiler logs stay in build/. The standard packages used by main.tex include
amsmath, amssymb, booktabs, graphicx, balance, fontenc and hyperref.
Alternatively run pdfLaTeX, BibTeX, then pdfLaTeX twice from this directory.
No Python, source dataset or Copilot account is needed to compile the paper.

The full analysis and checks are in the project repository:
https://github.com/kirillmehopov-design/research-methods-task2-makhmutov-and-kasimov/tree/task-4

## Bibliography status

All 12 entries are cited; Publisher record links open their DOI resolvers.
Original Task 1 bibliography bytes are preserved in the full repository.
Zotero application/account access was unavailable in the completion environment.
No Zotero import, export, account sync or Overleaf sync is claimed.
To complete that optional integration, import references.bib into a dedicated
Zotero collection, retain/pin its 12 existing citation keys, and export BibTeX.
Compare all keys and metadata, then rebuild and recheck the four-page PDF.
A library export should not silently replace the DOI hyperlink notes.
