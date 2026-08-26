# Day 3 — Checklist

**Definition of done.** `./o done 3` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
uv run uvicorn pulse.api:app --host 127.0.0.1 --port 8000 & sleep 2 && curl -sS http://127.0.0.1:8000/version && curl -sS -X POST http://127.0.0.1:8000/predict -H 'content-type: application/json' -d '{"subject":"cannot log in","body":"password reset loops"}'
```

A service you wrote, running on your machine, reporting its own version and honouring a contract that
will still be true on Day 236.

---

## Setup

- [ ] `./o check` is green before you start
- [ ] `git status --short` is clean
- [ ] versions looked up **live** with `curl … pypi.org/pypi/<pkg>/json` — not copied from the hub
- [ ] `uv add fastapi==… uvicorn==…` and `uv add --dev httpx2==…`, all pinned with `==`
- [ ] `tool.uv.package` flipped from `false` to **`true`** in `pyproject.toml` (the Day 0 comment says today)
- [ ] `git diff uv.lock` read before committing — the transitive versions that moved are the surprise
- [ ] ports 8000, 8001 and 8010 confirmed free with `netstat`
- [ ] `./o scaffold 3` has created the day's `lab/`

---

## Section 1 — `01-what-we-are-building`

- [ ] **1.1** read · answered out loud: *why does the `/predict` response carry `model_version` when there is no model?*
- [ ] **1.2** read · `lab/bare_asgi.py` written and run under uvicorn · answered out loud: *a request returns `404` — which of the two programs produced it, and what does that tell you about the other?*
- [ ] **1.3** read · the three versions looked up live · answered out loud: *the tests passed with the deprecated package too — what told you to switch?*
- [ ] **1.3** `uv pip list` run, and the gap between what you asked for and what you got counted

---

## Section 2 — `02-the-service`

- [ ] **2.1** read · `pulse/__init__.py` and the application object written · routing table printed · answered out loud: *two causes of a `404` on a route you can see, and the one command that distinguishes them*
- [ ] **2.2** read · `/healthz` written with **no dependency call** · ADR-0007 re-read · answered out loud: *the five steps from "the database is slow" to "the whole service is gone"*
- [ ] **2.3** read · `/version` written, reading `__version__` rather than a literal · answered out loud: *three reasons an edit might not appear to take effect, and which is specific to this machine*
- [ ] **2.4** read · `Ticket`, `Prediction` and `/predict` written · answered out loud: *what real work does `/predict` do with no model?*
- [ ] **2.4** all three refusal shapes produced by hand: a missing field, an empty `subject`, and malformed JSON — and the `type`/`loc`/`ctx` parts read rather than the prose

---

## Section 3 — `03-running-it`

- [ ] **3.1** read · the service started with `--host` stated explicitly · `netstat -ano` used to find its process id · answered out loud: *name the three separate concepts inside one command*
- [ ] **3.1** the process killed by id, and the port **verified free afterwards** rather than assumed
- [ ] **3.2** read · output captured with `> server.log 2>&1` · answered out loud: *name the four startup lines in order and which program owns each*
- [ ] **3.2** the two streams separated once, confirming startup → stderr and access log → stdout
- [ ] **3.2** the access log read, and the **missing duration** noticed
- [ ] **3.3** read · `/openapi.json` fetched and its paths and schemas listed · answered out loud: *the document lists three paths and the service serves seven — name the four and say why a generated inventory omits them*
- [ ] **3.3** the decision recorded: docs pages stay on in development and the switch arrives on Day 9

---

## Section 4 — `04-testing-it`

- [ ] **4.1** read · `tests/test_api.py` written with all four tests · `uv run python -m pytest -q` green
- [ ] **4.1** answered out loud: *nothing about the gate changed today — so what did?*
- [ ] **4.2** read · **breakage 1** done, reverted, green again
- [ ] **4.2** **breakage 2** done — and the `ResponseValidationError` understood as the framework catching it *before* your assertion
- [ ] **4.2** **breakage 3** done — and understood as the one where the broken version looks healthier
- [ ] **4.2** **breakage 4** done — the test file renamed, `pytest exit=5` observed, **and `./o check` seen to print `OK all green`**
- [ ] **4.2** everything reverted; `git status --short` clean; `pytest --collect-only -q | tail -1` says `4`

---

## Section 5 — `05-failure`

- [ ] **5.1** read · **all four errors caused deliberately**, and the exact first line of each written down
- [ ] **5.1** error 3's real exit code obtained **without a pipe**, and the reason understood
- [ ] **5.1** answered out loud: *"Application startup complete" then an error — which program is fine?*
- [ ] `TODO(me)` a **fifth** first-run error found that 5.1 does not list, caused, and recorded
- [ ] **5.2** read · the temporary drill route added · `healthz 200` and `503` observed from one process
- [ ] **5.2** answered out loud: *name the two things that would have caught it, which day each arrives, and which would have woken somebody*
- [ ] **5.2** the temporary route **deleted**, proven with `git diff`

---

## Build brief

- [ ] `pulse/__init__.py`, `pulse/api.py` and `tests/test_api.py` written by hand, every line
- [ ] `lab/bare_asgi.py` written and run
- [ ] `docs/ARCHITECTURE.md` updated — the `API` box is no longer a plan
- [ ] Day 2's `lab/check_architecture.sh` re-run and still green after that edit
- [ ] `TODO(me)` resident memory and startup duration measured on your machine and recorded
- [ ] `TODO(me)` the four routes you did not write examined, and a decision stated for each

---

## The check that must be able to fail

- [ ] the test suite seen **red** three different ways and **green** once with the suite missing
- [ ] the manual count habit established: `pytest --collect-only -q | tail -1` before trusting a green gate
- [ ] the [5.2](parts/05-failure/5.2-the-health-check-that-lies.md) drill run, and the fact that **neither probe would have fired** understood rather than fixed

---

## Ledgers

- [ ] `docs/PROGRESS.md` — Day 3's row appended with `>>`, verified with `tail -1`
- [ ] the `Commit` column filled in with the real short hash (not left as `pending`)
- [ ] `docs/PACKAGES.md` — three package rows plus your machine's memory and startup figures
- [ ] `docs/INCIDENTS.md` — **at least two rows**: the green-gate breakage and the honest health check, each with the *first symptom* written before the cause was known
- [ ] `docs/DECISIONS.md` — confirmed no new ADR is needed; ADR-0007 already covers `/healthz`
- [ ] every server started today confirmed stopped, with `netstat` rather than by assumption

---

## Cost

- [ ] `0` model calls, `0` tokens, `0` CI minutes confirmed
- [ ] ~40 MB of packages downloaded once and cached; the figure recorded
- [ ] `0` MB resident at the end of the day — the uvicorn process stopped and verified

---

## Commit

- [ ] `./o check` green
- [ ] `git status --short` shows only files you intended to change
- [ ] `git diff` confirms no drill code survived
- [ ] committed with the message from the hub's §11
- [ ] `./o done 3`
