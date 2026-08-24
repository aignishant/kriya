# ADR-0004 — Eighty-four days of platform, observability and SRE come before the first model

- **Date:** 2026-08-24
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Related:** ADR-0001 (charter)

## Context

The learner's request named five subjects: MLOps, LLMOps, AIOps, AgenticOps, MCPOps. None of them
is Linux, containers, Kubernetes, CI, infrastructure as code, metrics, logs, traces, SLOs or
incident response — and yet this plan spends **Days 1–84** on exactly those, and does not train a
model until **Day 97** or make an LLM call until **Day 125**.

That is 36% of the plan before the subject the learner asked for. It is the most contestable
decision in the charter, so it gets its own record.

The case for it is not "eat your vegetables". It is that **the named subjects are not separable from
the foundation**, in a specific and checkable way:

| A day in the "real" curriculum | What it silently requires |
| --- | --- |
| Day 110 — the model is too slow | latency budgets, p99 versus mean, histograms, load testing, resource limits |
| Day 115 — data drift alerting | Prometheus data model, alert precision/recall, symptom-based alerting, on-call cost |
| Day 122 — the serving failure lab | cold starts, OOM kills, thundering herd, readiness probes, connection pools |
| Day 134 — the 429 storm | retries, backoff, idempotency, timeouts, circuit-breaking, queue depth |
| Day 163 — anomaly detection on live metrics | what a counter is, what `rate()` does, what seasonality looks like in *your* traffic |
| Day 175 — the remediator that made it worse | rollback, blast radius, RBAC, disruption budgets, change attribution |
| Day 195 — proving it was the agent | audit trails, workload identity, structured logs, correlation ids |

Every entry in the right-hand column belongs to Phases 1–8. A curriculum that teaches the left
column first has to hand-wave the right column, and hand-waving is how a learner ends up able to
recite "we monitor for drift" without being able to say what fires, to whom, or why it is not noise.

There is also a market observation worth stating plainly: teams hiring for MLOps and LLMOps roles
interview for ordinary production engineering and then ask about models. A candidate who can debug a
`CrashLoopBackOff`, read a p99 latency graph and write a runbook, and who has *also* built a
retraining gate, is hireable. The reverse — model lifecycle fluency with no platform underneath — is
the most common failure mode in this field, and it is visible in about four minutes of interview.

## Options considered

| Option | Pros | Cons |
| --- | --- | --- |
| **A. Start at MLOps on Day 1; teach infrastructure as needed** | Motivating; matches what was asked for. | "As needed" arrives mid-incident, which is the worst time. Produces someone who can follow an MLOps tutorial and cannot debug one. Rejected. |
| **B. A short foundation — two weeks — then MLOps** | A compromise; feels efficient. | Two weeks is enough for vocabulary and not for practice. The Kubernetes material alone needs the object model *and* the failure modes, which is where the value is and where two weeks runs out. |
| **C. A full foundation (Phases 1–8, Days 1–84), then the five threads in dependency order** | Every later day can assume real ground. The hardest ML/LLM days become tractable because they are ordinary distributed-systems problems in costume. | 84 days before the subject the learner asked for. Requires trusting the plan for months. |
| **D. Interleave: one foundation day, one ML day, alternating** | Keeps motivation up throughout. | Both threads become incoherent; a phase gate cannot mean anything; the dependency order becomes invisible, which was the whole point. |

## Decision

**We adopt Option C.** Phases 1–8 (Days 1–84) teach the production mental model, Linux, delivery and
CI, containers, Kubernetes twice over, infrastructure as code and GitOps, observability, and SRE
practice — against `pulse`, which exists from Day 3 as an ordinary web service.

The first model is trained on **Day 97**. The first LLM call is made on **Day 125**. AIOps begins on
**Day 159**, on telemetry the learner has generated and instrumented themselves.

Two design choices make the wait tolerable and honest:

1. **`pulse` exists from Day 3.** The foundation is not abstract: every platform concept is applied
   to the service that will later carry the model. Nothing is learned in a vacuum (Principle 5).
2. **Every phase has a demonstrated gate** (§13). Progress is visible and provable every eight to
   twelve days, not deferred to Day 97.

## Consequences

**Easier.** Days 85–236 can be written at full depth without stopping to explain what a pod is.
AIOps in particular becomes possible at all: it operates on telemetry the learner built in Phase 7
and alerted on in Phase 8, so "is this detector any good?" is a question they can actually answer.

**Harder.** Motivation across 84 days that do not mention AI. The plan mitigates this with `pulse`
from Day 3, phase gates every eight to twelve days, and fifteen failure-lab days where breaking
something is the entire subject.

**Committed to.** Not moving ML material earlier when it gets tempting. If Phase 7 feels slow, the
answer is the next part, not a jump to Day 85.

## What would make us change our minds

- If a learner reaches Day 84 and cannot pass the Phase 8 gate — publish an SLO, alert on symptoms,
  run a staged incident, write the postmortem — the foundation phases are too shallow, not too long,
  and need more days rather than fewer.
- If Days 85–122 turn out **not** to lean on Phases 1–8 in practice — if the MLOps days can be read
  cold by someone who skipped them — then the dependency claim in this ADR is wrong and the ordering
  should be revisited.
- If the plan is abandoned before Day 84 twice, the failure is motivational rather than technical,
  and the fix is an earlier visible `pulse` milestone, not a shorter foundation.

## Cold read

*(Re-read this with a reviewer's hat on, later, and sign here.)*
