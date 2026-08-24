# ADR-0003 — Zero cost, local-first, open-source only; managed services are parked

- **Date:** 2026-08-24
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Related:** ADR-0001 (charter) · Addendum 01 (the zero-cost stack) · Addendum 02 (the machine)

## Context

Operations is the discipline most entangled with spending money. Almost every tutorial for the
subjects in this plan begins by creating a cloud account, and a large fraction of the material is
really product documentation for a specific vendor's console.

Three facts about this learner's situation:

| Fact | Consequence |
| --- | --- |
| No budget for infrastructure | Any plan requiring rented compute stalls at the first paid step. |
| One laptop, no GPU, Windows 11 | The environment is finite in a way a cloud account is not. |
| The plan runs for months | Any free trial with an expiry becomes a broken day later. |

And one about the subject itself: **a learning system is exactly the kind of system that runs away
with cost.** A misconfigured autoscaler, a retraining loop with no gate, an agent in a tool-calling
loop — these are normal things to build wrong on the way to building them right. Attaching a payment
method to that process converts a lesson into an invoice.

There is also a pedagogical argument that is stronger than the financial one. Clicking "create
cluster" teaches you that a button exists. Running a control plane, watching a pod get evicted under
memory pressure, and deciding what telemetry is worth keeping on a machine that cannot keep it all
teaches you what the button does — and a person who knows that can use any vendor's button, while
the reverse is not true.

## Options considered

| Option | Pros | Cons |
| --- | --- | --- |
| **A. Use a cloud free tier** | Closest to a real employer's environment; managed services work. | Every meaningful free tier requires a card. Expiring credits break days months later. Vendor-specific consoles date fast. |
| **B. Local-first, with a small paid budget for the hard parts (GPU, managed cluster)** | Unblocks GPU serving and multi-node clusters. | Reintroduces the runaway-cost hazard exactly where it is most likely — a learner's first autoscaler. And "small budget" is not a stable category. |
| **C. Zero cost, absolutely: open source self-hosted, free tiers that need no card, local compute; managed and GPU topics 🅿️ parked with full teaching parts** | No hazard, no expiry, no vendor lock. The free version of the observability and ML stack *is* the production version. Constraints become curriculum. | Cannot demonstrate GPU serving or multi-node cluster operation. Requires honesty about that gap. |
| **D. Option C, but skip the parked topics entirely** | Shorter. | Produces a learner who cannot hold a conversation about GPU scheduling or managed services at all. Worse than a learner who can say "I have not run that, and here is what I would ask". |

## Decision

**We adopt Option C.** The rule is: **no card on file, ever, for anything.**

1. Open source, self-hosted is the default: Prometheus, Grafana, Loki, OpenTelemetry, MLflow,
   Argo CD, Terraform, Qdrant, Kyverno, Vault-in-dev-mode.
2. Free tiers are allowed **only** where signup requires no payment method: GitHub Actions on a
   public repository, GHCR public images, Gemini AI Studio keys, Groq, OpenRouter `:free`.
3. The Kubernetes cluster is local (`kind`), disposable, and rebuilt on purpose.
4. Models are small and free: a gradient-boosted tree on synthetic tickets, a quantized local LLM,
   and three free hosted lanes with real rate limits.
5. Managed services, GPU infrastructure, multi-node clusters and vendor observability platforms are
   **🅿️ parked**: a full teaching part with a story, a mechanism and a production section, and no
   build step.
6. Budgets throughout the plan are denominated in **RPM, RPD, RAM, disk and CI minutes** — never
   dollars.
7. The rule is enforced mechanically: `scripts/depth_check.py` fails a day containing an unmarked
   `aws` / `az` / `gcloud` / `eksctl` / `doctl` / `databricks` / `sagemaker` command.

## Consequences

**Easier.** No expiry, no surprise bill, no vendor drift in the material. Resource pressure is felt
directly and early, which makes Days 42, 50 and 68 land harder than they would with elastic
infrastructure. The tools learned are the ones real teams run.

**Harder.** The machine is the bottleneck (Addendum 02): profiles must be started and stopped
deliberately, and the busiest combination the plan asks for is close to a 16 GB limit on purpose.

**Accepted gap.** No demonstrated experience of GPU serving, multi-node cluster operation, or a
specific vendor's managed platform. The plan's position is that this is better stated honestly than
faked — and §5 of Addendum 02 gives the exact wording for saying so in an interview.

**Committed to.** Amending the plan (Principle 14) rather than paying, if a free tier disappears.
The local model lane exists so the curriculum survives that.

## What would make us change our minds

- If two of the three free hosted model lanes disappear, the LLMOps phases lose their rate-limit and
  routing material, and Addendum 01 §3.5 needs rewriting around the local lane — an amendment, not a
  credit card.
- If a day cannot be taught at all without rented compute — not merely taught less richly — that day
  needs re-scoping in the day map, with its own ADR.
- If parked topics exceed roughly a fifth of the plan, the zero-cost constraint has started removing
  the curriculum rather than shaping it.

## Cold read

*(Re-read this with a reviewer's hat on, later, and sign here.)*
