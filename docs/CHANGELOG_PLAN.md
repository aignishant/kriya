# 📓 Plan Changelog — Project Kriya

Principle 14: *if reality changes, the plan is amended first.* Every amendment lands here **before**
any day or any code changes. **Append-only. Newest last.**

An amendment is required when any of these move:

- a tool this plan depends on ships a breaking change;
- a free tier disappears, shrinks, or starts asking for a card;
- a specification revision changes (MCP, OpenTelemetry semantic conventions);
- a day turns out to be in the wrong place, or to carry the wrong IDs;
- the depth contract itself needs changing.

**Never silently patch a day.** Amend here, add an ADR if the change is structural, then edit.

---

## v1.0.0 — 2026-08-24 — the plan

The initial plan: 237 days (Day 0 + Days 1–236), 24 phases, 279 concept IDs across 10 curricula,
one operated service (`pulse`), a zero-cost local-first stack, and the §17 depth contract with
`scripts/depth_check.py` enforcing its mechanical half.

Established at creation:

- **Principles 1–18**, including 16 (depth over density), 17 (a day is a unit of subject, not of
  time) and 18 (assume no prior knowledge, finish at production).
- **The depth contract** (§17): a day is a hub plus one document per subtopic, each part carrying
  ten required sections in a fixed order, ending in *In production* and *Check yourself*.
- **Three-digit day folders** (`days/day-NNN-<slug>/`), because 237 days sorted with two-digit
  padding put Day 100 between Day 10 and Day 11.
- **No version numbers in the plan** (§5). Everything is looked up live on the day it is used and
  recorded in `docs/PACKAGES.md`. A version written into a plan that runs for months is a lie with
  a delay fuse.
- **Zero cost, absolutely** (Addendum 01), enforced mechanically: `./o depth` fails a day that tells
  the reader to run a billable cloud command without marking it 🅿️ parked.
- **Fundamentals first** (ADR-0004): the first model is trained on Day 97 and the first LLM call is
  made on Day 125.

Supporting decisions: ADR-0001 (charter), ADR-0002 (depth contract), ADR-0003 (zero cost and
local-first), ADR-0004 (fundamentals before AI).

---

## 2026-08-24 — Addendum 02 amended: the reference machine is 11.7 GB / 4 cores, not 16 GB

**Trigger.** Day 0's first act is measuring the machine (Addendum 02 §3). The measurement came back
**11.7 GiB of RAM and 4 logical CPUs**, against an addendum written assuming a 16 GB laptop and
"roughly 12 GB to spend". Principle 14 says the plan is amended before the day is written, so it
was — this row was appended before a line of Day 0 existed.

**Amendment.**

- Addendum 02 gains **§3.1, the reference machine**: the observed numbers, dated, with the working
  budget restated as **~7.5 GB** rather than ~12 GB.
- §4's "legal combinations on a 16 GB machine" is replaced by a table calibrated to that budget.
  `core` + `cluster` + `obs` still fits on memory; `core` + `cluster` + `obs` + `llm` is now
  explicitly listed as the combination that swaps.
- **Four cores is named as the tighter constraint**, with three rules that follow from CPU
  contention rather than memory: do not benchmark while the observability stack is starting, stop
  the cluster before Day 126's local model, and start/stop one profile per concern every day.
- §3's RAM command changed from `wmic computersystem get totalphysicalmemory` to the PowerShell
  `Get-CimInstance` form. `wmic` is deprecated and absent on current Windows 11 builds, where it
  returns nothing instead of failing — a silent wrong answer, which is worse than an error.

**Not changed.** No day, no phase, no ID, no gate, no profile *content*. This is a calibration of
the resource envelope, not a change to the curriculum.

---

## v1.1.0 — 2026-08-25 — research is taught, not cited: the paper part

**Trigger.** A large share of what this curriculum teaches is not folklore — it is a published
result that a community argued about, measured, and eventually shipped as a default in a config
file. Exponential backoff, tail latency, the container's resource box, technical debt in
machine-learning systems, retrieval augmentation, the agent loop: every one of them was a paper
before it was a flag. The plan as written had nowhere to put that. A day could name a paper in
passing or not at all, and neither was checkable.

The instruction that produced this amendment was explicit on the shape: *a paper should be
explained like a day's part* — not a footnote, not a reading list at the bottom of a hub, but a
document of its own held to the same standard as every other document.

**Amendment.**

- **§17.4.2 is new — *The paper part*.** When an idea comes from research, the research is taught in
  a part of its own, written to the same ten-section contract as every other part: its own story,
  its own mechanism with the numbers the paper actually reported, its own failure mode, its own
  production face, its own check. **If the paper is worth citing it is worth a part; if it is not
  worth a part, it is not cited.**
- **Three extra sections, only on a paper part.** *The citation* (title verbatim, year, venue or
  arXiv identifier, a link that is free to read, and the date it was read) immediately after the
  one-line answer; ***The demo*** immediately after *The mechanism*; and ***What it did not claim***
  after the walkthrough. The last is the one that earns the part: most of the damage a famous paper
  does is done by the sentence it never contained.
- **The demo is a small end-to-end project that implements only the paper's feature** — the fewest
  files that can run it, the command, and the real output pasted underneath, typed into the day's
  gitignored `lab/<paper-slug>/`. Written twice where the idea allows: once without the paper's
  mechanism and once with it, so the reader watches the result fail to happen before it happens.
  Reading a paper and running its one idea in isolation are different kinds of knowing, and this
  curriculum has never accepted the first as a substitute for the second (Principle 4).
- **Every part now declares `papers:`** in its frontmatter — the slugs of the papers its idea rests
  on, or `[]`. `[]` is the common case and a real answer, exactly like `0` in a cost budget: there
  is no research behind `chmod`, and inventing one to fill a field would break Principle 8 in the
  most embarrassing way available. The field exists so the question is asked on every part and the
  answer is auditable.
- **A paper is explained once in the whole curriculum.** Its slug is its identity; a later day that
  rests on it declares the slug and links the part. Day 190 does not re-explain a paper Day 125 has
  already taught, any more than it re-explains a process.
- **§17.4.1 gains rule 6 — never invent a citation.** A paper is a fact like a version or a flag
  (Principles 7 and 8): opened, or `TODO`'d with the exact lookup URL. Never from memory.
- **Cited by title, never by author name.** §18.4 already forbade naming people; this states how a
  citation obeys it, and `./o depth` now rejects `et al.`. Citing a specification by its revision
  date was already the precedent.
- **The hub's §8** now names every paper the day teaches, with its identifier and the date read.
  §17.7 gains a split rule, §17.8 gains two failure modes (*a citation instead of an explanation*,
  *the claim the paper never made*), and §17.9 gains six mechanical checks.

**Days 0–11 were retrofitted** under the same amendment rather than being left on the old contract:
`papers: []` was recorded on every existing part, and the parts whose mechanism genuinely rests on
published research gained the paper part that grounds them.

**Not changed.** No day, no phase, no ID, no gate, no principle. The ten sections of an ordinary
part are untouched and in the same order. This adds a kind of part; it relaxes nothing.

**Supporting decision:** ADR-0005.

---
