---
day: 2
phase: 1
phase_name: "The production mental model and the machine"
title: "The shape of a production system"
ids: [FND-03]
principles: [1, 2, 8, 10, 11, 12, 13, 16, 17, 18]
kind: concept
plan_version: "v1.1.0"
parts: 13
generated: "2026-08-24"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 2 — The shape of a production system

> **Yesterday (Day 1):** what operations actually is — the four questions an operator must answer
> about a running system, and the four ledgers that make this repository the memory rather than the
> chat. You made the traceability check refuse on purpose and found that it is silent until a day is
> claimed as green.
> **Today:** the shape `pulse` will have, drawn before a line of it exists — the request path, the
> dependencies and what each one's absence costs, where state lives, and the blast-radius map. Four
> tables, one diagram, and a check that can refuse them.
> **Tomorrow (Day 3):** `pulse` v0. The first box on the diagram becomes a running process with a
> port, three routes and the first real test in this repository.

---

## §1 Where we are

There is a moment in any building project that costs almost nothing and decides almost everything:
the moment somebody draws the plan. Not the pretty elevation for the client — the boring one, with
the drains on it.

The drawing is cheap because nothing has been built. Moving a wall on paper takes a minute. The same
wall, once the plumbing runs through it, takes a week and three arguments. And the reason to draw the
drains rather than the elevation is that drains are where the expensive surprises live: the sink can
go anywhere, but the sink two rooms from the drain will block twice a year forever, and you will only
notice that by looking at the *connections* rather than at the rooms.

`pulse` does not exist. Nothing has been built. This is the drains drawing.

Today you write down four things about a system that has no code yet:

**What talks to what.** A request is not a function call — it is a journey through several machines,
and each leg can be slow, can fail, and can fail in a way the next leg cannot distinguish from
success. Drawing the legs turns *"the service is slow"* from an opinion into a question with eight
candidate answers.

**What you depend on, and what happens without it.** Every dependency is a permanent commitment to
somebody else's availability, latency and version. The useful question is never *"is it
important?"* — it is *"what does the user get when this is gone?"*, and there are exactly four
acceptable answers to that.

**Where the state lives.** Not in the process, if you want to be able to restart it. So it lives
somewhere else, and *somewhere else* is now the part of the system that needs backups, a tested
restore, and two numbers nobody usually decides: how much you may lose, and how long you may be
without it.

**What breaks when each part breaks.** One row per component, and the column that matters is not
*what stops working* but *how would we find out*. Six of today's twelve rows answer *nobody*, or *a
user tells us*. Writing that down honestly is the deliverable — those six rows are the alert backlog
for Phase 8, arrived at by reasoning about failure rather than by alerting on whatever the tooling
happens to expose.

Then you do the thing that makes it real rather than decorative: **you give the document a check, and
you make the check go red.** A fire evacuation plan in a frame, pointing at a door that was bricked up
two years ago, is worse than no plan — because people follow it. A diagram nothing can contradict will
eventually contradict reality, quietly, and the only defence is a command that compares two things and
exits non-zero.

Nothing today runs in production. Everything today is a decision that is free to make now and
expensive to make later.

---

## §2 The map

Thirteen documents in four sections. **All four close the same ID, `FND-03`**, and they are ordered as
the four questions above: the path, then the dependencies along it, then the state behind it, then
what happens when any of it fails. The last section is where the day's deliberate failure lives.

### Section 1 — `01-the-request-path`: what talks to what
*A request is a journey, not a call. Draw the journey, then find out where the time goes.*

| Part | Answers | Level |
| --- | --- | --- |
| [1.1 — A request is a path, not a function call](parts/01-the-request-path/1.1-a-request-is-a-path-not-a-function-call.md) | Why is "connection refused" better news than a timeout? | `foundation` |
| [1.2 — Drawing the path for `pulse`, before `pulse` exists](parts/01-the-request-path/1.2-drawing-the-path-for-pulse.md) | Nine boxes, and the one that is somebody else's uptime | `working` |
| [1.3 — Latency adds up along the path](parts/01-the-request-path/1.3-latency-adds-up-along-the-path.md) | Halving everything you control buys 6.7%. What buys the rest? | `working` |

### Section 2 — `02-dependencies`: what you are committing to
*Every arrow on that diagram is a promise somebody else keeps. Classify them, and decide the failure
behaviour before you need it.*

| Part | Answers | Level |
| --- | --- | --- |
| [2.1 — Hard and soft dependencies](parts/02-dependencies/2.1-hard-and-soft-dependencies.md) | Why is "soft" a property of your code rather than of the dependency? | `foundation` |
| [2.2 — Every dependency is a decision about what happens when it is gone](parts/02-dependencies/2.2-every-dependency-is-a-decision.md) | Five commitments — and the four in the pull request nobody mentions | `working` |
| [2.3 — The dependency that fails slowly](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md) | Why is CPU *low* during this kind of outage? | `production` |

### Section 3 — `03-state`: what the system remembers
*Statelessness is a claim about the process. The state did not vanish; it moved somewhere that now
needs the care.*

| Part | Answers | Level |
| --- | --- | --- |
| [3.1 — "Stateless" is a claim about the process](parts/03-state/3.1-stateless-is-a-claim-about-the-process.md) | Kill the process right now. Is anything lost? | `foundation` |
| [3.2 — Where `pulse`'s state will actually live](parts/03-state/3.2-where-pulse-state-will-live.md) | Four kinds of state, one durable store, and why `/healthz` touches none of it | `working` |
| [3.3 — What you can lose, and what you cannot](parts/03-state/3.3-what-you-can-lose-and-what-you-cannot.md) | Two numbers per store — and the third one nobody writes down | `production` |

### Section 4 — `04-blast-radius`: what breaks when it breaks
*The fault is not the variable you control; the containment is. Map it, then give the map a check it
can fail.*

| Part | Answers | Level |
| --- | --- | --- |
| [4.1 — What a blast radius actually is](parts/04-blast-radius/4.1-what-a-blast-radius-is.md) | Which of the three kinds never appears on an architecture diagram? | `foundation` |
| [4.2 — Drawing the blast-radius map](parts/04-blast-radius/4.2-drawing-the-blast-radius-map.md) | Twelve rows, and the four with no box on the diagram | `working` |
| [4.3 — The map is wrong — making the document go red](parts/04-blast-radius/4.3-the-map-is-wrong.md) | **Give the diagram a check, then break it** — and meet a false positive | `production` |
| [4.4 — The architecture document that survives you](parts/04-blast-radius/4.4-the-architecture-document-that-survives-you.md) | Brochure or handbook — which one are you writing, and for whom? | `production` |

**Each section climbs `foundation → working → production`.**
[4.3](parts/04-blast-radius/4.3-the-map-is-wrong.md) is the deliberate-failure part the depth contract
requires (plan §17.7): you write a consistency check for `docs/ARCHITECTURE.md`, watch it produce a
**false positive** on its first run, fix that, then break the document on purpose and watch it exit
`1`.

---

## §3 Setup — run this

**Stop nothing; start nothing that stays.** No profile runs today (Addendum 02 §4). Three parts start
a short-lived local Python server on loopback — ports **8765**, **8777** and **8788** — and every one
of them is killed within the same command. Nothing is resident at the end of the day.

**No packages are installed today.** `dependencies` stays `[]` in `pyproject.toml`; every experiment
uses the standard library. The first three runtime packages arrive tomorrow.

```bash
# 1 — yesterday's floor is still standing
./o check

# 2 — this day's scratch folder; three parts write scripts into it
./o scaffold 2

# 3 — confirm the three ports today uses are free before you start
netstat -ano | grep -E ":(8765|8777|8788).*LISTENING" || echo "all three ports free"

# 4 — the document you are writing today does not exist yet. Create it empty and commit nothing:
touch docs/ARCHITECTURE.md
```

**Versions in force**, unchanged from Day 0 and verified there on 2026-08-24: git
`2.54.0.windows.1`, uv `0.12.3`, python `3.12.12` under `uv run`, ruff `0.16.4`, pytest `9.1.1`. Two
more observed today while writing, and recorded in `docs/PACKAGES.md`: `curl 8.19.0`, which ships with
Git for Windows, and the fact that `python -m http.server` reports itself as `SimpleHTTP/0.6`.

⚠️ **A Windows behaviour worth knowing before you start** (found while writing
[2.3](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md)): killing a local test server and
starting another produced **two processes listening on the same port**, rather than the *address
already in use* refusal you would get on Linux. Verify with `netstat` rather than trusting a `kill`.

---

## §4 Build brief

Today writes no service code — `pulse/` stays empty until tomorrow. What you produce is **one document
with four sections, one shell check, three scratch scripts and one ADR.**

| File | Explained in | What it is |
| --- | --- | --- |
| `docs/ARCHITECTURE.md` §1 | [1.2](parts/01-the-request-path/1.2-drawing-the-path-for-pulse.md) | **Yours to write** — the request path, as a Mermaid diagram with nine named boxes |
| `docs/ARCHITECTURE.md` §2 | [2.1](parts/02-dependencies/2.1-hard-and-soft-dependencies.md) | **Yours to write** — components, classification per route, and what we do without each |
| `docs/ARCHITECTURE.md` §3 | [3.2](parts/03-state/3.2-where-pulse-state-will-live.md), [3.3](parts/03-state/3.3-what-you-can-lose-and-what-you-cannot.md) | **Yours to write** — state placement, then RPO, RTO and `last tested` |
| `docs/ARCHITECTURE.md` §4 | [4.2](parts/04-blast-radius/4.2-drawing-the-blast-radius-map.md) | **Yours to write** — twelve rows, including four with no box on the diagram |
| `docs/ARCHITECTURE.md` header | [4.4](parts/04-blast-radius/4.4-the-architecture-document-that-survives-you.md) | **Yours to write** — who it is for, what it is not, what the check does not cover |
| `docs/adr/ADR-0005-healthz-checks-the-process-only.md` | [4.4](parts/04-blast-radius/4.4-the-architecture-document-that-survives-you.md) | **Yours to write** — plus its row in `docs/DECISIONS.md` |
| `lab/check_architecture.sh` | [4.3](parts/04-blast-radius/4.3-the-map-is-wrong.md) | **Yours to write** — the check that can go red |
| `lab/budget.py` | [1.3](parts/01-the-request-path/1.3-latency-adds-up-along-the-path.md) | **Yours to write** — the latency budget, and what halving each hop buys |
| `lab/slow_dependency.py` | [2.3](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md) | **Yours to write** — one slow route, one fast one, one shared pool |
| `lab/stateful.py` | [3.1](parts/03-state/3.1-stateless-is-a-claim-about-the-process.md) | **Yours to write** — a counter that a restart forgets |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [2.3](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md), raise the number
  of concurrent slow requests until the `/fast` request's time actually moves. **Write down the
  number.** That is your machine's real concurrency limit, and almost nobody knows theirs.
- `TODO(me)` The `LLM` row in the components table is honestly `hard for /assist` today. Leave it that
  way. Write the sentence that will let Day 129 change it, and say what would have to be true.
- `TODO(me)` Add a **fourth column** to the blast-radius map that today's parts do not give you:
  *what if it is slow rather than down?* Fill it in for `DB`, `INDEX` and `LLM`. Two of the three
  answers will be worse than the "down" answer.
- `TODO(me)` Write `ADR-0005` from [4.4](parts/04-blast-radius/4.4-the-architecture-document-that-survives-you.md)
  in your own words, including a genuine advantage for the option you rejected. If you cannot think of
  one, you have not understood the option yet.
- `TODO(me)` Break `lab/check_architecture.sh` in a *second* way that is not the `CACHE` example —
  something that makes it produce a **false negative**, where the document is wrong and the check is
  green. Record it in `docs/INCIDENTS.md`.
- `TODO(me)` Score the seven handover questions from
  [Day 1, part 3.1](../day-001-what-operations-actually-is/parts/03-the-handover-test/3.1-the-handover-test.md)
  again, now that `docs/ARCHITECTURE.md` exists. Which ones moved?

---

## §5 The check that must be able to fail

Today's check is one you write yourself:
`days/day-002-shape-of-production-system/lab/check_architecture.sh`. It extracts the node identifiers
from the Mermaid block in `docs/ARCHITECTURE.md`, extracts the identifiers from the components table,
and refuses if the two sets differ.

```bash
./days/day-002-shape-of-production-system/lab/check_architecture.sh; echo "exit=$?"
```

**It goes red twice today, and the first time is an accident.** On its first run against a correct
document it reported:

```text
in the diagram, not in the table: LR
exit=1
```

`LR` is the direction word in `flowchart LR`, matched because it is two capital letters. That is a
**false positive**, and it is the most instructive failure a check can have — one is a puzzle, one
every run is a check people learn to ignore, and then the real failure arrives and nobody looks. The
fix is one `grep -v` line, written *after* seeing the failure.

**Then make it go red on purpose.** Add `ASSIST --> CACHE` to the diagram and no row to the table —
exactly what happens when somebody adds a component and updates the picture:

```text
FAIL in the diagram, not in the table: CACHE
exit=1
```

Add the row, run it again, and get:

```text
OK architecture map consistent: 9 components
```

**Three runs, not one** (Principle 11). And read
[4.3](parts/04-blast-radius/4.3-the-map-is-wrong.md)'s closing question before you move on: a green
result here entitles you to believe the document is internally consistent and *nothing at all* about
whether it describes the real system.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline yet; Day 13 builds the first one. |
| Network | one HTTPS request | [1.1](parts/01-the-request-path/1.1-a-request-is-a-path-not-a-function-call.md)'s timing check fetches one JSON document from `pypi.org`. Everything else is loopback. |
| RAM (resident) | **0** at the end | Three short-lived Python servers, a few MB each, all killed within their own command. |
| Disk | a few KB | One Markdown document, one ADR, four scratch scripts. |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). |

Day 2 is the last day with a zero in the *RAM* row. From tomorrow there is a process you deliberately
leave running.

---

## §7 Traps

- **Drawing boxes instead of lines.** The components are the easy part; the arrows are where the
  failures live. A diagram with no arrows crossing a network boundary has not said anything yet
  ([1.2](parts/01-the-request-path/1.2-drawing-the-path-for-pulse.md)).
- **Calling something "soft" with no fallback code.** Soft is a property of a code path that exists
  and has been tested, not of the dependency. Until that path exists the dependency is hard, whatever
  the table says ([2.1](parts/02-dependencies/2.1-hard-and-soft-dependencies.md)).
- **Optimising the hop you can see.** It is nearly always the small one. Look at the budget, find the
  biggest number, work on that ([1.3](parts/01-the-request-path/1.3-latency-adds-up-along-the-path.md)).
- **Assuming a dependency is either up or down.** The third state — up, answering, slow — is the one
  that takes the whole service with it, and CPU will be *low* while it happens
  ([2.3](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md)).
- **Making `/healthz` check the database.** It converts a database outage into a total outage, because
  every instance answers unhealthy at once and none recovers
  ([3.2](parts/03-state/3.2-where-pulse-state-will-live.md), ADR-0005).
- **Filling every cell in the blast-radius map.** Six rows should say *nobody* or *a user tells us*
  today. A map with no gaps on a system with no alerts is a map that is lying
  ([4.2](parts/04-blast-radius/4.2-drawing-the-blast-radius-map.md)).
- **Believing a green check means the document is right.** It means the diagram and the table name the
  same things. Correspondence to reality needs a failure drill
  ([4.3](parts/04-blast-radius/4.3-the-map-is-wrong.md)).
- **Trusting `kill` on Windows.** Two processes can end up listening on one port. Verify with
  `netstat -ano | grep :PORT` — see §3.
- **Leaving `print` unflushed in a server.** Python buffers standard output when it is not a terminal,
  so a redirected server's log appears minutes late or never. `flush=True`, until Day 67 replaces
  `print` entirely ([2.3](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md)).

**Named trap from plan §5.1: trap #2 — *the metric that is not a metric*.** Today is where it is
avoided rather than met. The label set on your latency metric is decided at diagram time: if it
carries the downstream component's name, *"which hop?"* is one query away; if it does not, no amount
of dashboard work recovers the information, because it was never recorded. Day 63 builds the metric;
today decides whether it can answer anything.

---

## §8 Verify before you build

Fetched and observed live on **2026-08-24** while writing this day (Principle 8 — look it up, never
remember it).

| What | Where / how | Why today |
| --- | --- | --- |
| HTTP `503 Service Unavailable` | `rfc-editor.org/rfc/rfc9110.txt`, §15.6.4 — fetched and grepped | the right status for a dependency outage, versus `500` ([2.1](parts/02-dependencies/2.1-hard-and-soft-dependencies.md), [2.2](parts/02-dependencies/2.2-every-dependency-is-a-decision.md)) |
| `curl` version and verbose format | `curl --version` → `8.19.0` | the pasted `-v` output is from this version and differs from older ones ([1.1](parts/01-the-request-path/1.1-a-request-is-a-path-not-a-function-call.md)) |
| `curl -w` timing variables | `curl --help all` and the manual's `--write-out` section | `time_namelookup`, `time_connect`, `time_total` ([1.1](parts/01-the-request-path/1.1-a-request-is-a-path-not-a-function-call.md), [1.3](parts/01-the-request-path/1.3-latency-adds-up-along-the-path.md)) |
| `python -m http.server` reports HTTP/1.0 | ran it, read the response line | the request goes out `1.1` and comes back `1.0`; both ends need not agree ([1.1](parts/01-the-request-path/1.1-a-request-is-a-path-not-a-function-call.md)) |
| two servers can bind one port on Windows | ran two, confirmed with `netstat -ano` | Python's `HTTPServer` sets `allow_reuse_address`; Linux would refuse ([2.3](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md)) |
| `print` is buffered when redirected | redirected a server's output, saw nothing until `flush=True` | ([2.3](parts/02-dependencies/2.3-the-dependency-that-fails-slowly.md)) |
| this repository's installed tree | `uv pip list` → seven packages for two requested | the transitive cost of a dependency ([2.2](parts/02-dependencies/2.2-every-dependency-is-a-decision.md)) |

**Not checked today, deliberately:** anything about FastAPI, Kubernetes, Postgres or any model
provider. None of their symbols are used today, and a note written now would be stale by the day it
matters.

---

## §9 Say it in an interview

> "Before I write a service I draw the request path, because 'the service is slow' isn't actionable —
> it's a claim about one of eight hops and you can't tell which without decomposing it. I did that
> literally last week: one request looked like it took fifty-two seconds, and the DNS and connect
> phases were under a tenth of a second between them, so the obvious first guess would have wasted an
> hour. Then for each thing on the path I write down what the user gets when it's unavailable — a
> worse answer, an honest error, a delayed answer, or a cached one — because if you don't choose, the
> default is that the user waits and then gets a stack trace. The one I care most about is the
> distinction between *down* and *slow*: down costs you a feature, slow costs you the whole service,
> because every waiting caller is holding a thread and the threads run out long before the dependency
> recovers. You can spot it from the outside — CPU flat and low during a total outage means blocked,
> not busy. And I keep a blast-radius table, one row per component, with a column for *how would we
> find out*. On the current system six of twelve rows say 'a user tells us', and I'd rather have that
> written down than have a table that looks complete. Those six rows are the alerting backlog, and
> that's a much better way to arrive at an alert set than alerting on whatever the tooling happens to
> expose."

---

## §10 Done when

Not when you have read all thirteen parts. **When every box in [`CHECKLIST.md`](CHECKLIST.md) is
honestly ticked and `./o check` is green.**

There is no time estimate in this day and there never will be (Principle 17).

```bash
./o done 2
```

---

## §11 Ledger & commit

Paste these before running `./o done 2`. **Use the values you actually observed** (Principle 7).

**`docs/PROGRESS.md`** — append one row:

```text
| 2 | 2026-08-24 | FND-03 | 13 | <hash> | ✅ |
```

Write `pending`, commit, then replace it with the real short hash in a follow-up commit. Nothing in
this repository validates that column, which is exactly why it is your job
([Day 1, part 2.6](../day-001-what-operations-actually-is/parts/02-the-repo-remembers/2.6-breaking-the-memory-on-purpose.md)).

**`docs/PACKAGES.md`** — **two rows**, and neither is a package. Both are observations about the
machine that later days depend on:

```text
| curl | 8.19.0 | 2026-08-24 | 2 | Ships with Git for Windows; the `-v` and `-w` output pasted in Day 2 is from this version. Observed with `curl --version`. |
| windows: port reuse | two listeners on one port | 2026-08-24 | 2 | Python's HTTPServer sets allow_reuse_address; on Windows a second process binds successfully instead of failing with "address already in use". Verify a kill with `netstat -ano`, never by assumption. |
```

**`docs/INCIDENTS.md`** — **two rows minimum.** The first is the false positive from
[4.3](parts/04-blast-radius/4.3-the-map-is-wrong.md), and its *first symptom* column is written before
you knew the cause:

```text
| 13 | 2026-08-24 | 2 | Ran the new lab/check_architecture.sh for the first time against a correct docs/ARCHITECTURE.md | `in the diagram, not in the table: LR` / exit=1 | `LR` is the direction word in `flowchart LR`, matched by the all-caps identifier pattern. The check was right that the lists differed and wrong about why — a false positive on run one | added `grep -v -E '^(```\|\s*flowchart\|\s*subgraph\|\s*end\|\s*style)'` before extracting identifiers | Nothing automatic. Recorded the boundary: the check matches by convention (all caps), so a node named `Api` is silently ignored — an intentional gap, now written down |
| 14 | 2026-08-24 | 2 | Added `ASSIST --> CACHE` to the diagram with no row in the components table | `FAIL in the diagram, not in the table: CACHE` / exit=1 | the check working as designed; a component added to the picture and not to the description | added the `CACHE` row | Nothing needed — this is the gate going red on purpose (Principle 11). Noted that the check verifies internal consistency only and would pass on a document that is wrong about the whole system |
```

**`docs/DECISIONS.md`** — **one new row**, for the ADR you write today:

```text
| [ADR-0005](adr/ADR-0005-healthz-checks-the-process-only.md) | 2026-08-24 | accepted | `/healthz` reports only that the process can respond; dependency status gets a separate endpoint when a supervisor exists to consume it (Day 41). |
```

**Commit message:**

```text
day 002: the shape of a production system — closes FND-03

Draws pulse before pulse exists: the request path as nine named boxes,
each dependency classified per route with the behaviour we owe the user
when it is gone, state placed so exactly one store is durable, and a
blast-radius map whose most valuable column is "how would we find out".

Six of twelve rows in that map answer "nobody" or "a user tells us".
Recorded as gaps with the days that close them rather than filled in
optimistically.

Gives the document a consistency check that can refuse, and breaks it
twice — once by accident, on a false positive that matched the diagram's
direction keyword, and once on purpose.
```
