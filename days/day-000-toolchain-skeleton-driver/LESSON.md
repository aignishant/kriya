---
day: 0
phase: 0
phase_name: "Foundry"
title: "Toolchain, skeleton and the ./o driver"
ids: []
principles: [1, 2, 7, 9, 10, 11, 13, 15, 16, 17, 18]
kind: setup
plan_version: "v1.1.0"
parts: 19
generated: "2026-08-24"
status: complete
lab_scaffolded: false
commit: "5a8edee"
---

# Day 0 — Toolchain, skeleton and the `./o` driver

> **Yesterday:** nothing. This is where the repository begins.
> **Today:** one tool owns the environment, so "which Python, with which libraries" has exactly one
> answer; the repository cannot leak a key by accident, and you have proved that by trying; and `./o`
> exists with two gates — one that reports whether the repository is healthy, and one that refuses to
> finish a day that is not.
> **Tomorrow (Day 1):** what operations actually is, and the ledgers that make this repository
> remember — the diary, the package record, and the incident log you started today.

---

## §1 Where we are

Nothing here is about AI yet. Today is about the floor.

Think about what it takes to hand someone a machine and have them reproduce your work. Not
approximately — *exactly*. The same program, the same libraries, the same versions, the same
settings, and the same answer to "is this finished?". Almost every frustrating day you will have in
the next two hundred days traces back to one of those five things being ambiguous, and ambiguity is
not a small problem that grows into a big one. It is a small problem that stays small and invisible
until the moment it is expensive.

Here is the shape of it. A word like `python` seems like it names one thing. On this machine it names
at least three, and which one you get depends on a list the operating system keeps and that any
installer can quietly reorder. A folder called `data` seems like it names one place, until somebody
renames it and six scripts break in five different ways, one of them silently. A rule that says
"secrets never go in the repository" seems like protection, until you find out it is a convention
that one extra character defeats.

So today has one idea, applied four times: **give every important question exactly one owner, decide
it before it can bite you, and then test that the answer holds by attacking it.**

- **One owner for the environment.** `uv` decides which interpreter runs and what is installed. Not
  your shell, not your editor, not whatever you last installed.
- **One shape for the repository**, decided while it is empty and free to change, including a rule
  about secrets written *before* the first secret exists — because you cannot un-publish anything.
- **One entry point for every operation.** `./o` — so "did you check?" has a yes-or-no answer rather
  than four commands people run inconsistently.
- **Two gates that say no.** One reports whether the repository is healthy; one refuses to call a day
  finished while any box is unticked or any check is red.

And then the part that makes it real: **you break all of it on purpose.** You put a fake secret in
`.env` and watch git refuse to see it — then defeat your own guard rail with one flag, so you know
exactly what it protects against and what it does not. You make each of the five checks fail and read
what it says. By the end you will have seen every safety mechanism in this repository both work and
fail, which is the only way to know the difference between a wall and a sign.

A fire alarm that has passed every inspection and has never been heard is not evidence of anything.
Today is the fire drill, done while the building is empty.

---

## §2 The map

Nineteen documents in five sections. **Each section is one owner** — the environment, the machine,
the repository, the driver, and the history. Read them in order; each names its prerequisite.

### Section 1 — `01-the-toolchain`: one owner for the environment
*Which program runs your code, and what is installed for it — decided once, written down, and
addressed explicitly rather than by luck.*

| Part | Answers | Level |
| --- | --- | --- |
| [1.1 — Why one tool owns the environment](parts/01-the-toolchain/1.1-why-one-tool-owns-the-environment.md) | Why does "works on my machine" happen at all, and what is the actual root cause? | `foundation` |
| [1.2 — Git and the shell these documents assume](parts/01-the-toolchain/1.2-git-and-the-shell-these-docs-assume.md) | Which command language does this curriculum speak, and why that one? | `foundation` |
| [1.3 — `uv`, the one binary](parts/01-the-toolchain/1.3-uv-the-one-binary.md) | What does a lockfile guarantee that a requirements list cannot? | `working` |
| [1.4 — The virtual environment you never activate](parts/01-the-toolchain/1.4-the-venv-you-never-activate.md) | What is a `.venv` really, and why does this project never activate one? | `working` |
| [1.5 — The editor's interpreter trap](parts/01-the-toolchain/1.5-the-editors-interpreter-trap.md) | Your editor says green and the gate says red — which do you believe? | `production` |

### Section 2 — `02-the-machine`: the numbers you reason about for 236 days
*Operations is running real work inside real limits. Measure the limits before you plan against
them.*

| Part | Answers | Level |
| --- | --- | --- |
| [2.1 — The numbers your machine actually has](parts/02-the-machine/2.1-the-numbers-your-machine-actually-has.md) | How much memory, how many cores, how much disk — and where does each one bite later? | `foundation` |
| [2.2 — OneDrive, and the defence against a bug you cannot reproduce](parts/02-the-machine/2.2-onedrive-and-the-hardlink-that-fails.md) | When is a defence against an unreproducible failure worth keeping? | `production` |

### Section 3 — `03-repo-skeleton`: a repository that cannot leak a key
*What a repository is, the shape decided while it is empty, and the guard rail written before the
thing it guards against exists.*

| Part | Answers | Level |
| --- | --- | --- |
| [3.1 — What a repository actually is](parts/03-repo-skeleton/3.1-what-a-repository-actually-is.md) | A commit is a snapshot, not a change — why does that distinction matter? | `foundation` |
| [3.2 — The ignore rule is written before the secret exists](parts/03-repo-skeleton/3.2-gitignore-before-the-secret-exists.md) | Why is the *order* of today's steps more important than their content? | `working` |
| [3.3 — The folder skeleton, decided early](parts/03-repo-skeleton/3.3-the-folder-skeleton-decided-early.md) | Why are ten folders empty, and why is that the decision? | `working` |
| [3.4 — `pyproject.toml` and the lockfile](parts/03-repo-skeleton/3.4-pyproject-and-the-lockfile.md) | One file configures every tool — what does that buy, and what does it risk? | `working` |
| [3.5 — Proving the guard rail holds, and finding its limit](parts/03-repo-skeleton/3.5-proving-the-guard-rail-holds.md) | **Defeat your own protection with one flag** — so you know what it is worth | `production` |

### Section 4 — `04-the-driver`: the gate that refuses
*One entry point for every operation, and the two gates the rest of this curriculum is built on.*

| Part | Answers | Level |
| --- | --- | --- |
| [4.1 — Why a driver script, and not `make`](parts/04-the-driver/4.1-why-a-driver-script-not-make.md) | Why does every operation need exactly one name? | `foundation` |
| [4.2 — `set -euo pipefail`](parts/04-the-driver/4.2-set-euo-pipefail.md) | A script's default is to ignore failures and report success — what stops that? | `working` |
| [4.3 — The dispatcher, and resolving a day by number](parts/04-the-driver/4.3-the-dispatcher-and-resolving-a-day.md) | Why can a folder be renamed without breaking a single tool? | `working` |
| [4.4 — The check gate](parts/04-the-driver/4.4-the-check-gate.md) | Five checks in a deliberate order — why that order, and why stop at the first failure? | `working` |
| [4.5 — The done gate that refuses](parts/04-the-driver/4.5-the-done-gate-that-refuses.md) | What can automation verify about "done", and what can it never verify? | `production` |

### Section 5 — `05-first-commit`: the history, and breaking it on purpose
*What a commit promises to a stranger under pressure — and the fire drill that makes the gates real.*

| Part | Answers | Level |
| --- | --- | --- |
| [5.1 — The first commit, and what it promises](parts/05-first-commit/5.1-the-first-commit-and-what-it-promises.md) | The diff records *what* forever — so what is the one thing a message can add? | `working` |
| [5.2 — Breaking every gate on purpose](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md) | **Make all five checks fail** — because a green check that cannot fail looks identical to a working one | `production` |

**Each section climbs `foundation → working → production`.** Sections 3 and 5 carry the two
deliberate-failure parts the depth contract requires (plan §17.7): [3.5](parts/03-repo-skeleton/3.5-proving-the-guard-rail-holds.md)
attacks the secrets guard rail, and [5.2](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md)
attacks every gate in the repository.

---

## §3 Setup — run this

**Nothing to stop first.** No profile is running today (Addendum 02 §4) — no containers, no cluster,
no observability stack. Day 0 is the only day in the plan with no resident memory cost at all, and it
is worth noticing what that feels like before Day 21 changes it.

**No runtime packages are installed today.** `dependencies` stays `[]` in `pyproject.toml` — packages
arrive on the day they are first used (Principle 7), and the first is on Day 3.

```bash
# 1 — confirm the three tools exist. If any of these fails, stop and install it first.
git --version
uv --version

# 2 — create the environment from the committed manifest and lockfile
uv sync

# 3 — measure your machine (part 2.1). Write these into docs/PACKAGES.md.
nproc
df -h .
#    memory needs PowerShell; `wmic` is removed on current Windows 11:
#    (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory

# 4 — confirm the guard rail is live BEFORE any secret exists (part 3.2)
git check-ignore -v .env          # must print a rule and exit 0
git check-ignore -v .env.example  # must print nothing and exit 1

# 5 — run the gate. Today it is RED, and that is the point (see §5).
./o check
```

**Verified live on 2026-08-24** (Principle 7 — looked up, not remembered):

| Tool | Version observed | How |
| --- | --- | --- |
| git | 2.54.0.windows.1 | `git --version` |
| uv | 0.12.3 | `uv --version` |
| python (this project) | 3.12.12 | `uv run python --version` — uv-managed, **not** the system 3.12.10 |
| ruff | 0.16.4 | `uv run ruff --version`; also the current release on PyPI |
| pytest | 9.1.1 | `uv run python -m pytest --version`; also the current release on PyPI |

**The reference machine**, measured today and recorded in Addendum 02 §3.1: **11.7 GiB RAM, 4 logical
CPUs, 45 GB free of 118 GB**, Windows 11 Home Single Language, no GPU. Your numbers will differ —
measure yours and write them down, because Day 42 asks you to reason about them.

---

## §4 Build brief

**Almost everything in this list already exists in the repository.** That is deliberate and it is the
only day where it is true: the scaffold had to exist before there was a driver to build it with. Your
job today is not to create these files but to **read every line and be able to defend it** — and to
change the two marked below.

| File | Explained in | What it is |
| --- | --- | --- |
| `.gitignore` | [3.2](parts/03-repo-skeleton/3.2-gitignore-before-the-secret-exists.md) | The guard rail, written before any secret existed |
| `pyproject.toml` | [3.4](parts/03-repo-skeleton/3.4-pyproject-and-the-lockfile.md) | Every tool's configuration, in one committed file |
| `uv.lock` | [1.3](parts/01-the-toolchain/1.3-uv-the-one-binary.md) | Exactly what was installed, with hashes. Committed. |
| `o` | [4.1](parts/04-the-driver/4.1-why-a-driver-script-not-make.md)–[4.5](parts/04-the-driver/4.5-the-done-gate-that-refuses.md) | The driver: dispatcher, resolver, and two gates |
| `.env.example` | [3.2](parts/03-repo-skeleton/3.2-gitignore-before-the-secret-exists.md) | Variable names, never values. Committed. |
| `.vscode/settings.json` | [1.5](parts/01-the-toolchain/1.5-the-editors-interpreter-trap.md) | **Yours to create** — point the editor at `.venv` |
| `docs/PACKAGES.md` rows | [2.1](parts/02-the-machine/2.1-the-numbers-your-machine-actually-has.md) | **Yours to write** — your machine's real numbers |
| `docs/INCIDENTS.md` rows | [5.2](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md) | **Yours to write** — one row per deliberate breakage |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` Read `o` top to bottom and be able to say what `${2:-}`, `local n d`, and `|| [ $? -eq 5 ]`
  each protect against. Three small things, three real failures.
- `TODO(me)` Create `.vscode/settings.json` from [1.5](parts/01-the-toolchain/1.5-the-editors-interpreter-trap.md),
  then deliberately point your editor at the **system** interpreter and record the exact message it
  shows you. Editors differ; the string that matters is yours.
- `TODO(me)` Measure your machine and write four rows into `docs/PACKAGES.md`: RAM, logical CPUs, free
  disk, and the date. Then do the arithmetic in [2.1](parts/02-the-machine/2.1-the-numbers-your-machine-actually-has.md):
  what is your platform budget after Windows and a browser?
- `TODO(me)` Do the guard-rail exercise in [3.5](parts/03-repo-skeleton/3.5-proving-the-guard-rail-holds.md)
  **including `git add -f`**. Watch your own protection fail. Clean up afterwards.
- `TODO(me)` Do all five breakages in [5.2](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md)
  and record each one in `docs/INCIDENTS.md` with the first line of output you saw. Then find **one
  more boundary** of the gate that nobody told you about.
- `TODO(me)` Try to reproduce the hardlink failure from [2.2](parts/02-the-machine/2.2-onedrive-and-the-hardlink-that-fails.md)
  in a scratch project. Record what happened — including "could not reproduce", which is a real
  result.

---

## §5 The check that must be able to fail

**This day's own gate was red while it was being written**, and the failure is worth seeing before
you make your own. Run:

```bash
./o check
```

It is green now. But while this document and its checklist did not yet exist, the very same command
printed:

```text
All checks passed!
40 files already formatted
FAIL day   0  2 problems
       - LESSON.md: missing - every day needs a hub
       - CHECKLIST.md: missing

depth contract: 0/1 days pass
```

Exit status `1`. Lint passed, formatting passed, the test step was silent (no tests exist yet — pytest
exits `5` for *"No tests were collected"*, which the gate forgives), and then the depth contract
refused: a day with `parts/` but no hub and no checklist is, by the plan's own definition, not
written.

It went green when the hub and the checklist were written. **That is a gate doing its job on the
document you are holding**, which is a more honest demonstration than any example: the check refused,
for a real reason, and stopped refusing when the reason was fixed.

**Your job today is to make it fail five more ways on purpose** — [5.2](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md)
walks each one: an unused import, a badly formatted file, a failing test, and a smuggled-in time
estimate. **Breakage 3 matters most**: until you add a failing test, the test step has only ever
passed by way of the exit-5 exemption, so you have never actually seen it run a test. Confirm that a
genuinely failing test stops the gate.

---

## §6 Cost & quota budget

| Resource | Today | Notes |
| --- | --- | --- |
| Model calls — any provider | **0** | No key is created today. The three free keys arrive on Day 9. |
| Tokens | **0** | — |
| CI minutes | **0** | No pipeline yet; Day 13 builds the first one. |
| Network | a few MB | `uv` downloads the interpreter and five small packages, once, then caches. |
| RAM (resident) | **0** | **No profile runs today.** Nothing is started; nothing needs stopping. |
| Disk | ~200 MB | `.venv` plus `uv`'s cache. |
| **Money** | **$0** | And no card exists anywhere in this plan (Addendum 01). |

Day 0 is the cheapest day in the curriculum by a wide margin. It is worth registering the contrast:
from Day 21 the *resident memory* row stops being zero and never returns, and from Day 125 the
*model calls* row starts being a number you have to think about.

---

## §7 Traps

- **Creating `.env` before checking the ignore rule.** Run `git check-ignore -v .env` **first**. If it
  prints nothing, stop — the rule is missing and you are one `git add -A` from an incident.
- **Believing `.gitignore` is a barrier.** It is a filter against accidents. `git add -f` defeats it in
  one character, and it does nothing at all for files already tracked
  ([3.5](parts/03-repo-skeleton/3.5-proving-the-guard-rail-holds.md)).
- **`>` instead of `>>`.** One character between appending a row to a ledger and destroying the file.
  Recover with `git checkout -- <file>`.
- **Editing a generated ledger.** `TRACKER.md`, `TRACEABILITY.md` and `CURRICULUM_INDEX.md` are
  rewritten by `./o check`. Your edit will vanish; fix the source instead (plan §16).
- **A bare `python` in anything automated.** It means whatever `PATH` says today. Use `uv run`
  ([1.4](parts/01-the-toolchain/1.4-the-venv-you-never-activate.md)).
- **Trusting the editor over the gate.** The editor keeps its own interpreter opinion and does not
  announce it ([1.5](parts/01-the-toolchain/1.5-the-editors-interpreter-trap.md)).
- **Removing `set -u` because one variable is optional.** Use `${VAR:-}` for that one variable.
  Deleting a safety setting because it is inconvenient once is how safety settings disappear
  ([4.2](parts/04-the-driver/4.2-set-euo-pipefail.md)).
- **"Fixing" a red gate by dropping `--check` from `ruff format`.** That makes the gate rewrite your
  files instead of reporting on them. A check that fixes things is not a check
  ([4.4](parts/04-the-driver/4.4-the-check-gate.md)).
- **Leaving a breakage in place.** After [5.2](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md),
  `git status --short` must be clean. A drill that leaves the system modified is an incident you
  caused.

**Named trap from plan §5.1: trap #1 — *the tutorial that runs as root, on `:latest`, with no
limits*.** Today is its opposite, at the smallest scale: everything is pinned exactly, nothing is
implicit, and every version was looked up rather than assumed. The habit starts here and pays on
Day 27, where `:latest` is the specific thing that makes a rollback meaningless.

---

## §8 Verify before you build

Fetched live on **2026-08-24** while writing this day. Re-check on yours — Principle 8 says look it
up, never remember it.

| What | Where | Why today |
| --- | --- | --- |
| `.gitignore` syntax | `git-scm.com/docs/gitignore` | The `!` negation, the parent-directory limitation, and "the last matching pattern decides" ([3.2](parts/03-repo-skeleton/3.2-gitignore-before-the-secret-exists.md)) |
| `uv` settings | `docs.astral.sh/uv/reference/settings/` | `link-mode` values and the Windows default; how the `dev` group is installed ([2.2](parts/02-the-machine/2.2-onedrive-and-the-hardlink-that-fails.md), [3.4](parts/03-repo-skeleton/3.4-pyproject-and-the-lockfile.md)) |
| `uv` project config | `docs.astral.sh/uv/concepts/projects/config/` | `tool.uv.package = false` and what a virtual project is ([2.2](parts/02-the-machine/2.2-onedrive-and-the-hardlink-that-fails.md)) |
| pytest exit codes | `docs.pytest.org/en/stable/reference/exit-codes.html` | Exit `5` is *"No tests were collected"* — the gate's one exemption ([4.4](parts/04-the-driver/4.4-the-check-gate.md)) |
| bash `set` builtin | `gnu.org/software/bash/manual/html_node/The-Set-Builtin.html` | The exact wording of `-e`, `-u`, `pipefail`, **and `-e`'s documented exceptions** ([4.2](parts/04-the-driver/4.2-set-euo-pipefail.md)) |
| ruff rules | `docs.astral.sh/ruff/rules/` | What `E F I UP B SIM` each select ([3.4](parts/03-repo-skeleton/3.4-pyproject-and-the-lockfile.md)) |
| editor interpreters | `code.visualstudio.com/docs/python/environments` | The interpreter setting and the `./**/.venv` discovery rule ([1.5](parts/01-the-toolchain/1.5-the-editors-interpreter-trap.md)) |

**Not checked today, deliberately:** anything about containers, Kubernetes or models. Principle 8
says the page is checked *on the day the symbol is used*, and none of those are used today.

---

## §9 Say it in an interview

> "The first thing I do on any project is remove ambiguity about the environment, because almost
> every 'works on my machine' bug is two things believing they own the same decision. So one tool
> owns the interpreter and the dependency set, everything runs through it rather than through
> whatever `PATH` resolves to, and the lockfile is committed with hashes — which is what makes a
> model I trained six months ago reproducible rather than approximately reproducible. Then I set up
> the repository so mistakes are structurally hard: the ignore rules for secrets go in before any
> secret exists, because you can't un-publish. And I tested that — I put a fake key in, watched git
> refuse to see it, then defeated my own guard rail with `git add -f`, so I know it's a filter
> against accidents and not a barrier, and I know I need a server-side scanner as well. The part I'd
> emphasise is the gate: one command that runs every check, so 'did you check?' is a yes-or-no
> question, and CI runs the same command rather than a second list that can drift. And I made every
> one of those checks fail on purpose before trusting any of them — a check that has never gone red
> is indistinguishable from a check that can't."

---

## §10 Done when

Not when you have read all nineteen parts. **When every box in [`CHECKLIST.md`](CHECKLIST.md) is
honestly ticked and `./o check` is green.**

There is no time estimate in this day and there never will be (Principle 17). Day 0 might take you one
sitting or five; both are the day done properly.

```bash
./o done 0
```

---

## §11 Ledger & commit

Paste these before running `./o done 0`. **Use the values you actually observed**, not the ones
printed here (Principle 7).

**`docs/PROGRESS.md`** — append one row:

```text
| 0 | 2026-08-24 | — | 19 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — the tool rows are already there from the scaffold. **Add four rows of your
own** for the machine (part 2.1):

```text
| machine: RAM | 11.7 GiB | 2026-08-24 | 0 | The platform's budget after ~4 GB for Windows is ~7.5 GB. Observed with Get-CimInstance. |
| machine: logical CPUs | 4 | 2026-08-24 | 0 | The tighter constraint of the two — CPU contention is silent. Observed with `nproc`. |
| machine: free disk | 45 GB of 118 GB | 2026-08-24 | 0 | Bounds log retention (Day 68) and image churn (Day 30). Observed with `df -h .`. |
| machine: GPU | none | 2026-08-24 | 0 | Day 128 is 🅿️ parked; the local model lane on Day 126 is CPU-only. |
```

**`docs/INCIDENTS.md`** — **six rows minimum**: one per deliberate breakage from
[5.2](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md), plus the guard-rail exercise from
[3.5](parts/03-repo-skeleton/3.5-proving-the-guard-rail-holds.md). The `git add -f` row is the
important one, and its *first symptom* column reads:

```text
| 1 | 2026-08-24 | 0 | committed a fake secret with `git add -f` | none — the commit succeeded normally | .gitignore is a filter, not a barrier | git rm --cached | rotate first, then add a CI scanner (Day 17) |
```

**`docs/DECISIONS.md`** — no new rows. ADR-0001 to ADR-0004 already record why this plan is shaped
the way it is; **read all four today**, because everything in this day follows from them.

**Commit message:**

```text
day 000: toolchain, skeleton and the ./o driver — closes no IDs

Establishes the environment contract before any code exists: uv owns
the interpreter and the lockfile, .gitignore precedes any secret, and
./o defines the only gate. Every safety mechanism was tested by being
made to fail.

Day 0 closes no curriculum IDs by design — it is a precondition for
the plan, not a member of it (plan §14).
```
