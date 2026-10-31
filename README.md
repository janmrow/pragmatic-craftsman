# pragmatic-craftsman

[**`pragmatic-craftsman/SKILL.md`**](pragmatic-craftsman/SKILL.md) is a self-contained Agent Skill that guides everyday software implementation and change: adding features, starting projects, setting up test infrastructure, fixing bugs, and refactoring.

Grounded in David Thomas and Andrew Hunt's **The Pragmatic Programmer** and Sandro Mancuso's **The Software Craftsman**, and informed by **Just Enough**, it is organized around one credo:

> **Solve the real problem. Keep the solution clear and complete. Make the next change easier.**

Its goal is practical engineering judgment that shows up in decisions and code rather than process narration:

- **Question unnecessary complexity, build needed structure:** reuse existing project capabilities where they fit, add boundaries or test setup when they improve present clarity or isolation, and skip speculative frameworks.
- **Protect meaning and contracts:** keep one authoritative owner for each domain rule across entry points, and preserve caller-visible defaults, signatures, and failure behavior when changing internals.
- **Match effort to consequences:** keep a trivial, reversible fix direct and fast even in a production codebase, while giving shared contracts, trust boundaries, and persistent data proportionate verification even in a "quick" prototype.
- **Stop at enough with credible evidence:** ground test expectations in contracts or hand-worked examples rather than mirroring generated code, and never weaken a failing assertion just to make a check pass.

## Illustrative example

Suppose you ask an agent:

> *"Users in tenant B can read tenant A's documents in `get_document`. Fix this access bug and add a regression test."*

Instead of patching only the reported line or inventing an authorization framework, `pragmatic-craftsman` biases the agent to:

1. Check sibling entry points in the module (such as `delete_document`) to see whether they share the same tenant-ownership rule.
2. Enforce the invariant in one place while preserving the existing public signature and not-found error policy.
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
| **OpenCode** | `.opencode/skills/pragmatic-craftsman/` | `~/.config/opencode/skills/pragmatic-craftsman/` | Ask to load the `pragmatic-craftsman` skill |

Install into one location per host rather than duplicate paths. To uninstall, remove the copied `pragmatic-craftsman` folder.

## Use

Invoke the skill explicitly on a task, or let a supporting host match it from its description during coding work (implicit matching depends on the host and is not guaranteed):

```text
Use $pragmatic-craftsman to add an include_archived filter to list_documents while preserving existing callers.
```

## Status and deeper material

This skill is ready for daily project use, though its effectiveness over a strong unassisted baseline has not been empirically established. The archived v0.1 pilot ([`evals/RESULTS.md`](evals/RESULTS.md)) evaluated an earlier three-file prototype; queued repairs to the local evaluation harness are tracked in [`EVALS.md`](EVALS.md) before running new trials.

- **Installed skill:** [`pragmatic-craftsman/SKILL.md`](pragmatic-craftsman/SKILL.md) and [`pragmatic-craftsman/agents/openai.yaml`](pragmatic-craftsman/agents/openai.yaml)
- **Design rationale & architecture:** [`DESIGN.md`](DESIGN.md)
- **Research & source mapping:** [`research/sources.md`](research/sources.md), [`research/synthesis.md`](research/synthesis.md), [`research/critique.md`](research/critique.md)
- **Evaluation protocol, harness, & v0.1 archive:** [`EVALS.md`](EVALS.md), [`evals/RESULTS.md`](evals/RESULTS.md), [`MANIFEST.json`](MANIFEST.json)
- **License:** MIT ([`LICENSE`](LICENSE))
