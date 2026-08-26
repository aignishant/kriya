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
10. **Never cite a paper.** This curriculum cites none (§17.4.2, ADR-0006). There is no `papers/`
    folder, no `papers:` frontmatter key and no `kind: paper` document, and `./o depth` fails a
    part that carries any of them. Where an idea came from published work and the origin changes
    how an operator behaves, say what it changed, in ordinary words, in the part that uses it, with
    no title, no year, no identifier, no link and no author.
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
    - **frontmatter** — `day`, `part`, `title`, `ids`, `level`, `prerequisites`, `prev`, `next`.
      **No duration field of any kind**, and **no `papers:`, `paper:` or `kind: paper` key**
      (step 10).
    - **One-line answer** — the claim in one sentence, before anything else.
    - **The story** — a concrete scene first: a person, a machine, a failure, a decision. **No jargon
      at all** in this section. This is the hook the definition hangs on. Written to the four story
      rules below, which are the ones this curriculum gets wrong most often.
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
24. Apply **Kriya's five additional part rules** (§17.4.1): name the official page checked, with a
    date · state the verified version or a `TODO` with the lookup command · **name the blast radius**
    of any new capability (worst case, who can trigger it, what bounds it) · **say how you would
    alert** on any new signal, or why you would not · **state the cost in quota units** (requests,
    tokens, RAM, disk, CI minutes; `0` is an answer).
25. Mermaid diagram whenever the concept is spatial, sequential, or a state machine — a request path,
    a rollout, a retry ladder, an incident timeline, an approval gate, a reconciliation loop.

### How to write *The story* (§18.1 rule 8)

The story is the section a reader meets first and the one they remember. Four rules, and a scene that
fails any of them is the wrong scene — rewrite it rather than patching it.

26. **A scene the reader has been inside.** A kitchen, a queue, a bus, a shared flat, a phone call, a
    school, a lost set of keys, a parcel that did not arrive. **Not a trade whose vocabulary is
    itself the obstacle** — not a pharmacy dispensing bench, not a touring theatre's stage
    management, not a building site's chain of command. If the scene has to be explained before it
    can illustrate anything, it has cost the reader more than it gave them.
27. **It has to work anywhere.** Somebody reading this has never seen a British postal sorting
    office, a locum pharmacist or a village fête. Things that travel: food, family, money, waiting,
    lost property, a full phone, a shared bathroom, a group chat, a bus that did not come. Prefer
    them.
28. **It must be literally realistic.** The scene should be something that plausibly happened to
    somebody last Tuesday, with real quantities in it — *four flatmates and one bathroom*, *ninety
    photos and a phone that says storage full*. A scene that is really a metaphor wearing a costume
    teaches the costume.
29. **Four beats, and every one of them a whole sentence** (§18.2): 🎬 the scene · 😬 the naive fix ·
    💥 why it fails · 💡 the insight. Keep it short. Roughly 120–200 words is enough for all four,
    and a story longer than the mechanism it introduces is a story that has become the point.

### How to write every other section (§18.1 rules 6–7)

30. **Whole sentences, properly punctuated.** A fragment with no verb reads as speed to somebody who
    already knows the subject and as fog to somebody who does not. Use commas and full stops. Keep
    the em dash for the one aside per paragraph that earns it — four ideas welded together with
    dashes is the habit this rule exists to break — and let a colon introduce a list rather than a
    thought.
31. **The plainest word that is still exact.** *use* over *utilise*, *starts* over *is initiated*,
    *find out* over *ascertain*, *about* over *approximately*. The rule stops at accuracy: a
    technical term that means something specific is kept, and defined on first use. Replacing a
    precise word with a vague one is not simplification.
32. **Plain words first, then the term.** Say the thing, give the concrete example, and only then
    name it. If a twelve-year-old could not follow the first sentence of a section, the first
    sentence is wrong.

## Step 5 — write the hub (`days/day-NNN-<slug>/LESSON.md`)

33. The hub orients and assembles; **it never teaches**. No `Line by line:` in the hub. Required
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
    - `## §8 Verify before you build` — live docs URLs, actually fetched, never from memory, each
      with the date it was fetched
    - `## §9 Say it in an interview` — one paragraph, spoken voice
    - `## §10 Done when` — pointer to `CHECKLIST.md`, defined by understanding and green checks
    - `## §11 Ledger & commit` — the verbatim `PROGRESS.md` row, any `PACKAGES.md`, `INCIDENTS.md`
      and `DECISIONS.md` rows, and the commit message `day NNN: <title> — closes <IDs>`.
      **The hub ends here.**

## Step 6 — the checklist (`days/day-NNN-<slug>/CHECKLIST.md`)

34. Demo command, setup boxes, **one box per part document** (read it, run its check-yourself, answer
    its out-loud question), build-brief boxes, a test box per test **including at least one "break
    it, watch it go red, fix it"**, the cost budget, the ledger rows pasted, and the commit box. No
    time estimates.
35. On a day that broke something, add the box: **"row appended to `docs/INCIDENTS.md`, with the
    first symptom written down before the cause"**.

## Step 7 — verify

36. Run `./o depth $ARGUMENTS`. **Fix every failure; never hand-wave past one.**
37. Run `./o trace` — the day's IDs must match §14 exactly, no more and no fewer.
38. Run `./o tracker`.
39. Finish by printing: today's IDs, the part count, the demo command, the cost budget, the profile
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
- **Never cite a paper and never create a `papers/` folder.** ADR-0006 removed both from this
  contract. Naming a paper inside a part is the same mistake in a smaller box.
- **Never write a story the reader has to decode.** The scene comes from ordinary life, works in
  any country, and is literally realistic (steps 26–29). A clever analogy that needs its own
  explanation is a failure, not a flourish.
- **Never write in fragments.** Whole sentences, commas and full stops, the plainest exact word
  (steps 30–32). This applies to every section, not only the story.
- Never name a person, instructor, author, channel, academy, bootcamp or training company anywhere
  in the output. The plan is self-contained and cites no external course. Tool and library names are
  required and fine, as is citing a specification by its revision date.
- The failures this format exists to prevent (§17.8): splitting without deepening · summary in place
  of explanation · **stopping at the toy example** · assuming the previous day · code without failure
  · **a capability without a bound** · **trimming to fit** · solved reps. If a part has no story, no
  real error text, no production section and no stated blast radius, it is not done.
