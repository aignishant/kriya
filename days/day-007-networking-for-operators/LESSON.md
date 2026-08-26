---
day: 7
phase: 1
phase_name: "The production mental model and the machine"
title: "Networking for operators"
ids: [FND-08, FND-09]
principles: [1, 2, 4, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18]
kind: lab
plan_version: "v1.2.0"
parts: 18
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 7 — Networking for operators — ports, sockets, DNS, TCP, and the timeout that saves the system

> **Yesterday (Day 6):** the two resources that are consumed rather than stored, and the moment the kernel
> chose one of your processes and killed it with a signal nothing could catch.
> **Today:** the resource that is not on your machine at all. How a name becomes an address, how a
> connection is established, and the one decision — how long to wait — that determines whether a slow
> dependency inconveniences your service or destroys it.
> **Tomorrow (Day 8):** HTTP and TLS in production — status codes that mean something, keep-alive, and the
> certificate that expires on a Sunday.

---

## §1 Where we are

Yesterday's failures were all *local*. A process was killed, and the kernel wrote a line about it. The
evidence was on the machine, even when it was in a file your service could not reach.

Today nothing is local, and that changes the character of every failure on this page.

Start with the plainest version. You type a name. Somewhere between typing it and receiving an answer,
a file is consulted, a cache is consulted, a query crosses the internet to a server you did not choose, a
list of eight addresses comes back in an order somebody else decided, three packets are exchanged with a
machine on another continent, and only then does your request begin. **Not one step of that is in your
code.** Every one can fail. Most of them can be slow instead of failing, which is worse.

The day divides into two halves, and the join between them is the point.

**The first half is identification.** An address says which machine and a port says which program, and
those are two questions with two failure modes that look identical from outside. A name is not an address,
so there is a lookup step in front of everything, run by machinery you do not own, which can hand two
clients different answers and be correct both times. Then the handshake: three packets, one round trip, and
a connection that can be fully established while your application is deadlocked and unaware.

**The second half is waiting.** Because here is the thing the first half keeps producing: **most network
failures are not errors.** A dropped packet is silence. A wedged server is silence. A resolver that does
not answer is silence. And silence has no duration of its own — it lasts exactly as long as somebody is
willing to wait, and the default in nearly every library is *for ever*.

So the day ends where the title says. You will point a service with four workers at a dependency that
accepts connections and never replies, and watch it die in about four seconds. The processor will be idle.
Memory flat. Error rate zero — because nothing failed. The latency graph unchanged, because a request that
never completes is never recorded. And a TCP port check will report the service healthy throughout, in
0.0 milliseconds, because the kernel completes handshakes without asking the application anything.

**Four of your five signals will be green.** That is the second consecutive day whose headline failure is
defined by the absence of evidence, and it is not a coincidence — it is what production failure mostly
looks like.

Then the two things that make it survivable: a deadline that travels down the chain instead of a timeout
each service invents for itself, and the understanding that retries are load aimed at something that has
just proved it cannot cope.

---

## §2 The map

**Section 1 — `01-the-address`.** What identifies a destination, what identifies a conversation, and the
first deliberate failure.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [An address and a port are two different questions](parts/01-the-address/1.1-an-address-and-a-port-are-two-questions.md) | the parcel reached the building — why is that not enough? | foundation |
| 1.2 | [The socket and the four-tuple](parts/01-the-address/1.2-the-socket-and-the-four-tuple.md) | one port, ten thousand connections — how are none confused? | foundation |
| 1.3 | [Binding `127.0.0.1` versus `0.0.0.0`](parts/01-the-address/1.3-binding-127-0-0-1-versus-0-0-0-0.md) | it works locally and nothing else can reach it — which one did you choose? | working |
| 1.4 | [The port that was already in use](parts/01-the-address/1.4-the-port-that-was-already-in-use.md) | the port is taken and `ps` shows nothing — what is holding it? | working |

**Section 2 — `02-names`.** The lookup step in front of everything, and the three ways it fails.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [What resolving a name actually does](parts/02-names/2.1-what-resolving-a-name-actually-does.md) | one name gave eight addresses — who chose the order? | foundation |
| 2.2 | [The resolver's order, and the file that wins before DNS](parts/02-names/2.2-the-resolver-order-and-the-file-that-wins.md) | `nslookup` says one address, your app uses another — who is lying? | working |
| 2.3 | [TTL, and the change that has not happened yet](parts/02-names/2.3-ttl-and-the-change-that-has-not-happened-yet.md) | the record is correct and half the traffic disagrees — how long for? | working |
| 2.4 | [When a name fails — NXDOMAIN, SERVFAIL and silence](parts/02-names/2.4-when-a-name-fails-nxdomain-servfail-and-silence.md) | which of the three must you never retry? | production |

**Section 3 — `03-the-connection`.** Three packets, two queues, and the distinction that decides who you
escalate to.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [The handshake, and what `connect()` actually waits for](parts/03-the-connection/3.1-the-handshake-and-what-connect-waits-for.md) | 0 ms on loopback, 62 ms across the internet — what is that number? | foundation |
| 3.2 | [The accept queue and the backlog](parts/03-the-connection/3.2-the-accept-queue-and-the-backlog.md) | a connection succeeded against a server that will never accept it — how? | working |
| 3.3 | [`TIME_WAIT`, and the ports you ran out of](parts/03-the-connection/3.3-time-wait-and-the-ports-you-ran-out-of.md) | `EADDRINUSE` from code that never binds — what ran out? | production |
| 3.4 | [Connection refused versus connection timed out](parts/03-the-connection/3.4-connection-refused-versus-connection-timed-out.md) | which of the two would you rather have, and why? | production |

**Section 4 — `04-timeouts`.** The decision nobody makes, the phase it fails to cover, and the multiplier
nothing warns you about.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [A timeout is a decision, not a safety net](parts/04-timeouts/4.1-a-timeout-is-a-decision-not-a-safety-net.md) | what is the default, and what does a timeout actually protect? | working |
| 4.2 | [The four timeouts of one request](parts/04-timeouts/4.2-the-four-timeouts-of-one-request.md) | 155 ms of setup for 60 ms of work — which phase hangs? | working |
| 4.3 | [The timeout that bounded nothing](parts/04-timeouts/4.3-the-timeout-that-bounded-nothing.md) | two seconds configured, eleven observed — where did nine go? | production |

**Section 5 — `05-when-it-adds-up`.** Where the whole day arrives: one slow dependency, and what it does to
a healthy service.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 5.1 | [Hanging `pulse` on purpose](parts/05-when-it-adds-up/5.1-hanging-pulse-on-purpose.md) | four signals green, service dead — name each blindness | production |
| 5.2 | [Retries, backoff and the storm you caused](parts/05-when-it-adds-up/5.2-retries-backoff-and-the-storm-you-caused.md) | the trigger is fixed and the outage continues — why? | production |
| 5.3 | [The deadline that travels](parts/05-when-it-adds-up/5.3-the-deadline-that-travels.md) | four services, five-second timeouts — what is the worst case? | production |

---

## §3 Setup — run this

**Stop first.** Today's measurements are about latency and sockets, and both are contaminated by anything
else on the network. Close anything syncing, downloading or updating. Stop every process from Day 6 —
today's drills bind ports and yesterday's allocators may still be holding memory.

**Profile:** `core` only (Addendum 02 §4). Nothing today is memory-hungry; the constraint is that **the
network must be quiet and the machine must be reachable by itself.**

```bash
# 1 — nothing from previous days survives, and today's ports are free
pgrep -af 'burn|allocate|hungry|uvicorn|dep.py|svc.py' || echo "nothing running"
netstat -an | grep -E ':809[3-9]' || echo "ports 8093-8099 are free"

# 2 — the instruments this day needs
for t in curl nslookup netstat ping; do
  command -v "$t" >/dev/null 2>&1 && echo "ok      $t" || echo "MISSING $t"
done
for t in dig ss nc getent host traceroute; do
  command -v "$t" >/dev/null 2>&1 && echo "ok      $t" || echo "MISSING $t  (expected — Day 21)"
done

# 3 — YOUR BASELINE. Every latency number today is compared against these.
curl -sS -o /dev/null -w 'dns=%{time_namelookup}s connect=%{time_connect}s tls=%{time_appconnect}s total=%{time_total}s\n' https://pypi.org/

# 4 — the two numbers section 3 does arithmetic with
netsh int ipv4 show dynamicport tcp
netstat -an | grep -c TIME_WAIT

# 5 — confirm you have a working network at all before diagnosing one
nslookup pypi.org >/dev/null 2>&1 && echo "DNS ok" || echo "DNS DOWN — stop and fix this first"

# 6 — gate green, tree clean, before you break anything
./o check && git status --short

# 7 — this day's scratch folder
./o scaffold 7
```

⚠️ **Step 2 will report six things missing, and that is expected.** `dig`, `ss`, `nc`, `getent`, `host` and
`traceroute` do not exist on this machine, and they are the instruments most networking material assumes.
**This is the fifth consecutive day with a diagnostic gap here** — Day 5 row 16 and Day 6 row 19 recorded
the previous ones. Every part that needs one of these tools carries a 🅿️ parked block with the command
written out, and Day 21's WSL2 setup is where they arrive. **The workaround throughout is Python's
`socket` module**, which is the same interface the missing tools use, and writing the check yourself is
Principle 4 rather than a consolation prize.

⚠️ **Step 5 is not ceremony.** Several parts today deliberately produce DNS and connection failures. If
your network is genuinely broken when you start, **every deliberate failure will succeed for the wrong
reason** and you will learn nothing. Establish that the baseline works first.

⚠️ **Two experiments today send packets off this machine**, and both are aimed at addresses reserved by
specification for exactly this purpose: names under `.invalid`, which can never exist, and addresses in
`203.0.113.0/24`, which is never routed. **Never point a failure experiment at somebody else's real
service.** It is unsolicited traffic, its results are unreliable because you do not control the target, and
in the case of connection scanning it is the technique a port scanner uses.

**No packages are added today.** Fourth day running. Everything uses the standard library, `curl` and
`netstat`.

---

## §4 Build brief

No project code. `pulse` is unchanged. The two files that resemble it — `lab/svc.py` and `lab/dep.py` —
are drill copies, deleted at the end of the day.

| File | Explained in | What it is |
| --- | --- | --- |
| `lab/reach.py` · `lab/bindwhere.py` | [1.1](parts/01-the-address/1.1-an-address-and-a-port-are-two-questions.md) · [1.3](parts/01-the-address/1.3-binding-127-0-0-1-versus-0-0-0-0.md) | **Yours to write** — what a port is, and what binding decides |
| `lab/fourtuple.py` · `lab/many.py` | [1.2](parts/01-the-address/1.2-the-socket-and-the-four-tuple.md) | **Yours to write** — one port, many connections, none confused |
| `lab/bindtwice.py` | [1.4](parts/01-the-address/1.4-the-port-that-was-already-in-use.md) | **Yours to write** — deliberate failure one: `EADDRINUSE` |
| `lab/resolve.py` | [2.1](parts/02-names/2.1-what-resolving-a-name-actually-does.md) | **Yours to write** — resolution the way a program does it, timed |
| `lab/order.py` | [2.2](parts/02-names/2.2-the-resolver-order-and-the-file-that-wins.md) | **Yours to write** — the search-suffix multiplier, measured |
| `lab/cached.py` | [2.3](parts/02-names/2.3-ttl-and-the-change-that-has-not-happened-yet.md) | **Yours to write** — the cache, proved by measurement |
| `lab/handshake.py` | [3.1](parts/03-the-connection/3.1-the-handshake-and-what-connect-waits-for.md) | **Yours to write** — four destinations, four outcomes |
| `lab/backlog.py` | [3.2](parts/03-the-connection/3.2-the-accept-queue-and-the-backlog.md) | **Yours to write** — deliberate failure two: a full accept queue |
| `lab/timewait.py` · `lab/twdur.py` | [3.3](parts/03-the-connection/3.3-time-wait-and-the-ports-you-ran-out-of.md) | **Yours to write** — 200 connections, and how long their residue lasts |
| `lab/refused_or_dropped.py` | [3.4](parts/03-the-connection/3.4-connection-refused-versus-connection-timed-out.md) | **Yours to write** — refusal against silence, side by side |
| `lab/nodeadline.py` | [4.1](parts/04-timeouts/4.1-a-timeout-is-a-decision-not-a-safety-net.md) | **Yours to write** — the default is `None`, demonstrated |
| `lab/dep.py` · `lab/svc.py` · `lab/hang_drill.sh` | [5.1](parts/05-when-it-adds-up/5.1-hanging-pulse-on-purpose.md) | **Yours to write** — **the day's headline failure** |
| `lab/storm.py` | [5.2](parts/05-when-it-adds-up/5.2-retries-backoff-and-the-storm-you-caused.md) | **Yours to write** — arithmetic, not traffic: when do retries arrive? |
| `lab/deadline.py` | [5.3](parts/05-when-it-adds-up/5.3-the-deadline-that-travels.md) | **Yours to write** — a budget that shrinks down a chain |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — five measurement rows |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — three rows, first symptom before cause |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [2.1](parts/02-names/2.1-what-resolving-a-name-actually-does.md), resolve the base URL of
  each free model provider from Addendum 01 and record **how many addresses each returns and how long the
  lookup took**. Day 9 depends on all three, and you will want the before-numbers.
- `TODO(me)` In [2.2](parts/02-names/2.2-the-resolver-order-and-the-file-that-wins.md), run `ipconfig /all`
  and write down **how many resolvers and how many search suffixes** this machine has. **Do not paste the
  output anywhere** — it describes your network. The two counts are the finding.
- `TODO(me)` In [2.3](parts/02-names/2.3-ttl-and-the-change-that-has-not-happened-yet.md), find one name
  your system will depend on and record its TTL. **Then write down how long a rollback of that name would
  take**, and decide whether you find that acceptable.
- `TODO(me)` In [3.1](parts/03-the-connection/3.1-the-handshake-and-what-connect-waits-for.md), record the
  loopback and internet round trips. **The gap between them is the difference between this machine and
  production**, and Day 25 and Day 41 both make it larger.
- `TODO(me)` In [3.3](parts/03-the-connection/3.3-time-wait-and-the-ports-you-ran-out-of.md), do the
  arithmetic: ephemeral range ÷ measured `TIME_WAIT` duration. **That quotient is this machine's outbound
  connection ceiling per destination.** Write it into `docs/PACKAGES.md`; Day 9 is the first day it binds.
- `TODO(me)` In [4.2](parts/04-timeouts/4.2-the-four-timeouts-of-one-request.md), subtract the five
  cumulative curl numbers into five phase durations and record all five. **State in one sentence what
  fraction of the request was setup rather than work**, and what that says about connection pooling.
- `TODO(me)` Do the [5.1](parts/05-when-it-adds-up/5.1-hanging-pulse-on-purpose.md) drill and record **all
  five observations**: the TCP check, the HTTP check, the error rate, the latency graph, and the socket
  census on both ports.
- `TODO(me)` Find a **sixth** signal that would have been blind during the 5.1 drill and that the part does
  not name.
- `TODO(me)` In [5.2](parts/05-when-it-adds-up/5.2-retries-backoff-and-the-storm-you-caused.md), change
  `CLIENTS` and `ATTEMPTS` to numbers that match a system you actually use, and **look at the peak.**
- `TODO(me)` Write the timeout you intend to put on Day 9's model call, **with the reasoning**, before Day 9
  asks you for it. "Because it seemed reasonable" is not reasoning; a percentile is.
- `TODO(me)` Delete every lab file, confirm with `netstat -an | grep -E ':809[3-9]'` that no listener
  survives, and prove the tree is clean with `git status --short`.

---

## §5 The check that must be able to fail

Two red gates. The first is a three-way diagnosis that must produce three different answers; the second is
the day's headline failure, and it is red in the sense that **the failure is invisible to almost everything
that is supposed to see it.**

**Gate one: three failures, three exit codes.**

```bash
curl -sS -o /dev/null http://no-such-host-kriya-day7.invalid/ ; echo "exit=$?"
curl -sS -o /dev/null http://127.0.0.1:8099/ ; echo "exit=$?"
curl -sS -o /dev/null --connect-timeout 3 http://203.0.113.1/ ; echo "exit=$?"
```

| Target | Expected exit | What it proves |
| --- | --- | --- |
| a name that cannot exist | **6** | the name step failed — nothing was attempted |
| loopback, nothing listening | **7** | something **answered** — the machine is up, the port is empty |
| a reserved, unrouted address | **28** | silence — you do not know how far it got |

**The gate is that all three numbers differ.** If any two match, you have not produced three distinct
conditions — most commonly the third one returns 7 instead of 28 because something on your network refuses
rather than drops, in which case say so and record it, because it is a real property of your network and
worth knowing.

**Gate two: the hang drill leaves your signals green.**

```bash
cd days/day-007-networking-for-operators/lab && ./hang_drill.sh
```

| Observation | Expected |
| --- | --- |
| TCP connect check | **`OK in 0.0 ms`** — green, instant |
| HTTP `/healthz` | **`http=000`, curl exit `28`** — no status code at all |
| error rate in the service | **`0`** — nothing failed |
| completed-request latency | **unchanged or improved** |
| socket census, both ports | **4 established connections held, doing nothing** |

**If `/healthz` returns 200 after the drill, the drill is lying to you** — fewer than `WORKERS` requests
were genuinely in flight, or the dependency was not running and `/predict` was refused rather than hung.
**Check the census first**: it must show exactly `WORKERS` established connections on port 8097 before any
of the other observations mean anything.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline until Day 13. |
| **Network** | **a few hundred kilobytes, and it is the point** | **The first day in this curriculum that uses the network at all.** Roughly thirty DNS queries, a handful of HTTPS requests to public hosts that serve millions per day, and about a dozen packets to a reserved address that go nowhere. |
| RAM | **negligible** | Two small Python processes at their largest. Nothing today allocates deliberately — a complete change from Day 6. |
| Processor | **idle throughout** | Worth noticing: today's headline failure consumes **no** processor, which is exactly why it is invisible. |
| **Sockets / ports** | **~250 ephemeral ports for two minutes each** | Part 3.3 leaves about 250 sockets in `TIME_WAIT`, roughly 1.5% of this machine's range, expiring by themselves. Parts 1.4, 3.2, 5.1 bind ports 8093–8098. |
| Disk | **0** | Nothing is written except lab files you delete. |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). Every destination today is either this machine, a reserved range, or a free public host. |

**The row to read before you start is Network.** Every previous day was self-contained. From today, a
failure can be somebody else's, and ⚠️ **the traffic you generate reaches machines you do not own.** That
is why the two failure experiments target reserved namespaces, and why there is no load-generating loop
anywhere in this day pointed at anything but loopback.

---

## §7 Traps

**An address and a port fail in ways that look identical.** *Connection refused* on the wrong port and
*connection refused* on the wrong host are the same sentence. Read which half of the pair you changed.
Part [1.1](parts/01-the-address/1.1-an-address-and-a-port-are-two-questions.md).

**`EADDRINUSE` has two unrelated causes.** A port collision, and ephemeral port exhaustion in a client that
never binds anything. The manual page lists both under one errno. Parts
[1.4](parts/01-the-address/1.4-the-port-that-was-already-in-use.md) and
[3.3](parts/03-the-connection/3.3-time-wait-and-the-ports-you-ran-out-of.md).

**`localhost` resolves to `::1` before `127.0.0.1`.** A server bound to `127.0.0.1` and a client connecting
to `localhost` are not necessarily talking about the same address. Parts
[1.3](parts/01-the-address/1.3-binding-127-0-0-1-versus-0-0-0-0.md) and
[2.2](parts/02-names/2.2-the-resolver-order-and-the-file-that-wins.md).

**`nslookup` and your application consult different lists.** `nslookup` speaks DNS; your program checks
built-in rules, the hosts file and a cache first. When they disagree, **neither is lying** — and a
sub-millisecond lookup is the tell that nothing left the machine.
Part [2.2](parts/02-names/2.2-the-resolver-order-and-the-file-that-wins.md).

**A name with fewer dots than `ndots` gets every search suffix tried first.** Measured here at 2718 ms
against 32 ms for the same failing lookup. Kubernetes sets `ndots:5`, which catches essentially every name
a human types. A trailing dot turns four queries into one.
Part [2.2](parts/02-names/2.2-the-resolver-order-and-the-file-that-wins.md).

**Negative answers are cached too.** Query a name before you create it and the `NXDOMAIN` is remembered.
The record exists and your resolver disagrees.
Part [2.4](parts/02-names/2.4-when-a-name-fails-nxdomain-servfail-and-silence.md).

**A completed handshake proves nothing about the application.** The kernel does all three packets and parks
the result in a queue. **A TCP port check goes green against a completely dead service** — measured at 0.0
milliseconds while `/healthz` timed out. Parts
[3.2](parts/03-the-connection/3.2-the-accept-queue-and-the-backlog.md) and
[5.1](parts/05-when-it-adds-up/5.1-hanging-pulse-on-purpose.md).

**A full accept queue refuses on Windows and drops on Linux.** The same overload reports *connection
refused* on one platform and *timed out* on the other, from one sentence in the same manual page.
Part [3.2](parts/03-the-connection/3.2-the-accept-queue-and-the-backlog.md).

**A round number is a policy; a ragged number is a measurement.** Exactly `5000.00 ms` is your
configuration expiring. `62.00 ms` is the world.
Part [3.1](parts/03-the-connection/3.1-the-handshake-and-what-connect-waits-for.md).

**A connect timeout does not bound a server that accepts and goes quiet.** Measured: connect satisfied in
2.5 ms, operation ran to the 8 s limit. **The phase that hangs is not the phase that is usually bounded.**
Part [4.2](parts/04-timeouts/4.2-the-four-timeouts-of-one-request.md).

**Your timeout bounds one attempt; your caller experiences attempts × addresses × layers.** Measured twice
today, in two unrelated tools: `--max-time 2` with retries took 11.2 s, and `nslookup -timeout=2` took
10.1 s. Part [4.3](parts/04-timeouts/4.3-the-timeout-that-bounded-nothing.md).

**Exponential backoff does not prevent a retry storm.** Doubling is the same number for everybody, so they
return together. **Jitter is the fix**, and it is the line people omit.
Part [5.2](parts/05-when-it-adds-up/5.2-retries-backoff-and-the-storm-you-caused.md).

**Many `TIME_WAIT` is usually normal; many `CLOSE_WAIT` is always a bug.** One is the kernel doing its job;
the other is an application that was told the connection ended and never noticed. Parts
[3.3](parts/03-the-connection/3.3-time-wait-and-the-ports-you-ran-out-of.md) and
[5.1](parts/05-when-it-adds-up/5.1-hanging-pulse-on-purpose.md).

**The named trap from plan §5.1 that this day touches:** *the capability without a bound.* An outbound call
with no timeout is a capability with no brake, and its blast radius is not the call — **it is every worker
your service has**, because each stuck call holds one for ever. Day 6's version was a process with no
memory limit taking down a node. Today's is a request with no deadline taking down a service, and the
containment is the same shape: a bound, chosen deliberately, that converts an unbounded failure into a
counted one. Parts [4.1](parts/04-timeouts/4.1-a-timeout-is-a-decision-not-a-safety-net.md) and
[5.3](parts/05-when-it-adds-up/5.3-the-deadline-that-travels.md).

---

## §8 Verify before you build

Fetched on **2026-08-26**, not recalled:

| Page | Used for |
| --- | --- |
| `docs.python.org/3.12/library/socket.html` | `getaddrinfo` signature and its 5-tuple return; `gaierror`; `settimeout` and the `timeout` exception; **`getdefaulttimeout` returning `None`, quoted verbatim**; `create_connection`'s timeout inheritance |
| `man7.org/linux/man-pages/man2/listen.2.html` | **the backlog sentence, verbatim**; the full-queue behaviour — `ECONNREFUSED` *or* a silent drop — quoted in full; `somaxconn` being *"silently capped"*; the two `EADDRINUSE` causes |
| `everything.curl.dev/cmdline/exitcode.html` | curl exit codes 6, 7, 28, 35, 52, 56 — **the 7 and 28 descriptions quoted verbatim** |
| `curl.se/docs/manpage.html` | **`--connect-timeout` quoted verbatim**, including the word *only* |
| local `curl --help all`, curl 8.19.0 | `--max-time` and `--retry-max-time`, confirmed on this machine |

**Everything else in this day was measured here rather than looked up**, and every observed block carries
the date. That list is worth stating explicitly because it is unusually long today: the eight addresses for
`pypi.org`, the 2718 ms against 32 ms suffix multiplier, the TTL counting down from 2 to 0 and refetching
at 109, the four connect outcomes, the backlog refusal at `listen(1)`, the 6 → 208 `TIME_WAIT` census, the
120-second expiry, the 16384-port ephemeral range, the connect-versus-total gap of 2.5 ms against 8004 ms,
the 2.1 s against 11.2 s retry multiplication, and the whole hang drill.

⚠️ **Three things in this day are platform-specific and flagged where they appear**, because a rule learned
here would be wrong elsewhere: a refused connection on loopback takes about two seconds on this machine and
well under a millisecond on Linux; a full accept queue refuses here and drops there; and the errnos differ
throughout — 10061 against 111, 11001 against −2, 10048 against 98. **Learn the error class and the
condition; the numbers are local.**

---

## §9 Say it in an interview

*"The thing that reorganised how I think about networking was realising that most network failures are not
errors — they are silences, and a silence has no duration except the one somebody chooses. A refused
connection is an answer: something sent a reset, so the host is up, packets reach it, replies come back,
and nothing is listening on that port. That narrows it to one machine I can log into. A timeout tells me
almost nothing — the packet may have been dropped by a firewall, the reply may have been lost on the way
back, or the host may be too busy to answer — so it is usually an escalation rather than a fix. I would
much rather have the refusal, which surprises people because it sounds worse.*

*"The distinction that costs the most time is the one in front of all of it. A name is not an address, so
before anything connects there is a lookup run by machinery I do not own, which checks a hosts file and a
cache before DNS is asked, which can return an answer that is a stale copy with a lifetime somebody set
months ago, and which can fail in three ways that need three different responses — the name does not exist,
the resolver could not find out, or nobody replied. My application collapses all three into one message,
so I recover the difference with one command and the duration: a fast failure is an answer, a slow one is
silence.*

*"What I actually got wrong, and fixed by causing it deliberately, was the timeout. The default in the
standard library is no timeout at all, and I had assumed the convenience wrapper supplied a sensible one.
It does not. I pointed a service with four workers at a dependency that accepted connections and never
replied, and it died in about four seconds — with the processor idle, memory flat, error rate at zero,
because nothing had failed, and the latency graph unchanged, because a histogram records a request when it
completes and these never completed. A TCP port check reported it healthy the whole time in essentially
zero milliseconds, because the kernel finishes handshakes and parks them in the accept queue without asking
the application anything. Four of my five signals were green.*

*"The two things I would build differently now are a deadline rather than a timeout, and jitter on every
retry. A timeout is a duration each service invents for itself, so four services with five-second timeouts
have a twenty-second worst case while the user left after three; a deadline is a point in time passed down
the chain, so a hop can refuse to start work whose answer nobody will still want, and retries stop
multiplying because they run against the remaining budget rather than a count. And retries synchronise:
every client fails at the same instant and exponential backoff is the same number for everybody, so they
all come back together, which is how a brief blip becomes an outage that continues after the trigger is
fixed. I have not operated this at fleet scale; what I have done is cause each failure on purpose and write
down what my signals said before I knew the cause."*

---

## §10 Done when

`days/day-007-networking-for-operators/CHECKLIST.md` has no unticked boxes, and `./o done 7` refuses to
commit until that is true.

Done is defined by understanding and green checks, never by elapsed time. Specifically: you can look at a
failed connection and say in one step whether it was the name, a refusal or a silence; you have seen a
connection succeed against a server that would never accept it; you have watched a service die with every
resource graph green; you can state the arithmetic that turns a worker pool and a request rate into a
time-to-death; and **every listener you started is confirmed stopped**, because today's leftovers hold
ports that tomorrow needs.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append this row verbatim, replacing the commit hash with your own after
committing:

```text
| 7 | 2026-08-26 | FND-08, FND-09 | 18 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — no package rows today. Five measurement rows:

```text
| curl | 8.19.0 | 2026-08-26 | 7 | Observed with `curl --version`. The day's primary instrument; `--write-out` phase variables and exit codes 6/7/28 are the whole diagnostic. |
| machine: ephemeral port range | <start> + <count> | 2026-08-26 | 7 | Observed with `netsh int ipv4 show dynamicport tcp`. The numerator of this machine's outbound connection ceiling. |
| machine: TIME_WAIT duration | <n> s | 2026-08-26 | 7 | Measured with `twdur.py`, Day 7 part 3.3. The denominator of the ceiling. Platform-specific — remeasure in WSL2 on Day 21. |
| machine: outbound connection ceiling | <n>/s per destination | 2026-08-26 | 7 | Ephemeral range ÷ TIME_WAIT duration. **The cap on Day 9's model calls if the client is not pooled.** |
| network: baseline request phases | dns <n> / connect <n> / tls <n> / ttfb <n> / total <n> ms | 2026-08-26 | 7 | From `curl --write-out` against a public host, Day 7 part 4.2. **The "before" numbers** — Day 9 chooses its timeout against these and Day 25 re-measures from inside a container. |
```

**`docs/INCIDENTS.md`** — three rows, and **write the first symptom before you investigate**:

```text
| 20 | 2026-08-26 | 7 | Hung a four-worker service on a dependency that accepts and never replies, part 5.1 | <what the TCP check and the HTTP check each returned, verbatim, including http= and exit=> | <what you found> | <smallest fix> | <what you changed so it cannot happen silently again> |
| 21 | 2026-08-26 | 7 | Set `--max-time 2` with retries and measured the wall clock, part 4.3 | <the two `time` results> | A per-attempt bound is not a bound on the operation; the multiplier is not written down anywhere in the configuration | `--retry-max-time`, or an overall deadline | <the number you will use on Day 9, and why> |
| 22 | 2026-08-26 | 7 | Environmental — no `dig`, `ss`, `nc`, `getent`, `host` or `traceroute` on this machine | <what §3 step 2 printed> | Git Bash over Windows ships none of the standard networking diagnostics; every part that needs one carries a 🅿️ parked block and a Python equivalent | none — run them in WSL2 from Day 21 | **Fifth consecutive day recording a diagnostic gap. Link this row to Day 6 row 19 and Day 5 row 16**, and make Day 21 close all three |
```

⚠️ **Row 22 is the fifth of its kind.** **Link them explicitly.** Five linked rows with a named closing day
is a finding with an owner; five separate shrugs are noise. Day 21 stops being a setup chore and becomes
the day that closes a documented, dated gap you found yourself.

**`docs/DECISIONS.md`** — an ADR is worth writing **if** your `TODO(me)` on Day 9's timeout reached a
conclusion. *"Every outbound call carries a deadline derived from the caller's remaining budget, retries are
bounded by that budget rather than by a count, and jitter is mandatory"* is exactly the shape of a decision
that is expensive to reverse, invisible in the code once made, and non-obvious to a stranger — and Day 9 is
the first day that implements whatever you decide.

**The commit:**

```text
day 007: networking for operators — names, connections and the timeout that saves the system — closes FND-08, FND-09
```
