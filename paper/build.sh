#!/bin/sh
# Build from any working directory. Requires TeX Live/MiKTeX and latexmk.
set -eu
cd "$(dirname "$0")"
latexmk -pdf -pdflatex='pdflatex -output-format=pdf %O %S' \
  -interaction=nonstopmode -halt-on-error -outdir=build main.tex
