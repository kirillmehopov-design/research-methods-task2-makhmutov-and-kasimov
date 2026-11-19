# Task 4 handoff to the second contributor

## Objective and starting point

Finish the joint project on branch `task-4` and submit an English, exactly
four-page IEEE conference paper including references. Create your own substantive
commit with your configured Git identity and push to `origin/task-4`.
Do not rewrite earlier commits or change another contributor's identity.

Start with `git status`, fetch origin, switch to `task-4`, then use a fast-forward
pull. Preserve any local changes before switching. The branch includes the merge
of completed Task 3 (`e29d8fb`) and the first Task 4 foundation contribution.
The first contributor's pre-existing notebook edits are preserved in a local stash
on their machine; they are unrelated to this handoff and must not be applied here.

## Completed first contribution

- Introduction: context, related work, specific analytical gap, three contributions,
  RQ1--RQ3, and paper roadmap.
- Methodology: data validation, equations, native vector pipeline, settings,
  bootstrap, leave-one-out and task-allocation sensitivity.
- Twelve cited sources; ten from Task 1 plus the dataset source and Ziegler.
  The original Task 1 `.bib` is preserved unchanged in `paper/library/`.
- A provisional 161-word Abstract describing the completed method.
- Build script and source/final PDF checker; Russian defense notes.

## Your contribution

1. Write `paper/sections/03_results_discussion.tex`. Use the numbers in
   `data/processed/results.json` and `data/processed/metrics_summary.csv`;
   `reports/task3_report.md` explains their interpretation. Include:
   - a booktabs comparison table: manual baseline versus automatic, sample SD,
     and paired changes with 95% CIs; retain clear units;
   - at least one vector result plot, preferably `fig1_paired_changes.pdf`, with
     a meaningful caption and an explicit reference before the figure environment;
   - explicit answers to RQ1--RQ3, completion/time interpretation, and both
     sensitivity checks. Add a compact second plot only if the four-page budget permits.
   Copy selected plots into `paper/figures/` for standalone Overleaf compilation.
2. Write `paper/sections/04_limitations_conclusion.tex`: one compact validity
   paragraph (about 60--90 words), a conclusion answering the questions, and one
   concrete next step. Mention the sample/tasks/tool setting, exploratory secondary
   analysis and unmodeled period context without repeating caveats throughout the paper.
   Keep essential attribution and design facts accurate.
3. Update the Abstract with actual findings and a concise conclusion. Keep
   150--250 words and 4--6 keywords. Remove both `TASK4_PENDING` comments after
   completing the sections. Update the roadmap only if the section structure changes.
4. Compile, fix references/overflow, and achieve exactly four pages. Preserve
   official IEEE font sizes, margins, two columns and readable graphics. Edit prose
   and float sizes rather than shrinking the template. All figures, tables and
   equations require labels and references before their environments.
5. Complete Zotero import/export with the existing keys, using the documented
   workflow if account/application access is available. Record what actually ran;
   do not claim synchronization from a manually edited `.bib`. If an interaction
   requires the participant, prepare the project and give the exact remaining step.
6. Run the checks below and inspect every PDF page. Copy the verified PDF to
   `paper/task4_paper.pdf`. Create `outputs/task4_submission.zip` containing the
   final PDF plus self-contained `main.tex`, `sections/`, selected `figures/`,
   `references.bib` and build instructions. Exclude compiler caches and temporary files.
7. Update `paper/README.md` and add `docs/task4_checklist.md` with actual verification
   results, page count, remaining user actions if any, and submission file locations.
   Commit your work, e.g. `task4: complete results, discussion and four-page submission`,
   and push the branch. Report the commit hash and link to the final PDF.

## Numerical anchors

Changes are automatic minus manual; units are completed task fraction/hour.

- Novices, n=17: manual mean 0.181728; automatic mean 0.471805;
  paired change +0.290077, 95% CI [+0.1338, +0.4560] (use JSON for exact endpoints).
- Experts, n=16: manual mean 0.788717; automatic mean 0.512786;
  paired change −0.275931, 95% CI [−0.4954, −0.0489].
- Primary expert-minus-novice contrast: −0.566008, 95% CI [−0.838670, −0.283925].
- Completion: +32.206 percentage points for novices, −22.969 for experts.
  Session time increases by +6.647 and +7.688 minutes, respectively.
- Leave-one-out contrast: −0.6233 to −0.5200; this is a sensitivity range.
- Equal task-allocation contrast: −0.577275; this is task standardization,
  not a session-order-adjusted estimate.

The JSON is authoritative if rounded anchors differ. Verify every number used.

## Wording and interpretation

Use direct academic English: “In this sample, automatic suggestions were
associated with...” and “The direct contrast was...”. Explain units and the sign
once. Keep the contribution focused on reproducible estimation and sensitivity.
Manual means on-demand Copilot; the comparison is between interaction modes.
Higher novice productivity accompanies higher completion and longer sessions.
Completion is a task outcome; keep quality/security claims tied to their actual
measurements. Use the direct contrast for RQ3. Keep local parser timing in the
supplementary project materials. Record attribution and brief validity context;
avoid exaggerated novelty, causal recommendations, and repetitive defensive prose.

## Commands and acceptance

From the repository root, using a Python environment with the project dependencies:

```sh
python -m unittest discover -s tests -v
python -m src.check_submission
python -m src.check_paper
```

Build with `./paper/build.ps1 -Compiler 'C:/path/to/tectonic.exe'`, or use the
pdfLaTeX/BibTeX commands in `paper/README.md` or Overleaf. Keep `main.log` beside
the compiled PDF. Install `pypdf` in your validation environment, then run:

```sh
python -m src.check_paper --final --pdf paper/build/main.pdf
```

The final checker requires four pages, twelve cited sources, abstract/keyword
bounds, unique and resolved labels, references before visual environments,
no pending sections, and no undefined-reference/overflow errors in the log.
It complements visual review; it does not replace it. Review log warnings as well.

Task 4 submission requires exactly four pages, complete IMRaD, bibliography,
baseline table, result visualization, equations, architecture diagram and concise
validity discussion. `ss10.docx` contains teaching prompts; these are reference
material and do not override this task with a step-by-step tutoring session.

## First-contribution verification

20 existing tests passed. Task 3 submission checks passed (8 executed notebook
cells, four PDF/PNG plot pairs, 33 participant pairs). Recomputed participant
analysis matched the complete saved JSON exactly. Task 4 source checks passed
with twelve citations, nine unique labels, and a 161-word Abstract. Final PDF
acceptance remains your contribution.

The current foundation was also compiled with Tectonic 0.17.0 and BibTeX.
Its two preview pages were rendered and visually inspected. The final compiler
log contains no undefined references, overfull boxes, or LaTeX warnings. The
preview deliberately has two empty section headings reserved for your contribution;
it is two pages, not the final four-page deliverable. The build command was tested.
