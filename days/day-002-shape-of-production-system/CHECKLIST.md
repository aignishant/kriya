# Day 2 — Checklist

**Definition of done.** `./o done 2` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
./days/day-002-shape-of-production-system/lab/check_architecture.sh && grep -c 'nobody\|a user tells us\|never\|TODO(me)' docs/ARCHITECTURE.md
```

A document describing a system that does not exist yet, a check that can refuse it, and a count of
everything it honestly admits it does not know.

---

## Setup

- [ ] `./o check` is green before you start
- [ ] `./o scaffold 2` has created `days/day-002-shape-of-production-system/lab/`
- [ ] ports 8765, 8777 and 8788 confirmed free with `netstat -ano | grep -E ":(8765|8777|8788).*LISTENING"`
- [ ] `git status --short` is clean, so anything that changes today is something you changed

---

## Section 1 — `01-the-request-path`

- [ ] **1.1** read · ran the loopback server and read the `-v` output by its `*`, `>` and `<` markers · answered out loud: *which of "connection refused" and "timeout" is the good news, and why?*
- [ ] **1.1** the refusal case and the timeout case both produced, and their **durations** noted — the refusal was not instant on this machine
- [ ] **1.2** read · `docs/ARCHITECTURE.md` §1 written with the Mermaid diagram and nine named boxes · answered out loud: *which of `API`'s four outgoing arrows must not block the response?*
- [ ] **1.3** read · `lab/budget.py` written and run · answered out loud: *name the three levers on the `LLM` hop, and which changes the experience without changing the total*
- [ ] **1.3** the `curl -w` timing run against a real host, and the three numbers read as three hops

---

## Section 2 — `02-dependencies`

- [ ] **2.1** read · `docs/ARCHITECTURE.md` §2 written, classified **per route** · answered out loud: *what makes a dependency soft, and why is the table not evidence of it?*
- [ ] **2.2** read · ran `uv pip list` and compared it to `pyproject.toml` · answered out loud: *name the five commitments, and which one is the only one in the pull request*
- [ ] **2.3** read · `lab/slow_dependency.py` written and run · answered out loud: *why is CPU low during this kind of outage?*
- [ ] **2.3** `TODO(me)` — concurrency raised until `/fast` actually slowed down, and **the number written down**
- [ ] **2.3** the `flush=True` behaviour confirmed by removing it and watching the log go silent

---

## Section 3 — `03-state`

- [ ] **3.1** read · `lab/stateful.py` written, run, killed, run again — the counter reset observed · answered out loud: *state the one-sentence test for statelessness*
- [ ] **3.2** read · `docs/ARCHITECTURE.md` §3 written, with exactly **one** row marked durable · answered out loud: *why does a health check that queries the database turn a database outage into a total outage?*
- [ ] **3.3** read · RPO, RTO and a `last tested` column added · answered out loud: *your RPO is one hour and the corruption started three days ago — which number failed you?*
- [ ] **3.3** every `last tested` cell honestly reads `never`, and none was left blank

---

## Section 4 — `04-blast-radius`

- [ ] **4.1** read · the three questions answered for `OTEL` and for `DB` · answered out loud: *which of the three kinds of blast radius never appears on a diagram?*
- [ ] **4.2** read · `docs/ARCHITECTURE.md` §4 written, **including the four rows with no box** (machine, network, disk, clock) · answered out loud: *why are those four the point rather than an oversight?*
- [ ] **4.2** the detection gaps counted, and left as gaps rather than filled in optimistically
- [ ] **4.3** read · `lab/check_architecture.sh` written and made executable · answered out loud: *what does a green result here entitle you to believe, and what does it not?*
- [ ] **4.4** read · the document's header written — who it is for, what it is not, what the check does not cover · answered out loud: *name the four places knowledge can live here, and what decides which*
- [ ] **4.4** `ADR-0007` written in your own words, with a **genuine advantage** given for the rejected option

---

## Build brief

- [ ] `docs/ARCHITECTURE.md` exists with all four sections and a header
- [ ] `docs/adr/ADR-0007-healthz-checks-the-process-only.md` written, with an expiry condition naming Day 41
- [ ] `lab/check_architecture.sh` · `lab/budget.py` · `lab/slow_dependency.py` · `lab/stateful.py` all written by hand and run
- [ ] `TODO(me)` — the fourth blast-radius column added: *what if it is slow rather than down?*, filled in for `DB`, `INDEX` and `LLM`
- [ ] `TODO(me)` — the `LLM` row left honestly `hard`, with the sentence that would let Day 129 change it
- [ ] `TODO(me)` — the seven handover questions from Day 1 re-scored now that `docs/ARCHITECTURE.md` exists, and the ones that moved noted

---

## The check that must be able to fail

- [ ] the check run **green** on a consistent document
- [ ] the **false positive** met — either reproduced by removing the `grep -v` line, or produced independently — and understood as the most dangerous kind of check failure
- [ ] the check run **red** on purpose: a node added to the diagram with no row in the table, `exit=1` confirmed
- [ ] the row added and the check run **green** again — three runs, not one (Principle 11)
- [ ] `TODO(me)` — a **false negative** found: a way the document can be wrong while the check stays green

---

## Ledgers

- [ ] `docs/PROGRESS.md` — Day 2's row appended with `>>`, verified with `tail -1`
- [ ] the `Commit` column filled in with the real short hash (not left as `pending`)
- [ ] `docs/PACKAGES.md` — the `curl` row and the Windows port-reuse row appended
- [ ] `docs/INCIDENTS.md` — **at least two rows**, the false positive and the deliberate break, each with the *first symptom* written before the cause was known
- [ ] `docs/DECISIONS.md` — the ADR-0007 row appended
- [ ] every server started today confirmed stopped, with `netstat` rather than by assumption

---

## Cost

- [ ] `0` model calls, `0` tokens, `0` CI minutes confirmed
- [ ] `0` MB resident at the end of the day — all three test servers killed and verified

---

## Commit

- [ ] `./o check` green
- [ ] `git status --short` shows only files you intended to change
- [ ] committed with the message from the hub's §11
- [ ] `./o done 2`
