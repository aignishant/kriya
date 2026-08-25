---
day: 7
phase: 1
phase_name: "The production mental model and the machine"
title: "Networking for operators"
ids: [FND-08, FND-09]
principles: [1, 2, 4, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18]
kind: lab
plan_version: "v1.1.0"
parts: 17
generated: "2026-08-24"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 7 — Networking for operators — ports, sockets, DNS, TCP, and the timeout that saves the system

> **Yesterday (Day 6):** memory and processor — the numbers that lie, the limits that kill versus the
> limits that merely slow you down, and a service OOM-killed with a request in flight while every signal
> you owned stayed green.
> **Today:** how one program reaches another — the address, the name, the connection — and then the single
> most consequential number in distributed systems: how long you are willing to wait.
> **Tomorrow (Day 8):** HTTP and TLS in production — status codes that mean something, keep-alive, and the
> certificate that expires on a Sunday.

---

## §1 Where we are

Everything so far has happened inside one machine. A process, its memory, its files, its share of the
processor. Today a second participant appears, and it changes the character of every failure you have
seen.

Here is the difference in one image. If you ask a colleague at the next desk a question and they do not
reply, you look up. You can see whether they are thinking, or have left the room, or did not hear you.
Now put them behind a closed door with a note slot. You post the question. Nothing comes back.

**You cannot tell the difference between: they are still writing the answer; they left an hour ago; the
door is jammed; there was never anybody in there.** Every one of those looks precisely the same from your
side — silence — and no amount of waiting distinguishes them. This is not a shortcoming of any particular
technology. It is what a network *is*: the only thing you ever observe is what came back, and nothing
coming back is not an observation.

Yesterday's failures had a body to examine. A process was killed and the kernel wrote it down. Today's
failures leave nothing at all: the connection looks perfect, the counters do not move, no error is
raised, and the request is simply still open.

So the day builds up in four layers and then puts them together. **Where does a message go** — an address
picks a machine, a port picks a program, and only one program can hold a port. **How does a name become
an address** — a whole separate network conversation that happens before yours and that most people
forget exists until it is the broken thing. **What is a connection** — a state machine, whose states you
can read, and which has an unpleasant property: it can be perfectly healthy on your side and gone on the
other, with no way to tell except by asking and waiting.

And then the number. Because every one of those failures ends in the same place — **you asked, and
nothing came back** — the only defence is a decision about how long you will wait. That decision is
usually made for you by a library default, and in most libraries the default is *forever*.

The day ends by driving that home on `pulse`. A copy of your own service, pointed at a dependency that
accepts connections and never answers, with the timeout left unset. **Forty requests, and the whole
service is gone — including the health check** — while the process is alive, the processor is idle, the
memory is flat, the error rate is zero and the last thing in the log is a success.

**That is the second time this week your service has died with every signal green**, by a completely
different mechanism, and noticing that pattern is more valuable than either drill on its own.

---

## §2 The map

**Section 1 — `01-addresses-and-ports`.** Where a message goes and who is entitled to receive it. The
naming layer: what a port is, what identifies a connection, which interfaces you accept on, and the four
distinct causes of the first networking error everybody meets.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A port is a doorway, not a place](parts/01-addresses-and-ports/1.1-a-port-is-a-doorway-not-a-place.md) | two programs, one port — why can only one of them have it? | foundation |
| 1.2 | [The socket and the four-tuple](parts/01-addresses-and-ports/1.2-the-socket-and-the-four-tuple.md) | one listening port, ten thousand clients — how does nobody get someone else's data? | foundation |
| 1.3 | [Binding `127.0.0.1` versus `0.0.0.0`](parts/01-addresses-and-ports/1.3-binding-127-0-0-1-versus-0-0-0-0.md) | it works on my machine and not from the container — which one line explains it? | working |
| 1.4 | [The port that was already in use](parts/01-addresses-and-ports/1.4-the-port-that-was-already-in-use.md) | `address already in use` — four causes, four fixes, which is yours? | working |

**Section 2 — `02-dns`.** How a name becomes an address. A separate service, over a separate protocol,
that runs before your request starts and is invisible in every application log you own.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [What resolution actually does](parts/02-dns/2.1-what-resolution-actually-does.md) | what happens between typing a hostname and the first byte being sent? | foundation |
| 2.2 | [Records, TTL, and the cache you do not control](parts/02-dns/2.2-records-ttl-and-the-cache-you-do-not-control.md) | you changed the record — when does the last client see it? | working |
| 2.3 | [The DNS failure that looks like a timeout](parts/02-dns/2.3-the-dns-failure-that-looks-like-a-timeout.md) | every request in the system got slower by the same amount — where do you look first? | production |

**Section 3 — `03-tcp`.** What a connection actually is, and the states it gets stuck in. The layer where
the difference between *slow*, *queued* and *dead* is decided — and where two of them are indistinguishable
from your side.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [The handshake and the connection states](parts/03-tcp/3.1-the-handshake-and-the-connection-states.md) | what is this socket doing, and which column tells you? | foundation |
| 3.2 | [The accept queue and the backlog](parts/03-tcp/3.2-the-accept-queue-and-the-backlog.md) | the application is stalled and clients see no error — where are their requests? | working |
| 3.3 | [`TIME_WAIT` and the ports you ran out of](parts/03-tcp/3.3-time-wait-and-the-ports-you-ran-out-of.md) | harmless on a server, fatal on a client — what changed? | production |
| 3.4 | [The connection that is open and dead](parts/03-tcp/3.4-the-connection-that-is-open-and-dead.md) | `ESTABLISHED` on your side, gone on theirs — how do you ever find out? | production |

**Section 4 — `04-timeouts`.** The decision. How long you are prepared to wait, what a phase timeout
bounds, and why four of them still do not bound a request.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [A timeout is a decision, not a safety net](parts/04-timeouts/4.1-a-timeout-is-a-decision-not-a-safety-net.md) | "we didn't set a timeout" — what did you actually agree to? | foundation |
| 4.2 | [The four timeouts of one HTTP call](parts/04-timeouts/4.2-the-four-timeouts-of-one-http-call.md) | you set a timeout and it never fired — which of the four did you set? | working |
| 4.3 | [The deadline that bounds the whole call](parts/04-timeouts/4.3-the-deadline-that-bounds-the-whole-call.md) | a 3-second timeout allowed a 15-second request and nothing malfunctioned — how? | production |

**Section 5 — `05-the-two-together`.** The network facts and the timeout, combined at the scale of a
system rather than a call. One request crossing several services, the retry that arrives when the system
can least carry it, and the drill that takes `pulse` down without producing a single error.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 5.1 | [The timeout budget down the request path](parts/05-the-two-together/5.1-the-timeout-budget-down-the-request-path.md) | which service in a five-hop path should have the smallest timeout? | production |
| 5.2 | [Retries that turn a blip into an outage](parts/05-the-two-together/5.2-retries-that-turn-a-blip-into-an-outage.md) | three layers, three attempts each — is that nine requests or twenty-seven? | production |
| 5.3 | [Hanging `pulse` on purpose](parts/05-the-two-together/5.3-hanging-pulse-on-purpose.md) | how many slow requests separate a healthy service from no service at all? | production |

**📄 The research — `papers/`.** The retry ladder 5.2 builds is not a convention somebody picked;
it is a published result, and this curriculum teaches a paper the way it teaches everything else — in
a document of its own, with a demo you run (plan §17.4.2). Read it after section 5.

| Paper | What it settles | Level |
| --- | --- | --- |
| [Congestion Avoidance and Control](papers/congestion-avoidance-and-control.md) (1988) | why the wait *doubles* rather than growing by a constant — and what the paper never said about jitter | production |

---

## §3 Setup — run this

**Stop first.** Everything from Day 6 holds memory or a core, and today's measurements are about *time*,
which is the quantity most easily contaminated by a busy machine. Close the browser.

**Profile:** `core` (Addendum 02 §4) — that is `pulse` alone, since Postgres does not arrive until Day 21.
Roughly 60 MB. **Today adds a handful of tiny lab servers on localhost**, none larger than a Python
interpreter, and the day never needs two profiles at once.

```bash
# 1 — nothing from Day 6 survives. Today's numbers are timings; a busy core ruins them.
pgrep -af 'burn|allocate|shared|mapshare|hungry|uvicorn' || echo "nothing running"

# 2 — this day claims a lot of ports. Find out now, not mid-experiment.
netstat -ano | grep -E ':80(0[0-9]|1[0-5]).*LISTENING' || echo "8000-8015 all free"

# 3 — the tools this day reads output from
for t in curl netstat nslookup; do command -v "$t" >/dev/null && echo "ok      $t" || echo "MISSING $t"; done

# 4 — which resolver this machine will actually use (section 2 depends on it)
nslookup example.com 2>&1 | head -4

# 5 — the library the timeout sections use. NOTE THE NAME.
uv run python -c "import httpx2; print('httpx2', httpx2.__version__)"

# 6 — gate green, tree clean, before you break anything
./o check && git status --short

# 7 — this day's scratch folder
./o scaffold 7
```

⚠️ **Step 2 matters more than it looks.** Sixteen ports are used across the day and several parts start
background servers. A port left occupied by a program you forgot produces `address already in use` — which
is [1.4](parts/01-addresses-and-ports/1.4-the-port-that-was-already-in-use.md)'s subject, so the first
time it happens it is a lesson, and the fifth time it is an evening. **Every part that starts a server
ends by stopping it; do not skip those lines.**

⚠️ **Step 5 names a trap.** The package is `httpx2` and it imports as **`httpx2`**. `import httpx` in this
environment raises `ModuleNotFoundError: No module named 'httpx'`. Day 3 installed it as a dev dependency
([Day 3](../day-003-pulse-v0/LESSON.md), §3) precisely because `starlette.testclient` deprecates plain
`httpx`, and today is the first day that calls it directly rather than through the test client.

⚠️ **`pkill -f` is unreliable from Git Bash on Windows.** Several parts use it to stop background servers,
and it will sometimes report success while leaving the process running — which then shows up as a port
conflict in the next part. **Confirm with `netstat`, every time**, and fall back to
`taskkill //F //IM python.exe` when you have nothing else in Python running. This is the fifth consecutive
day this machine has produced an environmental gap and it belongs in `docs/INCIDENTS.md` with the others.

**No packages are added today. Fourth day running.** Everything this day uses is either the standard
library or already installed.

---

## §4 Build brief

No project code. `pulse` is not modified today — **not one line**. The one file that resembles it,
`lab/hangy.py`, is a drill copy that is deleted at the end of the day, exactly as
[Day 6's `hungry.py`](../day-006-resources-and-the-oom-killer/parts/04-the-oom-killer/4.3-oom-killing-pulse-on-purpose.md)
was.

| File | Explained in | What it is |
| --- | --- | --- |
| `lab/claim_port.py` | [1.1](parts/01-addresses-and-ports/1.1-a-port-is-a-doorway-not-a-place.md) | **Yours to write** — hold a port, and watch the second attempt fail |
| `lab/hold_conns.py` | [1.2](parts/01-addresses-and-ports/1.2-the-socket-and-the-four-tuple.md) | **Yours to write** — many connections to one port; read the four-tuples |
| `lab/no_reuse.py` | [1.4](parts/01-addresses-and-ports/1.4-the-port-that-was-already-in-use.md) | **Yours to write** — bind without `SO_REUSEADDR` and meet cause three |
| `lab/slow_resolver.py` | [2.3](parts/02-dns/2.3-the-dns-failure-that-looks-like-a-timeout.md) | **Yours to write** — a resolver that never answers |
| `lab/no_close.py` | [3.1](parts/03-tcp/3.1-the-handshake-and-the-connection-states.md) | **Yours to write** — leave a socket unclosed and find `CLOSE_WAIT` |
| `lab/tiny_backlog.py` | [3.2](parts/03-tcp/3.2-the-accept-queue-and-the-backlog.md) | **Yours to write** — `listen(1)` and a queue nobody drains |
| `lab/keepalive.py` · `lab/silent_peer.py` | [3.4](parts/03-tcp/3.4-the-connection-that-is-open-and-dead.md) | **Yours to write** — the connection that is open and dead |
| `lab/no_timeout.py` · `lab/with_timeout.py` | [4.1](parts/04-timeouts/4.1-a-timeout-is-a-decision-not-a-safety-net.md) | **Yours to write** — the same hang, decided two ways |
| `lab/four_timeouts.py` · `lab/dribble.py` | [4.2](parts/04-timeouts/4.2-the-four-timeouts-of-one-http-call.md) | **Yours to write** — fire each of the four, then evade all of them |
| `lab/deadline.py` | [4.3](parts/04-timeouts/4.3-the-deadline-that-bounds-the-whole-call.md) | **Yours to write** — phase timeouts, then a real bound |
| `lab/hop.py` | [5.1](parts/05-the-two-together/5.1-the-timeout-budget-down-the-request-path.md) | **Yours to write** — one hop, two policies, three copies |
| `lab/counter.py` · `lab/retry_client.py` | [5.2](parts/05-the-two-together/5.2-retries-that-turn-a-blip-into-an-outage.md) | **Yours to write** — count what a retry policy actually sends |
| `lab/blackhole.py` · `lab/hangy.py` | [5.3](parts/05-the-two-together/5.3-hanging-pulse-on-purpose.md) | **Yours to write** — the day's deliberate failure |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — four measurement rows |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — three rows, first symptom before cause |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.3](parts/01-addresses-and-ports/1.3-binding-127-0-0-1-versus-0-0-0-0.md), start `pulse`
  on `127.0.0.1` and then on `0.0.0.0`, and reach it from a second terminal each way. **Write down which
  one your Day 22 container will need and why that is not a security regression.**
- `TODO(me)` In [2.2](parts/02-dns/2.2-records-ttl-and-the-cache-you-do-not-control.md), look up the TTL of
  a domain you use, and work out the earliest and the latest moment a change would reach everybody.
  **Two numbers, and the gap between them is the answer.**
- `TODO(me)` In [3.3](parts/03-tcp/3.3-time-wait-and-the-ports-you-ran-out-of.md), count this machine's
  ephemeral port range and divide by the `TIME_WAIT` duration. **That quotient is the maximum sustainable
  rate of new connections from one client to one server**, and Day 147's evaluation loop will run into it.
- `TODO(me)` In [4.2](parts/04-timeouts/4.2-the-four-timeouts-of-one-http-call.md), find a client library
  you use outside this project and answer: how many separately-configurable timeouts does it have, what
  are their defaults, and does it have a total? **Most answers are worse than you expect.**
- `TODO(me)` In [5.1](parts/05-the-two-together/5.1-the-timeout-budget-down-the-request-path.md), make a
  hop **refuse** on purpose by shrinking the budget below its own cost. The propagation code that only
  runs during an incident is the code you must exercise deliberately.
- `TODO(me)` In [5.2](parts/05-the-two-together/5.2-retries-that-turn-a-blip-into-an-outage.md), predict
  the arrival count for 3 layers × 3 attempts **before** running it, and write your prediction down. If
  you guessed nine, that error is the whole part.
- `TODO(me)` Do the [5.3](parts/05-the-two-together/5.3-hanging-pulse-on-purpose.md) drill and record
  **all six** observations: `/healthz` before, `/healthz` during, the blackhole's connection count, the
  processor reading, the error count, and the last application log line. Then run it at 39 and confirm the
  service survives.
- `TODO(me)` Put Day 6's OOM drill and today's exhaustion drill side by side and write **one paragraph**
  on what they have in common. Two totally different mechanisms produced the same dashboard. **That
  paragraph is the beginning of Day 62's argument for what to actually measure.**
- `TODO(me)` Delete every lab file, confirm with `netstat` that no server survives on 8000–8015, and prove
  the tree is clean with `git status --short`.

---

## §5 The check that must be able to fail

Two red gates. **Both are red in the sense that the system fails while every instrument reports normal** —
which is the same shape as Day 6's, arrived at from the opposite direction.

**Gate one: forty requests remove the service, and nothing reports an error.**

```bash
cd days/day-007-networking-for-operators
uv run python lab/blackhole.py 8015 & BH=$!
uv run uvicorn --app-dir lab hangy:app --host 127.0.0.1 --port 8010 --log-level warning & UV=$!
sleep 4
curl -sS -m 3 -o /dev/null -w 'before: healthz http=%{http_code} total=%{time_total}s exit=%{exitcode}\n' http://127.0.0.1:8010/healthz
uv run python -c "
import concurrent.futures, time, httpx2
def hit(i):
    try: httpx2.post('http://127.0.0.1:8010/predict', json={'text':'x'}, timeout=httpx2.Timeout(60.0))
    except Exception: pass
pool = concurrent.futures.ThreadPoolExecutor(max_workers=40)
[pool.submit(hit, i) for i in range(40)]
time.sleep(6)
" & sleep 9
curl -sS -m 8 -o /dev/null -w 'during: healthz http=%{http_code} total=%{time_total}s exit=%{exitcode}\n' http://127.0.0.1:8010/healthz
kill "$UV" "$BH" 2>/dev/null
```

| Observation | Expected |
| --- | --- |
| `/healthz` before | `http=200`, a few tens of milliseconds |
| `/healthz` during | **`http=000` `exit=28`** — no HTTP response at all |
| blackhole's own count | **`holding 40 connection(s)`** |
| processor | **≈0%** |
| errors anywhere | **0** |
| last application log line | **a success** |

**If `/healthz` returns `200` during the load, the gate has not gone red** and you have measured nothing.
Check the blackhole's count: fewer than forty means the requests were not all in flight together. **Then
set `TIMEOUT=2` and run it again**: the same forty requests become forty `500`s and `/healthz` answers in
about two milliseconds. That is the gate going green — and note carefully what green bought you, because
the upstream is exactly as broken in both runs.

**Gate two: one click, twenty-seven requests.**

```bash
cd days/day-007-networking-for-operators
uv run python lab/counter.py 8014 25 & sleep 2
uv run python lab/retry_client.py http://127.0.0.1:8014/ 3 3 nojitter 1
wait
```

| Layers × attempts | Expected arrivals |
| --- | --- |
| 1 × 1 | 1 |
| 3 × 3 | **27** |

**The gate is that the number is 27 and not 9.** If you get 9, the layers are adding rather than nesting
and the client is not modelling a stack. Run it at `1 1` first — **if the control does not print exactly
`1`, something else on this machine is talking to port 8014** and every number after it is contaminated.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline until Day 13. |
| **External network** | **a handful of DNS lookups** | Section 2 only, and `nslookup` against public resolvers. **Every other byte in this day is to `127.0.0.1`.** |
| RAM | **~400 MB peak** | One uvicorn (~60 MB) plus up to five small Python servers and a load generator. All returned at exit. |
| Processor | **negligible** | The day's characteristic reading is **0%**, on a service that is completely unresponsive. That is the finding, not an aside. |
| Disk | **0** | Three small log files in `/tmp`, removed by the cleanup steps. |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). |

**The row worth reading twice is Processor.** Yesterday the machine was the constraint and you were told to
check your headroom before starting. Today the machine is almost idle throughout, including at the exact
moment the service is dead. **Nothing you can measure about resource consumption will tell you today's
system is broken.**

⚠️ **One line in this day can cost you something real, and it is not on this machine.**
[5.2](parts/05-the-two-together/5.2-retries-that-turn-a-blip-into-an-outage.md) builds a load generator
that sends thirty synchronised clients with four attempts each. **Pointed at anything you do not own it is
a small denial-of-service; pointed at a free-tier API it exhausts a quota**, which Addendum 01 treats as
the one genuinely irreversible resource in this curriculum. Every command in that part targets
`127.0.0.1`. Keep it that way.

---

## §7 Traps

**A port is held by a process, not by a program.** Kill the process and the port is free; kill the wrong
one and you have not fixed anything. `address already in use` has four distinct causes and the skill is
naming which one in a single command, not restarting things until it works.
Part [1.4](parts/01-addresses-and-ports/1.4-the-port-that-was-already-in-use.md).

**`127.0.0.1` is not `0.0.0.0` and the difference is invisible until something else needs to reach you.**
Everything works from your own terminal either way, which is precisely why this surfaces on the day you
containerise. Part [1.3](parts/01-addresses-and-ports/1.3-binding-127-0-0-1-versus-0-0-0-0.md).

**DNS happens before your request and appears in none of your logs.** A resolver that answers wrongly
fails loudly; a resolver that does not answer at all adds its timeout to *every* request in the system and
looks exactly like the destination being slow.
Part [2.3](parts/02-dns/2.3-the-dns-failure-that-looks-like-a-timeout.md).

**A TTL is a lower bound on propagation, never an upper one.** Caches you have never heard of will ignore
it. Plan a change around the longest plausible time, not the number in the record.
Part [2.2](parts/02-dns/2.2-records-ttl-and-the-cache-you-do-not-control.md).

**`ESTABLISHED` means the kernel believes there is a connection, not that anybody is listening at the far
end.** An idle TCP connection sends nothing, so a peer that vanished leaves no trace — and the only way to
find out is to send a request and wait, which is exactly the operation you were trying to protect.
Part [3.4](parts/03-tcp/3.4-the-connection-that-is-open-and-dead.md).

**`TIME_WAIT` is harmless on a server and fatal on a client.** The same mechanism, the opposite
consequence, because the client is the side that runs out of ephemeral ports. Reusing connections is not
an optimisation; it is what stops this.
Part [3.3](parts/03-tcp/3.3-time-wait-and-the-ports-you-ran-out-of.md).

**Setting a connect timeout is not setting a timeout.** Connecting to a hung server succeeds instantly, so
the phase people bound is the one that almost never fires. Set all four, or set a total.
Part [4.2](parts/04-timeouts/4.2-the-four-timeouts-of-one-http-call.md).

**A read timeout measures inactivity, not elapsed time.** A peer sending one byte at a time never trips a
five-second read timeout and can hold a worker indefinitely. **The four phase timeouts do not sum to a
bound on the request.** Part [4.3](parts/04-timeouts/4.3-the-deadline-that-bounds-the-whole-call.md).

**A timeout tells you that you stopped waiting. It does not tell you the operation did not happen.** Any
retry after one has to be idempotent, or it is a decision to accept an unknown outcome — which is how
customers get charged twice.
Parts [4.1](parts/04-timeouts/4.1-a-timeout-is-a-decision-not-a-safety-net.md) and
[5.2](parts/05-the-two-together/5.2-retries-that-turn-a-blip-into-an-outage.md).

**Retries at different layers multiply, they do not add.** Three layers trying three times each is
twenty-seven requests at the bottom, and nobody wrote twenty-seven — it emerges from a stack no single
repository can see. Part [5.2](parts/05-the-two-together/5.2-retries-that-turn-a-blip-into-an-outage.md).

**The package is `httpx2` and it imports as `httpx2`.** `import httpx` fails in this environment. It is
the day's cheapest possible mistake and it costs a confusing traceback in the middle of an experiment.
§3, step 5.

**The named trap from plan §5.1 that this day touches:** *trap 4 — the autonomy with no brake.* The plan
defines it as *"a capability without a bound, a budget, a timeout or a kill switch"*, and today is the
first time all four words appear literally. An outbound call with no timeout is a capability with no
brake, and its blast radius is not the call — it is **your entire service**, because forty of them take
the health check with them. **Principle 13 in its plainest form: the ability to call another service
arrives with the obligation to bound the call, in the same commit.**
Part [5.3](parts/05-the-two-together/5.3-hanging-pulse-on-purpose.md).

---

## §8 Verify before you build

Fetched on **2026-08-24**, not recalled:

| Page | Used for |
| --- | --- |
| `python-httpx.org/advanced/timeouts/` | the four timeout classes and their exact definitions, the 5-second default, and the confirmation that **no total timeout exists** — all quoted verbatim in 4.2 and 4.3 |
| `docs.python.org/3.12/library/asyncio-task.html` | `asyncio.timeout()` and `asyncio.timeout_at()` — added in 3.11, `when` is *"an absolute time … as measured by the event loop's clock"*, `TimeoutError` is what it raises |
| `fastapi.tiangolo.com/async/` | *"When you declare a path operation function with normal `def` … it is run in an external threadpool"* — quoted verbatim in 5.3 |
| `anyio.readthedocs.io/en/stable/threads.html` | the default worker thread limiter of **40**, and `current_default_thread_limiter()` — quoted verbatim in 5.3, and confirmed by running it |
| `grpc.io/docs/guides/deadlines/` | deadline versus timeout, and why gRPC transmits a remaining duration rather than an instant — quoted verbatim in 4.3 and 5.1 |
| `rfc-editor.org/rfc/rfc9110` §9.2.2, §10.2.3 | the definitions of *idempotent* and of `Retry-After`, including the ABNF — quoted verbatim in 5.2 |
| `sre.google/sre-book/addressing-cascading-failures/` | retry amplification as a *product*, the retry budget, and *"always use randomized exponential backoff"* — quoted verbatim in 5.2 |
| Day 4's and Day 6's fetched pages | exit codes, process states, and `time.monotonic()` |

**📄 The paper this day teaches**, read in full on **2026-08-25** and taught in
[`papers/congestion-avoidance-and-control.md`](papers/congestion-avoidance-and-control.md):

| Slug | Title | Identifier | Read |
| --- | --- | --- | --- |
| `congestion-avoidance-and-control` | *Congestion Avoidance and Control* | Proceedings of ACM SIGCOMM 1988; copy at `https://ee.lbl.gov/papers/congavoid.pdf` | 2026-08-25 |

⚠️ **Two things in this day are environment-dependent and are flagged where they appear.** The AnyIO
limiter of 40 is a **default**, so 5.3's first step reads it live rather than trusting the number — if
yours differs, every count in that part shifts with it. And `netstat` output formatting differs between
Windows and Linux; the parts show what this machine printed, so **read the columns, not the byte
offsets**, and expect `ss -tan` to be the tool once WSL2 arrives on Day 21.

---

## §9 Say it in an interview

*"The thing that changed how I debug was realising that a network gives you exactly one observation —
what came back — and that nothing coming back is not an observation. Slow, queued, hung and gone all look
identical from the caller's side, and that's not a gap in the tooling, it's what a network is. So the
whole discipline is about converting silence into something you can act on, and the only instrument for
that is a timeout, because it's the one thing that turns 'no answer yet' into an event.*

*"What I'd want to be judged on is knowing that a timeout isn't one number. An HTTP call has at least four
separately-bounded phases, and the one people set is connect — which is nearly useless, because connecting
to a hung server succeeds instantly. The one that matters is read, and even that is an inactivity timeout
rather than a total: I've watched a three-second timeout permit a fifteen-second request against a server
sending one byte a second, with nothing malfunctioning. Bounding a request needs a deadline over the whole
thing, and that deadline has to travel with the request across services — each hop getting what's left
after the one above it, not a fresh clock. I built a three-hop chain to see it: with flat ten-second
timeouts the client gave up at five seconds and the chain kept working until eleven, three green services
producing an answer that arrived at a closed socket. With the deadline propagated, the deepest hop refused
before starting and the caller got a 504 in just over a second.*

*"The failure that taught me the most was the one with no symptoms. I pointed a copy of my service at a
dependency that accepts connections and never answers, and left the timeout unset. FastAPI runs `def`
endpoints in AnyIO's threadpool, which defaults to forty — so at forty concurrent requests the service was
completely unreachable, health check included, while the process was alive, the processor was at zero, the
memory was flat, the error rate was zero and the last log line was a success. Six accurate signals and a
dead service. Setting a timeout didn't fix anything — the upstream was just as broken — it converted an
invisible total outage into forty visible errors on one code path. That's the trade, and I'd rather state
it that way than pretend a timeout is a repair. The signal I'd actually alert on is in-flight request
count and the age of the oldest one, because an oldest-request age above my longest configured timeout can
only mean something is unbounded."*

---

## §10 Done when

`days/day-007-networking-for-operators/CHECKLIST.md` has no unticked boxes, and `./o done 7` refuses to
commit until that is true.

Done is defined by understanding and green checks, never by elapsed time. Specifically: you can go from
`address already in use` to the owning process in one command; you can look at a `netstat` line and say
what that connection is doing; you can name which of the four timeouts fired and why the other three did
not; you have watched a bounded timeout permit an unbounded request; you have taken your own service down
with forty requests and confirmed that every signal stayed green — and **every server you started is
confirmed stopped**, because today's leftovers hold ports you will need tomorrow.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append this row verbatim, replacing the commit hash with your own after
committing:

```text
| 7 | 2026-08-24 | FND-08, FND-09 | 17 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — no package rows today. Four measurement rows:

```text
| machine: ephemeral port range | <low>-<high> (<n> ports) | 2026-08-24 | 7 | From Day 7 part 3.3. Divided by the TIME_WAIT duration, this is the ceiling on new connections per second from one client to one server. Day 147's evaluation loop runs into it. |
| machine: default resolver | <address from §3 step 4> | 2026-08-24 | 7 | Which server answers this machine's DNS. Day 22's container will use a different one, and Day 37's cluster a third; this is the "before". |
| httpx2 | <version from §3 step 5> | 2026-08-24 | 7 | Confirmed, not added — Day 3 installed it. **Imports as `httpx2`, not `httpx`.** First day it is called directly rather than through the test client. |
| anyio: default thread limiter | <total_tokens from part 5.3> | 2026-08-24 | 7 | **The concurrency at which `pulse` stops answering anything, health check included.** A transitive default nobody chose. Day 41's probes and Day 44's autoscaling both depend on this number. |
```

**`docs/INCIDENTS.md`** — three rows, and **write the first symptom before you investigate**:

```text
| 20 | 2026-08-24 | 7 | Exhausted `pulse`'s worker pool with 40 hung requests, part 5.3 | <what curl printed for /healthz during the load, verbatim, including http code and exit> | <what you found> | <smallest fix> | <what you changed so it cannot happen silently again> |
| 21 | 2026-08-24 | 7 | One user action produced 27 requests at the bottom of a 3-layer retry stack, part 5.2 | <the counter's total, and your prediction before running it> | Retries at different layers multiply rather than add; nobody configured 27 | none — the finding is the arithmetic | Noted that no single repository can show this, so it has to be counted on a whiteboard |
| 22 | 2026-08-24 | 7 | Environmental — `pkill -f` reported success while leaving a background server holding its port | <the netstat line that proved it> | Git Bash over Windows does not reliably signal processes it started in the background | `taskkill //F //IM python.exe` | **Fifth consecutive day recording a diagnostic gap. Link this row to Day 6 row 19 and Day 5 row 16**, and make Day 21 close all of them |
```

⚠️ **Row 22 is the fifth of its kind.** Day 6's row 19 already linked four; **link this one to that
chain.** A gap recorded five times with a named closing day is a finding with an owner, and Day 21 stops
being a setup chore.

**`docs/DECISIONS.md`** — an ADR is worth writing **if** you reached a conclusion on where retries belong.
*"Retries live only at the gateway; service-to-service clients do not retry, because attempts multiply
across layers and no single team can see the product"* is exactly the shape of a decision that is
expensive to reverse, invisible in any one repository, and non-obvious to a stranger — and Day 46 will
implement whatever you decide.

**The commit:**

```text
day 007: networking for operators — ports, DNS, TCP and the timeout — closes FND-08, FND-09
```
