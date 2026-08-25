# ADR-0005 — Research is taught as a part of its own, never as a citation

- **Date:** 2026-08-25
- **Day:** 11 (amendment; applied retroactively to Days 0–11)
- **Phase:** 2
- **Status:** accepted
- **Related:** ADR-0002 (depth contract)
- **Implements:** master plan §17.4.2, Principles 7, 8, 16 and 18

## Context

Roughly a third of this plan's later material descends from a specific published result. The retry
ladder built on Day 7 is exponential backoff, which is a 1988 congestion-control paper. The resource
box of Day 6 and the whole of Phase 4 descend from a cluster-management paper. Phase 11's drift work,
Phase 13's retrieval work and Phase 17's agent loop each trace to a paper that is cited constantly
and read rarely.

The plan at v1.0.0 had no place to put that, which produced three observable problems.

1. **The citation had nowhere to live, so it lived nowhere.** Eleven written days cite zero papers.
   Not because the ideas have no provenance — Day 7's retry part is backoff, and Day 6's cgroup part
   is a container's resource box — but because the contract asked for ten sections and none of them
   was "where this came from", so the question was never asked.
2. **A reading list is not teaching.** The obvious cheap fix is a *Further reading* block at the
   bottom of a hub. This curriculum exists because that pattern does not work: the same argument that
   rejected one long page per day (ADR-0002) rejects a bibliography. A link is an address, not an
   explanation, and material at the bottom of a page is material that gets skimmed.
3. **The industry's misreadings are load-bearing.** The specific harm a famous paper does is done by
   the sentence it never contained: a benchmark read as a guarantee, a lab condition read as a
   default, an ablation read as a law. An operator who has only met the summary carries the
   misreading into production and cannot say which part of it was ever measured.

There is a fourth hazard specific to a curriculum written with an LLM in the loop: **citations are
the single easiest thing to fabricate**. A plausible title, a plausible year and a plausible venue
cost nothing to emit and are expensive to catch. Principle 8 already forbids inventing a flag; a
fabricated paper is the same failure with better camouflage.

## Options considered

| Option | Pros | Cons |
| --- | --- | --- |
| **A. Leave it. Cite inline where it helps.** | No work. | This is the status quo, and the status quo is eleven days and zero citations. Nothing asks the question, so nothing answers it. |
| **B. A *Further reading* block in each hub.** | Cheap, familiar. | A reading list — the exact pattern ADR-0002 rejected for days. Unenforceable, unread, and it teaches nothing about what the paper actually bounded its result to. |
| **C. An eleventh required section, *The paper behind it*, in every part.** | Keeps the paper next to the concept; one mechanism. | Forces the question into parts that have no paper (`chmod` has no paper), which invites invention — the precise failure Principle 8 exists to prevent. And a paper compressed into one section of somebody else's part is a summary, which §17.8 already names as a failure mode. |
| **D. A paper is a part: `kind: paper`, the same ten sections, plus a citation block, a runnable demo of the paper's one feature, and *What it did not claim*; every part declares `papers:` or `[]`.** | The paper gets a story, a mechanism with real numbers, a working miniature, a failure mode and a production face — the same depth as everything else. `papers: []` makes "I looked, there is none" auditable. One paper, one part, linked forever after. | More writing per day, and a demo that has to actually run. A new frontmatter key on all 190 existing parts. |

## Decision

**We adopt Option D**, as master plan §17.4.2.

1. A paper is taught in a **part document of its own**, written to the same ten-section contract as
   every other part, placed **last in the section folder whose mechanism it grounds**.
2. That part carries `kind: paper` and `paper: <slug>`, plus three extra sections in fixed
   positions: **The citation** after the one-line answer, **The demo** after *The mechanism*, and
   **What it did not claim** after the walkthrough.
3. **The demo is a small end-to-end project implementing only the paper's feature** — stdlib where
   possible, zero cost, real output pasted, and written twice (without the mechanism, then with it)
   wherever the idea allows. Build first, adopt after (Principle 4) applies to research too: the
   reader runs the idea in isolation before meeting the library that hides it.
4. **Every** part declares `papers:` — the slugs it rests on, or `[]`. The empty list is the common
   case and a real answer.
5. A paper is explained **once in the curriculum**. Later days declare the slug and link the part.
6. Citations name **title, year and identifier — never an author** (§18.4), and never from memory:
   a citation you have not opened is an invented fact (§17.4.1 rule 6).
7. `scripts/depth_check.py` enforces the mechanical half: the missing key, the undeclared paper part,
   the missing citation or identifier or read-date, the missing demo, the missing *What it did not
   claim*, those three sections out of order, `et al.`, and a hub that teaches a paper without
   naming it in §8.

## Consequences

**Easier.** A reader meets the research at the same depth as everything else, including the part of
it that never left the lab. `grep -r "papers:" days/` is the curriculum's bibliography, generated by
the same act that writes the day. A fabricated citation is now a contract violation with a name,
rather than a sentence nobody checks.

**Harder.** Days that rest on research take longer to write, because a paper part is a full part —
story, mechanism, numbers, failure, production face. Two of them on one day is two extra documents,
and §17.7's "no target part count" means that is simply what the day costs.

**Committed to.** Reading every paper this curriculum cites, on the day it is cited, and writing down
what it did not claim. Retrofitting the eleven days already written rather than grandfathering them.

## What would make us change our minds

- If a day arrives where the honest answer is more than roughly four paper parts, the day is a
  literature review and its **subject** is wrong, not this rule — the day map needs amending.
- If `papers: []` is being written without the question being asked — visible as a day whose subject
  is plainly a published result and whose parts all declare `[]` — the declaration has become
  ceremony, and the check needs to move to the day level rather than be relaxed.
- If a paper part regularly has nothing to put under *When it breaks*, the section list for a paper
  part is mis-specified and should be adjusted rather than filled with padding.
- If a paper's demo cannot be made to run in one folder with the standard library — a result that
  needs a cluster, a GPU or a proprietary dataset to show anything at all — the demo rule needs a
  named exemption for that class of paper, written down here, rather than a demo that fakes output.

## Cold read

*(Re-read this with a reviewer's hat on, later, and sign here.)*
