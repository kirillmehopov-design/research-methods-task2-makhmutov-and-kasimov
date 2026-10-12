# Experimental protocol (proposal; Week 7 real data collection)

1. Recruit participants voluntarily and record informed consent without collecting personally identifying information. Assign pseudonymous participant IDs.
2. Classify participants using total programming experience and professional experience. Do not retrospectively change categories.
3. Hold constant language, VS Code version, machine class, time limit, test suites, task difficulty and GitHub Copilot version. Record those versions in study metadata.
4. Randomize/counterbalance order: half in each group complete task A with AI then task B without AI; the other half receive task A without AI then task B with AI. Check comparability of A/B via a small pilot.
5. Use a standard timer and automated test runner; log start/stop times, task ID, passed/total unit tests, static-analysis defect counts and critical defects. With AI, record prompt events, accepted suggestions and verification actions using a consistent rubric.
6. Administer a short AI-use questionnaire (weekly frequency, primary use, prior experience) and provide a separate code-review task with identical seeded errors to all participants.
7. Store a row per participant-condition in the trials CSV, one review row, one survey row. Validate completeness using `python src/benchmark.py`. Protect data and avoid committing names or private responses.
8. In Week 7+, replace synthetic sample paths in `configs/config.json` with approved anonymized collected data, set `sample_is_synthetic` to `false`, run on the same pinned environment, and preregister confirmatory tests before inspecting outcomes. Descriptive output by itself does not prove a hypothesis.

## Operational definitions

- `time_reduction_pct`: `(no_ai_seconds - ai_seconds) / no_ai_seconds * 100` for the same participant.
- Primary estimand: `mean(time_reduction_pct|experienced) - mean(time_reduction_pct|novice)` in percentage points.
- Secondary guardrails: average within-group test-pass delta must be at least `-0.05`; AI task critical-defect count must be `0`.
- Seeded review task: identical AI-generated code and defect inventory for both experience groups. Review seconds, number discovered and number correctly fixed are recorded.
- Real participants may stop or opt out at any time; avoid collecting private project code or access tokens.
