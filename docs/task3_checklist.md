# Task 3 Submission Checklist

The project follows the Software Engineering track. The research is a secondary analysis of published participant measurements. A separate real code benchmark supplies the technical timing artifacts without changing the scientific dataset.

## Required artifacts

- [x] Public repository with the Task 2 foundation and Task 3 additions.
- [x] Original source CSVs and provenance retained in `data/raw/`.
- [x] Small real technical log at `data/raw/test_run.jsonl`, with explicit warm-up and evaluation phases.
- [x] Processed statistical summary at `data/processed/metrics_summary.csv`.
- [x] Additional technical summary at `data/processed/runtime_summary.csv`.
- [x] SE C4 Component model with collection and calculation points at `docs/domain_model.md`.
- [x] Executed notebook at `notebooks/01_data_analysis.ipynb`, with sequential execution counts, visible outputs, and no cell errors.
- [x] Modular processing and plotting in `src/process_data.py` and `src/visualize.py`.
- [x] Means, sample SD, medians, quartiles, p95, and paired bootstrap 95% confidence intervals.
- [x] Fixed bootstrap seeds and participant-pair resampling.
- [x] Four figure pairs in `reports/figures/`: vector PDF and PNG at 300 DPI.
- [x] Axes name measured quantities and units; categorical axes name their categories.
- [x] Uncertainty bars, observed distributions, colorblind-safe colors, and distinct markers.
- [x] README Results & Discussion, manual-baseline comparison table, figures, and domain-model link.
- [x] Markdown submission report at `reports/task3_report.md`.
- [x] `.gitignore` excludes environments, kernel files, checkpoints, caches, and temporary outputs.
- [x] Pinned dependencies, clean-kernel runner, tests, and automated artifact validation.

## Scope adaptations

**Human outcomes:** There are no technical cold-start measurements or API failure logs in the published participant tables. No human session is removed as warm-up. Completion change is the project-defined research guardrail; it is not relabelled as API error rate or code security.

**Technical timing:** Each of two workloads has 20 warm-up and 100 evaluation attempts. Only warm-up timing records are excluded from technical summaries. Errors remain in the denominator. The operation is parsing and pair validation on preloaded CSV text; I/O is outside timing. IQR flags do not delete observations. Successful-attempt latency and all-attempt error rates are reported separately.

**Benchmark comparison:** The scientific baseline is manual Copilot invocation, compared with automatic suggestions. These are existing interaction modes, not a newly invented algorithm. The extra timing benchmark compares input sizes, not a proposed faster method.

**Task and order:** Equal-task weighting and leave-one-out are implemented. Full session-order or carryover adjustment is not claimed without verified first/second-period labels. The limitation is explicit in the notebook and report.

These adaptations are scientifically appropriate for this dataset. The instructor decides whether a secondary-analysis project meets the intended experimental scope; this checklist does not claim an approved exception or guarantee a grade.

## Final checks

```sh
python -m unittest discover -s tests -v
python -m src.run_task3
python -m src.check_submission
```

The unit suite checks source integrity, statistical calculations, pair preservation, repeatability, warm-up exclusion, and failure accounting. The artifact checker validates executed notebook outputs, data counts, JSONL phases, and PDF/PNG exports. Figure readability is reviewed visually. GitHub Actions also rebuilds the complete submission in the pinned Linux Docker image.

## Submission

Submit the public repository URL and `reports/task3_report.md` to LMS. Use the report's GitHub page to display its relative image links. The submission is identified by the `task3-final` Git tag. No Task 4 work is included on this branch.
