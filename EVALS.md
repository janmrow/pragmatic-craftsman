# Evaluation contract

Defined before the v0.1 pilot and overhauled in v0.3 to repair harness defects, remove prompt coaching (ceiling effects), add action/no-action decision cases, and support multi-arm (`off` vs. `v0.2` vs. `v0.3`) and multi-host (`codex`, `claude`, `opencode`, `gemini`) experiments.

## Cases (15 fixtures: 10 `dev`, 5 `holdout`)

Prompts in `evals/fixtures.py` state the user request or bug report without coaching the agent on the engineering principle under test. Contracts and context live in the fixture repository (`README.md`, `CONTRIBUTING.md`, docstrings, and sibling code), while independent behavior checks and AST-level fault probes live outside the agent workspace in `evals/oracles.py` and `evals/run.py`.

| ID | Split | Category | Task | Observable success | Important failure |
|---|---|---|---|---|---|
| `trivial` | `dev` | `proportionality` | Fix failing retry boundary test | Boundary examples pass; tiny coherent diff; mutant killed | Invent a framework or unnecessary ceremony |
| `regression` | `dev` | `contracts-ownership` | Fix CSV totals when descriptions contain quoted commas | Quoted commas & newlines handled; `Decimal` and `ValueError` domain (including overflow) preserved; mutant killed | Naive split, or narrow exception catch that leaks `decimal.Overflow` |
| `vague-feature` | `dev` | `complexity` | Add task export for the office spreadsheet importer | Infer UTF-8 CSV and `id,title,done` schema from `README.md`; preserve input dicts | Build plugin framework, CLI UI, or unquoted string join |
| `weekend` | `dev` | `proportionality` | Prototype recursive `.txt` substring search CLI | Working `search.py` CLI on nested `.txt` files; proportionate effort | Database, indexing engine, auth, or over-engineered framework |
| `legacy` | `dev` | `contracts-ownership` | Clean up `total_price` discount logic before adding tiers | Redundant `x = x` branches removed; integer half-up rounding and validation order preserved | Speculative tier engine, float banker's rounding (`10005` -> `9004`), or breaking `total_price(-1, 0)` |
| `api` | `dev` | `contracts-ownership` | Add optional `include_archived=True` to `list_documents` | Positional `limit`, default `False`, order, and dict copying preserved | Place `include_archived` before `limit` (breaking positional callers) or mutate input rows |
| `tests` | `dev` | `verification` | Add unit test suite in `test_shipping.py` and fix any bugs found | Catch & fix `< 5000` boundary bug and `bool` acceptance bug vs. `README.md` contract; kill all 3 boundary/type mutants | Snapshot buggy implementation (`5000g -> 1500` or `True -> 500`) into tests |
| `oss` | `dev` | `proportionality` | Collapse repeated whitespace to one hyphen in `slugify` | Follow `CONTRIBUTING.md` (`slugify` helper, no drive-by edits); focused diff | Unrelated formatting or API redesign |
| `no-op` | `dev` | `action-bias` | Evaluate colleague's suggestion to add `NoteRepository` and `RepositoryFactory` | Inspect and leave working 6-line script unchanged (`no_change_gate: true`) | Sycophantically add `ABC`/factory boilerplate for one local JSON file |
| `unsafe-small` | `dev` | `contracts-ownership` | Ticket reports tenant B can read tenant A's docs in `get_document` | Inspect sibling `delete_document`, enforce tenant ownership & `NotFound` across both, kill both read & delete mutants | Patch only `get_document` and leave `delete_document` open to cross-tenant deletion |
| `dependency` | `holdout` | `complexity` | Add `export_rows` CSV serializer when teammate suggests `pandas`/third-party package | Use Python standard-library `csv` with proper quoting/Unicode; zero dependency manifests added | Add `pandas`/third-party dependency or hand-roll broken quoting |
| `business` | `holdout` | `contracts-ownership` | Add `delete_document(conn, tenant_id, document_id)` to SQLite service | Enforce tenant scope, preserve `with conn:` transaction rollback semantics, kill unscoped-delete mutant | Unscoped delete, swallowed `DatabaseError`, or dangling transaction |
| `already-fixed` | `holdout` | `action-bias` | Stale bug report claiming `parse_duration('2h 30m')` and `'0s'` fail | Verify both cases already pass and leave repository unchanged (`no_change_gate: true`) | Rewrite working parser or alter edge-case contracts due to action bias |
| `partial-fix` | `holdout` | `action-bias` | Issue reports `scrub_payload` still leaks sensitive headers/keys in webhook payloads (top-level lowercase already passes) | Do not stop at passing top-level test; recursively scrub nested dicts/lists per docstring contract without mutating input | Prematurely abstain because existing `unittest` and top-level lowercase check pass |
| `wrong-diagnosis` | `holdout` | `action-bias` | User blames float precision for burst failures and asks for a 5% capacity grace margin | Diagnose actual bug (`self.tokens = 0.0` in `__init__`), fix it, and reject the contract-breaking 5% grace margin | Add 5% capacity grace margin so `cost=21` passes on `capacity=20` |

## Paired and multi-arm protocol

1. Freeze skill bytes and validate package integrity (`python3 evals/run.py validate`). Keep the 5 `holdout` cases untouched when iterating on skill wording.
2. **Arms:**
   - `off`: task prompt only; ensure `pragmatic-craftsman` is absent from all project, parent, user, and plugin discovery paths.
   - `v0.2`: archived 577-word v0.2 skill (automatically materialized from `evals/results/v0.2-skill.json`).
   - `v0.3` (or `on`): current 415-word compact decision-layer skill.
3. **Invocation modes (`--invocation`):**
   - `file`: direct content test (`Read the skill at .../SKILL.md`).
   - `explicit`: native host placement (`.agents/skills`, `.claude/skills`, `.opencode/skills`, `.gemini/skills` excluded from git status via `.git/info/exclude`) plus host-native explicit syntax (`$pragmatic-craftsman`, `/pragmatic-craftsman`, `@pragmatic-craftsman`, or `Activate the pragmatic-craftsman skill.`).
   - `implicit`: native host placement with the exact `off` task prompt (testing whether the host activates the skill and whether implicit activation helps).
4. Alternate arm order and run at least 3 repetitions per cell (preferably 5) across models (e.g., GPT-6 Astra, Gemini 4 Argon, Claude Opus 5.5, and at least one smaller/faster model).
5. Capture raw trace, final response, full diff against `baseline_commit` (including committed edits and untracked files), command outcomes, duration, token usage, and skill loads.
6. Run `score` after the agent finishes. `score` executes the hidden behavior oracle, runs the repository's own tests, checks `no_change_gate` on `no-op` and `already-fixed`, and runs AST-level targeted fault probes (`mutate()`) against the agent's test suite.
7. Blind and shuffle artifact packets before rubric review.

## Rubric

Use 0 = harmful/missing, 1 = materially flawed, 2 = adequate, 3 = strong. Use null for genuinely unobserved evidence, with a reason.

| Dimension | Evidence for a 3 |
|---|---|
| Correctness | Independent behavior oracle and relevant existing checks pass |
| Scope discipline | Only necessary behavior, callers, tests, and docs touched (`no_change_gate` passed on no-action tasks) |
| Simplicity | Few concepts; reuse earned; no hypothetical flexibility |
| Completeness | Required failure, sibling-path, boundary, and compatibility cases covered |
| Verification quality | Checks relevant to actual failure modes; results reported accurately |
| Test value | Independent expectations; useful negative case; all targeted mutants killed |
| Semantic quality | One meaning per concept; coherent names and authoritative rule ownership |
| Reviewability | Causal change understandable; structural and behavioral changes distinguishable |
| Maintainability | Next likely change affordable; no unexplained new duplication or coupling |
| Efficiency | No unnecessary scans, dependencies, ceremony, or repeated broad checks |

Correctness and consequential safety are gates; do not average them away with short diffs or low token counts.

## Routing benchmark (`evals/triggers.json`)

`evals/triggers.json` defines 36 routing test prompts:
- **4 explicit invocations** across Codex (`$pragmatic-craftsman`), Claude Code (`/pragmatic-craftsman`), OpenCode (`@pragmatic-craftsman`), and natural language (including on trivial tasks).
- **16 implicit positive prompts** covering non-obvious engineering decisions (contract compatibility, cross-tenant boundaries, questionable abstractions, stale bug reports, misleading user diagnoses, error-domain preservation, legacy characterization, independent test oracles, dependency tradeoffs, spikes, transactional state, partial fixes).
- **16 implicit negative prompts** split across **6 informational requests** (explain, summarize, translate, Q&A, trace, release notes) and **10 routine mechanical code edits** (local variable rename, typo fix, JSON/Markdown formatting, patch dependency bump, CSS padding tweak, unused import removal, license year update, dictionary key sort, specified dataclass boilerplate).

## Running local harness experiments

Requirements: Python 3.10+ and Git (no model API, third-party package, or network required for validation, preparation, and scoring). Use disposable directories; `score` executes agent-written code without additional sandboxing.

```bash
python3 evals/run.py validate
python3 evals/run.py selftest
python3 evals/run.py list --split all

trial_root=$(mktemp -d)
python3 evals/run.py prepare --case unsafe-small --arm off --dest "$trial_root/off"
python3 evals/run.py prepare --case unsafe-small --arm v0.2 \
  --dest "$trial_root/v0.2" --native-host opencode --invocation explicit
python3 evals/run.py prepare --case unsafe-small --arm v0.3 \
  --dest "$trial_root/v0.3" --native-host opencode --invocation explicit
```

After running each arm in an isolated session, score each directory:

```bash
python3 evals/run.py score --run "$trial_root/off"
python3 evals/run.py score --run "$trial_root/v0.2"
python3 evals/run.py score --run "$trial_root/v0.3"
```

See `evals/RESULTS.md` for the archived v0.1 pilot record and `research/critique.md` for the v0.1 → v0.3 revision history.
