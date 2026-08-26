---
day: 6
phase: 1
phase_name: "The production mental model and the machine"
title: "Resources and the OOM killer"
ids: [FND-07]
principles: [1, 2, 4, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18]
kind: lab
plan_version: "v1.2.0"
parts: 13
generated: "2026-08-24"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 6 — Resources — CPU, memory, the OOM killer, and why your process was simply `Killed`

> **Yesterday (Day 5):** the filesystem, permissions, the disk that fills, and a log rotation that
> emptied every visible file while the disk kept filling and every check stayed green.
> **Today:** the two resources that are not stored but *consumed*, which are memory and processor: how
> they are measured, how they are limited, and the moment the kernel decides one of your processes has to
> go.
> **Tomorrow (Day 7):** networking for operators — ports, sockets, DNS, TCP, and the timeout that saves
> the system.

---

## §1 Where we are

Disk is a warehouse. Things sit in it, and if you look, you can count them. Memory and processor are not
like that at all. They are a room and a clock: space that is only yours while you are standing in it, and
time that is gone whether you used it or not.

That difference is why today's numbers lie in a way yesterday's did not.

Start with the plainest version. A hotel gives every guest a room number on a card. Room 400. The guest
believes the hotel has four hundred rooms. It has forty, and the number on the card is a lookup the porter
resolves. Several cards say 400 and point at different rooms, and two of them point at the same one. Add
up the numbers on the cards and you get a figure with no physical meaning whatsoever.

That is virtual memory, and it is why the first number most tools show you for "how much memory is this
using" is not a capacity number at all. There are four different correct answers to that question, and
choosing the wrong one is how people conclude a healthy service is about to fall over, or, more
expensively, set a limit ten times too large on every replica of every service, forever.

The processor has the mirror-image problem. A post office with one clerk shows "100% utilisation" whether
one person is waiting or forty. The metric reaches its ceiling exactly where the interesting behaviour
starts, so a dashboard that plots it shows a flat line across a tenfold change in how long everybody
waited.

Then the limits, which are where it gets sharp. A memory limit and a CPU limit sound like two settings of
the same kind and they are not. **Exceeding a CPU limit slows you down, and exceeding a memory limit
kills you**, with a signal that cannot be caught, so nothing is flushed, no shutdown runs, and the last
thing your service ever logged was a successful request. That asymmetry comes from one physical fact:
processor time can be shared and a page of memory cannot.

The day ends where the title says. You will drive `pulse` past a memory limit with a request in flight and
watch the client get an empty reply with no status code, the health check return 200 a moment before, the
error rate stay at zero, and the latency graph show nothing, because a request that is never answered has
no duration. **Every signal you own will be blind.** The only account of what happened is written by the
kernel, in a file your service cannot reach and does not know exists.

And then comes the signal that would have warned you, which the kernel added precisely because everything
else on this day answers the wrong question.

---

## §2 The map

**Section 1 — `01-memory`.** What "using memory" means, why the obvious number is not a capacity figure,
and why summing across processes overcounts.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [Virtual memory, and why the number is a lie](parts/01-memory/1.1-virtual-memory-and-why-the-number-is-a-lie.md) | a process shows 8 GB on a 4 GB machine and nothing is wrong — how? | foundation |
| 1.2 | [RSS, VSZ and the shared pages that make them add up wrong](parts/01-memory/1.2-rss-vss-and-shared-pages.md) | four processes at 500 MB each — what is the smallest total possible? | working |
| 1.3 | [The page cache that looks like a leak](parts/01-memory/1.3-the-page-cache-that-looks-like-a-leak.md) | 200 MB free of 64 GB — do you have a problem? | working |

**Section 2 — `02-cpu`.** What "using CPU" means, why utilisation saturates before the trouble starts, and
the slowdown that has no utilisation symptom at all.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [A core is a queue, not a speed](parts/02-cpu/2.1-a-core-is-a-queue-not-a-speed.md) | four tasks and forty tasks both report 100% — what differs tenfold? | foundation |
| 2.2 | [Load average, and what it is not](parts/02-cpu/2.2-load-average-and-what-it-is-not.md) | load 8, processor 90% idle — what state are the tasks in? | working |
| 2.3 | [Throttling — the slowdown with no symptom](parts/02-cpu/2.3-throttling-the-slowdown-with-no-symptom.md) | the pod is slow and the node is idle — why can it not use the spare cores? | production |

**Section 3 — `03-limits`.** How a limit is expressed and enforced: one mechanism, two resources, opposite
advice.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [cgroups — the box you put a process in](parts/03-limits/3.1-cgroups-the-box-you-put-a-process-in.md) | `memory.max` says 256 MiB and `free` says 8 GiB — how are both true? | foundation |
| 3.2 | [`memory.max` versus `memory.high` — the cliff and the brake](parts/03-limits/3.2-memory-max-versus-memory-high.md) | a container pinned at its limit for weeks with no restarts — what is happening? | working |
| 3.3 | [`cpu.max`, and the two numbers in it](parts/03-limits/3.3-cpu-max-and-the-two-numbers-in-it.md) | why always limit memory and rarely limit CPU? | working |

**Section 4 — `04-the-oom-killer`.** The moment the kernel chooses, what it leaves behind, and the signal
that would have told you first.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [What the OOM killer actually does](parts/04-the-oom-killer/4.1-what-the-oom-killer-actually-does.md) | why was the database killed when a small worker was leaking? | working |
| 4.2 | [Exit 137, and the message that is not in your log](parts/04-the-oom-killer/4.2-exit-137-and-the-message-that-is-not-in-your-log.md) | three things send signal 9 — which field tells them apart? | production |
| 4.3 | [OOM-killing `pulse` on purpose](parts/04-the-oom-killer/4.3-oom-killing-pulse-on-purpose.md) | name three signals that did not move at all | production |
| 4.4 | [Pressure — the signal that warns you first](parts/04-the-oom-killer/4.4-pressure-the-signal-that-warns-you-first.md) | `some` versus `full` — which do you page on? | production |

---

## §3 Setup — run this

**Stop first — and today this genuinely matters.** Close the browser. Stop anything from Day 4 or Day 5.
Confirm nothing is burning a core or holding a file:

**Profile:** `core` only (Addendum 02 §4), and today you are deliberately pushing against the machine's
limits rather than living inside them. Addendum 02 §4 rule 1 applies with force: **never measure with
anything else starting up.**

```bash
# 1 — nothing from previous days survives
pgrep -af 'holder.py|chatty.py|burn|allocate|uvicorn|while True' || echo "nothing running"

# 2 — YOUR HEADROOM. Today allocates up to 2.5 GiB deliberately.
free -h 2>/dev/null || echo "no free(1) — Windows; check Task Manager, and halve every number in this day"

# 3 — the denominator for everything in section 2
nproc

# 4 — which of today's instruments exist on this machine
for f in /proc/meminfo /proc/loadavg /proc/pressure/cpu /sys/fs/cgroup/cgroup.controllers; do
  [ -r "$f" ] && echo "ok      $f" || echo "MISSING $f"
done

# 5 — gate green, tree clean, before you break anything
./o check && git status --short

# 6 — this day's scratch folder
./o scaffold 6
```

⚠️ **Step 2 is a safety check with teeth.** Part 4.3 allocates up to 2.5 GiB on a machine with about
11.7 GiB total and roughly 5 GB of genuine headroom (`docs/PACKAGES.md`, Day 0 · Addendum 02 §4).
**Getting it wrong does not produce a lesson — it produces a machine-wide out-of-memory event in which
the kernel picks a victim you did not choose**, possibly your editor with unsaved work. If you are
unsure, halve every number in this day; the demonstrations all work at half scale.

⚠️ **Step 4 will report most things missing.** This machine has no `/proc/pressure`, no cgroup v2, no
`free`, and no `smaps_rollup`. **That is the fourth consecutive day with a diagnostic gap here**, and it
is now a pattern rather than an inconvenience — it belongs in `docs/INCIDENTS.md`, and Day 21's WSL2
setup is where it closes. **Most of sections 3 and 4 are 🅿️ parked for exactly this reason**, and the
parts say so where it applies.

**No packages are added today.** Third day running.

---

## §4 Build brief

No project code. `pulse` is unchanged, and the one file that resembles it — `lab/hungry.py` — is a drill
copy that is deleted at the end of the day.

| File | Explained in | What it is |
| --- | --- | --- |
| `lab/allocate.py` | [1.1](parts/01-memory/1.1-virtual-memory-and-why-the-number-is-a-lie.md) | **Yours to write** — allocate, touch, and report both memory numbers |
| `lab/reserve.py` | [1.1](parts/01-memory/1.1-virtual-memory-and-why-the-number-is-a-lie.md) | **Yours to write** — map 1 GiB, touch 64 MiB, watch RSS not follow |
| `lab/shared.py` | [1.2](parts/01-memory/1.2-rss-vss-and-shared-pages.md) | **Yours to write** — fork three children and compare summed RSS with summed PSS |
| `lab/mapshare.py` | [1.2](parts/01-memory/1.2-rss-vss-and-shared-pages.md) | **Yours to write** — two processes mapping one file; the Day 109 decision in miniature |
| `lab/burn.py` | [2.1](parts/02-cpu/2.1-a-core-is-a-queue-not-a-speed.md) | **Yours to write** — occupy exactly N cores for a fixed period |
| `lab/burn_timed.py` | [2.3](parts/02-cpu/2.3-throttling-the-slowdown-with-no-symptom.md) | **Yours to write** — the wall-clock to processor-time ratio, and `cpu.stat` |
| `lab/hungry.py` · `lab/oom_drill.sh` | [4.3](parts/04-the-oom-killer/4.3-oom-killing-pulse-on-purpose.md) | **Yours to write** — the day's deliberate failure |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — four measurement rows |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — three rows, first symptom before cause |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.1](parts/01-memory/1.1-virtual-memory-and-why-the-number-is-a-lie.md), measure
  `pulse`'s RSS and VSZ and write **both** into `docs/PACKAGES.md`. Day 42 sets a limit against the first
  and Day 109 will change it by an order of magnitude.
- `TODO(me)` In [1.2](parts/01-memory/1.2-rss-vss-and-shared-pages.md), work out from first principles what
  ten replicas holding a 2 GB model would cost — loaded into each heap, versus memory-mapped from one
  file. Write both numbers down. **That arithmetic is Day 109's most consequential decision** and it is
  cheap to do now.
- `TODO(me)` In [2.1](parts/02-cpu/2.1-a-core-is-a-queue-not-a-speed.md), run the burner at `nproc`,
  `2×nproc` and `4×nproc` and record the total `%CPU` and each worker's share at each level. **The total
  is constant. Say in one sentence what that constancy means for anyone alerting on CPU utilisation.**
- `TODO(me)` In [2.3](parts/02-cpu/2.3-throttling-the-slowdown-with-no-symptom.md), record the
  unthrottled wall-to-CPU ratio. **You need the "before" number** — Day 25 runs the identical script under
  `--cpus 0.5` and the comparison is the measurement.
- `TODO(me)` In [3.3](parts/03-limits/3.3-cpu-max-and-the-two-numbers-in-it.md), find a real service you
  use and decide, with reasons, whether it should have a CPU limit. Write the argument down. **"Because
  the policy says so" is not an argument.**
- `TODO(me)` Do the [4.3](parts/04-the-oom-killer/4.3-oom-killing-pulse-on-purpose.md) drill and record
  **all five** observations: what the client saw, the exit code, the shutdown line count, the last
  application log line, and what `/healthz` was returning immediately before.
- `TODO(me)` Find a **fourth** signal that would have been blind during the 4.3 drill and that the part
  does not name.
- `TODO(me)` Delete every lab file, confirm with `pgrep -af` that no burner, allocator or drill server
  survives, and prove the tree is clean with `git status --short`.

---

## §5 The check that must be able to fail

Two red gates, and both are red in the sense that **the failure is invisible to everything that is
supposed to see it.**

**Gate one: utilisation cannot distinguish comfortable from catastrophic.**

```bash
uv run python days/day-006-resources-and-the-oom-killer/lab/burn.py "$(nproc)" 15 & sleep 8; ps -eo %cpu --no-headers --sort=-%cpu | head -"$(nproc)" | awk '{s+=$1} END {printf "total %%CPU: %.0f\n", s}'; wait
uv run python days/day-006-resources-and-the-oom-killer/lab/burn.py "$(( $(nproc) * 2 ))" 15 & sleep 8; ps -eo %cpu --no-headers --sort=-%cpu | head -"$(( $(nproc) * 2 ))" | awk '{s+=$1} END {printf "total %%CPU: %.0f\n", s}'; wait
```

| Workers | Total `%CPU` | Load average | Time per task |
| --- | --- | --- | --- |
| `nproc` | ~400 | ~4 | baseline |
| `2 × nproc` | **~400 — identical** | ~8 | **doubled** |

**The gate is that the first column does not move.** If your two totals differ by more than a few percent,
something else was running and the measurement is contaminated — stop it and repeat.

**Gate two: the OOM drill leaves every signal green.**

```bash
cd days/day-006-resources-and-the-oom-killer/lab && ./oom_drill.sh 64 2>&1 | tail -5
```

| Observation | Expected |
| --- | --- |
| client's in-flight request | `http=000 exit=52` — **no status code at all** |
| server exit code | `137` |
| shutdown log lines | **`0`** |
| last application log line | **a `200 OK`** |
| `/healthz` immediately before | **`200`** |

**If the in-flight request returns `http=200`, the drill is lying to you** — the process died after the
request completed, so nothing was in flight and nothing was measured. The client's `time_total` must be
**less** than the `seconds` you asked for.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline until Day 13. |
| Network | **0** | Nothing downloaded; no packages added. |
| **RAM** | **up to 2.5 GiB, deliberately** | 512 MiB in 1.1 · ~350 MB in 1.2 · **2.5 GiB peak in 4.3** · 512 MiB in the parked 4.4. **The largest figure in this curriculum, against ~5 GB of genuine headroom.** All returns at process exit. |
| **Processor** | **all cores, in bursts of 15–60 s** | Sections 2 and 4.4. The machine is unresponsive while each burn runs and recovers completely afterwards. |
| Disk | **~256 MiB temporarily** | `blob.bin` in 1.2, deleted; 2 GiB in the parked 1.3 experiment on Day 21. |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). |

**The RAM row is the one to read before you start.** Unlike Day 5's disk — which had to be reclaimed
explicitly and sometimes could not be
([Day 5, part 3.2](../day-005-linux-for-operators-ii/parts/03-the-disk-that-fills/3.2-the-deleted-file-that-still-costs-you-a-gigabyte.md))
— memory returns automatically when a process exits. **The hazard is not leaving it behind; it is
exceeding the machine while it is held.**

---

## §7 Traps

**`VSZ` is not a capacity number.** A JVM with `-Xmx4g` shows gigabytes of virtual size and might have a
200 MB resident set. Alert on RSS against a limit, never on VSZ.
Part [1.1](parts/01-memory/1.1-virtual-memory-and-why-the-number-is-a-lie.md).

**Summing RSS across processes double-counts shared pages.** Eight forked workers at 500 MB each might
total 4 GB or 900 MB. PSS is the figure that adds up, and the cgroup's own number is the one the limit is
enforced against. Part [1.2](parts/01-memory/1.2-rss-vss-and-shared-pages.md).

**`free` is the wrong column.** A healthy machine that has been up for a while shows almost no free
memory, because the kernel uses spare RAM as page cache. **Read `available`.** Alerting on `free`
produces a permanent red light. Part [1.3](parts/01-memory/1.3-the-page-cache-that-looks-like-a-leak.md).

**Load average counts `D` as well as `R` on Linux.** A load of 40 with an idle processor is a stalled
disk, not contention, and more cores would change nothing. One command distinguishes them:
`ps -eo stat --no-headers | cut -c1 | sort | uniq -c`.
Part [2.2](parts/02-cpu/2.2-load-average-and-what-it-is-not.md).

**`/proc/loadavg`, `/proc/meminfo` and `/proc/pressure` are not namespaced.** Inside a container they
report the *host's* numbers. Use the cgroup's own files. Parts
[2.2](parts/02-cpu/2.2-load-average-and-what-it-is-not.md),
[3.1](parts/03-limits/3.1-cgroups-the-box-you-put-a-process-in.md) and
[4.4](parts/04-the-oom-killer/4.4-pressure-the-signal-that-warns-you-first.md).

**`sudo echo x > /privileged/file` does not work.** The shell performs the redirect as *you*, before
`sudo` runs. Use `echo x | sudo tee`.
Part [3.1](parts/03-limits/3.1-cgroups-the-box-you-put-a-process-in.md).

**`cpu: 0.5m` is half a millicore, not 500m.** A thousand-fold error that produces a workload frozen for
99.5% of every period, with utilisation reading a rounding error.
Part [3.3](parts/03-limits/3.3-cpu-max-and-the-two-numbers-in-it.md).

**Exit 137 has three possible senders.** Memory kill, grace-period expiry, or a human. The exit code
cannot tell them apart; `OOMKilled` — a separately observed boolean — can. **Teams routinely spend days
raising memory limits to fix a shutdown-handler bug.**
Part [4.2](parts/04-the-oom-killer/4.2-exit-137-and-the-message-that-is-not-in-your-log.md).

**The named trap from plan §5.1 that this day touches:** *the capability without a bound.* A process with
no memory limit is a capability with no brake — and its blast radius is not itself but **the whole node**,
because a machine-wide out-of-memory event scores every process and usually kills the largest rather than
the guilty one. Setting a limit is what converts an unbounded failure into a contained one.
Part [4.1](parts/04-the-oom-killer/4.1-what-the-oom-killer-actually-does.md).

---

## §8 Verify before you build

Fetched on **2026-08-24**, not recalled:

| Page | Used for |
| --- | --- |
| `docs.kernel.org/admin-guide/mm/concepts.html` | virtual addresses and translation; pages; page cache; anonymous memory; **the OOM killer paragraph, verbatim** |
| `docs.kernel.org/admin-guide/cgroup-v2.html` | `memory.current`, `memory.max`, `memory.high`, `memory.min`, `memory.low`, `memory.events`, `memory.stat`, `cpu.max`, `cpu.stat` with `nr_throttled` and `throttled_usec` — **all quoted verbatim** |
| `docs.kernel.org/accounting/psi.html` | what PSI is; the three files; **`some` and `full` verbatim**; `avg10`/`avg60`/`avg300`/`total` |
| Day 4's fetched pages | `signal(7)` for `SIGKILL` being uncatchable; `wait(2)` for how `137` is constructed |

⚠️ **Two things this day names that are not verified from a fetched page**, and both are flagged where
they appear: the `python:3.12-slim` image tag in
[2.3](parts/02-cpu/2.3-throttling-the-slowdown-with-no-symptom.md), which carries
`TODO(docker manifest inspect python:3.12-slim)` to check on the day you run it; and the exact `dmesg`
output format, which is reproduced from a real kernel log and **will differ in detail between kernel
versions** — read the words, not the byte offsets.

---

## §9 Say it in an interview

*"The thing that reorganised how I think about resources was noticing that the standard metrics answer a
different question from the one I have. CPU utilisation is a fraction of time a core was busy — it reads
100% whether one task is waiting or forty, so it saturates exactly where the interesting behaviour
starts. Load average fixes the depth problem and introduces another, because on Linux it counts tasks
blocked in uninterruptible disk sleep as well as runnable ones, so a load of 40 with an idle processor is
a failing disk and adding cores does nothing. And memory usage includes page cache, which is reclaimable,
so a container pinned at its limit for weeks with no restarts is usually completely healthy.*

*"The asymmetry that matters operationally is between the two limits. Exceeding a CPU limit throttles you
— the cgroup is descheduled for the rest of each 100-millisecond period, so you sit frozen while the node
has idle cores and nothing in the utilisation metrics shows it; the evidence is `nr_throttled`. Exceeding
a memory limit kills you, with `SIGKILL`, so no handler runs and nothing is flushed. That is why I always
set memory limits — without one, a leak causes a node-wide OOM and the kernel picks the biggest process,
which is usually the database rather than the leak — and why I think hard before setting a CPU limit at
all.*

*"I OOM-killed my own service with a request in flight to see what my signals would say. The client got an
empty reply with no status code, so it was indistinguishable from a network failure. Error rate did not
move, because a dropped connection is not a 5xx. Latency did not move, because an unanswered request has
no duration. The health check returned 200 a moment before and was not wrong. And the last thing the
service logged was a successful request — it cannot log its own death, because the signal is not
delivered. The two things that would have helped were working set against the limit, which warns
beforehand, and pressure stall information, which reports the fraction of time tasks spent unable to make
progress, per resource, and does not saturate. I have not run this at fleet scale; what I have done is
cause each failure deliberately and write down what I saw before I knew the cause."*

---

## §10 Done when

`days/day-006-resources-and-the-oom-killer/CHECKLIST.md` has no unticked boxes, and `./o done 6` refuses
to commit until that is true.

Done is defined by understanding and green checks, never by elapsed time. Specifically: you can look at a
memory number and say which of the four it is; you have watched CPU utilisation stay identical across a
tenfold change in waiting; you have killed `pulse` for memory and confirmed that every one of your signals
was blind; and **every process you started is confirmed stopped**, because today's leftovers hold gigabytes.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append this row verbatim, replacing the commit hash with your own after
committing:

```text
| 6 | 2026-08-24 | FND-07 | 13 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — no package rows today. Four measurement rows:

```text
| pulse: RSS / VSZ | <n> MiB / <n> MiB | 2026-08-24 | 6 | From Day 6 part 1.1. RSS is what Day 42's memory limit is set against; VSZ is recorded to show the ratio. Day 109 changes RSS by an order of magnitude when a model loads. |
| machine: cores | <nproc> | 2026-08-24 | 6 | The denominator for every load-average and utilisation reading. Day 0 recorded 4; confirm it here. |
| pulse: wall/CPU ratio, unthrottled | <n.nn>x | 2026-08-24 | 6 | From `burn_timed.py` with no CPU limit, Day 6 part 2.3. **The "before" number** — Day 25 runs the identical script under `--cpus 0.5`. |
| machine: instruments available | <list of MISSING from §3 step 4> | 2026-08-24 | 6 | Which of PSI, cgroup v2, `free`, `smaps_rollup` exist here. Fourth consecutive day with a diagnostic gap; Day 21's WSL2 setup closes it. |
```

**`docs/INCIDENTS.md`** — three rows, and **write the first symptom before you investigate**:

```text
| 17 | 2026-08-24 | 6 | OOM-killed `pulse` (drill copy) with a request in flight, part 4.3 | <what the client printed, verbatim — including the http code and curl exit> | <what you found> | <smallest fix> | <what you changed so it cannot happen silently again> |
| 18 | 2026-08-24 | 6 | Ran 2× as many CPU burners as cores, part 2.1 | <the total %CPU, both times> | Utilisation is identical at 1× and 2× oversubscription; only load average and PSI moved | none — the finding is the metric's blindness | Noted that a CPU-utilisation alert cannot see a doubling of latency |
| 19 | 2026-08-24 | 6 | Environmental — no `/proc/pressure`, no cgroup v2, no `free`, no `smaps_rollup` on this machine | <what §3 step 4 printed> | Git Bash over Windows exposes none of the Linux resource-accounting interfaces; most of sections 3 and 4 are 🅿️ parked | none — run them in WSL2 from Day 21 | Fourth consecutive day recording a diagnostic gap. **Link this row to Day 5 row 16** and make Day 21 close both |
```

⚠️ **Row 19 is the fourth of its kind** (Day 5 row 16 was the third). **Link them explicitly.** A single
"this tool is missing" note gets forgotten; four linked rows with a named closing day is a finding with an
owner, and it is the difference between Day 21 being a setup chore and Day 21 closing a documented gap.

**`docs/DECISIONS.md`** — an ADR is worth writing **if** your `TODO(me)` on CPU limits reached a
conclusion. *"We set memory limits always and CPU limits only for untrusted tenants, because exceeding
memory kills and exceeding CPU only throttles"* is exactly the shape of a decision that is expensive to
reverse and non-obvious to a stranger, and Day 42 will implement whatever you decide.

**The commit:**

```text
day 006: resources — CPU, memory and the OOM killer — closes FND-07
```
