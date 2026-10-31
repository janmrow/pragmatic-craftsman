# Evaluation contract

Defined before the v0.1 pilot and updated with v0.2 protocol notes. This is a decision-quality experiment, not a line-count contest.

## Cases

| ID | Task | Observable success | Important failure |
|---|---|---|---|
| trivial | Correct an inclusive retry boundary | Existing boundary examples pass; tiny coherent diff | Invent a framework or testing stack |
| regression | Fix CSV totals containing a quoted comma | CSV grammar handled; documented invalid-row behavior; behavioral regression test | Split strings or silently ignore bad rows |
| vague-feature | Add export to an internal task tracker | Infer CSV from existing consumers, state assumption, working export | Build plugin system or block on cosmetic choices |
| weekend | Explore whether a local text search is useful | Runnable experiment and evidence about the question | Authentication, database, deployment, speculative architecture |
| legacy | Make an awkward working price calculation easier to change | Preserve rounding, invalid-input behavior and existing API | Rewrite the module or silently change semantics |
| dependency | Add correctly quoted CSV export | Existing/platform mechanism used correctly | Add dependency merely for a few lines, or hand-roll a parser |
| api | Add optional archived-record filtering to a public library | Existing positional calls and default behavior preserved | Change defaults or return shape |
| tests | Add useful tests to a poorly tested shipping calculator | Independent expected values, thresholds, invalid input | Snapshot current implementation or assert private calls |
| oss | Fix a documented slug edge case | Follow contributor checks and canonical helper, focused diff | Drive-by formatting, unsolicited API redesign |
| business | Add a tenant-aware document deletion operation | Authorization, transaction behavior, failure evidence and rollback implications | Happy-path implementation that risks another tenant's data |
| no-op | Consider a generic repository abstraction for one stable store | Inspect and leave working source unchanged; explain concrete reason | Invent requirements to justify code |
| unsafe-small | Prevent cross-tenant document access | Cover read and delete boundaries, preserve not-found policy, tests for isolation | Patch only one endpoint or trust a caller-supplied owner |

All cases have runnable standard-library Python fixtures; preparation copies only task-local files. They are small synthetic proxies, not evidence of success on a production system. Prompts, independent oracles and test mutations are kept outside each agent's repository.

## Paired protocol

1. Freeze skill bytes and fixture version. Use fresh, identical repositories for each arm. Record agent CLI version, exact model, effort, permissions, machine, timestamps and loaded instruction files.
2. **Off:** task prompt only; ensure this skill is absent from project, parent, user and plugin discovery. **On:** same prompt plus explicit skill invocation. A direct file read is a content test; native loader activation is a separate test.
3. Alternate arm order. Run at least 3 repetitions per case for a pilot, preferably 5. Keep tool/time budgets equal. Disable auto-memory, unrelated plugins and internet for these offline fixtures where the host supports this. Do not weaken normal safety boundaries.
4. Capture raw trace, final response, full diff including untracked files, command outcomes, duration, usage when exposed, and skill file reads. No trace means process dimensions are unobserved, not zero.
5. Run `score` after the agent ends. Inspect its own tests and run a task-specific plausible mutant against them. A green test suite alone is not a test-value score.
6. Shuffle and blind artifact labels for review. Judge task and diff before seeing arm; use the same rubric for both. Do not give the coding agent grading criteria, reference answers or the other arm's output.
7. Keep failures. Report per-case paired results and raw denominators. Inspect variance; don't claim an improvement from one run or aggregate away a safety regression.

## Rubric

Use 0 = harmful/missing, 1 = materially flawed, 2 = adequate, 3 = strong. Use null for genuinely unobserved evidence, with a reason. Judge quality against task context, not ideal architecture.

| Dimension | Evidence for a 3 |
|---|---|
| Correctness | Independent behavior oracle and relevant existing checks pass |
| Scope discipline | Only necessary behavior, callers, tests and docs touched |
| Simplicity | Few concepts; reuse earned; no hypothetical flexibility |
| Completeness | Required failure, boundary and compatibility cases covered |
| Verification quality | Checks relevant to actual failure modes, results reported accurately |
| Test value | Independent expectations; useful negative case; relevant mutant killed |
| Semantic quality | One meaning per concept; coherent names and ownership |
| Reviewability | Causal change understandable; structural and behavior changes distinguishable |
| Maintainability | Next likely change affordable; no unexplained new duplication/coupling |
| Efficiency | No unnecessary scans, dependencies, process or repeated checks |

Correctness and consequential safety are gates. Do not average them away with short code or cheap tokens. Record changed files, added/deleted lines, command counts, skill loads, tokens and wall time as diagnostics, not direct rewards. TDD chronology is observable from a trace, not inferred from the final test file. Tests added after implementation can score highly if their oracle is independent.

## Activation and disclosure tests

Native-host tests: confirm discovery and explicit or implicit invocation. In v0.2, `SKILL.md` is self-contained (no `references/` directory) and `agents/openai.yaml` enables normal implicit matching (`allow_implicit_invocation: true`). For controlled A/B experiments, keep the `off` arm free of `pragmatic-craftsman` across all project, parent, user, and plugin discovery paths rather than relying on adapter flags.

Positive implicit candidates cover software creation and modification—adding features, starting projects, setting up test infrastructure, fixing bugs, and refactoring. Negative candidates cover general explanations, summaries, translation, and mechanical formatting: “Explain this function”; “Summarize this diff”; “Translate this comment”; “Format this JSON document.” Explicit invocation should work on all fixture sizes, including `trivial`.

Test at least 6 positive and 6 adjacent negative prompts, 3 repetitions each. A description-only routing exercise is a proxy, not native activation evidence. No always-read research documents.

## Running local harness experiments

Requirements: Python 3.10+ and Git (no model API, third-party package, or network required for fixture preparation and scoring). Use disposable directories; `score` executes agent-written code without additional sandboxing.

```bash
python3 evals/run.py list
python3 evals/run.py selftest

trial_root=$(mktemp -d)
python3 evals/run.py prepare --case regression --arm off --dest "$trial_root/off"
python3 evals/run.py prepare --case regression --arm on \
  --dest "$trial_root/on" --skill "$PWD/pragmatic-craftsman" --native-host codex
```

After running each arm in an isolated session (`off` must have no project or global `pragmatic-craftsman` skill in its discovery paths), score both directories:

```bash
python3 evals/run.py score --run "$trial_root/off"
python3 evals/run.py score --run "$trial_root/on"
```

## Queued harness and fixture repairs (deferred)

Static review before v0.2 consolidation identified three harness and fixture issues to repair in a dedicated evaluation update before running new trials:

1. **Baseline-commit diffing (`evals/run.py`):** `score()` diffs against `HEAD` rather than `meta['baseline_commit']` (which would hide changes if an agent runs `git commit`) and omits untracked files from `git_numstat`. `--native-host` also commits the installed skill as `HEAD` inside the fixture repo.
2. **Mutation-probe specificity (`evals/run.py`):** `mutate()` reverts entire baseline files on `trivial` and `regression` rather than applying a single targeted defect, and mutates only `get_document` on `unsafe-small`.
3. **Fixture prompt ceiling and oracle coverage (`evals/fixtures.py`, `evals/oracles.py`):** Several prompts explicitly state the engineering judgment under test (e.g., `no-op`, `weekend`, `api`, `unsafe-small`), `vague-feature` removes ambiguity in its `README.md`, `tests` has no discrepancy between `shipping.py` and `README.md`, and `legacy` passes `score()` with zero edits.

## Adoption decision

For the local pilot: no new correctness/safety failures, no systematic ceremony on trivial/no-op tasks, and useful paired gains in at least two decision dimensions on non-trivial tasks. These are provisional acceptance criteria, not statistical significance. Add real repository tasks before general adoption. Retain a holdout of new tasks after revisions.

## Unresolved hypotheses

- Does the consolidated v0.2 skill improve decisions beyond a capable agent's existing instructions once fixture prompts stop pre-specifying the tradeoff?
- Does normal implicit description matching (`allow_implicit_invocation: true`) activate on intended coding tasks without over-triggering on explanations or mechanical edits?
- Does consequence-based effort scaling reduce waste on trivial production changes while protecting high-consequence boundaries?
- Do the contract-preservation and independent-oracle rules transfer beyond these Python fixtures?
- *(Resolved in v0.2 by consolidation)* Whether the two v0.1 reference files (`design-decisions.md`, `evidence.md`) earned separate retrieval cost: removed due to heavy overlap with `SKILL.md` and zero observed loads in v0.1 pilot handoffs.

See `evals/RESULTS.md` for the archived v0.1 pilot execution record.
