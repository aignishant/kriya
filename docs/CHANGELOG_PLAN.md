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
