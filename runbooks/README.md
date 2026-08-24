# 📕 runbooks/ — the 3am documents

**One file per alert. No exceptions.** By the Phase 8 gate (Day 84), every alert that can page a
human has a runbook here, and an alert without one is a bug in the alert.

The first runbook is written on **Day 79**. `./o runbooks` lists them all.

---

## Why an alert without a runbook is a bug

An alert is a promise that a human should do something. If nobody wrote down what, the promise is
empty and the alert is noise — and noise is not neutral. It trains the person on call to ignore the
next one, which is how a real outage gets a nineteen-minute head start.

The test is not "could I figure this out?" — of course you could, you built it. The test is:
**could someone who has never seen this service act on this document, at 3am, half asleep, with no
context?**

## The shape of a runbook

```markdown
# <ALERT_NAME>

**Severity:** page | ticket        **Owner:** <team or person>
**Alert query:** <the exact PromQL or rule that fires this>

## What this means in one sentence
<Plain language. No jargon. What is the user actually experiencing?>

## Is it real? (30 seconds)
<The one or two commands that confirm this is not a false positive. With their expected output.>

## Immediate mitigation
<Stop the bleeding. Rollback, scale, disable the feature, drain the node.
 This section comes BEFORE diagnosis, deliberately.>

## Diagnosis
<Ordered. Each step: the command, what you are looking for, and what each answer means.
 Never "investigate the logs" — say which logs, filtered how, and what a bad line looks like.>

## Escalate when
<The specific condition. Not "if it's serious". A condition someone can evaluate at 3am.>

## Known false positives
<Every time this fired and was nothing. This section is what makes the runbook trustworthy.>

## Related
<Links: the dashboard, the ADR, the past incidents in docs/INCIDENTS.md>
```

## The four rules

1. **Mitigation before diagnosis.** At 3am you stop the bleeding first and understand it in the
   morning. A runbook that opens with "first, understand the root cause" has been written by someone
   who was awake.
2. **Every step has expected output.** "Run `kubectl get pods`" is not a step. "Run `kubectl get
   pods -n pulse` — every pod should be `Running` with restarts under 3; a `CrashLoopBackOff` here
   means go to step 4" is a step.
3. **Update it after every incident.** A runbook that did not help gets fixed the same week, while
   you remember why. The postmortem action item is usually "fix the runbook", and it is usually the
   most valuable one.
4. **Known false positives are mandatory.** They are what turns a document into something a
   responder believes. A runbook that has never been wrong has never been used.

## Testing a runbook

The only real test is a stranger following it. Failing a stranger, `/incident-drill` is the next best
thing: stage the failure the runbook covers, then follow **only** the runbook. Everywhere you had to
think, the runbook is missing a line.

Day 83 (game days) makes this a scheduled habit rather than an intention.
