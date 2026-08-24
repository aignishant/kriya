# Day 4 — Checklist

**Definition of done.** `./o done 4` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd days/day-004-linux-for-operators-i/lab && for M in clean hardkill shortgrace; do ./drop_drill.sh "$M" 2>/dev/null | sed "s/^/[$M] /"; done
```

Three ways of stopping a service, and the exact cost of each one printed from the **client's** point of
view. Yesterday you could start and stop `pulse`. Today you can say what it cost.

---

## Setup

- [ ] `./o check` is green before you start
- [ ] `git status --short` is clean
- [ ] ports 8000 **and** 8010 confirmed free with `netstat -ano | grep -E ':(8000|8010).*LISTENING'`
- [ ] `ps`, `pgrep`, `pkill`, `kill`, `netstat` and `curl` all confirmed present on this machine
- [ ] `kill -l` run once, and the Cygwin numbering noticed — `SIGSTOP` is **17** here and **19** on Linux
- [ ] `./o scaffold 4` has created the day's `lab/`
- [ ] no packages added, and `git diff pyproject.toml uv.lock` confirms it

---

## Section 1 — `01-the-process`

- [ ] **1.1** read · the running service edited underneath and confirmed still returning the old answer · file restored and `git diff --stat` empty · answered out loud: *name the three things copied at process creation, and which one causes the stale answer*
- [ ] **1.1** `TODO(me)` — a **fourth** thing copied at creation found, with a command that proves the running process disagrees with the machine
- [ ] **1.2** read · `ps -ef --forest` run and the three-level chain from terminal to shell to server seen
- [ ] **1.2** **the terminal closed on purpose** with the service running in it, and the death confirmed from a second terminal · answered out loud: *which process received what, and why the service was included*
- [ ] **1.3** read · `pgrep uvicorn` run **without** `-f` and the empty result understood before adding it
- [ ] **1.3** the `grep` matching itself seen at least once, and the `[u]vicorn` bracket trick understood
- [ ] **1.3** answered out loud: *the two `ps` columns most people omit, and the false conclusion each prevents*
- [ ] **1.4** read · `Sl` + `ep_poll` recognised as what a healthy idle server looks like
- [ ] **1.4** `kill -STOP` used on `pulse`, `curl` timed out against a process that still owns the port, `kill -CONT` recovered it
- [ ] **1.4** the processor-burning loop started, measured, and **killed** — confirmed with `ps` that it is gone
- [ ] **1.4** `TODO(me)` — state census run, result written into `docs/PACKAGES.md`
- [ ] **1.4** `TODO(me)` — an attempt made to produce state `D` on purpose, and what was tried and why it failed written down

---

## Section 2 — `02-signals`

- [ ] **2.1** read · `Ctrl-C` and `kill -INT` confirmed to produce **identical** output, proving they are the same mechanism
- [ ] **2.1** `sleep 300` signalled with `-TERM` and the `143` observed with no handler involved
- [ ] **2.1** answered out loud: *a signal carries no data — so how does a process distinguish two different reasons for being stopped, and what does that imply about shutdown code?*
- [ ] **2.2** read · the same server stopped with `-TERM` and with `-KILL`, and the **shutdown log line count** compared: `2` versus `0`
- [ ] **2.2** a request put in flight and destroyed with `-KILL`, and `curl: (52) Empty reply from server` seen with your own eyes
- [ ] **2.2** `pgrep -af` run before every `pkill` — no exceptions, including the ones that felt obvious
- [ ] **2.2** answered out loud: *why does a hard-killed process write no shutdown log line even though the code for it is present and correct?*
- [ ] **2.3** read · `lab/handler.py` written · signalled · clean exit `0` observed
- [ ] **2.3** `global` deliberately omitted once, and the "logs the signal and keeps running" bug produced and recognised
- [ ] **2.3** `lab/blocked_handler.py` written · `SIGTERM` sent and **ignored** · the process killed with `-KILL` · the process confirmed gone
- [ ] **2.3** `TODO(me)` — `handler.py` rewritten with `threading.Event`, and the class of bug it removes stated in one sentence
- [ ] **2.3** answered out loud: *two completely different causes of "logs caught SIGTERM, keeps running", and the one-line fix for each*
- [ ] **2.4** read · `lab/uncatchable.py` written · the kernel's refusal (`OSError: [Errno 22] Invalid argument` or equivalent) observed rather than assumed
- [ ] **2.4** `lab/blocking.py` written · `SIGTERM` absorbed, `SIGKILL` not
- [ ] **2.4** answered out loud: *three resources a `SIGSTOP`ped process keeps holding, and which health check fails to notice*

---

## Section 3 — `03-exit-codes`

- [ ] **3.1** read · `$?` deliberately destroyed by an intervening `echo`, and the `RC=$?` habit adopted
- [ ] **3.1** the pipeline trap produced: a failing command piped into `cat` reporting `0`, then `PIPESTATUS` and `set -o pipefail` both used to see the truth
- [ ] **3.1** `126` and `127` both produced deliberately, and the difference between them stated
- [ ] **3.1** answered out loud: *the three exit codes meaning "never ran", "could not be executed" and "was killed"*
- [ ] **3.2** read · all three of `130`, `143` and `137` produced with a loop over `INT`, `TERM`, `KILL`
- [ ] **3.2** `lab/wait_status.py` written · the **raw status word** seen (`9` for a kill, `768` for `exit(3)`) and understood as the thing the shell flattens
- [ ] **3.2** answered out loud: *`137` appears in your logs — the three possible senders, and the one field that identifies which*
- [ ] **3.3** read · `o` opened and `set -euo pipefail` found at the top
- [ ] **3.3** the `|| [ $? -eq 5 ]` line found, and what it forgives stated precisely
- [ ] **3.3** **half one** run: a deliberately failing test added, `./o check` confirmed to exit `1`, probe removed, gate green again
- [ ] **3.3** **half two** run: `tests/test_api.py` renamed, `./o check` confirmed to print `OK all green` and exit `0` with **zero tests collected**, then renamed back and collection confirmed restored
- [ ] **3.3** `pytest` exit codes for a bad path (`4`) and an empty collection (`5`) both observed, rather than trusted
- [ ] **3.3** `TODO(me)` — a **second** hole in `./o check` found, distinct from `docs/INCIDENTS.md` rows 4 and 9
- [ ] **3.3** answered out loud: *two situations that both produce `OK all green`, and what would tell them apart*

---

## Section 4 — `04-the-service-died`

- [ ] **4.1** read · `lab/slow_probe.py` written on port **8010**, not 8000
- [ ] **4.1** a request put in flight and `SIGTERM` sent mid-request — the `200` **arrived** and the ordering of the log lines read carefully
- [ ] **4.1** the second drill run: a late arrival **refused instantly** while the in-flight request completed
- [ ] **4.1** the `lifespan` shape read and understood as where Day 25's connection-pool close will live
- [ ] **4.1** `TODO(me)` — drain duration measured and written into `docs/PACKAGES.md`
- [ ] **4.1** answered out loud: *why the listening socket must close before draining, and what specifically goes wrong in the other order*
- [ ] **4.2** read · `lab/drop_drill.sh` written · `clean` run first as the control, and its three numbers recorded
- [ ] **4.2** **breakage 1** run — `lab/deaf_wrapper.sh` with `trap '' TERM` and `exec` · `143` and **zero** shutdown lines observed
- [ ] **4.2** **breakage 2** run — `hardkill` · `http=000 exit=52` and `137` observed
- [ ] **4.2** **breakage 3** run — `shortgrace` · `137` with **one** shutdown line, and the difference from breakage 2 understood
- [ ] **4.2** **breakage 4** reasoned through — what server behaviour would be needed to produce it, and why uvicorn does not
- [ ] **4.2** the drill checked for the "nothing was in flight" false pass: `time_total` confirmed **less** than `seconds=8` on the kill runs
- [ ] **4.2** answered out loud: *why three of four breakages leave the server's logs and error rate normal, and the one place the loss is observable*
- [ ] **4.3** read · `lab/zombie.py` written · three zombies produced and seen in `ps` as `Z` / `<defunct>`
- [ ] **4.3** a zombie's `rss` and `%cpu` confirmed to be **zero**, rather than assumed
- [ ] **4.3** the parent hard-killed with zombies outstanding, and the zombies confirmed **gone** — adoption and reaping by PID 1 observed
- [ ] **4.3** `lab/no_exec.sh` and `lab/with_exec.sh` written, one word apart · signal sent to each · **server survived one and stopped for the other**
- [ ] **4.3** answered out loud: *the two duties of PID 1, what breaks when each is neglected, and the one word that fixes both*

---

## Both red gates

- [ ] **Gate one** — `./drop_drill.sh hardkill` produced a genuinely lost request (`http=000`), not a false pass
- [ ] **Gate two** — `./o check` observed printing `OK all green` and exiting `0` with the test suite hidden
- [ ] both gates restored to their correct state, and `./o check` green again afterwards

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes, `0` network — confirmed, not assumed
- [ ] **both processor-burning processes killed** — `blocked_handler.py` and the busy loop from 1.4 · confirmed with `ps`
- [ ] the drill server on port 8010 stopped · `netstat -ano | grep ':8010'` returns nothing
- [ ] `server-*.log` files removed from `lab/`
- [ ] every lab file created today deleted, and `git status --short` clean

---

## Ledger & commit

- [ ] `docs/INCIDENTS.md` — **three rows appended, with the first symptom written down before the cause** (rows 11, 12, 13)
- [ ] row 13 explicitly links back to Day 0's row 4, whose predicted expiry it confirms
- [ ] `docs/PACKAGES.md` — the state census row and the drain duration row appended
- [ ] `docs/PROGRESS.md` — the Day 4 row pasted from the hub's §11
- [ ] `./o check` green
- [ ] `./o depth 4` green
- [ ] `./o trace` shows **FND-05** closed and nothing else newly closed
- [ ] committed: `day 004: Linux for operators I — processes, signals, exit codes — closes FND-05`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
