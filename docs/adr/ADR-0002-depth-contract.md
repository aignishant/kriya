# ADR-0002 — A day is a hub plus one document per subtopic, with no clocks anywhere

- **Date:** 2026-08-24
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Related:** ADR-0001 (charter)
- **Implements:** master plan §17, Principles 16–18

## Context

The default format for a curriculum day is one long Markdown file with an "estimated hours" field at
the top. It is the obvious choice and it fails in three specific, observable ways — observed in a
sibling curriculum in this workspace before this plan was written, across 107 written days averaging
roughly 471 lines each, every one of which carried a time estimate.

1. **A subject cannot be revisited alone.** When a day teaches probes, requests, limits and QoS under
   one `##` heading, a reader who wants to re-read *only* "what does `failureThreshold` actually do"
   re-reads three other subjects to get there. On a 237-day plan, re-reading is not an edge case —
   it is the primary access pattern after week three.
2. **A thin subtopic is invisible.** With one file per day there is no artifact that distinguishes
   "this day covered six subtopics and one of them got two paragraphs" from "this day covered five
   subtopics". Nothing in the repository can tell a reviewer, or the author, that a subject was
   skimmed.
3. **The time estimate authorises the worst edit in technical writing.** A number at the top of a
   document is a standing instruction to cut the explanation when the document runs long. For an ops
   curriculum this is fatal in a specific way: the parts that get cut are always the failure modes
   and the production caveats, because they are at the bottom. Those are the parts that are the
   entire point.

Hazard 3 is worse here than in most subjects. This plan's value is concentrated in *"what breaks,
what you see first, and what you do at 3am"* — and that material is structurally last on the page.

## Options considered

| Option | Pros | Cons |
| --- | --- | --- |
| **A. One long file per day** | Simplest. No tooling. | Fixes nothing. The largest files are already the worst to read; more content makes it worse. |
| **B. Split into unnumbered topic files** | Cheap; fixes revisiting. | No contract means no enforcement. Splitting a long page into short pages without adding story, failure text and a production section is reformatting, not depth — and nothing would catch it. |
| **C. Hub + `parts/<NN>-<slug>/<section>.<sub>-<slug>.md`, a ten-section part contract, a `level` ladder, a no-clocks rule, and a script enforcing the mechanical half** | Fixes all three. Part count per day becomes a visible depth signal in the tracker. Reviewable by reading, partly automatable. Proven in a sibling curriculum. | Days take substantially longer to write. Requires tooling before any day exists. |
| **D. Option C plus a required part count per day** | Would make thinness impossible. | Turns a quality target into a quota, which produces padding. Rejected: §17.7 deliberately sets no target part count. |

## Decision

**We adopt Option C**, as master plan §17, with `scripts/depth_check.py` (`./o depth [N]`) enforcing
the mechanical half. Concretely:

1. A day is `days/day-NNN-<slug>/{LESSON.md, CHECKLIST.md, parts/<NN>-<slug>/…, lab/}`. `parts/` is
   mandatory; a day without it is not written and its phase cannot go green.
2. Every part carries ten sections in a fixed order, ending in **In production** and **Check
   yourself**. *Line by line* is the single conditional section, required exactly when the part
   holds code needing a walkthrough.
3. Principles **16** (depth over density), **17** (a day is a unit of subject, not of time) and
   **18** (assume no prior knowledge, finish at production).
4. **No time estimate may appear anywhere in a day folder.** The depth check fails the day on one.
5. Five Kriya-specific part rules on top (§17.4.1): never invent an API or a version; name the blast
   radius of any new capability; say how you would alert on any new signal; state the cost in quota
   units.
6. Day folders are zero-padded to **three** digits, because this plan runs to Day 236 and two-digit
   padding sorts Day 100 between Day 10 and Day 11 everywhere.

## Consequences

**Easier.** A reader can open one idea. A reviewer can see part counts per day in `docs/TRACKER.md`
and spot a thin day without reading it. `./o depth N` catches a missing *In production* section, a
code block nobody explained, a numbering gap, a smuggled-in clock and an unmarked billable command.
Every part is readable cold, because the standalone test requires it to name and link its
prerequisite.

**Harder.** Writing a day is substantially more work. That is the intended trade: Principle 16 says
a wall of text is depth's disguise, and the cost of the real thing is that it takes longer to write.

**Committed to.** Writing all 237 days in this shape, including the fifteen failure-lab days where a
deliberate failure is the entire subject.

## What would make us change our minds

- If `./o depth` starts passing days that read badly, the mechanical half is measuring the wrong
  thing and needs a *different* check — never a relaxed one.
- If the median day exceeds roughly twenty-five parts, sections are being used as a substitute for
  day boundaries and the day map itself needs amending, with its own ADR.
- If a `concept` part regularly has to invent a code block to satisfy the walkthrough rule, the
  conditional-section rule is mis-specified and should be widened rather than worked around.

## Cold read

*(Re-read this with a reviewer's hat on, later, and sign here.)*
