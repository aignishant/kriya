---
plan: kriya
version: "v1.2.0"
curricula: 10
ids: 279
days: 237
phases: 24
doc_architecture: "hub + parts/ (see §17)"
created: "2026-08-24"
amended: "2026-08-25"
---

# ⚙️ MASTER PLAN v1.2.0 — Project **Kriya**
## Production operations for AI systems: **MLOps · LLMOps · AIOps · AgenticOps · MCPOps**

> **Kriya** (Sanskrit क्रिया) means *the action, the operation, the thing that is actually done* —
> as opposed to the thing that is merely known. That is the whole distinction this plan is built on.
> Knowing what a Kubernetes probe is takes ten minutes. Being the person who is paged when one is
> wrong is a different profession, and it is the one this plan trains.
>
> 📌 **Purpose:** the single source of truth. Every later document points back here.
>
> **Read §17 before writing a single day.** It is the depth contract — the standard a day document
> has to meet before it counts as written. `./o depth N` enforces the mechanical half of it.

---

## 📑 Table of Contents

| §  | Section |
| --- | --- |
| 1  | 🎬 The Vision — five kinds of ops, one system |
| 2  | 🧭 Core Principles — rules we never break |
| 3  | 🏗️ The Product — what `pulse` actually is |
| 4  | 💸 Cost Policy — the $0 constraint, and why it is the curriculum |
| 5  | ⚙️ The Stack Baseline — versions, the machine, verification |
| 6  | 🧶 The Ten Curricula & the ID scheme |
| 7  | 🧵 The threads, one by one |
| 8  | 💻 The machine you will actually use |
| 9  | 🧰 The zero-cost stack, tool by tool |
| 10 | 🚫 What you are deliberately not learning |
| 11 | 🔗 How this plan relates to the sibling curricula |
| 12 | 📖 The reader's contract — how to study this |
| 13 | 🗺️ The 24 Phases |
| 14 | 🗓️ The 237-Day Map (day → IDs closed) |
| 15 | 🚦 Phase Gates & the Freshness Check |
| 16 | 📒 Ledgers & Traceability |
| **17** | **📐 The Depth Contract — how a day is written** |
| 18 | ✍️ The Style Guide |

---

## 1 · 🎬 The Vision — five kinds of ops, one system

By Day 236 you will have **built, deployed, instrumented, secured, budgeted and broken** a real AI
system — `pulse` — and you will be able to defend every operational decision in it to somebody who
is paid to find the hole. The goal is a demonstrably **hireable production engineer for AI systems**,
with a public repository as the proof and a set of scars you acquired on purpose.

Five disciplines share this plan, and they are not five separate courses:

| Discipline | The question it answers |
| --- | --- |
| **MLOps** | How does a *model* get from a notebook into production and stay correct there? |
| **LLMOps** | What changes when the model is enormous, non-deterministic, rented, and charged per token? |
| **AIOps** | How do you use ML *on your own telemetry* to survive the volume of signals production produces? |
| **AgenticOps** | How do you operate a system that decides its own next step — and how do you sleep? |
| **MCPOps** | How do you run, secure and govern the tool boundary those agents reach through? |

They are taught in that order because each one **assumes the last**. AIOps is ML applied to
operations, so you cannot do it before you can do either. AgenticOps is LLMOps plus autonomy plus
blast radius. MCPOps is the boundary AgenticOps depends on. Learning them out of order produces
someone who can name all five and operate none.

Underneath all five sits the part nobody advertises and everybody needs: **you cannot do ops for AI
until you can do ops.** Phases 1–8 are Linux, delivery, containers, Kubernetes, infrastructure as
code, observability and SRE practice — 84 days before the first model is trained. That is not a
detour. Every genuinely hard MLOps problem you will meet is an ordinary distributed-systems problem
wearing a machine-learning hat, and the people who struggle with MLOps are almost always the people
who skipped this part.

Three commitments shape everything:

1. **One system, not eighty demos.** Every concept lands as a change to `pulse`. Nothing is learned
   in a vacuum; if removing an idea would not break `pulse`, it does not get a day.
2. **The repo is the memory, not the chat.** Ledgers, decision records and day documents mean that
   you — or a stranger, or a different assistant six months from now — can open this folder and know
   exactly where things stand and why every choice was made.
3. **You break it on purpose, before it breaks you.** Every phase contains at least one day whose
   entire subject is a deliberate failure. The error message you have seen once at 11am on a
   Saturday, on purpose, is not the same error message at 3am during an incident.

### 1.1 What "production" means in this plan

The word gets used loosely. Here it means a system that has all nine of these, and can prove it:

| | Property | Proved by |
| --- | --- | --- |
| 1 | It is **deployable** by anyone, from a commit, without you | Phase 2, Phase 6 |
| 2 | It is **observable** — you can answer questions you did not anticipate | Phase 7 |
| 3 | It has a **stated reliability target** and an error budget | Phase 8 |
| 4 | It is **reversible** — every change can be undone in one command | Phase 2, Phase 11 |
| 5 | It is **reproducible** — any artifact can be rebuilt from a commit | Phase 9, Phase 10 |
| 6 | It is **bounded** — nothing it does is unlimited, in cost, steps or blast radius | Phase 17, Phase 22 |
| 7 | It is **least-privileged** — every actor can do only what it must | Phase 5, Phase 20, Phase 21 |
| 8 | It is **auditable** — you can prove what ran, on what, when, under which version | Phase 21 |
| 9 | It is **documented for a stranger at 3am** | Phase 8, Phase 23 |

If a change to `pulse` breaks one of those nine, it is not finished, whatever the tests say.

### 1.2 Stated non-goals (decisions, not blind spots)

| Excluded | Why |
| --- | --- |
| Training large models from scratch | A different profession with a different budget. You operate models; you do not pre-train them. |
| Deep learning theory and model architecture | That is `setu`'s subject (§11). This plan assumes the model exists and asks what happens next. |
| Managed-cloud certification paths (a specific vendor's console) | Vendors change; the concepts do not. Every cloud service is taught as a *pattern* you run locally, plus a 🅿️ note on where the vendor button is. |
| Paid infrastructure, GPUs on rent, billable clusters | The $0 constraint (§4) is absolute and is itself a large part of the curriculum. |
| Data engineering at petabyte scale | Distributed data processing is its own discipline. You learn the pipeline *contract* and its failure modes, not Spark tuning. |
| Being an SRE for a company you do not work at | You are learning the practice, not roleplaying an org chart. |

---

## 2 · 🧭 Core Principles — rules we never break

1. **Doc-first.** The day document is written before any code; the code follows the doc.
2. **One day, one document, one commit.** Traceable, append-only history.
3. **Simple language + a concrete example, always.** If a concept cannot be explained simply with
   an example, it is not understood yet (§18 enforces this).
4. **Build first, adopt after.** Hand-roll the mechanism once — the health check, the metric, the
   retry, the drift detector — *then* adopt the tool that does it, so the tool is a convenience and
   never a mystery. You cannot debug on Day 160 what you never typed on Day 64.
5. **Every concept is load-bearing.** If removing it would not break `pulse`, it does not get a day.
6. **Verify the whole project after every step.** Each day ends with the full check suite green, not
   just today's snippet.
7. **Never invent a version number.** Look it up live, or leave a `TODO` with the exact lookup
   command. Record every pin in `docs/PACKAGES.md` with the date.
8. **Never invent an API, a flag or a field.** Every `kubectl` field, Prometheus function, Terraform
   argument and library symbol is verified against its official documentation **on the day it is
   used**, and the day document names the page checked.
9. **Secrets never touch git.** `.gitignore` before `.env` exists; the repository goes public in
   Phase 23, so the discipline is real from Day 0.
10. **Fail honestly and loudly.** Errors surface, escalate and are logged. Nothing — no service, no
    agent, and not you — ever fabricates a result to cover an error. A swallowed exception is a
    future incident with the evidence deleted.
11. **Every gate must be able to go red.** A check that has never failed is not a check; it is
    decoration. Every day ships at least one check you make fail on purpose before you make it pass.
12. **Everything is a trace.** If it is not observable, it did not happen. You cannot operate what
    you cannot see, and you cannot see it retroactively.
13. **Blast radius before capability.** Every new power — code execution, a write tool, an
    autoscaler, an auto-remediator, an agent that can act — arrives in the same day as its
    containment story. Never in a later one.
14. **If reality changes, the plan is amended first.** A new Kubernetes version, a changed free
    tier, a renamed API → amend via addendum + `docs/CHANGELOG_PLAN.md`, *then* continue. Days are
    never silently patched.
15. **Zero budget is a feature.** Quotas, local clusters, free tiers and resource limits are the
    curriculum, not obstacles to it (§4). Operating under a hard constraint is the job.
16. **Depth over density.** A day is taught as a **hub plus one document per subtopic** (§17), never
    as one long page. If a subtopic cannot be read on its own, understood without scrolling past a
    different subtopic, and explained back out loud, it has not been split finely enough. A wall of
    text is not depth — it is depth's disguise.
17. **A day is a unit of subject, not a unit of time.** No document carries a time estimate, an
    "estimated hours" field, a "should take ~2 hours", or a suggested pace. A topic is finished when
    it is understood — one sitting or five. **Nothing is ever trimmed to fit a clock**; if a day is
    getting long, it gets another part, not a shorter explanation.
18. **Assume no prior knowledge, finish at production.** Every subtopic opens where a reader who has
    never met the idea can stand, defines its jargon on first use — *including jargon from earlier
    days, with a link back* — and does not stop at the toy example. It ends with how the idea is used
    in a real system: what a senior engineer writes instead of the teaching version, what breaks at
    scale or under concurrency, the review comment, the interview question, and **what you would be
    paged for**. Strong basics and advanced technique are the same document, in that order.

> Principles 16–18 are made concrete by **§17, the depth contract**. They are enforced mechanically
> by `scripts/depth_check.py` (`./o depth N`) and, for the half a script cannot judge, by reading.

---

## 3 · 🏗️ The Product — what `pulse` actually is

**`pulse` is a small AI service with a large production surface.** It is deliberately trivial as a
piece of machine learning and deliberately complete as a piece of operated software, because the
operating is the subject.

What it does when finished:

- **A model that predicts.** A tabular classifier over synthetic support tickets — priority and
  likely queue. Ordinary, fast, and completely unglamorous, so that nothing about the ops is hidden
  behind interesting modelling.
- **An assistant that generates.** An LLM-backed endpoint that summarises a ticket and drafts a
  reply, grounded in a retrieval index over past tickets.
- **A platform that runs it.** Containers, a local Kubernetes cluster, infrastructure as code,
  GitOps reconciliation, CI that can go red, and a rollback that has been rehearsed.
- **Telemetry that explains it.** Metrics, structured logs and distributed traces through one
  collector, with published SLOs and an error budget policy.
- **An AIOps layer that reads its own telemetry.** Anomaly detection on live metrics, log
  clustering, alert correlation, change attribution, and one automated remediation with brakes.
- **An agent that operates it.** A runbook agent that diagnoses incidents read-only, proposes
  actions, and can only act through an approval gate that leaves an audit trail.
- **An MCP boundary.** Every data source those agents touch — metrics, logs, the ticket archive, the
  deploy history — is an MCP server that is deployed, versioned, authenticated, rate-limited and
  traced like any other service.
- **A cost model.** Every prediction, generation and agent task has a unit cost, an owner, a budget
  and an alert that fires before the budget is gone.

> ⚠️ **The data is synthetic, always.** Never feed real personal data, real employer data or real
> customer tickets through a free endpoint or a local experiment. `pulse`'s ticket archive is
> generated. This is Principle 9's cousin, and Day 156 makes it a mechanism rather than a promise.

**Repo layout (established Day 0, grown daily):**

```
ops/
├── o                       # the driver script — ./o check | depth | start | next | done  (Day 0)
├── Makefile                # a two-line shim so `make check` still reaches ./o check
├── CLAUDE.md               # standing instructions for the driver agent (Day 0)
├── README.md               # what this is, and how a stranger runs it
├── .env                    # names and values (never committed)   ·  .env.example (always)
├── pyproject.toml          # uv-managed; every pin dated in docs/PACKAGES.md
├── uv.lock                 # the exact transitive tree; committed
│
├── days/                   # 📚 THE TEACHING — one folder per day
│   ├── README.md           #    how to read a day
│   └── day-NNN-<slug>/     #    the number is the identity, the slug says what it teaches
│       ├── LESSON.md       #    the hub: story, part map, setup, build brief, check, budget
│       ├── CHECKLIST.md    #    the definition of done; ./o done NNN refuses until ticked
│       ├── parts/          #    one document per subtopic — the actual teaching
│       │   ├── 01-<slug>/1.1-<slug>.md …
│       │   └── 02-<slug>/2.1-<slug>.md …
│       └── lab/            #    the learner's own scratch code for that day
│
├── pulse/                  # THE SERVICE — api, model wrapper, assistant. You write every line.
├── platform_ops/           # THE PLATFORM CODE — aiops detectors, agents, mcp servers
│   ├── aiops/              #    detectors, log parsing, correlation, forecasting
│   ├── agents/             #    the runbook agent, the incident co-pilot, their brakes
│   └── mcp/                #    Kriya's own MCP servers and the policy in front of them
├── pipelines/              # data + training pipelines, and the CI workflows that run them
├── deploy/                 # Dockerfiles, compose, k8s manifests, helm, kustomize, terraform
├── observability/          # prometheus rules, grafana dashboards, otel collector config
├── evals/                  # model evalsets, LLM evalsets, agent trajectories
├── runbooks/               # one per alert — the 3am documents (from Day 79)
├── scripts/                # repo tooling: depth_check.py · tracker.py · trace.py
├── tests/                  # unit + integration + eval harness
└── docs/
    ├── 00_MASTER_PLAN.md          # this file
    ├── 01_ADDENDUM_ZERO_COST_STACK.md
    ├── 02_ADDENDUM_THE_MACHINE.md
    ├── CURRICULUM_INDEX.md        # generated: ID ↔ day cross-table
    ├── TRACKER.md · TRACEABILITY.md          # generated
    ├── PROGRESS.md · PACKAGES.md · INCIDENTS.md · DECISIONS.md · CHANGELOG_PLAN.md
    └── adr/                       # architecture decision records
```

> ⚠️ **Nothing under `pulse/`, `platform_ops/`, `pipelines/`, `deploy/` or `tests/` is pre-written.**
> Every line is printed in a day document and typed by you (`days/README.md`, rule 1). Reading a
> Dockerfile teaches you nothing you will remember at 3am; writing one and watching it fail does.

---

## 4 · 💸 Cost Policy — the $0 constraint, and why it is the curriculum

Governed in full by **`docs/01_ADDENDUM_ZERO_COST_STACK.md`**, which **wins over this plan** on any
question of tooling or paid services. The short version:

- **No card on file. Ever. For anything.** Not "a free trial with a card". Not "the free tier of a
  paid account". If signing up requires a payment method, the plan does not use it, and
  `./o depth` fails a day that tells you to run a billable command without marking it 🅿️ parked.
- **The cluster is local.** `kind` or `k3d` on your own machine. Cloud Kubernetes is taught as
  concepts plus a 🅿️ walkthrough you read and never run.
- **The models are free-tier or local.** Gemini Flash-class via an AI Studio key, Groq, OpenRouter
  models ending in `:free`, or Ollama on your own machine. **Never assume a paid model.**
- **The observability stack is the real one.** Prometheus, Grafana, Loki and the OpenTelemetry
  Collector are the actual production tools, are open source, and run in a compose file. There is
  no toy version of this and no reason to want one.
- **Quota is the currency.** Budgets in this plan are denominated in **requests per minute, requests
  per day, RAM and disk** — not dollars. A day's §6 states its budget in those units, and `0` is a
  legitimate and common answer.

**Why this is not a compromise.** Every constraint above is a constraint real teams have. A team
with a $2M cloud bill has quota limits, memory limits, and a finance director asking what a
prediction costs. Learning to operate inside hard limits — routing around a 429, running the whole
stack in 8GB, deciding what telemetry is worth keeping — *is* the skill. An engineer who has only
ever operated with an unlimited budget has not learned the interesting half of the job.

---

## 5 · ⚙️ The Stack Baseline — versions, the machine, verification

**No version number appears in this plan.** That is deliberate, and it is Principle 7. Kubernetes
ships three minor versions a year; Prometheus, MLflow, OpenTelemetry and every model provider's
free tier move faster than a document can. A version written here would be a lie within a quarter,
and a plausible-looking lie is worse than a `TODO`.

Instead:

| Rule | What it means in practice |
| --- | --- |
| **Look it up on the day** | The day that first installs a tool looks up its current version live, with the exact command in the doc, and records what it saw. |
| **Pin exactly** | `uv add pkg==X.Y.Z`, `image: repo/name@sha256:…`, `terraform required_version`. No ranges, no `latest`. |
| **Record it** | A dated row in `docs/PACKAGES.md`: package, version, date observed, day, why. |
| **Re-check at every gate** | The freshness check (§15) re-reads the moving parts each phase. A broken upstream is an amendment (Principle 14), not a silent patch. |

### 5.1 The four traps this plan exists to inoculate against

Named here so that a day touching one can say *which* one it is avoiding, in words.

| # | Trap | Why it eats an evening |
| --- | --- | --- |
| **1** | **The tutorial that runs as root, on `:latest`, with no limits** | It works immediately and teaches nothing that survives contact with a cluster that has other tenants, a registry that has moved, or a node under pressure. Day 27, Day 28 and Day 42 undo it. |
| **2** | **The metric that is not a metric** | A gauge where you needed a counter, an average where you needed a quantile, a label with unbounded values. It looks like observability for months and then answers no question during an actual outage. Days 62–65. |
| **3** | **The model that is fine offline** | Every ML failure mode that matters — skew, drift, leakage, stale features, delayed labels — is invisible to the offline metric that said 0.94. Days 90, 114–120. |
| **4** | **The autonomy with no brake** | An autoscaler, an auto-remediator or an agent, given a capability without a bound, a budget, a timeout or a kill switch. It behaves for weeks and then does the wrong thing very fast. Days 44, 175, 188, 194. |

Every one of the four is a real and common way that a working system quietly stops being one.

---

## 6 · 🧶 The Ten Curricula & the ID scheme

Every concept in this plan has an ID. A day **closes** an ID when the concept is built into (or
demonstrably exercised against) `pulse` and the day's gates are green. `docs/TRACEABILITY.md` is
regenerated from the day hubs by `scripts/trace.py`; **an open ID from a completed phase is a bug.**

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| A — Foundations & the production mental model | `FND` | 24 | What ops is, the machine, the network, config, environments, delivery metrics, readiness, handover |
| B — Platform | `PLT` | 42 | CI, artifacts, releases, containers, Kubernetes, infrastructure as code, GitOps |
| C — Observability & SRE | `OBS` | 27 | Metrics, logs, traces, dashboards, SLOs, alerting, on-call, incidents, postmortems, capacity |
| D — MLOps | `MLO` | 41 | Data versioning, contracts, pipelines, training, registry, serving, monitoring, drift, retraining |
| E — LLMOps | `LLM` | 34 | Inference stack, quotas, caching, prompts, retrieval, context, evaluation, hallucination |
| F — AIOps | `AIO` | 23 | Telemetry as data, anomaly detection, log clustering, correlation, RCA, auto-remediation |
| G — AgenticOps | `AGO` | 23 | Agents as workloads, traces, agent evals, versioning, containment, agents that operate |
| H — MCPOps | `MCO` | 16 | The tool boundary as infrastructure: deployment, auth, versioning, registries, governance |
| I — Security, governance & compliance | `SEC` | 33 | Secrets, RBAC, network policy, supply chain, injection, PII, audit, model governance |
| J — Cost, capacity & FinOps | `FIN` | 16 | Unit economics, attribution, token budgets, capacity, guardrails against runaway spend |

**Total: 279 concept IDs across 237 days.**

> 🅿️ Some IDs are **parked** — awareness-level: you learn the map and the vocabulary, you do not
> build the thing. Parked IDs are marked 🅿️ in the day documents and still close normally. A parked
> ID still gets a full part with a story, a mechanism and a production section; what it does not get
> is a build step. Managed cloud services are the main source of them (§4).

The per-ID topics live in the day map (§14) — **each day's row is the authoritative statement of
what its IDs mean.** §7 gives the narrative arc of each thread.

---

## 7 · 🧵 The threads, one by one

### 7.1 `FND` — Foundations & the production mental model (24)

What operations actually is and why the repository is the memory (FND-01..02); the shape of a
production system and the blast-radius map (FND-03); `pulse` itself (FND-04); Linux as an operator
sees it — processes, signals, exit codes, filesystems, permissions, disks, logs, CPU, memory and the
OOM killer (FND-05..07); networking, DNS, TCP, timeouts, HTTP and TLS (FND-08..10); configuration,
secrets and the twelve-factor service (FND-11..12); environments and promotion (FND-13); version
control for operators (FND-14..15); the four delivery metrics (FND-16); and the closing arc —
production readiness review, documentation that survives you, handover, day-2 operations, and the
three-day capstone (FND-17..24).

### 7.2 `PLT` — Platform (42)

Continuous integration and the gate that refuses (PLT-01..03); artifacts, reproducibility, releases,
deployment strategies and rollback (PLT-04..07); containers from "why" through images, layers,
Dockerfiles, multi-stage builds, compose, healthchecks, registries and digests, ending in the
container failure lab (PLT-08..16); Kubernetes as objects — the orchestrator's job, a local cluster,
pods, deployments, services, DNS, config, ingress, namespaces, and the first real deploy
(PLT-17..26); Kubernetes done well — probes, requests and limits, rollouts, autoscaling, disruption
budgets, jobs, storage and resource pressure (PLT-27..34); and infrastructure as code and GitOps —
Terraform, Helm, Kustomize, Argo CD, promotion, and drift (PLT-35..42).

### 7.3 `OBS` — Observability & SRE (27)

Delivery measurement (OBS-01); observability versus monitoring (OBS-02); metrics from the data model
through PromQL, RED/USE instrumentation, cardinality and dashboards (OBS-03..08); logs — structure,
correlation ids, shipping, retention and cost (OBS-09..10); traces — spans, propagation, sampling
and one collector (OBS-11..13); the observability failure lab (OBS-14); and SRE practice — SLIs,
SLOs, error budgets, indicators for an ML service, error budget policy, symptom-based alerting,
alert quality, on-call, runbooks, incident command, a real staged incident, blameless postmortems,
game days, and capacity (OBS-15..27).

### 7.4 `MLO` — MLOps (41)

What MLOps is and the failure modes ML adds (MLO-01..02); data — versioning, contracts, quality,
splits and leakage, features, feature stores, pipelines, scheduling, and the data failure lab
(MLO-03..13); training — reproducibility, experiment tracking, the registry, model cards, offline
evaluation, validation gates, continuous training, CI for models, packaging, versioning, audit
reproduction, and the training failure lab (MLO-14..26); serving and the production loop — serving
patterns, latency, batch scoring, shadow/canary/A-B, rollback, monitoring, data drift, concept
drift, feedback loops, alerting integration, the retraining loop, skew, multi-model serving, and the
serving failure lab (MLO-27..41).

### 7.5 `LLM` — LLMOps (34)

What changes with an LLM (LLM-01); tokens and context as units of cost (LLM-02); hosted APIs,
quotas and 429 (LLM-03); local models and quantization (LLM-04); inference servers, batching and the
KV cache (LLM-05..06); GPUs, streaming, routing and fallback, caching, retries (LLM-07..11); serving
the assistant to an SLO and the inference failure lab (LLM-12..13); prompts as code, a prompt
registry, structured output (LLM-14..16); retrieval as a production pipeline — ingestion, chunking,
embeddings, the vector store, embedding versioning, retrieval evaluation, context budgets, and the
retrieval failure lab (LLM-17..25); fine-tuning as an ops problem (LLM-26); and evaluation —
why it is different, evalsets that fail, model-as-judge, regression testing, online evaluation,
human review, groundedness monitoring, and the evaluation failure lab (LLM-27..34).

### 7.6 `AIO` — AIOps (23)

What AIOps is and is not (AIO-01); telemetry as a dataset and the ground truth problem (AIO-02);
time series for operators (AIO-03); anomaly detection from thresholds to learned detectors, and
evaluating a detector honestly (AIO-04..07); log parsing and clustering (AIO-08..09); forecasting
saturation (AIO-10); the detector failure lab (AIO-11); then the incident half — the event data
model, correlation, topology, root cause ranking, change attribution, automated remediation and its
brakes, the feedback loop, measuring the AIOps system itself, and the AIOps failure lab
(AIO-12..23).

### 7.7 `AGO` — AgenticOps (23)

Agents as production workloads — runtime, state, tracing, metrics, non-determinism, evaluation in
CI, versioning, shipping a change, sessions and memory, containment, tool permissions, and the
agent failure lab (AGO-01..15); then agents that operate — the runbook agent, read-only diagnosis,
approval gates, action tiers, audit trails, dry runs, the incident co-pilot, and the agentic
operations failure lab (AGO-16..23).

### 7.8 `MCO` — MCPOps (16)

MCP as an operations problem (MCO-01); servers as services, transports and health (MCO-02..03);
stateless scaling (MCO-04); deployment (MCO-05); authentication (MCO-06); schema versioning
(MCO-07); observability of a tool call (MCO-08); `pulse`'s own boundary (MCO-09); and governance —
registries, allowlists and scopes, supply chain, rate limits, incident response for a bad tool,
multi-tenancy, and the MCP failure lab (MCO-10..16).

### 7.9 `SEC` — Security, governance & compliance (33)

Woven through the whole plan rather than saved for the end: secrets from Day 9 (SEC-01..03);
container hardening and supply chain (SEC-04..06); RBAC, service accounts and network policy in the
cluster (SEC-07..09); secrets management and policy as code (SEC-10..12); model documentation
(SEC-13); deletion and the right to be forgotten (SEC-14); guardrails, prompt injection and the
lethal trifecta, and PII (SEC-15..19); least privilege for non-human actors and audit trails
(SEC-20..21); the MCP boundary (SEC-22..25); and the dedicated Phase 21 — threat modelling, workload
identity, supply chain, data governance, model governance, regulation, auditability, and the
security failure lab (SEC-26..33).

### 7.10 `FIN` — Cost, capacity & FinOps (16)

Also woven: resource requests as a cost decision (FIN-01..02), the cost of a log line (FIN-03),
capacity and load testing (FIN-04), tokens as a unit of cost and caching as a cost control
(FIN-05..06), token budgets and attribution (FIN-07..08), forecasting saturation (FIN-09), tool
rate limits (FIN-10); then Phase 22 — unit economics, attribution, training versus serving,
optimisation, budgets and guardrails, and capacity planning (FIN-11..16).

---

## 8 · 💻 The machine you will actually use

Governed in full by **`docs/02_ADDENDUM_THE_MACHINE.md`**. Summary:

This plan is written for **a single ordinary laptop**, with no GPU and no cloud account. That is a
constraint with teeth — a Kubernetes cluster, a Prometheus, a Grafana, a Loki, an MLflow, a Postgres
and a local language model do not all fit in memory at once — and the plan treats it as part of the
subject rather than an inconvenience:

- **Nothing runs that is not needed today.** Every day's §3 says what to start and what to stop. A
  compose profile per concern, not one file that starts everything.
- **The local cluster is disposable.** `kind delete cluster` and rebuild is a normal move, and the
  fact that it *is* normal is the GitOps lesson (Day 56) arriving early.
- **The local model lane is small on purpose.** A quantized small model on CPU is slow and that is
  useful: latency you can feel is latency you will design around (Day 129).
- **Windows is a first-class target.** The day documents are written for **Git Bash**, with a
  PowerShell translation table in `days/README.md`, and the Docker/Kubernetes days assume **WSL2**
  because that is what actually works.

---

## 9 · 🧰 The zero-cost stack, tool by tool

The full table with the reasoning is in `docs/01_ADDENDUM_ZERO_COST_STACK.md`. What each layer uses:

| Layer | Tool | First day |
| --- | --- | --- |
| Environment & packaging | `uv`, Python 3.12 | 0 |
| Repo gate | `./o`, `ruff`, `pytest` | 0 |
| Service | FastAPI + Uvicorn | 3 |
| CI | GitHub Actions (free tier for public repos) | 13 |
| Containers | Docker Desktop / Docker Engine, BuildKit | 21 |
| Registry | GHCR (free for public images) | 27 |
| Cluster | `kind` (or `k3d`), `kubectl` | 32 |
| Infrastructure as code | Terraform (local + kind providers), Helm, Kustomize | 52 |
| GitOps | Argo CD | 56 |
| Metrics | Prometheus | 62 |
| Dashboards | Grafana | 66 |
| Logs | Loki + Promtail/Alloy | 68 |
| Traces & pipeline | OpenTelemetry SDK + Collector | 69 |
| Alerting | Alertmanager | 76 |
| Load testing | k6 (open-source binary) | 84 |
| Data versioning | DVC with a local remote | 87 |
| Data validation | Pandera / Great Expectations | 89 |
| Orchestration | Prefect or Dagster, local | 93 |
| Experiments & registry | MLflow, local server | 98 |
| Model monitoring | Evidently | 118 |
| Local LLM | Ollama | 126 |
| Hosted LLM | Gemini free tier · Groq · OpenRouter `:free` | 125 |
| Vector store | Qdrant (local container) | 140 |
| Agent tracing | OpenTelemetry + OpenInference conventions | 181 |
| Tool boundary | MCP Python SDK | 200 |
| Secrets | SOPS + age, sealed-secrets, dev-mode Vault | 58 |
| Policy | Kyverno or OPA Gatekeeper | 59 |
| Supply chain | Syft, Grype, Cosign | 15 · 29 · 217 |

**Every one of these is the tool a real team uses.** None of them is a teaching substitute. That is
the point of choosing the open-source layer: the free version *is* the production version.

---

## 10 · 🚫 What you are deliberately not learning

Beyond the non-goals in §1.2, these are parked (🅿️) — you learn the vocabulary, the shape and when
you would reach for them, and you do not build them:

| Parked | Where it is covered | Why parked |
| --- | --- | --- |
| A specific cloud's managed ML platform | Days 99, 109, 202 | Vendor-specific, billable, and the concepts transfer. |
| Multi-node and production-grade cluster operation | Days 32, 45 | Needs hardware you do not have; the failure modes are taught, the node pool is not. |
| GPU cluster scheduling and multi-GPU training | Day 128 | Requires GPUs. The operator's mental model is taught; the hardware is not. |
| Petabyte-scale distributed data processing | Day 93 | Its own discipline; the pipeline contract is what transfers. |
| Streaming infrastructure operation (Kafka administration) | Day 109 | You learn the streaming *serving pattern*, not broker administration. |
| Service meshes | Day 49 | The problems (mTLS, traffic policy) are taught at the primitive level, where they are legible. |
| Vendor observability platforms | Day 71 | The collector makes them interchangeable; you learn the seam, not the SaaS. |

A parked topic still gets a full part with a story, a mechanism and a production section. Parking
means "no build step", never "no explanation" — the point is that you can hold a conversation about
it honestly, including saying *"I have not run that in production."*

---

## 11 · 🔗 How this plan relates to the sibling curricula

Kriya is self-contained: it assumes no other course and teaches every prerequisite it needs. But it
lives beside other plans in this workspace and deliberately does not duplicate them.

| Plan | Subject | Relationship to Kriya |
| --- | --- | --- |
| `setu` | Data science → ML → deep learning → generative AI | Teaches how to *build* the models. Kriya assumes a model exists and asks what happens next. Days 85–122 will feel familiar to a `setu` reader and are written to stand alone anyway. |
| `sutra` · `mandala` | Agentic AI engineering with specific frameworks | Teach how to *build* agents. Kriya's Phases 17–20 teach how to *operate* them — the traces, budgets, evals, brakes and audit trails a built agent does not come with. |
| `kosha` | Git and GitHub in depth | Kriya Days 11–12 and 17 teach exactly the git an operator needs and no more. |
| `krama` | Data structures, algorithms, system design | Kriya's Phase 8 and Phase 23 are the operational face of the same systems. |

**No day in Kriya requires a day in another plan.** Where a concept overlaps, Kriya teaches it from
zero in its own words, because Principle 18 does not admit "see the other course".

---

## 12 · 📖 The reader's contract — how to study this

Six rules that decide whether these 237 days produce an engineer or a reading list.

1. **Type every line.** Nothing under `pulse/`, `deploy/`, `pipelines/` or `platform_ops/` is
   pre-written. Copy-pasting a manifest teaches your clipboard.
2. **Break it before you move on.** Every day has at least one check that must go RED first. Make it
   fail, read the actual error, then fix it. The error text is the thing you are actually learning.
3. **Answer the out-loud question.** Each part ends with one question to answer aloud without
   scrolling up. If you cannot, you have read the part rather than learned it — and that is fine,
   read it again. Nothing here is on a clock.
4. **Do not skip the boring phases.** Phases 1–8 are where the leverage is. Everyone wants to start
   at Day 85. The people who do are the people who cannot debug Day 122.
5. **Keep the ledgers honest.** `PROGRESS.md` is your diary and `./o done N` will not commit a day
   with an unticked box. The checklist cannot tell whether you were honest; that part is yours.
6. **Finish a day, then stop.** One day, one commit, one clean tree. A half-finished day left
   overnight is the single most common way a long curriculum dies.

**The daily rhythm:**

```bash
./o status         # where am I
./o next           # what is next, and the command that writes it
./o start 42       # open the hub, and list its parts
./o scaffold 42    # create the day's lab/
# ... read the hub's §1 and §2, then every part in order, then implement every TODO(me) ...
./o check          # ruff + tests + the depth contract + traceability
./o done 42        # refuses until the checklist is ticked and checks are green
```

---

## 13 · 🗺️ The 24 Phases

Each phase ends with a **gate** — something demonstrated, not asserted. The gate is the answer to
*"what can this system now do that it could not before?"*, and it is run as a command in the last
day's checklist.

| Phase | Days | Theme | Gate |
| --- | --- | --- | --- |
| **0** | **0** | Foundry | `./o check` green; one commit; no secret in git; a driver that refuses a half-finished day |
| **1** | 1–10 | The production mental model and the machine | `pulse` runs on your machine, reads its whole configuration from the environment, and you can name every process, port and file it touches |
| **2** | 11–20 | Change: version control, CI and releases | Every change to `pulse` reaches the main branch through a pipeline that can go red, produces a versioned artifact, and can be reverted in one command |
| **3** | 21–30 | Containers | `pulse` builds to a small, non-root, digest-pinned image that runs identically on your laptop and in CI, and you can diagnose it when it will not start |
| **4** | 31–40 | Kubernetes I — the objects | `pulse` serves traffic from a local cluster through a Service and an Ingress, and you can read `kubectl describe` well enough to explain any pod's state |
| **5** | 41–50 | Kubernetes II — running it well | `pulse` survives a node drain, scales on a real signal, rolls out and rolls back without dropping a request, and runs under least privilege |
| **6** | 51–60 | Infrastructure as code and GitOps | The whole `pulse` platform is described in the repository, reconciled automatically, and a manual `kubectl edit` is detected and reverted |
| **7** | 61–72 | Observability — metrics, logs and traces | One question — "why was that request slow?" — is answerable end to end from `pulse`'s own telemetry, through a single collector |
| **8** | 73–84 | SRE — service levels, alerts and incidents | `pulse` has published SLOs with an error budget, alerts that fire on symptoms only, a runbook per alert, and one real incident with a written postmortem |
| **9** | 85–96 | MLOps I — data and reproducibility | `pulse`'s dataset is versioned, validated at the boundary, and its pipeline is idempotent, re-runnable, and fails loudly on bad data |
| **10** | 97–108 | MLOps II — training, registry and CI for models | A training run is reproducible from a commit, tracked, gated on an offline evaluation, and promoted to a registry that is the only source of truth for what is deployable |
| **11** | 109–122 | MLOps III — serving, monitoring and drift | `pulse` serves a registry model behind a latency SLO, ships new models by canary, detects drift on live traffic, and retrains through a gate rather than on a whim |
| **12** | 123–134 | LLMOps I — the inference stack | `pulse`'s LLM feature runs against a local model and two free providers, with a routing and fallback path that survives a 429 storm inside the same service level as everything else |
| **13** | 135–146 | LLMOps II — prompts, retrieval and context | A prompt change ships through the same pipeline as a code change, and `pulse`'s retrieval index has an owner, a rebuild schedule, a deletion path and a measured recall |
| **14** | 147–158 | LLMOps III — evaluation, guardrails and cost | `pulse`'s assistant has an evalset that can go red in CI, production traffic sampled and scored, guardrails on both sides of the model, and a per-feature cost number |
| **15** | 159–168 | AIOps I — telemetry as data | Your own telemetry becomes a dataset, and a detector you built and honestly measured runs against `pulse`'s live metrics without drowning you in alerts |
| **16** | 169–178 | AIOps II — correlation, cause and remediation | Four hundred alerts collapse into one incident with a ranked list of candidate causes, and one safe remediation runs automatically with brakes you have tested |
| **17** | 179–190 | AgenticOps I — operating agents | `pulse`'s agent is a traced, budgeted, versioned production workload with an evalset in CI, a step cap, a kill switch, and a cost-per-task you can quote |
| **18** | 191–198 | AgenticOps II — agents that operate | An agent diagnoses a real `pulse` incident from telemetry, proposes an action, and only acts through an approval gate that leaves an audit trail |
| **19** | 199–206 | MCPOps I — the tool boundary as infrastructure | Every data source `pulse`'s agents touch is an MCP server that is deployed, versioned, health-checked, authenticated and traced like any other service |
| **20** | 207–214 | MCPOps II — governing the boundary | Every tool an agent can reach is catalogued, scoped, rate-limited, provenance-checked and revocable in one command |
| **21** | 215–222 | Security, governance and compliance | You can produce, on demand, a threat model, an SBOM, a data lineage answer, a model register entry, and an audit trail for any prediction `pulse` has ever made |
| **22** | 223–228 | Cost, capacity and FinOps | Every prediction, generation and agent task in `pulse` has a unit cost, an owner, a budget, and an alert before the budget is gone |
| **23** | 229–236 | Production readiness and the capstone | The whole system passes its own readiness review, survives a staged multi-layer incident, and every claim in the review is provable from the repository alone |
**Every phase gate includes the freshness check (§15).** Phase 0 has no freshness check to run —
nothing is pinned yet except the toolchain — but it does have a gate: `./o check` green, one commit,
and `git ls-files` free of any secret.

**Notice where the AI is.** The first model is trained on Day 97, and the first LLM call is made on
Day 125. Eighty-four days of Phases 1–8 come first. That ordering is the single most important
design decision in this plan: **every hard problem in MLOps and LLMOps is an ordinary
distributed-systems problem in a costume**, and you cannot see the costume until you know the shape
underneath it.

---

## 14 · 🗓️ The 237-Day Map (day → IDs closed)

> The authoritative day→ID assignment. Day documents close **exactly** these IDs — no more, no
> fewer. Every ID appears exactly once across the whole table; `scripts/trace.py` proves it at every
> `./o check`.
>
> Day 0 closes **no IDs** by design: it is the machine, the skeleton and the driver script, which
> are preconditions for the curriculum rather than part of it.
>
> Days whose title contains *"failure lab"* are days where breaking the thing on purpose is the
> entire subject. There are fifteen of them, one per major phase, and they are not optional — they
> are where the curriculum stops being reading.

### Phase 0 — Foundry (Day 0)

| Day | Title | IDs closed |
| --- | --- | --- |
| 0 | Toolchain, skeleton and the `./o` driver — one owner for the environment, a repo that cannot leak a key, and a gate that refuses a half-finished day | — |

### Phase 1 — The production mental model and the machine (Days 1–10)

| Day | Title | IDs closed |
| --- | --- | --- |
| 1 | What operations actually is — the day the code met real traffic, and the repo that remembers instead of the chat | FND-01, FND-02 |
| 2 | The shape of a production system — the request path, the dependencies, the state, and the blast-radius map you draw before anything exists | FND-03 |
| 3 | `pulse` v0 — the service you will operate for the next two hundred days | FND-04 |
| 4 | Linux for operators I — processes, signals, exit codes, and what "the service died" really means | FND-05 |
| 5 | Linux for operators II — the filesystem, permissions, the disk that fills, the log that must rotate | FND-06 |
| 6 | Resources — CPU, memory, the OOM killer, and why your process was simply `Killed` | FND-07 |
| 7 | Networking for operators — ports, sockets, DNS, TCP, and the timeout that saves the system | FND-08, FND-09 |
| 8 | HTTP and TLS in production — status codes that mean something, keep-alive, and the certificate that expires on a Sunday | FND-10 |
| 9 | Configuration and secrets — the twelve-factor service, `.env`, and code that refuses to start rather than failing late | FND-11, FND-12, SEC-01 |
| 10 | Environments and promotion — what the word "production" actually promises | FND-13 |

### Phase 2 — Change: version control, CI and releases (Days 11–20)

| Day | Title | IDs closed |
| --- | --- | --- |
| 11 | Version control for operators — the history you will read at 2am, and the commit that explains itself | FND-14 |
| 12 | Branching, review and the change that can be reverted | FND-15 |
| 13 | The first pipeline — continuous integration that can genuinely fail | PLT-01, PLT-02 |
| 14 | Quality gates — lint, format, types, tests, and a gate that refuses rather than warns | PLT-03 |
| 15 | Build artifacts and reproducibility — the lockfile, the hash, and the first SBOM | PLT-04, SEC-02 |
| 16 | Versioning and releases — semantic versions, tags, changelogs, and the artifact that *is* the release | PLT-05 |
| 17 | Secrets in CI — the token that must never be printed, and the scan that proves it was not | SEC-03 |
| 18 | Deployment strategies on paper — recreate, rolling, blue/green, canary, and what each one costs | PLT-06 |
| 19 | Rollback is a feature — the undo you rehearse before you need it | PLT-07 |
| 20 | Measuring change — the four delivery metrics, computed from your own repository | FND-16, OBS-01 |

### Phase 3 — Containers (Days 21–30)

| Day | Title | IDs closed |
| --- | --- | --- |
| 21 | Why containers — the "works on my machine" bug, solved and not solved | PLT-08 |
| 22 | Images and layers — what is actually inside a container, and what a layer really costs | PLT-09 |
| 23 | Writing the Dockerfile for `pulse` | PLT-10 |
| 24 | Multi-stage builds, small images and a build cache that actually hits | PLT-11 |
| 25 | Running a container — flags, volumes, networks, and `compose` for the whole local stack | PLT-12, PLT-13 |
| 26 | Healthchecks, restart policies, and the container that lies about being up | PLT-14 |
| 27 | Registries, tags and the digest you should deploy instead of `:latest` | PLT-15 |
| 28 | Container security — non-root, read-only root filesystem, dropped capabilities | SEC-04, SEC-05 |
| 29 | The supply chain of your image — base image provenance, scanning and signing | SEC-06 |
| 30 | The container failure lab — exit 137, CrashLoopBackOff, a full disk, a build that will not cache | PLT-16 |

### Phase 4 — Kubernetes I — the objects (Days 31–40)

| Day | Title | IDs closed |
| --- | --- | --- |
| 31 | Why an orchestrator — the problems `compose` stops solving | PLT-17 |
| 32 | A cluster on your laptop — kind, `kubectl`, contexts, and not breaking the real one | PLT-18 |
| 33 | Pods — the unit of scheduling, and why you never create one directly | PLT-19 |
| 34 | Deployments and ReplicaSets — declarative desired state, and the controller that argues with you | PLT-20 |
| 35 | Services and cluster DNS — how a request finds a pod that keeps being replaced | PLT-21 |
| 36 | ConfigMaps, Secrets and the twelve-factor service inside a cluster | PLT-22 |
| 37 | Ingress — getting outside traffic in, and terminating TLS | PLT-23 |
| 38 | Namespaces, labels and selectors — how a cluster stays legible at three hundred objects | PLT-24 |
| 39 | `pulse` on Kubernetes — the first real deploy, from image digest to served request | PLT-25 |
| 40 | The Kubernetes failure lab — ImagePullBackOff, Pending, CrashLoopBackOff, Evicted | PLT-26 |

### Phase 5 — Kubernetes II — running it well (Days 41–50)

| Day | Title | IDs closed |
| --- | --- | --- |
| 41 | Probes — liveness, readiness, startup, and the liveness probe that took production down | PLT-27 |
| 42 | Requests, limits and quality of service — the four numbers everybody guesses | PLT-28, FIN-01 |
| 43 | Rollouts, revisions and `rollout undo` — deployment as a state machine | PLT-29 |
| 44 | Horizontal autoscaling, and why more replicas do not fix a slow model | PLT-30, FIN-02 |
| 45 | Disruption budgets, drains, and surviving a node that goes away | PLT-31 |
| 46 | Jobs and CronJobs — the batch half of every ML system | PLT-32 |
| 47 | Persistent storage and StatefulSets — because models and indexes are not stateless | PLT-33 |
| 48 | RBAC and service accounts — least privilege for the things that are not people | SEC-07, SEC-08 |
| 49 | Network policy — the blast radius of one compromised pod | SEC-09 |
| 50 | The resource-pressure lab — throttling, evictions and a noisy neighbour | PLT-34 |

### Phase 6 — Infrastructure as code and GitOps (Days 51–60)

| Day | Title | IDs closed |
| --- | --- | --- |
| 51 | Infrastructure as code — the idea, and the drift it exists to kill | PLT-35 |
| 52 | Terraform I — providers, resources, state, and `plan` before `apply` | PLT-36 |
| 53 | Terraform II — modules, variables, and the state file you must not lose | PLT-37 |
| 54 | Helm — templating, values, releases, and when templating is the wrong answer | PLT-38 |
| 55 | Kustomize — overlays, and one manifest set for three environments | PLT-39 |
| 56 | GitOps — the cluster reconciles itself to the repository | PLT-40 |
| 57 | Promotion between environments, GitOps-style — and the pull request that is a deploy | PLT-41 |
| 58 | Secrets management — SOPS, sealed secrets, and a development Vault | SEC-10, SEC-11 |
| 59 | Policy as code — admission control, and a guardrail that says no before the cluster says yes | SEC-12 |
| 60 | Drift and reconciliation — the `kubectl edit` you will regret, caught by the system | PLT-42 |

### Phase 7 — Observability — metrics, logs and traces (Days 61–72)

| Day | Title | IDs closed |
| --- | --- | --- |
| 61 | Observability versus monitoring — the question you cannot think of in advance | OBS-02 |
| 62 | Metrics I — counters, gauges, histograms, and Prometheus' data model | OBS-03 |
| 63 | Metrics II — PromQL, `rate()`, quantiles, and the lie told by an average | OBS-04 |
| 64 | Instrumenting `pulse` — RED and USE, done properly and only once | OBS-05, OBS-06 |
| 65 | Cardinality — the label that killed the metrics backend | OBS-07 |
| 66 | Dashboards that answer a question instead of showing everything | OBS-08 |
| 67 | Logs I — structured logging, levels, and the correlation id that ties a request together | OBS-09 |
| 68 | Logs II — shipping, indexing, retention, and what one log line actually costs | OBS-10, FIN-03 |
| 69 | Traces I — spans, context propagation and OpenTelemetry | OBS-11 |
| 70 | Traces II — sampling, tail sampling, and finding the dependency that is slow | OBS-12 |
| 71 | One pipeline for everything — the collector as the single telemetry seam | OBS-13 |
| 72 | The observability failure lab — the outage your dashboards cannot see | OBS-14 |

### Phase 8 — SRE — service levels, alerts and incidents (Days 73–84)

| Day | Title | IDs closed |
| --- | --- | --- |
| 73 | Reliability is a number — indicators, objectives and the error budget | OBS-15, OBS-16 |
| 74 | Choosing indicators for an ML service — and why model accuracy is not one of them | OBS-17 |
| 75 | Error budget policy — the rule that ends the argument between shipping and stability | OBS-18 |
| 76 | Alert on symptoms, not on causes | OBS-19 |
| 77 | Alert quality — precision, recall, fatigue, and the courage to delete an alert | OBS-20 |
| 78 | On-call — rotation, escalation, handover, and being humane about all three | OBS-21 |
| 79 | Runbooks that work at 3am for someone who did not write the service | OBS-22 |
| 80 | Incident command — roles, communication, and the timeline that writes itself | OBS-23 |
| 81 | Your first incident, staged for real, on `pulse` | OBS-24 |
| 82 | Postmortems without blame, and action items that actually get done | OBS-25 |
| 83 | Game days — breaking it on purpose, on a schedule | OBS-26 |
| 84 | Capacity and load testing — knowing your limit before your traffic finds it | OBS-27, FIN-04 |

### Phase 9 — MLOps I — data and reproducibility (Days 85–96)

| Day | Title | IDs closed |
| --- | --- | --- |
| 85 | What MLOps actually is — three things that change independently: code, data, model | MLO-01 |
| 86 | The failure modes an ML system has that ordinary software does not | MLO-02 |
| 87 | Data versioning — content addressing, and the dataset that quietly changed | MLO-03 |
| 88 | Data contracts — the schema agreement at the boundary, enforced | MLO-04 |
| 89 | Data quality — expectations, validation, and failing a pipeline on the data | MLO-05 |
| 90 | Splits, leakage, and the evaluation number you are allowed to believe | MLO-06 |
| 91 | Feature engineering as code — and the training/serving skew it creates | MLO-07 |
| 92 | Feature stores — what they solve, and when a table is genuinely enough | MLO-08 |
| 93 | Pipelines — DAGs, orchestration, idempotency and backfills | MLO-09, MLO-10 |
| 94 | Scheduling and dependencies — the nightly job that must never run twice | MLO-11 |
| 95 | `pulse`'s data pipeline, end to end and re-runnable | MLO-12 |
| 96 | The data failure lab — silent corruption, late data, duplicates, a changed unit | MLO-13 |

### Phase 10 — MLOps II — training, registry and CI for models (Days 97–108)

| Day | Title | IDs closed |
| --- | --- | --- |
| 97 | Reproducible training — seeds, environments, and a run you can run again in a year | MLO-14 |
| 98 | Experiment tracking — runs, parameters, metrics, artifacts, and one place to compare them | MLO-15 |
| 99 | The model registry — stages, lineage, and a single answer to "what is in production?" | MLO-16 |
| 100 | Model cards, and the questions a reviewer asks before they approve | MLO-17, SEC-13 |
| 101 | Offline evaluation — the metric that matches the business, slices, and an honest baseline | MLO-18, MLO-19 |
| 102 | Validation gates — the check that refuses to promote a worse model | MLO-20 |
| 103 | Continuous training — what should trigger a retrain, and what should not | MLO-21 |
| 104 | CI for models — testing the data, the training code, and the model itself | MLO-22 |
| 105 | Packaging a model — formats, artifacts, and the pickle that will not load next month | MLO-23 |
| 106 | Model versioning, and staying compatible with the code that calls it | MLO-24 |
| 107 | Reproducing a six-month-old prediction — the audit request, answered | MLO-25 |
| 108 | The training failure lab — non-determinism, a drifted dependency, a lost run | MLO-26 |

### Phase 11 — MLOps III — serving, monitoring and drift (Days 109–122)

| Day | Title | IDs closed |
| --- | --- | --- |
| 109 | Serving patterns — batch, online, streaming, and choosing between them on purpose | MLO-27 |
| 110 | Online serving — the latency budget, p99, and the model that is simply too slow | MLO-28 |
| 111 | Batch scoring — the pipeline that writes predictions nobody is waiting for | MLO-29 |
| 112 | Shipping a model — shadow, canary and A/B for something that has no single right answer | MLO-30, MLO-31 |
| 113 | Rollback for models — the version you can always go back to | MLO-32 |
| 114 | Monitoring a model in production — inputs, outputs, and the ground truth you do not have yet | MLO-33 |
| 115 | Data drift — detection, thresholds, and the drift alert that cried wolf | MLO-34 |
| 116 | Concept drift and model decay — when the world changes instead of the data | MLO-35 |
| 117 | Feedback loops, delayed labels, and the loop that trains on its own output | MLO-36 |
| 118 | Wiring model monitoring into the alerting you already built | MLO-37 |
| 119 | The retraining loop, automated and gated | MLO-38 |
| 120 | Skew — the training/serving difference that only ever shows up in production | MLO-39 |
| 121 | Multi-model serving, ensembles, and routing between them | MLO-40 |
| 122 | The serving failure lab — cold start, memory blow-up, thundering herd, stale features | MLO-41 |

### Phase 12 — LLMOps I — the inference stack (Days 123–134)

| Day | Title | IDs closed |
| --- | --- | --- |
| 123 | What changes when the model is an LLM — and what does not change at all | LLM-01 |
| 124 | Tokens and context windows — the units your latency, your quota and your bill are measured in | LLM-02, FIN-05 |
| 125 | Hosted model APIs — quotas, rate limits, and reading a 429 properly | LLM-03 |
| 126 | Running a model on your own machine — quantization, and what actually fits in your RAM | LLM-04 |
| 127 | Inference servers — continuous batching, the KV cache, and throughput against latency | LLM-05, LLM-06 |
| 128 | GPUs for operators — what they change, and how to do this without one | LLM-07 |
| 129 | Streaming responses, and the operational cost of a generation that takes forty seconds | LLM-08 |
| 130 | Routing and fallback — surviving one provider having a bad day | LLM-09 |
| 131 | Caching — exact, semantic, and provider-side prompt caching | LLM-10, FIN-06 |
| 132 | Timeouts, retries, backoff and idempotency for a call that costs money | LLM-11 |
| 133 | `pulse`'s assistant behind the same service level as the rest of the system | LLM-12 |
| 134 | The inference failure lab — a 429 storm, a context overflow, a silent truncation, a dead provider | LLM-13 |

### Phase 13 — LLMOps II — prompts, retrieval and context (Days 135–146)

| Day | Title | IDs closed |
| --- | --- | --- |
| 135 | The prompt is code — versioned, reviewed and diffed like anything else that changes behaviour | LLM-14 |
| 136 | A prompt registry, and rolling out a prompt change safely | LLM-15 |
| 137 | Structured output in production — schemas, validation and repair | LLM-16 |
| 138 | Retrieval in production I — ingestion is a data pipeline, with everything that implies | LLM-17 |
| 139 | Retrieval in production II — chunking, embeddings, and the reindex you must schedule | LLM-18, LLM-19 |
| 140 | Vector store operations — recall, latency, updates, and the delete that must actually delete | LLM-20 |
| 141 | Embedding model versioning, and the day you have to re-embed everything | LLM-21 |
| 142 | Retrieval evaluation — measuring the half of the system that fails silently | LLM-22 |
| 143 | Context as a budget — truncation, compaction, and what gets dropped first | LLM-23 |
| 144 | Freshness, deletion, and the right to be forgotten inside an index | LLM-24, SEC-14 |
| 145 | The retrieval failure lab — a stale index, a poisoned document, an empty result treated as an answer | LLM-25 |
| 146 | Fine-tuning as an operations problem — the lifecycle, and why you probably should not yet | LLM-26 |

### Phase 14 — LLMOps III — evaluation, guardrails and cost (Days 147–158)

| Day | Title | IDs closed |
| --- | --- | --- |
| 147 | Why evaluating an LLM is different — there is no single right answer | LLM-27 |
| 148 | Building an evalset that can actually fail | LLM-28 |
| 149 | A model judging a model — the operational version, and its own failure modes | LLM-29 |
| 150 | Regression testing prompts and models in the pipeline | LLM-30 |
| 151 | Online evaluation — sampling live traffic and scoring it | LLM-31 |
| 152 | Human review — annotation as an operational pipeline with a queue and a cost | LLM-32 |
| 153 | Groundedness and hallucination monitoring | LLM-33 |
| 154 | Guardrails — input filters, output filters, and defence in depth | SEC-15, SEC-16 |
| 155 | Prompt injection against a production system — and the three capabilities you must never combine | SEC-17, SEC-18 |
| 156 | Personal data, redaction, and the boundary your model traffic crosses | SEC-19 |
| 157 | Token budgets and cost attribution — the number finance will eventually ask you for | FIN-07, FIN-08 |
| 158 | The evaluation failure lab — a green evalset that shipped a broken assistant | LLM-34 |

### Phase 15 — AIOps I — telemetry as data (Days 159–168)

| Day | Title | IDs closed |
| --- | --- | --- |
| 159 | What AIOps is — and the four things it is regularly sold as and is not | AIO-01 |
| 160 | Your telemetry is a dataset — collection, retention, labelling, and the ground truth problem | AIO-02 |
| 161 | Time series for operators — trend, seasonality, change points, and what "normal" means | AIO-03 |
| 162 | Anomaly detection I — thresholds and baselines, and exactly why static thresholds fail | AIO-04 |
| 163 | Anomaly detection II — statistical and learned detectors on real `pulse` metrics | AIO-05, AIO-06 |
| 164 | Evaluating a detector honestly — precision, recall, and alert fatigue as a measurable cost | AIO-07 |
| 165 | Log parsing — templates, and turning free text into countable events | AIO-08 |
| 166 | Log clustering — finding the error that is new rather than the error that is loud | AIO-09 |
| 167 | Forecasting — saturation, capacity, and predicting the wall before you hit it | AIO-10, FIN-09 |
| 168 | The detector failure lab — the model that alerts on every deploy and nothing else | AIO-11 |

### Phase 16 — AIOps II — correlation, cause and remediation (Days 169–178)

| Day | Title | IDs closed |
| --- | --- | --- |
| 169 | Events, alerts and incidents — the data model underneath all of it | AIO-12 |
| 170 | Correlation and grouping — from four hundred alerts to one incident | AIO-13 |
| 171 | Topology — knowing what talks to what, and deriving it rather than drawing it | AIO-14 |
| 172 | Root cause analysis, honestly — ranked candidates, not an oracle | AIO-15, AIO-16 |
| 173 | Change intelligence — attributing an incident to the deploy that caused it | AIO-17 |
| 174 | Automated remediation I — the safe actions, and the ladder of trust you climb slowly | AIO-18 |
| 175 | Automated remediation II — brakes, rate limits, and the remediator that made it worse | AIO-19, AIO-20 |
| 176 | Closing the loop — responder feedback that improves the system instead of vanishing | AIO-21 |
| 177 | Measuring the AIOps system itself — acknowledgement, resolution, noise, false confidence | AIO-22 |
| 178 | The AIOps failure lab — beautifully correlated nonsense during a real outage | AIO-23 |

### Phase 17 — AgenticOps I — operating agents (Days 179–190)

| Day | Title | IDs closed |
| --- | --- | --- |
| 179 | What AgenticOps is — operating a system that decides its own next step | AGO-01 |
| 180 | The agent as a production workload — runtime, concurrency, and where the state lives | AGO-02 |
| 181 | Tracing an agent — the span tree that explains a run you did not watch | AGO-03 |
| 182 | Metrics for agents — task success, steps per task, cost per task, and time to answer | AGO-04, AGO-05 |
| 183 | Non-determinism in production — testing something that does not repeat | AGO-06 |
| 184 | Agent evaluation in the pipeline — trajectories, rubrics, and a gate that can go red | AGO-07, AGO-08 |
| 185 | Versioning an agent — prompt, tools, model, and the compatibility matrix between them | AGO-09 |
| 186 | Shipping an agent change — canary, shadow, and what rollback means for a conversation | AGO-10 |
| 187 | Sessions, state and memory as operational surfaces with a lifecycle | AGO-11 |
| 188 | Containment — step caps, budgets, timeouts, and a kill switch that has been tested | AGO-12, AGO-13 |
| 189 | Least privilege for a non-human actor — tool permissions and the identity behind them | SEC-20, AGO-14 |
| 190 | The agent failure lab — the loop that spent the entire day's quota in nine minutes | AGO-15 |

### Phase 18 — AgenticOps II — agents that operate (Days 191–198)

| Day | Title | IDs closed |
| --- | --- | --- |
| 191 | The runbook agent — turning `runbooks/` into something a machine can execute | AGO-16 |
| 192 | Read-only first — the diagnosis agent that is structurally unable to change anything | AGO-17 |
| 193 | Approval gates and human-in-the-loop for an operational action | AGO-18 |
| 194 | Action tiers and blast radius — read, suggest, act, act-with-approval | AGO-19 |
| 195 | Audit trails — who did what, and proving afterwards that it was the agent | AGO-20, SEC-21 |
| 196 | Dry run — the plan you review before anything happens | AGO-21 |
| 197 | The incident co-pilot, wired to telemetry you built yourself | AGO-22 |
| 198 | The agentic operations failure lab — a confident agent, a wrong action, a real outage | AGO-23 |

### Phase 19 — MCPOps I — the tool boundary as infrastructure (Days 199–206)

| Day | Title | IDs closed |
| --- | --- | --- |
| 199 | What MCP is, and the exact moment it stops being a protocol and becomes an operations problem | MCO-01 |
| 200 | MCP servers as services — lifecycle, transports and health | MCO-02, MCO-03 |
| 201 | Stateless scaling and session semantics at the tool boundary | MCO-04 |
| 202 | Deploying an MCP server exactly the way you deploy everything else | MCO-05 |
| 203 | Authentication and authorization at the boundary | MCO-06, SEC-22 |
| 204 | Versioning tools and schemas without breaking every client at once | MCO-07 |
| 205 | Observability for MCP — tracing one tool call from agent to database and back | MCO-08 |
| 206 | `pulse`'s data boundary — the servers your agents are actually allowed to use | MCO-09 |

### Phase 20 — MCPOps II — governing the boundary (Days 207–214)

| Day | Title | IDs closed |
| --- | --- | --- |
| 207 | Registries and discovery — a catalogue of tools that is true today | MCO-10 |
| 208 | Allowlists and scopes — per-agent tool policy, enforced at the boundary | MCO-11, SEC-23 |
| 209 | The supply chain of a third-party MCP server | SEC-24, MCO-12 |
| 210 | Rate limits and quotas — the tool that hammered the production database | MCO-13, FIN-10 |
| 211 | Secrets at the boundary — what the tool sees, and what it must never see | SEC-25 |
| 212 | Incident response for a bad tool — revoke, roll back, audit, and tell people | MCO-14 |
| 213 | Multi-tenant tool serving — isolating one caller from another | MCO-15 |
| 214 | The MCP failure lab — a poisoned tool description and a perfectly compliant agent | MCO-16 |

### Phase 21 — Security, governance and compliance (Days 215–222)

| Day | Title | IDs closed |
| --- | --- | --- |
| 215 | Threat modelling an AI system — assets, actors, and the diagram that finds the hole | SEC-26 |
| 216 | Identity for workloads — what a service is, and how it proves it | SEC-27 |
| 217 | Supply chain — SBOMs, signing, provenance, and dependency risk you can actually act on | SEC-28 |
| 218 | Data governance — classification, retention, lineage, and deletion that is real | SEC-29 |
| 219 | Model governance — approval, documentation, and a register that is not theatre | SEC-30 |
| 220 | Regulation without the panic — what the frameworks actually require of an operator | SEC-31 |
| 221 | Auditability — proving what ran, on which data, at what time, under which version | SEC-32 |
| 222 | The security failure lab — a leaked key and an exposed endpoint, rehearsed on purpose | SEC-33 |

### Phase 22 — Cost, capacity and FinOps (Days 223–228)

| Day | Title | IDs closed |
| --- | --- | --- |
| 223 | FinOps for AI systems — the unit economics of one prediction and one generation | FIN-11 |
| 224 | Cost attribution — tagging, and answering "which feature spent that?" | FIN-12 |
| 225 | The cost of training against the cost of serving, measured rather than assumed | FIN-13 |
| 226 | Making serving cheaper without breaking the service level | FIN-14 |
| 227 | Budgets, alerts, and the guardrail that stops a runaway spend at 3am | FIN-15 |
| 228 | Capacity planning for quota-shaped and GPU-shaped resources | FIN-16 |

### Phase 23 — Production readiness and the capstone (Days 229–236)

| Day | Title | IDs closed |
| --- | --- | --- |
| 229 | The production readiness review — the checklist you now actually understand | FND-17 |
| 230 | Documentation that survives you — architecture, runbooks, decisions | FND-18 |
| 231 | The handover — operating a system somebody else built | FND-19 |
| 232 | Day-2 operations — upgrades, migrations, deprecations, and the long tail | FND-20 |
| 233 | Capstone I — the full stack, deployed, observed and defended | FND-21 |
| 234 | Capstone II — a staged incident that crosses the ML, LLM, agent and tool layers | FND-22 |
| 235 | Capstone III — the audit: prove every claim in the readiness review from the repo alone | FND-23 |
| 236 | What you can now say in an interview, and an honest map of what you have not learned | FND-24 |

---

## 15 · 🚦 Phase Gates & the Freshness Check

A phase is **green** only when all six hold:

1. Every day in the phase has its row in `docs/PROGRESS.md` with gates green.
2. `scripts/trace.py` shows **no open IDs** from this or any earlier phase.
3. `./o check` passes on the whole repo — lint, format, offline tests, **the §17 depth contract for
   every written day**, and traceability.
4. Every day in the phase has a `parts/` directory. A day with no `parts/` is not written (§17.2),
   so a phase containing one cannot be green.
5. The phase's own gate, from the table in §13, is demonstrated — not asserted. The demo command is
   in that phase's last day's `CHECKLIST.md`, and it either produces the stated output or it does
   not.
6. The **freshness check** passes.

### 15.1 The freshness check

Run at every phase gate, and recorded in `docs/PROGRESS.md`. This plan pins nothing by version
(§5), which means the ecosystem is allowed to move underneath it — so it must be re-read on a
schedule rather than trusted.

| Check | The question | If it moved |
| --- | --- | --- |
| Kubernetes | Has the minor version you pinned gone out of support? Any API removed? | Amend, then upgrade the local cluster deliberately as a day-2 exercise (Day 232). |
| Container base images | New CVEs in your base? A new digest? | Rebuild and re-scan; a row in `docs/PACKAGES.md`. |
| Prometheus / OTel | Any metric or semantic-convention rename? | OpenTelemetry conventions move; a renamed attribute silently empties a dashboard. |
| Model free tiers | Do all three providers still have a free lane? Same model ids? | Free rosters move without notice. If a pinned model lost its free tier, **amend first** (Addendum 01's rule). |
| MLflow / DVC / Evidently | Breaking change in a format you have artifacts in? | An artifact format change is a migration, and migrations get an ADR. |
| MCP | Has the specification revision changed? | Re-read the spec revision before writing any MCP day. |
| Your own quotas | GitHub Actions minutes, GHCR storage, disk on your laptop | Quota is the currency (§4). Running out is an incident, and it is a good one to have had. |

**Never** skip a day, merge two days, or reorder days without an ADR. A gate is never passed because
time ran out (Principle 17): `./o done N` is gated on a ticked `CHECKLIST.md` and green checks, and
on nothing else.

---

## 16 · 📒 Ledgers & Traceability

All ledgers live in `docs/`.

| File | Nature | Rule |
| --- | --- | --- |
| `docs/PROGRESS.md` | Append-only | One row per completed day; **the last row is where we are.** |
| `docs/PACKAGES.md` | Append-only | Every install: tool, version, date observed, day, why. No invented versions (Principle 7). |
| `docs/INCIDENTS.md` | Append-only | Every failure lab and every real incident: what broke, what you saw first, what it actually was, what you changed. **This is the most valuable file in the repository.** |
| `docs/DECISIONS.md` | Append-only | The one-line index of ADRs, so a cold reader finds the decision without grepping. |
| `docs/CHANGELOG_PLAN.md` | Append-only | Every amendment to this plan (Principle 14). |
| `docs/TRACEABILITY.md` | **Regenerated** | `scripts/trace.py` scans every hub against §14. An open ID in a completed phase is a bug. |
| `docs/CURRICULUM_INDEX.md` | **Regenerated** | The reverse of §14: ID → day, grouped by curriculum. |
| `docs/TRACKER.md` | **Regenerated** | `scripts/tracker.py` reports what is written, **how many parts each day has**, and what is pending. A thin day is visible from this table alone. |

**Three ledgers are regenerated and five are written by hand — do not confuse them.**
`TRACEABILITY.md`, `CURRICULUM_INDEX.md` and `TRACKER.md` are outputs; editing them by hand only
means the next `./o check` silently overwrites you. The other five are append-only history, written
by the day you are finishing — every day document ends with the exact rows to paste (§17.5).

**On `INCIDENTS.md`.** Ninety of these 237 days end with something deliberately broken. The ledger
that records what you saw *first* — before you knew the cause — is the one that turns those days
into operational instinct. Six months later it is also the most convincing document in the
repository: a list of failures you have personally caused and diagnosed is worth more in an
interview than any certificate.

Addenda are `docs/NN_ADDENDUM_*.md`; ADRs are `docs/adr/ADR-NNNN-*.md`.

---

## 17 · 📐 The Depth Contract — how a day is written

> **Why this section exists.** The obvious way to write an ops curriculum is one long page per day.
> It fails for three reasons, and they are worth stating before the rules that prevent them.
>
> A reader cannot revisit *one* idea without re-reading four. There is no artifact that
> distinguishes a thinly-covered subtopic from a missing one — a day either "exists" or does not.
> And a time estimate at the top of a page silently authorises the worst edit in technical writing:
> cutting an explanation because the document is getting long.
>
> So a day here is **one hub plus one document per subtopic**, every document written from zero
> prior knowledge and carried through to how the idea is used in production. This section states
> exactly what "covered properly" means, so it can be reviewed by reading and partly checked by a
> script. It is Principles 16, 17 and 18, made concrete.

### 17.1 The three commitments

Everything below follows from three sentences.

**One idea per document.** A subtopic that cannot be read alone, understood without scrolling past a
different subtopic, and explained back out loud is not one subtopic — it is several, badly stacked.
If a document needs the word "also" to introduce its second half, it is two documents.

**No clocks.** Nothing in a day folder carries a time estimate, an "estimated hours" field, a "this
should take 90 minutes", or a suggested pace. A topic takes as long as it takes; the reader may
spend one sitting or five on a single part. **Content is never trimmed to fit a schedule**, and a
day is never declared finished because a duration elapsed. The day number is an index into the
subject, nothing more.

**Zero to production, in one document.** Each part starts where a reader who has never heard of the
idea can stand, and ends where a working professional stands: how the idea appears in a real system,
what a senior engineer does differently from the tutorial version, what fails at scale or under
concurrency, what a reviewer or an interviewer will probe, and **what you would be paged for**.
Strong fundamentals and advanced technique are not separate tracks — they are the beginning and the
end of the same page.

### 17.2 The folder shape

Every day, without exception, is a folder of this shape:

```
days/day-NNN-<day-slug>/
├── LESSON.md          # the hub — orientation, story, part map, build brief, check, budget, ledger
├── CHECKLIST.md       # the definition of done; ./o done NNN refuses to commit until ticked
├── parts/             # THE TEACHING — one document per subtopic
│   ├── 01-<slug>/     # section 1 — two digits, zero-padded, then what the section is about
│   │   ├── 1.1-<slug>.md
│   │   └── 1.2-<slug>.md
│   ├── 02-<slug>/     # section 2
│   │   ├── 2.1-<slug>.md
│   │   └── 2.2-<slug>.md
│   └── 03-<slug>/
│       └── 3.1-<slug>.md
└── lab/               # created by ./o scaffold NNN; the learner's own scratch code
```

`parts/` is mandatory. **A day with no `parts/` directory is, by definition, not written** — the
tracker reports it as pending and the phase gate cannot go green.

**Every folder name carries its subject.** A number alone tells a reader nothing: `days/day-143/` and
`parts/02/` are addresses, not answers, and 237 days of them are indistinguishable in a file tree, a
`git log` or an editor's tab bar. So the number is followed by a short kebab-case slug naming what
is inside — `days/day-023-the-dockerfile-for-pulse/`, `parts/03-probes/`. The rules:

| Folder | Shape | Slug comes from | Length |
| --- | --- | --- | --- |
| the day | `day-NNN-<slug>` | the hub's `title` frontmatter, minus articles | 1–4 words |
| a section | `NN-<slug>` | the section's heading in the hub's §2 map | 1–3 words |

**Day numbers are zero-padded to three digits.** This plan runs to Day 236, and two-digit padding
sorts day 100 between day 10 and day 11 in every file listing there is. `day-007-networking` and
`day-115-data-drift` sort correctly; `day-7` and `day-115` do not.

**The number is still the identity.** The slug is a label on it, never a key: every tool resolves a
day by its number and accepts whatever slug follows, so renaming a folder to a better slug can never
break `./o`, the depth check, the tracker or the traceability generator. Part *filenames* already
carry a full slug and do not change.

**Every part lives inside its section's folder**, named with two digits, zero-padded, then the slug:
section 1 is `parts/01-<slug>/`, section 12 is `parts/12-<slug>/`. A part document is never loose in
`parts/`. The folder number and the number before the dot in the filename must agree —
`parts/02-images/2.3-<slug>.md` is correct; `parts/02-images/3.1-<slug>.md` is a bug the depth check
rejects. The folders exist for navigation: a day with eighteen parts is a wall of filenames without
them, and a section is exactly the unit a reader wants to open at once.

### 17.3 The numbering rule — what `1.1` and `2.3` mean

Part numbers are **`<section>.<subtopic>`**, both scoped to the day.

- The **section** number groups subtopics that share one mental model. A section is usually one
  curriculum ID, one stage of a pipeline, or one phase of a mechanism.
- The **subtopic** number is the reading order inside that section. It starts at `1`, never `0`, and
  has no gaps.

The hub's §2 map declares what each section *is*. A typical two-ID day:

| Section | Means | Example subtopics |
| --- | --- | --- |
| **1.x** | the day's first ID | `1.1` what it is · `1.2` how it behaves · `1.3` where it bites |
| **2.x** | the day's second ID | `2.1` … `2.2` … |
| **3.x** | the synthesis — the two IDs meeting | `3.1` the trap only visible when both are true |

An observability day uses sections as *signal types*: `1.x` what the signal is, `2.x` how it is
collected, `3.x` what it costs, `4.x` what it cannot tell you. A Kubernetes day uses them as *object,
then behaviour, then failure*. An incident day uses them as *stages of the incident*. **The grouping
must be stated in the hub**; an unexplained numbering is a bug in the doc.

**Links between parts are relative.** Inside one section a sibling is just its filename
(`1.2-<slug>.md`); across sections it goes up one level (`../01-<slug>/1.5-<slug>.md`); the hub is
`../../LESSON.md`. Every `prev`/`next` in the frontmatter uses the same form. The hub's §2 map links
from the day folder: `parts/01-<slug>/1.1-<slug>.md`.

### 17.4 What a part document must contain

Every file in `parts/` carries all ten of these, **in this order**. Sections 2–10 are the reader's
path from "never heard of it" to "could defend this in a design review at 3am".

| # | Section | The rule |
| --- | --- | --- |
| 1 | **frontmatter** | `day`, `part`, `title`, `ids`, `level`, `prerequisites`, `prev`, `next`. Machine-read; the reader ignores it. **No duration field of any kind** (Principle 17), and **no `papers:`, `paper:` or `kind: paper` key** — this curriculum cites no papers (ADR-0006), and `./o depth` fails a part that carries one. |
| 2 | **One-line answer** | The subtopic's claim in a single sentence, before anything else. A reader who reads only this line has learned something true. |
| 3 | **The story** | A concrete scene before any abstraction: a person, a machine, a failure, a decision. Storytelling is not decoration here — it is the hook the definition hangs on. It comes **first**, in plain words, with **no jargon at all**. |
| 4 | **The idea in plain language** | The concept itself, assuming the reader has never met it (Principle 18). Every term defined the first time it appears — *including terms from earlier days, with a link to the part that introduced them*, never an assumption of recall. No code. |
| 5 | **Why Kriya needs it** | The concrete later day that breaks without this. *"You meet this again on Day 115, where a drift detector has to distinguish a broken upstream from a changed world"* is the shape. Never "this is important". |
| 6 | **The mechanism** | How it actually works: the runnable code, the manifest, the protocol exchange written out, or the diagram. Nothing skipped as "obvious". Mermaid whenever the concept is spatial, sequential, or a state machine. |
| 7 | **Line by line** | Every non-obvious token of every code block, explained — and *why it is that line and not another*. Written as a `**Line by line:**` list **immediately after each code block**, so the reader never scrolls to find the explanation of what they are looking at. Blocks showing error output, a bare check command, or a diagram are exempt. **An unexplained line is a bug in the doc.** This is the contract's **only conditional section**: a part that carries no code needing a walkthrough — a `concept` part, legitimately — does not carry this section, and `./o depth` does not ask for it. |
| 8 | **When it breaks** | The **real** error text, reproduced verbatim — the traceback, the HTTP status, the `kubectl describe` events block, the PromQL error, the 429 body. What it says, what it actually means, and the smallest fix. This is what you meet at 3am; the happy path is not. |
| 9 | **In production** | Where this idea shows up in a real system and what changes there: the version a professional writes instead of the teaching version, what degrades at scale or under concurrency, the failure mode that only appears with real traffic, the review comment a senior engineer leaves, **the signal you would alert on**, and the question an interviewer asks to find out whether you have actually used it. **This is the section that makes the document professional rather than introductory. It is not optional.** |
| 10 | **Check yourself** | One command the reader can run right now, plus one question they must answer **out loud** without scrolling up. |

Three further rules that have no section of their own:

- **The one-idea test.** If a part needs "also" to introduce its second half, split it.
- **The standalone test.** A part must be readable cold. If it depends on an earlier idea, **name
  that part and link it** — never assume the reader remembers Day 22 on Day 190.
- **The no-shortcut test.** "For now, just accept that" is banned unless it links forward to the part
  that explains it. **A deferred explanation must have an address.**

#### 17.4.1 Kriya's five additional part rules

These come from Principles 7, 8, 12, 13 and 15 and apply on top of the ten sections above:

1. **Never invent an API, a flag or a field.** Any part that uses a `kubectl` field, a PromQL
   function, a Terraform argument or a library symbol names the **official page checked that day**,
   inline, next to the code: *"Verified against `kubernetes.io/docs/…` on YYYY-MM-DD."*
2. **Never invent a version.** Any part that installs something states the version it verified and
   how, or leaves a `TODO` containing **the exact lookup command**. The row lands in
   `docs/PACKAGES.md` the same day.
3. **Every part that introduces a capability names its blast radius** (Principle 13). What is the
   worst thing this can now do, who can trigger it, and what bounds it? A part that adds a write
   path, an autoscaler, a remediation or a tool without answering those three has taught half the
   subject.
4. **Every part that introduces a signal says how you would alert on it** (Principle 12), or says
   explicitly that you would not and why. "You would not page a human for this" is a real and
   frequently correct answer, and saying it is the lesson.
5. **Every part that costs anything states the cost in quota units** — requests, tokens, RAM, disk,
   CI minutes (Principle 15 · Addendum 01). `0` is an answer; state it.
#### 17.4.2 Research, and why no part cites a paper

Plenty of what this curriculum teaches began as a published result. Exponential backoff, the
container's resource box, the tail-latency problem and the agent loop all arrived as research before
they arrived as a flag in a config file.

**None of that is cited here, and no day carries a `papers/` folder.** ADR-0006 removed it. The
short version is that an operator needs the retry ladder, the jitter and the ceiling rather than the
venue an idea was published in, and that a citation was the single easiest fact in this plan to
fabricate.

Where research genuinely changed how an operator behaves, the ordinary part says so in ordinary
words — *"this is the retry pattern the internet settled on after congestion collapse in the
1980s"* — with no title, no year, no identifier, no link and no author. Where it does not change how
an operator behaves, it is not mentioned. There is no `papers:` key, no `paper:` key and no
`kind: paper` document, and `./o depth` fails a part that carries any of the three.


### 17.5 What the hub (`LESSON.md`) must contain

The hub is **orientation and assembly, never the teaching itself**. It carries no `Line by line:`
walkthrough — that lives in the parts. Required, in this order:

1. **frontmatter** — `day`, `phase`, `phase_name`, `title`, `ids`, `principles`, `kind`,
   `plan_version`, `parts` (the count), `generated`, `status`, `lab_scaffolded`, `commit`.
2. **yesterday / today / tomorrow** — one line each, as a blockquote. No time estimate.
3. **`## §1 Where we are`** — the day's whole idea as a scene and an analogy, in plain language,
   before any code and before any jargon.
4. **`## §2 The map`** — a table of every part: number, linked title (`parts/01-<slug>/1.1-<slug>.md`),
   what it answers, and its `level`. Grouped by section, with **one line saying what each section
   means for this day**. **No minutes column, ever.**
5. **`## §3 Setup — run this`** — every `mkdir`, `uv add <pkg>==<exact>`, `docker compose up`,
   `kind create` the day needs, pinned, with the version verified that day — **and what to stop**,
   because the machine is finite (§8).
6. **`## §4 Build brief`** — the files to create, with `TODO(me)` markers left **unsolved**.
7. **`## §5 The check that must be able to fail`** — the check that is RED before the work is done
   (Principle 11). State how to make it go red on purpose.
8. **`## §6 Cost & quota budget`** — model calls per provider in RPM/RPD, CI minutes, RAM and disk
   for anything started today (Principle 15 · Addendum 01). `0` is an answer; state it.
9. **`## §7 Traps`** — the mistakes that eat an evening, including the named trap from §5.1 if the
   day touches one.
10. **`## §8 Verify before you build`** — the live documentation URLs actually fetched on the day of
    writing (Principle 8), each with the date it was fetched.
11. **`## §9 Say it in an interview`** — one paragraph, spoken voice, honest, tied to what was built.
    War stories with numbers beat adjectives.
12. **`## §10 Done when`** — pointer to `CHECKLIST.md`. Defined by understanding and green checks,
    **never by elapsed time**.
13. **`## §11 Ledger & commit`** — the verbatim snippets that end every day: the `PROGRESS.md` row,
    any `PACKAGES.md` rows, any `INCIDENTS.md` row for a failure lab, any `DECISIONS.md` row, and
    the git commit message `day NNN: <title> — closes <IDs>`. **The hub ends with these.** *(Ritual
    is the point: the repo is the memory, not the chat.)*

### 17.6 The `level` field — how a day climbs

Every part declares exactly one `level`, and a well-built day climbs through them in order:

| `level` | The reader at the end of this part |
| --- | --- |
| `foundation` | Knows what the thing *is* and could define it to someone else without using the word itself. |
| `working` | Can use it correctly on their own problem, and recognises its error messages on sight. |
| `production` | Knows what changes when it runs in a real system — scale, concurrency, quota, failure, review, the page at 3am — and can defend the choice. |

A day that is all `foundation` is a tutorial. A day that opens at `production` has skipped the
reader. Most days run `foundation → working → production`; a single part may itself climb, which is
exactly what its *In production* section is for.

### 17.7 How finely to split

Split by **idea boundaries, never by length or by pace**. A part is finished when its one idea is
fully explained — *including its production face* — and not before.

| Day kind | Split by |
| --- | --- |
| `setup` | one tool, one file, or one command per part |
| `lab` (1 ID) | mechanism → behaviour → edge case → failure mode → production use |
| `lab` (2–3 IDs) | one section per ID, plus a synthesis section where they meet |
| `concept` | one claim per part, each with its evidence |
| `incident` | one stage of the incident per part: detect → triage → mitigate → resolve → learn |
| `gate` | one acceptance criterion per part |
| `capstone` | one component per part, in build order |

There is deliberately **no target part count and no target length**. If a subject needs four parts it
gets four; if it needs twenty-two it gets twenty-two, and the day simply spans more sittings
(Principle 17). The only wrong answers are a part that carries two ideas and a part that stops before
production.

**Every day carries at least one part whose subject is a deliberate failure.** Breaking the thing on
purpose is not a bonus section at the bottom of a page — it is a document of its own, usually at
`production` level, and on the days titled *"the … failure lab"* it is the entire day.

### 17.8 What "in depth" is not

The failure modes this format exists to prevent, stated so they can be caught in review:

- **Splitting without deepening.** Cutting one 30 000-character page into six 5 000-character pages
  changes nothing. Each part must **gain** the story, the mechanism, the failure text, the production
  face and the check it never had.
- **Summary in place of explanation.** *"This line sets the readiness probe"* is a caption. *"This
  probe's `failureThreshold: 3` with a 10-second period means a pod is pulled from the Service after
  30 seconds of failing — which is why a 45-second model load without a `startupProbe` gets killed
  before it ever serves"* is an explanation.
- **Stopping at the toy example.** A part that shows the idea working on one request and never says
  what happens at ten thousand has taught half the subject. Section 9 is where the other half lives.
- **Assuming the previous day.** Each part names its prerequisite and links it. 237 days is long
  enough that Day 22 is genuinely forgotten by Day 190.
- **Code without failure.** Every mechanism has a matching *When it breaks* with the **actual** error
  string, because that string is what the reader will paste into a search box at 3am.
- **A capability without a bound.** Every new power arrives with its brake in the same document
  (Principle 13). "We will add limits later" is how trap #4 happens.
- **Trimming to fit.** Cutting an explanation because the day "is getting long" is the one edit this
  format forbids outright (Principle 17). **Split it into another part instead.**
- **A citation instead of an explanation.** Naming a paper is not teaching it, and this curriculum
  does not cite papers at all (§17.4.2). If the origin of an idea matters, say what it changed, in
  ordinary words, in the part that uses it.
- **The sentence built out of clauses.** A fragment with no verb, or four ideas joined by dashes,
  reads quickly to somebody who already knows the subject and reads as fog to somebody who does not.
  Write whole sentences and punctuate them (§18.1).
- **Solved reps.** `TODO(me)` stays `TODO(me)`. Depth is in the explanation, never in doing the
  learner's exercise for them.

### 17.9 Enforcement

`scripts/depth_check.py`, run as `./o depth [NNN]`, is the machine-readable half of this contract.
It fails on:

- a missing `parts/` directory;
- a part loose in `parts/` instead of inside a section folder;
- a day folder or section folder that is a bare number with no slug;
- a part whose section folder disagrees with the number in its filename;
- a filename that does not match `<section>.<subtopic>-<slug>.md`;
- a gap in the section or subtopic numbering;
- any of the ten required part sections missing or out of contract order (with the single exception
  in §17.4: *Line by line* is required exactly when the part holds a code block that needs one);
- a code block with no `Line by line:` walkthrough following it;
- a `level` outside `foundation` · `working` · `production`;
- a part carrying a `papers:`, `paper:` or `kind: paper` key, or a day carrying a `papers/` folder,
  all of which ADR-0006 removed from this contract and which are checked so they cannot return by
  accident;
- **any time estimate anywhere in a day folder** (Principle 17);
- **a billable cloud command that is not marked 🅿️ parked** (Principle 15 · Addendum 01);
- a hub that carries teaching, or whose §2 map does not link every part on disk;
- a `parts:` frontmatter count that disagrees with the directory;
- a missing `CHECKLIST.md`.

What it **cannot** check is whether an explanation is any good. That is what §17.8 is for, and it is
reviewed by reading. `docs/TRACKER.md` reports the part count of every written day, so a thin day is
visible from the progress table alone.

`scripts/trace.py` remains the ID-level check: it reads each hub against §14 and regenerates
`docs/TRACEABILITY.md` and `docs/CURRICULUM_INDEX.md`. **An open ID in a completed phase is a bug.**

---

## 18 · ✍️ The Style Guide

§17 says what a day must *contain*. This section says how it must *read*. Both are enforced by
review; the mechanical half is `./o depth`.

### 18.1 The register

1. **Storytelling is the default, not a flourish.** A scene before an abstraction, every time. The
   story section of a part carries **no jargon at all** — a person, a machine, a Saturday lost. The
   definition then hangs on that hook. A reader remembers the engineer whose liveness probe restarted
   every pod during a slow database query long after they have forgotten the phrase "cascading
   failure".
2. **Simple language first.** Every concept: plain words → concrete example → *only then* the
   terminology. If a twelve-year-old could not follow the first sentence, rewrite the first sentence.
   This is not dumbing down; it is putting the definition after the thing it defines.
3. **Define every term on first use — including your own terms from earlier days.** 237 days is long
   enough that Day 22 is genuinely forgotten by Day 190. Link the part that introduced it. "As we saw
   earlier" is not a link.
4. **Second person, present tense, active voice.** "You run `kubectl describe`, and the events block
   tells you the scheduler never placed it." Not "the pod is then described".
5. **No person names, no course or creator brand names.** This curriculum is self-contained and
   promotes nobody: never name an instructor, author, channel, academy, bootcamp or training company
   — in a lesson, a checklist, a docstring or a commit message. Naming the **tools** you actually use
   is required and unaffected (Kubernetes, Prometheus, MLflow, Terraform, uv, ruff…), as is citing a
   specification by its revision date and a project by its official documentation URL.

6. **Whole sentences, properly punctuated.** A fragment with no verb and a dash used as a
   general-purpose joint both read as speed to somebody who already knows the subject, and as fog to
   somebody meeting the idea for the first time. Use commas and full stops. Keep the dash for the
   one aside per paragraph that has earned it, and let a colon introduce a list rather than a
   thought.
7. **The plainest word that is still exact.** Where an everyday word means the same thing as a
   longer one, the everyday word wins: *use* over *utilise*, *starts* over *is initiated*, *find
   out* over *ascertain*. This rule stops at accuracy. A technical term that means something
   specific is kept and defined, because replacing it with a vague word is not simplification.
8. **A story anyone can stand inside.** The scene in a part's *The story* has to be one the reader
   has plausibly lived: a kitchen, a queue, a shared flat, a phone call, a school, a bus. Not a
   trade whose vocabulary is itself the obstacle, and not one that only makes sense in one country.
   If the scene needs explaining before it can illustrate anything, it is the wrong scene.

### 18.2 The scene format

For failures and motivations, use the four-beat scene. It is what a part's *The story* and *When it
breaks* sections are built from:

> 🎬 **The scene:** what you are doing.
> 😬 **The naive fix:** what everyone tries.
> 💥 **Why it fails:** the mechanism — not the symptom.
> 💡 **The insight:** the principle that survives after the details are forgotten.

### 18.3 Code and commands

9. **Every command is given in full.** `mkdir -p`, `uv add pkg==1.2.3`, the `docker run` with all its
   flags, the `kubectl` with its namespace, the check command. A reader should never have to infer
   "and now presumably I create a namespace".
10. **Every code block is followed by `**Line by line:**`** — every non-obvious token, and *why it is
   that line and not another*. Not a summary. **An unexplained line is a bug in the doc.** Blocks
   that are pure error output, a bare check command, or a Mermaid diagram are exempt.
11. **Every mechanism has a matching failure with the real error text**, reproduced verbatim.
   Paraphrasing a traceback is worse than omitting it — the reader searches for the string.
12. **`TODO(me)` stays unsolved.** The doc teaches; it never does the reps.
13. **Mermaid whenever the concept is spatial, sequential, or a state machine.** A request path, a
    rollout, a retry ladder, an incident timeline, an approval gate and a reconciliation loop all
    earn a diagram.
14. **Show the output, not just the command.** An operator's skill is reading output. A `kubectl
    describe` with no output pasted underneath has taught the reader to type, not to read.

### 18.4 Facts

15. **No invented facts.** Versions, flags, field names, quotas, API signatures and spec revisions:
    looked up live and dated, or explicitly `TODO`'d **with the exact lookup command**, never from
    memory. This curriculum cites no papers (§17.4.2), so there is no citation to get wrong.
16. **Tables for enumerable facts, prose for reasoning.** Never a table of one row.
17. **Emoji section markers, consistent and not decorative** — 🎬 🎯 📚 🛠️ 💥 🎤 ✅ 💡 🅿️ 📌 ⚠️ 🔒 📐.
18. **🅿️ = parked**: awareness-level, interview-ready, deliberately not built. A parked topic still
    gets a story and a production section; what it does not get is a build step.
19. **The interview paragraph is honest.** An answer you could actually defend, tied to what you
    built. "I have not run that at scale" is a legitimate sentence and a better one than a bluff.

### 18.5 The three things that are never written

20. **Never a clock.** Not "estimated hours", not "this takes an evening", not "quick", not "a short
    detour". `./o depth` fails the day on any of them (Principle 17).
21. **Never a trim.** If the day is getting long, it gets another part (§17.7). Cutting an
    explanation to fit is the one edit this format forbids outright.
22. **Never a command that needs a card.** A billable cloud command appears only as 🅿️ parked
    reading, marked as such on or immediately above the fence. `./o depth` fails the day otherwise.

### 18.6 The ritual

23. **Every day ends the same way** — the checklist, then the ledger snippets, then the commit
    message `day NNN: <title> — closes <IDs>`. The sameness is the point: the repo is the memory,
    not the chat, and a stranger — or a different CLI agent six months from now — has to be able to
    pick up from the last row of `docs/PROGRESS.md` alone.
