# Day 7 — Checklist

**Definition of done.** `./o done 7` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd days/day-007-networking-for-operators && uv run python lab/blackhole.py 8015 & BH=$!; uv run uvicorn --app-dir lab hangy:app --host 127.0.0.1 --port 8010 --log-level warning & UV=$!; sleep 4; curl -sS -m 3 -o /dev/null -w 'before: healthz http=%{http_code} exit=%{exitcode}\n' http://127.0.0.1:8010/healthz; uv run python -c "
import concurrent.futures, time, httpx2
def hit(i):
    try: httpx2.post('http://127.0.0.1:8010/predict', json={'text':'x'}, timeout=httpx2.Timeout(60.0))
    except Exception: pass
pool = concurrent.futures.ThreadPoolExecutor(max_workers=40)
[pool.submit(hit, i) for i in range(40)]
time.sleep(6)
" & sleep 9; curl -sS -m 8 -o /dev/null -w 'during: healthz http=%{http_code} exit=%{exitcode}\n' http://127.0.0.1:8010/healthz; kill "$UV" "$BH" 2>/dev/null
```

A service made completely unreachable by forty requests to a dependency that is up and silent — with the
processor idle, the memory flat, no errors anywhere and a health check that returns nothing at all.
Yesterday you could explain why a killed service reported nothing. Today you can explain why a perfectly
healthy one does.

---

## Setup

- [ ] **nothing from Day 6 still running** — `pgrep -af 'burn|allocate|shared|mapshare|hungry|uvicorn'`
- [ ] **ports 8000–8015 confirmed free** before starting, not assumed
- [ ] `curl`, `netstat` and `nslookup` all present, or the MISSING ones written down
- [ ] this machine's **default resolver** recorded from §3 step 4
- [ ] **`import httpx2` confirmed working, and `import httpx` confirmed failing** — the name is the trap
- [ ] `./o check` green and `git status --short` clean before breaking anything
- [ ] `./o scaffold 7` has created the day's `lab/`
- [ ] no packages added, and `git diff pyproject.toml uv.lock` confirms it — fourth day running

---

## Section 1 — `01-addresses-and-ports`

- [ ] **1.1** read · `lab/claim_port.py` written · **the second bind refused while the first still holds
      the port**
- [ ] **1.1** the address/port split understood: **the address picks a machine, the port picks a program**
- [ ] **1.1** answered out loud: *two programs, one port — why can only one of them have it, and what
      exactly is the thing being claimed*
- [ ] **1.2** read · `lab/hold_conns.py` written · **many connections to one listening port, and the
      four-tuples read from `netstat`**
- [ ] **1.2** confirmed that **only the source port differs** between them, and why that is sufficient
- [ ] **1.2** answered out loud: *one listening port, ten thousand clients — name the four values and say
      which of them makes each connection unique*
- [ ] **1.3** read · `pulse` started on `127.0.0.1`, then on `0.0.0.0`, and reached from a second terminal
      **each way**
- [ ] **1.3** `TODO(me)` — which bind address the Day 22 container needs, **written down with the reason
      it is not a security regression**
- [ ] **1.3** answered out loud: *"it works on my machine but not from the container" — the one line that
      explains it, and what each of the two values actually permits*
- [ ] **1.4** read · `lab/no_reuse.py` written · **`address already in use` produced deliberately**
- [ ] **1.4** **all four causes** distinguished — forgotten process · different bind address · `TIME_WAIT`
      · something you did not start
- [ ] **1.4** the **one command** that goes from the error to the owning process practised, not read
- [ ] **1.4** answered out loud: *name the four causes and the single command that tells them apart*

---

## Section 2 — `02-dns`

- [ ] **2.1** read · a lookup watched happening **before** any connection is made
- [ ] **2.1** understood that resolution is **a separate service over a separate protocol**, and that it
      appears in none of your application logs
- [ ] **2.1** answered out loud: *what happens between typing a hostname and the first byte being sent*
- [ ] **2.2** read · the record types distinguished, and a real TTL looked up
- [ ] **2.2** `TODO(me)` — **earliest and latest** moment a record change reaches everybody, both numbers
      written down, and the gap between them named
- [ ] **2.2** **a TTL understood as a lower bound on propagation and never an upper one**
- [ ] **2.2** answered out loud: *you changed the record — when does the last client see it, and why is
      the honest answer not the TTL*
- [ ] **2.3** read · `lab/slow_resolver.py` written · **a resolver that never answers**
- [ ] **2.3** the delay confirmed landing **before** any application log line
- [ ] **2.3** understood why this looks like the *destination* being slow rather than the resolver
- [ ] **2.3** answered out loud: *every request in the system got slower by the same amount — where you
      look first, and why the application logs will not help*

---

## Section 3 — `03-tcp`

- [ ] **3.1** read · the handshake traced · `lab/no_close.py` written
- [ ] **3.1** **`CLOSE_WAIT` produced on purpose** and recognised as *the application did not close it*
- [ ] **3.1** the `State` column read fluently — at least `LISTENING`, `ESTABLISHED`, `TIME_WAIT`,
      `CLOSE_WAIT`
- [ ] **3.1** answered out loud: *what is this socket doing, and which column tells you*
- [ ] **3.2** read · `lab/tiny_backlog.py` written with `listen(1)` · **a queue nobody drains**
- [ ] **3.2** confirmed that **the kernel completes the handshake whether or not the application accepts**
- [ ] **3.2** understood why the client sees **no error at all** while waiting in that queue
- [ ] **3.2** answered out loud: *the application is stalled and clients see no error — where are their
      requests, and what does the latency they experience consist of*
- [ ] **3.3** read · `TIME_WAIT` sockets observed after a burst of closes
- [ ] **3.3** **why it is harmless on a server and fatal on a client** stated in your own words
- [ ] **3.3** `TODO(me)` — ephemeral port range counted and divided by the `TIME_WAIT` duration; **that
      quotient written into `docs/PACKAGES.md`**
- [ ] **3.3** connection reuse understood as **the fix, not an optimisation**
- [ ] **3.3** answered out loud: *harmless on a server, fatal on a client — what changed, and what the
      ceiling actually is*
- [ ] **3.4** read · `lab/silent_peer.py` and `lab/keepalive.py` written
- [ ] **3.4** **a connection confirmed `ESTABLISHED` on one side while the peer is unresponsive**
- [ ] **3.4** understood that an idle TCP connection **sends nothing**, so neither end learns anything
- [ ] **3.4** answered out loud: *`ESTABLISHED` on your side, gone on theirs — how you ever find out, and
      why that discovery method is the exact operation you were trying to protect*

---

## Section 4 — `04-timeouts`

- [ ] **4.1** read · `lab/no_timeout.py` and `lab/with_timeout.py` written
- [ ] **4.1** **both run against the same silent peer**, and the exit codes compared — `124` for the one
      killed from outside, `0` for the one that decided
- [ ] **4.1** the resources a hung request holds listed: **a thread, two file descriptors, buffers, and
      your caller**
- [ ] **4.1** the library defaults table read, and **"no timeout" understood as a decision to wait
      forever** rather than an omission
- [ ] **4.1** answered out loud: *"we didn't set a timeout" is a decision — state what it commits you to
      and name the resource it spends*
- [ ] **4.2** read · `lab/four_timeouts.py` written · **each of the four exception classes seen by name**
- [ ] **4.2** confirmed that **connecting to a hung server succeeds instantly**, so a connect timeout
      protects against the least likely failure
- [ ] **4.2** `lab/dribble.py` written · **a 3-second timeout permitting a 20-second request**, seen not
      believed
- [ ] **4.2** DNS noted as the **fifth** phase, and the one the client does not control
- [ ] **4.2** `TODO(me)` — another client library audited: how many timeouts, what defaults, is there a
      total
- [ ] **4.2** answered out loud: *name the four phases, say which one a hung upstream actually trips, and
      explain why setting all four still does not bound the total*
- [ ] **4.3** read · `lab/deadline.py` written · **both bounds run against the identical server**
- [ ] **4.3** the timeout/deadline distinction stated as **duration versus instant**, not as two words for
      the same thing
- [ ] **4.3** `asyncio.timeout_at` understood, **including why it needs `AsyncClient`** — cancellation
      only takes effect at an `await`
- [ ] **4.3** the thread-wrapper failure understood: **`future.result(timeout=...)` bounds the caller and
      not the work**, and the worker stays held
- [ ] **4.3** `time.monotonic()` versus `time.time()` decided correctly for **both** cases — in-process,
      and across a process boundary
- [ ] **4.3** answered out loud: *the difference in one sentence, then why a thread wrapper does not bound
      the work*

---

## Section 5 — `05-the-two-together`

- [ ] **5.1** read · `lab/hop.py` written · **three copies started, deepest first**
- [ ] **5.1** the **flat** run done, and the wasted work counted: **when the client gave up versus when the
      chain stopped**
- [ ] **5.1** `client had already gone - the answer went nowhere` seen in the log, not inferred
- [ ] **5.1** the **budget** run done, and **the budget observed shrinking at each hop** (4.9 → 4.3 → 3.8
      on the reference machine)
- [ ] **5.1** `TODO(me)` — **a hop made to REFUSE on purpose** by shrinking the budget below its own cost
- [ ] **5.1** the inverted budget recognised as the common shape: **the deepest service with the loosest
      timeout**
- [ ] **5.1** the clock-skew trade-off understood — absolute instant versus remaining duration, and why
      gRPC chose the second
- [ ] **5.1** answered out loud: *the rule in one sentence · which hop in a five-service path gets the
      smallest timeout and why that is the opposite of what usually happens · what a hop should do when the
      budget is smaller than its own cost*
- [ ] **5.2** read · `lab/counter.py` and `lab/retry_client.py` written
- [ ] **5.2** the **control run** done first — `1 1` must print exactly `1` arrival, or everything after is
      contaminated
- [ ] **5.2** `TODO(me)` — **your prediction for 3 layers × 3 attempts written down before running it**
- [ ] **5.2** **27 arrivals from one user action** confirmed, and the difference from 9 understood as
      multiplying rather than adding
- [ ] **5.2** the herd run done **both ways**, and the two histograms compared
- [ ] **5.2** **the totals confirmed identical (120 and 120)** — jitter spreads load, it does not reduce it
- [ ] **5.2** the four retry rules stated: **bounded · spread · budgeted · safe to repeat**
- [ ] **5.2** `Retry-After` understood as **the server telling you when**, and overriding it recognised as
      overruling the only party who knows
- [ ] **5.2** idempotency understood, and **the key generated once per operation rather than per attempt**
- [ ] **5.2** answered out loud: *how many requests reach the bottom with 3 layers × 3 attempts and why it
      is not nine · what jitter changes and what it provably does not · the one thing a timeout does not
      tell you that makes retrying a `POST` dangerous*
- [ ] **5.3** read · **the AnyIO limiter read live rather than trusted** from the document
- [ ] **5.3** `lab/blackhole.py` written, **with the `held.append(conn)` line understood** — dropping the
      reference closes the socket and the drill silently stops working
- [ ] **5.3** `lab/hangy.py` written **as a copy**, and `pulse` confirmed untouched with `git status`
- [ ] **5.3** the drill run · **`/healthz` before recorded** (`http=200`, a few tens of milliseconds)
- [ ] **5.3** **`/healthz` during recorded** — `http=000`, `exit=28`, no HTTP response at all
- [ ] **5.3** **the blackhole's own count confirmed at `holding 40 connection(s)`** — the drill validated,
      not assumed
- [ ] **5.3** `TODO(me)` — **all six observations recorded**: healthz before, healthz during, connection
      count, processor reading, error count, last application log line
- [ ] **5.3** the drill re-run with **39** and the service confirmed to survive — *one request from a total
      outage, with every signal green*
- [ ] **5.3** the drill re-run with **`TIMEOUT=2`** and the trade understood: **forty visible errors
      instead of one invisible outage**, with the upstream just as broken
- [ ] **5.3** `def` versus `async def` understood — **40 versus 1** as the concurrency at which each dies
- [ ] **5.3** the restart recognised as **not a fix** — it drops the queue and the pool refills
- [ ] **5.3** answered out loud: *the number that decides when this happens and where it comes from · three
      signals that stayed green and why each was blind rather than broken · what setting a timeout actually
      bought you*

### 📄 The paper — `papers/congestion-avoidance-and-control.md`

- [ ] **paper** read · the 1988 collapse understood as **32 Kbps to 40 bps between two buildings four
      hundred yards apart**, caused by senders being impatient rather than by anything breaking
- [ ] **paper** the citation opened at `https://ee.lbl.gov/papers/congavoid.pdf` — **not taken on trust
      from this repository**
- [ ] **paper** `lab/congestion-avoidance-and-control/collapse.py` typed and both runs done · **250
      transmissions versus 172 for the identical 96 packets of useful work** confirmed
- [ ] **paper** the queue reading understood: **peak 40, pegged at the limit** is the collapse, and it is
      why the impatient timer also finished *later*
- [ ] **paper** the failure run done with `CAPACITY = 8` and `DAMAGE = 0.30`, and **`finished 10/12`**
      seen — backoff losing to a fixed timer when loss does **not** mean congestion
- [ ] **paper** the demo knobs put back (`CAPACITY = 2`, `DAMAGE = 0.0`) before moving on
- [ ] **paper** **what it did not claim** stated in your own words: *the word jitter appears nowhere in
      it*, the proof is explicitly out of scope, and it is about one connection's retransmit timer
- [ ] **paper** answered out loud: *why exponential and not linear · why exponential alone is not enough
      for thirty clients that failed at the same instant*

---

## Both red gates

- [ ] **Gate one** — the drill produced `http=200` before and **`http=000` `exit=28` during**, with the
      blackhole holding **40** connections
- [ ] **Gate one, green half** — `TIMEOUT=2` produced **forty `500`s and a `/healthz` answering in about
      two milliseconds**
- [ ] **Gate two** — the control printed `1`, and 3 layers × 3 attempts printed **27**
- [ ] neither gate produced a false pass: the forty requests were genuinely simultaneous, and nothing else
      on this machine was talking to port 8014

---

## The pattern across two days

- [ ] `TODO(me)` — **one paragraph written** on what Day 6's OOM drill and today's exhaustion drill have in
      common: two unrelated mechanisms, the same completely green dashboard
- [ ] the shared conclusion named: **resource metrics cannot see either failure**, and what that implies
      for what you will actually instrument on Day 62

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes confirmed, not assumed
- [ ] **the load generator was never pointed at anything but `127.0.0.1`** — checked, not remembered
- [ ] **`netstat -ano | grep -E ':80(0[0-9]|1[0-5]).*LISTENING'` returns nothing** — no server survives
- [ ] `pkill -f` verified with `netstat` rather than trusted, and `taskkill` used where it did not take
- [ ] `/tmp/a.log`, `/tmp/b.log`, `/tmp/c.log` removed
- [ ] **`lab/hangy.py` deleted** — the drill copy of `pulse` does not survive the day
- [ ] every lab file created today deleted, and `git status --short` clean
- [ ] **`pulse` confirmed unmodified** — `git diff pulse/` is empty

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — four measurement rows appended (ephemeral port range · default resolver ·
      `httpx2` version · anyio thread limiter)
- [ ] `docs/INCIDENTS.md` — **three rows appended, first symptom written before the cause** (rows 20, 21, 22)
- [ ] **row 22 explicitly linked to Day 6's row 19 and Day 5's row 16** — five consecutive days of
      diagnostic gaps, with Day 21 named as where they close
- [ ] `docs/DECISIONS.md` — an ADR written **if** the retries `TODO(me)` reached a conclusion about which
      layer owns them
- [ ] `docs/PROGRESS.md` — the Day 7 row pasted from the hub's §11
- [ ] `./o check` green
- [ ] `./o depth 7` green
- [ ] `./o trace` shows **FND-08** and **FND-09** closed and nothing else newly closed
- [ ] committed: `day 007: networking for operators — ports, DNS, TCP and the timeout — closes FND-08, FND-09`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
