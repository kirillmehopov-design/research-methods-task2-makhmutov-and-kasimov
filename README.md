# Programmer Experience and AI Coding Assistant Effectiveness

**Research Methods - Task 2: Methodology Passport and Reproducible Benchmark**

**Authors:** Makhmutov Damir; Kasimov Amir

**Public GitHub repository:** https://github.com/kirillmehopov-design/research-methods-task2-makhmutov-and-kasimov

## Overview

This repository contains a reproducible **measurement and analysis harness** for the proposed study from Task 1, *The Influence of Programmer Experience Level on the Effectiveness of AI Tools in Programming*. It uses a **mixed-methods** design: a questionnaire and observed AI-use patterns, paired AI/no-AI task measurements, and standardized reviews of AI-generated code containing known defects. Programmers are grouped as **novice** or **experienced**. The same GitHub Copilot configuration, programming language, environment, test suite and evaluation protocol must be used during real data collection.

**Important:** The files in `data/sample/` are synthetic smoke-test fixtures, NOT participant observations or scientific evidence. This code processes recorded observations; it does not launch or control GitHub Copilot. The Week 6 deliverable is the *working measurement pipeline*, not proof of the hypotheses. Record real measurements only after informed consent and the approved Week 7 protocol.

## Research questions

- **RQ1 (descriptive):** How do novice and experienced programmers differ in frequency, purposes, prompting and verification patterns when using AI tools?
- **RQ2 (explanatory):** Does experience level moderate the effect of AI assistance, compared with a no-AI baseline, on task completion time and code correctness?
- **RQ3 (comparative):** How do novice and experienced programmers differ in detection and repair of seeded defects in AI-generated code?

## Study variables and baseline

- **Independent:** experience group (`novice` / `experienced`), condition (`ai` / `no_ai`) for RQ2.
- **Primary dependent metric:** difference between experience groups in the **mean within-participant percentage reduction in completion time** due to AI. Positive = experienced developers benefit more; negative = novices benefit more.
- **Secondary:** unit-test pass rate, static-analysis defects, critical defects, AI prompt count, accepted suggestions, verification actions, code-review detection/fix rates, review time.
- **Guardrails:** mean unit-test pass rate for AI tasks must not decrease by >5 percentage points vs matched no-AI tasks **within either experience group**; no critical defects in AI task outputs. These are *proposed*, pre-registered thresholds, not observed scientific results.
- **Baseline:** the same participant completes a matched task **without AI**; tasks A/B and condition order are counterbalanced. All programmers use the same IDE, language, test suites, limits, and machine class. Experience cannot be randomized, so cross-group conclusions are associations/moderation rather than causal effects of experience itself.

## System requirements

- Docker Engine / Docker Desktop (Linux/macOS/Windows); no local Python installation required for the Docker route.
- Alternatively, Python **3.12.12** with standard library only (no external pip packages). Tests were also run on Python 3.13 locally.
- No network connection needed after pulling the pinned Docker base image.

## Quickstart: 2 commands

From the repository root:

```bash
docker build -t ai-experience-benchmark .
docker run --rm ai-experience-benchmark
```

The container runs the bundled unit tests at build time and prints a `SMOKE_TEST_SYNTHETIC_NOT_RESEARCH` summary during `docker run`. It also writes `outputs/benchmark_results.json` and `outputs/benchmark.log` **inside the container**; the summary is printed to stdout. To save generated results on your computer, use a volume mount appropriate for your shell, or run locally as below.

**Local Python (also 2 commands):**

```bash
python -m unittest discover -s tests -v
python src/benchmark.py --config configs/config.json
```

Outputs are saved in `outputs/` when run locally. This directory is excluded from Git commits.

## Planned benchmark matrix

| Comparison | Participants / input | Primary or secondary metric | Baseline / control |
|---|---|---|---|
| AI vs no-AI within novice group | Matched tasks A/B, counterbalanced | Relative completion-time change (%) | Same novice, no-AI condition |
| AI vs no-AI within experienced group | Matched tasks A/B, counterbalanced | Relative completion-time change (%) | Same experienced participant, no-AI condition |
| Experience interaction (primary) | Mean paired benefit by group | Difference in time benefit, percentage points | Between-group contrast of paired changes |
| Correctness guardrail | Same test suite per matched task | Pass-rate difference (fraction) | No-AI scores; must not drop >0.05 |
| Critical-defect guardrail | Same severity criteria | Critical-defect count | 0 permitted in AI condition |
| RQ3 error detection/repair | Identical seeded-defect review material | Detection and correct-fix rates | Novice vs experienced |
| RQ1 usage patterns | Short questionnaire + observed event counts | Use frequency, task purpose, prompts, verification | Novice vs experienced |

## Repository structure

```text
.
├── README.md
├── .gitignore
├── .dockerignore
├── Dockerfile
├── LICENSE
├── requirements.txt
├── configs/
│   └── config.json
├── src/
│   ├── __init__.py
│   └── benchmark.py
├── tests/
│   └── test_benchmark.py
├── data/
│   └── sample/
│       ├── trials.csv
│       ├── survey.csv
│       └── reviews.csv
├── docs/
│   ├── Methodology_Passport.md
│   └── Experiment_Protocol.md
├── notebooks/  # reserved for future analysis
├── .github/workflows/ci.yml
└── outputs/     # generated, ignored by Git
```

## Data collection and analysis notes

- **Experience classification:** novice = up to 2 years programming and no more than 6 months professional experience; experienced = at least 3 years programming and at least 1 year professional experience. Exclude ambiguous middle band rather than reassign it post hoc.
- **Task design:** all participants complete two comparable tasks (A/B); AI condition and order are balanced, avoiding direct repetition of exactly the same task for the same person.
- **RQ2 metric:** calculate `(baseline_seconds - ai_seconds) / baseline_seconds * 100` for each paired participant, then compare group means; the report prints the group difference as a descriptive effect, not a p-value.
- **Guardrails:** compare average functional pass-rate deltas in *each* experience group; also check for AI critical defects.
- **Limitations:** no causal inference about a participant's experience level, no hidden AI interaction telemetry, no genuine findings from synthetic data. For the real study, record task assignments and timeouts, establish a statistical plan (e.g., interval estimates or interaction model), record tool version, and obtain consent.

## Citation and license

For attribution, cite the project as: **Makhmutov, D. & Kasimov, A. (2026). Programmer Experience and AI Coding Assistant Effectiveness: Benchmark and Methodology Passport. Research Methods Task 2.**

Code distributed under [MIT License](LICENSE). Task 1 literature is documented in the prior report; references are not substituted with synthetic benchmark results.

## Collaboration and Git workflow

The public GitHub repository for this study includes the methodology/data schema and the tested measurement pipeline in genuine, descriptive commits. Each author should make their own contributions using their actual Git identity; do not fabricate contribution history. GitHub Actions runs the Docker image build and synthetic smoke test after push.
