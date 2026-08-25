---
day: 10
phase: 1
phase_name: "The production mental model and the machine"
title: "Environments and promotion"
ids: [FND-13]
principles: [1, 2, 4, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18]
kind: lab
plan_version: "v1.0.0"
parts: 14
generated: "2026-08-25"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 10 — Environments and promotion — what the word "production" actually promises

> **Yesterday (Day 9):** the service's inputs — one typed settings object, a refusal to start on a bad value,
> and the first credential `pulse` must never print. It ended with that credential published into the log by a
> line of code every part of the day recommended.
> **Today:** where those settings *go*. What an environment actually is, what may differ between two of them
> and what must not, what it means to move a build from one to the next, and what the word "production"
> commits you to. It ends with a promotion where every gate is green, the record is written, and the change
> never arrived.
> **Tomorrow (Day 11):** version control for operators — the history you will read at 2am, and the commit that
> explains itself. Today's artifact identity is a commit SHA; tomorrow is where that stops being a magic
> string.

---

## §1 Where we are

Yesterday `pulse` learned to be told things. Today it learns that there is more than one of it.

Think about a touring theatre company again, but from the other side. Yesterday's question was *what is written
on the script and what is on a separate card*. Today's is: **there are three venues, and something has to be
true about all three or the rehearsal was pointless.**

The play is the same everywhere — same lines, same order, same cues — and if it is not identical then "we
rehearsed it" is a claim about a different play. What changes is the venue: the address, the door code, the
number of seats, whether the bar is slow. Four things, written on a card, and everybody knows what is on the
card.

Now the part that makes it an *operations* problem rather than a filing problem. There is a rehearsal room and
there is an opening night. The rehearsal room has no audience, which is what makes it useful — and it is also
what makes it a liar. Everything you learn there is true of a room with no audience in it. The acoustics with
four hundred people in wet coats are not the acoustics you rehearsed in, and no amount of care in the
rehearsal room produces that information.

So the answer is not a better rehearsal room. **The answer is that the opening night is watched carefully, the
changes are small, and there is a way to stop.**

That sentence is the second half of this curriculum in miniature — canary deploys, progressive rollout,
observability, rehearsed rollback — and today is where the argument for it is made.

And the day ends with the failure that motivates every one of those: **a deploy where the paperwork was
perfect.** The gate passed, the artifact was right, the configuration matched, the release was recorded — and
the process serving traffic was the old one, because a port was already taken and nothing ever asked the
running service what it was.

**That is the sixth consecutive day where the thing that was wrong was invisible to every cheap signal.** Day
5's disk, Day 6's kill, Day 7's connections, Day 8's certificate, Day 9's credential, and today's deploy that
never took. Today is where the property they share finally gets named — *the signals that are cheap to check
are the ones that stay green* — and where the counter-measure gets built: **check the outcome from outside,
with a source that is independent of the process that produced it.**

---

## §2 The map

**Section 1 — `01-what-an-environment-is`.** The vocabulary, made precise enough to build on. What an
environment is, what may differ between two of them, how far apart they drift, and the one thing the
environment's *name* must never be used for.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [An environment is a deploy, not a folder](parts/01-what-an-environment-is/1.1-an-environment-is-a-deploy-not-a-folder.md) | what makes two copies of a service two environments rather than one? | foundation |
| 1.2 | [The four things that differ](parts/01-what-an-environment-is/1.2-the-four-things-that-differ.md) | which differences are allowed, and which one turns a green test into a lie? | foundation |
| 1.3 | [Dev/prod parity and the three gaps](parts/01-what-an-environment-is/1.3-dev-prod-parity-and-the-three-gaps.md) | how far is your laptop from production, in numbers? | working |
| 1.4 | [The environment name is not a switch](parts/01-what-an-environment-is/1.4-the-environment-name-is-not-a-switch.md) | what happens to a deploy called `prod-eu` when the code says `if env == "prod"`? | working |

**Section 2 — `02-promotion`.** Moving a change from one environment to the next: what actually travels, the
three stages it travels through, what must be true before it moves, and why "the same commit" is not "the same
program".

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Build once, promote the artifact](parts/02-promotion/2.1-build-once-promote-the-artifact.md) | why is rebuilding from the same commit not the same as promoting? | working |
| 2.2 | [Build, release, run](parts/02-promotion/2.2-build-release-run.md) | a config change with no code change — what exactly do you roll back to? | working |
| 2.3 | [The promotion gate](parts/02-promotion/2.3-the-promotion-gate.md) | four conditions, and which one you would drop first | production |
| 2.4 | [The rebuild that promoted something different](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) | the source diff is empty and the artifacts differ — how? | production |

**Section 3 — `03-what-production-promises`.** What the word commits you to, the one thing that can never
travel between environments, and why a green pre-production run is a claim about pre-production.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [What the word "production" actually promises](parts/03-what-production-promises/3.1-what-the-word-production-promises.md) | is a nightly batch job with no users production? | production |
| 3.2 | [Data is the thing that cannot be promoted](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md) | what arrives with a copy of production's data, and what does not? | production |
| 3.3 | [The staging environment that lied](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md) | same code, same config, p99 nineteen times worse — and every signal green | production |

**Section 4 — `04-pulse-across-environments`.** All of it, on the service: three releases of one artifact, an
identity on everything `pulse` emits, and the drill where the paperwork was perfect.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [One artifact, three releases](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md) | how do you check that the thing running is the thing you promoted? | production |
| 4.2 | [The environment banner](parts/04-pulse-across-environments/4.2-the-environment-banner.md) | a log line pasted into a chat at 3am — which deploy produced it? | production |
| 4.3 | [The promotion that was not verified](parts/04-pulse-across-environments/4.3-the-promotion-that-was-not-verified.md) | every gate green, the record written, the change absent — how? | production |

---

## §3 Setup — run this

**Profile:** `core` only (Addendum 02 §4). Today runs up to **three** `pulse` processes at once — the most any
day in this phase asks for — on a machine with four logical CPUs (`docs/PACKAGES.md`, Day 0). **Nothing else
may be running**, and that includes the observability stack, any container runtime and anything left from
Days 4–9.

**Stop first:**

```bash
# 1 — nothing from previous days survives
pgrep -af 'uvicorn|blackhole|hangy|hungry|burn|allocate|holder|slow_resolver|leaky|provider' || echo "clean"
pkill -f 'blackhole|hangy|hungry|burn|allocate|holder|slow_resolver|leaky:app|provider:app' 2>/dev/null

# 2 — the ports this day uses must be CONFIRMED free, not assumed.
#     Today's deliberate failure IS a held port, so a leftover process makes the drill lie.
netstat -ano | grep -E ':(8000|8001|8002|8017).*LISTENING' || echo "all ports free"

# 3 — this day's scratch folder
./o scaffold 10
```

**The working tree must be clean.** Three parts run `git commit --allow-empty` and `git reset --hard`, and
one part refuses to build on a dirty tree by design. **`git reset --hard` destroys uncommitted work** — check
before starting, not after:

```bash
# 4 — MUST print nothing. If it does not, commit or stash before going any further.
git status --short
```

**Yesterday's gate applies today.** Part [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md)
adds two settings fields, and Day 9's example-file check will refuse until the file is regenerated. That is
the gate working, not a problem:

```bash
# 5 — green now; it will go red in 4.1 and you will regenerate
uv run python scripts/gen_env_example.py --check
```

**No packages are added today.** Everything uses `git`, the standard library, and the three packages Day 3
pinned plus the two Day 9 added:

```bash
# 6 — confirm, do not assume
git --version
uv run python -c "import httpx2, fastapi, pydantic_settings; print('httpx2', httpx2.__version__, '| fastapi', fastapi.__version__, '| pydantic-settings', pydantic_settings.__version__)"
```

| Tool | Observed here | How | Why today needs it |
| --- | --- | --- | --- |
| git | `2.54.0.windows.1` | `git --version` (Day 0's row) | the artifact identity in [2.1](parts/02-promotion/2.1-build-once-promote-the-artifact.md) is a commit SHA |
| httpx2 | `2.12.0` | pinned on [Day 3](../day-003-pulse-v0/LESSON.md) | the concurrency client in [3.3](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md) |
| pydantic-settings | `2.15.0` | pinned on [Day 9](../day-009-configuration-and-secrets/LESSON.md) | the two new fields in [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md) |

⚠️ **`uv add` is not run today.** `git diff pyproject.toml uv.lock` must be empty at the end — the first day
since Day 8 with no new dependency.

---

## §4 Build brief

Today changes **project code** in three places and writes a small deployment toolchain in `lab/` that is
deleted at the end.

| File | Explained in | What it is |
| --- | --- | --- |
| `pulse/config.py` | [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md) | **Yours to change** — two fields: `build_id`, `release_id` |
| `pulse/api.py` | [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md) · [4.2](parts/04-pulse-across-environments/4.2-the-environment-banner.md) | **Yours to change** — two fields on `/version`, and the header middleware |
| `pulse/observability.py` | [4.2](parts/04-pulse-across-environments/4.2-the-environment-banner.md) | **Yours to write** — the deploy-identity logging filter |
| `.env.example` | [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md) | **Yours to regenerate** — Day 9's gate refuses until you do |
| `lab/envs/{dev,staging,prod}.env` | [1.1](parts/01-what-an-environment-is/1.1-an-environment-is-a-deploy-not-a-folder.md) | **Yours to write** — three complete configurations, every key in all three |
| `lab/differences.md` | [1.2](parts/01-what-an-environment-is/1.2-the-four-things-that-differ.md) | **Yours to write** — with a `Deliberate?` column and three "not yet real" rows |
| `lab/parity.md` | [1.3](parts/01-what-an-environment-is/1.3-dev-prod-parity-and-the-three-gaps.md) | **Yours to write** — the three gaps, measured, including "what will make it worse" |
| `lab/switched.py` · `lab/settings_only.py` | [1.4](parts/01-what-an-environment-is/1.4-the-environment-name-is-not-a-switch.md) | **Yours to write** — `prod-eu`, and what each version does with it |
| `lab/promote.sh` | [2.1](parts/02-promotion/2.1-build-once-promote-the-artifact.md) | **Yours to write** — refuses on a dirty tree |
| `lab/build.sh` · `lab/release.sh` · `lab/run.sh` | [2.2](parts/02-promotion/2.2-build-release-run.md) | **Yours to write** — the three stages, and an append-only ledger |
| `lab/chain.txt` · `lab/gate.sh` | [2.3](parts/02-promotion/2.3-the-promotion-gate.md) | **Yours to write** — the order as data, and the four conditions |
| `lab/rebuild/requirements-*.txt` | [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) | **Yours to write** — a range and a pin, resolved side by side |
| `lab/production_promises.md` · `lab/promises.tsv` · `lab/reset_env.sh` | [3.1](parts/03-what-production-promises/3.1-what-the-word-production-promises.md) | **Yours to write** — four questions, and a guard that is data rather than code |
| `lab/data_policy.tsv` · `lab/gen_tickets.py` · `lab/refresh_data.sh` | [3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md) | **Yours to write** — a required seed, and a refusal to copy real data downwards |
| `lab/lying_dep.py` · `lab/load.py` · `lab/staging_caveats.md` | [3.3](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md) | **Yours to write** — the same code at concurrency 2 and 40 |
| `lab/verify.sh` | [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md) | **Yours to write** — the ledger against the running service |
| `lab/promote_and_verify.sh` | [4.3](parts/04-pulse-across-environments/4.3-the-promotion-that-was-not-verified.md) | **Yours to write** — four stages; **the red gate** |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — three measurement rows |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — two rows, first symptom before cause |
| `docs/ARCHITECTURE.md` | §11 | **Yours to update** — `pulse` now exists in three deploys |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.1](parts/01-what-an-environment-is/1.1-an-environment-is-a-deploy-not-a-folder.md), the
  three environments differ in **port** only because they share one machine. Write down what would differ
  instead on three machines, and which of today's checks would break.
- `TODO(me)` In [1.2](parts/01-what-an-environment-is/1.2-the-four-things-that-differ.md), fill in the
  `differences.md` table for a system you actually use outside this project. **The rows you cannot fill in are
  the finding.**
- `TODO(me)` In [1.3](parts/01-what-an-environment-is/1.3-dev-prod-parity-and-the-three-gaps.md), record the
  build-environment fingerprint in `docs/PACKAGES.md`. **Day 21 will compare against it**, and a "before"
  number you did not take is a comparison you cannot make.
- `TODO(me)` In [1.4](parts/01-what-an-environment-is/1.4-the-environment-name-is-not-a-switch.md), run the
  environment-branching grep over `pulse/` and justify **in one sentence** every match you decide to keep. If
  you cannot, it is not an exception.
- `TODO(me)` In [2.2](parts/02-promotion/2.2-build-release-run.md), the release counter breaks if two releases
  are created at once. Say what you would use instead, and why Day 55's answer (a git commit) solves it.
- `TODO(me)` In [2.2](parts/02-promotion/2.2-build-release-run.md), `release.sh` stores a `config_hash` and
  nothing ever checks it. **Make `run.sh` verify it before launching**, and then make it fail on purpose by
  editing the config file.
- `TODO(me)` In [2.3](parts/02-promotion/2.3-the-promotion-gate.md), add a **recorded bypass** — a `--reason`
  that is required and appends a row to a log — and then decide what bypass rate would tell you a condition is
  wrong.
- `TODO(me)` In [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md), decide whether
  the build ID should come from the **commit** or from the **tree** (`git rev-parse HEAD^{tree}`). Write the
  argument on both sides and pick one. **This is a real trade and there is no right answer that fits in a
  sentence.**
- `TODO(me)` In [3.1](parts/03-what-production-promises/3.1-what-the-word-production-promises.md), `reset_env.sh`
  reads `may_be_reset` by column position. Make it read by **column name**, the way
  [3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md)'s script does, and
  say why that script got it right and this one did not.
- `TODO(me)` In [3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md),
  extend `gen_tickets.py` to produce **three** realistic messes the current version does not: a very long body,
  a non-ASCII subject, and an empty-but-present field. Then check whether `pulse` still accepts them.
- `TODO(me)` In [3.3](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md), predict the
  p99 at concurrency 40 **before running it**, and write the prediction down. A prediction made afterwards is
  not one.
- `TODO(me)` In [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md), `verify.sh`
  contains one line that re-reads a value it already has. Find it, delete it, and say what class of change
  leaves lines like that behind.
- `TODO(me)` In [4.1](parts/04-pulse-across-environments/4.1-one-artifact-three-releases.md), make `verify.sh`
  **refuse when any field is empty on either side**, then prove it by breaking the JSON pattern. This is the
  seventh vacuous-check in ten days.
- `TODO(me)` In [4.3](parts/04-pulse-across-environments/4.3-the-promotion-that-was-not-verified.md), replace
  the fixed `sleep 4` before verification with a **bounded poll**. Say what deadline you chose and what happens
  when it is exceeded.
- `TODO(me)` Write one paragraph on what Days 5, 6, 7, 8, 9 and 10 have in common. **Six mechanisms, one
  property.** Name the property and the single kind of check that would have caught all six.
- `TODO(me)` Delete every lab file, confirm with `netstat` that nothing survives on 8000–8002 or 8017, and
  prove `git diff pulse/` shows **only** today's intended changes.

---

## §5 The check that must be able to fail

**Three gates today**, and they fail on three different kinds of wrong: a promotion that should not happen, a
copy that must not be made, and a deploy that did not arrive.

**Gate one — the promotion gate** ([2.3](parts/02-promotion/2.3-the-promotion-gate.md)):

```bash
bash days/day-010-environments-and-promotion/lab/gate.sh staging
```

Four conditions. **Each one must be seen red on purpose**: change the build with an empty commit, add a key to
one environment's config and not the other, and stop the previous environment. **A gate whose conditions you
have never failed is a light, not a gate.**

**Gate two — the data guard** ([3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md)):

```bash
bash days/day-010-environments-and-promotion/lab/refresh_data.sh prod staging
```

Must refuse, and must name the alternative command. Then run it `staging → dev` and watch it allow.

**Gate three — the day's red gate: promote and verify**
([4.3](parts/04-pulse-across-environments/4.3-the-promotion-that-was-not-verified.md)):

```bash
bash days/day-010-environments-and-promotion/lab/promote_and_verify.sh staging
```

| Stage | With a clean staging | With an old release already holding the port |
| --- | --- | --- |
| gate — four conditions | green | **green** |
| build | `build-14a1dcd2f0b4` | **identical** |
| release recorded | `r014` | **recorded** |
| run — command issued | yes | **yes** |
| `/version` `environment` | `staging` | **`staging`** |
| `/version` `build_id` | matches | **matches** |
| `/version` `release_id` | matches | **`r015` ≠ `r017`** |

**Six of seven rows are identical.** The gate is the last one — and it is the only check in the entire
pipeline that asks the running service rather than reading a file.

**Make it go red on purpose:** start an old release on staging's port first, then promote. **Then restore and
confirm green** — a drill that only goes red has proved the failure, not the fix.

---

## §6 Cost & quota budget

| Resource | Today | Note |
| --- | --- | --- |
| Model calls | **`0`** | no provider is contacted |
| Tokens | **`0`** | — |
| CI minutes | **`0`** | nothing pushed today runs in CI |
| New packages | **`0`** | first zero-dependency day since Day 8. `git diff pyproject.toml uv.lock` must be empty |
| Disk | **~50 KB** | release and build records, three env files, a few small scripts |
| RAM | **~180 MB peak** | **three** uvicorn processes at roughly 60 MB each — the most this phase asks for (Addendum 02 §3) |
| CPU | one burst of 40 concurrent requests | [3.3](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md), on four cores, all loopback |
| Network | **a few hundred KB** | two `uv pip compile` resolutions against the package index in [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md). **Everything else is loopback.** |

**If you would rather send nothing outside this machine:** the only external traffic is the two `uv pip
compile` calls, and they can be skipped — you lose the demonstration that a version range resolves to
*today's* release, and nothing else. **Everything in sections 1, 3 and 4 is entirely offline.**

---

## §7 Traps

| # | Trap | What it looks like | Where it is covered |
| --- | --- | --- | --- |
| 1 | **A branch used as an environment** | promoting produces a merge conflict | [1.1](parts/01-what-an-environment-is/1.1-an-environment-is-a-deploy-not-a-folder.md) |
| 2 | **A shared database between environments** | a migration "in staging" alters production | [1.1](parts/01-what-an-environment-is/1.1-an-environment-is-a-deploy-not-a-folder.md) · [3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md) |
| 3 | **`if environment == "prod"`** | `prod-eu` silently takes the development branch | [1.4](parts/01-what-an-environment-is/1.4-the-environment-name-is-not-a-switch.md) |
| 4 | **Rebuilding per environment** | production runs the one artifact nobody tested | [2.1](parts/02-promotion/2.1-build-once-promote-the-artifact.md) |
| 5 | **A moving tag** (`python:3.12`, `v1.4.0` re-pointed) | the same name, two different objects | [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) |
| 6 | **A dependency range instead of a pin** | correct today; a different program next month | [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) |
| 7 | **A release ID from a clock** | two releases in one second collide | [2.2](parts/02-promotion/2.2-build-release-run.md) |
| 8 | **Copying production data downwards** | obligations arrive, protections do not | [3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md) |
| 9 | **A deterministic hash called "anonymisation"** | a stable pseudonym is re-identifiable by joining | [3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md) |
| 10 | **"It worked in staging"** | p99 nineteen times worse, `200`s, no errors | [3.3](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md) |
| 11 | **A vacuous check** — comparing two absences | `diff` of two empty streams is a match | [2.3](parts/02-promotion/2.3-the-promotion-gate.md) · [4.3](parts/04-pulse-across-environments/4.3-the-promotion-that-was-not-verified.md) |
| 12 | **A stale process holding the port** | the record says deployed; the old code is serving | [4.3](parts/04-pulse-across-environments/4.3-the-promotion-that-was-not-verified.md) |
| 13 | **`git reset --hard` with uncommitted work** | the work is gone; only the reflog remains | §3 · [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) |

**And the named trap from the plan's §5.1 that today touches: #1, the tutorial that runs on `:latest` with no
limits.** Its promotion cousin is the **moving tag** — trap 5 above. `:latest`, `python:3.12` and a re-pointed
`v1.4.0` are the same mistake: a name that is supposed to identify an object and is actually a pointer
somebody else can move. It works immediately, it teaches nothing that survives, and the day it changes
underneath you there is no diff to look at.

---

## §8 Verify before you build

Every page below was fetched on **2026-08-25**, the day this was written (Principle 8). Fetch them again on
the day you run it.

| Fact used | Source page | What was checked |
| --- | --- | --- |
| *"config is everything that is likely to vary between deploys"*; *"never grouped together as environments"*; the combinatorial-explosion warning | `https://12factor.net/config` | [1.1](parts/01-what-an-environment-is/1.1-an-environment-is-a-deploy-not-a-folder.md), [1.4](parts/01-what-an-environment-is/1.4-the-environment-name-is-not-a-switch.md) — quoted verbatim |
| the three stages; *"a release cannot be mutated once it is created"*; *"the run stage should be kept to as few moving parts as possible"* | `https://12factor.net/build-release-run` | [2.2](parts/02-promotion/2.2-build-release-run.md) — quoted verbatim |
| the three gaps — time, personnel, tools — and the traditional-versus-twelve-factor table | `https://12factor.net/dev-prod-parity` | [1.3](parts/01-what-an-environment-is/1.3-dev-prod-parity-and-the-three-gaps.md) — quoted verbatim |
| `logging.Filter.filter()` may modify the record; `%(name)s` formatting reads record attributes | `https://docs.python.org/3/library/logging.html` | [4.2](parts/04-pulse-across-environments/4.2-the-environment-banner.md) |
| `random.Random(seed)` is reproducible; `secrets` is the one to use when it must not be | `https://docs.python.org/3/library/random.html` · `.../secrets.html` | [3.2](parts/03-what-production-promises/3.2-data-is-the-thing-that-cannot-be-promoted.md) |
| `asyncio.Semaphore` admits N concurrent holders and queues the rest | `https://docs.python.org/3/library/asyncio-sync.html` | [3.3](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md) |
| `time.monotonic()` — *"only the difference between the results of two calls is valid"* | `https://docs.python.org/3/library/time.html` | [3.3](parts/03-what-production-promises/3.3-the-staging-environment-that-lied.md) |
| `git rev-parse`, `git hash-object`, `%cI`, `--allow-empty`, `rev-parse HEAD^{tree}` | `https://git-scm.com/docs/git-rev-parse` · `.../git-hash-object` · `.../git-commit` | [2.1](parts/02-promotion/2.1-build-once-promote-the-artifact.md), [2.2](parts/02-promotion/2.2-build-release-run.md), [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) |
| `uv pip compile` resolves a specification to exact pins without installing | `https://docs.astral.sh/uv/` | [2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) |
| FastAPI `@app.middleware("http")` runs for every response, including framework-generated errors | `https://fastapi.tiangolo.com/tutorial/middleware/` | [4.2](parts/04-pulse-across-environments/4.2-the-environment-banner.md) |

---

## §9 Say it in an interview

*"The environments day is where 'it worked in staging' stopped being something I said. I built the three
stages by hand — build, release, run — because until you have a release object you cannot answer 'what
changed' after a configuration edit: there is no artifact to point at and rollback becomes guesswork. And I
measured the parity gap rather than asserting it. The one that surprised me was the tools gap: two thousand
lines of pinned dependency graph in the lockfile, and underneath it four facts nothing pins — the operating
system, the Python patch version, OpenSSL and the ABI. Same commit, same lockfile, different program.*

*The thing I actually took away was the ending. I promoted a build to staging with every gate green — the
artifact matched, the configuration keys matched, the previous environment was healthy, the release was
recorded — and the change never arrived, because an old process still held the port and nothing in the
pipeline ever asked the running service what it was. Every artifact of the process said success. The only
check that caught it was a comparison between the release ledger and what the service reported about itself,
and I made it go red on purpose before I trusted it.*

*That was the sixth day running where the thing that was wrong was invisible to every cheap signal — a disk
that did not free, a process the kernel killed, exhausted connections, an expired certificate, a published
credential, and a deploy that did not take. The property they share is that a cheap signal examines something
nearby: the process, the file, the record. The failure is always one step further out. So what I now insist on
is one outside-in check per mechanism, with an independent source, and I check that it can actually fail —
because the recurring bug in my own checks has been comparing two absences and calling it a match."*

---

## §10 Done when

`days/day-010-environments-and-promotion/CHECKLIST.md` — every box ticked honestly. `./o done 10` counts them
and refuses to commit while any remain, and it **cannot** detect a dishonest tick (`docs/INCIDENTS.md` row 6).
That part is yours.

**Done is defined by understanding and green checks, not by anything else.** In particular: all three gates
must have been seen red *and* green, every one of `gate.sh`'s four conditions must have been failed
individually, the ports must be confirmed clear with `netstat`, and `git diff pulse/` must show only the
intended changes.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — paste this row verbatim, with the commit hash filled in:

```text
| 10 | 2026-08-25 | FND-13 | 14 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — three measurement rows, with the values *you* observed:

```text
| measurement: build-environment fingerprint | <python>/<openssl>/<platform>/<abi> = <16-hex> | 2026-08-25 | 10 | The four facts uv.lock does not pin (part 1.3). Day 21 compares against this; a container should make it constant across machines. |
| measurement: uv.lock pinned lines | <n> | 2026-08-25 | 10 | Printed next to the four unpinned facts above. The ratio is the honest size of the tools gap before Phase 3. |
| measurement: p99 at concurrency 2 vs 40 | <a>s vs <b>s, same code and config | 2026-08-25 | 10 | Part 3.3. The number behind "it worked in staging". Day 63 replaces this hand-rolled percentile with a histogram. |
```

**`docs/INCIDENTS.md`** — two rows. **Write the first symptom before you investigate**, not after:

```text
| 17 | 2026-08-25 | 10 | Promotion gate green, release recorded, and the old process was still serving staging (part 4.3) | ... | ... | ... | ... |
| 18 | 2026-08-25 | 10 | Same artifact and configuration; p99 nineteen times worse at concurrency 40, with 200s and no error lines (part 3.3) | ... | ... | ... | ... |
```

**Row 17 must explicitly link Day 9's row 16, Day 8's row 13, Day 7's row 22, Day 6's row 19 and Day 5's row
16** — six consecutive days — and must name the shared property in one sentence, plus the single kind of check
that would have caught all six.

**`docs/DECISIONS.md`** — an ADR **if** the `TODO(me)` in
[2.4](parts/02-promotion/2.4-the-rebuild-that-promoted-something-different.md) reached a conclusion about
whether the build identity comes from the commit or from the tree. That is a decision Day 15 will inherit and
a stranger will want the reasoning for.

**`docs/ARCHITECTURE.md`** — `pulse` is no longer one box. Add the three deploys, note that they share one
artifact and differ only in configuration, and record that **none of them is a production system** by
[3.1](parts/03-what-production-promises/3.1-what-the-word-production-promises.md)'s four promises.

**The commit:**

```text
day 010: environments and promotion — one artifact, three releases, and the deploy that never arrived — closes FND-13
```
