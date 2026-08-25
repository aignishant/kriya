# Day 9 — Checklist

**Definition of done.** `./o done 9` reads this file and refuses to commit while any `- [ ]` remains. It
counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd "$(git rev-parse --show-toplevel)" && \
PULSE_ENVIRONMENT=prod PULSE_DOCS_ENABLED=true uv run uvicorn pulse.api:app --port 8000; echo "  refused, exit=$?"; \
PULSE_ENVIRONMENT=prod PULSE_DOCS_ENABLED=false PULSE_MODEL_API_KEY='LEAKDEMO-not-a-real-credential-0001' \
  uv run uvicorn pulse.api:app --host 127.0.0.1 --port 8000 > /tmp/demo.log 2>&1 & \
sleep 4; \
echo "  version : $(curl -sS http://127.0.0.1:8000/version)"; \
echo "  docs    : $(curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/docs)"; \
echo "  startup : $(grep -o 'startup config .*' /tmp/demo.log | head -1)"; \
echo "  the key appears $(grep -c 'LEAKDEMO' /tmp/demo.log) times in the log"; \
pkill -f 'pulse.api:app'
```

A service that **refuses** a legal-but-forbidden configuration with a named field and a non-zero exit; then
starts, reports which deploy it is, serves no documentation, and prints its entire configuration into the log
with the credential as `**********`. Yesterday `pulse` could not be told anything. Today it can be told seven
things, it refuses four kinds of wrong, and it can say what it was told without giving away the one thing it
must not.

---

## Setup

- [ ] **nothing from Days 4–8 still running** — `pgrep -af 'uvicorn|blackhole|hangy|hungry|burn|allocate|holder|slow_resolver|terminator'`
- [ ] **ports 8000, 8010–8016 and 8099 confirmed free** before starting, not assumed
- [ ] **`git check-ignore -v .env` exits `0`** and **`git check-ignore -v .env.example` exits `1`** — two
      different exit codes, both from rules written on Day 0, checked **before** either file exists
- [ ] `pydantic-settings` version **looked up live** with `curl`, not copied from the document
- [ ] `uv add pydantic-settings==2.15.0` run, and `python-dotenv` observed arriving **transitively**
- [ ] `pydantic`'s version printed and recorded — **it was already there via FastAPI; today adds no second copy**
- [ ] `./o check` green and `git status --short` clean before breaking anything
- [ ] `./o scaffold 9` has created the day's `lab/`

---

## Section 1 — `01-configuration`

- [ ] **1.1** read · the setting inventory for `pulse` written **before** reading the part's table
- [ ] **1.1** both `grep` audits run against `pulse/` and `git log --all -S 'sk-'` — **while the answer is
      still empty**, so you know what clean looks like
- [ ] **1.1** the litmus test applied out loud: *could this repository be public in the next few seconds?*
- [ ] **1.1** `TODO(me)` — one value in `pulse` that **sounds** like configuration and is actually code, named
      with the reason
- [ ] **1.1** answered out loud: *the two tests for whether a value is configuration*
- [ ] **1.2** read · `printenv | wc -l` run — **the number surprised you, or you can say why it did not**
- [ ] **1.2** the inheritance chain watched: a value passed through bash → `uv` → `python` with nobody
      forwarding it
- [ ] **1.2** the **snapshot** proved: a variable exported while a process runs, and the process never sees it
- [ ] **1.2** `export` versus the inline `VAR=value command` form understood — and the inline form used for
      every experiment afterwards
- [ ] **1.2** answered out loud: *why a config change in production is always a process replacement*
- [ ] **1.3** read · `bool('false')` seen returning `True` **with your own eyes**
- [ ] **1.3** all four states produced: unset · empty · whitespace · a real value, printed with `!r`
- [ ] **1.3** confirmed that `os.environ.get(name, default)` **does not fire for an empty value**
- [ ] **1.3** `float('inf')` accepted as a timeout, and the Day 7 consequence named
- [ ] **1.3** `TODO(me)` — a fifth state found, or the argument that there are only four
- [ ] **1.3** answered out loud: *why `DEBUG=false` turns debugging on*
- [ ] **1.4** read · `lab/ladder.py` written · **the `(from …)` column present, because a resolver without it
      answers the wrong question**
- [ ] **1.4** all four rungs walked, **one change per run**
- [ ] **1.4** the malformed line produced and watched being **silently skipped**
- [ ] **1.4** `PYDANTIC_SETTINGS_DEBUG=1` run and its source report read — including a value that lost
- [ ] **1.4** `TODO(me)` — `read_env_file` made to raise on an unparseable line
- [ ] **1.4** answered out loud: *the precedence order, and the one-sentence principle that generates it*
- [ ] **1.5** read · `lab/awkward.env` written · `cat -A` used to **see the trailing whitespace**
- [ ] **1.5** the naive parser's three defects found in eight lines
- [ ] **1.5** `git check-ignore -v .env` run **against a real `.env` holding an obviously-fake value**, and the
      file deleted in the same block
- [ ] **1.5** `git status --short` confirmed **silent** while that `.env` existed
- [ ] **1.5** answered out loud: *the two legitimate jobs of `.env`, the one it must never have, and why
      `.gitignore` does not protect a file that was committed last week*

---

## Section 2 — `02-typed-settings`

- [ ] **2.1** read · `lab/settings_by_hand.py` written · **frozen, and `FrozenInstanceError` seen**
- [ ] **2.1** `PULSE_DOCS_ENABLED=false` read as `False` — the bug from 1.3, fixed in two lines
- [ ] **2.1** `PULSE_DOCS_ENABLED=flase` **refused**, with a non-zero exit code read
- [ ] **2.1** the six things this version still cannot do listed **from memory** before re-reading the table
- [ ] **2.1** `TODO(me)` — the empty-string hole in `_raw` closed **per field**, and the one field where
      stripping would be wrong named
- [ ] **2.1** answered out loud: *three things one settings object gives you that scattered reads cannot*
- [ ] **2.2** read · `lab/settings_pydantic.py` written · `env_prefix`, `extra`, `frozen` all present
- [ ] **2.2** **three validation errors reported in one run**, each naming the field and the offending value
- [ ] **2.2** `input_type=str` noticed on every error — the 1.3 lesson, printed by the library
- [ ] **2.2** `extra="forbid"` seen catching a typo **in the file** — and confirmed **not** catching one in a
      real environment variable
- [ ] **2.2** `PULSE_ENVIRONMENT=production` refused by the `Literal` — **`production` is not `prod`**
- [ ] **2.2** answered out loud: *which kind of typo `extra="forbid"` catches and which it does not*
- [ ] **2.3** read · `lab/collide.py` written · **`home` populated by the operating system, unasked**
- [ ] **2.3** `HOST=… PORT=…` seen configuring an unprefixed class
- [ ] **2.3** `lab/audit_env.py` written · **`PULSE_PROT` finally caught**, after six parts of walking past it
- [ ] **2.3** the error message confirmed to **list the names you could have meant**
- [ ] **2.3** `TODO(me)` — the prefix read from `model_config`, **and** the non-empty assertion on
      `known_names()` added. *The second one matters more.*
- [ ] **2.3** answered out loud: *what a prefix makes possible that has nothing to do with collisions*
- [ ] **2.4** read · `lab/import_time.py` and `lab/lazy_time.py` written · **the two `[...]` lines appearing at
      different moments**
- [ ] **2.4** `os.environ` changed mid-process and both versions compared
- [ ] **2.4** `cache_clear()` seen rebuilding the object
- [ ] **2.4** `lab/test_import_time.py` run · **`assert 8000 == 7777` seen** — the test that cannot be written
- [ ] **2.4** `TODO(me)` — the `autouse` fixture written, then its *after* half removed, and the test that
      starts failing identified
- [ ] **2.4** answered out loud: *why a test that sets an environment variable can have no effect at all*

---

## Section 3 — `03-fail-fast`

- [ ] **3.1** read · `lab/fail_late.py` written · **`healthz : 200` and `predict : 500` seen together**
- [ ] **3.1** `lab/fail_fast.py` written · **exit `78`, four lines, no traceback**
- [ ] **3.1** the good run done **before** the bad one — a red gate never seen green proves nothing
- [ ] **3.1** the `sys.exit(0)` failure understood: *a perfect message and an inverted mechanism*
- [ ] **3.1** the secret-in-the-refusal hazard noticed — **a defensive practice creating a new leak path**
- [ ] **3.1** answered out loud: *the one situation where refusing to start makes an outage worse, and what
      stops it*
- [ ] **3.2** read · `lab/rungs.py` written · **the `present` column seen accepting six of seven values**
- [ ] **3.2** `lab/consistent.py` written · **three individually-valid values refused together**
- [ ] **3.2** the model validator's `return self` present — and its absence tried once, to see the
      `AttributeError`
- [ ] **3.2** `TODO(me)` — every rule classified **impossibility** or **preference**, with the argument
      written down, and every preference deleted or relocated
- [ ] **3.2** answered out loud: *a value that passes rungs one to three and fails rung four*
- [ ] **3.3** read · `lab/startup_dep.py` written · **exit `69`, the process never existed**
- [ ] **3.3** `lab/ready_dep.py` written · **`healthz : 200` and `readyz : 503` at the same moment**
- [ ] **3.3** the stand-in dependency started and readiness seen **recovering with no restart**
- [ ] **3.3** understood that a connect-only probe proves **a listener exists**, not that anything answers
- [ ] **3.3** the metastable failure explained in your own words: *removing the cause does not fix the system*
- [ ] **3.3** answered out loud: *the one-sentence rule for startup versus readiness*
- [ ] **3.4** read · `lab/announcing.py` and `lab/config_drill.sh` written
- [ ] **3.4** **the six-column table produced, and the four identical columns counted**
- [ ] **3.4** `lab/smoke.sh` written · run **red first**, then green · **three distinct exit codes understood**
- [ ] **3.4** the `${1:?message}` form used, and the reason understood: *a smoke test with a defaulted
      expectation always passes*
- [ ] **3.4** the empty-query-result problem understood: **an alert on a threshold never fires on no data**
- [ ] **3.4** `TODO(me)` — a seventh distinguishing observation found, and classified machine or human
- [ ] **3.4** answered out loud: *why a production dashboard shows "no data" rather than something wrong*

---

## Section 4 — `04-secrets`

- [ ] **4.1** read · `lab/bearer.py` written · **two identical `True`s from two differently-labelled callers**
- [ ] **4.1** `hmac.compare_digest` used rather than `==`, and the timing reason stated
- [ ] **4.1** `lab/classification.md` written — **six rows, five `no`, and a blast-radius column**
- [ ] **4.1** the secret / confidential distinction stated: *a secret is never logged; confidential data is
      logged carefully*
- [ ] **4.1** `TODO(me)` — the `Rotation` column filled in for a provider you actually intend to use.
      **"I do not know" is a finding, and it goes in the table**
- [ ] **4.1** answered out loud: *the two consequences of sharing a credential that have nothing to do with it
      being read*
- [ ] **4.2** read · **the marker value used throughout — nothing real, ever**
- [ ] **4.2** `lab/leaky.py` written · **two log lines containing the key, one of which you did not write**
- [ ] **4.2** the command-line leak produced, and the `ps`/PowerShell limitation on this machine recorded
      rather than glossed over
- [ ] **4.2** `lab/traceback_leak.py` written · **a key in an exception nobody logged**
- [ ] **4.2** `git log --all -S 'LEAKDEMO'` run and **clean**
- [ ] **4.2** the seven paths ranked by **duration**, and the three permanent ones named
- [ ] **4.2** `history | grep -c 'LEAKDEMO'` run — **path 7 checked, not assumed**
- [ ] **4.2** `TODO(me)` — an eighth leak path found and ranked
- [ ] **4.2** answered out loud: *why a key in a URL query string leaks into systems you do not own*
- [ ] **4.3** read · `lab/secrets_type.py` written · **six safe paths, one unsafe, from one run**
- [ ] **4.3** `model_dump()` versus `model_dump(mode='json')` understood — and the `TypeError` that makes the
      plain dump un-serialisable noted as a **safety property**
- [ ] **4.3** `lab/secrets_escape.py` written · **three escapes, all written in careful style**
- [ ] **4.3** `grep -rn 'get_secret_value'` run — **the review command**, and every call site looked at
- [ ] **4.3** `lab/redact_filter.py` written · `record.args = ()` present and the reason understood
- [ ] **4.3** the filter's **miss** seen, and accepted as honest rather than fixed away
- [ ] **4.3** `TODO(me)` — the fourth line caught, **and** a new false positive found. Both halves
- [ ] **4.3** answered out loud: *why `SecretStr('')` displaying as empty is a feature*
- [ ] **4.4** read · `lab/provider.py` and `lab/caller.py` written
- [ ] **4.4** `lab/rotate_drill.sh` run · **failures counted in both scenarios** — the numbers, not the idea
- [ ] **4.4** the five-step procedure performed in order, including **step 3, confirming no use of the old key**
- [ ] **4.4** understood why a service with nine replicas **cannot** rotate without an overlap even with a
      perfect operator
- [ ] **4.4** the connection-pool caveat noted: **the overlap must outlast the longest cached connection**
- [ ] **4.4** answered out loud: *what a rotation produces besides safety*
- [ ] **4.5** read · `lab/spawner.py` written · **a child process holding a credential nobody passed it**
- [ ] **4.5** `env=` passed explicitly to the second child, and `SYSTEMROOT` understood as a real requirement
- [ ] **4.5** `lab/run_secrets/` created with `printf` (**not `echo`**) and `chmod 600`
- [ ] **4.5** `lab/from_file.py` written · **the credential present in the process and absent from its
      environment**
- [ ] **4.5** `TODO(me)` — **Day 5's outstanding question answered**: is `chmod 600` honoured on this
      filesystem? Written into `docs/PACKAGES.md`
- [ ] **4.5** the ladder recited: source → command line → environment → file → store → workload identity, and
      **which rung Day 9 lands on**
- [ ] **4.5** answered out loud: *the one leak path an environment variable genuinely closes, and three it
      does not*

---

## Section 5 — `05-pulse-configured`

- [ ] **5.1** read · `pulse/config.py` **written by you, line by line, not pasted**
- [ ] **5.1** all seven fields present, **each with its bound in the same line as its default**
- [ ] **5.1** `pulse/api.py` edited: composition root, startup line, `Depends(get_settings)`, `environment` on
      `/version`
- [ ] **5.1** `redoc_url` handled as well as `docs_url` — **both, or the setting is half-done**
- [ ] **5.1** all three cases run: **invalid**, **valid-but-refused**, **correct** — and the `404` on `/docs`
      in prod confirmed as a *pass*
- [ ] **5.1** the bare `:` in the model-validator refusal noticed **before** reading that it was deliberate
- [ ] **5.1** `TODO(me)` — the three defects in `_configure()` fixed (exit code · garbled expression ·
      validator location)
- [ ] **5.1** `TODO(me)` — the `error.get("input")` trade **decided in writing**, then implemented
- [ ] **5.1** `TODO(me)` — `create_app(settings)` factory written, and the `docs_enabled` test that it enables
- [ ] **5.1** answered out loud: *why `get_settings()` at module scope in `api.py` does not contradict 2.4*
- [ ] **5.2** read · field `description`s added · `scripts/gen_env_example.py` written
- [ ] **5.2** `--write` run and `.env.example` **read end to end**
- [ ] **5.2** `newline="\n"` present, and the line-endings failure understood **before** meeting it
- [ ] **5.2** the gate seen **green → red → green**, with the red produced by adding a field and not
      regenerating
- [ ] **5.2** `cp .env.example .env` performed and `git status --short` confirmed **silent**, then `.env`
      removed
- [ ] **5.2** `TODO(me)` — boolean rendering fixed (`True` → `true`) and `Optional[SecretStr]` handled
- [ ] **5.2** answered out loud: *why a hand-maintained example file is more dangerous than none*
- [ ] **5.3** read · `lab/leaky_config.py` and `lab/leak_drill.py` written
- [ ] **5.3** **the occurrence count predicted before running it**, then measured
- [ ] **5.3** the six-row table produced, and **the two rows that are identical** identified
- [ ] **5.3** `lab/leak_gate.sh` written · run **green**, then **red** by changing one annotation, then
      **green again**
- [ ] **5.3** `cp pulse/config.py /tmp/config.py.bak` taken **before** the edit
- [ ] **5.3** `openapi.json` included in the gate, and the reason understood
- [ ] **5.3** the response written out **in order** — rotate, update, confirm, revoke, fix, record — and
      **why deleting the log is not on the list** stated in one sentence
- [ ] **5.3** the vacuous-gate failure understood: **a gate run with no credential set is green forever**
- [ ] **5.3** `TODO(me)` — the shell gate converted to a **pytest** using `caplog`, and added to `./o check`
- [ ] **5.3** answered out loud: *why this failure is caused by following good advice rather than ignoring it*

---

## The three gates

- [ ] **gate one** — `smoke.sh` seen **exit 1** against the `dev` deploy and **exit 0** against `prod`
- [ ] **gate two** — `leak_gate.sh` seen **green → red → green**, the red produced by one annotation
- [ ] **gate three** — `gen_env_example.py --check` seen **green → red → green**
- [ ] **all three seen red on purpose**, and all three seen green afterwards. *A drill that only goes red has
      proved the failure, not the fix.*

---

## The pattern across five days

- [ ] `TODO(me)` — **one paragraph written** on what Day 5's disk, Day 6's OOM kill, Day 7's exhausted
      connections, Day 8's expired certificate and today's published credential have in common — **and what
      makes today's different**
- [ ] the difference named: **the first four were invisible to everyone; this one is visible to everyone
      except you**
- [ ] the consequence named: **the other four could be fixed by fixing the cause; this one cannot** — the
      exposure has already happened, and only rotation responds to it

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes confirmed, not assumed
- [ ] **2 packages added** — `git diff pyproject.toml uv.lock` shows exactly `pydantic-settings` and
      `python-dotenv`, and **nothing else**
- [ ] **no real credential was used anywhere today** — every value contains `not-a-real-credential`, checked
      rather than remembered
- [ ] **`netstat -ano | grep -E ':(8000|801[0-6]|8099).*LISTENING'` returns nothing** — no server survives
- [ ] `pkill -f` verified with `netstat` rather than trusted
- [ ] `/tmp/leaky.log`, `/tmp/drill.log`, `/tmp/provider.log`, `/tmp/leak_drill.log`,
      `/tmp/pulse_leak_gate.log`, `/tmp/config.py.bak`, `/tmp/version.json`, `/tmp/openapi.json` removed
- [ ] **`days/day-009-configuration-and-secrets/lab/run_secrets/` DELETED** — the secrets directory does not
      survive the day
- [ ] **`.env` does not exist at the repository root** — and `.env.example` does, and is staged
- [ ] `git status --short` clean, and **`git log --all -S 'LEAKDEMO' --oneline` returns nothing**
- [ ] **`git diff pulse/` shows only today's intended changes** — `config.py` added, `api.py` edited, and
      **`model_api_key` is a `SecretStr`**
- [ ] `./o check` green

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — **three rows appended** (`pydantic-settings` · `python-dotenv` transitive · the
      `chmod 600` measurement from 4.5)
- [ ] `docs/INCIDENTS.md` — **three rows appended, first symptom written before the cause** (rows 14, 15, 16)
- [ ] **row 16 states the response in order** and says **why deleting the log is not on the list**
- [ ] **row 16 explicitly linked to Day 8's row 13, Day 7's row 22, Day 6's row 19 and Day 5's row 16**, with
      the difference named
- [ ] `docs/DECISIONS.md` + `docs/adr/ADR-0006-*.md` — **the fail-fast ADR**, whose *"what would make us change
      our minds"* section contains a number or an observable condition
- [ ] `docs/ARCHITECTURE.md` updated — `pulse` now has a configuration surface, and it is part of the shape
- [ ] `docs/PROGRESS.md` — the Day 9 row pasted from the hub's §11
- [ ] `./o depth 9` green
- [ ] `./o trace` shows **FND-11, FND-12 and SEC-01** closed and nothing else newly closed
- [ ] committed: `day 009: configuration and secrets — the settings object, the refusal, and the credential in the log — closes FND-11, FND-12, SEC-01`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
