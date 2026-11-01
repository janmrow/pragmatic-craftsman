# Executed evaluation (v0.1 archive) — 2026-10-31

Historical record of the v0.1 pilot (which tested the earlier three-file prototype with `references/design-decisions.md` and `references/evidence.md`). Neither the archived v0.2 single-file skill (`evals/results/v0.2-skill.json`) nor the current v0.3 compact decision-layer skill has been evaluated across full multi-model trials yet; no empirical superiority over the baseline is claimed.

## What ran

- Schema validation of the installable skill passed; both relative references exist. The core has no network/tool dependency.
- All 12 fixture baselines behaved as the harness self-test expected: 3 already-working baselines passed the behavior oracle; 9 intentionally incomplete/broken baselines failed it.
- Native file placement for Codex, Claude Code and OpenCode, native-mode prompt construction and the nonempty-destination guard were exercised. The native agents themselves were unavailable in this environment.
- **Six paired content trials, 12 fresh subagent sessions**, used the same task prompts and isolated repos: trivial bug, CSV regression, tenant isolation, no-op abstraction request, weekend experiment, public API extension. Arm order alternated across cases.
- **One further paired trial, 2 fresh sessions**, repeated the unchanged CSV prompt after a general error-contract instruction revision. No failing input or intended fix was disclosed to either coding agent.
- Three independent critique reviewers covered all six requested perspectives before the pilot; the critique changed the prototype. A separate fresh reviewer graded 12 anonymized artifact packets without arm labels.

These are direct skill-file content tests, not native Codex/Claude/OpenCode loader tests. The baseline inherited the platform's existing engineering instructions; it was not an unguided model. Exact serving model ID, effort, per-session cost, token usage and raw action traces were not exposed. Commands in handoff summaries are self-reports; independent execution checks and complete file diffs are retained. This is a small unreplicated pilot, not a statistical comparison.

## Behavioral results

| Case | First off | First on | Material observation |
|---|---|---|---|
| trivial | pass | pass | Same one-line fix; existing test was enough. |
| regression | pass | **fail strengthened oracle** | Both handled quoted CSV. On missed arithmetic overflow's ValueError contract. |
| unsafe-small | pass | pass | Both repaired read and delete through one ownership rule and added six tests. |
| no-op | pass | pass | Both left all source unchanged; existing check passed. |
| weekend | pass | pass | Both built small local CLIs and distinguished synthetic mechanics from actual usefulness. No retained unittest suite; runtime oracle passed. |
| api | pass | pass | Both preserved positional callers and defaults. On supplied more compatibility tests and brief API docs; neither added a framework. |

The initial minimal behavior oracle passed all 12 artifacts. Blind review then identified an untested error-contract regression: `invoice_total('description,amount\nTea,1e1000000\n')` formerly translated decimal overflow to ValueError, but one replacement caught only InvalidOperation. Running that case confirmed it. The final oracle includes it. Under that stronger oracle, first off is **6/6**, first on **5/6**.

Revision: root guidance now explicitly compares caller-visible failure behavior when replacing a mechanism, with detail in the evidence reference. In the repeated unchanged CSV task, **both off and on failed the overflow case** while their own four tests passed. This does not show that the revision fixed the failure. It also shows why one successful baseline run does not establish a reliable baseline rate.

The final candidate's error-contract behavior remains an unresolved weakness. Do not add many narrow instructions merely to fit one numeric example. Next test whether a compact failure-example requirement or better reference routing earns its cost on unseen boundary substitutions.

## Rubric comparison

Blind LLM artifact judgments on the first 12 candidates, 0–3; these are descriptive, uncalibrated judgments, not objective measurements. The reviewer found the overflow gap independently, then received confirmation of its execution. No aggregate score is used because correctness is a gate. Missing history/metrics remain unobserved.

| Dimension | Off mean | On mean |
|---|---:|---:|
| correctness | 3.00 (n=6) | 2.67 (n=6) |
| scope_discipline | 3.00 (n=6) | 3.00 (n=6) |
| simplicity | 3.00 (n=6) | 3.00 (n=6) |
| completeness | 3.00 (n=6) | 2.67 (n=6) |
| verification_quality | 2.67 (n=6) | 2.50 (n=6) |
| test_value | 3.00 (n=5) | 2.80 (n=5) |
| semantic_quality | 3.00 (n=5) | 2.80 (n=5) |
| reviewability | 3.00 (n=6) | 3.00 (n=6) |
| maintainability | 3.00 (n=6) | 2.83 (n=6) |
| efficiency | unobserved | unobserved |

Most dimensions tied at this coarse scale; the error-contract failure lowers on scores. Efficiency could not be scored honestly. One extra no-test unittest discovery appeared in the on weekend handoff, but there is no trace-level cost comparison. Fewer source lines or tests are not a proxy for efficiency.

## Test sensitivity

Targeted wrong versions were killed by the existing/authored tests in all evaluated trivial, quoted-CSV and tenant-isolation cells, including the two repeat CSV cells. They demonstrate sensitivity to those defects. They **did not** establish complete regression protection: tests that caught the CSV-parser mutant still missed the overflow contract. The no-op and public-API mutation probes were not implemented. No mutation score is assigned to the throwaway experiment without retained tests.

## Limits and next experiments

Only 6 of 12 cases received model trials. Legacy refactoring, dependency choice, vague feature scope, adding tests, small OSS contribution and SQLite business deletion have runnable fixtures/oracles but remain unrun by agents. All cases are small Python proxies; no real application performance, production safety or cross-language transfer was established.

The final skill snapshot differs from the first pilot by the error-contract sentence and reference paragraph; only the CSV pair was rerun against that revision. Native explicit/implicit discovery and progressive disclosure remain unverified at host level. The public-API and weekend on handoffs reported reading the root and no optional references; these are reports rather than loader traces.

Priorities: (1) native CLI A/B with recorded exact model/trace; (2) repeated boundary-substitution tasks plus unseen holdouts; (3) remaining fixture contexts and a real repository contribution; (4) core-only ablation to measure whether the two references earn their cost. Do not broaden activation until correctness and proportionality gates hold.

## Artifact guide

`cell-a` through `cell-l` are the first paired trials; `cell-m`/`cell-n` are repeated CSV off/on. Each includes original prompt, provenance, complete final repository files, diff and independent check output. `.git` and interpreter caches are omitted. Use `prepare` to create a fresh scored repository; copied result folders are evidence, not restartable worktrees.

`blind-packets.json`, `blind-scores.json` and `blind-map.json` allow auditing the blinded review. The packets preserve the original minimal-oracle pass flags; per-cell checks use the strengthened final oracle. `iteration-1-skill.json` preserves the initial v0.1 pilot skill bytes; `cell-n/run.json` records the hashes of the post-pilot v0.1 error-contract revision; `v0.2-skill.json` preserves the v0.2 consolidated skill bytes. The shipped `pragmatic-craftsman/` package and `MANIFEST.json` now contain the v0.3 compact decision-layer skill. No raw subagent action transcript is claimed or fabricated.
