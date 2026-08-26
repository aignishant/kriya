# ADR-0006 — The curriculum teaches no papers

- **Date:** 2026-08-26
- **Day:** 11 (amendment; applied retroactively to Days 0–11)
- **Phase:** 2
- **Status:** accepted
- **Supersedes:** ADR-0005 (research is taught as a part of its own)
- **Implements:** master plan §17, Principles 8, 16 and 18

## Context

ADR-0005 added a `papers/` folder to the day format. A paper became a document of its own, written
to the ordinary ten-section contract plus three extra sections, and every part in the curriculum
grew a `papers:` frontmatter key so that the question *"where did this come from?"* was asked on
every subtopic.

One paper was written under that contract, on Day 7. Reading it back against the rest of the
curriculum showed three things.

1. **It is the wrong unit of teaching for this reader.** This is a production-operations
   curriculum. What the reader needs from exponential backoff is the retry ladder, the jitter, the
   ceiling and the failure it prevents. All of that already lives in the part that builds it. The
   paper document restates the same mechanism a second time, in a second place, with a second
   story, and the reader now has two documents to hold for one idea. That is exactly the density
   that Principle 16 splits parts to avoid, arriving from the other direction.
2. **The extra sections pull the writing away from plain language.** *The citation*, *the demo* and
   *what it did not claim* are academic moves. They import venue names, identifiers, ablations and
   "the workload it was measured on" into a document that is supposed to open where somebody who
   has never met the idea can stand (Principle 18). Every one of those sentences is a sentence not
   spent on the operator's version of the idea.
3. **The hazard ADR-0005 itself named never went away.** That ADR listed fabrication as its fourth
   hazard, and answered it with a rule: papers are written on request, never generated. So the
   contract's research half was opt-in, unexercised on all but one day, and still carried
   curriculum-wide machinery — a frontmatter key on every part, a slug index across every day, and
   nine separate checks in `scripts/depth_check.py`. A feature used once should not cost that.

## Options considered

| Option | Pros | Cons |
| --- | --- | --- |
| **A. Keep ADR-0005 as written.** | No work. The provenance question stays askable. | Keeps a second explanation of every idea that has one, keeps the academic register, and keeps nine checks and a frontmatter key alive for a feature used on one day out of twelve. |
| **B. Keep `papers:` as a frontmatter key, drop the paper document.** | Cheap. Provenance stays recorded. | A slug with nothing behind it is a citation with no explanation — the reading list ADR-0005 correctly rejected, now with worse ergonomics. |
| **C. Remove papers from the contract entirely. Where research genuinely changed how an operator behaves, the ordinary part teaches that consequence in plain language, with no citation.** | One explanation per idea, in one place, in the register the rest of the curriculum uses. Removes the largest fabrication surface in the plan. Removes a frontmatter key, a folder, and nine checks. | Provenance is no longer recorded anywhere. Somebody who wants the original source has to go and find it. |

## Decision

**We adopt Option C.**

1. **There is no `papers/` folder.** It is removed from §17.2's day format, and Day 7's
   `papers/congestion-avoidance-and-control.md` is deleted. What that document taught about the
   retry ladder already lives in Day 7's part 5.2.
2. **There is no `papers:` frontmatter key.** It is removed from §17.4's frontmatter row and from
   every part written so far.
3. **`kind: paper` and `paper:` are not part of this format.**
4. **No part cites a paper.** Where an idea came from published research and the provenance changes
   how an operator behaves, the part says so in ordinary words — *"this is the retry pattern the
   internet settled on after congestion collapse in the 1980s"* — with no title, no year, no
   identifier and no link. Where it does not change how an operator behaves, it is not mentioned.
5. **§17.4.1 returns to five additional rules.** Rule 6, *never invent a citation*, goes with the
   feature it guarded. Rules 1 and 2 — never invent an API or a version — are unchanged and still
   cover every fact a part states.
6. **`scripts/depth_check.py` drops all paper checks** and gains one: a part carrying a `papers:`,
   `paper:` or `kind: paper` key fails, so the removed format cannot come back by accident.

## Consequences

- The plan loses its only mechanism for recording provenance. That is accepted. This curriculum
  teaches how to operate systems, not where the ideas were first published, and Principle 18 sets
  its finish line at production rather than at the literature.
- Day 7 loses a document and gains nothing, because its retry part already carried the mechanism.
  Its hub part count and §8 change accordingly.
- Every part written so far loses one frontmatter line.
- ADR-0005 is superseded, not deleted. It records why the paper part looked right, which is worth
  keeping — the reasoning was sound and the outcome was still wrong.
