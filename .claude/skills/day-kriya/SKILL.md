---
name: day-kriya
description: Generate the hub, the parts/ sub-documents, the lab scaffold and the checklist for a given day of the Kriya plan (MLOps · LLMOps · AIOps · AgenticOps · MCPOps)
argument-hint: [day-number]
---

# Generate Day $ARGUMENTS of the Kriya plan (v1.1.0 — hub + `parts/`)

> **Read `docs/00_MASTER_PLAN.md` §17 before writing a single line.** It is the depth contract this
> skill implements. This skill is the procedure; §17 is the standard.

## The three commitments (§17.1 — everything below follows from these)

1. **One idea per document.** If it needs "also" to introduce its second half, it is two documents.
2. **No clocks.** Never write a time estimate, a duration, an "estimated hours" field, or a pace —
   not in frontmatter, not in prose, not in the checklist. A topic is finished when it is
   understood, and a reader may spend five sittings on one part. **Never trim an explanation because
   the day is getting long — split it into another part instead.**
3. **Zero to production, in one document.** Open where a reader who has never heard of the idea can
   stand. End where a professional stands: the real-system version, what breaks at scale or under
   concurrency, what a senior reviewer says, **what you would be paged for**, what an interviewer
   probes.

---

## Step 1 — gather

1. Read the plan: **§2** (principles), **§5 + §5.1** (the version policy and the four traps),
   **§14** (the day map — the authoritative ID list for day $ARGUMENTS), **§17** (the depth
   contract), **§18** (the style guide). Collect every ID slotted to day $ARGUMENTS, the phase
   theme, and the gate that phase feeds.
2. Read `docs/PROGRESS.md`. **Confirm $ARGUMENTS is exactly one more than the last row.** If it is
   not, say so and stop — do not generate out of order (plan §15: never skip, merge or reorder a day
   without an ADR).
3. Read `docs/TRACEABILITY.md`. Any open ID from a completed phase is a bug — report it, don't paper
   over it.
4. Read the previous day's `days/day-NNN-<slug>/LESSON.md` and `CHECKLIST.md`. If the checklist has
   unticked boxes, warn me and ask before proceeding. Build on the code the previous days told the
   learner to write in `pulse/`, `platform_ops/`, `deploy/` and `pipelines/` — never duplicate it,
   never rewrite it.
5. Read the addenda that bind this day: `01_ADDENDUM_ZERO_COST_STACK.md` for anything that installs,
   hosts or calls a model, and `02_ADDENDUM_THE_MACHINE.md` §4 for which profile the day needs and
   what must be stopped first.
6. **Look at what `pulse` actually is right now.** Read the real files, not your memory of them. A
   day that instruments an endpoint that does not exist is a day that wastes an evening.

## Step 2 — verify reality before you write (Principles 7, 8, 14)

7. **Never invent an API, a flag or a field.** For every `kubectl` field, PromQL function, Terraform
   argument, manifest key and library symbol the day will use, fetch the live official page and note
   the URL and the date. The part that uses the symbol states the page checked. If the live docs
   disagree with the plan, **stop and propose an amendment** — do not silently adapt.
8. **Never invent a version.** For every tool the day installs, read the version live (`curl -s
   https://pypi.org/pypi/<pkg>/json`, the project's releases page, `uv pip compile` for a resolved
   answer). Record tool, version and date in `docs/PACKAGES.md`. If a lookup fails, leave a
   `TODO(<exact command>)` — never a guess.
9. **Never invent a model name.** Any day that names a model looks up the provider's current free
   list first (Gemini AI Studio · console.groq.com/settings/limits · openrouter.ai filtered to
   `:free`) and records model + date. Free rosters move.
10. **Never invent a citation, and never go looking for one.** Every part you write declares
    `papers: []`, and **this skill does not create a `papers/` folder or a paper document** — that
    is deliberate (§17.4.2). A plausible title, year and venue cost nothing to emit and are
    expensive to catch, so research is written up only when I ask for it, by somebody who has read
    the paper. If a day's mechanism plainly comes from published work and you think it deserves a
    paper document, **say so at the end and stop there** — do not write one, and do not name the
    paper in a part.
11. **MCP days:** check the specification revision on the spec page before writing. If it moved,
    amend first (Principle 14).
12. **Cost check.** If the day would tell the reader to run anything billable, it is wrong. Rework
    it to the local equivalent, or park the topic 🅿️ with a full teaching part and no build step.

## Step 3 — plan the split (do this before writing prose)

13. List the day's subtopics. Group them into **sections** that share one mental model — usually one
    section per curriculum ID, per lifecycle stage, or per phase of a mechanism. State the grouping
    in the hub; an unexplained numbering is a bug.
14. Split by **idea boundaries, never by length or pace** (§17.7). There is no target part count.
    Four parts if the subject needs four; twenty-two if it needs twenty-two. `setup` days split per
    tool or file; `lab` days per mechanism → behaviour → edge case → failure mode → production use;
    `concept` days one claim per part; `incident` days one stage per part; `gate` days one acceptance
    criterion per part.
15. **Every day gets at least one part whose subject is a deliberate failure.** On the fifteen days
    titled *"the … failure lab"*, that is the entire day.
16. Assign each part a `level` — `foundation` (knows what it is), `working` (can use it on their own
    problem), `production` (knows what changes in a real system). A day should climb. A day that is
    all `foundation` is a tutorial; a day opening at `production` has skipped the reader.
17. Apply the **one-idea test**, the **standalone test** and the **no-shortcut test** (no "for now,
    just accept that" without a forward link) to each planned part *before* writing.
18. **Print the planned part list to me before writing.** If it looks thin, I will say so.

## Step 4 — write the parts

> Path: `days/day-NNN-<day-slug>/parts/<NN>-<section-slug>/<section>.<sub>-<slug>.md`

19. **Name the day folder `days/day-NNN-<slug>/`** — the number zero-padded to **three** digits, then
    a kebab-case slug of 1–4 words taken from the hub's `title` with articles dropped:
    `days/day-023-the-dockerfile-for-pulse/`. A number alone is an address, not an answer, and 237 of
    them are indistinguishable in a file tree. The number stays the identity — `./o`,
    `depth_check.py`, `tracker.py` and `trace.py` all resolve a day by number and accept any slug.
20. **One folder per section**, two zero-padded digits **then a kebab-case slug of 1–3 words saying
    what the section is about** — `parts/01-what-a-probe-is/`, `parts/03-failure-modes/`. Take the
    slug from the section's heading in the hub's §2 map. A bare `parts/01/` is rejected by `./o
    depth`. Every part lives inside its section's folder; none is ever loose in `parts/`, and the
    folder number must match the number before the dot in the filename.
21. One file per subtopic, named `<section>.<subtopic>-<kebab-slug>.md`. The slug says what the part
    *teaches*, never where it sits. Numbering starts at `1` and has no gaps.
22. **Links are relative to the part's own folder**: a sibling in the same section is
    `1.2-<slug>.md`; a part in another section is `../01-<slug>/1.5-<slug>.md`; the hub is
    `../../LESSON.md`. `prev` and `next` in the frontmatter use the same form. The hub's §2 map links
    the full path from the day folder: `parts/01-<slug>/1.1-<slug>.md`.
23. Every part carries all ten sections of §17.4, **in this order**:
    - **frontmatter** — `day`, `part`, `title`, `ids`, `level`, `papers`, `prerequisites`, `prev`,
      `next`. **`papers` is always `[]` in a generated day** (step 10). **No duration field of any
      kind.**
    - **One-line answer** — the claim in one sentence, before anything else.
    - **The story** — a concrete scene first: a person, a machine, a failure, a decision. **No jargon
      at all** in this section. This is the hook the definition hangs on.
    - **The idea in plain language** — the concept assuming zero prior knowledge; every term defined
      on first use, **including terms from earlier days**, with a link to the part that introduced
      them. No code.
    - **Why Kriya needs it** — the concrete later day that breaks without this. Never "this is
      important".
    - **The mechanism** — how it actually works: runnable code, the manifest, the protocol exchange
      written out, or the diagram. Nothing skipped as "obvious". **Paste the real output**, not just
      the command.
    - **Line by line** — a `**Line by line:**` list **immediately after each code block**: every
      non-obvious token, and *why that line and not another*.
    - **When it breaks** — the **real** error text verbatim (the traceback, the `kubectl describe`
      events block, the HTTP status, the PromQL error, the 429 body), what it means, the smallest fix.
    - **In production** — the real-system version: what a professional writes instead of the teaching
      version, what degrades at scale or under concurrency, the failure that only shows with real
      traffic, the review comment a senior engineer leaves, **the signal you would alert on**, and
      the interview question that finds out whether you have actually used it. **Not optional. This
      is the section that makes the document professional rather than introductory.**
    - **Check yourself** — one command to run now, one question to answer out loud.
24. Apply **Kriya's six additional part rules** (§17.4.1): name the official page checked, with a
    date · state the verified version or a `TODO` with the lookup command · **name the blast radius**
    of any new capability (worst case, who can trigger it, what bounds it) · **say how you would
    alert** on any new signal, or why you would not · **state the cost in quota units** (requests,
    tokens, RAM, disk, CI minutes; `0` is an answer) · **never invent a citation**.
25. Mermaid diagram whenever the concept is spatial, sequential, or a state machine — a request path,
    a rollout, a retry ladder, an incident timeline, an approval gate, a reconciliation loop.

## Step 5 — write the hub (`days/day-NNN-<slug>/LESSON.md`)

26. The hub orients and assembles; **it never teaches**. No `Line by line:` in the hub. Required
    sections, in order (§17.5):
    - YAML frontmatter (`day`, `phase`, `phase_name`, `title`, `ids`, `principles`, `kind`,
      `plan_version: "v1.1.0"`, `parts`, `generated`, `status`, `lab_scaffolded`, `commit`)
    - a **yesterday / today / tomorrow** blockquote — no time estimate
    - `## §1 Where we are` — a scene and an analogy, plain language, NO code, NO jargon
    - `## §2 The map` — a table of every part: number, linked title
      (`parts/01-<slug>/1.1-<slug>.md`), what it answers, `level`, grouped by section with one line
      saying what each *section* means. **No minutes column, ever.**
    - `## §3 Setup — run this` — every `mkdir`, `uv add`, `docker compose up`, `kind create` the day
      needs, pinned — **and what to stop first** (Addendum 02 §4, the profiles)
    - `## §4 Build brief` — files to create, with `TODO(me)` markers left unsolved
    - `## §5 The check that must be able to fail` — the check that is RED before the work is done,
      and how to make it go red on purpose
    - `## §6 Cost & quota budget` — model calls per provider in RPM/RPD, CI minutes, RAM and disk for
      anything started today (`0` is an answer; state it)
    - `## §7 Traps` — the mistakes that eat an evening, including the named trap from §5.1
    - `## §8 Verify before you build` — live docs URLs, actually fetched, never from memory. A
      generated day teaches no paper, so it lists none here
    - `## §9 Say it in an interview` — one paragraph, spoken voice
    - `## §10 Done when` — pointer to `CHECKLIST.md`, defined by understanding and green checks
    - `## §11 Ledger & commit` — the verbatim `PROGRESS.md` row, any `PACKAGES.md`, `INCIDENTS.md`
      and `DECISIONS.md` rows, and the commit message `day NNN: <title> — closes <IDs>`.
      **The hub ends here.**

## Step 6 — the checklist (`days/day-NNN-<slug>/CHECKLIST.md`)

27. Demo command, setup boxes, **one box per part document** (read it, run its check-yourself, answer
    its out-loud question), build-brief boxes, a test box per test **including at least one "break
    it, watch it go red, fix it"**, the cost budget, the ledger rows pasted, and the commit box. No
    time estimates.
28. On a day that broke something, add the box: **"row appended to `docs/INCIDENTS.md`, with the
    first symptom written down before the cause"**.

## Step 7 — verify

29. Run `./o depth $ARGUMENTS`. **Fix every failure; never hand-wave past one.**
30. Run `./o trace` — the day's IDs must match §14 exactly, no more and no fewer.
31. Run `./o tracker`.
32. Finish by printing: today's IDs, the part count, the demo command, the cost budget, the profile
    the day needs, and the official documentation pages you actually fetched.

---

## Always

- Honor `CLAUDE.md`: doc-first · build-first-adopt-after · exact pins looked up live · at least one
  check that can go red · blast radius in the same document as the capability · zero-cost only.
- Do **not** solve the `TODO(me)` sections, and do **not** write project code. The learner types
  every line of `pulse/`, `platform_ops/`, `deploy/` and `pipelines/`. Teach; don't do the reps.
- **Never write a command that requires a card on file.** `aws`, `az`, `gcloud`, `eksctl`, `doctl`,
  `databricks` and `sagemaker` appear only as 🅿️ parked reading, marked on or immediately above the
  fence. `./o depth` fails the day otherwise.
- **Never assume everything is running.** State the profile and what to stop (Addendum 02 §4).
- **Never invent a citation, and never write a paper document.** Generated parts declare
  `papers: []`. The `papers/` contract (§17.4.2) exists for research written up deliberately, on
  request, by somebody who has read the paper — not for a generator that would eventually cite one
  that does not exist. Naming a paper inside a part is the same mistake in a smaller box.
- Never name a person, instructor, author, channel, academy, bootcamp or training company anywhere
  in the output. The plan is self-contained and cites no external course. Tool and library names are
  required and fine, as is citing a specification by its revision date.
- The failures this format exists to prevent (§17.8): splitting without deepening · summary in place
  of explanation · **stopping at the toy example** · assuming the previous day · code without failure
  · **a capability without a bound** · **trimming to fit** · solved reps. If a part has no story, no
  real error text, no production section and no stated blast radius, it is not done.
