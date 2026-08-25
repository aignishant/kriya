# Day 10 — Checklist

**Definition of done.** `./o done 10` reads this file and refuses to commit while any `- [ ]` remains. It
counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd "$(git rev-parse --show-toplevel)" && LAB=days/day-010-environments-and-promotion/lab && \
pkill -f 'pulse.api:app' 2>/dev/null; sleep 1; \
BUILD=$(bash "$LAB/build.sh") && \
for env in dev staging prod; do R=$(bash "$LAB/release.sh" "$BUILD" "$env"); bash "$LAB/run.sh" "$R" > "/tmp/pulse-$env.log" 2>&1 & done; \
sleep 6; \
for port in 8000 8001 8002; do curl -sS "http://127.0.0.1:$port/version"; echo; done; \
for env in dev staging prod; do bash "$LAB/verify.sh" "$env"; done; \
pkill -f 'pulse.api:app'
```

One build. Three releases. Three running copies of the **same artifact**, each reporting which deploy it is,
which artifact it is running and which release it belongs to — and three independent checks confirming that
what is running is what the ledger says. Yesterday `pulse` could be told seven things. Today there are three
of it, they are provably the same program, and the difference between them is a list you can print.

---

## Setup

- [ ] **nothing from Days 4–9 still running** — `pgrep -af 'uvicorn|leaky|provider|hangy|hungry|burn'`
- [ ] **ports 8000, 8001, 8002 and 8017 confirmed free with `netstat`** — not assumed. **Today's red gate IS a
      held port; a leftover process makes the drill lie**
- [ ] **`git status --short` prints nothing** before starting — three parts run `git reset --hard`, which
      destroys uncommitted work
- [ ] `uv run python scripts/gen_env_example.py --check` green **before** starting (it will go red in 4.1)
- [ ] `git`, `httpx2`, `fastapi` and `pydantic-settings` versions printed and confirmed
- [ ] `./o check` green and `./o scaffold 10` has created the day's `lab/`
- [ ] **no `uv add` today** — confirmed at the end with `git diff pyproject.toml uv.lock`

---

## Section 1 — `01-what-an-environment-is`

- [ ] **1.1** read · `lab/envs/{dev,staging,prod}.env` written · **every key present in all three files**, even
      the identical ones
- [ ] **1.1** two environments started at once and `/version` read from both — **same version, different
      environment**
- [ ] **1.1** the `( set -a; . file; set +a )` subshell understood — **without the parentheses the first
      environment's values leak into the second and the demonstration silently lies**
- [ ] **1.1** `diff` run on **values** and separately on **key sets**, and the difference between the two
      questions stated
- [ ] **1.1** `TODO(me)` — what would differ on three machines instead of three ports, and which check breaks
- [ ] **1.1** answered out loud: *the four things an environment consists of, and which one makes it a real
      boundary*
- [ ] **1.2** read · `lab/differences.md` written · **with a `Deliberate?` column**
- [ ] **1.2** the table built from **what the running services report**, not from the config files
- [ ] **1.2** three rows honestly marked **"not yet real"**, and the closing note about easy conditions written
- [ ] **1.2** the "must be identical" list recited and one entry chosen as the one you would most likely let
      drift
- [ ] **1.2** `TODO(me)` — the same table filled in for a system outside this project; **the rows you cannot
      fill in recorded as the finding**
- [ ] **1.2** answered out loud: *one thing that must be identical which people routinely let drift, and the
      failure it causes*
- [ ] **1.3** read · the time gap computed from **this repository's own git history**
- [ ] **1.3** the four unpinned facts printed next to the lock file's line count — **the ratio seen, not read
      about**
- [ ] **1.3** `lab/parity.md` written **including the "what will make it worse" column**
- [ ] **1.3** the personnel row marked zero **and marked as an artefact of being one person**, not an
      achievement
- [ ] **1.3** `TODO(me)` — the build-environment fingerprint recorded in `docs/PACKAGES.md`. **Day 21 compares
      against it**
- [ ] **1.3** answered out loud: *one thing in the tools gap that `uv.lock` does not cover*
- [ ] **1.4** read · `lab/switched.py` and `lab/settings_only.py` written
- [ ] **1.4** `prod-eu` run against both — **one starts happily with development settings, one refuses**
- [ ] **1.4** the `Literal` understood as what turns a silent `else` into a startup refusal
- [ ] **1.4** the **one legitimate exception** identified — a validator refusing a combination, not choosing a
      value — and justified in one sentence
- [ ] **1.4** the environment-branching grep run over `pulse/`, and **every match justified**
- [ ] **1.4** answered out loud: *what happens to a deploy called `prod-eu` under the anti-pattern*

---

## Section 2 — `02-promotion`

- [ ] **2.1** read · `lab/promote.sh` written · **the dirty-tree refusal is the first thing in the script**
- [ ] **2.1** the refusal **seen**, by dirtying the tree on purpose and restoring with `git checkout <file>`
- [ ] **2.1** the seven things that can differ between two builds of identical source listed, and **the two
      this project has already closed** named
- [ ] **2.1** understood that `/version` **cannot yet** participate in the comparison, and why that is a real
      gap rather than a detail
- [ ] **2.1** answered out loud: *what `pulse`'s artifact identity is today and what it becomes after Day 15*
- [ ] **2.2** read · `lab/build.sh`, `lab/release.sh`, `lab/run.sh` written
- [ ] **2.2** **one build, three releases** produced — the section title, executed
- [ ] **2.2** the release record confirmed to hold **the config hash and the key names, and no values** — a
      record containing values is a record containing credentials
- [ ] **2.2** `exec` in `run.sh` understood — **one process, not two**, and signals reaching uvicorn directly
- [ ] **2.2** the conflict noticed: `run.sh` exports `PULSE_RELEASE_ID` and Day 9's audit would refuse it.
      **The audit is right; the fix is 4.1**
- [ ] **2.2** `TODO(me)` — what to use instead of the naive release counter, and why a git commit solves it
- [ ] **2.2** `TODO(me)` — **`run.sh` made to verify the stored `config_hash`**, then made to fail by editing
      the config file
- [ ] **2.2** answered out loud: *why a configuration change creates a new release but not a new build*
- [ ] **2.3** read · `lab/chain.txt` and `lab/gate.sh` written · **the order is data, not logic**
- [ ] **2.3** the gate seen **green**
- [ ] **2.3** condition **[2]** failed on purpose with an empty commit
- [ ] **2.3** condition **[3]** failed on purpose by adding a key to one environment only
- [ ] **2.3** condition **[4]** failed on purpose by stopping the previous environment
- [ ] **2.3** confirmed that **all four conditions still report** when one fails — one run, all the news
- [ ] **2.3** the first-hop case understood: promoting to `dev` exits **`0`**, not `1`
- [ ] **2.3** `TODO(me)` — a **recorded bypass** added, and a bypass rate chosen that would mean a condition is
      wrong
- [ ] **2.3** answered out loud: *what a bypass counter tells you that the pass rate does not*
- [ ] **2.4** read · `lab/rebuild/requirements-{loose,pinned}.txt` written
- [ ] **2.4** two build IDs from an **empty source diff** seen
- [ ] **2.4** `uv pip compile` run on both files — **and the trap noticed: they agree today**
- [ ] **2.4** `python-dotenv` spotted in the resolved output as a transitive pin **nobody wrote down**
- [ ] **2.4** the four uncontrolled inputs printed, and the fingerprint recorded
- [ ] **2.4** the gate seen refusing a promotion whose **source diff was empty**
- [ ] **2.4** `git reset --hard` used **only with a clean tree**, and the restore verified by re-running
      `build.sh`
- [ ] **2.4** `TODO(me)` — **commit-hash versus tree-hash decided in writing**, with the argument on both sides
- [ ] **2.4** answered out loud: *four inputs to a build that are not your source code*

---

## Section 3 — `03-what-production-promises`

- [ ] **3.1** read · `lab/production_promises.md` written · **four questions, four answers, four dates**
- [ ] **3.1** the "Therefore" section written — **the conclusion stated, not left to the reader**
- [ ] **3.1** `lab/promises.tsv` and `lab/reset_env.sh` written
- [ ] **3.1** three outcomes seen: **allowed**, **refused by policy**, **refused because unclassified**
- [ ] **3.1** the inconsistency noticed: `prod` is refused while all four of its promises say `no` — **the
      refusal is a rehearsal, not a justification**
- [ ] **3.1** `TODO(me)` — `reset_env.sh` changed to read **by column name** rather than by position
- [ ] **3.1** answered out loud: *the one-question test, and a system that is production despite having no
      users*
- [ ] **3.2** read · `lab/data_policy.tsv` written · **`data_source` chosen first, every other column a
      consequence**
- [ ] **3.2** `lab/gen_tickets.py` written · **`--seed` is required, not defaulted**
- [ ] **3.2** reproducibility **proved with two identical `sha256sum` outputs**, and a third that differs
- [ ] **3.2** every generated id confirmed to begin `synthetic-` — **so it is unmistakable in a production log**
- [ ] **3.2** `random` versus `secrets` understood — **predictability is the requirement here, and either is
      wrong in the other's place**
- [ ] **3.2** `lab/refresh_data.sh` written · refusal seen for `prod → staging` · allowance seen for
      `staging → dev`
- [ ] **3.2** the refusal confirmed to **name the alternative command**
- [ ] **3.2** `TODO(me)` — three realistic messes added to the generator, and `pulse` re-tested against them
- [ ] **3.2** answered out loud: *three obligations that travel with a copy and three protections that do not;
      why a deterministic hash is not anonymisation*
- [ ] **3.3** read · `lab/lying_dep.py` and `lab/load.py` written
- [ ] **3.3** `TODO(me)` — **the p99 at concurrency 40 predicted in writing before running it**
- [ ] **3.3** the same code and configuration run at concurrency 2 and 40, and **both p99 numbers recorded**
- [ ] **3.3** the three cheap signals gathered **during** the degradation: status codes, error lines, process
      state — **all green**
- [ ] **3.3** `lab/staging_caveats.md` written · **with the "it tells us" section, not only the limitations**
- [ ] **3.3** the four replacements named — canary, shadow traffic, progressive rollout, rehearsed rollback
- [ ] **3.3** answered out loud: *three bug classes a green staging run says nothing about, and why a bigger
      staging is the wrong answer*

---

## Section 4 — `04-pulse-across-environments`

- [ ] **4.1** read · `build_id` and `release_id` added to `pulse/config.py` · **defaults are `"unknown"`, not
      required**
- [ ] **4.1** `/version` extended · **nothing removed** — a field removed from a response is a breaking change
- [ ] **4.1** `run.sh` updated to export both identities **from the release record**, not from arguments
- [ ] **4.1** `.env.example` regenerated — **and Day 9's `--check` gate seen refusing beforehand**
- [ ] **4.1** `lab/verify.sh` written · seen **green**
- [ ] **4.1** seen **red** by recording a new release while the old process is still serving
- [ ] **4.1** the limitation stated out loud: **this reconciles, it does not prove** — the identity is supplied
      by the environment and Day 15 is what fixes it
- [ ] **4.1** `TODO(me)` — the redundant re-read line in `verify.sh` found and deleted
- [ ] **4.1** `TODO(me)` — `verify.sh` made to **refuse on an empty field on either side**, and proved
- [ ] **4.1** answered out loud: *the two independent sources, and the failure a ledger alone cannot catch*
- [ ] **4.2** read · `pulse/observability.py` written · **fields computed once in `__init__`, not per record**
- [ ] **4.2** the middleware added · **`x-pulse-*` headers seen on a `404`**, not only on a `200`
- [ ] **4.2** the log format updated, and the **loud failure** understood: a missing filter raises on the first
      log line rather than silently omitting the field
- [ ] **4.2** `install()` confirmed to run **after** `basicConfig`, and the consequence of reversing them stated
- [ ] **4.2** the cardinality rule stated: which of these values is safe as a **metric label** and which is not
- [ ] **4.2** the banner confirmed to be **carried, never consumed** — nothing branches on it
- [ ] **4.2** answered out loud: *a value that is safe in a log line and dangerous as a metric label, and why*
- [ ] **4.3** read · `lab/promote_and_verify.sh` written · **four numbered stages, each with `|| exit 1`**
- [ ] **4.3** run **green** end to end
- [ ] **4.3** run **red** by starting an old release on staging's port first
- [ ] **4.3** the seven-row comparison produced, and **six identical rows counted**
- [ ] **4.3** the `EADDRINUSE` error read from the new process's own log — **the cause, not inferred**
- [ ] **4.3** noted that `build_id` **matched** in the failing case — the artifact was right and the deploy
      still did not take
- [ ] **4.3** the failure message confirmed to say **what state the system is now in**, not just what failed
- [ ] **4.3** restored, ports verified clear with `netstat`, and run **green again**
- [ ] **4.3** `TODO(me)` — the fixed `sleep 4` replaced with a **bounded poll**, and the deadline chosen and
      justified
- [ ] **4.3** answered out loud: *why a process that confirms each of its own steps is not a process that
      checks the outcome*

---

## The three gates

- [ ] **gate one** — `gate.sh`: green, then **each of the four conditions failed individually**, then green
- [ ] **gate two** — `refresh_data.sh`: refuses `prod → staging`, allows `staging → dev`, and refuses an
      unclassified environment
- [ ] **gate three** — `promote_and_verify.sh`: **green → red → green**, the red produced by a held port
- [ ] **all three seen red on purpose**, and all three seen green afterwards

---

## The pattern across six days

- [ ] `TODO(me)` — **one paragraph written** on what Day 5's disk, Day 6's OOM kill, Day 7's connections, Day
      8's certificate, Day 9's credential and today's deploy have in common
- [ ] the shared property named: **the signals that are cheap to check are the ones that stay green**, because
      a cheap signal examines something nearby and the failure is one step further out
- [ ] the single kind of check that would have caught all six named: **an outside-in check with a source
      independent of the process that produced the state**
- [ ] the days where that check now exists listed, and the ones where it does not yet

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes confirmed, not assumed
- [ ] **`0` packages added** — `git diff pyproject.toml uv.lock` empty. First zero-dependency day since Day 8
- [ ] **the only external network was two `uv pip compile` calls** — checked, not remembered
- [ ] **`netstat -ano | grep -E ':(8000|8001|8002|8017).*LISTENING'` returns nothing** — no server survives
- [ ] `pkill -f` verified with `netstat` rather than trusted — **today's red gate was a held port**
- [ ] `/tmp/pulse-*.log`, `/tmp/dep.log`, `/tmp/dev.log`, `/tmp/old.log`, `/tmp/keydiff.txt` removed
- [ ] **`lab/releases/`, `lab/builds/` and `lab/rebuild/` deleted** — the ledgers do not survive the day
- [ ] `git status --short` clean
- [ ] **`git diff pulse/` shows only today's intended changes** — two settings fields, two `/version` fields,
      the middleware, and `observability.py`
- [ ] **`git log --oneline -3` shows no leftover `--allow-empty` commits** from 2.3 or 2.4
- [ ] `./o check` green

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — **three measurement rows appended** (build-environment fingerprint · lock file line
      count · the two p99 numbers)
- [ ] `docs/INCIDENTS.md` — **two rows appended, first symptom written before the cause** (rows 17, 18)
- [ ] **row 17 explicitly linked to Day 9's row 16, Day 8's row 13, Day 7's row 22, Day 6's row 19 and Day 5's
      row 16** — six consecutive days — with the shared property named in one sentence
- [ ] `docs/DECISIONS.md` — an ADR written **if** the commit-hash-versus-tree-hash `TODO(me)` reached a
      conclusion
- [ ] `docs/ARCHITECTURE.md` — updated: three deploys, one artifact, **and none of them is a production
      system** by 3.1's four promises
- [ ] `docs/PROGRESS.md` — the Day 10 row pasted from the hub's §11
- [ ] `./o depth 10` green
- [ ] `./o trace` shows **FND-13** closed and nothing else newly closed
- [ ] committed: `day 010: environments and promotion — one artifact, three releases, and the deploy that never arrived — closes FND-13`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
