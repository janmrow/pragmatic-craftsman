# pragmatic-craftsman

[**`pragmatic-craftsman/SKILL.md`**](pragmatic-craftsman/SKILL.md) is a compact, self-contained Agent Skill (~415 body words) that acts as a **decision-quality layer for coding agents**.

Rather than teaching a capable model how to write code, it intervenes when an agent faces non-obvious engineering decisions or predictable judgment traps—grounded in David Thomas and Andrew Hunt's **The Pragmatic Programmer**, Sandro Mancuso's **The Software Craftsman**, and **Just Enough**:

> **Solve the real problem. Keep the solution clear and complete. Make the next change easier.**

Its rules target four high-leverage failure modes:

- **Counter action and sycophancy bias:** separate the needed outcome from a user-suggested mechanism or diagnosis; leave working code unchanged when a reported bug is already resolved or a proposed abstraction solves no present problem, fix the real root cause when a suggested mechanism is wrong, and check sibling paths or composite inputs when an issue is only partially fixed.
- **Make complexity earn its place today:** require present value for every added layer, dependency, or option while introducing boundaries or test scaffolding when they improve present correctness, isolation, or near-term changeability.
- **Protect semantic ownership and caller contracts:** keep one authoritative owner for each domain rule or security invariant across affected entry points, maintain separate enforcement across trust boundaries, and preserve caller-visible signatures, defaults, return shapes, and error domains (without silently narrowing caught exceptions) when changing internals.
- **Scale effort to consequences and verify independently:** keep a trivial, reversible fix direct and fast even in a production repo, while verifying rejected inputs, failure semantics, and recovery on shared contracts or state even in a "quick" prototype; ground test expectations in contracts or hand-worked examples rather than mirroring generated code.

## Illustrative example

Suppose a ticket says:

> *"Users in tenant B can read tenant A's documents via `get_document` in `service.py`. Fix this tenant isolation bug."*

Instead of patching only the reported line or inventing an authorization framework, `pragmatic-craftsman` biases the agent to:

1. Inspect sibling entry points in `service.py` (such as `delete_document`) to see whether they share the same tenant-ownership invariant.
2. Enforce the invariant in one place while preserving public signatures and the documented `NotFound` error policy.
3. Verify both authorized and unauthorized read/delete behavior with expectations derived from the contract.

## Install

Clone this repository and copy [`pragmatic-craftsman/`](pragmatic-craftsman) into one skill directory used by your coding agent:

```bash
git clone https://github.com/janmrow/pragmatic-craftsman.git
cd pragmatic-craftsman

# Run from this checkout; set repo to your target project path:
repo=/absolute/path/to/your/repository
mkdir -p "$repo/.agents/skills"
test ! -e "$repo/.agents/skills/pragmatic-craftsman" &&
  cp -R pragmatic-craftsman "$repo/.agents/skills/pragmatic-craftsman"
```

| Host | Project skill path | Global skill path | Explicit invocation |
|---|---|---|---|
| **Codex CLI** | `.agents/skills/pragmatic-craftsman/` | `~/.agents/skills/pragmatic-craftsman/` | `$pragmatic-craftsman` |
| **Claude Code** | `.claude/skills/pragmatic-craftsman/` | `~/.claude/skills/pragmatic-craftsman/` | `/pragmatic-craftsman` |
| **OpenCode** | `.opencode/skills/pragmatic-craftsman/` (or `.agents/skills/...`) | `~/.config/opencode/skills/pragmatic-craftsman/` (or `~/.agents/skills/...`) | `@pragmatic-craftsman` |
| **Gemini CLI** | `.gemini/skills/pragmatic-craftsman/` (or `.agents/skills/...`) | `~/.gemini/skills/pragmatic-craftsman/` (or `~/.agents/skills/...`) | Ask to activate `pragmatic-craftsman` (or manage via `/skills`) |

Install into one location per host rather than duplicate paths. To uninstall, remove the copied `pragmatic-craftsman` folder.

## Use

Invoke the skill explicitly on a task, or let a supporting host match it when diagnosing bugs, evaluating abstractions or dependencies, refactoring, changing APIs or security/state boundaries, or writing test suites (routine mechanical edits and explanations are skipped unless explicitly invoked):

```text
Use $pragmatic-craftsman to add an include_archived filter to list_documents while preserving existing callers.
```

## Status and deeper material

Ready for experimentation and real-project evaluation; effectiveness over a strong unassisted baseline has not yet been empirically established. See [`EVALS.md`](EVALS.md) for the 15-case evaluation harness and multi-arm protocol, and [`evals/RESULTS.md`](evals/RESULTS.md) for the archived v0.1 pilot record.

- **Installed skill:** [`pragmatic-craftsman/SKILL.md`](pragmatic-craftsman/SKILL.md) and [`pragmatic-craftsman/agents/openai.yaml`](pragmatic-craftsman/agents/openai.yaml)
- **Design rationale & architecture:** [`DESIGN.md`](DESIGN.md)
- **Research & source mapping:** [`research/sources.md`](research/sources.md), [`research/synthesis.md`](research/synthesis.md), [`research/critique.md`](research/critique.md)
- **Evaluation protocol, harness, & archives:** [`EVALS.md`](EVALS.md), [`evals/RESULTS.md`](evals/RESULTS.md), [`MANIFEST.json`](MANIFEST.json)
- **License:** MIT ([`LICENSE`](LICENSE))
