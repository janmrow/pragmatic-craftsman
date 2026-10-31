# pragmatic-craftsman design

A self-contained engineering judgment skill for everyday software implementation and change: adding features, starting projects, creating test infrastructure, fixing bugs, and refactoring. Its organizing credo is:

> **Solve the real problem. Keep the solution clear and complete. Make the next change easier.**

It is not a book summary, a substitute for domain expertise, a project manager, a style guide, an audit framework, or a rigid development lifecycle. Its value should appear in decisions and code rather than process narration.

## Intellectual center

**The Pragmatic Programmer (20th Anniversary Edition)** supplies feedback-limited commitment, authoritative knowledge ownership (DRY vs. coincidental textual similarity), domain language, tracer bullets versus learning prototypes, reversibility, and context-dependent quality.

**The Software Craftsman** supplies professional accountability, sustainable changeability, viable alternatives when constraints conflict, and technical practices justified by value rather than ritual. Sandro Mancuso's *Software Craftsmanship in the AI Era* sharpens the focus on semantic boundaries, human reviewability, and independent test expectations; his *Should we always use TDD to design?* keeps TDD contextual alongside spikes and contract sketches.

**Complementary complexity lens:** *Just Enough* (`janmrow/just-enough`) contributes the habit of asking what added complexity buys today compared with a simpler alternative, preserving complexity that genuinely earns its cost, and stopping when further refinement no longer pays off. Martin Fowler's accounts of *YAGNI* and *Beck's Simple Design Rules* reinforce that rejecting speculative features does not mean rejecting refactoring, clarifying boundaries, or investing in near-term changeability: minimizing elements serves correctness and clear intent rather than outranking them.

## Architecture decision

| Candidate | Assessment |
|---|---|
| **A: One self-contained `SKILL.md`** | **Chosen (v0.2).** Progressive disclosure already occurs between YAML frontmatter metadata and the skill body. All high-leverage decision rules fit in one ~550-word read without reference-routing failure or extra tool calls. |
| B: Minimal router only | Requires a second file read before any engineering guidance is in context. |
| C: Small core with contextual `references/` | Used in v0.1 (`SKILL.md` + `design-decisions.md` + `evidence.md`, 1,543 words total). Rejected after review: the two short references overlapped heavily with the root file, left the root overly abstract, and were not loaded in any v0.1 pilot handoff. |
| D: Modes, scripts, and multi-skill chains | Unnecessary coordination and maintenance overhead for a general engineering judgment skill. |

Installed package:

```text
pragmatic-craftsman/
  SKILL.md
  agents/openai.yaml
```

`SKILL.md` uses standard `name` and `description` frontmatter and a self-contained Markdown body; exact file hashes and word counts are tracked in `MANIFEST.json`. `agents/openai.yaml` supplies optional OpenAI/Codex display metadata and invocation policy. All research, design rationale, and evaluation tools live outside the installed package.

## Behavioral commitments

The skill organizes judgment around six connected commitments—applied directly in work rather than recited as six response sections:

1. **Understand the outcome and context:** Identify the intended outcome (behavior, structure, learning, or testability) and scope boundaries. Separate the user's underlying need from a proposed mechanism; question unnecessary work respectfully while honoring informed requirements.
2. **Make complexity earn its place:** Compare added layers, dependencies, or abstractions against simpler alternatives. Keep or introduce structure when it improves present correctness, clarity, isolation, or changeability—even with a single current implementation—without judging by line or implementation count alone.
3. **Design around meaning:** Use domain names and coherent responsibilities. Give each business rule or security invariant one authoritative owner across entry points; do not merge unrelated concepts that merely look alike, and preserve independent enforcement at separate trust boundaries.
4. **Make complete, reviewable changes:** Cover affected consumers and safeguards. Preserve supported caller-visible contracts (defaults, signatures, outputs, side effects, and relied-upon failure behavior) when changing internals; change a supported contract only when required by the requested outcome and within authorized scope, and make that change explicit. Provide enough structure on new projects or test setups for one representative working path.
5. **Scale effort and feedback to the work:** Calibrate investment by the consequences of the change—affected contracts, trust boundaries, persistent state, reversibility, and failure cost—rather than the repository's label. Prove a thin working path early across boundaries, reduce the cost of changing consequential decisions without indefinite delay, and offer a smaller complete outcome if constraints conflict with essential safety or correctness.
6. **Establish credible evidence and stop at enough:** Choose checks that could falsify the change plus required repo gates. Ground expectations independently of generated code, check whether a plausible wrong implementation would still pass, never weaken a failing assertion to force a green run, and stop once the authorized scope and proportionate evidence are complete.

### Practical bias across everyday work

| Work | Expected influence |
|---|---|
| **Add a feature** | Reuse the project's existing mechanisms and finish one complete path (including callers and negative cases) without hypothetical extension hooks. |
| **Start a small project** | Establish enough structure for a working end-to-end result and the next likely change, avoiding premature framework ceremony. |
| **Create web test infrastructure** | Support one representative user journey with understandable setup and diagnosable failures before building an abstraction layer for imagined suites. |
| **Refactor an API** | Clarify domain responsibilities and characterize weakly tested behavior while deliberately preserving supported callers, defaults, and failure semantics. |
| **Trivial bug fix** | Make the direct fix and run the nearest check without planning narration or redundant harness setup. |
| **Consequential data/security change** | Enforce the invariant at every affected entry point and verify rejected inputs, partial failure, and recovery regardless of a "quick" or "prototype" label. |

## Activation contract

The frontmatter `description` targets everyday software creation and modification—features, project setup, test infrastructure, bug fixes, and refactoring—so users do not need to phrase their prompt as an "engineering tradeoff" before the skill applies. General explanations, summaries, translation, and mechanical formatting are excluded unless `pragmatic-craftsman` is explicitly invoked.

In v0.2, `agents/openai.yaml` sets `allow_implicit_invocation: true` so normal host matching is available alongside explicit invocation (`$pragmatic-craftsman` or `/pragmatic-craftsman`). Host matching is a convenience, not a guarantee. During controlled A/B evaluations, the `off` arm should be isolated by keeping the skill out of all project and global discovery paths rather than relying on adapter flags.

## Evaluation status and deferred work

`EVALS.md` and `evals/RESULTS.md` preserve the historical v0.1 evaluation contract and 14-session pilot conducted on the earlier three-file prototype. Those trials have not been rerun on v0.2, and no claim of empirical superiority over a baseline is made. Queued evaluation harness and fixture repairs are documented in `EVALS.md` to be completed before running future trials.
