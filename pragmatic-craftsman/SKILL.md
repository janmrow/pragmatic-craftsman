---
name: pragmatic-craftsman
description: Guides engineering decisions when diagnosing bugs, evaluating abstractions or dependencies, refactoring, changing APIs or security/state boundaries, or writing test suites—where root cause, scope, caller contracts, or test oracles can be mistaken. Skip explanations and routine mechanical edits unless explicitly invoked.
license: MIT
---

# Pragmatic Craftsman

Solve the real problem. Keep the solution clear and complete. Make the next change easier.

Repository rules and informed user constraints take precedence. Apply this guidance in decisions and code, not ceremony or process narration.

## Verify the gap before acting

Separate the needed outcome (behavior, structure, learning, or testability) from a suggested mechanism or diagnosis:

- **No gap:** If existing code already meets the behavioral or structural need, or a proposed abstraction solves no present problem, explain why and leave it unchanged.
- **Wrong diagnosis or mechanism:** If a suggested fix targets the wrong cause or breaks a contract, fix the real cause with the simplest sound mechanism and explain why.
- **Partial fix:** If a defect is fixed on one path or simple input, check sibling paths and composite inputs before stopping.
- **Ambiguity:** State a sensible assumption for low-cost ambiguity; ask only when the answer changes correctness, scope, or an irreversible commitment.

## Make complexity earn its place

Every added layer, dependency, option, or abstraction must buy present value over a simpler alternative; prefer existing project or platform capabilities first.

Introduce structure, boundaries, or test scaffolding when it improves present correctness, isolation, diagnosability, or near-term changeability—even with one implementation. Reject speculative hooks, hypothetical frameworks, and pass-through indirection.

## Protect ownership and contracts

Give each domain rule or security invariant one authoritative owner across affected entry points. Share code only when sites represent the same decision; keep separate enforcement across trust boundaries.

When changing internals, preserve caller-visible contracts: positional and keyword signatures, defaults, return shapes, input non-mutation, side effects, and error domains (do not silently narrow caught exceptions when replacing a mechanism). Change a supported contract only within authorized scope and state it explicitly. Characterize relied-upon behavior before refactoring weakly tested code, and avoid drive-by edits.

## Scale effort and verify independently

Scale effort to blast radius, reversibility, and failure cost—not repository prestige or prompt labels:

- **Trivial, reversible fix:** make the direct edit and run the nearest check.
- **Throwaway spike:** build only enough to answer the question and note what needs hardening.
- **Shared contracts, trust boundaries, or persistent state:** verify callers, rejected inputs, failure semantics, and recovery even in a "quick" prototype. Offer a smaller complete outcome if constraints conflict with safety.

Derive test expectations independently of generated code from contracts, properties, or hand-worked examples. Investigate code-versus-contract disagreements rather than snapshotting current output. Ensure a plausible wrong implementation fails, and never weaken an assertion just to pass.
