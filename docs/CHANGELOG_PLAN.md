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
