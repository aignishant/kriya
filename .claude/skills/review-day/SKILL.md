---
name: review-day
description: Review a written Kriya day against the half of the depth contract a script cannot check — whether the explanations are actually any good
argument-hint: [day-number]
---

# Review Day $ARGUMENTS against §17.8

`./o depth $ARGUMENTS` checks structure: sections present, in order, numbered correctly, no clocks,
no unmarked billable commands, every code block explained. It **cannot** check whether an explanation
is any good. That is this skill's job, and it is done by reading.

Run `./o depth $ARGUMENTS` **first**. If it fails, stop — fix the structure before reviewing prose.

---

## Step 1 — read the whole day, in order

Read `days/day-NNN-<slug>/LESSON.md`, then every part in numerical order, then `CHECKLIST.md`. Read
it as a learner would: cold, without the plan open, without assuming you remember Day 22.

## Step 2 — the ten failure modes (plan §17.8)

For each one, either say **"clear"** or quote the exact passage that fails it. Never a vague verdict.

| # | Failure mode | The test |
| --- | --- | --- |
| 1 | **Splitting without deepening** | Did each part *gain* a story, a mechanism, real failure text and a production section — or is it a long page cut into short ones? |
| 2 | **Summary in place of explanation** | Find every `Line by line:` entry that restates the code in English ("this sets the timeout") instead of explaining *why that line and not another*. Quote them. |
| 3 | **Stopping at the toy example** | Does every *In production* section say what changes at scale, under concurrency, or under real traffic? A section that just repeats the mechanism in longer words is a miss. |
| 4 | **Assuming the previous day** | Every term from an earlier day: is it defined here or **linked** to the part that introduced it? "As we saw earlier" is not a link. Check the first three paragraphs of each part especially. |
| 5 | **Code without failure** | Does every mechanism have a matching *When it breaks* with the **real, verbatim** error string? A paraphrased traceback is a fail — the reader searches for the string. |
| 6 | **A capability without a bound** | Does every part that introduces a write path, an autoscaler, a remediation, a tool or an agent action name its blast radius: worst case, who can trigger it, what bounds it? (§17.4.1 rule 3) |
| 7 | **Trimming to fit** | Is there a place where the explanation obviously stops early — a "we won't go into that here" with no forward link, a mechanism section shorter than its story? |
| 8 | **Solved reps** | Is every `TODO(me)` still unsolved? Did the document quietly do the learner's exercise for them? |
| 9 | **A citation** | Does any part name a paper, carry a `papers:`, `paper:` or `kind: paper` key, or sit beside a `papers/` folder? All of these were removed by ADR-0006. Provenance belongs in ordinary words, in the part that uses the idea. |
| 10 | **The sentence built out of clauses** | Read every part's first three paragraphs aloud. Count fragments with no verb, and dashes used where a comma or a full stop belongs. Quote the worst three and rewrite them. (§18.1 rule 6) |
| 11 | **The word that shows off** | Is there a longer word where an everyday one means the same thing, or a technical term used before it is defined? (§18.1 rule 7) |
| 12 | **A story nobody has lived** | Is every *The story* scene one the reader has plausibly been inside — a kitchen, a queue, a phone call — rather than a trade whose vocabulary is itself the obstacle, or one that only works in one country? Does it need explaining before it can illustrate anything? (§18.1 rule 8) |

## Step 3 — the three tests, per part

- **One-idea test.** Does any part use "also", "additionally" or "as well as" to introduce its second
  half? Name it and say where it should split.
- **Standalone test.** Pick the three parts furthest from the start. Could each be read cold? Name
  every unlinked prerequisite.
- **No-shortcut test.** Find every "for now, just accept that", "we'll cover this later", "don't
  worry about". Each one must link forward to a specific part. A deferred explanation must have an
  address.

## Step 4 — the ops-specific checks (§17.4.1)

- **Every API, flag and field** used: does the part name the official page checked, with a date?
  Spot-check two of them against the live docs. If one is wrong, say so loudly — an invented field is
  the worst defect this curriculum can ship.
- **Every version** installed: a real observed version with a date, or a `TODO` containing the exact
  lookup command? Is there a matching row in `docs/PACKAGES.md`?
- **Every new signal**: does the part say how you would alert on it, or explicitly that you would
  not and why?
- **Every cost**: stated in quota units — requests, tokens, RAM, disk, CI minutes?
- **The machine**: does the hub's §3 say which profile to start **and what to stop first**
  (Addendum 02 §4)? Does the day's resident memory fit alongside what earlier days left running?

## Step 5 — the reader simulation

Answer these as if you were the learner, using only what the day contains:

1. What is the **one sentence** this day exists to teach? Is it stated anywhere, or only implied?
2. Could you do the `CHECKLIST.md` demo command from the day alone, with no external search?
3. Which part is the **weakest**, and what single addition would fix it?
4. Which failure in *When it breaks* is the one you are actually most likely to hit? Is it first?
5. Is the §9 interview paragraph something a person could **say out loud** and defend, or is it a
   list of nouns?

## Step 6 — the verdict

Print exactly this shape:

```
day NNN — <title>
depth check:   PASS / FAIL
parts:         N across M sections, levels: <foundation×a, working×b, production×c>

BLOCKING (must fix before this day counts as written)
  - <file>: <what, with the quoted passage>

SHOULD FIX
  - <file>: <what>

STRONGEST PART:  <which, and why>
WEAKEST PART:    <which, and the one change that would fix it>
```

**Do not fix anything unless I ask.** This skill reports; it does not edit. A review that quietly
rewrites the thing it is reviewing is not a review.
