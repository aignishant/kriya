---
day: 3
phase: 1
phase_name: "The production mental model and the machine"
title: "pulse v0"
ids: [FND-04]
principles: [1, 2, 4, 7, 8, 10, 11, 13, 16, 17, 18]
kind: lab
plan_version: "v1.2.0"
parts: 14
generated: "2026-08-24"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 3 — `pulse` v0

> **Yesterday (Day 2):** the shape of a production system, drawn before any of it existed — the
> request path as nine named boxes, each dependency classified per route, state placed so exactly one
> store is durable, and a blast-radius map whose most valuable column was *how would we find out*. Six
> of twelve rows answered "nobody" or "a user tells us".
> **Today:** the first box on that diagram becomes a running process. Three routes, three pinned
> packages, four tests, and a service you can start, stop, break and diagnose.
> **Tomorrow (Day 4):** Linux for operators I — the process you started today, the signals that kill
> it, the exit codes it returns, and what "the service died" actually means.

---

## §1 Where we are

Two days of drawing. Today something runs.

It is worth being clear about how little it does, because the smallness is the design. `pulse` v0
answers three questions and nothing else: *are you alive?*, *what are you?*, and *here is a support
ticket, what do you make of it?* The answer to the third is a fixed stub, because there is no model
until Day 109.

That sounds like a toy and it is not, for the same reason a first driving lesson spent entirely in an
empty car park is not a waste. The next hundred days do things *to* this service. They put it in a container,
onto a cluster, behind an ingress, through a pipeline, under a load test, into a canary, behind an
objective. Every one of those days needs something to operate. If that something is complicated, each
day is partly about the complication. If it is three routes, each day is entirely about the subject.

So today builds the smallest thing that is genuinely a service, and then spends most of its effort on
the parts that are not the code:

**What the pieces actually are.** A web framework is two programs rather than one: a server that owns
the socket and speaks HTTP, and an application that owns the routing and speaks Python. Knowing where
that boundary sits decides which program you look at when something fails, and today four of the five
errors you produce are on one side or the other.

**What is being decided permanently.** The model is an implementation detail; the *contract* is not.
What a client must send, what it gets back, and how it is refused — those three outlive every version
of the thing behind them, which is why `/predict` has a `model_version` field on a day when there is no
model.

**What you looked up rather than remembered.** Three packages arrive, each version fetched live. One of
them is not the package you would have guessed, and the only reason you know is that a deprecation
warning was read rather than skimmed. The tests passed either way — which is the whole argument for
reading the output above the last line.

**What breaks, and how to tell the shapes apart.** Four first-run errors, each produced on purpose:
wrong module, wrong attribute, port in use, wrong path. They are distinguishable in seconds by counting
the startup lines, and that count is a skill you will use on Day 40 when the only window into a
crashing container is the same output.

And then the day's real lesson, which is uncomfortable: **you make the health check tell the truth and
be useless at the same time.** `/healthz` returns `200` while the endpoint people actually need returns
`503`. Nothing is broken, nothing would restart, nothing would alert, and every user is stuck. That is
not a bug to fix today — it is the cost of a decision made on Day 2, seen clearly, so that Day 41 and
Day 73 are recognitions rather than surprises.

---

## §2 The map

Fourteen documents in five sections, all closing `FND-04`. **The sections are the build order**: decide
what to build, write it, run it, test it, break it. Sections 4 and 5 carry the deliberate failures.

### Section 1 — `01-what-we-are-building`: the decisions before the code
*What v0 is for, what the framework actually does, and three versions looked up rather than
remembered.*

| Part | Answers | Level |
| --- | --- | --- |
| [1.1 — Why the first version does almost nothing](parts/01-what-we-are-building/1.1-why-the-first-version-does-almost-nothing.md) | Three routes and a stub — what is being decided permanently anyway? | `foundation` |
| [1.2 — What an HTTP framework actually gives you](parts/01-what-we-are-building/1.2-what-an-http-framework-gives-you.md) | Two programs, one interface — which one produced your `404`? | `foundation` |
| [1.3 — Choosing the pieces, and pinning them](parts/01-what-we-are-building/1.3-choosing-the-pieces-and-pinning-them.md) | The tests passed with the deprecated package too. What told you to switch? | `working` |

### Section 2 — `02-the-service`: writing it
*Four routes' worth of decisions, in about forty lines. The application object, then one part per
endpoint.*

| Part | Answers | Level |
| --- | --- | --- |
| [2.1 — The application object and the first route](parts/02-the-service/2.1-the-application-object-and-the-first-route.md) | A route exists in the file and returns `404` — which two causes, and which command tells them apart? | `working` |
| [2.2 — `/healthz` — the endpoint that must not lie](parts/02-the-service/2.2-healthz-the-endpoint-that-must-not-lie.md) | Five steps from "the database is slow" to "the whole service is gone" | `working` |
| [2.3 — `/version` — what is actually running](parts/02-the-service/2.3-version-what-is-actually-running.md) | Every other way of answering "what is deployed?" is stale. Why? | `working` |
| [2.4 — `/predict` — the contract before the model](parts/02-the-service/2.4-predict-the-contract-before-the-model.md) | There is no model — so what real work does this endpoint do? | `working` |

### Section 3 — `03-running-it`: starting, reading, and what you published
*One command that hides three concepts, five lines of output that are a checklist, and four routes you
did not write.*

| Part | Answers | Level |
| --- | --- | --- |
| [3.1 — The server, the port and the process](parts/03-running-it/3.1-the-server-the-port-and-the-process.md) | Three separate things in one command — and one of them can be claimed twice on Windows | `working` |
| [3.2 — Reading the startup output](parts/03-running-it/3.2-reading-the-startup-output.md) | "Application startup complete" then an error. What succeeded? | `working` |
| [3.3 — The interactive docs, and why you will turn them off](parts/03-running-it/3.3-the-interactive-docs-and-why-you-turn-them-off.md) | You wrote three routes and published seven. What is the eighth thing you did not check? | `production` |

### Section 4 — `04-testing-it`: the first real tests
*Four tests with no server, and the moment a three-day-old exemption stops being honest.*

| Part | Answers | Level |
| --- | --- | --- |
| [4.1 — The first real test, and the end of the exit-5 exemption](parts/04-testing-it/4.1-the-first-real-test.md) | Nothing about the gate changed today — so what did? | `working` |
| [4.2 — Making the tests go red — four breakages on purpose](parts/04-testing-it/4.2-making-the-test-go-red.md) | **Three breakages turn it red. One turns it green.** | `production` |

### Section 5 — `05-failure`: the errors, and the honest one
*The four errors of a first run, and then the health check that is right and useless.*

| Part | Answers | Level |
| --- | --- | --- |
| [5.1 — The four errors of a first run](parts/05-failure/5.1-the-four-errors-of-a-first-run.md) | Count the `INFO` lines — what does each count eliminate? | `production` |
| [5.2 — The health check that lies](parts/05-failure/5.2-the-health-check-that-lies.md) | **`200` and `503` from one process, in the same second, both correct** | `production` |

**The day climbs `foundation → working → production`.** Two parts carry the deliberate failures the
depth contract requires (plan §17.7):
[4.2](parts/04-testing-it/4.2-making-the-test-go-red.md) breaks each test in a different way and finds
that one breakage leaves the gate **green**, and
[5.2](parts/05-failure/5.2-the-health-check-that-lies.md) makes the service useless while every health
signal stays healthy.

---

## §3 Setup — run this

**Nothing to stop.** No profile is running (Addendum 02 §4). Today starts the `core` profile's first
component — but only as a plain local process: the `core` profile in Addendum 02 eventually means
`pulse` plus Postgres, and Postgres arrives with containers on Day 21. Today `core` is one Python
process at roughly 60 MB.

**Three packages arrive today** — the first runtime dependencies this project has ever had. Look them
up rather than copying the numbers below (Principle 7):

```bash
# 1 — look up the current version of each, live
for p in fastapi uvicorn httpx2; do
  v=$(curl -s "https://pypi.org/pypi/$p/json" | python -c "import sys,json;print(json.load(sys.stdin)['info']['version'])")
  echo "$p == $v"
done

# 2 — add them, pinned exactly. httpx2 is a DEV dependency: it exists only for the tests.
uv add fastapi==0.141.1 uvicorn==0.52.4
uv add --dev httpx2==2.12.0

# 3 — pulse/ gains real modules today, so the project must be installable
#     FLIP tool.uv.package FROM false TO true in pyproject.toml — the Day 0 comment says to do it today

# 4 — confirm the ports this day uses are free
netstat -ano | grep -E ":(8000|8001|8010).*LISTENING" || echo "all three ports free"

# 5 — this day's scratch folder
./o scaffold 3
```

**Verified live on 2026-08-24** (Principle 7 — looked up, not remembered):

| Package | Version | How | Why |
| --- | --- | --- | --- |
| fastapi | 0.141.1 | `curl -s https://pypi.org/pypi/fastapi/json` | routing, validation, OpenAPI from type hints |
| uvicorn | 0.52.4 | same | the ASGI server FastAPI's own docs use |
| httpx2 | 2.12.0 | same | **dev only** — `starlette.testclient` deprecates plain `httpx`; see [1.3](parts/01-what-we-are-building/1.3-choosing-the-pieces-and-pinning-them.md) |

Those three resolve to **ten** installed packages. `starlette 1.6.0` and `pydantic 2.13.4` are the two
worth knowing by name; they will appear in tracebacks for the next two hundred days.

⚠️ **`tool.uv.package = false` must become `true` today.** Day 0 set it to `false` because `pulse/`
held nothing importable, and the comment in `pyproject.toml` says *"FLIP THIS TO TRUE ON DAY 3"*. Today
is that day: the tests import `pulse.api`, and they cannot if the project is not installed.

---

## §4 Build brief

Today you write the first project code in this repository. **Every line is printed in the parts and
typed by you** (`days/README.md`, rule 1).

| File | Explained in | What it is |
| --- | --- | --- |
| `pulse/__init__.py` | [2.1](parts/02-the-service/2.1-the-application-object-and-the-first-route.md) | **Yours to write** — three lines, and the single definition of `__version__` |
| `pulse/api.py` | [2.1](parts/02-the-service/2.1-the-application-object-and-the-first-route.md)–[2.4](parts/02-the-service/2.4-predict-the-contract-before-the-model.md) | **Yours to write** — the application object, two pydantic models, three routes |
| `tests/test_api.py` | [4.1](parts/04-testing-it/4.1-the-first-real-test.md) | **Yours to write** — four tests, no server, no port |
| `pyproject.toml` | §3 above | **Yours to change** — three pins, and `package = true` |
| `lab/bare_asgi.py` | [1.2](parts/01-what-we-are-building/1.2-what-an-http-framework-gives-you.md) | **Yours to write** — an ASGI app in twelve lines, no framework |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — three rows, dated, with a reason each |
| `docs/ARCHITECTURE.md` | [2.1](parts/02-the-service/2.1-the-application-object-and-the-first-route.md) | **Yours to update** — the `API` row stops being a plan |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` Write `lab/bare_asgi.py` from [1.2](parts/01-what-we-are-building/1.2-what-an-http-framework-gives-you.md)
  and run it under the same uvicorn that runs `pulse`. Then add a second `send` call and find out what
  happens when a response body arrives after the response has ended.
- `TODO(me)` Print the routing table and count it. You wrote three routes; the object holds seven. For
  each of the four you did not write, say what it is for and whether you want it in production.
- `TODO(me)` In [4.2](parts/04-testing-it/4.2-making-the-test-go-red.md), do **all four** breakages
  including the fourth. Record the fourth in `docs/INCIDENTS.md` — it is the one that leaves the gate
  green.
- `TODO(me)` Find a **fifth** first-run error that [5.1](parts/05-failure/5.1-the-four-errors-of-a-first-run.md)
  does not list. Cause it deliberately, write down the exact first line of output, and add a row.
- `TODO(me)` Measure `pulse`'s resident memory and its startup duration on your machine, and write both
  into `docs/PACKAGES.md`. Startup is effectively instant today; on Day 109 it will not be, and you will
  want to know what it used to be.
- `TODO(me)` Update `docs/ARCHITECTURE.md`: the `API` box now exists. Change its row, and re-run
  `lab/check_architecture.sh` from Day 2 to confirm the document is still consistent.
- `TODO(me)` Delete the temporary route from [5.2](parts/05-failure/5.2-the-health-check-that-lies.md)
  and prove it with `git diff`. A drill that leaves the system modified is an incident you caused.

---

## §5 The check that must be able to fail

Today the repository gets its first real tests, so the gate's test step finally runs something. **It
goes red four different ways**, and the fourth is the one worth the day.

```bash
uv run python -m pytest -q
```

[4.2](parts/04-testing-it/4.2-making-the-test-go-red.md) walks all four. In summary:

| Breakage | Result |
| --- | --- |
| 1 — `/healthz` returns `"OK"` | `AssertionError: assert {'status': 'OK'} == {'status': 'ok'}` — your test caught it |
| 2 — `/predict` returns two fields short | `fastapi.exceptions.ResponseValidationError` — **the framework caught it first** |
| 3 — `body` loses its constraints | `assert 200 == 422` — **the broken version looks healthier** |
| 4 — the test file is renamed | `no tests ran`, `pytest exit=5`, **`./o check` → `OK all green`** |

**Breakage 4 is the point.** `pytest` exits `5` for *"no tests collected"*, and `o`'s
`|| [ $? -eq 5 ]` forgives it — correctly on Day 0, when there were no tests, and **wrongly from today**,
when four exist and their absence means the suite did not run. `docs/INCIDENTS.md` row 4 predicted this
expiry three days ago; today confirms it arrived. Day 14 closes it with a minimum test count.

Until then the only evidence is a manual count:

```text
$ uv run python -m pytest --collect-only -q | tail -1
4 tests collected in 0.44s
```

**And the second red gate today** is [5.2](parts/05-failure/5.2-the-health-check-that-lies.md), which
is red in a different sense — the service becomes useless while every signal stays green:

```text
healthz -> 200
HTTP/1.1 503 Service Unavailable
{"detail":"classification unavailable: model not loaded"}
```

Both true, one process, same second. Nothing would restart and nothing would alert.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline yet; Day 13 builds the first one, and today's tests are what it will run. |
| Network | ~40 MB, once | Three packages and their transitive tree, downloaded and then cached. Three lookups against `pypi.org`. |
| RAM (resident) | **~60 MB while running** | One uvicorn process. **The first non-zero entry in this row**, and it never returns to zero. |
| Disk | ~40 MB | The three packages in `.venv`, plus about 100 lines of your own code. |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). |

Day 0, 1 and 2 all had a zero in the RAM row. Today ends that, and from Day 21 a container runtime
joins it and never leaves.

---

## §7 Traps

- **Forgetting `content-type: application/json` on a `curl -d`.** `curl` defaults to form encoding,
  FastAPI does not parse the body as JSON, and you get a confusing `422` about a field that is plainly
  present. The single most common self-inflicted error when testing an API by hand
  ([2.4](parts/02-the-service/2.4-predict-the-contract-before-the-model.md)).
- **Believing an edit took effect.** Python imports a module once. A running process never sees your
  change — restart it, or use `--reload` in development
  ([2.3](parts/02-the-service/2.3-version-what-is-actually-running.md), [3.1](parts/03-running-it/3.1-the-server-the-port-and-the-process.md)).
- **Trusting a `kill`.** On this machine two processes can end up listening on one port and no error is
  printed. `netstat -ano | grep :8000` after every kill, and **count the lines**
  ([5.1](parts/05-failure/5.1-the-four-errors-of-a-first-run.md)).
- **Reading only the last line of `pytest`.** `4 passed` was true both before and after the `httpx2`
  fix; the warning above it was the thing that mattered
  ([1.3](parts/01-what-we-are-building/1.3-choosing-the-pieces-and-pinning-them.md)).
- **Stopping at `Application startup complete`.** It is printed *before* the port is bound, so a service
  can report itself started and then fail ([3.2](parts/03-running-it/3.2-reading-the-startup-output.md)).
- **Piping a command whose exit code you need.** In a pipeline `$?` is the last command's status, so
  `uvicorn … | tail` reported `exit=0` on a run that actually exited `3`
  ([5.1](parts/05-failure/5.1-the-four-errors-of-a-first-run.md)).
- **Unquoted `curl -w` format strings in Git Bash.** `%{...}` containing a leading-slash path gets
  rewritten into a Windows path — a real, observed, baffling output
  ([3.3](parts/03-running-it/3.3-the-interactive-docs-and-why-you-turn-them-off.md)).
- **Making `/healthz` "better".** Every dependency you add to it is a way for that dependency's outage
  to restart every instance you have ([2.2](parts/02-the-service/2.2-healthz-the-endpoint-that-must-not-lie.md)).
- **Leaving the [5.2](parts/05-failure/5.2-the-health-check-that-lies.md) drill route in place.** It
  always returns `503`. `git diff` before you commit.

**Named trap from plan §5.1: trap #1 — *the tutorial that runs as root, on `:latest`, with no
limits*.** Today is its opposite at the smallest scale: three versions looked up live and pinned with
`==`, a bind to loopback stated explicitly rather than inherited, and length limits on every input
field in the same change that introduced the input. The habit costs nothing today and is the whole of
Day 27 and Day 28.

---

## §8 Verify before you build

Fetched and observed live on **2026-08-24** while writing this day (Principle 8).

| What | Where / how | Why today |
| --- | --- | --- |
| fastapi, uvicorn, httpx2 versions | `curl -s https://pypi.org/pypi/<pkg>/json` | the three pins ([1.3](parts/01-what-we-are-building/1.3-choosing-the-pieces-and-pinning-them.md)) |
| `httpx` is deprecated for `starlette.testclient` | the warning in `pytest` output, then `pypi.org/pypi/httpx2/json` | why the dev pin is `httpx2` and not `httpx` |
| the resolved tree | `uv pip compile` and `uv sync` | ten packages for three requests ([1.3](parts/01-what-we-are-building/1.3-choosing-the-pieces-and-pinning-them.md)) |
| HTTP `503 Service Unavailable` | `rfc-editor.org/rfc/rfc9110.txt` §15.6.4 — fetched and grepped | `503` not `500` for a dependency outage ([5.2](parts/05-failure/5.2-the-health-check-that-lies.md)) |
| the OpenAPI document `pulse` publishes | `curl /openapi.json` — `3.1.0`, three paths, **four** schemas | two schemas were added by the framework ([3.3](parts/03-running-it/3.3-the-interactive-docs-and-why-you-turn-them-off.md)) |
| the routing table | `python -c "…[r.path for r in app.routes]"` — **seven** routes | four you did not write ([2.1](parts/02-the-service/2.1-the-application-object-and-the-first-route.md)) |
| uvicorn's log streams | redirected stdout and stderr separately | **startup → stderr, access log → stdout** ([3.2](parts/03-running-it/3.2-reading-the-startup-output.md)) |
| the four first-run errors | each one caused deliberately | verbatim text in [5.1](parts/05-failure/5.1-the-four-errors-of-a-first-run.md) |
| `kill %1` from Git Bash | ran it, read the log | **no shutdown handshake** — the graceful path is not exercised here ([3.2](parts/03-running-it/3.2-reading-the-startup-output.md)) |

**Not checked today, deliberately:** anything about containers, Kubernetes, Postgres or a model
provider. None of their symbols are used today.

---

## §9 Say it in an interview

> "The first version of a service I build does almost nothing on purpose — the point is to prove the
> whole path from client to deployment before anything interesting depends on it, because what that
> finds is never the code, it's the certificate or the permission or the base image. What I *do* decide
> properly on day one is the contract: what a client must send, what it gets back, and how it's
> refused. Those outlive every implementation. Concretely, our prediction response carried a
> `model_version` field months before there was a model, because the first time you run two model
> versions side by side you need every response attributable and by then every client would have to
> change. I'm also fairly deliberate about health checks. Ours reports only that the process can
> respond — it deliberately doesn't touch the database, because if it did, a database outage would fail
> every instance's liveness probe simultaneously, restart all of them, and none would recover; you'd
> turn a partial outage into a total one with your own monitoring. The honest cost is that a green
> health check doesn't mean the service is useful, and I've demonstrated that — same process, `200` on
> health and `503` on the endpoint people need, and nothing would have paged. What catches that isn't a
> better probe, it's measuring whether real requests succeed. And on dependencies: I look versions up
> rather than remembering them. Last time I did that the test client I'd always used had been
> deprecated in favour of a successor package; the tests passed either way, and the only reason I
> caught it was reading the warning above the summary line."

---

## §10 Done when

Not when the three routes answer. **When every box in [`CHECKLIST.md`](CHECKLIST.md) is honestly ticked
and `./o check` is green.**

There is no time estimate in this day and there never will be (Principle 17).

```bash
./o done 3
```

---

## §11 Ledger & commit

Paste these before running `./o done 3`. **Use the values you actually observed** (Principle 7).

**`docs/PROGRESS.md`** — append one row:

```text
| 3 | 2026-08-24 | FND-04 | 14 | <hash> | ✅ |
```

Write `pending`, commit, then replace it with the real short hash in a follow-up commit. Nothing in
this repository validates that column.

**`docs/PACKAGES.md`** — **three rows minimum**, plus your machine's numbers:

```text
| fastapi | 0.141.1 | 2026-08-24 | 3 | Routing, validation and an OpenAPI document generated from type hints. Observed with `curl -s https://pypi.org/pypi/fastapi/json`. Pulls in starlette 1.6.0 and pydantic 2.13.4. |
| uvicorn | 0.52.4 | 2026-08-24 | 3 | The ASGI server. One process, one core — Day 42 revisits workers. Observed with `curl -s https://pypi.org/pypi/uvicorn/json`. |
| httpx2 | 2.12.0 | 2026-08-24 | 3 | **Dev only.** `starlette.testclient` warns that plain `httpx` is deprecated and names httpx2; switching removed the warning and the four tests still pass. Released 2026-08-18. |
| pulse: resident memory | <yours> MB | 2026-08-24 | 3 | Measured while running with no traffic. The first non-zero RAM figure in this plan; Day 42 sets a limit against it. |
| pulse: startup duration | <yours> | 2026-08-24 | 3 | Effectively instant with no startup hooks. Day 109 loads a model here and Day 41 needs a startupProbe because of it. |
```

**`docs/INCIDENTS.md`** — **two rows minimum.** The first is breakage 4 from
[4.2](parts/04-testing-it/4.2-making-the-test-go-red.md), and it is the important one because the gate
stayed green:

```text
| 15 | 2026-08-24 | 3 | Renamed tests/test_api.py to tests/api_tests.py so pytest could not collect it, then ran the gate | `no tests ran in 0.01s`, pytest exit=5 — and then **`./o check` printed `OK all green`, exit=0** | The exit-5 exemption in `o` (`\|\| [ $? -eq 5 ]`) was correct on Day 0 when no tests existed and became a hole the moment tests did. Four tests were effectively deleted and the gate could not tell | renamed the file back; confirmed 4 collected | Nothing yet — Day 14 adds a minimum test count. Until then the only evidence is `pytest --collect-only -q \| tail -1`, run by hand. Predicted by row 4 three days ago |
| 16 | 2026-08-24 | 3 | Ran the 5.2 drill: a route that raises 503 while /healthz still answers | `healthz -> 200` and `HTTP/1.1 503 Service Unavailable` from the same process in the same second | Not a bug. Liveness answers "can this process respond?", and it can. Nothing would restart, nothing would alert, and every user is stuck | deleted the temporary route, verified with `git diff` | Nothing yet. Readiness is Day 41 and the user-outcome SLO is Day 73 — and only the second would have caught this |
```

**`docs/DECISIONS.md`** — no new rows. ADR-0007 from Day 2 already records why `/healthz` checks only
the process, and today is the code that follows from it. **Re-read it before writing
[2.2](parts/02-the-service/2.2-healthz-the-endpoint-that-must-not-lie.md).**

**Commit message:**

```text
day 003: pulse v0 — closes FND-04

The first running service: three routes, three pinned packages, four
tests. /healthz answers only that the process can respond (ADR-0007),
/version reports what is actually running from a single definition, and
/predict fixes the request and response contract before there is a model
to fill it — including the model_version field Day 111's canary needs.

Versions looked up live rather than remembered, which is how the test
client turned out to want httpx2 rather than httpx; the tests passed
either way and only the warning said so.

Broke the tests four ways. Three went red. The fourth — renaming the
test file — left the gate green, because the exit-5 exemption written on
Day 0 stopped being honest today. Recorded, with the day that closes it.

Then made the service useless while every health signal stayed green:
200 on /healthz and 503 on the route people need, from one process, in
the same second. Neither probe would have fired.
```
