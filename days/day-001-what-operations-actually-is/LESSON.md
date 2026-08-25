---
day: 1
phase: 1
phase_name: "The production mental model and the machine"
title: "What operations actually is"
ids: [FND-01, FND-02]
principles: [1, 2, 10, 11, 12, 13, 16, 17, 18]
kind: concept
plan_version: "v1.1.0"
parts: 13
generated: "2026-08-24"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 1 — What operations actually is

> **Yesterday (Day 0):** one tool owns the environment, the repository cannot leak a key by accident,
> and `./o` exists with two gates — one that reports health and one that refuses to finish a
> half-done day. Every one of them was made to fail on purpose before being trusted.
> **Today:** what the word *operations* actually names — the four questions an operator has to be able
> to answer about a running system, why failure is the normal state rather than the exception, and why
> this repository, not any conversation, is where the answers have to live.
> **Tomorrow (Day 2):** the shape of a production system — the request path, the dependencies, the
> state and the blast-radius map you draw for `pulse` before a single line of it exists.

---

## §1 Where we are

Yesterday built a floor. Today is about what gets built on it, and it starts with a question that
sounds too simple to spend a day on: *what is operations?*

Here is the honest version. Imagine you write something small and useful — a script that reads a list
of support tickets and sorts them by urgency. On your own machine it is finished. It runs, you read
the output, you are the only person who could possibly be disappointed by it.

Now other people start using it. Nothing about the program changed. But a whole set of new facts came
into existence, all at once, and none of them are facts about the code:

It runs when you are asleep, so somebody other than you finds out when it stops. It runs against
inputs you did not choose. It runs next to other programs competing for the same memory. And when it
is wrong, the cost lands on somebody else's morning rather than on your afternoon.

**Everything in the next two hundred and thirty-six days is a response to that paragraph.** Health
checks exist because you are asleep. Timeouts exist because things compete. Validation exists because
inputs surprise you. Rollbacks exist because being wrong is expensive for other people.

There is a useful analogy and it is worth taking seriously, because it explains the *shape* of the
job rather than just its content. A restaurant kitchen and a home kitchen contain the same equipment
and produce the same food. What separates them is not skill at cooking. It is that a restaurant has
to produce a consistent result, at volume, at an unpredictable rate, with staff who change, when the
supplier sends the wrong delivery — and that is why professional kitchens have checklists, station
prep, temperature logs and a person whose whole job is calling out what happens next. None of that is
about food. All of it is about *repeatability under conditions you do not control*.

Operations is the same discipline, for software. And like a kitchen, the memory has to live in the
room rather than in a person: the recipe on the wall, the log by the fridge, the note explaining why
this oven runs hot. **That is the second half of today.** A system whose explanations live in a chat
thread or in your head has, for operational purposes, not recorded them at all — because the question
gets asked at 3am, by somebody else, from a file.

So today gives you two things and then joins them. Four questions an operator must be able to answer.
Four ledgers where the answers live. And one test — *could a competent stranger operate this from the
repository alone?* — which is the exam Day 231 sets and which you begin passing or failing today.

---

## §2 The map

Thirteen documents in three sections. **Section 1 is `FND-01`** — what the job actually is.
**Section 2 is `FND-02`** — why the repository is the memory. **Section 3 is the synthesis**, where
the two IDs meet and produce something neither one contains.

### Section 1 — `01-what-ops-is`: what the job actually is
*The mental model: what changes when software has users, the questions that follow from it, and why
"the five kinds of ops" are one job rather than five.*

| Part | Answers | Level |
| --- | --- | --- |
| [1.1 — The day the code met real traffic](parts/01-what-ops-is/1.1-the-day-the-code-met-real-traffic.md) | What actually changes when other people start depending on your code? | `foundation` |
| [1.2 — "Does it work?" versus "Is it working?"](parts/01-what-ops-is/1.2-does-it-work-versus-is-it-working.md) | Two questions that sound identical — why does only one of them expire? | `foundation` |
| [1.3 — The four questions an operator must be able to answer](parts/01-what-ops-is/1.3-the-four-questions-an-operator-answers.md) | You are paged for a system you have never seen. What do you ask, in what order? | `working` |
| [1.4 — Failure is the normal state](parts/01-what-ops-is/1.4-failure-is-the-normal-state.md) | Why is the system that breaks thirteen times as often the more available one? | `working` |
| [1.5 — The five kinds of ops are one job](parts/01-what-ops-is/1.5-the-five-kinds-of-ops-are-one-job.md) | MLOps, LLMOps, AIOps, AgenticOps, MCPOps — what is genuinely new, and what is a costume? | `working` |
| [1.6 — Toil, and the line you automate](parts/01-what-ops-is/1.6-toil-and-the-line-you-automate.md) | Not *can* this be automated — **what happens when the automation is wrong?** | `production` |

### Section 2 — `02-the-repo-remembers`: the memory, and how it decays
*Where a system's knowledge has to live to survive a year and a departure, the four ledgers that hold
it, and the difference between a fact and a report computed from facts.*

| Part | Answers | Level |
| --- | --- | --- |
| [2.1 — Why the chat is not the memory](parts/02-the-repo-remembers/2.1-why-the-chat-is-not-the-memory.md) | The thread was accurate, detailed and searchable — so why did it fail? | `foundation` |
| [2.2 — The four ledgers](parts/02-the-repo-remembers/2.2-the-four-ledgers.md) | Four files, four questions — why not one file called `notes.md`? | `working` |
| [2.3 — The first-symptom column](parts/02-the-repo-remembers/2.3-the-first-symptom-column.md) | Which column of an incident record can you never reconstruct afterwards? | `working` |
| [2.4 — The ADR, and its expiry condition](parts/02-the-repo-remembers/2.4-the-adr-and-its-expiry-condition.md) | What turns a justification into a decision someone else can review? | `working` |
| [2.5 — Generated files, and why you never edit one](parts/02-the-repo-remembers/2.5-generated-files-you-never-edit.md) | Your edit vanished and nothing warned you — why is that the correct behaviour? | `production` |
| [2.6 — Breaking the memory on purpose](parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md) | **Make the traceability check refuse** — and find the moment it becomes armed | `production` |

### Section 3 — `03-the-handover-test`: where the two halves meet
*Neither half is worth much alone. The join is a test you can run today and will be graded on in
Phase 23.*

| Part | Answers | Level |
| --- | --- | --- |
| [3.1 — The handover test](parts/03-the-handover-test/3.1-the-handover-test.md) | Could a competent stranger operate this tomorrow, using only the repository? | `production` |

**The day climbs `foundation → working → production` in each section.**
[2.6](parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md) is the deliberate-failure
part the depth contract requires (plan §17.7): you make this repository's consistency check refuse,
and you discover on the way that it is silent until the moment you claim a day is finished.

---

## §3 Setup — run this

**Stop nothing; start nothing.** No profile runs today (Addendum 02 §4) — no containers, no cluster,
no observability stack. Day 1 has the same zero resident memory cost as Day 0, and it is the last day
in Phase 1 that involves no running service: `pulse` starts on Day 3.

**No packages are installed today.** `dependencies` stays `[]` in `pyproject.toml`. Packages arrive on
the day they are first used (Principle 7), and the first three arrive on Day 3.

```bash
# 1 — confirm yesterday's floor is still there. Should print "OK all green".
./o check

# 2 — create this day's scratch folder. Part 1.4 puts a small script in it.
./o scaffold 1

# 3 — read the four decision records. Everything in Day 0 and Day 1 follows from them.
ls docs/adr/

# 4 — read the incident ledger end to end, symptom column first. Ten rows, all from Day 0.
awk -F'|' 'NF>5 && $2 ~ /^ *[0-9]+ *$/ {printf "%s %s\n", $2, substr($6,1,60)}' docs/INCIDENTS.md
```

**Nothing new is pinned today**, so there are no version lookups and no new `docs/PACKAGES.md` rows
for tools. The versions in force are the ones Day 0 recorded and verified on 2026-08-24: git
`2.54.0.windows.1`, uv `0.12.3`, python `3.12.12` under `uv run`, ruff `0.16.4`, pytest `9.1.1`.

---

## §4 Build brief

Today writes no service code. `pulse/` stays empty until Day 3 — that is the plan's ordering, not an
omission (plan §13: eighty-four days of platform and observability come before the first model).

What you produce today is **five ledger rows, one scratch script and one drill.**

| File | Explained in | What it is |
| --- | --- | --- |
| `days/day-001-.../lab/availability.py` | [1.4](parts/01-what-ops-is/1.4-failure-is-the-normal-state.md) | **Yours to write** — the MTBF/MTTR arithmetic, so the counterintuitive result is one you produced |
| `docs/PROGRESS.md` row | [2.2](parts/02-the-repo-remembers/2.2-the-four-ledgers.md) | **Yours to write** — Day 1's row, appended with `>>` |
| `docs/INCIDENTS.md` rows | [2.6](parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md) | **Yours to write** — at least two, symptom column first |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` Write `lab/availability.py` from [1.4](parts/01-what-ops-is/1.4-failure-is-the-normal-state.md)
  and run it. Then change the numbers until System A beats System B, and write down the MTTR at which
  the crossover happens. That number is the argument for rehearsing a rollback.
- `TODO(me)` Score this repository against the seven handover questions in
  [3.1](parts/03-the-handover-test/3.1-the-handover-test.md). One is red today. Write your scores
  somewhere you will find them again on Day 229, and add an eighth question of your own.
- `TODO(me)` Do the drill in [2.6](parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md)
  **including step 1** — the one where the check stays silent. Record both observations as separate
  incident rows, because they are two different findings.
- `TODO(me)` Read all four ADRs in `docs/adr/`. For each one, find its *"what would make us change our
  minds"* section and decide whether the condition is genuinely observable by someone who was not in
  the room. One of them is weaker than the others; say which and why.
- `TODO(me)` Apply the four questions from [1.3](parts/01-what-ops-is/1.3-the-four-questions-an-operator-answers.md)
  to a system you actually use — your editor, your phone's backup, anything. Find the first question
  you cannot answer. That is where that system's operational work would start.
- `TODO(me)` Find one **boundary** of `./o check` that nobody told you about, the way rows 7 to 9 of
  `docs/INCIDENTS.md` were found. Something the gate does not look at. Record it whether or not you
  intend to fix it.

---

## §5 The check that must be able to fail

Today's gate is `scripts/trace.py`, the consistency check between three files: the plan's §14 (what
day 1 *should* close), this hub's `ids:` frontmatter (what it *claims*), and `docs/PROGRESS.md` (whether
day 1 is *green*).

```bash
./o trace
```

**Make it go red on purpose** —
[2.6](parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md) walks all four steps. The
short version: change this hub's `ids:` to a wrong claim, run the check, and observe that **it says
nothing** because Day 1 is not yet in `docs/PROGRESS.md`. Then append Day 1's progress row and run the
same check against the same broken hub, and watch it refuse:

```text
traceability: 0/279 closed, 3 problem(s); index: 279 IDs
```

Exit status `1`, and `docs/TRACEABILITY.md` gains a `## 🐛 Problems` section naming each disagreement
individually rather than reporting one generic failure.

**Step 1 is the one that teaches.** A check that is inert during the work and absolute at the boundary
is one of the most common shapes in production — a deploy gate, an admission controller, a GitOps
reconciler. Knowing *when* a check is armed matters as much as knowing what it checks, and the only
way to find out is to try it at both moments.

Restore the hub, run `./o check`, and confirm `2/279 closed, 0 problem(s)`. Two IDs closed,
permanently and provably, because three independent files agree.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline yet; Day 13 builds the first one. |
| Network | **0** | Nothing is downloaded. `uv sync` was Day 0's work and the cache is warm. |
| RAM (resident) | **0** | **No profile runs today.** Nothing to start, nothing to stop. |
| Disk | a few KB | Thirteen Markdown files, one scratch script, five ledger rows. |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). |

Day 1 and Day 0 are the last two days with a zero in the *RAM* row. From Day 3 there is a process
running, and from Day 21 there is a container runtime that never fully goes away.

---

## §7 Traps

- **Writing the incident row after you know the cause.** The first-symptom column is the only one you
  cannot reconstruct, and by the time you know the answer the symptom no longer looks mysterious.
  Capture it *before* you investigate ([2.3](parts/02-the-repo-remembers/2.3-the-first-symptom-column.md)).
- **`>` instead of `>>`.** One character between appending a ledger row and destroying the ledger.
  `git checkout -- <file>` recovers it *if* the file was committed.
- **Editing a generated file.** `TRACKER.md`, `TRACEABILITY.md` and `CURRICULUM_INDEX.md` are rewritten
  by the tools with no warning and no diff
  ([2.5](parts/02-the-repo-remembers/2.5-generated-files-you-never-edit.md)). Change the input.
- **Skipping step 1 of the drill.** Going straight to the red output loses the whole point — that the
  check was silent for as long as you were working, and only armed when you claimed to be done.
- **Leaving `pending` in the progress row.** Nothing checks the commit column. A row that says
  `pending` forever passes every gate in this repository and is useless on Day 107, when you need it
  to say which commit produced a result.
- **Reading "the five kinds of ops" as five toolchains.** They are the same four questions with a
  wider change surface. Treating them as separate is exactly the hospital-department failure in
  [1.5](parts/01-what-ops-is/1.5-the-five-kinds-of-ops-are-one-job.md).
- **Pasting a secret into an incident row.** Incident output routinely contains tokens and connection
  strings, `docs/INCIDENTS.md` is deliberately tracked, and `.gitignore` matches paths and never
  content — that is row 9 of the ledger. Redact before you paste; the CI scanner is Day 17.

**Named trap from plan §5.1: trap #4 — *the autonomy with no brake*.** Today meets it in its smallest
and most everyday form, in [1.6](parts/01-what-ops-is/1.6-toil-and-the-line-you-automate.md):
automating a task silently deletes the human inspection that came free with it. The rule that survives
to Day 175 and Day 194 is that the automation and the check that the automation worked land in the
same change — never in a later one.

---

## §8 Verify before you build

Today introduces no new tool, flag or API, so there is no version to look up and no vendor page to
check (Principle 8 says the page is checked *on the day the symbol is used*, and no new symbol is used
today). What is verified instead is this repository's own behaviour, observed live on **2026-08-24**:

| What | How it was verified | Where it is used |
| --- | --- | --- |
| `./o check` regenerates three files in `docs/` | ran it, then `git status --short docs/` | [1.2](parts/01-what-ops-is/1.2-does-it-work-versus-is-it-working.md), [2.5](parts/02-the-repo-remembers/2.5-generated-files-you-never-edit.md) |
| a hand edit to a generated file vanishes with no warning | appended a line, ran `./o tracker`, `grep -c` returned `0` | [2.1](parts/02-the-repo-remembers/2.1-why-the-chat-is-not-the-memory.md), [2.5](parts/02-the-repo-remembers/2.5-generated-files-you-never-edit.md) |
| `scripts/trace.py` reports problems only for days in `docs/PROGRESS.md` | read the source, then ran the drill both ways | [2.6](parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md) |
| the plan holds exactly 279 IDs across ten curricula | `grep -c '^\| \`' docs/CURRICULUM_INDEX.md` | [1.5](parts/01-what-ops-is/1.5-the-five-kinds-of-ops-are-one-job.md) |
| `awk` tie order is not deterministic | ran the same pipeline twice, got different orders for equal counts | [1.5](parts/01-what-ops-is/1.5-the-five-kinds-of-ops-are-one-job.md) |
| the linter ignores `days/*/lab` | `pyproject.toml` `extend-exclude`, confirmed by `docs/INCIDENTS.md` rows 7–8 | [1.2](parts/01-what-ops-is/1.2-does-it-work-versus-is-it-working.md), [1.4](parts/01-what-ops-is/1.4-failure-is-the-normal-state.md) |

**Not checked today, deliberately:** anything about HTTP, containers, Kubernetes, models or providers.
None of it is used today, and checking it now would produce a note that is stale by the day it matters.

---

## §9 Say it in an interview

> "I think of operations as the set of facts that become true the moment somebody else depends on your
> code — it runs when you're asleep, against inputs you didn't choose, sharing a machine, and the cost
> of being wrong lands on someone else. So the job reduces to being able to answer four questions
> fast, about a system you may not have written: is it up, is it correct, is it fast enough, and what
> changed. I ask them in that order deliberately, because each answer deletes a category of cause, and
> the classic waste is starting with 'what did we deploy' for a service that was never actually up.
> The second half is where the answers live. I'm fairly hard-line that a decision which only exists in
> a chat thread hasn't been recorded, because the question always gets asked from the artifact — so
> the reason a setting is odd goes in a comment next to the setting, pointing at a decision record. On
> the current project I keep four append-only ledgers: what's done, what versions we observed and
> when, what broke, and why things are the way they are. The one I'd defend hardest is the incident
> log, and specifically its *first symptom* column, filled in before the investigation — because
> debugging is a lookup from symptom to cause and that table is the only place it gets built. Three of
> the ten rows in mine have 'nothing — the check was green' in that column, which tells whoever
> inherits it exactly where our blind spots are."

---

## §10 Done when

Not when you have read all thirteen parts. **When every box in [`CHECKLIST.md`](CHECKLIST.md) is
honestly ticked and `./o check` is green.**

There is no time estimate in this day and there never will be (Principle 17). Day 1 is a unit of
subject, not a unit of time.

```bash
./o done 1
```

---

## §11 Ledger & commit

Paste these before running `./o done 1`. **Use the values you actually observed**, not the ones printed
here (Principle 7).

**`docs/PROGRESS.md`** — append one row:

```text
| 1 | 2026-08-24 | FND-01, FND-02 | 13 | <hash> | ✅ |
```

The commit hash does not exist until you commit, so write `pending`, commit, then replace it in a
follow-up commit — exactly as Day 0's row was filled in by commit `2c36b16`. **Do not leave it as
`pending`**: nothing in this repository checks that column, which is precisely why it is your job.

**`docs/PACKAGES.md`** — **no new rows.** Nothing is installed or pinned today. Stating that
explicitly is the discipline; a silent gap in a package ledger is indistinguishable from a forgotten
entry.

**`docs/INCIDENTS.md`** — **two rows minimum**, from the drill in
[2.6](parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md). They are two different
findings and belong in two rows. The first is the surprising one, and its *first symptom* column reads:

```text
| 11 | 2026-08-24 | 1 | Set this hub's `ids:` to FND-03, an ID the plan assigns to Day 2, while Day 1 had no row in PROGRESS.md | **nothing — `traceability: 0/279 closed, 0 problem(s)`, exit 0** | scripts/trace.py only reports a disagreement for days that are green in PROGRESS.md. An unfinished day is allowed to be wrong, so the check is inert for the whole time you are writing the day | none needed — restore the correct ids | Nothing yet, and that is the finding: the check is armed at the boundary, not during the work. Same shape as a GitOps reconciler (Day 56) |
| 12 | 2026-08-24 | 1 | Appended Day 1's PROGRESS row with the hub still claiming FND-03 | `traceability: 0/279 closed, 3 problem(s)` and a `## 🐛 Problems` section listing each ID separately | set equality is checked in both directions: two IDs assigned-but-unclaimed, one claimed-but-unassigned | restored `ids: [FND-01, FND-02]` | Nothing needed. Noted separately that the `Commit` column of PROGRESS.md is never validated — a row reading `pending` passes every gate |
```

**`docs/DECISIONS.md`** — no new rows. ADR-0001 to ADR-0004 already record why this plan is shaped
this way; **read all four today** ([2.4](parts/02-the-repo-remembers/2.4-the-adr-and-its-expiry-condition.md)
explains what to look for in each).

**Commit message:**

```text
day 001: what operations actually is — closes FND-01, FND-02

Establishes the mental model the next 235 days are built on: operations
is the set of facts that become true when other people depend on the
code, reduced to four questions an operator must answer about a running
system in a fixed order.

And establishes where the answers live. The repository is the memory:
four append-only ledgers, an ADR format whose expiry condition is
observable by a stranger, and three generated reports that are computed
rather than written. Made the traceability check refuse on purpose, and
found on the way that it is silent until a day is claimed as green.
```
