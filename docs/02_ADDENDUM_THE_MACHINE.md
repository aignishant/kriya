# 💻 Addendum 02 — The Machine You Will Actually Use

> **This addendum wins over the master plan** on anything to do with the local environment, the
> shell, resource profiles and what may be running at once.
>
> Status: **binding** · Created 2026-08-24 · Amendments go in `docs/CHANGELOG_PLAN.md`

---

## 1 · The premise

This curriculum is written for **one ordinary laptop**, with **no GPU** and **no cloud account**,
running **Windows 11**, and it treats that as part of the subject rather than as a limitation to
apologise for.

A single machine cannot run a Kubernetes cluster, Prometheus, Grafana, Loki, an OpenTelemetry
collector, MLflow, Postgres, Qdrant and a local language model at the same time. Neither can a
production node, which is why requests, limits, eviction and scheduling exist — so the constraint
does not merely permit the lesson, it *is* the lesson. Day 42 (requests and limits) and Day 50
(resource pressure) land very differently when you have already watched your own machine swap.

---

## 2 · Windows, WSL2 and the shell

**Every command in every day document is written for Git Bash**, which installs with Git for
Windows. `days/README.md` carries the PowerShell translation table for the handful of places it
matters.

**WSL2 is required from Day 21**, because Docker Desktop on Windows uses it and because everything
container-shaped behaves correctly there and strangely without it. The relevant facts:

| Fact | Consequence |
| --- | --- |
| WSL2 runs a real Linux kernel in a lightweight VM | Container and cluster behaviour matches Linux, which is what every doc you read assumes. |
| WSL2 claims memory dynamically and returns it reluctantly | Set a ceiling in `.wslconfig` (Day 21), or Docker will slowly eat the machine. |
| Filesystem performance across the Windows/WSL boundary is poor | Keep container build contexts small. This is why Day 24's `.dockerignore` matters more here than on Linux. |
| Windows Home supports WSL2 and Docker Desktop | No edition upgrade is needed. |

> ⚠️ **This repository lives under OneDrive.** Two consequences, both already handled:
>
> `pyproject.toml` sets `link-mode = "copy"`. By default `uv` hardlinks packages out of its cache
> into `.venv`, and when OneDrive's Files On-Demand has turned a cached file into a cloud
> placeholder, hardlinking it fails part-way through an install with `os error 396` — *"the cloud
> operation cannot be performed on a file with incompatible hardlinks"* (reported upstream as
> astral-sh/uv#7906 and #9721; a related path-traversal case is #19616). **Measured on this machine
> on 2026-08-24, hardlinking worked** — the failure depends on the sync state of the moment, which
> makes it intermittent and environmental rather than certain. `copy` costs a few hundred
> milliseconds and removes the class. Day 0 part 2.2 is about exactly this judgement call.
>
> And `.gitignore` excludes `data/`, `mlruns/` and model artifacts, because a synced folder full of
> regenerating binary artifacts is a slow-motion disaster. **Do not remove either.**

---

## 3 · The resource envelope

Establish these numbers on Day 0 and write them into `docs/PACKAGES.md`, because several later days
ask you to reason about them.

| Number | How to find it | Where it binds |
| --- | --- | --- |
| Total RAM | `(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory` in PowerShell | Day 6, Day 42, Day 126 |
| Free disk | `df -h .` in Git Bash | Day 5, Day 30, Day 68 |
| Logical CPUs | `nproc` in Git Bash | Day 6, Day 44, Day 127 |
| WSL2 memory ceiling | your `%UserProfile%\.wslconfig` | Day 21 onward |

> ⚠️ `wmic` is deprecated and absent on current Windows 11 builds — it returns nothing rather than
> failing loudly, which is its own small lesson. Use the PowerShell form above.

### 3.1 The reference machine

Measured on **2026-08-24**, Day 0. Every resource claim in this plan is calibrated against these
numbers, not against a hypothetical developer laptop:

| | Observed |
| --- | --- |
| Total RAM | **11.7 GiB** (12 612 919 296 bytes) |
| Logical CPUs | **4** |
| Free disk | **44 GB** of 118 GB |
| OS | Windows 11 Home Single Language |
| GPU | none |

**The rule of thumb this plan uses:** leave roughly **4 GB** for Windows, the browser and your
editor, and treat what is left as the platform's budget. On the reference machine that is
**about 7.5 GB** — not the 12 GB a 16 GB laptop would give you.

**Four cores is the tighter constraint, and it is the one people miss.** Memory pressure announces
itself (a container is `Killed`, exit 137, Day 30); CPU contention just makes everything slower and
lies to you about which component is slow. A `kind` control plane, a Prometheus scraping every 15
seconds and a model doing inference will contend for the same four cores, and the resulting latency
graph will look exactly like a slow dependency. Day 50 and Day 110 both depend on you having felt
this.

If your machine differs, **re-measure and write your own numbers into `docs/PACKAGES.md`** — the
profiles in §4 are stated in GB so you can do the arithmetic for your own hardware.

---

## 4 · The profiles — what may run at once

Every day's `## §3 Setup — run this` states which profile it needs **and what to stop first**. There
is never a single compose file that starts everything, because that is how you learn nothing about
resource pressure except that your laptop is slow.

| Profile | Contains | Roughly | Used by |
| --- | --- | --- | --- |
| `core` | `pulse` + Postgres | ~700 MB | Days 3–20, and always |
| `obs` | Prometheus, Grafana, Loki, OTel Collector, Alertmanager | ~1.5 GB | Days 61–84, 118, 159–178 |
| `cluster` | kind (one node) + ingress | ~1.5 GB | Days 31–60 |
| `ml` | MLflow + orchestrator | ~600 MB | Days 87–122 |
| `llm` | Ollama + Qdrant | ~1 GB idle, much more while generating | Days 126–158 |
| `agents` | MCP servers + agent runtime | ~400 MB | Days 179–214 |

**Legal combinations on the reference machine (~7.5 GB of budget, 4 cores):**

| Combination | Memory | Verdict |
| --- | --- | --- |
| `core` | ~0.7 GB | always on |
| `core` + `cluster` | ~2.2 GB | comfortable (Phases 4–6) |
| `core` + `obs` | ~2.2 GB | comfortable (Phases 7–8 before the cluster) |
| `core` + `cluster` + `obs` | ~3.7 GB | **fits on memory, contends on CPU** — the busiest combination the plan asks for regularly, and deliberately close to the line. Day 50 asks you to push it over. |
| `core` + `ml` | ~1.3 GB | comfortable (Phases 9–11) |
| `core` + `llm` | ~1.7 GB idle, **much more generating** | the tight one. Stop everything else first. |
| `core` + `cluster` + `obs` + `llm` | — | **do not.** This is the combination that swaps. |

**Three rules that follow from four cores rather than from memory:**

1. **Never benchmark with the observability stack starting up.** Prometheus' first scrapes and
   Grafana's provisioning will eat a core, and the p99 you measure will be your own laptop.
2. **Stop the cluster before Day 126's local model.** `kind` idles at real CPU cost, and inference
   on four cores is slow enough already — which is the point of that day.
3. **One profile per concern, started and stopped deliberately.** `docker compose --profile <name>
   up -d` and `down`, every single day. This is a habit, not a suggestion.

**When it does not fit** — and it will not, at least once — that is a capacity incident on your own
infrastructure. Log it in `docs/INCIDENTS.md`. What you saw first, what it actually was, what you
changed. This is not a joke: a real operator's instinct for "the machine is out of memory" comes
from exactly these moments, and yours will be cheaper than most.

---

## 5 · The no-GPU position, stated honestly

You will not train a large model and you will not serve one at speed. What you will do:

- **Run a small quantized model locally** (Day 126) and feel the latency. Slow inference is a
  design constraint you can experience rather than read about.
- **Learn the GPU operator's mental model** (Day 128) — what a GPU changes about scheduling,
  memory, batching, utilisation and cost — as a 🅿️ parked topic with a full teaching part.
- **Use free hosted APIs** for anything that needs a capable model, inside their rate limits, which
  is itself the LLMOps lesson (Days 125, 130, 132).

**What to say about this in an interview:** *"I have not operated GPU infrastructure. I have operated
an inference path against three providers with different rate limits, built the routing and the
backoff, and measured what a cache hit was worth. The GPU questions I would ask on day one are: what
is the batching strategy, what is the KV cache eviction policy, and what is our utilisation."* That
is an honest and strong answer. A bluff is neither.

---

## 6 · Reset drills

Two commands that should stop feeling scary, both introduced early on purpose:

```bash
kind delete cluster --name "$KIND_CLUSTER_NAME"   # Day 32 — the cluster is disposable
docker system prune -a --volumes                  # Day 30 — so is everything in it
```

**Line by line:** `kind delete cluster` destroys the whole local control plane and its nodes; the
`--name` flag matters because you will eventually have more than one and deleting the wrong one is a
lesson nobody needs twice. `docker system prune -a --volumes` removes every stopped container, unused
image, network and **volume** — `--volumes` is the flag that also deletes data, which is why it is
listed here rather than reached for casually.

Being able to destroy and rebuild the environment in two commands is what makes the GitOps lesson
(Day 56) land: if the repository is the source of truth, deleting the cluster is an inconvenience
rather than an incident. Practise it before you need it.
