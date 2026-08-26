# Day 7 — Checklist

**Definition of done.** `./o done 7` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd days/day-007-networking-for-operators/lab && ./hang_drill.sh
```

A healthy service killed by a dependency that never failed, and a TCP health check that stays green
throughout. Yesterday you could explain why a dead service reported nothing at all. Today you can explain
why a *live* one does — and name the four signals that were blind.

---

## Setup

- [ ] **nothing from Day 6 still running** — `pgrep -af 'burn|allocate|hungry|uvicorn'`
- [ ] **ports 8093–8099 free** — `netstat -an | grep -E ':809[3-9]'` returns nothing
- [ ] §3 step 2 run, and the **six MISSING tools written down** rather than skimmed
- [ ] **baseline captured** — the `curl --write-out` phase numbers from §3 step 3, before anything else
- [ ] ephemeral port range and starting `TIME_WAIT` count recorded — §3 step 4
- [ ] **DNS confirmed working before producing deliberate DNS failures** — §3 step 5
- [ ] read and accepted the reserved-target rule: `.invalid` names and `203.0.113.0/24` only, **never
      somebody else's service**
- [ ] `./o check` green and `git status --short` clean before breaking anything
- [ ] `./o scaffold 7` has created the day's `lab/`
- [ ] no packages added, and `git diff pyproject.toml uv.lock` confirms it

---

## Section 1 — `01-the-address`

- [ ] **1.1** read · the address/port split understood as **two questions with two failure modes**
- [ ] **1.1** `lab/reach.py` written · `netstat -ano` read with `-o` and the pid column noticed
- [ ] **1.1** the privileged port range understood, and `EACCES` distinguished from `EADDRINUSE`
- [ ] **1.1** answered out loud: *the parcel reached the building — name the two questions and say which
      one the tracking answered*
- [ ] **1.2** read · `lab/fourtuple.py` written · **one server port holding several connections at once,
      seen rather than believed**
- [ ] **1.2** `lab/many.py` written · the four-tuple identified in `netstat` output, both halves
- [ ] **1.2** the listening socket's empty remote half noticed — **it is not a connection**
- [ ] **1.2** answered out loud: *one port, ten thousand connections — what makes each one distinct, and
      which of the four numbers varies*
- [ ] **1.3** read · `lab/bindwhere.py` written · bound to `127.0.0.1`, then `0.0.0.0`, and the difference
      in reachability confirmed
- [ ] **1.3** understood as **a security boundary, not a convenience setting**
- [ ] **1.3** answered out loud: *it works locally and nothing else can reach it — which did you bind, and
      what does changing it admit besides your traffic*
- [ ] **1.4** read · `lab/bindtwice.py` written · **deliberate failure one produced on purpose**
- [ ] **1.4** the errno recorded — 10048 here, 98 on Linux — and **the errno learned rather than the
      sentence**
- [ ] **1.4** the culprit found in two commands: `netstat -ano` → pid → `ps -o pid,args`
- [ ] **1.4** ⚠️ **the rule accepted: never kill a pid you have not identified**
- [ ] **1.4** the `TIME_WAIT` variant understood — port held, `ps` shows nothing — and forward-linked to 3.3
- [ ] **1.4** answered out loud: *"address already in use" on port 8000 — the two commands, in order, and
      what each tells you that the error did not*

---

## Section 2 — `02-names`

- [ ] **2.1** read · `lab/resolve.py` written, **with `proto=socket.IPPROTO_TCP`** and why understood
- [ ] **2.1** one name resolved to **several addresses**, and the count recorded
- [ ] **2.1** the lookup **timed**, and the duration recognised as a separate cost before any connection
- [ ] **2.1** `nslookup` run · **`Server:` and `Non-authoritative answer` both noticed** — a dependency you
      did not know you had, and an answer that came from a cache
- [ ] **2.1** `TODO(me)` — all three free providers from Addendum 01 resolved, **address counts and lookup
      durations written down** for Day 9
- [ ] **2.1** answered out loud: *name the three parties, say which one your program talks to, and say what
      `Non-authoritative answer` tells you*
- [ ] **2.2** read · `localhost` resolved and **`::1` seen returned before `127.0.0.1`**
- [ ] **2.2** the hosts file read **as the machine reads it** — comments and blanks filtered out
- [ ] **2.2** `lab/order.py` written · **the dotless-versus-dotted multiplier measured** on this machine
- [ ] **2.2** the trailing dot understood as a control character, and `ndots:5` noted as Kubernetes' default
- [ ] **2.2** `TODO(me)` — resolver count and search-suffix count recorded, **and the output not pasted
      anywhere**
- [ ] **2.2** answered out loud: *list the sources consulted before DNS in order, and explain how `nslookup`
      and your application can disagree without either being broken*
- [ ] **2.3** read · `lab/cached.py` written · **the cold lookup and the warm ones measured**
- [ ] **2.3** `nslookup -debug` run **twice**, and the TTL seen counting down and resetting
- [ ] **2.3** the difference between a **configured** TTL and a **remaining** TTL understood
- [ ] **2.3** ⚠️ **the sequence rule understood: lower the TTL *before* the change, not during it** — and
      why doing it during achieves nothing
- [ ] **2.3** `TODO(me)` — one real dependency's TTL recorded, **and how long a rollback of that name would
      take** written down with a verdict
- [ ] **2.3** answered out loud: *why is a DNS change a window rather than an event, and what must happen
      first if you need it fast*
- [ ] **2.4** read · **all three failures produced**: `Non-existent domain`, `Server failed`, and a timeout
- [ ] **2.4** **the silent case timed**, and the ratio between the configured per-attempt timeout and the
      wall clock recorded
- [ ] **2.4** the three responses distinguished: **never retry NXDOMAIN**, retry SERVFAIL, check
      reachability on silence
- [ ] **2.4** negative caching understood — **do not query a name before you create it**
- [ ] **2.4** the reserved-target rule honoured: `.invalid` and `203.0.113.0/24`, nothing real
- [ ] **2.4** answered out loud: *the three ways a lookup fails, which you must never retry, and which one
      you can identify from duration alone*

---

## Section 3 — `03-the-connection`

- [ ] **3.1** read · `lab/handshake.py` written · **four destinations, four outcomes**
- [ ] **3.1** the three packets named in order, and **which one `connect()` returns after** understood
- [ ] **3.1** the loopback and internet round trips recorded — **the gap is production**
- [ ] **3.1** the exact-round-number timeout recognised as **a policy rather than a measurement**
- [ ] **3.1** ⚠️ the platform note recorded: a loopback refusal takes about two seconds here and well under
      a millisecond on Linux — **so duration alone does not separate the cases on this machine**
- [ ] **3.1** `TODO(me)` — both round trips written into `docs/PACKAGES.md`
- [ ] **3.1** answered out loud: *the three packets, what a connection costs in round trips, and why a
      successful handshake says almost nothing about the application*
- [ ] **3.2** read · `lab/backlog.py` written with `listen(1)` and **no `accept()` anywhere**
- [ ] **3.2** **`connect 1: connected` observed against a server that will never accept it** — the day's
      most important single line
- [ ] **3.2** the two queues distinguished — SYN queue and accept queue
- [ ] **3.2** the `listen(2)` sentence read verbatim, and **both branches understood**: refuse *or* drop
- [ ] **3.2** `somaxconn` noted as **silently capping** a configured backlog
- [ ] **3.2** **a bigger queue understood as more delay, not more capacity**
- [ ] **3.2** answered out loud: *who performs the handshake, what `accept()` does, and why a TCP port check
      is green against a dead application*
- [ ] **3.3** read · `lab/timewait.py` written · **before and after `TIME_WAIT` counts recorded**
- [ ] **3.3** the census on the experiment's port run, showing **sockets with no owning process**
- [ ] **3.3** `lab/twdur.py` written · **the `TIME_WAIT` duration measured on this machine**, not quoted
- [ ] **3.3** the ephemeral range read, and **which end of a connection pays** understood
- [ ] **3.3** `TODO(me)` — **range ÷ duration computed**, and the quotient written into `docs/PACKAGES.md`
      as this machine's outbound connection ceiling per destination
- [ ] **3.3** the two reasons `TIME_WAIT` exists stated, and ⚠️ **`tcp_tw_recycle` recognised as advice not
      to follow**
- [ ] **3.3** answered out loud: *which end enters `TIME_WAIT` and why, the ceiling arithmetic, and why the
      fix is a connection pool rather than a kernel setting*
- [ ] **3.4** read · `lab/refused_or_dropped.py` written · **refusal and silence produced side by side**
- [ ] **3.4** **what a refusal proves** listed — host up, reachable, replies return, port empty
- [ ] **3.4** **what a timeout proves** listed — and the answer *almost nothing* accepted
- [ ] **3.4** **exit 6, 7 and 28 memorised**, with where each one sends you to look first
- [ ] **3.4** the exception understood: an intermittent, load-correlated refusal is a **full accept queue**,
      not a missing process
- [ ] **3.4** ⚠️ the scanning boundary understood — refusal and silence are what a port scanner collects, so
      **target and authorisation are what make this legitimate**
- [ ] **3.4** answered out loud: *what a refusal proves that a timeout does not, and which of the two is
      more dangerous to your own capacity*

---

## Section 4 — `04-timeouts`

- [ ] **4.1** read · **`socket.getdefaulttimeout()` run, and `None` seen with your own eyes**
- [ ] **4.1** `lab/nodeadline.py` written · **the socket's own timeout confirmed `None` after
      `create_connection`**
- [ ] **4.1** the watchdog line identified as **scaffolding, not the lesson**
- [ ] **4.1** **both halves of the decision** stated: bound the wait, *and* decide what happens when it
      fires — and the second half recognised as the one people ship without
- [ ] **4.1** what a timeout protects understood — **your own capacity**, not the dependency
- [ ] **4.1** the too-low failure understood: **an aggressive timeout is a decision to fail healthy
      traffic**
- [ ] **4.1** answered out loud: *what a timeout protects, the two halves of the decision, and why leaving
      it unset is worse than setting it badly*
- [ ] **4.2** read · the **five cumulative curl variables** captured for one real request
- [ ] **4.2** ⚠️ **the numbers subtracted into phase durations** — the step that is easy to miss
- [ ] **4.2** `TODO(me)` — all five phase durations written into `docs/PACKAGES.md`, **with the setup
      fraction stated in one sentence**
- [ ] **4.2** **`--connect-timeout` observed being satisfied while bounding nothing** — connect in
      milliseconds, operation running to `--max-time`
- [ ] **4.2** the **fifth wait** named: queueing for a connection from an exhausted pool, before any network
      timeout applies
- [ ] **4.2** an inactivity timeout distinguished from a duration limit, and **the drip-feed defeat**
      understood
- [ ] **4.2** answered out loud: *the phases in order, which phase a connect timeout bounds, which phase a
      wedged server hangs in, and the wait that precedes all your timeouts*
- [ ] **4.3** read · **the control measured first** — one attempt, bound honoured
- [ ] **4.3** **deliberate failure three produced**: the same timeout with retries, timed from outside
- [ ] **4.3** the ratio recorded, and **each attempt confirmed to have honoured its own bound**
- [ ] **4.3** the **three multipliers** named — retries, addresses, layers — and ⚠️ **the one not in your
      own configuration** identified
- [ ] **4.3** `--retry-max-time` (or the library equivalent) understood as **the setting that bounds the
      sequence**
- [ ] **4.3** the same trap recognised in `nslookup` from part 2.4 — **two unrelated tools, one mistake**
- [ ] **4.3** answered out loud: *the three multipliers, which is not yours, and the setting that bounds the
      sequence rather than the attempt*

---

## Section 5 — `05-when-it-adds-up`

- [ ] **5.1** read · `lab/dep.py` written — **it reads the request before going silent**, and why understood
- [ ] **5.1** `lab/svc.py` written — **the missing `timeout=` identified as the entire bug**
- [ ] **5.1** `/healthz` noticed as **deliberately well written** — it does not touch the dependency — and
      seen to fail anyway
- [ ] **5.1** `lab/hang_drill.sh` written · **the drill run with the pool genuinely exhausted**
- [ ] **5.1** ⚠️ **the drill validated before it was believed**: the census shows exactly `WORKERS`
      established connections on the dependency's port
- [ ] **5.1** `TODO(me)` — **all five observations recorded**: TCP check, HTTP check, error rate, latency,
      and the socket census on both ports
- [ ] **5.1** the two health checks put side by side — **`OK in 0.0 ms` against `http=000`**
- [ ] **5.1** the **time-to-death arithmetic** stated: workers ÷ requests per second
- [ ] **5.1** the one-argument fix applied and the drill re-run, with `/healthz` surviving and `/predict`
      **failing honestly**
- [ ] **5.1** `TODO(me)` — a **sixth** blind signal found that the part does not name
- [ ] **5.1** **`CLOSE_WAIT` distinguished from `TIME_WAIT`** — one is always a bug, one usually is not
- [ ] **5.1** **both background processes confirmed stopped** and both ports clear
- [ ] **5.1** answered out loud: *the time-to-death arithmetic, the four signals that stayed green and why
      each was blind, and the one measurement that sees a request which never completes*
- [ ] **5.2** read · `lab/storm.py` written · **both shapes produced from the same total volume**
- [ ] **5.2** the peak recorded for each, and **the four walls in the fixed-backoff output seen**
- [ ] **5.2** **jitter identified as the fix for synchronisation**, and backoff as the fix for volume — two
      different problems
- [ ] **5.2** **metastable failure** understood: the trigger is gone and the outage continues, and **waiting
      does not end it**
- [ ] **5.2** the amplification table read — **three layers at three attempts is twenty-seven**
- [ ] **5.2** the retry rules stated: **not NXDOMAIN, not 4xx, not a timeout on a write**, and
      `Retry-After` honoured when present
- [ ] **5.2** `TODO(me)` — `CLIENTS` and `ATTEMPTS` changed to numbers matching a system you use, **and the
      peak looked at**
- [ ] **5.2** answered out loud: *why backoff alone does not prevent a storm, the one line that does, and
      what a metastable failure is*
- [ ] **5.3** read · `lab/deadline.py` written · **four hops, three different behaviours observed**
- [ ] **5.3** **the `SKIPPED` line understood as the decision a duration cannot express**
- [ ] **5.3** the clamp line identified — `min(cost, left - reserve)` — as **the whole of propagation**
- [ ] **5.3** `time.monotonic()` understood as mandatory, and **`max(0.0, ...)` understood as preventing a
      negative timeout becoming no timeout**
- [ ] **5.3** the additive arithmetic done: **four services, five-second timeouts, twenty-second worst case**
- [ ] **5.3** ⚠️ **the rule accepted: a hop's timeout must be smaller than the deadline it was given** —
      never larger
- [ ] **5.3** **remaining milliseconds preferred over an absolute timestamp**, and clock skew understood as
      the reason
- [ ] **5.3** a propagated deadline distinguished from an **honoured** one
- [ ] **5.3** `TODO(me)` — **Day 9's model-call timeout written down with its reasoning**, before Day 9 asks
- [ ] **5.3** answered out loud: *the four-hop worst case and why a deadline avoids it, the three things a
      deadline lets you do, and why you would send a duration rather than a timestamp*

---

## Both red gates

- [ ] **Gate one** — three failures produced and **all three exit codes differ**: 6, 7 and 28
- [ ] **Gate one** — if the third returned 7 rather than 28, **that is recorded as a property of your
      network** rather than ignored
- [ ] **Gate two** — the hang drill produced `OK in 0.0 ms` from the TCP check and `http=000` with exit `28`
      from `/healthz`, at the same moment, against the same service
- [ ] **Gate two** — the socket census showed connections **held open to a dependency that will never
      answer**
- [ ] neither gate produced a false pass: the deliberate failures genuinely failed for the reason claimed,
      and the drill genuinely exhausted the pool

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes — confirmed, not assumed
- [ ] **every deliberate failure was aimed at a reserved target** — `.invalid`, `203.0.113.0/24` or
      loopback — and **nothing was pointed at a service you do not own**
- [ ] **`netstat -an | grep -E ':809[3-9]'` shows no `LISTENING` socket** — no drill server survives
- [ ] `pgrep -af 'dep.py|svc.py|backlog|timewait|handshake'` returns nothing
- [ ] `TIME_WAIT` count back near its starting value — **confirmed, after waiting out the duration you
      measured in 3.3**
- [ ] every lab file created today deleted, and `git status --short` clean
- [ ] **no network configuration on this machine was changed** — no hosts file edit, no resolver change, no
      kernel or registry setting

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — five measurement rows appended (curl version · ephemeral range · `TIME_WAIT`
      duration · connection ceiling · baseline request phases)
- [ ] `docs/INCIDENTS.md` — **three rows appended, first symptom written before the cause** (rows 20, 21, 22)
- [ ] **row 22 explicitly linked to Day 6 row 19 and Day 5 row 16** — five consecutive days of diagnostic
      gaps, with Day 21 named as where they close
- [ ] `docs/DECISIONS.md` — an ADR written **if** the deadline-and-retry `TODO(me)` reached a conclusion
- [ ] `docs/PROGRESS.md` — the Day 7 row pasted from the hub's §11
- [ ] `./o check` green
- [ ] `./o depth 7` green
- [ ] `./o trace` shows **FND-08 and FND-09** closed and nothing else newly closed
- [ ] committed: `day 007: networking for operators — names, connections and the timeout that saves the system — closes FND-08, FND-09`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
