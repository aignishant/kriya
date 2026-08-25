---
day: 9
phase: 1
phase_name: "The production mental model and the machine"
title: "Configuration and secrets"
ids: [FND-11, FND-12, SEC-01]
principles: [1, 2, 4, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18]
kind: lab
plan_version: "v1.0.0"
parts: 21
generated: "2026-08-25"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 9 — Configuration and secrets — the twelve-factor service, `.env`, and code that refuses to start rather than failing late

> **Yesterday (Day 8):** the protocol on the wire and the layer underneath it, ending with `pulse` completely
> unreachable behind an expired certificate while the health check returned `200` — the fourth consecutive day
> where the service was down and every signal was green.
> **Today:** the service's *inputs*. What varies between one running copy and another, how it arrives, why it
> is always text, why a bad value should stop the process rather than surprise you at 3am — and the first
> value `pulse` holds that must never be seen by anyone. Today ends with that value published, on purpose, by
> a line of code that every part of this day recommends.
> **Tomorrow (Day 10):** environments and promotion — what the word "production" actually promises, and why
> moving a build between deploys only means something if the configuration is the only thing that changed.

---

## §1 Where we are

For eight days `pulse` has been a thing that runs. Today it becomes a thing that can be *told* something.

Start with a touring theatre company. One play, forty towns. The script is identical everywhere — same lines,
same cues, same order — and if it were not identical, then "we rehearsed it" would mean nothing, because you
rehearsed something else. What changes in every town is the stuff around the play: which door the actors come
in through, the code on that door, how many seats there are, the phone number of the local box office.

The stage manager who writes the door code onto page one of the script has done two things wrong, and only
one of them is obvious. The obvious one: next week the code is for a building two hundred miles away. The one
nobody notices for a year: **the code is now in forty photocopies, in forty bags, in forty houses**, and one
of those bags gets left on a train. There is no way to know which. There is no way to get them back. And
changing the code means changing it at a venue the company has already left.

That is the whole day. The first half is the boring, load-bearing half: what is script and what is a door
code, how the door code reaches the actors, and what happens when somebody writes it down wrong. The second
half is the door code itself — the value where *possession is permission*, where sharing destroys your ability
to say who did something, and where taking it back hurts everyone who legitimately had it.

And the ending is not the one you expect. Every part of today argues for the same excellent practice: **the
service should say what it was configured with, once, at startup, in the log.** It is the single most useful
diagnostic line a service has, and without it a deploy that received the wrong environment's settings is
completely undetectable.

Today you will write that line, with the credential declared as an ordinary string, and watch it publish a
secret to a file, an aggregator and a backup in one go.

**Days 5 through 8 all ended with a failure nobody could see. Today's ends with one everybody can see —
except you, because to you it was a successful startup.** That asymmetry is the point, and it is the reason
this is the day the repository stops being able to go public by accident.

---

## §2 The map

**Section 1 — `01-configuration`.** What configuration *is*, where it comes from, and the four properties of
the channel it arrives on. Nothing here is about secrets; everything here is what secrets are built on.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [What configuration actually is](parts/01-configuration/1.1-what-configuration-actually-is.md) | could you make this repository public in the next few seconds? | foundation |
| 1.2 | [The environment is the interface](parts/01-configuration/1.2-the-environment-is-the-interface.md) | you set the variable and the service ignored it — why? | foundation |
| 1.3 | [Everything from the environment is a string](parts/01-configuration/1.3-everything-from-the-environment-is-a-string.md) | why does `DEBUG=false` turn debugging **on**? | foundation |
| 1.4 | [The precedence ladder](parts/01-configuration/1.4-the-precedence-ladder.md) | four sources say four different things — which wins, and how do you find out? | working |
| 1.5 | [`.env` is a developer convenience](parts/01-configuration/1.5-dotenv-is-a-developer-convenience.md) | it works perfectly in a deploy — so what exactly is wrong with it? | working |

**Section 2 — `02-typed-settings`.** Turning text into an object you can trust. Built by hand first, then
adopted from a library, because a tool you have not built once is a tool whose failures are magic
(Principle 4).

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Hand-rolling the settings object](parts/02-typed-settings/2.1-hand-rolling-the-settings-object.md) | what does one object give you that six `os.environ.get` calls cannot? | working |
| 2.2 | [Adopting `pydantic-settings`](parts/02-typed-settings/2.2-adopting-pydantic-settings.md) | which six holes does the library close, and what does it cost? | working |
| 2.3 | [Naming, prefixes, and the variable nobody read](parts/02-typed-settings/2.3-naming-prefixes-and-the-variable-nobody-read.md) | `PULSE_PROT=8001` — six parts have walked past it; what notices? | working |
| 2.4 | [The settings object read at import time](parts/02-typed-settings/2.4-the-settings-object-read-at-import-time.md) | a test passes alone and fails in the suite — what changed? | production |

**Section 3 — `03-fail-fast`.** What a service does when the configuration is wrong: refuse, immediately,
naming the field — and where that check belongs, which is not where most people put it.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Fail fast — the crash that saves the night](parts/03-fail-fast/3.1-fail-fast-the-crash-that-saves-the-night.md) | why is exiting non-zero safer than logging an error and carrying on? | working |
| 3.2 | [Validating the value, not just its presence](parts/03-fail-fast/3.2-validating-the-value-not-just-its-presence.md) | three settings, all valid, describing an impossible system — which check sees it? | working |
| 3.3 | [Where the check belongs — startup versus readiness](parts/03-fail-fast/3.3-where-the-check-belongs-startup-versus-readiness.md) | why does checking the database at startup turn a blip into an outage that outlives it? | production |
| 3.4 | [The service that started with the wrong config](parts/03-fail-fast/3.4-the-service-that-started-with-the-wrong-config.md) | every value legal, every check green, and the dashboard shows no data — how? | production |

**Section 4 — `04-secrets`.** The subset of configuration where possession is authority. This is `SEC-01`, the
first of thirty-three security IDs, and it is deliberately on Day 9 rather than in Phase 21.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [What makes a secret a secret](parts/04-secrets/4.1-what-makes-a-secret-a-secret.md) | why is a customer's email address not a secret? | foundation |
| 4.2 | [The seven places a secret leaks](parts/04-secrets/4.2-the-seven-places-a-secret-leaks.md) | which two exposures can never be undone? | working |
| 4.3 | [Redaction that actually holds](parts/04-secrets/4.3-redaction-that-actually-holds.md) | why does a list of sensitive names always eventually fail? | working |
| 4.4 | [A secret has a lifetime](parts/04-secrets/4.4-a-secret-has-a-lifetime.md) | you have nine replicas — why can you not just change the key? | production |
| 4.5 | [The environment variable is not a vault](parts/04-secrets/4.5-the-environment-variable-is-not-a-vault.md) | which unrelated process on this machine is holding your provider key right now? | production |

**Section 5 — `05-pulse-configured`.** All of it, landing on the service. The only section that changes
project code.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 5.1 | [`pulse/config.py` — the settings object](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md) | nine requirements from four sections, in forty lines — where does each one land? | production |
| 5.2 | [`.env.example` — the contract with a stranger](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md) | why is a hand-written example file worse than none at all? | production |
| 5.3 | [The secret that reached the log](parts/05-pulse-configured/5.3-the-secret-that-reached-the-log.md) | the good practice published a credential — what do you do first? | production |

---

## §3 Setup — run this

**Profile:** `core` only (Addendum 02 §4) — `pulse` plus a handful of short-lived uvicorn processes on
loopback. **Nothing else may be running.**

**Stop first.** Today runs several servers on ports 8000 and 8010–8016, and this machine has four logical CPUs
(`docs/PACKAGES.md`, Day 0). Anything left over from Days 4–8 will bind a port you need or make a result
meaningless:

```bash
# 1 — nothing from previous days survives
pgrep -af 'uvicorn|blackhole|hangy|hungry|burn|allocate|holder|slow_resolver|terminator' || echo "clean"
pkill -f 'blackhole|hangy|hungry|burn|allocate|holder|slow_resolver|terminator' 2>/dev/null

# 2 — the ports this day uses must be free, confirmed rather than assumed
netstat -ano | grep -E ':(8000|801[0-6]|8099).*LISTENING' || echo "all ports free"

# 3 — this day's scratch folder
./o scaffold 9
```

**Secrets before the secret exists (Principle 9).** Today is the first day `pulse` has a field for a
credential, and the first day you will create a `.env`. The ignore rule was written on **Day 0**, before
either existed — confirm it rather than trusting it:

```bash
# 4 — CONFIRM the ignore covers .env BEFORE you create one, and that .env.example is NOT ignored
sed -n '1,12p' .gitignore
git check-ignore -v .env         && echo "✅ .env is ignored by a Day 0 rule"
git check-ignore -v .env.example || echo "✅ .env.example is NOT ignored — it is meant to be committed"
```

**The two exit codes must differ.** `.env` ignored (exit `0`), `.env.example` not ignored (exit `1`). If they
do not, stop and fix `.gitignore` before writing anything — adding the rule after the file exists is too late
by the width of one `git add -A`.

**The one new dependency.** This is the first package added since Day 3 — four days with none, and the streak
ends deliberately. **Look the version up yourself** (Principle 7); the number below was observed on
**2026-08-25** and it moves:

```bash
# 5 — look it up live, then pin exactly
curl -sS --compressed https://pypi.org/pypi/pydantic-settings/json | tr ',' '\n' | grep -m1 -o '"version":"[^"]*"'
uv add pydantic-settings==2.15.0
uv run python -c "import pydantic_settings, pydantic; print('pydantic-settings', pydantic_settings.__version__); print('pydantic', pydantic.VERSION)"
```

| Tool | Observed here | How | Why today needs it |
| --- | --- | --- | --- |
| pydantic-settings | `2.15.0` | `curl` PyPI, then `uv add` | the settings class in [2.2](parts/02-typed-settings/2.2-adopting-pydantic-settings.md) and [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md) |
| python-dotenv | `1.2.3` | **transitive** — required by the above | parses `.env`; named in [1.5](parts/01-configuration/1.5-dotenv-is-a-developer-convenience.md) |
| pydantic | `2.13.4` | already present via FastAPI (Day 3) | `SecretStr`, `Field`, `model_validator` |

⚠️ **`pydantic` is not added today** — FastAPI already required it on Day 3. Print its version anyway: a
settings library and a validation library disagreeing about pydantic's major version is a real and unpleasant
failure. **Three rows go into `docs/PACKAGES.md`** (§11).

---

## §4 Build brief

Today writes **project code** for the first time since Day 3. Two files under `pulse/`, one under `scripts/`,
one at the repository root — plus a lab folder that is deleted at the end.

| File | Explained in | What it is |
| --- | --- | --- |
| `pulse/config.py` | [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md) | **Yours to write** — seven fields, one validator, one cached accessor |
| `pulse/api.py` | [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md) | **Yours to change** — a composition root, a startup line, `Depends`, `environment` on `/version` |
| `scripts/gen_env_example.py` | [5.2](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md) | **Yours to write** — `--write` and `--check` |
| `.env.example` | [5.2](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md) | **Yours to generate** — committed; the only file here that is |
| `lab/ladder.py` | [1.4](parts/01-configuration/1.4-the-precedence-ladder.md) | **Yours to write** — four sources, and the `(from …)` column that matters |
| `lab/awkward.env` | [1.5](parts/01-configuration/1.5-dotenv-is-a-developer-convenience.md) | **Yours to write** — eight lines, three defects |
| `lab/settings_by_hand.py` | [2.1](parts/02-typed-settings/2.1-hand-rolling-the-settings-object.md) | **Yours to write** — the version you throw away in 2.2 |
| `lab/settings_pydantic.py` | [2.2](parts/02-typed-settings/2.2-adopting-pydantic-settings.md) | **Yours to write** — the same four settings, declared once |
| `lab/collide.py` · `lab/audit_env.py` | [2.3](parts/02-typed-settings/2.3-naming-prefixes-and-the-variable-nobody-read.md) | **Yours to write** — the collision, and the detector that finally catches `PULSE_PROT` |
| `lab/import_time.py` · `lab/lazy_time.py` · `lab/test_import_time.py` | [2.4](parts/02-typed-settings/2.4-the-settings-object-read-at-import-time.md) | **Yours to write** — two shapes, one deliberately failing test |
| `lab/fail_late.py` · `lab/fail_fast.py` | [3.1](parts/03-fail-fast/3.1-fail-fast-the-crash-that-saves-the-night.md) | **Yours to write** — `500` at request time versus exit `78` at startup |
| `lab/rungs.py` · `lab/consistent.py` | [3.2](parts/03-fail-fast/3.2-validating-the-value-not-just-its-presence.md) | **Yours to write** — the ladder, and three valid values that are jointly impossible |
| `lab/startup_dep.py` · `lab/ready_dep.py` | [3.3](parts/03-fail-fast/3.3-where-the-check-belongs-startup-versus-readiness.md) | **Yours to write** — the fleet that cannot come back, and the one that waits |
| `lab/announcing.py` · `lab/config_drill.sh` · `lab/smoke.sh` | [3.4](parts/03-fail-fast/3.4-the-service-that-started-with-the-wrong-config.md) | **Yours to write** — six observations, four identical; **red gate one** |
| `lab/bearer.py` · `lab/classification.md` | [4.1](parts/04-secrets/4.1-what-makes-a-secret-a-secret.md) | **Yours to write** — two identical `True`s, and the table with a blast-radius column |
| `lab/leaky.py` · `lab/traceback_leak.py` | [4.2](parts/04-secrets/4.2-the-seven-places-a-secret-leaks.md) | **Yours to write** — a key in a URL, and a key in an exception nobody logged |
| `lab/secrets_type.py` · `lab/secrets_escape.py` · `lab/redact_filter.py` | [4.3](parts/04-secrets/4.3-redaction-that-actually-holds.md) | **Yours to write** — six safe paths, three escapes, one imperfect filter |
| `lab/provider.py` · `lab/caller.py` · `lab/rotate_drill.sh` | [4.4](parts/04-secrets/4.4-a-secret-has-a-lifetime.md) | **Yours to write** — ten failures versus zero, from one step |
| `lab/spawner.py` · `lab/from_file.py` · `lab/run_secrets/` | [4.5](parts/04-secrets/4.5-the-environment-variable-is-not-a-vault.md) | **Yours to write** — the child that inherited a credential it never asked for |
| `lab/leaky_config.py` · `lab/leak_drill.py` · `lab/leak_gate.sh` | [5.3](parts/05-pulse-configured/5.3-the-secret-that-reached-the-log.md) | **Yours to write** — one annotation, one leak; **red gate two** |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — three rows, dated |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — three rows, first symptom before cause |
| `docs/DECISIONS.md` + an ADR | §11 | **Yours to write** — fail-fast in a single-process service, before Day 41 exists |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.1](parts/01-configuration/1.1-what-configuration-actually-is.md), write the full setting
  inventory for `pulse` yourself **before** reading the table, then compare. Any row you disagree with is worth
  arguing out in writing, and the `secret?` column is the one to argue about.
- `TODO(me)` In [1.3](parts/01-configuration/1.3-everything-from-the-environment-is-a-string.md), find a
  **fifth** state an environment variable can be in that the part does not list, or prove there are only four.
- `TODO(me)` In [1.4](parts/01-configuration/1.4-the-precedence-ladder.md), make `read_env_file` **raise** on a
  line that is neither blank, nor a comment, nor a `KEY=value` pair, and say in one sentence which of
  [1.3](parts/01-configuration/1.3-everything-from-the-environment-is-a-string.md)'s rules that is.
- `TODO(me)` In [2.1](parts/02-typed-settings/2.1-hand-rolling-the-settings-object.md), close the empty-string
  hole in `_raw` — **per field, not globally** — and write down the one field where stripping whitespace would
  be wrong.
- `TODO(me)` In [2.3](parts/02-typed-settings/2.3-naming-prefixes-and-the-variable-nobody-read.md), make
  `audit_env.py` read the prefix from `Settings.model_config` instead of retyping it, **and** add the assertion
  that `known_names()` is non-empty. The second one matters more than the first.
- `TODO(me)` In [2.4](parts/02-typed-settings/2.4-the-settings-object-read-at-import-time.md), write the
  `autouse` fixture that clears the settings cache before and after every test, and then deliberately remove the
  *after* half and find the test that starts failing.
- `TODO(me)` In [3.2](parts/03-fail-fast/3.2-validating-the-value-not-just-its-presence.md), classify each of
  `pulse`'s validation rules as an **impossibility** or a **preference**, and delete or relocate every
  preference. Write the argument down; "because the policy says so" is not an argument.
- `TODO(me)` In [3.4](parts/03-fail-fast/3.4-the-service-that-started-with-the-wrong-config.md), find a
  **seventh** observation that would distinguish the two deploys, and say whether a machine or a human would
  notice it.
- `TODO(me)` In [4.1](parts/04-secrets/4.1-what-makes-a-secret-a-secret.md), fill in the `Rotation` column of
  the classification table for a provider you actually intend to use on Day 126. **If the answer is "I do not
  know", that is the finding**, and it belongs in the table.
- `TODO(me)` In [4.2](parts/04-secrets/4.2-the-seven-places-a-secret-leaks.md), find an **eighth** leak path
  the part does not list, produce it if you safely can, and rank it on the duration scale.
- `TODO(me)` In [4.3](parts/04-secrets/4.3-redaction-that-actually-holds.md), make `redact_filter.py` catch the
  fourth test line, then find a **new** false positive your improved pattern creates. Both halves.
- `TODO(me)` In [4.5](parts/04-secrets/4.5-the-environment-variable-is-not-a-vault.md), answer Day 5's
  outstanding question: **is `chmod 600` actually honoured on this filesystem?** Write the answer into
  `docs/PACKAGES.md`, because it decides whether the file rung of the ladder is real on this machine.
- `TODO(me)` In [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md), fix **three** things
  in `_configure()`: make the unknown-variable case exit non-zero, repair the garbled "known settings are"
  expression, and give the model-level validator's refusal a readable location instead of a bare `:`.
- `TODO(me)` In [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md), decide the trade on
  printing `error.get("input")` in a refusal: more useful messages for ordinary fields, a credential in the
  deployment log for one. **Write the decision and the reason**, then implement it.
- `TODO(me)` Convert `pulse/api.py` to an **application factory** — `create_app(settings) -> FastAPI` — and
  then write the test that `docs_enabled` could not previously have.
- `TODO(me)` In [5.2](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md), fix the
  boolean rendering (`True` should be `true`) and handle `Optional[SecretStr]`, which the type check currently
  misses.
- `TODO(me)` Turn [5.3](parts/05-pulse-configured/5.3-the-secret-that-reached-the-log.md)'s shell gate into a
  **pytest** using `caplog`, and add it to `./o check`. Day 13 will run it in CI; today it should already run
  locally.
- `TODO(me)` Delete every lab file, delete `lab/run_secrets/`, confirm with `netstat` that nothing survives on
  8000, 8010–8016 or 8099, and prove `git diff pulse/` is empty. **Two drills today modified project code.**

---

## §5 The check that must be able to fail

**Two red gates today**, and they fail on opposite sides of the same idea: one catches a configuration that is
*wrong*, one catches a configuration that is *published*.

**Gate one — the wrong deploy** ([3.4](parts/03-fail-fast/3.4-the-service-that-started-with-the-wrong-config.md)):

```bash
bash days/day-009-configuration-and-secrets/lab/config_drill.sh
bash days/day-009-configuration-and-secrets/lab/smoke.sh prod http://127.0.0.1:8014
```

| Observation | Intended (`prod`) | Wrong-but-valid (`dev`) |
| --- | --- | --- |
| `/healthz` | `200` | `200` |
| `/version` status | `200` | `200` |
| `/docs` | `404` | **`200`** |
| reports as | `prod` | **`dev`** |
| error lines in its own log | `0` | `0` |
| the process | running | running |

**Four of six are identical.** The gate is `smoke.sh`, which must **exit 1** against the `dev` deploy and
**exit 0** against the `prod` one. Making it go red is the exercise: run it against the wrong deploy first.

**Gate two — the published credential** ([5.3](parts/05-pulse-configured/5.3-the-secret-that-reached-the-log.md)):

```bash
bash days/day-009-configuration-and-secrets/lab/leak_gate.sh
```

Green with `pulse` as written. Then change **one annotation** in `pulse/config.py` — `SecretStr` to `str` —
and watch the gate report the credential in the startup log and exit `1`. **Restore, and confirm green again**;
a drill that leaves the service modified is an incident you caused, and `git diff pulse/` must be empty at the
end of the day.

**And the third gate, which is not about failure at all** ([5.2](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md)):

```bash
uv run python scripts/gen_env_example.py --check
```

Green, then add a field to `pulse/config.py` without regenerating, watch it go red naming the exact command to
fix it, then restore. **Three gates, all three seen red on purpose, all three seen green afterwards.**

---

## §6 Cost & quota budget

| Resource | Today | Note |
| --- | --- | --- |
| Model calls | **`0`** | no provider is contacted; the "provider" in [4.4](parts/04-secrets/4.4-a-secret-has-a-lifetime.md) is a local process |
| Tokens | **`0`** | — |
| CI minutes | **`0`** | nothing pushed today runs in CI — but [5.2](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md)'s check adds a step to Day 13's job |
| New packages | **2** | `pydantic-settings==2.15.0` (direct) and `python-dotenv==1.2.3` (transitive). First since Day 3 |
| Disk | **~500 KB** | ~200 KB in `.venv` for the new packages, plus lab files and `/tmp` logs |
| RAM | **~180 MB peak** | up to three uvicorn processes at roughly 60 MB each (Addendum 02 §3) |
| Network | **a few hundred KB** | one PyPI metadata fetch and two wheel downloads. **Everything else is loopback.** |
| Credentials created | **`0` real** | every value today contains the words `not-a-real-credential` |

**If you would rather send nothing outside this machine:** the only external traffic today is the `uv add`.
There is no way around it — the package has to come from somewhere — and after it completes, **every remaining
command in this day is loopback or local disk.**

---

## §7 Traps

| # | Trap | What it looks like | Where it is covered |
| --- | --- | --- | --- |
| 1 | **`bool(os.environ.get("X"))`** | `DEBUG=false` turns debugging **on**; no error, no log line | [1.3](parts/01-configuration/1.3-everything-from-the-environment-is-a-string.md) |
| 2 | **`get(name, default)` with an empty value** | the default does not fire; an empty credential is sent to a provider | [1.3](parts/01-configuration/1.3-everything-from-the-environment-is-a-string.md) |
| 3 | **No `env_prefix`** | a CI runner's `HOST` becomes your listen address | [2.3](parts/02-typed-settings/2.3-naming-prefixes-and-the-variable-nobody-read.md) |
| 4 | **`extra="forbid"` believed to catch everything** | it catches a typo in `.env`, **not** a typo in a real environment variable | [2.2](parts/02-typed-settings/2.2-adopting-pydantic-settings.md) · [2.3](parts/02-typed-settings/2.3-naming-prefixes-and-the-variable-nobody-read.md) |
| 5 | **`settings = Settings()` at module scope** | a test passes alone and fails in the suite | [2.4](parts/02-typed-settings/2.4-the-settings-object-read-at-import-time.md) |
| 6 | **A dependency check at startup** | a blip becomes a crash-loop that outlives it | [3.3](parts/03-fail-fast/3.3-where-the-check-belongs-startup-versus-readiness.md) |
| 7 | **Catching the error and `sys.exit(0)`** | a perfect message, and every supervisor thinks it succeeded | [3.1](parts/03-fail-fast/3.1-fail-fast-the-crash-that-saves-the-night.md) |
| 8 | **A model validator with no `return self`** | `AttributeError: 'NoneType' object has no attribute …`, far from the cause | [3.2](parts/03-fail-fast/3.2-validating-the-value-not-just-its-presence.md) |
| 9 | **`docs_url=None` and not `redoc_url`** | one documentation UI off, the other serving the same document | [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md) |
| 10 | **A credential in a URL query string** | logged by uvicorn, the ingress, and every proxy — none of whose retention you own | [4.2](parts/04-secrets/4.2-the-seven-places-a-secret-leaks.md) |
| 11 | **`echo` into a secrets file** | a trailing newline, a `401`, and an error that never mentions whitespace | [4.5](parts/04-secrets/4.5-the-environment-variable-is-not-a-vault.md) |
| 12 | **A realistic-looking fake credential** | gets copied into a real deploy; trains people to ignore the scanner | [1.5](parts/01-configuration/1.5-dotenv-is-a-developer-convenience.md) · [5.2](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md) |

**And the named trap from the plan's §5.1 that today touches: #4, the autonomy with no brake.** Its
configuration cousin is a setting whose bound is missing — a `port` with no range, a `request_timeout` that
accepts `inf`, a retry count with no ceiling. Every field written today arrives with its bound in the same
line as its default, which is Principle 13 at the smallest possible scale, and
[3.2](parts/03-fail-fast/3.2-validating-the-value-not-just-its-presence.md) is where the argument is made.

---

## §8 Verify before you build

Every page below was fetched on **2026-08-25**, the day this was written (Principle 8). Fetch them again on
the day you run it — **the pydantic rows in particular move between minor versions.**

| Fact used | Source page | What was checked |
| --- | --- | --- |
| *"config is everything that is likely to vary between deploys"*; the open-source litmus test; *"never grouped together as environments"* | `https://12factor.net/config` | [1.1](parts/01-configuration/1.1-what-configuration-actually-is.md), [1.2](parts/01-configuration/1.2-the-environment-is-the-interface.md) — quoted verbatim |
| `os.environ` is a mapping of `str` to `str` | `https://docs.python.org/3/library/os.html` | [1.2](parts/01-configuration/1.2-the-environment-is-the-interface.md), [1.3](parts/01-configuration/1.3-everything-from-the-environment-is-a-string.md) |
| field value priority order; `PYDANTIC_SETTINGS_DEBUG`; default `env_prefix` is `''`; names are case-insensitive by default; `extra='forbid'` behaviour on dotenv vs env; `python-dotenv` parses the file | `https://docs.pydantic.dev/latest/concepts/pydantic_settings/` | [1.4](parts/01-configuration/1.4-the-precedence-ladder.md), [1.5](parts/01-configuration/1.5-dotenv-is-a-developer-convenience.md), [2.2](parts/02-typed-settings/2.2-adopting-pydantic-settings.md), [2.3](parts/02-typed-settings/2.3-naming-prefixes-and-the-variable-nobody-read.md) |
| `SecretStr` displays `'**********'` in `repr()`/`str()` and serialises as `**********`; `get_secret_value()`; `SecretStr('')` shows empty | `https://docs.pydantic.dev/latest/api/types/` | [4.3](parts/04-secrets/4.3-redaction-that-actually-holds.md) |
| `model_validator(mode='after')` is an instance method and **must return the instance** | `https://docs.pydantic.dev/latest/concepts/validators/` | [3.2](parts/03-fail-fast/3.2-validating-the-value-not-just-its-presence.md), [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md) |
| `protected_namespaces` defaults to `('model_validate', 'model_dump')` — so a `model_*` field is fine | `https://docs.pydantic.dev/latest/api/config/` | [5.1](parts/05-pulse-configured/5.1-pulse-config-the-settings-object.md) |
| `FieldInfo.default` holds `PydanticUndefined` when a field is required | `https://docs.pydantic.dev/latest/api/fields/` | [5.2](parts/05-pulse-configured/5.2-env-example-the-contract-with-a-stranger.md) |
| `subprocess.run` **inherits** the environment unless `env=` is passed | `https://docs.python.org/3/library/subprocess.html` | [4.5](parts/04-secrets/4.5-the-environment-variable-is-not-a-vault.md) |
| `secrets` for token generation; `hmac.compare_digest` is constant-time | `https://docs.python.org/3/library/secrets.html` · `https://docs.python.org/3/library/hmac.html` | [4.1](parts/04-secrets/4.1-what-makes-a-secret-a-secret.md) |
| `logging.Filter.filter()` may modify the record; `lru_cache` exposes `cache_clear()`; `time.monotonic()` is for intervals | `https://docs.python.org/3/library/logging.html` · `.../functools.html` · `.../time.html` | [4.3](parts/04-secrets/4.3-redaction-that-actually-holds.md), [2.4](parts/02-typed-settings/2.4-the-settings-object-read-at-import-time.md), [4.4](parts/04-secrets/4.4-a-secret-has-a-lifetime.md) |
| `pydantic-settings 2.15.0` requires `pydantic>=2.7.0`, `python-dotenv>=0.21.0`, `typing-inspection>=0.4.0` | `https://pypi.org/pypi/pydantic-settings/json` | §3, [2.2](parts/02-typed-settings/2.2-adopting-pydantic-settings.md) |

---

## §9 Say it in an interview

*"The configuration day is where I stopped thinking of secrets as a security topic and started thinking of
them as a typing problem. I built the settings object by hand first — one frozen object, read once at startup,
with explicit conversions — and the exercise was worth it because I could then name the six things the library
does that I could not cheaply do myself. Two of them mattered: reporting every validation error at once
instead of one per restart, which in a container is the difference between one crash-loop cycle and three, and
rejecting values it does not recognise instead of defaulting.*

*The thing I actually took away was the ending. Every part of that day argues for the same practice — log the
resolved configuration once at startup — because without it, a deploy that received the wrong environment's
settings is undetectable: it works, and it labels all its logs and metrics with the wrong environment, so the
production dashboard shows no data and every alert scoped to production is silently satisfied, because an
empty query result never crosses a threshold. Then I ran that same recommended line with the API key declared
as a plain string and watched it publish a credential into the log, the aggregator and the backup in one go.
Nobody wrote `print(key)`. The good practice caused it.*

*So now the credential is a `SecretStr` rather than a naming convention, because a type redacts in every
printing path including the ones that do not exist yet, and unwrapping it takes a method call I can grep the
whole codebase for. And I have a check that supplies a marker value and asserts it appears nowhere in the
service's own output — which I made go red by changing one annotation, because a gate I have only ever seen
pass is not a gate. I have not run a fleet at scale, but I can tell you exactly which line would have leaked
our key and why the response is rotate-first-fix-second, because the credential is live the entire time you
are editing the code."*

---

## §10 Done when

`days/day-009-configuration-and-secrets/CHECKLIST.md` — every box ticked honestly. `./o done 9` counts them
and refuses to commit while any remain, and it **cannot** detect a dishonest tick (`docs/INCIDENTS.md` row 6).
That part is yours.

**Done is defined by understanding and green checks, not by anything else.** In particular: all three gates
must have been seen red *and* green, `git diff pulse/` must be empty, `lab/run_secrets/` must be deleted, and
`git log --all -S 'LEAKDEMO' --oneline` must return nothing.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — paste this row verbatim, with the commit hash filled in:

```text
| 9 | 2026-08-25 | FND-11, FND-12, SEC-01 | 21 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — three rows, with the values *you* observed:

```text
| pydantic-settings | 2.15.0 | 2026-08-25 | 9 | Typed settings from the environment: prefix, bounds, SecretStr, all errors at once. First dependency since Day 3. Observed with `curl -sS https://pypi.org/pypi/pydantic-settings/json`. |
| python-dotenv | 1.2.3 | 2026-08-25 | 9 | Transitive (`pydantic-settings` requires `>=0.21.0`). It is the parser behind `env_file=`, which is why part 1.5 names it. |
| measurement: chmod 600 honoured on this filesystem? | <yes/no> | 2026-08-25 | 9 | Day 5's outstanding TODO, answered in part 4.5. Decides whether a file-based secret is a real control on this machine or theatre. |
```

**`docs/INCIDENTS.md`** — three rows. **Write the first symptom before you investigate**, not after:

```text
| 14 | 2026-08-25 | 9 | A deploy served /docs and reported environment=dev while every check was green (part 3.4) | ... | ... | ... | ... |
| 15 | 2026-08-25 | 9 | Rotating a credential with no overlap window dropped 10 of 19 requests (part 4.4) | ... | ... | ... | ... |
| 16 | 2026-08-25 | 9 | The startup config line published the model API key; one annotation was the cause (part 5.3) | ... | ... | ... | ... |
```

**Row 16 must state the response in order** — rotate, update holders, confirm no use, revoke, *then* fix the
annotation — and must say explicitly **why deleting the log is not on that list.** It must also link Day 8's
row 13, Day 7's row 22, Day 6's row 19 and Day 5's row 16, and name what makes today's different: **the first
four were invisible to everyone; this one is visible to everyone except you.**

**`docs/DECISIONS.md`** — one ADR is required today:

```text
| ADR-0006 | 2026-08-25 | accepted | pulse refuses to start on invalid configuration, exiting 78, before the rollout machinery that makes that safe exists. |
```

Its **"what would make us change our minds"** section must contain a number or an observable condition — the
honest one is *"if a refusal ever blocks a legitimate operator change during an incident before Day 41's
rolling update exists, revisit."*

**The commit:**

```text
day 009: configuration and secrets — the settings object, the refusal, and the credential in the log — closes FND-11, FND-12, SEC-01
```
