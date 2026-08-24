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
> `pyproject.toml` sets `link-mode = "copy"` because OneDrive refuses the hardlinks `uv` prefers and
> the install otherwise dies half-done with `os error 396`; and `.gitignore` excludes `data/`,
> `mlruns/` and model artifacts, because a synced folder full of regenerating binary artifacts is a
> slow-motion disaster. **Do not remove either.**

---

## 3 · The resource envelope

Establish these numbers on Day 0 and write them into `docs/PACKAGES.md`, because several later days
ask you to reason about them.

| Number | How to find it | Where it binds |
| --- | --- | --- |
| Total RAM | `wmic computersystem get totalphysicalmemory` (or Task Manager) | Day 6, Day 42, Day 126 |
| Free disk | `df -h` in Git Bash | Day 5, Day 30, Day 68 |
| Logical CPUs | `nproc` in Git Bash | Day 6, Day 44, Day 127 |
| WSL2 memory ceiling | your `%UserProfile%\.wslconfig` | Day 21 onward |

**The rule of thumb this plan uses:** leave 4 GB for Windows and your editor, and treat everything
else as the cluster's budget. If your machine has 16 GB, that is roughly 12 GB to spend, and the
profiles below fit inside it. If it has 8 GB, run one profile at a time and expect Day 126's local
model to be the tightest day in the plan — which is itself worth experiencing, because "the model
does not fit" is a real production conversation.

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

**Legal combinations on a 16 GB machine:** `core` + any two others. `core` + `cluster` + `obs` is
the busiest combination the plan asks for regularly (Phases 7–8) and is deliberately close to the
limit — Day 50 asks you to push it over.

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
