# Day 5 — Checklist

**Definition of done.** `./o done 5` reads this file and refuses to commit while any `- [ ]` remains.
It counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd days/day-005-linux-for-operators-ii/lab && df -h . | tail -1 && uv run python holder.py demo.bin & sleep 8; echo "--- after writing 500 MiB ---"; df -h . | tail -1; rm -f demo.bin; echo "--- after deleting it ---"; df -h . | tail -1; pkill -f 'holder.py demo.bin'; sleep 1; echo "--- after killing the holder ---"; df -h . | tail -1
```

Four readings that prove the file was never the thing occupying the disk. Yesterday you could stop a
process. Today you can explain why deleting a file did not free anything, and what did.

---

## Setup

- [ ] nothing from Day 4 still running — `pgrep -af 'holder.py|chatty.py|uvicorn'` checked
- [ ] **free space checked with `df -h .` before starting** — today writes ~700 MB at peak
- [ ] `df -i .` run, and the zeros on NTFS noticed rather than glossed over
- [ ] `./o check` green and `git status --short` clean before breaking anything
- [ ] `./o scaffold 5` has created the day's `lab/`
- [ ] tool availability checked: `stat`, `du`, `df`, `find`, `namei`, `lsof`, `logrotate`, `truncate` —
      and the missing ones written down
- [ ] no packages added, and `git diff pyproject.toml uv.lock` confirms it

---

## Section 1 — `01-the-filesystem`

- [ ] **1.1** read · a hard link created with `ln`, both names confirmed to share one inode number with
      `ls -li`, and the link count seen going 1 → 2 → 1
- [ ] **1.1** one name deleted and the data confirmed intact through the other
- [ ] **1.1** a symlink created, its target renamed, and the dangling link's error message read carefully —
      **noting that the error names the link, not the missing target**
- [ ] **1.1** `stat` run on a file, and `Modify` versus `Change` understood as data versus metadata
- [ ] **1.1** answered out loud: *the two conditions that must both hold before `unlink` frees disk space,
      and a real situation where the second is false*
- [ ] **1.1** `TODO(me)` — `link-mode = "hardlink"` tried on a branch, result recorded, **change not
      committed**
- [ ] **1.2** read · `df -hT` run and the **`-T` column** noticed as the flag most people omit
- [ ] **1.2** `mv` timed within one filesystem and across two — the ~100× difference observed, not assumed
- [ ] **1.2** the 200 MB test file **deleted and the reclaim confirmed** with `df`
- [ ] **1.2** answered out loud: *why `mv` is instant one day and minutes the next, and the one command
      that tells you in advance*
- [ ] **1.3** read · `du -xh --max-depth=1` drill-down run twice, descending into the largest child
- [ ] **1.3** `TODO(me)` — `lab/layout.md` written **before** reading the version in the part, then compared,
      and any disagreement argued out in writing
- [ ] **1.3** answered out loud: *your container writes uploads to `/app/uploads` and everything passes in
      testing — say exactly when it breaks and why no error appears*

---

## Section 2 — `02-permissions`

- [ ] **2.1** read · `id` run, and the numeric uid noted as the left-hand side of every permission check
- [ ] **2.1** three files created at `644`, `600` and `755`, and each mode string read against the table
- [ ] **2.1** execute bit removed from a script and **exit code `126` observed** — distinguished from `127`
- [ ] **2.1** `chmod 044` used to lock yourself out of your own file, and the "stop at the first matching
      category" rule confirmed rather than believed
- [ ] **2.1** answered out loud: *you own a file, the world can read it, you cannot — walk the kernel's
      three checks and say why "stop at first match" beats "most permissive wins"*
- [ ] **2.2** read · `umask` printed, then `022`, `077` and `002` compared with identical file creations
- [ ] **2.2** `chmod +x` versus `chmod 755` compared from a `640` starting point — **the `750` versus `755`
      difference seen**, and why it matters on a credential
- [ ] **2.2** `lab/write_secret.py` written, using `os.open` with an explicit mode rather than
      `open`-then-`chmod`
- [ ] **2.2** `TODO(me)` — **determined whether `chmod 600` is actually honoured here**, and the answer
      written into `docs/PACKAGES.md`
- [ ] **2.2** answered out loud: *a starting mode where `chmod +x` and `chmod 755` differ, and which you
      would rather have typed on a secret*
- [ ] **2.3** read · **a file with mode `000` deleted successfully** — the central fact of this section
- [ ] **2.3** a file you own confirmed undeletable from a directory you cannot write
- [ ] **2.3** `ls -ld` used rather than `ls -l` on directories, deliberately
- [ ] **2.3** `namei -l` run on a deep path (or the `ls -ld`-per-ancestor equivalent where `namei` is absent)
- [ ] **2.3** answered out loud: *the two-step procedure for changing a `444` file you cannot write, and
      what `ls -l` shows afterwards*
- [ ] **2.4** read · `stat` used to print numeric uid/gid **and** the resolved names side by side
- [ ] **2.4** the 🅿️ parked container commands read and the arithmetic followed — 1000 against 0, and which
      of the three categories applies
- [ ] **2.4** answered out loud: *image runs as uid 1000, volume owned by uid 0 mode 755 — which operation
      fails, and why the file's own permissions are irrelevant*

---

## Section 3 — `03-the-disk-that-fills`

- [ ] **3.1** read · `df -h .` and `du -sh .` run on the same place, and the two questions distinguished
- [ ] **3.1** a one-byte file confirmed to occupy 4 KB, with `stat` showing size, blocks and block size
- [ ] **3.1** a sparse file created with `truncate -s 1G` — **`ls` says 1 GB, `du` says 0**, and both are
      correct
- [ ] **3.1** `TODO(me)` — a **fifth** reason `df` and `du` disagree found, and produced if possible
- [ ] **3.1** answered out loud: *the four reasons they disagree, which you check first, and with what
      single command*
- [ ] **3.2** read · `lab/holder.py` written · 500 MiB written and the `df` movement confirmed
- [ ] **3.2** **the file deleted and `df` confirmed unchanged** — the gate
- [ ] **3.2** `du` confirmed unable to see the 500 MiB that is definitely still there
- [ ] **3.2** diagnosis attempted with `lsof +L1` **and** `/proc/<pid>/fd` — **and the unavailability of both
      on this machine recorded**
- [ ] **3.2** the holder killed and **`df` confirmed to return to baseline**
- [ ] **3.2** answered out loud: *the two counters that must both reach zero, which command decrements each,
      and the one command that finds a file with no name*
- [ ] **3.3** read · `df -i` run and this machine's inability to report inodes noted
- [ ] **3.3** the 🅿️ parked loopback exhaustion read, and **why it is confined to a loop device** understood
- [ ] **3.3** the file-**count** drill-down run (`find | wc -l` per directory) as the inode equivalent of `du`
- [ ] **3.3** answered out loud: *`df -h` shows 20% used and a write fails with ENOSPC — what ran out, what
      confirms it, and why deleting your largest file would not help*
- [ ] **3.4** read · `pulse` started and all three routes confirmed `200` **while disk was being consumed**
- [ ] **3.4** the reason for that immunity stated precisely — not "it's small" but which paths touch the
      filesystem
- [ ] **3.4** the 🅿️ parked buffered-versus-flushed comparison read, and **why the error arrives on close**
      understood
- [ ] **3.4** answered out loud: *the three ways a service fails on a full disk, which `pulse` exhibits
      today, and the day on which a full disk starts preventing it from starting*

---

## Section 4 — `04-logs-that-rotate`

- [ ] **4.1** read · **bytes per request measured** with 200 requests, not estimated
- [ ] **4.1** the arithmetic run for 1, 10, 100 and 1,000 req/s, and the bottom row taken seriously
- [ ] **4.1** `TODO(me)` — the measured figure written into `docs/PACKAGES.md`
- [ ] **4.1** answered out loud: *1,000 req/s at 200 bytes a line — roughly how long does 20 GB last, and
      the two things you would change first*
- [ ] **4.2** read · `lab/writer.py` written · **naive rotation performed and the inversion observed**:
      new file at 0 lines, "archived" file still growing
- [ ] **4.2** the count repeated after a further pause, to show a trend rather than a state
- [ ] **4.2** `lab/writer_hup.py` written with `hasattr(signal, "SIGHUP")` guarding, and the platform
      message read rather than skipped
- [ ] **4.2** the `logrotate` config read directive by directive — **`delaycompress` and `olddir`'s
      same-filesystem requirement understood**
- [ ] **4.2** answered out loud: *why the writer does not notice a rename, and the two different ways of
      making it notice*
- [ ] **4.3** read · `lab/seq_writer.py` written using **consecutive integers**, and why that design choice
      makes the loss countable
- [ ] **4.3** `copytruncate` performed by hand · **the exact number of lost lines computed**, not estimated
- [ ] **4.3** repeated against a pre-filled 200 MB file · **the loss confirmed to scale with copy duration**
- [ ] **4.3** the 400 MB peak noticed — two copies at once — and why that fails on a full disk
- [ ] **4.3** everything deleted and **`df` confirmed back to baseline**
- [ ] **4.3** answered out loud: *the two things that widen the loss window, which you control, and the one
      kind of log this must never be used for*
- [ ] **4.4** read · `lab/chatty.py` and `lab/badrotate.sh` written
- [ ] **4.4** **four rotations run, with `du` and `df` printed each cycle** — and row 4 reached: four
      zero-byte files, 4 KB directory, writer still writing
- [ ] **4.4** `kill -0` used to confirm the writer is alive, and the technique understood
- [ ] **4.4** diagnosis attempted, and **the unavailability of `lsof` and `/proc/fd` here recorded again**
- [ ] **4.4** `TODO(me)` — **the whole exercise repeated with the `SIGHUP` version**, and `du`/`df`
      confirmed to stay in agreement through all four cycles
- [ ] **4.4** answered out loud: *the full chain from "rotation renamed the log" to "disk full, log
      directory empty" — four mechanisms, and which section taught each*

---

## Both red gates

- [ ] **Gate one** — a deleted 500 MiB file produced **no change in `df`**, and killing the holder did
- [ ] **Gate two** — four rotations produced four zero-byte files, a 4 KB `du`, and a still-writing process
- [ ] both gates restored: every writer killed, every file removed, `df` back to its starting value

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes, `0` network — confirmed, not assumed
- [ ] **`pgrep -af 'holder.py|chatty.py|writer|seq_writer'` returns nothing** — no process is still writing
- [ ] every large file removed: `held.bin`, `big.bin`, `big.log`, `fill.bin`, `app.log*`, `ct.log*`
- [ ] **`df -h .` confirmed back to its value from §3 step 2** — the reclaim verified, not assumed
- [ ] `/tmp` capture files removed (`pulse-vol.log`, `lv.log`)
- [ ] every lab file created today deleted, and `git status --short` clean

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — three measurement rows appended (filesystems · chmod honoured? · log bytes per
      request)
- [ ] `docs/INCIDENTS.md` — **three rows appended, first symptom written before the cause** (rows 14, 15, 16)
- [ ] row 16 records the **environmental limitation** — `lsof`, `/proc/<pid>/fd` and `df -i` unavailable —
      and Day 21's WSL2 setup is noted as where it closes
- [ ] `docs/DECISIONS.md` — an ADR written **if** your `lab/layout.md` disagreed with part 1.3 on where
      `pulse`'s data lives
- [ ] `docs/PROGRESS.md` — the Day 5 row pasted from the hub's §11
- [ ] `./o check` green
- [ ] `./o depth 5` green
- [ ] `./o trace` shows **FND-06** closed and nothing else newly closed
- [ ] committed: `day 005: Linux for operators II — filesystem, permissions, disks, logs — closes FND-06`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
