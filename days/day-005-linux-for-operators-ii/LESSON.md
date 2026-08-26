---
day: 5
phase: 1
phase_name: "The production mental model and the machine"
title: "Linux for operators II"
ids: [FND-06]
principles: [1, 2, 4, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18]
kind: lab
plan_version: "v1.2.0"
parts: 15
generated: "2026-08-24"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 5 — Linux for operators II — the filesystem, permissions, the disk that fills, the log that must rotate

> **Yesterday (Day 4):** the process — what it is, how you signal it, what it says on the way out, and the
> discovery that three of the four ways a shutdown drops requests leave every server-side signal green.
> **Today:** the other half of the machine. Where files actually live, who is allowed to touch them, why
> the disk fills, and why the most common cause of a full disk is a log rotation that appeared to work.
> **Tomorrow (Day 6):** resources — CPU, memory, the OOM killer, and why your process was simply
> `Killed`.

---

## §1 Where we are

Yesterday's subject was a thing that runs. Today's is a thing that persists, and the two have opposite
failure modes: a process that stops tells you loudly, and a filesystem that is going wrong tells you
nothing at all until it is too late to act gently.

Start with the plainest possible version. Imagine a warehouse with numbered bays and a book of names at
the front desk. The book says *"kitchen order — bay 4471"*. The pallet is in the bay; the line in the book
is just a label pointing at it. Two labels can point at the same bay. Crossing a label out does not empty
the bay — and if somebody is still working in there, the bay stays occupied no matter what the book says.

That is a filesystem. The bay is the file; the line in the book is its name. Almost everything surprising
today follows from keeping them apart: deleting a name is not deleting a file, so a "deleted" thirty
gigabyte log can keep filling your disk with nothing to show for it. Renaming a file is invisible to
whoever is writing into it, so the tidy rotation that runs every night can quietly divert your logs into a
file it is about to destroy.

The second half of the day is about who is allowed to do any of this, and the answer is less intuitive
than it looks. Permission to change a file's *contents* and permission to *delete* it are held in two
different places — the file and the directory — so making a config file read-only protects it from being
edited and not at all from being replaced.

And then the arithmetic that ties it together. A log line is two hundred bytes, which feels free. A
thousand requests a second, five lines each, is eighty-six gigabytes a day. Nothing in that sentence is a
mistake; it is multiplication, and multiplication is where capacity incidents come from.

The day ends with a failure that requires all four sections at once: a disk that fills while the log
directory is empty, every log file is zero bytes, and the rotation job reports success every single night.
Four green checks and one red one, and the red one is the only true one.

---

## §2 The map

**Section 1 — `01-the-filesystem`.** What a file actually is, where it lives, and what the tree is made
of. Everything else today is a consequence of these three parts.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A file is an inode; a name is a pointer](parts/01-the-filesystem/1.1-a-file-is-an-inode-a-name-is-a-pointer.md) | what two conditions must both hold before deleting a file frees any disk? | foundation |
| 1.2 | [Paths, mounts, and the tree that is not one disk](parts/01-the-filesystem/1.2-paths-mounts-and-the-tree-that-is-not-one-disk.md) | why does `mv` take a moment one day and minutes the next, with the same file? | foundation |
| 1.3 | [Where things belong on a Unix system](parts/01-the-filesystem/1.3-where-things-belong-on-a-unix-system.md) | your container writes uploads to `/app/uploads` — say exactly when that breaks | working |

**Section 2 — `02-permissions`.** Who may do what, and the two rules that catch everybody: exactly one
category applies, and deletion is governed by the directory.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [User, group, other — and three bits](parts/02-permissions/2.1-user-group-other-and-three-bits.md) | you own a file, the world can read it, and you cannot — how? | foundation |
| 2.2 | [Reading and changing a mode, and the umask that decided it for you](parts/02-permissions/2.2-reading-and-changing-a-mode.md) | why does the same code write a world-readable file on one host and not another? | working |
| 2.3 | [The permission that is on the directory, not the file](parts/02-permissions/2.3-the-permission-that-is-on-the-directory-not-the-file.md) | how does someone change a file you set to `444`? | working |
| 2.4 | [The container user you will meet on Day 28](parts/02-permissions/2.4-the-container-user-you-will-meet-on-day-28.md) | why does the same image write fine on your laptop and fail in the cluster? | production |

**Section 3 — `03-the-disk-that-fills`.** Capacity as an operational property: two measurements, two
separate resources, and what a full disk actually does to `pulse`.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [`df`, `du`, and why they disagree](parts/03-the-disk-that-fills/3.1-df-du-and-why-they-disagree.md) | name the four reasons the two tools give different answers | working |
| 3.2 | [The deleted file that still costs you a gigabyte](parts/03-the-disk-that-fills/3.2-the-deleted-file-that-still-costs-you-a-gigabyte.md) | you deleted a 30 GB log and freed nothing — what now? | production |
| 3.3 | [Running out of inodes with disk to spare](parts/03-the-disk-that-fills/3.3-running-out-of-inodes-with-disk-to-spare.md) | `No space left on device` at 20% used — which resource ran out? | production |
| 3.4 | [What a full disk does to `pulse`](parts/03-the-disk-that-fills/3.4-what-a-full-disk-does-to-pulse.md) | name the three ways a service fails on a full disk, and which one is dangerous | production |

**Section 4 — `04-logs-that-rotate`.** The single largest consumer of disk in almost every real system,
and the mechanism that bounds it — ending in the day's synthesis failure.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [Why a log file is an operational liability](parts/04-logs-that-rotate/4.1-why-a-log-file-is-an-operational-liability.md) | at 1,000 req/s and 200 bytes a line, how long does 20 GB last? | foundation |
| 4.2 | [Rotation — the mechanism](parts/04-logs-that-rotate/4.2-rotation-the-mechanism.md) | rotation renamed the log — why does the writer not notice? | working |
| 4.3 | [`copytruncate`, and the lines you lose](parts/04-logs-that-rotate/4.3-copytruncate-and-the-lines-you-lose.md) | what makes the loss window larger, and which log must never use this? | production |
| 4.4 | [The rotation that did not free anything](parts/04-logs-that-rotate/4.4-the-rotation-that-did-not-free-anything.md) | the disk is full and the log directory is empty — walk the whole chain | production |

---

## §3 Setup — run this

**Stop first:** anything from Day 4. Check port 8000 and 8010 are free, and confirm no `holder.py`,
`chatty.py` or busy loop survived yesterday — **yesterday's parts included two processes that consume a
full processor core**, and one of today's consumes disk continuously.

**Profile:** `core` only (Addendum 02 §4) — `pulse` at about 60 MB, started briefly in part 3.4 and 4.1.
No containers, no cluster. **Today's real resource is disk**, and the day deliberately consumes several
hundred megabytes at a few points.

**No packages are added today.** Second day running with an empty `docs/PACKAGES.md` package diff. What
today *does* add to that file is measurements.

```bash
# 1 — check nothing from yesterday survived
pgrep -af 'holder.py|chatty.py|uvicorn|while True' || echo "nothing running"

# 2 — CHECK YOUR HEADROOM. Today writes ~700 MB at peak across the exercises.
df -h .

# 3 — inodes, which you will discover this machine cannot report
df -i .

# 4 — the gate green and the tree clean before you break anything
./o check && git status --short

# 5 — this day's scratch folder
./o scaffold 5

# 6 — which of today's tools actually exist here
for t in stat du df find namei lsof logrotate truncate; do
  command -v "$t" >/dev/null && echo "ok      $t" || echo "MISSING $t"
done
```

⚠️ **Step 2 is a safety check, not a formality.** Parts 3.2, 3.4 and 4.3 each write hundreds of megabytes,
and part 4.4 writes continuously until you stop it. **If you have less than a few gigabytes free, do not
run today's disk exercises** — read them and run them on Day 21 inside WSL2.

⚠️ **Several of today's diagnostics do not exist on this machine.** `lsof` is absent, `/proc/<pid>/fd` is
partial, `df -i` reports zeros on NTFS, and `chmod` is only partially honoured. **This is a finding, not a
problem with the day** — each part says so where it applies, and each names the alternative. Record it in
`docs/INCIDENTS.md`: you can *produce* the day's failures here and you cannot always *diagnose* them here,
which is a genuine operational limitation of your primary machine and one more reason WSL2 arrives on
Day 21.

---

## §4 Build brief

Today writes **no project code**. `pulse` is unchanged. Everything lives in this day's `lab/` and is
deleted at the end — with more care than usual, because two of today's files keep growing while they exist.

| File | Explained in | What it is |
| --- | --- | --- |
| `lab/layout.md` | [1.3](parts/01-the-filesystem/1.3-where-things-belong-on-a-unix-system.md) | **Yours to write** — where `pulse`'s files will live, and the rule that decides |
| `lab/write_secret.py` | [2.2](parts/02-permissions/2.2-reading-and-changing-a-mode.md) | **Yours to write** — a file created at mode `600` with no window |
| `lab/holder.py` | [3.2](parts/03-the-disk-that-fills/3.2-the-deleted-file-that-still-costs-you-a-gigabyte.md) | **Yours to write** — writes 500 MiB and holds the descriptor open |
| `lab/writer.py` · `lab/writer_hup.py` | [4.2](parts/04-logs-that-rotate/4.2-rotation-the-mechanism.md) | **Yours to write** — one word of difference: a `SIGHUP` reopen |
| `lab/seq_writer.py` | [4.3](parts/04-logs-that-rotate/4.3-copytruncate-and-the-lines-you-lose.md) | **Yours to write** — consecutive integers, so lost lines are countable |
| `lab/chatty.py` · `lab/badrotate.sh` | [4.4](parts/04-logs-that-rotate/4.4-the-rotation-that-did-not-free-anything.md) | **Yours to write** — the day's synthesis failure |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — three measurement rows |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — three rows, first symptom before cause |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.1](parts/01-the-filesystem/1.1-a-file-is-an-inode-a-name-is-a-pointer.md), find out
  whether `link-mode = "copy"` in `pyproject.toml` is still necessary on your machine. Try `link-mode =
  "hardlink"` on a branch, run `uv sync`, and record what happened. **Do not commit the change** —
  `CLAUDE.md` says the setting stays; the exercise is to know *why* rather than to obey.
- `TODO(me)` Write `lab/layout.md` yourself before reading the version in
  [1.3](parts/01-the-filesystem/1.3-where-things-belong-on-a-unix-system.md), then compare. Any row you
  disagree with is worth arguing out in writing.
- `TODO(me)` In [2.2](parts/02-permissions/2.2-reading-and-changing-a-mode.md), determine whether `chmod
  600` is actually honoured on this filesystem. **The answer decides what Day 9 can rely on**, so write it
  into `docs/PACKAGES.md` rather than leaving it in your head.
- `TODO(me)` Find a **fifth** reason `df` and `du` could disagree that
  [3.1](parts/03-the-disk-that-fills/3.1-df-du-and-why-they-disagree.md) does not list. Produce it if you
  can.
- `TODO(me)` In [4.1](parts/04-logs-that-rotate/4.1-why-a-log-file-is-an-operational-liability.md),
  measure `pulse`'s bytes-per-request log cost on **your** machine and write it into `docs/PACKAGES.md`.
  Day 68 needs it and Day 223 costs it.
- `TODO(me)` Do the [4.4](parts/04-logs-that-rotate/4.4-the-rotation-that-did-not-free-anything.md)
  exercise **twice** — once with `badrotate.sh` and once with a version that ends in `kill -HUP` and a
  writer that reopens. The comparison is the day.
- `TODO(me)` Delete every lab file, confirm no `holder.py` or `chatty.py` survives with `pgrep -af`, and
  prove the tree is clean with `git status --short`. **Today is the first day where a forgotten process
  gets worse over time rather than merely persisting.**

---

## §5 The check that must be able to fail

Two red gates today, and both are red in the sense that *nothing reports an error*.

**Gate one: delete a file and watch the disk not change.**

```bash
cd days/day-005-linux-for-operators-ii/lab && df -h . | tail -1 && uv run python holder.py held.bin & sleep 8; df -h . | tail -1; rm -f held.bin; df -h . | tail -1
```

Three readings. **The third must equal the second** — the delete frees nothing, because a process still
holds the descriptor. If the third reading drops, the holder was not running and the drill measured
nothing. Killing the holder is what returns the space, and
[3.2](parts/03-the-disk-that-fills/3.2-the-deleted-file-that-still-costs-you-a-gigabyte.md) is why.

**Gate two: rotate a log and watch `du` and `df` diverge.**

```bash
cd days/day-005-linux-for-operators-ii/lab && ./badrotate.sh app.log && du -sh . && df -h . | tail -1
```

Run four times, per [4.4](parts/04-logs-that-rotate/4.4-the-rotation-that-did-not-free-anything.md).

| After rotation | `ls` shows | `du` shows | `df` shows | Writer |
| --- | --- | --- | --- | --- |
| 1 | one archive, growing | tracks it | unchanged | writing to `app.log.1` |
| 2 | two archives, one growing | tracks it | unchanged | writing to `app.log.2` |
| 3 | three archives, one growing | tracks it | unchanged | writing to `app.log.3` |
| 4 | **four empty files** | **4 KB** | **still climbing** | writing to **nothing with a name** |

**Row 4 is the gate.** Every visible instrument says the directory is empty; the disk disagrees; nothing
errored at any point. If your row 4 does not show four zero-byte files, the writer died — check with
`pgrep -af chatty.py` before concluding the mechanism does not work.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key exists yet. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline until Day 13. |
| Network | **0** | Nothing downloaded; no packages added. |
| RAM | **~60 MB** | `pulse`, started briefly in 3.4 and 4.1. Plus a few small Python writers. |
| Processor | **negligible** | Unlike yesterday, nothing here pins a core. The 200 MB random writes are brief I/O bursts. |
| **Disk** | **~700 MB at peak, all reclaimed** | 500 MiB in 3.2 · 200 MB twice in 1.2 and 4.3 (**400 MB at once** during the `copytruncate` copy) · a few hundred MB in 4.4. **This is the day's real budget.** |
| **Money** | **$0** | No card exists anywhere in this plan (Addendum 01). |

**The disk row is the first non-trivial one in this curriculum**, and unlike RAM it does not return by
itself when a process ends — parts 3.2 and 4.4 exist precisely because it sometimes does not return when
you delete the file either. **Every disk exercise today ends with a `df` that confirms the reclaim.**
Treat a missing reclaim as the finding it is.

---

## §7 Traps

**`rm` on an active log file makes things worse, not better.** The space is not freed and you lose the
name, so nothing can rotate or read it while it keeps growing. Truncate in place instead: `: > file`.
Part [3.2](parts/03-the-disk-that-fills/3.2-the-deleted-file-that-still-costs-you-a-gigabyte.md).

**`chmod` is only partially honoured on NTFS here.** `chmod 600` may leave the mode at `644`. **Find out
before Day 9 puts a real API key in a file**, and do not assume this defence exists on this machine.
Part [2.1](parts/02-permissions/2.1-user-group-other-and-three-bits.md).

**`chmod -R 777` is never the fix.** It is irreversible — the previous modes are recorded nowhere — and it
exposes every credential in the tree. The correct response to `Permission denied` is `ls -l` plus `id`,
which identifies which of the three categories applied.
Part [2.2](parts/02-permissions/2.2-reading-and-changing-a-mode.md).

**`du` without `-x` walks into every mount point**, including network shares and `/proc`, and on a dead
mount it hangs in uninterruptible sleep — an unkillable diagnostic
([Day 4, part 1.4](../day-004-linux-for-operators-i/parts/01-the-process/1.4-process-states-and-the-d-that-will-not-die.md)).
Always `-x`. Part [1.3](parts/01-the-filesystem/1.3-where-things-belong-on-a-unix-system.md).

**`sort -h` for sizes, `sort -n` for counts.** Using the wrong one silently produces a wrong ordering:
`sort -n` reads `2.1G` as 2.1 and `900M` as 900. Parts
[3.1](parts/03-the-disk-that-fills/3.1-df-du-and-why-they-disagree.md) and
[3.3](parts/03-the-disk-that-fills/3.3-running-out-of-inodes-with-disk-to-spare.md).

**`ls -l` is not a capacity tool.** A sparse file reports gigabytes and occupies nothing; a one-byte file
occupies four kilobytes. Part [3.1](parts/03-the-disk-that-fills/3.1-df-du-and-why-they-disagree.md).

**A green rotation job is not a working rotation.** The `|| true` that makes `postrotate` robust also makes
its permanent failure invisible. Monitor the *outcome* — the current log's modification time — not the exit
code. Part [4.4](parts/04-logs-that-rotate/4.4-the-rotation-that-did-not-free-anything.md).

**The named trap from plan §5.1 that this day touches:** *the capability without a bound.* A log file is a
capability — the ability to record what happened — shipped with no bound at all by default. Nobody decides
to keep logs forever; the absence of a retention decision *is* the decision, and it is always the most
expensive one available. Part
[4.1](parts/04-logs-that-rotate/4.1-why-a-log-file-is-an-operational-liability.md).

---

## §8 Verify before you build

Fetched on **2026-08-24**, not recalled:

| Page | Used for |
| --- | --- |
| `man7.org/linux/man-pages/man7/inode.7.html` | `st_mode`, `st_nlink`, `st_size`, `st_blocks`, the timestamps, and that the name is not in the inode |
| `man7.org/linux/man-pages/man2/unlink.2.html` | the two conditions for freeing space, verbatim; the `EACCES`/`EBUSY`/`EISDIR`/`EPERM`/`EROFS` list |
| `linux.die.net/man/8/logrotate` | `rotate`, `size`, `compress`, `delaycompress`, `copytruncate` and its data-loss caveat verbatim, `create`, `missingok`, `notifempty`, `postrotate`, `olddir` |
| Day 4's fetched pages | `signal(7)` for `SIGHUP`; `docs.python.org/3/library/signal.html` for the Windows-supported signal list |

⚠️ **The Filesystem Hierarchy Standard is cited by convention rather than by a fetched URL.** The layout
table in [1.3](parts/01-the-filesystem/1.3-where-things-belong-on-a-unix-system.md) describes what systems
actually do rather than what the standard says, which is the useful version — but if you want the
normative text: `TODO(curl -s https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)`.

---

## §9 Say it in an interview

*"The thing that changed how I debug disk problems was separating the file from its name. A name is a
directory entry pointing at an inode, and the file only goes away when the link count and the open
descriptor count both reach zero. So `rm` on a log that a service still has open frees nothing — and it
is worse than doing nothing, because you have lost the name, so you cannot rotate it or read it, and it
keeps growing. The tell is `df` and `du` disagreeing, and `lsof +L1` names the file in one command.*

*"The failure I actually caused on my own machine was the compound one. I wrote a rotation script that
renames the log, creates a new one, and deletes the oldest — no signal to the writer. After four cycles
every log file on disk was zero bytes, `du` reported four kilobytes for the whole directory, and the
process was still appending megabytes a second to a file with no name at all. Four green checks and one
red one, and the red one was `df`. That is why I alert on `df` with a projection rather than on a
`du`-derived number: a `du` metric is structurally blind to that failure.*

*"The second thing I got wrong was permissions, in the direction people do not expect. Deleting a file is
a write to the *directory*, not to the file, so setting a config file to `444` protects it from being
edited and not at all from being replaced by anyone with write on the directory. That is what the sticky
bit is for on shared directories, and it is why the first thing I look at on a create-or-delete permission
error is the directory rather than the file.*

*"I have not operated a large fleet yet. What I have done is produce each of these on purpose and write
down what I saw before I knew the cause — including the honest finding that two of the diagnostic tools
this needs do not exist on my primary machine."*

---

## §10 Done when

`days/day-005-linux-for-operators-ii/CHECKLIST.md` has no unticked boxes, and `./o done 5` refuses to
commit until that is true.

Done is defined by understanding and green checks, never by elapsed time. Specifically: you have deleted a
file and watched the disk not change; you have rotated a log four times and watched the directory become
empty while the disk kept filling; and **every process you started is confirmed stopped and every byte you
wrote is confirmed reclaimed**, because today is the first day where a forgotten process keeps consuming.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append this row verbatim, replacing the commit hash with your own after
committing:

```text
| 5 | 2026-08-24 | FND-06 | 15 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — no package rows today. Three measurement rows:

```text
| machine: filesystems | <df -hT output summary> | 2026-08-24 | 5 | Which filesystems this machine actually has, from `df -hT`. Day 0 recorded "45 GB free of 118 GB" without saying of what; this row says which mount that was and what else exists. |
| machine: chmod honoured? | <yes / no — mode after `chmod 600`> | 2026-08-24 | 5 | Whether this filesystem honours Unix permission bits, from Day 5 part 2.2. **Day 9 must not rely on `chmod 600` protecting `.env` if this says no.** |
| pulse: log bytes per request | <n> bytes | 2026-08-24 | 5 | Measured with 200 requests to `/healthz`, from Day 5 part 4.1. Multiplicand for every capacity conversation from Day 67; Day 68 sets retention from it and Day 223 costs it. |
```

**`docs/INCIDENTS.md`** — three rows, and **write the first symptom before you investigate**:

```text
| 14 | 2026-08-24 | 5 | Deleted a 500 MiB file that a running process still had open (part 3.2) | <what df showed, verbatim> | <what you found> | <smallest fix> | <what you changed so it cannot happen silently again> |
| 15 | 2026-08-24 | 5 | Rotated a log four times with no reopen signal, until the chain deleted the file being written (part 4.4) | <first symptom> | <cause> | <fix> | <change> |
| 16 | 2026-08-24 | 5 | Environmental — `lsof`, `/proc/<pid>/fd` and `df -i` all unavailable on this machine | <what you got instead> | Git Bash over NTFS emulates part of the Unix model; the diagnosis step for rows 14 and 15 is not available here | none — run them in WSL2 from Day 21 | Recorded the gap rather than working around it, so Day 21 closes a limitation I found rather than one I was told about |
```

⚠️ **Row 16 is the one worth writing carefully.** It records something you *cannot* do rather than
something that broke, and that is exactly the kind of finding that gets forgotten and then rediscovered
expensively. Day 21's WSL2 setup should reference it.

**`docs/DECISIONS.md`** — no ADR today, unless your `lab/layout.md` disagreed with
[1.3](parts/01-the-filesystem/1.3-where-things-belong-on-a-unix-system.md) on where `pulse`'s data lives.
If it did, that is a genuine decision that Day 23 and Day 25 will implement, and it is cheap to record
now and expensive to reverse later — write the ADR.

**The commit:**

```text
day 005: Linux for operators II — filesystem, permissions, disks, logs — closes FND-06
```
