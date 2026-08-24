# 💸 Addendum 01 — The Zero-Cost Stack

> **This addendum wins over the master plan** on any question of tooling, hosting or paid services.
> Where §9 of the plan and this file disagree, this file is right and the plan gets amended.
>
> Status: **binding** · Created 2026-08-24 · Amendments go in `docs/CHANGELOG_PLAN.md`

---

## 1 · The rule

**No card on file. Ever. For anything.**

Not "a free trial that asks for a card". Not "the free tier of an account that has billing enabled".
Not "it is only a few cents". The rule is absolute for three reasons, in ascending order of
importance:

1. **A card is how a learning project becomes a bill.** A misconfigured autoscaler, a runaway
   retraining loop or an agent in a tool-calling loop is a normal thing to build wrong on the way to
   building it right. The cost of getting it wrong should be a lesson, not an invoice.
2. **Constraints are the curriculum.** Quota exhaustion, memory pressure, rate limits and "we cannot
   afford to keep those logs" are the actual daily texture of production operations. A budget-free
   environment removes the most interesting half of the job.
3. **It keeps the plan honest.** A curriculum that reaches for a managed service every time
   something gets hard teaches you to click buttons. Running Prometheus yourself teaches you what
   the button does.

`scripts/depth_check.py` enforces the mechanical half: a day document that tells you to run `aws`,
`az`, `gcloud`, `eksctl`, `doctl`, `databricks` or `sagemaker` fails the depth check unless the
command is marked 🅿️ parked on, or immediately above, its own line.

---

## 2 · What "free" means here, precisely

| Category | Allowed | Example |
| --- | --- | --- |
| **Open source, self-hosted** | ✅ Always. This is the default. | Prometheus, Grafana, Loki, MLflow, Argo CD, Qdrant |
| **Free tier, no card required** | ✅ Yes, and record the limits the day you use it | GitHub Actions on a public repo, GHCR public images, Gemini AI Studio key |
| **Free tier, card required** | ❌ No | Most cloud provider free tiers |
| **Free trial with an expiry** | ❌ No | Anything that becomes billable by elapsed time |
| **Local compute** | ✅ Yes, within §3's limits | Your laptop's CPU and RAM |
| **Rented compute** | ❌ No | Any GPU rental, any managed cluster |

**When a free tier disappears** — and one will, this plan runs for months — that is Principle 14: it
is an amendment, logged in `docs/CHANGELOG_PLAN.md`, before any day is edited. The local lane exists
precisely so that the curriculum survives a provider withdrawing a free model.

---

## 3 · The stack, layer by layer, with what it costs you

Cost is denominated in the units that actually bind: **RAM, disk, CI minutes, requests per minute
and requests per day.** Never dollars.

### 3.1 The always-on layer

| Tool | Role | Rough resident cost | Notes |
| --- | --- | --- | --- |
| `uv` + Python 3.12 | Environment and packaging | negligible | One binary owns the environment (Day 0). |
| `ruff`, `pytest` | The gate | negligible | Dev dependencies only. |
| Git + Git Bash | Version control and the shell every day is written for | negligible | Day 0. |

### 3.2 The platform layer — started per day, stopped after

| Tool | Role | Rough resident cost | First day |
| --- | --- | --- | --- |
| Docker Desktop / Engine | Container runtime | 2–4 GB with WSL2 | 21 |
| `kind` | A Kubernetes cluster in containers | ~1.5 GB for one node | 32 |
| Argo CD | GitOps reconciliation | ~400 MB in-cluster | 56 |
| Terraform | Infrastructure as code, against local + kind providers | negligible when idle | 52 |

> ⚠️ **Do not run the cluster and the full observability stack and a local model at once** unless
> you have the memory for it. §4 of `02_ADDENDUM_THE_MACHINE.md` gives the profiles.

### 3.3 The observability layer

| Tool | Role | Rough resident cost | First day |
| --- | --- | --- | --- |
| Prometheus | Metrics storage and query | ~500 MB, grows with retention | 62 |
| Grafana | Dashboards | ~200 MB | 66 |
| Loki + agent | Log storage and shipping | ~400 MB | 68 |
| OpenTelemetry Collector | The single telemetry seam | ~150 MB | 71 |
| Alertmanager | Routing and silencing | ~100 MB | 76 |
| k6 | Load generation | spiky by design | 84 |

**Retention is a cost decision and is taught as one.** Day 68 sets Loki's retention deliberately and
Day 70 sets trace sampling deliberately, because on a laptop the consequence of getting it wrong
arrives within a day rather than within a quarter — which makes it a better teacher than a cloud
bill.

### 3.4 The ML layer

| Tool | Role | Rough resident cost | First day |
| --- | --- | --- | --- |
| DVC, local remote | Data versioning | disk only | 87 |
| Pandera / Great Expectations | Data validation | negligible | 89 |
| Prefect or Dagster, local | Orchestration | ~300 MB | 93 |
| MLflow, local server | Experiments + registry | ~250 MB + artifact disk | 98 |
| scikit-learn / LightGBM | The model itself | CPU, seconds to minutes | 97 |
| Evidently | Drift and performance reports | negligible | 118 |

**The model is deliberately small.** A gradient-boosted tree on synthetic tickets trains in seconds
on a laptop CPU. That is the point: nothing about the *ops* should be waiting on a GPU, and a model
you can retrain in ten seconds is a model whose whole lifecycle you can exercise fifty times.

### 3.5 The LLM layer

| Lane | What it is | Bound by | First day |
| --- | --- | --- | --- |
| **Local** | Ollama with a small quantized model | your RAM and CPU | 126 |
| **Free hosted 1** | Gemini Flash-class, AI Studio key, `GOOGLE_GENAI_USE_VERTEXAI=FALSE` | per-project RPM/RPD, read from your own dashboard | 125 |
| **Free hosted 2** | Groq | RPM, and per-model RPD/TPM, per organization | 125 |
| **Free hosted 3** | OpenRouter models ending `:free` | RPM and RPD on the free floor | 125 |

**Three rules that are not negotiable:**

1. **Never invent a model name.** Free rosters change. The day that pins a model looks up the
   provider's current free list first and records model + date in `docs/PACKAGES.md`.
2. **An OpenRouter model id must end in `:free`.** The missing suffix silently selects a paid model.
   This is the single trap in the plan that can actually cost money, and it is linted from Day 125.
3. **Every model call path handles HTTP 429** with `retry-after` and backoff, then escalates
   honestly. Never fabricate a result to cover a rate limit (Principle 10). Day 132 builds it; Day
   134 breaks it on purpose.

### 3.6 The agent and tool layer

| Tool | Role | Bound by | First day |
| --- | --- | --- | --- |
| OpenTelemetry + OpenInference conventions | Agent tracing | disk | 181 |
| MCP Python SDK | The tool boundary | RAM per server | 200 |
| Qdrant, local container | Vector store | ~300 MB + index disk | 140 |

**Agents are budgeted in requests, not dollars.** `AGENT_DAILY_CALL_BUDGET` and `AGENT_MAX_STEPS`
are in `.env.example` from the start for a reason: an agent with no bound is trap #4, and the free
tier is exactly the right place to learn that lesson, because the punishment is a dead quota rather
than a dead budget.

### 3.7 Security and supply chain

| Tool | Role | First day |
| --- | --- | --- |
| Syft | SBOM generation | 15 |
| Grype / Trivy | Vulnerability scanning | 29 |
| Cosign | Signing and verification | 217 |
| SOPS + age | Encrypted secrets in git | 58 |
| sealed-secrets | Cluster-side secret decryption | 58 |
| Vault, dev mode | The dynamic-secret model, locally | 58 |
| Kyverno or OPA Gatekeeper | Admission policy | 59 |

All open source, all free, all the tools a real team uses.

---

## 4 · The parked list — what you read about and never run

These get a full teaching part with a story, a mechanism and a production section. What they do not
get is a step you execute. Every one is marked 🅿️ in the day document.

| Parked | Day | What you learn instead |
| --- | --- | --- |
| Managed Kubernetes (any vendor) | 32 | What the control plane does, by running one you own. |
| Managed model endpoints | 109 | The serving patterns, by building them. |
| Managed feature stores | 92 | What a feature store solves, and when a table is enough. |
| Managed vector databases | 140 | The operational surface — recall, latency, deletes — on a local one. |
| GPU rental and multi-GPU training | 128 | The operator's mental model, and honest limits about what you have not done. |
| Vendor observability SaaS | 71 | The collector, which makes the backend interchangeable. |
| Cloud cost consoles | 224 | Attribution and unit economics, computed from your own telemetry. |

**How to talk about a parked topic honestly:** *"I have not operated a managed GPU cluster. I have
operated a scheduler under memory pressure, and I know the questions I would ask: what is the
scheduling unit, what happens to a pod that cannot be placed, and who pays for the idle time."*
That answer is worth more than a bluff, and it is exactly what a good interviewer is listening for.

---

## 5 · The escape hatch, stated once

If you later have a budget, nothing in this plan is wasted and nothing has to be relearned.
Prometheus is Prometheus whether you run it or rent it. A Deployment manifest is the same in kind
and in a managed cluster. An SLO is arithmetic. The only things that change are who runs the
control plane and who sends the invoice — and having run it yourself first is the difference
between choosing a managed service and being managed by one.
