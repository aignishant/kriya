# ADR-0001 — Kriya exists as a distinct curriculum: ops for AI systems

- **Date:** 2026-08-24
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Related:** ADR-0003 (zero cost) · ADR-0004 (fundamentals before AI)

## Context

The workspace already contains curricula for building things: `setu` (data science through
generative AI), `sutra` and `mandala` (agentic AI engineering with specific frameworks), `krama`
(algorithms and system design), `kosha` (git and GitHub). All of them end at a working system on a
laptop.

None of them answer the question that decides whether that system is worth anything to an employer:
**what happens after it works?** Who is paged when it stops? How does a new version get out and how
does it come back? What does one prediction cost? What happens when the model is fine and the
feature pipeline is not? Who is allowed to make the agent do something?

The learner's stated goal is to **work on production systems**, starting from no operations
background at all. Five terms name the pieces of that goal — MLOps, LLMOps, AIOps, AgenticOps,
MCPOps — and the industry uses all five inconsistently, which makes self-study by search
unusually unproductive.

Three specific hazards in the existing material:

| Hazard | Why it matters here |
| --- | --- |
| The five "ops" terms are marketing categories as often as they are disciplines | A curriculum that follows the marketing teaches vocabulary, not practice. |
| Most MLOps material assumes ordinary ops as a prerequisite and never says so | A beginner reaches "deploy the model to Kubernetes" on page four with no idea what a pod is. |
| Almost all of it assumes a cloud account | A learner with no budget either stops or, worse, learns to click buttons in a console. |

## Options considered

| Option | Pros | Cons |
| --- | --- | --- |
| **A. Add an "ops" phase to `setu` or `sutra`** | No new repository; concepts land where the models are built. | Ops is not a phase, it is a profession. Ten days bolted onto a modelling course reproduces exactly the "deploy it to Kubernetes" hand-wave this plan exists to fix. |
| **B. Five separate small curricula, one per ops term** | Matches how the industry names things; each could be short. | The terms overlap heavily and depend on each other in a strict order. Five separate plans would duplicate observability five times and teach the dependencies nowhere. |
| **C. One curriculum, one operated system, five threads in dependency order, with the ordinary-ops foundation built in** | The dependencies are visible; every concept lands on a system that actually exists; the foundation is not assumed. | Long — 237 days. Requires building and operating a real service, not reading about one. |
| **D. Option C, but starting at MLOps and back-filling infrastructure as needed** | Faster to something that looks like the goal. | "As needed" means "never properly". Debugging a serving latency problem requires the platform knowledge before the incident, not during it. Rejected in ADR-0004. |

## Decision

**We adopt Option C.** Kriya is a distinct curriculum of 237 days across 24 phases, closing 279
concept IDs in 10 threads, teaching MLOps, LLMOps, AIOps, AgenticOps and MCPOps **in that order**,
on top of an explicit 84-day foundation of Linux, delivery, containers, Kubernetes, infrastructure
as code, observability and SRE practice.

Everything is built against one system, `pulse` — a deliberately boring AI service with a
deliberately complete production surface. The service is small so that nothing about the operations
is hidden behind interesting modelling.

## Consequences

**Easier.** Every concept has somewhere to land. A drift detector monitors a real model; an alert
has a real runbook; an agent operates a real cluster. The dependency order is visible in the day
numbers rather than assumed.

**Harder.** 237 days is a year of evenings. The plan is explicitly not survivable by skimming, and
Principle 17 removes the pressure valve of "just do it faster" on purpose.

**Committed to.** One product across the whole plan. Every day changes `pulse` or the platform
around it. If a concept cannot be landed on `pulse`, it does not get a day (Principle 5).

**Not changed.** The sibling curricula. Kriya duplicates none of them and requires none of them; a
concept that overlaps is taught from zero in Kriya's own words, because Principle 18 does not admit
"see the other course".

## What would make us change our minds

- If, by Phase 9, `pulse` turns out to be too small to carry a real MLOps lesson — if a day has to
  invent a hypothetical rather than change the service — the product is wrong and needs an ADR, not
  a workaround.
- If the five threads turn out to be separable in practice — if AgenticOps genuinely does not need
  the observability thread — then the single-plan decision was wrong and the threads should split.
- If more than roughly a fifth of days end up parked (🅿️) for lack of hardware or budget, the plan
  is teaching a tour rather than a practice, and the scope needs cutting rather than parking.

## Cold read

*(Re-read this with a reviewer's hat on, later, and sign here.)*
