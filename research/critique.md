# Adversarial critique and revision

Three fresh-context reviewers inspected only the first skill folder, each covering two requested perspectives. They received no intended diagnosis. This is a qualitative design review, not proof of runtime effectiveness. The paired content pilot used the revised bytes.

| Perspective | Concrete problem found | Revision actually made |
|---|---|---|
| Pragmatic Programmer | “Obtain feedback” could turn small steps into repeated approval stops. “Fewer concepts” could reject useful domain states. | Require slice validation and continue authorized scope; judge refactoring by responsibility and change risk, allowing concepts that expose invariants. |
| Software Craftsmanship | No explicit response when constraints conflict with essential quality; DRY could remove repeated enforcement. | Offer a smaller complete outcome without silently lowering correctness/safety; preserve safeguards at separate trust boundaries. |
| AI-agent engineer | The no-change rule could suppress a requested nonfunctional refactor. Evidence expiry was too broad. | Include maintainability in the intended outcome; bind evidence to checked code, dependencies, environment and claim. Required gates cover delivered state. |
| Senior OSS maintainer | Subjective “clearer” could permit drive-by cleanup; invisible consumers could be treated as hypothetical. | Refactor only to remove a concrete obstacle/risk; follow public compatibility/deprecation policy; report material adjacent defects without silently expanding scope. |
| Startup engineer | “Preserve safeguards” did not require safeguards absent from new code. Production recovery advice applied too broadly. | “Provide or preserve” necessary controls; recovery/observation detail applies to material production exposure/data risk. |
| SDET/quality engineer | Independent AI examples can share the same error; round trips can share defects; local integration can still point at live systems. | Ground decisive expectations in a contract, hand calculation, trusted reference or consumer requirement; flag round-trip weakness; use isolated integration fixtures and account for partial failures/retries/concurrency. |

Other applied changes: remove the book-name sentence from runtime instructions (attribution remains in research/design); require reasonable investigation/setup before labeling a check unavailable; retain a concise report of material gaps.

Not adopted: widening automatic triggering to all consequential coding work. Explicit-first experimentation and a description tied to tradeoff requests better satisfy the project's over-triggering constraint. Whether selective implicit activation is worthwhile remains an eval hypothesis.

Pilot follow-up: no new root instructions were added merely because the baseline performed similarly. The weekend skill-on agent ran unittest discovery despite having no tests; this is a small redundant check, not evidence that another unconditional prohibition is needed. Both arms used behavior-specific smoke checks. Native loader and repeated-run evaluation are the next meaningful tests.

A later blind artifact review caught an arithmetic error-domain regression in a CSV replacement that passed the original oracle. The final root gained one general sentence about comparing caller-visible failures; the evidence reference gained a paragraph about substitution error domains. The oracle was strengthened and the unchanged task rerun. Both new arms still missed that case. This revision is retained as a plausible control, not presented as a validated fix. See evals/RESULTS.md.

## v0.2 concept and repository review

A subsequent whole-repository review examined the v0.1 prototype, research trail, harness and pilot artifacts before further trials:

- **Consolidated runtime skill:** `references/design-decisions.md` and `references/evidence.md` overlapped heavily with `SKILL.md` and were not reported as loaded in the v0.1 pilot handoffs. Their high-leverage rules (legacy characterization, independent expectations, test sensitivity, never weakening failing assertions to force a pass, and preserving caller-visible contracts) were folded into a single self-contained `SKILL.md`, and `references/` was removed.
- **Constructive complexity lens:** Incorporated *Just Enough* (`R16`) and Fowler's *YAGNI* / *BeckDesignRules* (`C10`/`C11`) so the skill guides constructive structure (new projects, test setups, clarifying boundaries) as well as restraint, and stops when further refinement no longer earns its cost.
- **Behavioral precision and daily activation:** Broadened the `SKILL.md` description to everyday software implementation and change, clarified that non-implementation exclusions apply unless `pragmatic-craftsman` is explicitly invoked, calibrated verification by change consequences rather than repository label, bounded contract changes to authorized scope, and enabled `allow_implicit_invocation: true` in `agents/openai.yaml`.
- **Deferred evaluation repairs:** Static harness and fixture findings are tracked in `EVALS.md` for a separate repair pass, preserving historical v0.1 artifacts intact.

## v0.3 decision-layer repositioning and evaluation overhaul

A second audit evaluated v0.2 against current vendor skill guidance (OpenAI Astra, Anthropic Opus, Google Gemini CLI, OpenCode v2) and empirical coding-agent benchmarks (`E3`, `E5` FixedBench, `E6` TestSuiteBench):

- **From catch-all coding advice to a decision-quality layer:** Capable coding models do not need instructions to read files, use sensible names, or run tests. `SKILL.md` was compressed from 577 to 415 body words, removing generic competence reminders and focusing on four high-leverage failure modes: action/sycophancy bias (including wrong user diagnoses and partial-fix premature abstention), speculative complexity vs. earned structure, semantic/contract/error-domain drift (including not silently narrowing caught exceptions), and self-confirming verification.
- **Precedence and calibrated activation boundary:** Added `Repository rules and informed user constraints take precedence` and `license: MIT` in frontmatter. Focused `description` on diagnosing bugs, evaluating abstractions/dependencies, refactoring, changing APIs or security/state boundaries, and writing test suites where root cause, scope, contracts, or test oracles can be mistaken—skipping explanations and routine mechanical edits.
- **Evaluation harness and fixture repairs (`evals/run.py`, `evals/fixtures.py`, `evals/oracles.py`, `evals/triggers.json`):** Repaired `score()` to diff against `baseline_commit` and include untracked files in `git_numstat`; excluded `--native-host` skill files via `.git/info/exclude`; replaced whole-file reverts with AST-level multi-probe mutations (including both read and delete on `unsafe-small` and 3 boundary/type probes on `tests`); removed prompt coaching across fixtures; introduced real code-vs-contract discrepancies in `tests` and AST cleanup checks in `legacy`; added three holdout action-judgment cases (`already-fixed`, `partial-fix`, `wrong-diagnosis`); expanded `triggers.json` to 36 prompts including 10 routine mechanical coding negatives; and added `validate` + GitHub Actions CI.
