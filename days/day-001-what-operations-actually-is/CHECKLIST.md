# Day 1 — Checklist

**Definition of done.** `./o done 1` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
./o trace && tail -1 docs/PROGRESS.md && awk -F'|' 'NF>5 && $2 ~ /^ *[0-9]+ *$/ {printf "%s %s\n", $2, substr($6,1,60)}' docs/INCIDENTS.md
```

Two curriculum IDs provably closed, a progress row that says so, and an incident ledger you can read
symptom-first — which is the artifact a stranger inherits.

---

## Setup

- [ ] `./o check` is green before you start (nothing from Day 0 is broken)
- [ ] `./o scaffold 1` has created `days/day-001-what-operations-actually-is/lab/`
- [ ] `git status --short` is clean, so anything that changes today is something you changed

---

## Section 1 — `01-what-ops-is`

- [ ] **1.1** read · ran `./o next` · answered out loud: *name the five questions, and say which one the sandwich arrangement failed first*
- [ ] **1.2** read · ran `./o check` twice · answered out loud: *what does the low-battery chirp buy you, in this part's vocabulary?*
- [ ] **1.3** read · ran `git log --oneline -5 && time ./o check` · answered out loud: *why is "what changed?" asked last?*
- [ ] **1.4** read · wrote and ran `lab/availability.py` · answered out loud: *which term of the formula does a rehearsed rollback move?*
- [ ] **1.5** read · ran the `grep -c` and the `awk` over `docs/CURRICULUM_INDEX.md` · answered out loud: *name a failure invisible to two specialisms and visible to one end-to-end check*
- [ ] **1.6** read · ran `scripts/depth_check.py 0` · answered out loud: *which row of the three-outcome table is a weekly auto-restart, and what must ship with it?*

---

## Section 2 — `02-the-repo-remembers`

- [ ] **2.1** read · ran `ls docs/` and the header check · answered out loud: *what property did the accurate, searchable chat thread lack?*
- [ ] **2.2** read · ran `wc -l` over the four ledgers · answered out loud: *name the four questions, and which ledger you reach for to reproduce a March prediction in September*
- [ ] **2.3** read · printed the first-symptom column with `awk` · answered out loud: *why can that column not be filled in accurately afterwards?*
- [ ] **2.4** read · all four ADRs read · answered out loud: *state the two-part filter for whether something deserves an ADR*
- [ ] **2.5** read · ran `./o trace && git status --short docs/` · answered out loud: *state the mistake that `kubectl edit` and a hand edit to `TRACKER.md` have in common*
- [ ] **2.6** read · **the drill is done, both steps** · answered out loud: *why was the check silent in step 1, and what production mechanism behaves the same way?*

---

## Section 3 — `03-the-handover-test`

- [ ] **3.1** read · ran the four handover commands · answered out loud: *which of the seven questions is red today, which day turns it green, and why is fudging it worse than leaving it red?*

---

## Build brief

- [ ] `lab/availability.py` written by hand and run; output matches the arithmetic in the part
- [ ] the MTTR crossover point found — the value at which System A becomes the more available one — and written down
- [ ] all four ADRs read, and the weakest *"what would make us change our minds"* section identified with a reason
- [ ] the seven handover questions scored for this repository, with your own eighth question added
- [ ] the four operator questions applied to one system you actually use, and the first unanswerable one named

---

## The check that must be able to fail

- [ ] **Step 1** — hub `ids:` set to a wrong claim while Day 1 has no `PROGRESS.md` row · `./o trace` run · **the silence observed and written down before moving on**
- [ ] **Step 2** — Day 1's `PROGRESS.md` row appended with the hub still broken · `./o trace` run · `3 problem(s)` and exit `1` observed
- [ ] `docs/TRACEABILITY.md`'s `## 🐛 Problems` section read — all three lines, and the difference between the two kinds understood
- [ ] **Step 3** — hub restored · `./o check` green · `2/279 closed, 0 problem(s)`
- [ ] one **boundary** of `./o check` found that nobody pointed out, in the manner of `docs/INCIDENTS.md` rows 7–9

---

## Ledgers

- [ ] `docs/PROGRESS.md` — Day 1's row appended with `>>`, verified with `tail -1`
- [ ] the `Commit` column filled in with the real short hash (not left as `pending`)
- [ ] `docs/INCIDENTS.md` — **at least two rows**, one per drill step, each with the *first symptom* written before the cause was known
- [ ] `docs/PACKAGES.md` — confirmed **no new rows** are needed today, and that this is a decision rather than an omission
- [ ] `docs/DECISIONS.md` — confirmed no new ADR is warranted today

---

## Cost

- [ ] `0` model calls, `0` tokens, `0` CI minutes, `0` MB resident confirmed — nothing was started today, so nothing needs stopping (Addendum 02 §4)

---

## Commit

- [ ] `./o check` green
- [ ] `git status --short` shows only files you intended to change
- [ ] committed with the message from the hub's §11
- [ ] `./o done 1`
