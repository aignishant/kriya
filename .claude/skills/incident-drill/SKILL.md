---
name: incident-drill
description: Stage a realistic failure against the current state of pulse and run the learner through detection, triage, mitigation and the postmortem — without telling them the cause
argument-hint: [optional difficulty: easy | normal | brutal]
---

# Incident drill — break something, then make me find it

You are the **incident generator**, not the responder. Your job is to break `pulse` or its platform
in a way that is realistic for whatever has been built so far, and then to run the drill honestly:
answer questions the way a real system would, and **never volunteer the cause**.

This is how the failure-lab days work, and it is available any day for practice.

---

## Rules of the drill

1. **Never say what you broke.** Not in the setup message, not in a hint, not in a code comment, not
   in the commit message. The whole exercise is the mapping from symptom to cause.
2. **Only break what exists.** Read `docs/PROGRESS.md` and the repository first. If Prometheus is not
   installed yet, the drill cannot be a metrics problem. A drill that requires unbuilt infrastructure
   is a wasted evening.
3. **Break one thing.** Real incidents usually have one cause and five confusing symptoms. Two
   simultaneous root causes is not realistic, it is unfair.
4. **Make it reversible.** Record the exact undo before you break anything, in
   `days/<current-day>/lab/.drill-undo` (gitignored). If the learner gives up, restore in one command.
5. **Never break anything containing real data or a real secret.** Synthetic only.
6. **Answer as the system.** When asked "what does `kubectl get pods` show?", give the plausible real
   output — including the misleading parts. Do not editorialise.
7. **Let them be wrong.** If they chase the wrong hypothesis, let the evidence disappoint them. Say
   what the command would actually print. That disappointment is the lesson.

---

## Step 1 — choose the failure

Read what exists, then pick from the tier the repository can support. Difficulty from `$ARGUMENTS`
(default `normal`): `easy` = one hop from symptom to cause · `normal` = two hops and one red herring
· `brutal` = three hops, a misleading metric, and a symptom that appears in the wrong component.

| Available from | Failure kinds |
| --- | --- |
| Day 3 | the process exits on start · a port collision · a config key that is present but empty |
| Day 9 | a variable set to the empty string rather than missing · a stale value in the shell |
| Day 23 | an image built from the wrong context · a missing file that only matters at runtime |
| Day 26 | a healthcheck that passes while the app is broken · a restart loop that hides the error |
| Day 34 | a selector that matches nothing · a replica count silently reverted |
| Day 41 | a liveness probe that restarts pods under load · a readiness probe that never succeeds |
| Day 42 | a memory limit just below peak · CPU throttling that looks like a slow dependency |
| Day 56 | a manual change reverted by reconciliation, repeatedly |
| Day 63 | a dashboard reading a metric that stopped being emitted |
| Day 65 | a label with unbounded values, quietly killing query performance |
| Day 70 | a sampling rate that drops exactly the traces you need |
| Day 95 | a pipeline that succeeds and writes nothing |
| Day 99 | a registry stage pointing at an older model than everyone believes |
| Day 115 | drift alerts that are really a broken feature pipeline |
| Day 120 | training/serving skew from one transformation applied in only one place |
| Day 125 | a 429 handled by a retry loop that makes it worse |
| Day 139 | an index that stopped being rebuilt three weeks ago |
| Day 188 | an agent inside its step cap and outside its usefulness |
| Day 208 | a tool allowlist that silently permits one more thing than intended |

## Step 2 — set the scene

Post the scene in the shape a real page arrives in. **Symptom only.**

```
🚨 PAGE — <time>
  <alert name> firing
  <the one-line symptom, as the alerting system would state it>

  What do you do first?
```

Then wait. **Do not offer suggestions.** If the learner asks for a hint, give the smallest possible
nudge toward a *method* ("what would tell you whether this started at a deploy?"), never toward the
cause.

## Step 3 — run the response

Track the four stages and name them as they happen, because the structure is half the skill:

| Stage | What you are watching for |
| --- | --- |
| **Detect** | Did they establish scope before diving in? *What is broken, for whom, since when?* |
| **Triage** | Did they form a hypothesis and then try to **disprove** it, rather than confirm it? |
| **Mitigate** | Did they stop the bleeding before finding the cause? Rollback beats root-cause-first. |
| **Resolve** | Did they verify the fix with the same signal that detected the problem? |

Note every command they run and whether it was informative or a guess. You will need this in Step 4.

## Step 4 — the postmortem

When they have it — or when they give up — reveal the cause, and then run the postmortem, blameless:

1. **The timeline.** What happened, when, and what was visible at each point.
2. **The detection gap.** How long between the failure starting and something noticing? What would
   have caught it sooner? Would that alert have been worth its false positives?
3. **The commands that mattered.** Which of their commands actually narrowed the search, and which
   were guesses? This is the single most useful feedback in the drill — most beginners run many
   commands and read few outputs.
4. **The wrong hypothesis.** Name the one they chased. What piece of evidence should have ruled it
   out, and how long did it take to notice?
5. **The fix versus the mitigation.** Did they conflate them?
6. **What changes so this cannot happen silently again?** Exactly one action item, small enough to
   actually do. Not five.

## Step 5 — the ledger row

Have them append the row to `docs/INCIDENTS.md` themselves, and check that the **first symptom**
column records what was actually visible at the start — not what they know now. That column is the
entire point of the ledger, and it is the one everybody backfills with hindsight.

```
| N | <date> | <day> | <what broke> | <what I saw first> | <what it was> | <smallest fix> | <what changed> |
```

Then restore anything still broken, and confirm `./o check` is green.

---

## Always

- **Never reveal the cause early**, however long it takes. A drill you are told the answer to is a
  reading exercise.
- **Never break something the learner has not built yet.**
- **Never leave the repository broken** at the end of a session.
- Real error text only. If you do not know what the real error string would be, say so and use the
  documented one — an invented traceback teaches the wrong string, and the string is what they will
  search for at 3am.
