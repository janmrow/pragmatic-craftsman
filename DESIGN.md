# pragmatic-craftsman design

A portable, self-contained **decision-quality layer for coding agents**. Rather than trying to teach a capable model how to write code, `pragmatic-craftsman` intervenes on the specific engineering judgment failures that remain common even in frontier coding agents. Its organizing credo is:

> **Solve the real problem. Keep the solution clear and complete. Make the next change easier.**

User instructions and repository-specific rules take precedence. The skill is not a book summary, a substitute for domain expertise, a project manager, a style guide, an audit framework, or mandatory ceremony. Its value should appear in decisions and code rather than process narration.

## Intellectual and empirical center

**The Pragmatic Programmer (20th Anniversary Edition)** supplies feedback-limited commitment, authoritative knowledge ownership (DRY vs. coincidental textual similarity), domain language, tracer bullets versus learning prototypes, reversibility, and context-dependent quality.

**The Software Craftsman** supplies professional accountability, sustainable changeability, viable alternatives when constraints conflict, and technical practices justified by value rather than ritual. Sandro Mancuso's *Software Craftsmanship in the AI Era* sharpens the focus on semantic boundaries, human reviewability, and independent test expectations; his *Should we always use TDD to design?* keeps TDD contextual alongside spikes and contract sketches.

**Complementary complexity lens:** *Just Enough* (`janmrow/just-enough`) contributes the habit of asking what added complexity buys today compared with a simpler alternative, preserving complexity that genuinely earns its cost, and stopping when further refinement no longer pays off. Martin Fowler's accounts of *YAGNI* and *Beck's Simple Design Rules* reinforce that rejecting speculative features does not mean rejecting refactoring, clarifying boundaries, or investing in near-term changeability.

**Empirical failure modes of coding agents:**
- **Action bias & premature abstention (`E5`, FixedBench):** Coding agents frequently modify already-correct code on stale reports or unwarranted requests, yet naive "reproduce first" instructions can make them abstain prematurely on partially fixed issues.
- **Self-confirming verification (`E6`, TestSuiteBench):** Agents often build software they fail to verify adequately, writing tests that mirror implementation assumptions or miss boundary and error-domain mutants.
- **Always-on instruction overhead (`E3`, SRI/ETH `AGENTS.md` study):** Broad repository context files can increase exploration and testing cost without improving task success, motivating a compact, conditionally activated skill rather than always-on generic advice.

## Architecture decision

| Candidate | Assessment |
|---|---|
| **A: Compact single-file `SKILL.md` (~415 body words)** | **Chosen (v0.3).** Progressive disclosure already occurs between YAML frontmatter metadata and the skill body. Compressing from v0.2's 577 body words to 415 dense words removes generic coding advice ("read relevant files", "use domain names") and highlights high-contrast decision rules. |
| B: Broader single-file `SKILL.md` (v0.2, 577 body words) | Consolidated v0.1's three files into one, but used a catch-all coding `description` and retained ~30% generic guidance that capable models already follow by default. Archived in `evals/results/v0.2-skill.json` for 3-arm comparisons. |
| C: Small core with contextual `references/` (v0.1, 1,493–1,543 words) | Rejected after v0.1 review: the two short references overlapped heavily with the root file and were never loaded in v0.1 pilot handoffs. Initial pilot snapshot archived in `evals/results/iteration-1-skill.json`. |
| D: Modes, scripts, and multi-skill chains | Unnecessary coordination and maintenance overhead for an engineering decision skill. |

Installed package:

```text
pragmatic-craftsman/
  SKILL.md
  agents/openai.yaml
```

`SKILL.md` uses standard `name`, `description`, and `license: MIT` frontmatter and a self-contained Markdown body; exact file hashes and word counts are validated against `MANIFEST.json` by `python3 evals/run.py validate`. `agents/openai.yaml` supplies optional OpenAI/Codex display metadata and invocation policy. All research, design rationale, and evaluation tools live outside the installed package.

## Target failure modes and behavioral commitments

The skill organizes judgment around four connected commitments—applied directly in work rather than recited as response sections:

| Agent failure mode | `pragmatic-craftsman` commitment |
|---|---|
| **Action & sycophancy bias** (modifying working code on stale reports, blindly building a user-suggested mechanism, or stopping at the first passing check on a partial fix) | **1. Verify the gap before acting:** Separate the needed outcome from a suggested mechanism or diagnosis. Leave working code unchanged when no gap exists; inspect sibling paths and nested cases when a bug is only partially fixed. |
| **Architecture / complexity bias** (adding speculative abstractions, hooks, or dependencies—or refusing structure that improves present clarity and isolation) | **2. Make complexity earn its place:** Require present value over a simpler alternative and prefer existing platform capabilities, while introducing boundaries or test scaffolding when they improve present correctness, isolation, or near-term changeability. |
| **Semantic & contract drift** (patching only one endpoint of a shared invariant, deduplicating across distinct trust boundaries, or silently narrowing caller-visible error domains and signatures) | **3. Protect ownership and contracts:** Give each domain or security rule one authoritative owner across affected entry points, keep independent enforcement across trust boundaries, and preserve caller-visible signatures, defaults, return shapes, and error domains unless authorized. |
| **Disproportionate ceremony & self-confirming tests** (running heavyweight process on a 1-line fix, under-verifying destructive prototype code, or mirroring buggy code into test assertions) | **4. Scale effort and verify independently:** Scale effort to blast radius, reversibility, and failure cost rather than repo labels; derive test expectations from contracts or hand-worked examples, investigate code-vs-contract disagreements, and ensure a plausible wrong implementation would fail. |

## Activation contract

Unlike v0.2's broad "everyday software engineering" description, v0.3 targets **diagnosing bugs, evaluating abstractions or dependencies, refactoring, changing APIs or security/state boundaries, and writing test suites—where root cause, scope, caller contracts, or test oracles can be mistaken**. Explanations, summaries, Q&A, and routine mechanical edits (renames, formatting, typos, minor dependency bumps, CSS tweaks, standard boilerplate) are excluded unless `pragmatic-craftsman` is explicitly invoked.

In `agents/openai.yaml`, `allow_implicit_invocation: true` remains enabled so supporting hosts can match the narrowed description automatically alongside explicit invocation (`$pragmatic-craftsman` in Codex, `/pragmatic-craftsman` in Claude Code, `@pragmatic-craftsman` in OpenCode, or skill activation in Gemini CLI). During controlled A/B evaluations, the `off` arm must be isolated by keeping the skill out of all project and global discovery paths, and routing, explicit invocation, and skill content are evaluated as distinct experimental questions.
