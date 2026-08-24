# Day 6 — Checklist

**Definition of done.** `./o done 6` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd days/day-006-resources-and-the-oom-killer/lab && ./oom_drill.sh 64 2>&1 | tail -5
```

A service killed for memory with a request in flight, and the five observations that show every signal you
own was blind. Yesterday you could explain why a deleted file did not free disk. Today you can explain why
a dead service reported nothing at all.

---

## Setup

- [ ] **nothing from Day 4 or Day 5 still running** — `pgrep -af 'holder.py|chatty.py|burn|allocate|uvicorn'`
- [ ] **browser closed** and Addendum 02 §4's rule read: never measure with anything else starting up
- [ ] **`free -h` (or Task Manager) checked before starting** — today allocates up to 2.5 GiB deliberately
- [ ] `nproc` recorded — the denominator for every reading in section 2
- [ ] §3 step 4 run, and the **MISSING** list written down rather than skimmed
- [ ] `./o check` green and `git status --short` clean before breaking anything
- [ ] `./o scaffold 6` has created the day's `lab/`
- [ ] no packages added, and `git diff pyproject.toml uv.lock` confirms it

---

## Section 1 — `01-memory`

- [ ] **1.1** read · `lab/allocate.py` written · VSZ and RSS printed side by side for `pulse`
- [ ] **1.1** `lab/reserve.py` written · **1 GiB mapped for ~4 KiB of RSS**, then 64 MiB touched and RSS
      following — the divergence seen rather than believed
- [ ] **1.1** `TODO(me)` — `pulse`'s RSS **and** VSZ written into `docs/PACKAGES.md`
- [ ] **1.1** answered out loud: *8 GB of virtual size on a 4 GB machine with nothing wrong — how, and
      which number you would have read instead*
- [ ] **1.2** read · `lab/shared.py` written · **summed RSS and summed PSS compared, and the ratio noticed
      as equal to the process count**
- [ ] **1.2** the parent's `Private_Dirty` seen becoming `Shared_Dirty` at the moment of forking
- [ ] **1.2** `lab/mapshare.py` written · two processes mapping one file · PSS splitting between them
- [ ] **1.2** the 256 MiB `blob.bin` deleted and **`df` confirmed back to baseline**
- [ ] **1.2** `TODO(me)` — the ten-replicas-with-a-2 GB-model arithmetic done **both ways**, both numbers
      written down
- [ ] **1.2** answered out loud: *four processes at 500 MB RSS — smallest and largest possible real total,
      and the measurement that decides*
- [ ] **1.3** read · the `free` versus `available` distinction understood, or the Windows gap recorded
- [ ] **1.3** the 🅿️ parked cache experiment read, and **why `buff/cache` collapsing under an allocation is
      the system working** understood
- [ ] **1.3** answered out loud: *a node at 98% memory for a month with no incidents — what is happening,
      what should the dashboard plot, and the one distinction that decides whether high memory is dangerous*

---

## Section 2 — `02-cpu`

- [ ] **2.1** read · `lab/burn.py` written using **`multiprocessing`, not `threading`** — and why
      understood
- [ ] **2.1** run at 1 core, `nproc` cores and `2 × nproc` cores
- [ ] **2.1** **the total `%CPU` recorded at each level and confirmed constant** — the day's central
      measurement
- [ ] **2.1** the per-worker share confirmed halving at 2× oversubscription
- [ ] **2.1** `TODO(me)` — run also at `4 × nproc`, and the constancy of the total stated in one sentence
- [ ] **2.1** **every burner confirmed stopped** with `pgrep -af burn.py` before moving on
- [ ] **2.1** answered out loud: *what is identical between 4-on-4 and 40-on-4, what is ten times worse,
      and the metric that tells them apart*
- [ ] **2.2** read · `uptime` and `/proc/loadavg` compared, and the **`runnable/total` fourth field**
      noticed
- [ ] **2.2** load average measured **after 45 seconds**, not after 3 — and why understood
- [ ] **2.2** the state census run alongside, showing **which** state inflated the count
- [ ] **2.2** the 🅿️ parked I/O experiment read, and **`D` counting towards load on Linux** understood as
      the reason a load of 40 can accompany an idle processor
- [ ] **2.2** answered out loud: *load 8, processor 90% idle — the state, why more cores would not help,
      and the one command that would have told you*
- [ ] **2.3** read · `lab/burn_timed.py` written, using **`process_time` and `monotonic` together**
- [ ] **2.3** run unthrottled · **the wall-to-CPU ratio recorded** (should be ~1.0)
- [ ] **2.3** `TODO(me)` — that ratio written into `docs/PACKAGES.md` as the "before" number for Day 25
- [ ] **2.3** the multi-threaded trap understood: four threads against a one-core quota, and the fraction
      of each period spent frozen
- [ ] **2.3** answered out loud: *a container at its CPU limit on an idle node — what fraction of each
      period is it frozen, what does utilisation report, and which counter reveals it*

---

## Section 3 — `03-limits`

- [ ] **3.1** read · `/proc/self/cgroup` read, or the Windows gap recorded
- [ ] **3.1** the cgroup file table understood — **`cgroup.procs` as the thing you write a pid into**
- [ ] **3.1** the `sudo echo >` versus `echo | sudo tee` distinction understood **before** you need it
- [ ] **3.1** the 🅿️ parked by-hand cgroup creation read, and **`mkdir` being the creation API** noticed
- [ ] **3.1** answered out loud: *`memory.max` 256 MiB and `free` reporting 8 GiB — why both are true, and
      one concrete way a program is harmed by believing `free`*
- [ ] **3.2** read · the four thresholds distinguished — `max`, `high`, `min`, `low`
- [ ] **3.2** **`memory.high` never invoking the OOM killer** noted as an unconditional guarantee
- [ ] **3.2** the two 🅿️ parked runs compared: `oom_kill 1` with no brake, `high 3812` and `oom_kill 0` with
      one
- [ ] **3.2** **why almost nobody sets `memory.high`** understood — orchestrators do not expose it
- [ ] **3.2** answered out loud: *a container pinned at 100% of its memory limit for three weeks with no
      restarts — what is happening, which counter proves it, and what you should have alerted on*
- [ ] **3.3** read · the `cpu.max` conversion script run, and **`50000 100000` versus `25000 50000`**
      compared
- [ ] **3.3** requests mapping to `cpu.weight` and limits to `cpu.max` understood as **two different
      mechanisms**, not two strengths
- [ ] **3.3** **the memory/CPU asymmetry** stated in your own words: exceeding one kills, exceeding the
      other throttles, because CPU is time-shareable and a page is not
- [ ] **3.3** `TODO(me)` — a real service chosen and a **written argument** for or against a CPU limit
- [ ] **3.3** answered out loud: *two containers with the same ratio and different periods — what is
      identical, what differs, and which workload shape cares*

---

## Section 4 — `04-the-oom-killer`

- [ ] **4.1** read · the kernel documentation's OOM paragraph read **verbatim**, including the word *hope*
- [ ] **4.1** `oom_score` and `oom_score_adj` read for your own processes, or the gap recorded
- [ ] **4.1** **cgroup-scoped versus machine-wide** understood as the single most important distinction
- [ ] **4.1** why the killer uses `SIGKILL` and not `SIGTERM` understood — a graceful shutdown might need
      to allocate
- [ ] **4.1** answered out loud: *the database was killed and a small worker was leaking — why the kernel
      chose the database, and the one change that would have made the worker die instead*
- [ ] **4.2** read · a hand-sent `SIGKILL` used to produce `137` and **the process's silence observed**
- [ ] **4.2** the four record-keeping sources listed, **with each one's gap**
- [ ] **4.2** `dmesg -T` noted as the flag that makes kernel timestamps correlatable
- [ ] **4.2** **`OOMKilled: false` with exit 137** understood as a shutdown bug, not a memory one
- [ ] **4.2** answered out loud: *the three things that produce exit 137, the field that distinguishes the
      memory one, and why that field is not derived from the exit code*
- [ ] **4.3** read · `lab/hungry.py` written, with **module-level retention** and why understood
- [ ] **4.3** `lab/oom_drill.sh` written · **run with a request genuinely in flight**
- [ ] **4.3** the drill validated: the client's `time_total` is **less** than the `seconds` requested
- [ ] **4.3** `TODO(me)` — **all five observations recorded**: client result, exit code, shutdown line
      count, last application log line, and what `/healthz` returned immediately before
- [ ] **4.3** `TODO(me)` — a **fourth** blind signal found that the part does not name
- [ ] **4.3** **the drill server confirmed stopped** with `pgrep -af 'uvicorn hungry:app'`
- [ ] **4.3** answered out loud: *three signals that did not move, why each was blind, and the one that
      would have warned you beforehand*
- [ ] **4.4** read · the three pressure files read, or the unavailability recorded
- [ ] **4.4** **`cpu.some` measured at `nproc` and `2 × nproc` workers** — the ~1% versus ~50% contrast
      seen, against identical utilisation
- [ ] **4.4** `some` and `full` distinguished, and **why CPU has no `full` line** understood
- [ ] **4.4** `total` recognised as the field to scrape, and the `avg` fields as the ones for humans
- [ ] **4.4** **`/proc/pressure` not being namespaced** noted, and the cgroup files named as the container
      answer
- [ ] **4.4** answered out loud: *define `some` and `full`, say which you would page on and why, and
      explain why CPU has no `full`*

---

## Both red gates

- [ ] **Gate one** — total `%CPU` measured at `nproc` and `2 × nproc` and confirmed **identical**, while
      per-task time doubled
- [ ] **Gate two** — the OOM drill produced `http=000 exit=52`, exit `137`, **zero** shutdown lines, and a
      last log line that was a `200 OK`
- [ ] neither gate produced a false pass: the burn totals were not contaminated by other load, and the
      in-flight request was genuinely interrupted

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes, `0` network — confirmed, not assumed
- [ ] **`pgrep -af 'burn|allocate|shared|mapshare|hungry|uvicorn'` returns nothing** — no process is still
      holding memory or a core
- [ ] `blob.bin` and any other large files removed · **`df -h .` confirmed back to its starting value**
- [ ] `oom-drill.log` removed
- [ ] every lab file created today deleted, and `git status --short` clean
- [ ] **memory confirmed returned** — `free -h` (or Task Manager) back to roughly where §3 step 2 found it

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — four measurement rows appended (RSS/VSZ · cores · wall/CPU ratio · instruments
      available)
- [ ] `docs/INCIDENTS.md` — **three rows appended, first symptom written before the cause** (rows 17, 18, 19)
- [ ] **row 19 explicitly linked to Day 5's row 16** — four consecutive days of diagnostic gaps, with
      Day 21 named as where they close
- [ ] `docs/DECISIONS.md` — an ADR written **if** the CPU-limits `TODO(me)` reached a conclusion
- [ ] `docs/PROGRESS.md` — the Day 6 row pasted from the hub's §11
- [ ] `./o check` green
- [ ] `./o depth 6` green
- [ ] `./o trace` shows **FND-07** closed and nothing else newly closed
- [ ] committed: `day 006: resources — CPU, memory and the OOM killer — closes FND-07`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
