# ⚙️ Project Kriya

**Production operations for AI systems — MLOps, LLMOps, AIOps, AgenticOps and MCPOps — built one
day at a time on one service you actually operate.**

> **Kriya** (Sanskrit क्रिया) means *the action, the operation, the thing that is actually done* — as
> opposed to the thing that is merely known. Knowing what a Kubernetes probe is takes ten minutes.
> Being the person who is paged when one is wrong is a different profession, and it is the one this
> repository trains.

| | |
|---|---|
| **Plan** | [`docs/00_MASTER_PLAN.md`](docs/00_MASTER_PLAN.md) — v1.0.0, the single source of truth |
| **Days** | 237 (Day 0 – Day 236) |
| **Phases** | 24, each ending in a gate you demonstrate rather than assert |
| **Concept IDs** | 279 across 10 threads |
| **Cost** | **$0.** No card on file, ever, for anything ([Addendum 01](docs/01_ADDENDUM_ZERO_COST_STACK.md)) |
| **Hardware** | One laptop, no GPU ([Addendum 02](docs/02_ADDENDUM_THE_MACHINE.md)) |
| **Progress** | [`docs/TRACKER.md`](docs/TRACKER.md) · [`docs/PROGRESS.md`](docs/PROGRESS.md) |

---

## What this is

A curriculum that turns someone with no operations background into someone who can be trusted with a
production AI system — and can prove it, from a public repository, without ever having spent money.

It is built around **one service, `pulse`**: a deliberately boring AI service (a ticket classifier
and an LLM-backed assistant) with a deliberately complete production surface. Everything is learned
by changing `pulse` or the platform around it. Nothing is learned in a vacuum.

**Five threads, taught in dependency order, because they depend on each other:**

| Thread | The question | Days |
|---|---|---|
| **MLOps** | How does a model get into production and stay correct there? | 85–122 |
| **LLMOps** | What changes when the model is huge, non-deterministic, rented and charged per token? | 123–158 |
| **AIOps** | How do you use ML on your *own telemetry* to survive production's volume of signals? | 159–178 |
| **AgenticOps** | How do you operate a system that decides its own next step — and still sleep? | 179–198 |
| **MCPOps** | How do you run, secure and govern the tool boundary those agents reach through? | 199–214 |

**And the part nobody advertises:** Days 1–84 are Linux, delivery, containers, Kubernetes,
infrastructure as code, observability and SRE practice — 84 days before the first model is trained.
That ordering is the most important decision in the plan, and it has its own decision record:
[ADR-0004](docs/adr/ADR-0004-fundamentals-before-ai.md). Every genuinely hard MLOps problem is an
ordinary distributed-systems problem in a costume, and you cannot see the costume until you know the
shape underneath.

---

## How a day works

A day is **not** one long page. It is a hub plus one document per subtopic:

```
days/day-115-data-drift/
├── LESSON.md      # the hub — story, part map, setup, build brief, the check, the budget
├── CHECKLIST.md   # the definition of done. ./o done 115 refuses until it is ticked.
├── parts/
│   ├── 01-what-drift-is/
│   │   ├── 1.1-….md      ← one idea, from zero prior knowledge through to production
│   │   └── 1.2-….md
│   └── 02-detecting-it/
│       └── 2.1-….md
└── lab/           # your own scratch code
```

Every part carries ten sections in a fixed order — **one-line answer · the story · the idea in plain
language · why Kriya needs it · the mechanism · line by line · when it breaks · in production ·
check yourself** — and `./o depth 115` refuses the day if any is missing.

Three rules that make it different from a tutorial:

- **You type every line.** Nothing under `pulse/`, `deploy/` or `pipelines/` is pre-written.
- **Every day has a check that must go red first.** Break it, read the real error, then fix it.
- **There are no clocks.** No "estimated hours" anywhere. A day is a unit of subject, not of time,
  and nothing is ever trimmed to fit a schedule.

Full contract: [`days/README.md`](days/README.md) and §17 of the plan.

---

## Getting started

```bash
# 1. this repository is not a git repository yet — that is Day 0's first lesson
git init

# 2. the environment (Day 0 explains every line of this)
uv sync

# 3. your keys — names only in .env.example, values only in .env, which git never sees
cp .env.example .env      # then fill in what Day 9 tells you to, and nothing before

# 4. where am I
./o status
./o next
```

Then write the first day:

```
/day-kriya 0
```

That is a Claude Code skill ([`.claude/skills/day-kriya/`](.claude/skills/day-kriya/SKILL.md)). It
reads the plan, the ledgers and the current state of the repository, verifies every version and
every API symbol live, and produces the hub, the parts, the lab scaffold and the checklist — then
runs `./o depth 0` on its own output.

---

## The driver

`make` is not used. `./o` is the driver.

```bash
./o status         # how many days written / complete
./o next           # the next unwritten day, and the command that writes it
./o start 42       # open day 42's hub and list its parts
./o parts 42       # just the sub-topic list
./o scaffold 42    # create day 42's lab/
./o depth [42]     # check against the depth contract (plan §17)
./o trace          # regenerate TRACEABILITY.md + CURRICULUM_INDEX.md
./o tracker        # regenerate TRACKER.md
./o runbooks       # list every runbook in the repository
./o check          # ruff + offline pytest + depth contract + traceability
./o done 42        # refuses unless the checklist is ticked and checks are green, then commits
```

---

## The skills

| Skill | What it does |
|---|---|
| `/day-kriya N` | Write day N — hub, parts, lab scaffold, checklist — to the depth contract |
| `/review-day N` | Read a written day against the quality half of the contract, which no script can check |
| `/incident-drill` | Stage a realistic failure against the current `pulse` and run the response, without telling you the cause |

---

## The ledgers

Three are generated and five are written by hand. Do not confuse them — editing a generated one just
means the next `./o check` silently overwrites you.

| File | Nature | What it is |
|---|---|---|
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | hand | One row per completed day. **The last row is where you are.** |
| [`docs/PACKAGES.md`](docs/PACKAGES.md) | hand | Every tool, the version actually observed, and the date |
| [`docs/INCIDENTS.md`](docs/INCIDENTS.md) | hand | Every failure, and **what you saw first** — the most valuable file here |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | hand | The index of architecture decision records |
| [`docs/CHANGELOG_PLAN.md`](docs/CHANGELOG_PLAN.md) | hand | Every amendment to the plan |
| [`docs/TRACKER.md`](docs/TRACKER.md) | generated | What is written, at what depth |
| [`docs/TRACEABILITY.md`](docs/TRACEABILITY.md) | generated | Every ID, and whether it is closed |
| [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md) | generated | ID → day, so you can find where something is taught |

---

## Layout

```
pulse/          # THE SERVICE — api, model wrapper, assistant. You write every line, from the docs.
platform_ops/   # THE PLATFORM CODE — aiops/ detectors · agents/ and their brakes · mcp/ servers
pipelines/      # data + training pipelines, and the CI workflows that run them
deploy/         # Dockerfiles, compose, k8s manifests, helm, kustomize, terraform
observability/  # prometheus rules, grafana dashboards, otel collector config
evals/          # model evalsets, LLM evalsets, agent trajectories
runbooks/       # one per alert — the 3am documents
scripts/        # repo tooling: depth_check.py · tracker.py · trace.py
tests/          # pytest
days/           # the teaching
docs/           # the plan, the addenda, the ledgers, the ADRs
```

Everything except `scripts/`, `days/` and `docs/` starts empty on purpose. That is the point.
