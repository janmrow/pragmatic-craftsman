# Synthesis into agent decisions

KEEP preserves a useful decision criterion. ADAPT changes its application for an agent. CONTEXTUAL loads or applies it only for the named need. REJECT rejects the stated interpretation for this skill, not the author's entire idea. Source IDs refer to `sources.md`.

## The Pragmatic Programmer → modern agent behavior

| Principle | Classification | Applied decision, and limit |
|---|---|---|
| Care and thoughtfulness | ADAPT | Accountability becomes explainable decisions and evidence, not a persona. [P1/P2] |
| Good-enough quality | KEEP | Match effort to actual consequences; keep essential safeguards. [P1/P2] |
| Knowledge duplication | KEEP | Share one changing domain decision; resemblance alone is insufficient. [P3] |
| Orthogonality/decoupling | ADAPT | Protect change boundaries; avoid ceremonial layers. [P2] |
| Reversibility | KEEP | Reduce replacement cost; delay also has a cost. [P2/C8] |
| Tracer bullets | CONTEXTUAL | Prove a thin integrated path when integration is uncertain. [P2] |
| Learning prototypes | CONTEXTUAL | Answer a question; don't silently promote shortcuts. [P2] |
| Domain language/naming | KEEP | Make responsibility and business meaning visible. [P2/C7] |
| Contracts/assertions | CONTEXTUAL | Expose invariants; distinguish internal assumptions from untrusted input. [P2/P5] |
| Headlights/feedback | ADAPT | Validate before expanding commitments; continue authorized work. [P4] |
| Coincidental success | KEEP | Passing examples require a causal explanation of the fix. [P1/P2] |
| Refactoring | CONTEXTUAL | Remove a concrete change obstacle; preserve relevant behavior. [P2] |
| Test-to-code | ADAPT | Tests clarify intent; order alone does not establish quality. [P2/C8] |
| Property testing | CONTEXTUAL | Use independent invariants where examples underexplore input. [P2/E4] |
| Requirements/collaboration | ADAPT | Separate need from proposed solution; ask on consequential ambiguity. [P1/P2] |
| Teams/pride | ADAPT | Handoff reviewable work and material limits. No motivational ritual. [P2] |
| Every tip on every task | REJECT | A reference collection is not a useful execution policy. [P1/O1] |

## The Software Craftsman → modern agent behavior

| Principle | Classification | Applied decision, and limit |
|---|---|---|
| Professional attitude | ADAPT | Own the outcome; explain viable alternatives when constraints conflict. [C1/C9] |
| Working software beyond a demo | KEEP | Include future change costs appropriate to lifetime. [C3/C6] |
| Debt and legacy | ADAPT | Improve the relevant seam; don't moralize or rewrite everything. [C2/C3/C8] |
| Technical practices | KEEP | Practices earn their cost through feedback and risk reduction. [C4/C8] |
| Pragmatic craftsmanship | KEEP | A complete small result can satisfy delivery and quality together. [C5/C8] |
| Katas and deliberate practice | CONTEXTUAL | In a learning task, the technique may be the goal. [C1] |
| Pet projects/open source | CONTEXTUAL | Respect the actual experiment or maintainer contract; no assumed enterprise bar. [C1] |
| Pairing/learning culture | ADAPT | Use focused discussion or fresh review when useful, not mandatory agents. [C1/C2] |
| Driving technical change | ADAPT | Demonstrate a local benefit; avoid unsolicited architecture campaigns. [C2/C9] |
| Four Rules of Simple Design | ADAPT | Behavioral confidence, intent, knowledge ownership and fewer unnecessary mechanisms; concision serves clarity and correctness rather than outranking them. [C2/C8/C11] |
| Justified complexity / YAGNI | KEEP | Ask what complexity buys over a simpler alternative; keep structure that improves present clarity, isolation or changeability; stop when further refinement no longer pays off. [C10/R16] |
| Reviewability at AI speed | KEEP | Bound patch growth by what can be explained and checked. [C7] |
| Semantic boundaries/drift | KEEP | Preserve conceptual ownership across paths; question copied bad patterns. [C7] |
| Human code ownership | ADAPT | Supply enough rationale and evidence for maintainers to own the result. [C7] |
| Tests after implementation | ADAPT | The danger is a shared wrong assumption; require an independent oracle. Chronology is not the sole criterion. [C7/C8] |
| AI as design partner | KEEP | Explore a boundary or counterexample before committing to a design. [C7/C8] |
| Universal TDD/emergent architecture | REJECT | Strategic contracts and feasibility work may precede code or tests. [C8] |
| Career hierarchy/elitism | REJECT | Human career metaphors add no operational value here. [C1/C2] |

## Modern LLM constraints → skill behavior

| Constraint or hypothesis | Classification | Applied control | Evidence category |
|---|---|---|---|
| Generation can outpace review | ADAPT | Coherent slices; inspect final causal diff | Practitioner analysis [C7], not a measured universal law |
| Local patterns influence generation | ADAPT | Read a relevant example, preserve intent, challenge a known defect | Practitioner/vendor experience [C7/V1] |
| Selective context is valuable | KEEP | Self-contained single `SKILL.md` (metadata first, body on activation; no overlapping `references/`) | Specification & vendor guidance [A1/A2/O1/V1]; related context-file experiment [E3] |
| Tests/builds provide executable feedback | KEEP | Use real repo commands and relevant boundaries | Vendor operational practice [O2/R13] |
| Generated code/tests can share mistakes | ADAPT | Hand-derived/contract expectations and targeted counterexamples | Practitioner warning [C7]; own control design |
| Long autonomous work can drift | ADAPT | Reconcile slice and final diff with outcome; preserve state when needed | Vendor experience [V2] |
| Fresh review may catch other defects | CONTEXTUAL | Raw task, contract and diff for consequential uncertainty | Evaluation practice [A3/V3]; benefit here unproven |
| Vague goals invite too much/too little code | ADAPT | Concrete success example and consequential-ambiguity rule | Practitioner experience; own synthesis |
| Models differ and improve | KEEP | Explicit paired tests, model/version capture; remove unhelpful guidance | [O1/E1/E2] |
| More instructions guarantee better work | REJECT | Test marginal value against a capable baseline | [E3/O1] |

## Decisions where slogans fail

These are the prototype's own decision rules, informed by the sources above:

- **Reuse versus independence:** consolidate a domain rule when it has one owner and reason to change. Keep distinct concepts independent. Multiple trust boundaries may need repeated enforcement.
- **Minimal patch versus complete safety:** make the invariant explicit at every affected entry point; a larger patch is justified when the smaller one leaves a real failure open.
- **YAGNI versus compatibility:** supported downstream consumers are a present obligation even when invisible in the checkout. Speculative extension points are not.
- **Reversibility versus architecture avoidance:** decide what the next outcome needs; make an expensive decision replaceable where feasible. Waiting indefinitely is not reversible design.
- **Small slices versus throughput:** use slices at feedback and reasoning boundaries. Don't force arbitrary micro-commits, test runs after each line, or broken intermediate submissions.
- **Refactoring versus scope:** remove a concrete obstacle to the requested outcome. Report serious unrelated defects without using them to justify a renovation.
- **Test-first versus feasibility:** use examples to discover behavior; use a spike or a contract sketch to discover whether a design is viable. Post-code tests can be strong if independently grounded.
- **Quality versus ceremony:** expected lifetime and cost of failure change the evidence bar. A short-lived program with destructive effects still needs strong safeguards.

## Why this is not a generic mega-skill

The two books contribute the central tension: useful progress now, affordable change later. The distinctive mechanisms are knowledge ownership rather than textual DRY; feedback-limited commitment; reduced cost of reversal; accountable options; context-dependent technical quality; and semantic coherence under rapid generation. The agent-specific adaptation protects understanding and test intent without imposing a particular stack or methodology.

Intentionally omitted: tool mastery curricula, career advice, recruiting, team transformation programs, mandatory pair programming, universal design patterns, fixed coverage targets, always-on security audits and a complete release process. Those may be valuable elsewhere. None earns an unconditional place in this skill.
