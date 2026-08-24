# Day 0 — CHECKLIST

**IDs closed:** none — Day 0 is a precondition for the curriculum, not a member of it (plan §14)
**Principles served:** 1, 2, 7, 9, 10, 11, 13, 15, 16, 17, 18
**Parts:** 19 across 5 sections

> `./o done 0` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours ([4.5](parts/04-the-driver/4.5-the-done-gate-that-refuses.md)).

## Demo command

```bash
./o check && ./o status && git log --oneline -1
```

Expected: `OK all green`, then `Kriya: 1/237 days written (19 sub-topic docs), …`, then one commit
reading `day 000: toolchain, skeleton and the ./o driver — closes no IDs`.

---

## Setup

- [x] `git --version` and `uv --version` both answer
- [x] `uv sync` completes and `.venv/` exists
- [x] `uv run python -c "import sys; print(sys.executable)"` prints a path **inside** `.venv`
- [x] `git check-ignore -v .env` prints a rule and exits `0`
- [x] `git check-ignore -v .env.example` prints **nothing** and exits `1`
- [x] `./o` with no arguments prints the full command list

## Section 1 — one owner for the environment

- [x] Can explain "works on my machine" in terms of **two things owning one decision**, without using
      the phrase "virtual environment"
- [x] Ran both interpreter probes and can say what differs between the two paths they printed
- [x] Can say what a lockfile records that a requirements list does not — and why the **hash** matters
- [x] Can say what `.venv/pyvenv.cfg`'s `include-system-site-packages = false` line prevents
- [x] Can say why this project never activates its environment, and what breaks when a scheduler runs
      your job instead of you
- [x] Know which flag CI uses to verify the lockfile — and why the *other* one that sounds identical
      would silently accept a stale lock

## Section 2 — the machine

- [x] Measured RAM, logical CPUs and free disk, and **wrote all four rows into `docs/PACKAGES.md`**
- [x] Did the arithmetic: what is your platform budget after Windows, a browser and an editor?
- [x] Can say which of memory and CPU produces a **visible** failure and which produces a
      **misdiagnosed** one
- [x] Read the `link-mode` and `package` comments in `pyproject.toml` and can say why each exists
- [x] Can state the three questions that separate a **defence** from a **muffler**
- [x] Tried to reproduce the hardlink failure in a scratch project and **recorded the result**,
      including if it could not be reproduced

## Section 3 — a repository that cannot leak a key

- [x] Can say why a commit is a **snapshot** rather than a change, and what that buys on Day 19
- [x] Can state the `.gitignore` precedence rule and why `!.env.example` must come **after** `.env.*`
- [x] Can say what `.gitignore` does **not** do — the two cases
- [x] Can say what goes in `pulse/` versus `platform_ops/`, and what breaks if they are merged
- [x] Read `pyproject.toml` in full and can defend `--strict-markers` and `extend-exclude`
- [x] **Did the guard-rail exercise**: fake `.env`, `git add -A` (not staged), then `git add -f`
      (staged), then `git rm --cached`, then deleted the file
- [x] `git ls-files | grep -i "env\|key\|secret"` prints **only** `.env.example`
- [x] Can say why **rotation comes before cleanup** when a real key leaks

## Section 4 — the gate that refuses

- [x] Can say why `make` was rejected — naming the one thing it offers and why it is worth nothing here
- [x] Can say what each of `-e`, `-u` and `pipefail` prevents, and name one documented **exception**
      to `-e`
- [x] Can explain `${2:-}` and why deleting `set -u` instead would be the wrong fix
- [x] Can explain why `daydir()` globs on the number and never builds a path from the slug
- [x] Can say why the five checks are in that order, and why the gate stops at the first failure
- [x] Can explain `|| [ $? -eq 5 ]` — what it forgives, and what it deliberately does not
- [x] Can say what `./o done` **cannot** verify, and what that implies about who is responsible

## Section 5 — the history, and breaking it on purpose

- [x] Can say the one thing a commit message adds that the diff never can
- [x] Read all four ADRs in `docs/adr/`
- [x] **Breakage 1** — unused import: gate went red at `ruff check`, then cleaned up
- [x] **Breakage 2** — bad formatting: gate went red at `ruff format --check`, and **nothing on disk
      was modified**, then cleaned up
- [x] **Breakage 3** — failing test: gate went red at `pytest`. **This is the first time the test step
      has actually run a test** — confirm it was not swallowed by the exit-5 exemption
- [x] **Breakage 4** — a time-estimate line appended to this file: depth check refused, then cleaned
      up (used `>>`, not `>`). *Note: the exact line is printed in
      [5.2](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md) and cannot be quoted here —
      writing it into this file is itself the violation, which is a neat demonstration that the rule
      is enforced rather than described.*
- [x] **Breakage 5** — unticked a box: `./o done 0` refused **and named the line number**, then ticked
      it back
- [x] Found **one more boundary** of the gate that nobody pointed out, and recorded it
- [x] `git status --short` is clean — every breakage undone

## Read the parts — one box each

Tick only when you have **read it, run its Check yourself, and answered its out-loud question**.

- [x] [1.1 Why one tool owns the environment](parts/01-the-toolchain/1.1-why-one-tool-owns-the-environment.md)
- [x] [1.2 Git and the shell these documents assume](parts/01-the-toolchain/1.2-git-and-the-shell-these-docs-assume.md)
- [x] [1.3 uv, the one binary](parts/01-the-toolchain/1.3-uv-the-one-binary.md)
- [x] [1.4 The virtual environment you never activate](parts/01-the-toolchain/1.4-the-venv-you-never-activate.md)
- [x] [1.5 The editor's interpreter trap](parts/01-the-toolchain/1.5-the-editors-interpreter-trap.md)
- [x] [2.1 The numbers your machine actually has](parts/02-the-machine/2.1-the-numbers-your-machine-actually-has.md)
- [x] [2.2 OneDrive, and the defence against a bug you cannot reproduce](parts/02-the-machine/2.2-onedrive-and-the-hardlink-that-fails.md)
- [x] [3.1 What a repository actually is](parts/03-repo-skeleton/3.1-what-a-repository-actually-is.md)
- [x] [3.2 The ignore rule is written before the secret exists](parts/03-repo-skeleton/3.2-gitignore-before-the-secret-exists.md)
- [x] [3.3 The folder skeleton, decided early](parts/03-repo-skeleton/3.3-the-folder-skeleton-decided-early.md)
- [x] [3.4 pyproject.toml and the lockfile](parts/03-repo-skeleton/3.4-pyproject-and-the-lockfile.md)
- [x] [3.5 Proving the guard rail holds](parts/03-repo-skeleton/3.5-proving-the-guard-rail-holds.md)
- [x] [4.1 Why a driver script, and not make](parts/04-the-driver/4.1-why-a-driver-script-not-make.md)
- [x] [4.2 set -euo pipefail](parts/04-the-driver/4.2-set-euo-pipefail.md)
- [x] [4.3 The dispatcher, and resolving a day by number](parts/04-the-driver/4.3-the-dispatcher-and-resolving-a-day.md)
- [x] [4.4 The check gate](parts/04-the-driver/4.4-the-check-gate.md)
- [x] [4.5 The done gate that refuses](parts/04-the-driver/4.5-the-done-gate-that-refuses.md)
- [x] [5.1 The first commit, and what it promises](parts/05-first-commit/5.1-the-first-commit-and-what-it-promises.md)
- [x] [5.2 Breaking every gate on purpose](parts/05-first-commit/5.2-breaking-every-gate-on-purpose.md)

## Build brief

- [x] Read `o` top to bottom; can defend `${2:-}`, `local n d`, and `|| [ $? -eq 5 ]`
- [x] **Created `.vscode/settings.json`** pointing at `.venv`, and committed it
- [x] Pointed the editor at the **system** interpreter on purpose, and **recorded the exact message it
      showed** — editors differ, so the string that matters is yours
- [x] Read `.gitignore`, `pyproject.toml` and `.env.example` in full

## Cost & quota budget

- [x] Confirmed today's budget: **0 model calls, 0 tokens, 0 CI minutes, 0 resident RAM, $0**
- [x] Confirmed nothing was left running — no containers, no cluster, no compose profile

## Ledger

- [x] `docs/PACKAGES.md` — four machine rows added, with today's date
- [x] `docs/INCIDENTS.md` — **six rows minimum**, one per breakage plus the guard-rail exercise
- [x] Every `INCIDENTS.md` row's *first symptom* column says what you saw **before** you knew the
      cause — including *"none — the commit succeeded normally"* for the `git add -f` row
- [x] `docs/PROGRESS.md` — Day 0's row appended
- [x] Confirmed `TRACKER.md`, `TRACEABILITY.md` and `CURRICULUM_INDEX.md` were **not** hand-edited

## Commit

- [x] `./o check` is green
- [x] `./o done 0` committed, with the message from the hub's §11
