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

## v1.1.0 — 2026-08-25 — research is taught, not cited: the `papers/` folder

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

- **§17.4.2 is new — *The `papers/` folder*.** When an idea comes from research, the research is
  taught in a document of its own — `days/day-NNN-<slug>/papers/<paper-slug>.md`, a sibling of `parts/`
  — written to the same ten-section contract as every other part: its own story,
  its own mechanism with the numbers the paper actually reported, its own failure mode, its own
  production face, its own check. **If the paper is worth citing it is worth a part; if it is not
  worth a part, it is not cited.**
- **Three extra sections, only on a paper document.** *The citation* (title verbatim, year, venue or
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
published research gained the `papers/` document that grounds them.

**Not changed.** No day, no phase, no ID, no gate, no principle. The ten sections of an ordinary
part are untouched and in the same order. This adds a kind of part; it relaxes nothing.

**Supporting decision:** ADR-0005.

---

## 2026-08-26 — papers are opt-in: a day generator never writes one

**Trigger.** v1.1.0 gave research a home and, in the same breath, told the day generator to go and
find it. Reviewing the first paper document made the hazard in that second half plain: a generator
asked *"where did this mechanism come from?"* on every part of every day will eventually answer with
a paper that does not exist. A fabricated citation is more convincing than a fabricated flag and far
harder to catch, and Principle 8 does not bend for footnotes.

**Amendment.**

- **§17.4.2 gains an opening rule: a paper document is written on request, never by default.**
  `/day-kriya N` creates no `papers/` folder and writes no paper document; **every part of a
  generated day declares `papers: []`**. If a day's mechanism plainly rests on published work, the
  generator says so at the end and stops there.
- **The `day-kriya` skill loses its research steps** — the "find the papers, and open them" lookup,
  the "every paper gets a document" split rule, and the paper-document shape. What remains is the
  prohibition: never invent a citation, never name a paper inside a part.
- **The `review-day` skill stops treating `papers: []` as a finding.** It is the expected state of a
  generated day. The paper checks now run only when a day has a `papers/` folder.

**Not changed.** Everything §17.4.2 says about *how* a paper is written when one is written: the
citation with its read-date, the demo, *what it did not claim*, one document per paper, cited by
title and never by author. `scripts/depth_check.py` is untouched — it already enforced that contract
only where a paper actually exists. Day 7's `papers/congestion-avoidance-and-control.md` stands as
the worked example, and the `papers:` key stays on every part.

**Why keep the contract at all.** Because the standard is the useful half. When research *is* written
up here, it is held to it; what is removed is the instruction to go hunting for research on every
day, which is where the invented citation would have come from.

---

---

## v1.2.0 — 2026-08-26 — papers are removed from the contract, and the day format loses a folder

**What moved.** Not the ecosystem this time, but a reading of the material. The first eleven days
were read back for tone, and two problems were found in the same pass.

**1. The `papers/` folder is removed entirely.** [ADR-0006](adr/ADR-0006-no-papers.md) supersedes
ADR-0005. One paper document was written, on Day 7, and reading it against the part it grounded
showed that it taught the same mechanism a second time, in a second place, in an academic register
the rest of the curriculum does not use. A feature exercised once should not cost a frontmatter key
on every part, a slug index across every day, and nine checks in the depth script.

Removed from the plan:

- **§17.2** — the `papers/` entry in the day folder tree, and the paragraph explaining when it is
  present.
- **§17.4** — the `papers` key in the frontmatter row, and the `kind: paper` / `paper:` clause.
- **§17.4.1** — rule 6, *never invent a citation*. The section is back to five rules, which is what
  its heading always said. Rules 1 and 2 already forbid inventing an API or a version, and they
  cover every fact a part states.
- **§17.4.2** — the whole subsection.
- **§17.5** — the clause in hub §8 requiring every paper to be named.
- **§17.7** — the `any day citing research` row, and the paragraph forbidding a paper from being
  squeezed into a part.
- **§17.8** — *a citation instead of an explanation* and *the claim the paper never made*.
- **§17.9** — the nine paper checks.
- **§18.4** — the paper-citation clause in rule 12. *No invented facts* is unchanged and still
  covers versions, flags, field names, quotas, API signatures and spec revisions.

Deleted from the days: `days/day-007-networking-for-operators/papers/`. What that document taught
about the retry ladder was already in that day's part 5.2, which is where it stays.

`scripts/depth_check.py` drops every paper check and gains one in their place: a part carrying a
`papers:`, `paper:` or `kind: paper` key now **fails**, so the removed format cannot return by
accident in a later day.

**Where research still shows up.** In ordinary words, inside the ordinary part, when and only when
the provenance changes how an operator behaves — *"this is the retry pattern the internet settled
on after congestion collapse in the 1980s"*. No title, no year, no identifier, no link, no author.
Where it does not change behaviour, it is not mentioned at all.

**2. The house style gains three rules on language** (§18.1, rules 6–8; everything after them is renumbered), because the first eleven
days drifted away from the register Principle 18 asks for:

- **Complete, punctuated sentences.** The clipped fragment and the em-dash used as a general-purpose
  joint read as speed on the page and as fog to somebody meeting the idea for the first time. Commas
  and full stops do the work.
- **The plainest word that is still exact.** Where a shorter everyday word means the same thing, it
  wins.
- **Stories anyone can stand inside.** A scene has to be one the reader has plausibly lived: a
  kitchen, a queue, a phone, a shared flat, a school. Not a trade whose vocabulary is itself the
  obstacle, and not one that only works in one country.

Applied retroactively to Days 1–11: every story section rewritten, and the language of every other
section brought to the same standard. Day 0 is unchanged.
