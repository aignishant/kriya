---
day: 4
phase: 1
phase_name: "The production mental model and the machine"
title: "Linux for operators I"
ids: [FND-05]
principles: [1, 2, 4, 7, 8, 10, 11, 12, 13, 16, 17, 18]
kind: lab
plan_version: "v1.2.0"
parts: 14
generated: "2026-08-24"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 4 — Linux for operators I — processes, signals, exit codes, and what "the service died" really means

> **Yesterday (Day 3):** `pulse` v0 became a running process — three routes, three pinned packages, four
> tests, and a health check that answers truthfully about the only thing it claims to know.
> **Today:** the thing you started yesterday gets taken apart. What a process actually is, how you talk
> to one, what it says on the way out, and why "the service died" is four words hiding four completely
> different events.
> **Tomorrow (Day 5):** Linux for operators II — the filesystem, permissions, the disk that fills and the
> log that must rotate.

---

## §1 Where we are

Yesterday you typed a command and something started answering on port 8000. Today is about the thing
that started.

Here is the shape of the problem, without any jargon. There is a recipe card in a drawer and there is a
meal being cooked. They are related — the meal came from the card — and they are completely different
objects. You can edit the card while the meal cooks and nothing on the stove changes. You can burn the
meal without the card being wrong. Almost every confusing conversation about a running system is one
person talking about the card while the other talks about the stove.

The card is your code. The meal is a **process**, and it is the only thing any operational verb ever
acts on. Restart, kill, scale, limit memory, drain, replace — all of them are about the meal, never the
card. This sounds obvious and it is not: the single most common false diagnosis in operations is *"I
deployed the fix and the bug is still there"*, which is nearly always *"the fix is not running"* — an
instance that was never replaced, cooking from yesterday's card.

Once you can see the process as a thing in its own right, three questions become askable, and the day is
built out of them.

**How do you talk to it?** You cannot call a function in a running process from outside. What you have
is a doorbell with about thirty buttons and no message field — a **signal**. `Ctrl-C` is one of the
buttons. So is the thing your container runtime presses when it wants your service to stop, and so is
the thing the kernel presses when the machine is out of memory. The whole art of stopping a service
without dropping work is: which button, who is allowed to press it, what your program does when it
rings, and the fact that exactly two of the buttons cannot be answered at all.

**What does it say on the way out?** One number, between 0 and 255. Not a message, not a log line — one
number, handed only to whoever started it. Every automated decision about whether something worked is
made from that number and from nothing else. Your CI pipeline reads it. Your container's restart policy
reads it. `./o check` has been reading it since Day 0 and you have never looked at how.

**And what does "it died" actually mean?** Today's answer is uncomfortable. Of the four ways an in-flight
request gets destroyed during a shutdown, three of them leave the server's own logs, its error rate and
its exit status looking entirely normal — because from the process's point of view nothing went wrong.
It was stopped. Correctly. By something entitled to stop it. And the work was lost anyway, and the only
place it is visible is at the client.

That last finding is the reason today is a lab and not a reading day. You will break shutdown four ways
and watch every signal you own stay green.

---

## §2 The map

**Section 1 — `01-the-process`.** The object itself: what it is, where it sits in the tree of everything
running, how to find it, and what state it is in. Everything else today acts on this object.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A process is not a program](parts/01-the-process/1.1-a-process-is-not-a-program.md) | why does the running service still return the old answer after you edited the file? | foundation |
| 1.2 | [The PID, the parent, and the process tree](parts/01-the-process/1.2-pid-parent-and-the-process-tree.md) | why did closing the terminal stop the service you never told to stop? | foundation |
| 1.3 | [Reading `ps`, and finding your service when you have lost it](parts/01-the-process/1.3-reading-ps-and-finding-your-service.md) | which two columns do beginners omit, and what false conclusion does each prevent? | working |
| 1.4 | [Process states, and the `D` that will not die](parts/01-the-process/1.4-process-states-and-the-d-that-will-not-die.md) | the service accepts connections and answers nothing, and the processor graph is flat — what state is it in? | working |

**Section 2 — `02-signals`.** The only channel you have to a running process. One number, no payload, a
fixed vocabulary, and two entries that cannot be refused.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [What a signal actually is](parts/02-signals/2.1-what-a-signal-actually-is.md) | how does a process tell "shut down, we are deploying" from "shut down, you are out of memory"? | foundation |
| 2.2 | [`SIGTERM` and `SIGKILL` — the request and the order](parts/02-signals/2.2-sigterm-and-sigkill-the-request-and-the-order.md) | why does a hard-killed process write no shutdown log line even though its shutdown code is perfectly good? | working |
| 2.3 | [Catching a signal in Python](parts/02-signals/2.3-catching-a-signal-in-python.md) | your service logs "caught SIGTERM" and keeps running forever — name two causes | working |
| 2.4 | [The signals you cannot catch](parts/02-signals/2.4-the-signals-you-cannot-catch.md) | why is a stopped process arguably more dangerous to a live system than a killed one? | production |

**Section 3 — `03-exit-codes`.** What the process hands back, who reads it, and the fact that your gate
has been living on it since Day 0.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [The exit code is the whole return value](parts/03-exit-codes/3.1-the-exit-code-is-the-whole-return-value.md) | which three exit codes mean "never ran", "could not be executed" and "was killed"? | foundation |
| 3.2 | [`128 + N` — when a signal becomes an exit code](parts/03-exit-codes/3.2-128-plus-n-when-a-signal-becomes-an-exit-code.md) | `137` appears in your logs — name the three possible senders and the one field that identifies which | working |
| 3.3 | [The exit code your gate already reads](parts/03-exit-codes/3.3-the-exit-code-your-gate-already-reads.md) | `./o check` prints `OK all green` — name two situations that produce exactly that | production |

**Section 4 — `04-the-service-died`.** The three sections above, applied to `pulse`, ending in the day's
deliberate failure and the structural bug that causes it in production.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [Graceful shutdown for `pulse`](parts/04-the-service-died/4.1-graceful-shutdown-for-pulse.md) | why must the listening socket close *before* in-flight requests drain, not after? | production |
| 4.2 | [The shutdown that dropped requests](parts/04-the-service-died/4.2-the-shutdown-that-dropped-requests.md) | three of four breakages leave every server-side signal normal — why, and where is the loss visible? | production |
| 4.3 | [Zombies, orphans, and why PID 1 is a job](parts/04-the-service-died/4.3-zombies-orphans-and-pid-1.md) | name the two duties PID 1 has that no other process has, and the one word that fixes both | production |

---

## §3 Setup — run this

**Stop first:** nothing needs stopping, but **check nothing is already listening on 8000 or 8010** —
today runs two servers and a forgotten one from Day 3 will produce a confusing bind error rather than a
confusing lesson.

**Profile:** `core` only (Addendum 02 §4), and today `core` still means one Python process. At two points
today you will briefly run **two** uvicorn processes — `pulse` on 8000 and the drill on 8010 — at about
60 MB each. That is the first time this curriculum has had two of anything running. Stop the drill when
you are done with it.

**No packages are added today.** Everything used is either already installed from Day 3 or is a standard
Unix tool. This is the first day since Day 0 with an empty `docs/PACKAGES.md` diff, and it is worth
noticing: a day can be substantial and add no dependencies.

```bash
# 1 — confirm both ports are free before you start
netstat -ano | grep -E ':(8000|8010).*LISTENING' || echo "8000 and 8010 both free"

# 2 — confirm the gate is green and the tree is clean before you break anything
./o check && git status --short

# 3 — this day's scratch folder
./o scaffold 4

# 4 — confirm the tools this day reads output from actually exist here
for t in ps pgrep pkill kill netstat curl; do
  command -v "$t" >/dev/null && echo "ok   $t" || echo "MISSING $t"
done
```

⚠️ **Step 4 matters more than it looks.** This day is built on reading tool output, and Git Bash on
Windows ships a subset of the usual Unix toolkit. If `pgrep` or `pkill` is missing, the parts tell you
the `ps | grep` equivalent — and part 1.3 explains why the bracket trick exists.

⚠️ **Signal numbers differ here.** `kill -l` in Git Bash uses the Cygwin numbering, in which `SIGSTOP`
is 17 and `SIGCHLD` is 20 — not the Linux 19 and 17. **Send signals by name, never by number.** Part 2.1
has the observed listing.

---

## §4 Build brief

Today writes **no project code**. Nothing under `pulse/` changes, and that is deliberate: `pulse` already
shuts down gracefully because uvicorn does, and today is about proving and breaking that rather than
building it. Everything you write lives in this day's `lab/` and is deleted at the end.

| File | Explained in | What it is |
| --- | --- | --- |
| `lab/handler.py` | [2.3](parts/02-signals/2.3-catching-a-signal-in-python.md) | **Yours to write** — the smallest honest handler: set a flag, return |
| `lab/blocked_handler.py` | [2.3](parts/02-signals/2.3-catching-a-signal-in-python.md) | **Yours to write** — proves a Python handler cannot interrupt a long C call |
| `lab/uncatchable.py` | [2.4](parts/02-signals/2.4-the-signals-you-cannot-catch.md) | **Yours to write** — watch the kernel refuse a `SIGKILL` handler |
| `lab/blocking.py` | [2.4](parts/02-signals/2.4-the-signals-you-cannot-catch.md) | **Yours to write** — `SIGTERM` blocks, `SIGKILL` does not |
| `lab/wait_status.py` | [3.2](parts/03-exit-codes/3.2-128-plus-n-when-a-signal-becomes-an-exit-code.md) | **Yours to write** — the raw status word the shell hides behind `137` |
| `lab/slow_probe.py` | [4.1](parts/04-the-service-died/4.1-graceful-shutdown-for-pulse.md) | **Yours to write** — a copy of `pulse` with one slow route, so shutdown has something to drain |
| `lab/drop_drill.sh` | [4.2](parts/04-the-service-died/4.2-the-shutdown-that-dropped-requests.md) | **Yours to write** — the harness that reports what the *client* saw |
| `lab/deaf_wrapper.sh` | [4.2](parts/04-the-service-died/4.2-the-shutdown-that-dropped-requests.md) | **Yours to write** — breakage 1: an inherited ignore |
| `lab/zombie.py` | [4.3](parts/04-the-service-died/4.3-zombies-orphans-and-pid-1.md) | **Yours to write** — three zombies, then reap them |
| `lab/no_exec.sh` · `lab/with_exec.sh` | [4.3](parts/04-the-service-died/4.3-zombies-orphans-and-pid-1.md) | **Yours to write** — one word apart, opposite outcomes |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — three rows, first symptom before cause |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.1](parts/01-the-process/1.1-a-process-is-not-a-program.md), find the *fourth* thing
  copied at process creation that the part does not list. Prove it with a command that shows the running
  process disagreeing with the current state of the machine.
- `TODO(me)` In [1.4](parts/01-the-process/1.4-process-states-and-the-d-that-will-not-die.md), take the
  state census on your own machine and write the result into `docs/PACKAGES.md` next to the machine rows.
  **You need to know what normal looks like before you can recognise abnormal**, and this is the cheapest
  possible baseline.
- `TODO(me)` Produce state `D` on purpose. It is genuinely hard on a healthy laptop — that is the point.
  Write down what you tried and why each attempt failed; the reasoning is the exercise, not the result.
- `TODO(me)` In [2.3](parts/02-signals/2.3-catching-a-signal-in-python.md), rewrite `handler.py` using a
  `threading.Event` instead of a global boolean, and say in one sentence which class of bug that removes.
- `TODO(me)` In [3.3](parts/03-exit-codes/3.3-the-exit-code-your-gate-already-reads.md), find a **second**
  hole in `./o check` that the parts do not name — a way to make it print `OK all green` while something
  real is wrong. Row 9 of `docs/INCIDENTS.md` is one that Day 0 already found; find another.
- `TODO(me)` Measure `pulse`'s drain duration with the command in
  [4.1](parts/04-the-service-died/4.1-graceful-shutdown-for-pulse.md) and write the number into
  `docs/PACKAGES.md`. Day 41 needs it.
- `TODO(me)` Do **all four** breakages in [4.2](parts/04-the-service-died/4.2-the-shutdown-that-dropped-requests.md),
  including reasoning through breakage 4, which cannot be produced with uvicorn. Say what server behaviour
  would be required to produce it.
- `TODO(me)` Delete every file in this day's `lab/` and prove the working tree is clean with `git status
  --short`. A drill that leaves the system modified is an incident you caused.

---

## §5 The check that must be able to fail

Today has **two** red gates, and they fail in opposite directions — which is the point.

**Gate one: the shutdown drill must show a lost request.** Run the harness from
[4.2](parts/04-the-service-died/4.2-the-shutdown-that-dropped-requests.md) in `hardkill` mode:

```bash
cd days/day-004-linux-for-operators-i/lab && ./drop_drill.sh hardkill
```

| Mode | Client sees | Server exit | Shutdown log lines |
| --- | --- | --- | --- |
| `clean` | `http=200` after the full request | `0` | `2` |
| `nosignal` | `http=200`, but nothing shut down | `143` | **`0`** |
| `hardkill` | `http=000 exit=52` — empty reply | `137` | **`0`** |
| `shortgrace` | `http=000 exit=52` — empty reply | `137` | **`1`** |

**If `hardkill` shows `http=200`, the drill is lying to you** — the request finished before the kill
landed, so nothing was in flight and nothing was measured. That is the same class of error as a gate
that is green because it checked nothing, and part 4.2's *When it breaks* covers how to tell.

**Gate two: `./o check` must be able to be green while nothing is tested.** This is the uncomfortable
one, and it is Day 0's `docs/INCIDENTS.md` row 4 arriving at the expiry date it predicted:

```bash
git mv tests/test_api.py tests/api_tests.py && ./o check; echo "gate exit: $?"; git mv tests/api_tests.py tests/test_api.py
```

Expected: `OK all green` and `gate exit: 0`, with zero tests collected.
[3.3](parts/03-exit-codes/3.3-the-exit-code-your-gate-already-reads.md) walks through why, and Day 14
closes it with a minimum test count. **Today's job is to have watched it, not to fix it** — the fix has a
day of its own and fixing it here would put the plan out of order.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline until Day 13. **Last day this is free by default** — from Day 13 every `./o check` run costs against a free-tier budget. |
| Network | **0** | Nothing is downloaded. No packages are added today. |
| RAM | **~60 MB, briefly ~120 MB** | One `pulse` at ~60 MB; during the shutdown drills a second uvicorn on port 8010 at ~60 MB. **Stop the drill server when you finish with it.** |
| Processor | **up to 1 core, briefly** | `blocked_handler.py` and the busy loop in 1.4 each pin one core until killed. On four cores that is 25% of the machine. **Kill them.** |
| Disk | **< 1 MB** | A handful of lab files and four small log files, all deleted at the end of the day. |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). |

The processor row is new. Days 0 through 3 never asked you to run anything that consumed a core; today
does, twice, deliberately. Leaving either running distorts every measurement you take afterwards.

---

## §7 Traps

**The signal number that is not the signal number.** `kill -l` in Git Bash reports the Cygwin numbering:
`SIGSTOP` is 17 here and 19 on Linux, `SIGCHLD` is 20 here and 17 on Linux. Sending `kill -17` means two
different things on two machines. **Send by name.** Part 2.1 has the observed listing.

**`$?` is destroyed by the next command.** Including an `echo`. Capture it into a named variable on the
immediately following line or it is gone. Part 3.1 demonstrates the loss.

**`$!` after a pipeline is the last process, not the first.** `uvicorn ... | tee log &` gives you `tee`'s
PID, so killing it terminates the log writer and leaves the server running — until the server's next
write produces `SIGPIPE`. Part 2.1 has the shape.

**`pgrep uvicorn` finds nothing while uvicorn is running.** The executable is `python`; `uvicorn` is an
argument. Without `-f`, `pgrep` never looks at arguments, and an empty result reads as "the service is
down". Part 1.3.

**`pkill -f <pattern>` has no confirmation and no undo.** Always run `pgrep -af <pattern>` first and read
the list. On a shared machine a broad pattern takes out other people's work. Part 2.2, *Blast radius*.

**A green gate is not evidence of a passing test suite.** `pytest` exits `5` for "no tests collected" and
`./o check` forgives it — correctly on Day 0, wrongly from Day 3. Part 3.3, and Day 14 closes it.

**The named trap from plan §5.1 that this day touches:** *a capability without a bound.* Installing a
signal handler takes over a decision the kernel was making correctly. A handler that hangs converts a
service that stopped instantly into one that cannot be stopped politely at all — **strictly worse than
no handler.** Every shutdown step needs a deadline. Part 2.3, *Blast radius*.

---

## §8 Verify before you build

Fetched on **2026-08-24**, not recalled:

| Page | Used for |
| --- | --- |
| `man7.org/linux/man-pages/man7/signal.7.html` | the standard signal table and numbers; *"SIGKILL and SIGSTOP cannot be caught, blocked, or ignored"*; disposition inheritance across `fork` and `execve` |
| `man7.org/linux/man-pages/man3/exit.3.html` | *"the least significant byte of status (i.e., status & 0xFF) is returned to the parent"*; `EXIT_SUCCESS` / `EXIT_FAILURE` |
| `man7.org/linux/man-pages/man2/wait.2.html` | `WIFEXITED`, `WEXITSTATUS`, `WIFSIGNALED`, `WTERMSIG`, `WCOREDUMP`; the definition of a zombie |
| `docs.python.org/3/library/signal.html` | handlers run only in the main thread of the main interpreter; handlers run between bytecode instructions and cannot interrupt a long C call; the Windows-supported signal list |
| `fastapi.tiangolo.com/advanced/events/` | the `lifespan` async context manager, and the deprecation of `@app.on_event` |
| uvicorn settings documentation | `--timeout-graceful-shutdown`, `--timeout-keep-alive`, `--workers`, `--backlog` |

⚠️ `www.uvicorn.org` did not resolve from this machine on 2026-08-24; the settings above were read from
the project's own `docs/settings.md` in its repository. **Re-verify before you rely on a default:**
`curl -s https://raw.githubusercontent.com/encode/uvicorn/master/docs/settings.md | grep -A2 'graceful'`

---

## §9 Say it in an interview

*"The thing that finally made deployments make sense to me was separating the program from the process.
A program is a file; a process is a running instance with its own memory, its own open sockets and its
own identity — and every operational verb acts on the process. So 'I deployed the fix and the bug is
still there' is usually 'the fix isn't running', and the first thing I check is process start time
against deploy time, not the code.*

*"Then the two things I got wrong on my own service. First, stopping it. Every orchestrator stops a
workload by sending `SIGTERM` to PID 1 and hard-killing after a grace period, and `SIGKILL` isn't
delivered to the process at all — so no handler runs, nothing is flushed, and in-flight requests just
become empty replies for the client. I broke my own shutdown four ways and measured what the client saw
each time. The finding that stuck was that three of the four left the server's logs, its exit status and
its error rate looking completely normal, because from the process's point of view nothing went wrong —
it was stopped. The only place the loss was visible was at the caller, which is why service level
objectives get measured from the client side and not from the server's error rate.*

*"Second, PID 1. If the container entrypoint is a shell that starts your app as a child, the `SIGTERM`
goes to the shell and never reaches the app, so every stop waits out the full grace period and then
hard-kills — and the shell doesn't reap orphans either, so zombies accumulate. One word, `exec`, fixes
both, and `docker exec <container> ps -o pid,args` is how I check. I have not run this at real scale
yet; what I have done is cause each failure deliberately on my own machine and write down what I saw
before I knew the cause."*

---

## §10 Done when

`days/day-004-linux-for-operators-i/CHECKLIST.md` has no unticked boxes, and `./o done 4` refuses to
commit until that is true.

Done is defined by understanding and green checks, never by elapsed time. Specifically: you can look at
an exit code and say what ended the process; you have watched a request be destroyed and confirmed that
nothing in your own logs noticed; and every lab file you created is deleted with `git status --short`
clean.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append this row verbatim, replacing the commit hash with your own after
committing:

```text
| 4 | 2026-08-24 | FND-05 | 14 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — no package rows today. Add these two measurement rows instead:

```text
| machine: process state census | S=<n> R=<n> D=<n> Z=<n> I=<n> | 2026-08-24 | 4 | Baseline of what "normal" looks like on this machine, from `ps -eo stat --no-headers | cut -c1 | sort | uniq -c`. Day 6 reasons against it; a sustained non-zero D or Z is a machine problem, not an app problem. |
| pulse: drain duration | <n>s (artificial, /slow?seconds=5) | 2026-08-24 | 4 | Time between SIGTERM and exit with one request in flight, from Day 4 part 4.1. Day 41's `terminationGracePeriodSeconds` must exceed this; Day 109 replaces the artificial number with real inference time. |
```

**`docs/INCIDENTS.md`** — three rows, and **write the first symptom before you investigate**:

```text
| 11 | 2026-08-24 | 4 | Breakage — hard-killed uvicorn mid-request (`drop_drill.sh hardkill`) | <what the client printed, verbatim> | <what you found> | <smallest fix> | <what you changed so it cannot happen silently again> |
| 12 | 2026-08-24 | 4 | Breakage — wrapper with `trap '' TERM` + `exec`, so the ignore was inherited | <first symptom> | <cause> | <fix> | <change> |
| 13 | 2026-08-24 | 4 | Confirmed Day 0 row 4's expiry — renamed `tests/test_api.py` and ran `./o check` | <first symptom> | <cause> | <fix> | <change> |
```

⚠️ **Row 13 closes a loop opened on Day 0.** Row 4 of that ledger predicted this exemption would become
wrong on Day 3; today confirms it arrived and Day 14 closes it. **An incident row that names an expiry
condition is the only kind that reliably gets fixed** — link row 13 back to row 4 explicitly.

**`docs/DECISIONS.md`** — no ADR today. Nothing expensive to reverse was decided; `pulse` is unchanged.

**The commit:**

```text
day 004: Linux for operators I — processes, signals, exit codes — closes FND-05
```
