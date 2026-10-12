# Qualitative Analysis Plan — AI Coding Assistant Study

**Project:** The Influence of Programmer Experience Level on the Effectiveness of AI Tools in Programming  
**Study:** Research Methods Task 2 (pre-data-collection methodology)  
**Status:** Planned analysis only. This document contains no participant findings.

## Why qualitative data are included

The experiment's quantitative outcomes measure completion time, functional correctness, code quality and defect verification. Short open-ended responses and structured observation notes help explain **how** participants approached GitHub Copilot suggestions. This complements, but does not replace, the numerical comparison between novice and experienced programmers.

The study is therefore *mixed-methods with a quantitative core*. The qualitative component specifically supports **RQ1 (usage strategies)** and interpretation of **RQ2–RQ3 (why time or verification outcomes may differ)**.

## Collection procedure

1. After the paired programming tasks, ask each participant two optional, open-ended questions, using the same wording for both experience groups:
   - "When did you accept, modify or reject an AI suggestion, and why?"
   - "How did you decide whether the AI-generated code was correct or safe?"
2. Record brief observations using a common template: pseudonymous participant ID; experience group; task/condition; observation timestamp; observed action; verbatim participant comment when volunteered; researcher's interpretation stored in a separate field.
3. In the standardized seeded-defect code-review task, record any explanation the participant volunteers for finding or missing a defect, without prompting them toward a particular answer.
4. Avoid recording names, private repository content, credentials, or unrelated personal details. Obtain informed consent and permit skipped questions.

## Initial coding scheme (subject to revision)

| Code | Definition | Example of an action that would qualify |
|---|---|---|
| `ACCEPT_DIRECT` | Accepts AI-generated code with no meaningful revision | Inserts a complete suggested function unchanged |
| `VERIFY_TEST` | Uses execution or unit tests to validate a suggestion | Runs automated tests after accepting AI code |
| `VERIFY_READ` | Manually checks logic or requirements before acceptance | Compares output with specification or traces control flow |
| `REVISE_OUTPUT` | Edits AI-generated code to fix issues or adapt style | Changes validation logic in a generated solution |
| `REJECT_OUTPUT` | Declines an unsuitable AI suggestion | Discards a proposed implementation |
| `EXPLORE_AI` | Uses AI primarily to understand or compare approaches | Requests an explanation rather than final code |
| `OVERRELIANCE_RISK` | Accepts questionable output without verification | Uses a suggestion despite uncertainty about correctness |

These are **proposed analytic labels, not observed counts**. Multiple codes may apply to a single observation. Do not assume novice or experienced participants will exhibit any particular behavior.

## Analysis process

1. Remove identifying information and separate direct observations from researcher interpretations.
2. Read the notes in full, then pilot the codebook on a small subset; record code definition changes in a dated memo **before** coding the full dataset.
3. Apply one or more codes to each segment, retaining an anonymized evidence excerpt and links to task ID and condition.
4. Where feasible, have two reviewers independently code a subset, discuss disagreements, and record final coding decisions. Do not claim inter-rater reliability unless it has actually been assessed.
5. Compare **themes** across experience groups and AI-use conditions without treating isolated anecdotes as causal evidence.
6. Triangulate coded patterns with prompt counts, accepted-suggestion counts, verification events, task time, unit-test results and seeded-defect review outcomes.
7. Report exceptions and negative cases as well as common patterns. Distinguish planned explanations from conclusions justified by collected data.

## Integration with quantitative metrics

| Research question | Quantitative data from current pipeline | Qualitative interpretation |
|---|---|---|
| RQ1 | Uses/week and primary use; recorded prompt and verification counts | How programmers decide to accept, question or reject suggestions |
| RQ2 | Paired AI/no-AI time benefit and code-quality guardrails | Whether observed checking or modification strategies may help interpret different task outcomes |
| RQ3 | Seeded defects detected/fixed and review time | Descriptions of reasoning, review and validation practices |

The existing `src/benchmark.py` **does not automatically collect, transcribe or code open-ended observations**. The qualitative stage will be conducted separately during real data collection. Synthetic CSV fixtures are only for verifying that the numerical pipeline executes; they must never be described as participant responses.

## Data management and limitations

- Keep raw interview/observation notes in an approved private study location; do **not** commit real participant notes to the public GitHub repository.
- Use pseudonymous IDs matching the existing trials/survey/reviews data model when integrating results, without publishing an identifying key.
- Predefine the sampling window and maintain an audit trail of codebook revisions.
- Treat experience as an observed characteristic, not a randomized treatment. The AI/no-AI task assignment is counterbalanced, but experience-group differences alone are not proof of causality.
- Present coded material as contextual evidence. Confirmatory tests and inferential conclusions require real participant data and a prespecified statistical plan.
