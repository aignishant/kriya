---
day: 11
phase: 2
phase_name: "Change: version control, CI and releases"
title: "Version control for operators"
ids: [FND-14]
principles: [1, 2, 4, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18]
kind: lab
plan_version: "v1.0.0"
parts: 17
generated: "2026-08-25"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 11 — Version control for operators — the history you will read at 2am, and the commit that explains itself

> **Yesterday (Day 10):** environments and promotion — one artifact, three releases, and a deploy where every
> gate was green, the record was written, and the change never arrived because a port was already held.
> **Today:** the first day of Phase 2, and the first day about *change* rather than about the machine. What a
> commit actually is, why a branch is forty-one bytes, how to interrogate a history you did not write, the
> four undos and which one is safe once anybody else has a copy — ending with a regression you find using only
> the history, and a gate that refuses if you fixed the symptom and destroyed the record.
> **Tomorrow (Day 12):** branching, review, and the change that can be reverted — the workflow built on top of
> everything today establishes.

---

## §1 Where we are

Yesterday's artifact identity was a commit hash. Today that stops being a magic string.

Start with a shipping company's ledger, kept in a bound book with numbered pages. Every entry has the date,
who wrote it, what happened, and the page and line of the entry before it. Not *what changed* — the complete
state: what is in the warehouse now.

A clerk who finds this repetitive starts writing only the differences. *"Add 40 crates of tea."* Faster, and
the total is easy enough to work out.

Then somebody asks what was in the warehouse on the 14th of March. With snapshots you open the book at the
14th and read. With differences you add up every entry from the beginning — and if one is illegible, or was
written out of order, or was quietly amended, **every total after it is wrong and there is no way to tell.**

That is git. A commit is a complete snapshot plus a pointer to the one before it, and its name is a hash of
exactly that — so two identical commits anywhere in the world have the same name, and altering anything
changes every commit after it. **The chain is not a storage optimisation; it is what makes the record
evidence.**

The second half of the day is what an operator does with that. You will be reading this history at 2am, in a
specific state: something is broken, it worked before, you do not know which change did it, and you are
tired. Every tool in sections 3 and 4 exists for that moment — a query language instead of scrolling, a binary
search instead of reading, and four different undos of which exactly one is coherent once somebody else has a
copy.

And the day ends with the drill: a regression planted at a position you do not know, in a history whose commit
messages are conventional, plausible and silent about behaviour. **You may not read the diffs while searching.**
Find it, undo it safely, write the record — and the gate checks all three, because fixing the symptom while
destroying the record is the failure this day is actually about.

**This is the seventh consecutive day ending in a deliberate failure, and it is the first with no dashboard to
be green.** Day 5's disk, Day 6's kill, Day 7's connections, Day 8's certificate, Day 9's credential, Day 10's
deploy that never arrived — every one of those had an instrument that could have shown it. Today's has none.
**The only record is the one somebody chose to write.**

---

## §2 The map

**Section 1 — `01-the-object-model`.** What git actually stores. Four documents that make every later command
predictable instead of memorised.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A commit is a snapshot with a parent](parts/01-the-object-model/1.1-a-commit-is-a-snapshot-with-a-parent.md) | if a commit stores no diff, how does `git show` know what changed? | foundation |
| 1.2 | [The three trees](parts/01-the-object-model/1.2-the-three-trees.md) | why does `git diff` show nothing after `git add`? | foundation |
| 1.3 | [Branches and `HEAD` are just pointers](parts/01-the-object-model/1.3-branches-and-head-are-just-pointers.md) | what exactly does deleting a branch delete? | foundation |
| 1.4 | [Nothing is lost — the object database](parts/01-the-object-model/1.4-nothing-is-lost-the-object-database.md) | you ran `reset --hard` and lost three commits. Where are they? | working |

**Section 2 — `02-the-message`.** The half of a commit that a machine cannot generate, written for a reader
who is tired and has no context.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [What a commit message is for](parts/02-the-message/2.1-what-a-commit-message-is-for.md) | the diff already says what changed — so what is the message for? | foundation |
| 2.2 | [The anatomy of a message](parts/02-the-message/2.2-the-anatomy-of-a-message.md) | what does the blank line after the subject actually do? | working |
| 2.3 | [Conventional Commits](parts/02-the-message/2.3-conventional-commits.md) | which single field, if wrong, breaks somebody else's deploy automatically? | working |
| 2.4 | [One change per commit](parts/02-the-message/2.4-one-change-per-commit.md) | how big should a commit be, and why is "as small as possible" wrong? | production |

**Section 3 — `03-reading-history`.** Interrogating a history you did not write, under time pressure.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [`git log` as a query language](parts/03-reading-history/3.1-log-as-a-query-language.md) | six questions at 2am — which flag answers each? | working |
| 3.2 | [Finding the change that introduced a line](parts/03-reading-history/3.2-finding-the-change-that-introduced-a-line.md) | `git blame` points at the formatter. Now what? | working |
| 3.3 | [`git bisect`](parts/03-reading-history/3.3-bisect-binary-search-over-history.md) | four thousand commits, one bug — how many tests? | production |

**Section 4 — `04-undo`.** Four undos, and the one question that chooses between them.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [The four undos](parts/04-undo/4.1-the-four-undos.md) | which one can lose work that no reflog can recover? | working |
| 4.2 | [`revert` versus `reset`](parts/04-undo/4.2-revert-versus-reset.md) | the files end up identical — so why does the choice matter? | production |
| 4.3 | [The force-push that erased an afternoon](parts/04-undo/4.3-the-force-push-and-the-reflog.md) | it removed the commit and then somebody's `git pull` put it back — how? | production |

**Section 5 — `05-repo-as-memory`.** Day 1's claim, made mechanical — and the drill that tests it.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 5.1 | [The repository is the incident record](parts/05-repo-as-memory/5.1-the-repository-is-the-incident-record.md) | can you reconstruct an incident from the repository alone? | production |
| 5.2 | [The secret that reached history](parts/05-repo-as-memory/5.2-the-secret-that-reached-history.md) | five ways to remove a committed credential, and why all five fail | production |
| 5.3 | [The 2am drill](parts/05-repo-as-memory/5.3-the-2am-drill.md) | a regression, an unknown culprit, and no reading the diffs | production |

---

## §3 Setup — run this

**Profile:** none. Today starts **no servers at all** — the first day since Day 2 with nothing listening. This
is a `git` day, and the only resources it needs are a shell and disk.

**Stop first.** Nothing from Days 4–10 should be running, and today is a good moment to confirm it because
nothing today will notice if something is:

```bash
# 1 — nothing from previous days survives
pgrep -af 'uvicorn|lying_dep|provider:app|leaky:app' || echo "clean"
netstat -ano | grep -E ':(8000|8001|8002|801[0-7]|8099).*LISTENING' || echo "all ports free"

# 2 — this day's scratch folder
./o scaffold 11
```

**The working tree must be clean, and today this matters more than usual.** Several parts run
`git reset --hard`, `git bisect`, `git filter-branch` and `git push --force` — **every one of them inside a
temporary repository**, and a mistyped `cd` is the difference between a demonstration and a lost afternoon:

```bash
# 3 — MUST print nothing. Commit or stash before going any further.
git status --short
git stash list
```

**Read this before section 1.** Every destructive command today runs in a scratch repository created with
`mktemp -d`, with its own `git config user.name` and `user.email` set **locally** so your real configuration is
untouched. **If a block does not begin by creating or entering a scratch directory, it is read-only against
this repository.** The one exception is `./o scaffold 11`, which creates this day's `lab/`.

**No packages are added today.** Everything uses `git`, `python` and the standard library:

```bash
# 4 — confirm, do not assume
git --version
git config --get user.name  || echo "(no global user.name — the scratch repos set their own)"
git config --get user.email || echo "(no global user.email)"
python --version
```

| Tool | Observed here | How | Why today needs it |
| --- | --- | --- | --- |
| git | `2.54.0.windows.1` | `git --version` (Day 0's row) | every part |
| python | `3.12.10` | `python --version` (Day 0's row) | the bisect reproduction in [3.3](parts/03-reading-history/3.3-bisect-binary-search-over-history.md) and [5.3](parts/05-repo-as-memory/5.3-the-2am-drill.md) |

⚠️ **`uv add` is not run today.** `git diff pyproject.toml uv.lock` must be empty at the end — the second
consecutive zero-dependency day.

**One optional configuration**, and it is left as a `TODO(me)` rather than done for you
([2.1](parts/02-the-message/2.1-what-a-commit-message-is-for.md)):

```bash
# 5 — what editor will `git commit` open? Find out BEFORE your first commit without -m.
git config --get core.editor || echo "(unset — git will use \$EDITOR, then vi)"
```

---

## §4 Build brief

Today writes **no project code**. Nothing under `pulse/` changes — not one line — and that is deliberate: this
day is about the repository that holds the code rather than the code. Everything you write lives in this day's
`lab/` or in a temporary directory, and all of it is deleted at the end.

| File | Explained in | What it is |
| --- | --- | --- |
| `lab/history_report.sh` | [5.1](parts/05-repo-as-memory/5.1-the-repository-is-the-incident-record.md) | **Yours to write** — the six 2am questions, answered from the repository alone |
| `lab/setup_drill.sh` | [5.3](parts/05-repo-as-memory/5.3-the-2am-drill.md) | **Yours to write** — plants a regression at a position you do not choose |
| `lab/drill_gate.sh` | [5.3](parts/05-repo-as-memory/5.3-the-2am-drill.md) | **Yours to write** — six conditions; **the red gate** |
| `.git-blame-ignore-revs` | [3.2](parts/03-reading-history/3.2-finding-the-change-that-introduced-a-line.md) | **Yours to consider** — a `TODO(me)`, not a file to create yet |
| scratch repositories | sections 1–5 | **Yours to create and delete** — every destructive command runs in one |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — two measurement rows |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — one row, first symptom before cause |
| `docs/DECISIONS.md` + an ADR | §11 | **Yours to write** — the commit convention and the protected-branch rule |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.1](parts/01-the-object-model/1.1-a-commit-is-a-snapshot-with-a-parent.md), compute a **tree**
  hash by hand the way the part computes a blob hash. It is harder than the blob and the difference is
  instructive. If you cannot, write down exactly where you got stuck.
- `TODO(me)` In [1.2](parts/01-the-object-model/1.2-the-three-trees.md), find a file in this repository whose
  executable bit git is tracking, or establish that there is none — and say what that means for the `.sh`
  scripts Day 10 wrote.
- `TODO(me)` In [1.4](parts/01-the-object-model/1.4-nothing-is-lost-the-object-database.md), find out this
  machine's actual reflog expiry settings (`git config --get gc.reflogExpire` and
  `gc.reflogExpireUnreachable`) and **write both into `docs/PACKAGES.md`.** They are the size of your recovery
  window and almost nobody knows their own.
- `TODO(me)` In [2.1](parts/02-the-message/2.1-what-a-commit-message-is-for.md), write the commit messages that
  Days 7 and 8 **should** have had, in this project's format from plan §18.6. You cannot fix the history; you
  can stop the pattern.
- `TODO(me)` In [2.1](parts/02-the-message/2.1-what-a-commit-message-is-for.md), install the commit template
  with `git config commit.template` — **or decide not to and write down why.** Either is a real answer; not
  deciding is not.
- `TODO(me)` In [2.3](parts/02-the-message/2.3-conventional-commits.md), decide whether this project should
  adopt Conventional Commits. **The part argues no** — read the argument, then argue the other side in writing,
  and note what Day 16 would need for the answer to change.
- `TODO(me)` In [2.4](parts/02-the-message/2.4-one-change-per-commit.md), find a commit in any repository you
  have worked on whose message contains "and". Split it on paper into the commits it should have been.
- `TODO(me)` In [3.1](parts/03-reading-history/3.1-log-as-a-query-language.md), write the four `git log`
  queries you would put in a runbook, with the flags you would actually need at 2am. **Day 79 will ask for
  them.**
- `TODO(me)` In [3.2](parts/03-reading-history/3.2-finding-the-change-that-introduced-a-line.md), decide
  whether this repository should have a `.git-blame-ignore-revs` yet. **It has had no bulk reformat, so the
  honest answer may be "not yet"** — write down the trigger that would change it.
- `TODO(me)` In [3.3](parts/03-reading-history/3.3-bisect-binary-search-over-history.md), work out how many
  bisect steps this repository would need today, and how many it will need at Day 236 assuming one commit per
  day. **The arithmetic is the point.**
- `TODO(me)` In [4.2](parts/04-undo/4.2-revert-versus-reset.md), revert a merge commit and then try to merge
  the branch again. Record what git says and why. **It is the corner everybody meets once.**
- `TODO(me)` In [4.3](parts/04-undo/4.3-the-force-push-and-the-reflog.md), install the `pre-receive` hook in a
  scratch remote and confirm `--force` cannot get past it — then explain in one sentence why a local
  `pre-push` hook is not the same thing.
- `TODO(me)` In [5.1](parts/05-repo-as-memory/5.1-the-repository-is-the-incident-record.md), `history_report.sh`
  contains a pipeline that does nothing. **Find it, and either make it work or delete it and say why the
  `--shortstat` version is sufficient.**
- `TODO(me)` In [5.1](parts/05-repo-as-memory/5.1-the-repository-is-the-incident-record.md), make the ledger
  parsing read **by column name** rather than by position, the way
  [Day 10, 3.2](../day-010-environments-and-promotion/parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md)
  does. Then add a column to a ledger and prove the report still works.
- `TODO(me)` In [5.3](parts/05-repo-as-memory/5.3-the-2am-drill.md), run the drill **twice with different
  seeds**, and time yourself. The second one is the measurement; the first is learning the tools.
- `TODO(me)` Write one paragraph on what Days 5 through 11 have in common — **seven mechanisms** — and what
  makes today's different from the other six.
- `TODO(me)` Delete every scratch directory, confirm `git status --short` is clean, and prove
  `git diff pulse/` is empty. **`pulse` must be untouched.**

---

## §5 The check that must be able to fail

**One gate today**, and it is the day's whole argument in six conditions
([5.3](parts/05-repo-as-memory/5.3-the-2am-drill.md)):

```bash
LAB=days/day-011-version-control-for-operators/lab
B=$(mktemp -d)/drill
bash "$LAB/setup_drill.sh" "$B" "$$"
# ... perform the seven steps in "$B/work" ...
bash "$LAB/drill_gate.sh" "$B/work"
```

| Condition | Checks |
| --- | --- |
| 1 | the symptom is gone |
| 2 | there is a revert commit in the recent history |
| 3 | **the culprit is still in the history** |
| 4 | an incident row was written |
| 5 | the working tree is clean |
| 6 | no bisect is still in progress |

**Condition 3 is the gate.** Conditions 1 and 2 can both be satisfied by fixing the symptom; only condition 3
distinguishes `revert` from `reset` — and the file contents are identical either way, which is exactly what
makes the wrong choice so easy to make at 2am.

**Make it go red on purpose**, and make it red *the interesting way*: do the drill, then
`git reset --hard <culprit>~1` instead of reverting. **The symptom is fixed and three conditions fail.** Then
recover with the reflog and do it properly, so the gate goes green.

**And the green half you must also see:** the drill run correctly end to end, with the incident row written.
**A gate you have only seen fail has proved the failure, not the fix.**

---

## §6 Cost & quota budget

| Resource | Today | Note |
| --- | --- | --- |
| Model calls | **`0`** | no provider is contacted |
| Tokens | **`0`** | — |
| CI minutes | **`0`** | nothing pushed today runs in CI |
| New packages | **`0`** | second consecutive zero-dependency day. `git diff pyproject.toml uv.lock` must be empty |
| Servers started | **`0`** | the first day since Day 2 with nothing listening |
| Network | **`0`** | every "remote" today is a directory on this machine (`git init --bare`) |
| Disk | **~1 MB** | a dozen scratch repositories, each a few kilobytes, all deleted |
| RAM | negligible | `git` and short-lived `python` processes |
| CPU | one `filter-branch` over four commits | [5.2](parts/05-repo-as-memory/5.2-the-secret-that-reached-history.md) — instant here, hours on a real repository |

**This is the cheapest day in the phase and the one with the largest blast radius if a command is run in the
wrong directory.** The cost is not in resources; it is in the fact that `reset --hard`, `filter-branch` and
`push --force` all appear today and every one of them is destructive in a real repository.

---

## §7 Traps

| # | Trap | What it looks like | Where it is covered |
| --- | --- | --- | --- |
| 1 | **`reset --hard` with uncommitted work** | the working tree is clean and the afternoon is gone | [1.2](parts/01-the-object-model/1.2-the-three-trees.md) · [4.1](parts/04-undo/4.1-the-four-undos.md) |
| 2 | **`.gitignore` on a tracked file** | it does nothing at all, and no error says so | [1.2](parts/01-the-object-model/1.2-the-three-trees.md) · [5.2](parts/05-repo-as-memory/5.2-the-secret-that-reached-history.md) |
| 3 | **Believing `--amend` edits a commit** | a rejected push, and the word "behind" | [1.1](parts/01-the-object-model/1.1-a-commit-is-a-snapshot-with-a-parent.md) |
| 4 | **A missing blank line after the subject** | `--oneline` prints a hundred characters; `%b` is empty | [2.2](parts/02-the-message/2.2-the-anatomy-of-a-message.md) |
| 5 | **A trailer that is not in the last paragraph** | the tracker silently does not close the issue | [2.2](parts/02-the-message/2.2-the-anatomy-of-a-message.md) |
| 6 | **`chore:` as a third of the history** | the taxonomy has gone dishonest; version bumps understate reality | [2.3](parts/02-the-message/2.3-conventional-commits.md) |
| 7 | **A path without `--`** | `fatal: ambiguous argument`, most often for a deleted file | [3.1](parts/03-reading-history/3.1-log-as-a-query-language.md) |
| 8 | **`-S` when you wanted `-G`** | nothing found, because the count did not change | [3.1](parts/03-reading-history/3.1-log-as-a-query-language.md) |
| 9 | **Trusting `git blame` after a reformat** | one commit owns four hundred lines and explains none | [3.2](parts/03-reading-history/3.2-finding-the-change-that-introduced-a-line.md) |
| 10 | **A bisect script with no `125`** | the first commit predating a dependency becomes the culprit | [3.3](parts/03-reading-history/3.3-bisect-binary-search-over-history.md) |
| 11 | **A tracked bisect script** | it vanishes at every older commit; every step exits `127` | [3.3](parts/03-reading-history/3.3-bisect-binary-search-over-history.md) |
| 12 | **Forgetting `git bisect reset`** | detached HEAD three days later, and commits on no branch | [3.3](parts/03-reading-history/3.3-bisect-binary-search-over-history.md) · [5.3](parts/05-repo-as-memory/5.3-the-2am-drill.md) |
| 13 | **`reset` on shared history** | a rejected push, then a colleague's merge puts it back | [4.2](parts/04-undo/4.2-revert-versus-reset.md) · [4.3](parts/04-undo/4.3-the-force-push-and-the-reflog.md) |
| 14 | **A local hook as a "control"** | `--no-verify` skips it; a fresh clone does not have it | [4.3](parts/04-undo/4.3-the-force-push-and-the-reflog.md) |
| 15 | **Rewriting history to remove a secret** | your check says clean; every clone still has it | [5.2](parts/05-repo-as-memory/5.2-the-secret-that-reached-history.md) |

**And the named trap from the plan's §5.1 that today touches: #1, the tutorial that runs on `:latest` with no
limits.** Its version-control cousin is **trap 15** — the fix that works immediately, produces a clean-looking
result, teaches nothing that survives contact with a distributed system, and cannot be detected afterwards
because the check you would use to verify it is the one that lies. Day 10's moving tag and today's history
rewrite are the same mistake in two systems: **a name or a record that somebody can change out from under
everybody who already has it.**

---

## §8 Verify before you build

Every page below was fetched on **2026-08-25**, the day this was written (Principle 8). Fetch them again on
the day you run it — **git's own documentation is versioned with the binary, so `git help <command>` is the
authority for the version you have.**

| Fact used | Source page | What was checked |
| --- | --- | --- |
| commit object contents; `cat-file`; `<commit>:<path>`; `^{tree}` | `https://git-scm.com/docs/git-cat-file` · `.../git-rev-parse` | [1.1](parts/01-the-object-model/1.1-a-commit-is-a-snapshot-with-a-parent.md) |
| blob hash = `blob <len>\0<content>` under SHA-1 | `https://git-scm.com/docs/git-hash-object` | [1.1](parts/01-the-object-model/1.1-a-commit-is-a-snapshot-with-a-parent.md) — verified by hand against `sha1sum` |
| `restore` / `reset --soft|--mixed|--hard` and which trees each moves | `https://git-scm.com/docs/git-reset` · `.../git-restore` | [1.2](parts/01-the-object-model/1.2-the-three-trees.md) · [4.1](parts/04-undo/4.1-the-four-undos.md) |
| refs are files under `.git/refs`; `HEAD` holds `ref:` or a hash; `packed-refs` | `https://git-scm.com/docs/git-symbolic-ref` · `.../git-pack-refs` | [1.3](parts/01-the-object-model/1.3-branches-and-head-are-just-pointers.md) |
| reflog syntax `<ref>@{n}`; expiry defaults 90/30 days; `fsck --lost-found` | `https://git-scm.com/docs/git-reflog` · `.../git-fsck` · `.../git-gc` | [1.4](parts/01-the-object-model/1.4-nothing-is-lost-the-object-database.md) |
| `%s`, `%b`, `%(trailers:key=…,valueonly)`; trailers must be the last paragraph | `https://git-scm.com/docs/git-log` · `.../git-interpret-trailers` | [2.2](parts/02-the-message/2.2-the-anatomy-of-a-message.md) |
| `<type>[optional scope]: <description>`; `feat`/`fix`; `!` and `BREAKING CHANGE:` footer | `https://www.conventionalcommits.org/en/v1.0.0/` | [2.3](parts/02-the-message/2.3-conventional-commits.md) — quoted verbatim |
| `-S` (pickaxe) vs `-G`; `-L <range>:<file>`; `--all`; `--` before a path | `https://git-scm.com/docs/git-log` | [3.1](parts/03-reading-history/3.1-log-as-a-query-language.md) |
| `blame -w -M -C`; `blame.ignoreRevsFile` | `https://git-scm.com/docs/git-blame` | [3.2](parts/03-reading-history/3.2-finding-the-change-that-introduced-a-line.md) |
| `bisect run` exit codes: 0 good, 1–124/126/127 bad, **125 skip**, 128+ abort | `https://git-scm.com/docs/git-bisect` | [3.3](parts/03-reading-history/3.3-bisect-binary-search-over-history.md) |
| `revert -m <parent>` for merges; revert is an ordinary commit | `https://git-scm.com/docs/git-revert` | [4.1](parts/04-undo/4.1-the-four-undos.md) · [4.2](parts/04-undo/4.2-revert-versus-reset.md) |
| `--force-with-lease` compares against the remote-tracking ref; `pre-receive` gets `old new ref` | `https://git-scm.com/docs/git-push` · `.../githooks` | [4.3](parts/04-undo/4.3-the-force-push-and-the-reflog.md) |
| `filter-branch --index-filter`; the recommendation to prefer `filter-repo` | `https://git-scm.com/docs/git-filter-branch` | [5.2](parts/05-repo-as-memory/5.2-the-secret-that-reached-history.md) |

---

## §9 Say it in an interview

*"The version control day is where git stopped being a set of commands I had memorised. A commit stores a
complete snapshot plus its parent's hash, and its name is the hash of all of that — so `--amend` cannot edit a
commit, it creates a new one; a branch is forty-one bytes in a file; and deleting a branch deletes a pointer,
not the commits. Once I had that, `reset --soft`, `--mixed` and `--hard` stopped being degrees of severity and
became 'how many of the three trees move', which is why only `--hard` can lose work: the working tree is the
one tree git never stored.*

*The part I actually use is the 2am sequence. Reproduce with one command — a property, not an example, because
an example can pass by coincidence at some commits and send a bisect down the wrong half. Verify the
known-good end is actually good. `git bisect run` with a script that exits 125 for commits it cannot test.
Read the culprit's message before the diff. Then the undo, and the only question that matters is whether
anybody else has it: `reset` on a shared branch is not an undo, it is two incompatible histories, and the
file contents come out the same either way, which is what makes it easy to get wrong.*

*The thing I took away is about the record rather than the code. I ran a drill where I fixed the symptom with
a reset instead of a revert — the bug was gone, the tests passed — and a six-condition gate still failed three
of them, all about the history. Every question afterwards is a question about the past: when did it ship, what
was in that release, can we re-apply it with a fix. And I learned the same lesson from the other direction:
you cannot remove a leaked credential by rewriting history, because every clone still has it, the first
ordinary pull and push puts it back, and in the meantime everybody has stopped treating it as compromised. The
answer is always rotate first."*

---

## §10 Done when

`days/day-011-version-control-for-operators/CHECKLIST.md` — every box ticked honestly. `./o done 11` counts
them and refuses to commit while any remain, and it **cannot** detect a dishonest tick
(`docs/INCIDENTS.md` row 6). That part is yours.

**Done is defined by understanding and green checks, not by anything else.** In particular: the drill gate must
have been seen red *and* green, the red produced by choosing `reset` rather than an arbitrary breakage, every
scratch directory must be deleted, `git status --short` must be clean, and `git diff pulse/` must be empty —
**`pulse` is not touched today.**

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — paste this row verbatim, with the commit hash filled in:

```text
| 11 | 2026-08-25 | FND-14 | 17 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — two measurement rows, with the values *you* observed:

```text
| measurement: reflog expiry on this machine | reachable <n> days / unreachable <n> days | 2026-08-25 | 11 | `git config --get gc.reflogExpire` and `gc.reflogExpireUnreachable` (part 1.4). This is the size of the recovery window for a bad `reset --hard`, and almost nobody knows their own. |
| measurement: bisect steps for this history | <n> commits → <k> steps; at Day 236 → <k'> steps | 2026-08-25 | 11 | log₂(n), computed in part 3.3. Day 20 will care about the commit count; this row is why the number matters. |
```

**`docs/INCIDENTS.md`** — one row. **Write the first symptom before you investigate**, not after:

```text
| 19 | 2026-08-25 | 11 | No ticket was ever routed to the "high" queue; nothing errored and no signal fired (part 5.3) | ... | ... | ... | ... |
```

**Row 19 must record three things the other rows have not needed**: the **method** (`git bisect run` over N
commits, K tests), the **finding about the process** — that the culprit's commit message said "simplify" and
had no body, so `--grep` found nothing and a search was the only option — and the fact that
**no instrument would have reported this**, which is the difference between today and Days 5 through 10.

**`docs/DECISIONS.md`** — **two ADRs are required today**, and both are decisions a stranger will need the
reasoning for:

```text
| ADR-0007 | 2026-08-25 | accepted | Commit messages follow plan §18.6 (`day NNN: <title> — closes <IDs>`) rather than Conventional Commits, because nothing in this repository reads a type prefix. |
| ADR-0008 | 2026-08-25 | accepted | `main` is protected: no non-fast-forward update. History is append-only; corrections are reverts. |
```

**ADR-0007's "what would make us change our minds" must name a number or a condition** — the honest one is
*"when Day 16 introduces semantic versioning for `pulse` and a release tool computes the bump from commit
types"*. **ADR-0008's** is *"never, while the repository is the deployment record"* — and stating a decision
you do not expect to revisit is legitimate, provided you say so.

**The commit:**

```text
day 011: version control for operators — the object model, the message, and the 2am drill — closes FND-14
```
