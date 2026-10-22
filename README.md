# Copilot Interaction Mode and Productivity Across Programmer Experience Levels

**Research Methods — Task 2**
**Authors:** Makhmutov Damir and Kasimov Amir
**Repository:** https://github.com/kirillmehopov-design/research-methods-task2-makhmutov-and-kasimov

## Overview

We study how automatic and manually requested GitHub Copilot suggestions relate to productivity among novice and experienced programmers. We use published measurements from Guglielmi et al. The source experiment has 33 participants: 17 novices and 16 experts. Each participant completed two different Java maintenance tasks under two Copilot modes, giving 66 observations.

This quantitative secondary analysis uses the published dataset to compare participant-level results and check their robustness. The current Task 2 pipeline validates the data and calculates initial summaries and bootstrap confidence intervals. The full notebook, scientific plots and adjusted analysis are planned for Task 3.

## Research questions

1. How does productivity change between manual and automatic suggestions among novices?
2. How does productivity change between these modes among experts?
3. Does the average change differ between the two experience groups?

The third question is our main question.

## Method and metrics

The [Methodology Passport](docs/Methodology_Passport.md) contains the hypotheses, variables, metrics and research plan.

The baseline is **manual invocation of Copilot suggestions**. The comparison is **automatic suggestions enabled**. Copilot is available in both modes.

Productivity is calculated as:

`productivity = (completion_percent / 100) / (time_minutes / 60)`

The unit is completed task fraction per hour. For each participant, we subtract manual-mode productivity from automatic-mode productivity. Our primary metric is the expert group's mean change minus the novice group's mean change.

| Planned comparison | Metric | Reference |
| --- | --- | --- |
| Automatic vs manual among novices | Mean paired productivity change, with 95% CI | Manual mode for the same participants |
| Automatic vs manual among experts | Mean paired productivity change, with 95% CI | Manual mode for the same participants |
| Experience-group difference | Expert mean change minus novice mean change, with 95% CI | Novice group's mean change |
| Completion guardrail | Mean paired completion change, percentage points | A drop greater than 5 points is flagged in either group |
| Time and completion | Mean, median and 95th percentile | Reported separately for each group and mode |

We set the completion guardrail at a maximum average drop of five percentage points in either group. Completion and time are reported separately to help interpret productivity.

Bootstrap resampling preserves each participant's pair and samples separately within experience groups. The seed is 42 and the default is 10,000 repetitions. Current estimates are unadjusted. Task 3 will check task assignment, condition order and sensitivity to individual participants.

## Data

The two small source CSV files are included in `data/raw/`. They contain participant IDs, assignment groups, task/mode labels, completion, time and published productivity. Their original bytes are preserved. The script checks SHA-256 hashes and independently recalculates productivity.

- [Source paper](https://doi.org/10.1007/s10664-026-10965-6)
- [Replication package](https://figshare.com/s/2f26b8ee294a3a87c908)
- [Data description and attribution](data/README.md)

`data/sample/` contains eight real source rows representing four complete participant pairs. It is only for tests and demonstration; research summaries use all 66 observations.

## System requirements

- Docker Engine or Docker Desktop with Linux containers; or Python 3.12 (locally checked with 3.12.14). Docker pins Python 3.12.12.
- The analysis uses only the Python standard library. There are no pip dependencies.
- Internet access is needed to obtain the repository and Docker base image. The analysis itself runs offline.

## Quickstart

From the repository root, using Python:

```sh
python -m unittest discover -s tests -v
python src/benchmark.py --config configs/config.json
```

Or using Docker:

```sh
docker build -t copilot-mode-study .
docker run --rm copilot-mode-study
```

Docker runs the tests during the build. Its generated files stay inside the container unless a volume is mounted. To save them on the host, replace the run command with:

```sh
docker run --rm --mount type=bind,source="<absolute-output-directory>",target=/app/outputs copilot-mode-study
```

Create that output directory first. With the Python route, files are saved directly in `outputs/`:

- `observations.csv`: validated measurements with consistent field names and units;
- `paired_changes.csv`: one row per participant;
- `results.json`: summaries, confidence intervals and guardrail flags;
- `benchmark.log`: run summary.

Parameters and source paths are in `configs/config.json`. For an eight-row demonstration, pass `--config configs/sample.json` instead. The output folder is excluded from Git.

## Project structure

```text
.
├── .github/workflows/ci.yml
├── configs/
│   ├── config.json
│   └── sample.json
├── data/
│   ├── README.md
│   ├── raw/                 # Two original CSV files and provenance
│   └── sample/              # Eight real rows for tests
├── docs/
│   ├── Methodology_Passport.md
│   ├── Analysis_Protocol.md
│   └── Defense_Notes.md
├── notebooks/              # Reserved for Task 3
├── outputs/                # Generated files, ignored by Git
├── src/
│   ├── benchmark.py
│   └── process_data.py
├── tests/
├── Dockerfile
├── requirements.txt
└── LICENSE
```

## Citation and license

Cite the source paper and its replication package when using the measurements. Source authors: Emanuela Guglielmi, Venera Arnaoudova, Gabriele Bavota, Rocco Oliveto and Simone Scalabrino. DOI: `10.1007/s10664-026-10965-6`.

For our analysis: Makhmutov, D., & Kasimov, A. (2026). *Copilot Interaction Mode and Productivity Across Programmer Experience Levels*. Research Methods project.

Our code is under the MIT License. The included source data are attributed separately under CC BY 4.0, as stated on the Figshare page. MIT does not replace the data license.
