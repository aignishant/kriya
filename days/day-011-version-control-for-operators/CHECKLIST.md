# Day 11 — Checklist

**Definition of done.** `./o done 11` reads this file and refuses to commit while any `- [ ]` remains. It
counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd "$(git rev-parse --show-toplevel)" && LAB=days/day-011-version-control-for-operators/lab && \
B=$(mktemp -d)/demo && bash "$LAB/setup_drill.sh" "$B" "$$" && cd "$B/work" && \
cat > /tmp/repro.sh <<'EOF'
set -u
cd "$(git rev-parse --show-toplevel)"
python -c "
import sys; sys.path.insert(0, '.')
try: import tickets
except Exception: sys.exit(125)
sys.exit(0 if 'high' in {tickets.route('x'*n) for n in range(1,30)} else 1)"
EOF
git bisect start >/dev/null && git bisect bad HEAD >/dev/null && \
git bisect good "$(git rev-list --max-parents=0 HEAD)" >/dev/null && \
git bisect run bash /tmp/repro.sh 2>&1 | grep 'first bad commit' && \
CULPRIT=$(git rev-parse --short refs/bisect/bad) && git bisect reset >/dev/null && \
git show --no-patch --format='  culprit: %h  %s' "$CULPRIT" && \
git revert --no-edit "$CULPRIT" >/dev/null && bash /tmp/repro.sh && echo "  symptom fixed, culprit still in the history" ; \
cd /tmp && rm -rf "$B" /tmp/repro.sh
```

Fifteen commits, one two-character regression, a message that says `simplify the score calculation` and
mentions no behaviour — **found in about four tests without reading a single diff, undone in a way that leaves
the record intact.** Yesterday you could prove what was running. Today you can find out which change broke it
and undo that change without destroying the evidence.

---

## Setup

- [ ] **nothing from Days 4–10 still running** — `pgrep -af 'uvicorn|lying_dep|provider:app'` and a `netstat`
      sweep of 8000–8017 and 8099
- [ ] **`git status --short` prints nothing** and `git stash list` is empty **before starting** — today runs
      `reset --hard`, `filter-branch` and `push --force`
- [ ] read §3's rule and understood it: **every destructive command today runs in a `mktemp -d` scratch
      repository**, and a block that does not create or enter one is read-only
- [ ] `git --version` and `python --version` recorded; **no `uv add` today**
- [ ] `git config --get core.editor` checked — **before** the first `git commit` without `-m`
- [ ] `./o check` green and `./o scaffold 11` has created the day's `lab/`

---

## Section 1 — `01-the-object-model`

- [ ] **1.1** read · `git cat-file -p HEAD` run · **six lines seen, with no diff in them**
- [ ] **1.1** a blob hash computed **by hand** with `printf 'blob 6\0hello\n' | sha1sum` and confirmed
      identical to `git hash-object`
- [ ] **1.1** two different files with identical content confirmed to share one hash — **content-addressing,
      seen**
- [ ] **1.1** the parent chain read in `git log --format='%h tree=%t parent=%p'`, and the **root commit's
      empty parent** noticed
- [ ] **1.1** the file mode `100644` understood — **git tracks the executable bit and nothing else**
- [ ] **1.1** `TODO(me)` — a **tree** hash attempted by hand, or the exact point of failure written down
- [ ] **1.1** answered out loud: *why `git commit --amend` cannot edit a commit*
- [ ] **1.2** read · the three trees printed side by side and the **wavefront** watched: working → index → HEAD
- [ ] **1.2** `git show :file` used to read the **index** directly
- [ ] **1.2** `MM` produced on one file, and both status letters explained
- [ ] **1.2** `git diff` versus `git diff --cached` understood as **two different comparisons**, one letter
      apart
- [ ] **1.2** `git add -p` used to stage one hunk of a two-hunk file
- [ ] **1.2** understood that **untracked files are in none of the three**, and that this is why `.gitignore`
      does nothing to a tracked file
- [ ] **1.2** `TODO(me)` — is any file's executable bit tracked in this repository? Answered, with the
      consequence for Day 10's `.sh` scripts
- [ ] **1.2** answered out loud: *why `reset --hard` can lose work that `reset --soft` cannot*
- [ ] **1.3** read · `cat .git/HEAD` and `cat .git/refs/heads/main` — **the `ref:` line and forty-one bytes**
- [ ] **1.3** `wc -c` on a branch file confirmed **41**
- [ ] **1.3** a commit watched moving **one** branch and not the other
- [ ] **1.3** detached HEAD entered deliberately with `--detach`, and `.git/HEAD` seen holding a **hash**
- [ ] **1.3** a branch deleted and **its commit read afterwards** by hash
- [ ] **1.3** `git for-each-ref` used rather than parsing `git branch` — and the reason stated
- [ ] **1.3** answered out loud: *what a branch is, in one sentence*
- [ ] **1.4** read · three commits destroyed with `reset --hard` and **recovered from the reflog**
- [ ] **1.4** `HEAD@{1}` **quoted**, and the difference from `HEAD~1` stated
- [ ] **1.4** a deleted branch's commit found with `git fsck --lost-found` **after** its own reflog was gone
      with it
- [ ] **1.4** `git reflog expire --expire-unreachable=now` + `git gc --prune=now` run **in the scratch
      repository only**, and an object confirmed **genuinely gone**
- [ ] **1.4** understood that the reflog is **local and never pushed**
- [ ] **1.4** `TODO(me)` — this machine's `gc.reflogExpire` and `gc.reflogExpireUnreachable` **written into
      `docs/PACKAGES.md`**
- [ ] **1.4** answered out loud: *the one kind of work the reflog cannot recover*

---

## Section 2 — `02-the-message`

- [ ] **2.1** read · this repository's own history graded: **subject lengths, and how many commits have a body**
- [ ] **2.1** confirmed that **two of five commits say `day 7` and `day 8`** and carry no information
- [ ] **2.1** the one-sentence test applied: *would this message still be true if the code were rewritten?*
- [ ] **2.1** `TODO(me)` — the messages Days 7 and 8 **should** have had, written out in plan §18.6's format
- [ ] **2.1** `TODO(me)` — `commit.template` installed, **or the decision not to written down**
- [ ] **2.1** answered out loud: *why a commit message is more trustworthy documentation than a code comment*
- [ ] **2.2** read · a full message written with `git commit -F -`: subject, blank line, body, blank line,
      trailers
- [ ] **2.2** `%s`, `%b` and `%(trailers)` extracted separately — **three fields, from git, not a regex**
- [ ] **2.2** the missing-blank-line failure produced: **a 100-character `--oneline` and an empty `%b`**
- [ ] **2.2** a `Key: value` line placed **not** in the last paragraph and confirmed **not** to be a trailer
- [ ] **2.2** the 72-character limit understood as the four-space `git log` indent plus an 80-column terminal
- [ ] **2.2** answered out loud: *the rule that decides whether a `Key: value` line is a trailer*
- [ ] **2.3** read · the specification quoted and checked at `conventionalcommits.org/en/v1.0.0/`
- [ ] **2.3** a `feat(config)!:` commit written with **both** the `!` and a `BREAKING CHANGE:` footer
- [ ] **2.3** `semver_from_log.py` written · **a major bump computed** from the history, by a machine
- [ ] **2.3** unconventional subjects **counted and reported**, not silently skipped
- [ ] **2.3** a changelog generated, and confirmed that `chore:` **does not appear in it**
- [ ] **2.3** `check_msg.sh` written · **four cases run: one good, three bad, each failing a different rule**
- [ ] **2.3** `TODO(me)` — the adopt-or-not decision argued **on both sides** in writing, with what Day 16
      would change
- [ ] **2.3** answered out loud: *which single field, if wrong, breaks a consumer automatically*
- [ ] **2.4** read · a mixed commit made, then `git revert` run, and **the typo fix seen coming back**
- [ ] **2.4** the same two changes split with `git add` per file, and the revert seen undoing **one**
- [ ] **2.4** `git add -p` with `s` used to split a **single hunk** into two commits
- [ ] **2.4** the rule stated correctly: **the smallest change that leaves the repository working** — not "as
      small as possible"
- [ ] **2.4** the refactor rule understood: **a refactor commit changes no behaviour; a behaviour commit
      changes no names**
- [ ] **2.4** `TODO(me)` — a real commit containing "and", split on paper into what it should have been
- [ ] **2.4** answered out loud: *the specific review failure a mixed refactor causes*

---

## Section 3 — `03-reading-history`

- [ ] **3.1** read · a format string used to produce **columns**, not a wall of text
- [ ] **3.1** `-- <path>` used **with the dashes**, and the ambiguous-argument error seen at least once
- [ ] **3.1** `-S 'link-mode'` run against this repository and **the Day 0 comment found** that explains it
- [ ] **3.1** `-S` versus `-G` demonstrated: **a value edited from 1.0 to 3.0 does not match `-S 'TIMEOUT'`**
- [ ] **3.1** `-L '/regex/,+1:file'` used, and understood to **imply `-p`** and follow renames
- [ ] **3.1** `--all` used, and the reason understood: `git log` walks back from `HEAD` only
- [ ] **3.1** commits-per-day and files-changed-most computed — **Day 20's metrics, nine days early**
- [ ] **3.1** `TODO(me)` — the four runbook queries written out. **Day 79 will ask for them**
- [ ] **3.1** answered out loud: *when `--` before a path matters most*
- [ ] **3.2** read · a reformat commit created on top of a real change, and **blame seen naming the reformat**
- [ ] **3.2** all three ways past it used: **blame the parent**, `-w -M -C`, and `.git-blame-ignore-revs`
- [ ] **3.2** confirmed that `-w` **did not help** here and the ignore file did — and why
- [ ] **3.2** a line **deleted**, and the pickaxe used to recover its whole life when blame could not
- [ ] **3.2** the social point registered: **"last touched" is a lead, never a conclusion**, and it has a
      person's name on it
- [ ] **3.2** `TODO(me)` — does this repository need `.git-blame-ignore-revs` yet? **The trigger written down**
- [ ] **3.2** answered out loud: *which tool to use when the line no longer exists*
- [ ] **3.3** read · a fifteen-commit history bisected in **about four tests**
- [ ] **3.3** the bisect script written with **`sys.exit(125)`** on import failure, and the skip case proved
- [ ] **3.3** the script kept **outside the repository**, and the reason understood
- [ ] **3.3** `git bisect reset` run **every time**, and `git status` confirmed clean afterwards
- [ ] **3.3** understood that a **flaky test breaks the only assumption** bisect makes
- [ ] **3.3** `TODO(me)` — bisect steps for this repository today **and at Day 236**, computed
- [ ] **3.3** answered out loud: *the one property the history must have for bisect to be valid*

---

## Section 4 — `04-undo`

- [ ] **4.1** read · all four undos run against the same mistake, with the **three trees plus `log=` printed**
      at each step
- [ ] **4.1** `--soft`, `--mixed` and `--hard` distinguished by **how many trees move**, not by severity
- [ ] **4.1** `git revert` seen making `log=` go **up** while `reset` makes it go down
- [ ] **4.1** `git restore --source=<commit> -- <path>` used — **one file back, nothing else touched**
- [ ] **4.1** the decision rule stated in one question: **has anybody else got it?**
- [ ] **4.1** answered out loud: *which undo can lose work no reflog can recover, and why*
- [ ] **4.2** read · a **bare remote and two clones** created, so "shared" is real rather than hypothetical
- [ ] **4.2** a `reset` **push rejected** as non-fast-forward — the refusal seen, not described
- [ ] **4.2** a `revert` pushed **with no flags**, and the second clone's ordinary `git pull` seen working
- [ ] **4.2** the three questions answered from the reverted history: **when it shipped, what it changed, and
      re-applying it by reverting the revert**
- [ ] **4.2** `git revert -m 1` used on a **merge** commit, and the ambiguity error seen first
- [ ] **4.2** `TODO(me)` — the merge reverted, then re-merged, and **`Already up to date.`** recorded with the
      explanation
- [ ] **4.2** answered out loud: *three questions only a reverted history can answer*
- [ ] **4.3** read · **both failure directions produced**: work disappearing, and work coming back through an
      ordinary pull
- [ ] **4.3** the force-push output read carefully — **`+` and `(forced update)`, no warning, no error**
- [ ] **4.3** `--force-with-lease` seen **refusing** where `--force` would have succeeded
- [ ] **4.3** the lease's limit understood: **a background fetch satisfies it**
- [ ] **4.3** `TODO(me)` — the `pre-receive` hook installed in a scratch remote and `--force` confirmed
      **refused**
- [ ] **4.3** stated in one sentence why a **local** `pre-push` hook is not a control
- [ ] **4.3** answered out loud: *why force-pushing does not remove a leaked credential*

---

## Section 5 — `05-repo-as-memory`

- [ ] **5.1** read · the six properties of a git history named **without looking**
- [ ] **5.1** the four ledgers' row counts **and last-changed dates** printed
- [ ] **5.1** understood that `last-changed` is the only way to tell **"nothing happened"** from **"nobody
      wrote it down"**
- [ ] **5.1** `lab/history_report.sh` written · the six 2am questions answered from the repository alone
- [ ] **5.1** the report's **missing-file** case and **empty-file** case handled separately
- [ ] **5.1** `TODO(me)` — the pipeline in the report **that does nothing** found, and fixed or deleted with a
      reason
- [ ] **5.1** `TODO(me)` — ledger parsing changed to read **by column name**, then proved by adding a column
- [ ] **5.1** answered out loud: *two kinds of fact a git history cannot hold*
- [ ] **5.2** read · **the marker value used throughout — no real credential, anywhere**
- [ ] **5.2** all five removals attempted and **all five seen failing**: delete the file, `.gitignore`,
      `git rm --cached`, `--amend`, `filter-branch`
- [ ] **5.2** after `filter-branch`, the credential confirmed **still present** in three places: the server,
      the other clone, **and your own object database**
- [ ] **5.2** the force-push done, the server confirmed "clean", and then **the credential seen coming back**
      through an ordinary pull and push
- [ ] **5.2** the response written out **in order** — rotate, update, confirm, revoke, record, prevent,
      *then* consider a rewrite
- [ ] **5.2** understood why the rewrite is **the most dangerous of the five**, not the most thorough
- [ ] **5.2** `git log --all --grep='sk-'` run — **the check for credentials in messages**, which file scanners
      miss
- [ ] **5.3** read · `lab/setup_drill.sh` written · **both arguments required**, and the seed unchosen (`$$`)
- [ ] **5.3** step 1 done: a reproduction that tests a **property**, not an example
- [ ] **5.3** step 2 done: **the known-good end verified**, not assumed
- [ ] **5.3** step 3 done: the culprit found by `git bisect run`, **without reading any diff**
- [ ] **5.3** step 4 done: the culprit's **message** read before its diff, and its uselessness noted
- [ ] **5.3** step 5 done: `git log origin/main` checked **before** choosing the undo · `revert`, not `reset`
- [ ] **5.3** step 6 done: **the same command from step 1**, now passing
- [ ] **5.3** step 7 done: the incident row written with the first symptom first, **the method**, and the
      finding about the commit message
- [ ] **5.3** `git bisect reset` run, and `refs/bisect/bad` captured **before** it
- [ ] **5.3** `TODO(me)` — the drill run **twice with different seeds**, and the second one timed
- [ ] **5.3** answered out loud: *why the gate checks that the culprit is still in the history*

---

## The gate

- [ ] `lab/drill_gate.sh` written · **six conditions, each reported separately**
- [ ] the gate seen **green** after doing the drill correctly
- [ ] the gate seen **red**, and the red produced by **using `reset` instead of `revert`** — not by an
      arbitrary breakage
- [ ] confirmed that in the red case **the symptom was fixed anyway**, and that three conditions failed
      regardless — all three about the record
- [ ] the reflog used to recover from the deliberate `reset`, then the drill completed properly and the gate
      seen **green again**
- [ ] **a gate you have only seen pass is not a gate** — both states seen, in that order

---

## The pattern across seven days

- [ ] `TODO(me)` — **one paragraph written** on what Day 5's disk, Day 6's OOM kill, Day 7's connections, Day
      8's certificate, Day 9's credential, Day 10's deploy and today's regression have in common
- [ ] **what makes today's different named**: the other six had an instrument that could have shown them.
      **Today's had none** — no error, no latency change, no log line, just a queue nobody was routed to
- [ ] the kind of signal that *would* have caught today's named: **a business-level one** — tickets routed per
      priority, where a category going to zero is the alert (Day 75)
- [ ] Day 62, Day 74 and Day 75 identified as where that gap starts closing

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes, **`0` servers started**, **`0` network** confirmed — every
      "remote" today was a local directory
- [ ] **`0` packages added** — `git diff pyproject.toml uv.lock` empty. Second consecutive zero-dependency day
- [ ] **every scratch directory deleted** — `ls /tmp | grep -c 'tmp\.'` checked, not assumed
- [ ] `/tmp/repro.sh`, `/tmp/t.sh`, `/tmp/commit-template.txt`, `/tmp/good.txt`, `/tmp/bad*.txt` removed
- [ ] **`git status --short` clean** in this repository
- [ ] **`git diff pulse/` empty** — `pulse` is not touched today, not one line
- [ ] **`git log --oneline -3` shows no leftover scratch commits** and no `--allow-empty` commits
- [ ] **`git bisect reset` confirmed** — `git status` does not say "You are currently bisecting"
- [ ] **`git log --all -S 'LEAKDEMO' --oneline` returns nothing** in this repository
- [ ] `git config --get user.name` unchanged — **the scratch repositories set their own, locally**
- [ ] `./o check` green

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — **two measurement rows appended** (reflog expiry on this machine · bisect steps for
      this history, now and at Day 236)
- [ ] `docs/INCIDENTS.md` — **one row appended, first symptom written before the cause** (row 19)
- [ ] **row 19 records the method** (`git bisect run` over N commits, K tests) **and the finding about the
      commit message** — the part that changes behaviour
- [ ] **row 19 states that no instrument would have reported this**, and links Day 10's row 17, Day 9's row 16,
      Day 8's row 13, Day 7's row 22, Day 6's row 19 and Day 5's row 16
- [ ] `docs/DECISIONS.md` + `docs/adr/ADR-0007-*.md` — **the commit-message convention**, with what Day 16
      would change
- [ ] `docs/DECISIONS.md` + `docs/adr/ADR-0008-*.md` — **`main` is protected; corrections are reverts**, with
      an honest "we do not expect to revisit this, and here is why"
- [ ] `docs/PROGRESS.md` — the Day 11 row pasted from the hub's §11
- [ ] `./o depth 11` green
- [ ] `./o trace` shows **FND-14** closed and nothing else newly closed
- [ ] committed: `day 011: version control for operators — the object model, the message, and the 2am drill — closes FND-14`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
