# Research trail

Research date: 2026-10-31. Sources were opened or fetched, not merely collected from search snippets. Repository snapshots are pinned below. This is a selective design investigation, not a substitute for either book.

Authority labels: **P** = primary text/standard/vendor documentation; **E** = empirical research by its authors; **V** = vendor engineering experience; **A** = author/practitioner judgment; **R** = project-maintained example or self-reported benchmark; **S** = secondary framing. Primary publication does not make an opinion an empirical finding.

## Intellectual core: legitimate primary material

| ID | Source and access | Authority | Learning → design consequence |
|---|---|---|---|
| P1 | [Pragmatic Bookshelf book page, contents and extract links](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) | P; publisher | Establishes edition and thematic scope → frame the skill around problem solving and affordable change, rather than a technology checklist. |
| P2 | [Official tips](https://pragprog.com/tips/) | P; authorized extracts | Feedback, context-dependent quality and responsibility → short decision controls, not all 100 tips. |
| P3 | [DRY extract](https://media.pragprog.com/titles/tpp20/dry.pdf) | P; authorized PDF | Knowledge has ownership; superficial similarity is insufficient → distinguish shared rules from coincidental resemblance. |
| P4 | [Headlights extract](https://media.pragprog.com/titles/tpp20/dont-outrun-your-headlights.pdf) | P; authorized PDF | Feedback limits safe commitment → slices bounded by understanding, not a fixed line limit. |
| P5 | [Official source materials](https://media.pragprog.com/titles/tpp20/code/tpp20-code.zip) | P; publisher archive | Inspected archive structure: contracts, concurrency and testing examples are executable material → prefer runnable eval fixtures to prose-only demonstrations. No book code copied. |
| C1 | [Pearson public sample](https://ptgmedia.pearsoncmg.com/images/9780134052502/samplepages/9780134052502.pdf) | P; publisher | Contains contents and chapter 4 on attitude, learning and practice → separate learning experiments from delivery; offer viable options and own outcomes. |
| C2 | [O’Reilly book information and contents](https://www.oreilly.com/library/view/the-software-craftsman/9780134052625/) | P; licensed publisher platform | Maps chapters on working software, technical practices, learning, technical change and pragmatic craftsmanship → quality is tied to future usefulness, not status or ritual. |
| C3 | [Working Software preview](https://www.oreilly.com/library/view/the-software-craftsman/9780134052625/ch06.xhtml) | P; limited preview | Technical quality coexists with business constraints → assess lifetime and cost of failure. |
| C4 | [Technical Practices preview](https://www.oreilly.com/library/view/the-software-craftsman/9780134052625/ch07.xhtml) | P; limited preview | Practices need a value argument → no universal TDD or mandatory process stack. |
| C5 | [Pragmatic Craftsmanship preview](https://www.oreilly.com/library/view/the-software-craftsman/9780134052625/ch15.xhtml) | P; limited preview | Quality and delivery need joint consideration → small complete outcomes instead of silent corner cutting. |
| C6 | [Software Craftsmanship Manifesto](https://manifesto.softwarecraftsmanship.org/), [official English data](https://manifesto.softwarecraftsmanship.org/jsons/manifesto/en.json) | P; original statement | Delivery, sustainable value and partnership → explicit tradeoffs and maintainability; no claims that process alone delivers quality. |
| C7 | [Mancuso: Software Craftsmanship in the AI Era](https://www.codurance.com/publications/software-craftsmanship-in-the-ai-era) | A; author, published 2026-02-09, updated 2026-06-01 | Read fully. Review capacity, semantic boundaries, ownership and implementation-shaped tests → explainable slices, authoritative business concepts and independent expectations. |
| C8 | [Mancuso: Should we always use TDD to design?](https://www.codurance.com/publications/2018/05/26/should-we-always-use-tdd-to-design) | A; author | Architecture, macro/micro design and uncertainty call for different methods; delay has costs → test-first, contracts and spikes are alternatives. URL says 2018; current page displays 2020-08-26. |
| C9 | [InfoQ Q&A with Mancuso](https://www.infoq.com/articles/mancuso-software-craftsman/) | A for attributed answers; S for introduction; 2015-04-25 | Inspected author answers on feedback, technical quality and practices → outcomes matter more than process artifacts. |
| C10 | [Martin Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html) | A; practitioner | Avoiding speculative features depends on keeping code malleable; it does not reject refactoring, useful abstractions or investing in changeability → constructive structure when it serves present clarity/changeability. |
| C11 | [Martin Fowler: BeckDesignRules](https://martinfowler.com/bliki/BeckDesignRules.html) | A; practitioner | In Beck's simple-design rules, fewer elements follows passing tests, revealing intent and removing knowledge duplication → concision serves correctness and clarity rather than outranking them. |
| C12 | [PEP 8 exception handling guidance](https://peps.python.org/pep-0008/) | P; language guide | Precise exception handling is good practice when compatible with callers → preserve supported caller-visible guarantees without forbidding valid internal improvements. |

Access limit: no claim to have read paywalled chapters in full. C1 exposes the full attitude sample; C2–C5 expose contents and short chapter openings. Four Rules of Simple Design are investigated through C2/C5's chapter structure and C8's explicit use in refactoring; this prototype does not pretend the available preview establishes Mancuso's entire treatment. No unauthorized book mirror was used. The resulting rules are original adaptations, not reproduced passages.

C7 is central practitioner analysis, not controlled evidence that AI universally damages architecture. Its cited productivity and Stanford claims were not adopted as established causal results. In particular, repository context can influence generation; it is not necessarily retraining a deployed model on the repository.

## Current skill and coding-agent primary guidance

| ID | Source | Authority | Learning → design consequence |
|---|---|---|---|
| O1 | [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | P/V; model-specific vendor guidance | Remove elaborate itineraries and unnecessary instructions; routers are for multi-workflow skills → self-contained single `SKILL.md` for a cohesive judgment skill; no compulsory survey or repeated broad checks. Treat as model-specific advice to evaluate cross-vendor. |
| O2 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | P/V; 2026-01-22 | Define success before writing; capture runs and combine deterministic checks with rubrics → fixture contract first, independent oracles and paired trials. |
| O3 | [Codex skills](https://developers.openai.com/codex/skills) | P; current docs redirect to ChatGPT Learn | Metadata discovery, `.agents/skills`, explicit invocation and invocation policy → portable package plus small optional OpenAI adapter. Older eval examples use `.codex/skills`; current installation instructions follow current docs. |
| O4 | [AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md) | P; current docs redirect to ChatGPT Learn | Repository-wide constraints have a different scope from task-specific skills → respect repository gates without duplicating them in this skill. |
| O5 | [Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk) | V; vendor implementation experience | Operational knowledge belongs near the repo; deterministic mechanics can be scripts → keep generic judgment portable; put eval mechanics outside the installed skill. |
| O6 | [Codex noninteractive mode](https://developers.openai.com/codex/noninteractive) | P; CLI documentation | Traceable execution exists → document native CLI follow-up testing; do not pretend the in-session subagents validate that loader. |
| A1 | [Agent Skills specification](https://agentskills.io/specification) | P; open format | Only `SKILL.md` (`name` + `description` frontmatter) is required; metadata first and body on activation is already progressive disclosure → single self-contained `SKILL.md` without redundant `references/`. |
| A2 | [Anthropic authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | P/V | Start with a basic `SKILL.md`, assume a capable model, and add supporting files only when they earn their cost → high freedom for judgment; single-file core. |
| A3 | [anthropics/skills](https://github.com/anthropics/skills), [skill creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | R; primary vendor examples | Inspect baseline and skill-on artifacts; blind comparisons and iteration → preserve artifacts and keep graders outside agent workspaces. Do not copy its broad activation strategy. |
| A4 | [Claude Code skills](https://code.claude.com/docs/en/skills) | P | `.claude/skills` and slash invocation; host-specific controls → vendor differences documented outside core. |
| A5 | [OpenCode skills](https://opencode.ai/docs/skills/) | P; page updated 2026-10-30 | `.opencode/skills`, `.agents/skills`, on-demand skill tool; unknown metadata may be ignored → natural-language explicit invocation and no claim of a universal implicit-disable switch. |

## Existing engineering skills: inspected design references

Repository snapshots fetched during research:

- `DietrichGebert/ponytail`: `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`.
- `addyosmani/agent-skills`: `8bfcc1f9916f2eea55494d8c1fa7f4bde867dd9e`.
- `openai/openai-agents-python`: `e355d69152d4f4730dfb03b63dbce53e8d9f5d8c`.
- `trailofbits/skills`: `2be6433b39e009cd2b6fd3be1895f6b1faa5af9a`.
- `janmrow/just-enough`: `ac4816838e71c4bee9bb85d017c607c3bb882262`.

The links below track current upstream; use these commits to recover inspected versions. No source SKILL.md was copied into the prototype.

| ID | Reference | Authority | Design lesson and limit |
|---|---|---|---|
| R1 | [Ponytail core](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md) | R | A few concrete decision preferences can have more leverage than a long checklist. Borrow the design lesson, not the persona, text, session-wide persistence or shortest-diff objective. |
| R2 | [Ponytail review](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-review/SKILL.md) and [audit](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-audit/SKILL.md) | R | Connected callers and plausible failure scenarios matter beyond changed lines. Keep implementation scope narrower than an audit. |
| R3 | [Ponytail benchmark methodology](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-10-07-agentic.md) | R; self-reported | Paired repeated runs, hidden checks, mutations and explicit limitations → adopt measurement ideas. Shell disabled in its benchmark; results do not establish this skill's performance or general autonomous debugging effectiveness. |
| R4 | [Addy Osmani skill anatomy](https://github.com/addyosmani/agent-skills/blob/main/docs/skill-anatomy.md) | R | Specific and testable skill contract; optional resources. Its acknowledged pack-level shared-reference portability issue → keep this package fully self-contained. |
| R5 | [using-agent-skills](https://github.com/addyosmani/agent-skills/blob/main/skills/using-agent-skills/SKILL.md) | R | DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP makes completion explicit; use as a mental model, not six compulsory deliverables or a chain of imported skills. |
| R6 | [incremental-implementation](https://github.com/addyosmani/agent-skills/blob/main/skills/incremental-implementation/SKILL.md) | R | Complete thin paths and feedback → adopt; reject fixed line quotas, mandatory commits and generic rollback-migration assumptions. |
| R7 | [test-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md) | R | Repository-native commands and regression reproduction → adopt; reject universal test-first/full-suite sequencing and fixed test-pyramid percentages. |
| R8 | [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) | R | Code health and real structural remedies → review responsibilities and changed boundaries, not taste; no blanket file/line threshold. |
| R9 | [code-simplification](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md) | R | Understand why code exists and preserve behavior → keep; mechanical extraction or pass-through deletion can change semantics and must not be assumed safe. |
| R10 | [context-engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md) | R | Selective files and restartable evidence → targeted reads, no mandatory context dump or task documents. |
| R11 | [debugging-and-error-recovery](https://github.com/addyosmani/agent-skills/blob/main/skills/debugging-and-error-recovery/SKILL.md) | R | Narrow reproduction and root cause → fix the owning rule, not a convenient symptom. |
| R12 | [api-and-interface-design](https://github.com/addyosmani/agent-skills/blob/main/skills/api-and-interface-design/SKILL.md) | R | Consumers, validation and failure semantics deserve deliberate design → compatibility is a present obligation; no imposed naming/schema convention. |
| R13 | [OpenAI Agents SDK verification skill](https://github.com/openai/openai-agents-python/blob/main/.agents/skills/code-change-verification/SKILL.md) | R; operational vendor repo | Precise commands and start conditions are powerful when repo-specific. Generic craft skill should honor those gates, not invent universal equivalents. |
| R14 | [obra/superpowers verification](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) | R; established OSS workflow | Claims need evidence. Its requirement to rerun verification in the same message is deliberately not adopted: unchanged evidence remains usable. |
| R15 | [Trail of Bits differential review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md) | R; security practitioners | Risk and blast radius outrank patch size → preserve that distinction. Do not import mandatory audit reports, full baselines or quantitative caller counts for every edit. |
| R16 | [janmrow/just-enough](https://github.com/janmrow/just-enough/blob/ac4816838e71c4bee9bb85d017c607c3bb882262/SKILL.md) | R | Ask what complexity buys, compare against a simpler alternative, keep justified structure, and stop when further improvement no longer earns its cost → integrate into implementation judgment while keeping both skills independent. |

## Evidence about AI-assisted engineering

| ID | Source | Category | Findings/limitations → design consequence |
|---|---|---|---|
| E1 | [METR early-2025 RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) | E; controlled field study | 16 experienced maintainers, 246 tasks; AI-allowed work took 19% longer in that setting. Older tools and established repos; not a 2026 universal result → measure outcomes and human review cost, not production speed alone. |
| E2 | [METR 2026 update](https://metr.org/blog/2026-02-24-uplift-update/) | E; authors' methodological update | Newer data suffers selection/time-measurement problems; authors call effect-size evidence weak → don't extrapolate E1 or claim a current universal slowdown/speedup. |
| E3 | [Evaluating AGENTS.md, SRI/ETH](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd) | E; 2026 workshop research | Tested context files did not improve success and increased inference cost by over 20%. Different artifact/harness from an explicitly invoked skill → supports minimal-instruction hypothesis, not proof that all guidance harms. |
| E4 | [Finding bugs with Claude and property-based testing](https://www.anthropic.com/research/property-based-testing) | E/V; authors' research report | Investigates agents deriving properties and finding defects → use independent domain properties when appropriate; does not show every generated property is valid. |
| V1 | [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | V; engineering experience | Limited attention, useful abstraction level and selective retrieval → keep active instructions compact and high-contrast in a single self-contained `SKILL.md`. |
| V2 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | V; engineering experience | Incremental progress and durable state help long work → bounded slices and inspect actual final diff; no compulsory session infrastructure for small work. |
| V3 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | V; evaluation guidance, 2026-01-09 | Outcome, trace and grader are distinct; repeated trials and calibrated judgments matter → separate deterministic checks, rubric judgments and unobserved process metrics. |

Own synthesis: semantic drift, oversized patches, false confidence from generated tests and over/under-building are plausible mechanisms worth controlling. Their magnitude is workload-dependent. None of the above proves that this particular prompt improves them. The local pilot tests that claim directly, with substantial limits recorded in `evals/RESULTS.md`.
