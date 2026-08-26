# 📅 days/ — the 237 written days

**Never done this before?** Run `./o next`; it tells you which day to write and how.
**Already started?** Run `./o status`; it tells you where you are.
**Want the map?** [`../docs/CURRICULUM_INDEX.md`](../docs/CURRICULUM_INDEX.md).
**Want progress?** [`../docs/TRACKER.md`](../docs/TRACKER.md).

---

## The six rules these documents follow

1. **All the code lives in the documents. None of it is pre-written in the repo.**
   You type it, you own it. There is no `pulse/*.py` and no `deploy/*.yaml` waiting for you — every
   line you will ever run is written out in a lesson, and you create the file yourself. **You cannot
   debug on Day 122 what you never typed on Day 41.**

2. **Every code block is followed by a line-by-line walkthrough.**
   Not a summary — an explanation of what each line does and *why it is that line and not another*.
   If a line is unexplained anywhere in these documents, that is a bug in the document.

3. **Every command is given in full, and its output is shown.**
   `mkdir -p`, `uv add package==1.2.3`, the `docker run` with all its flags, the `kubectl` with its
   namespace. And the output underneath it — because an operator's actual skill is reading output,
   and a command with nothing pasted below it teaches you to type rather than to read.

4. **One idea per document.** *(Principle 16)*
   A day is not one long page. It is a short hub plus one document per subtopic, in `parts/`. If a
   document needs the word "also" to introduce its second half, it should have been two documents.

5. **There are no clocks here.** *(Principle 17)*
   You will not find "this takes 90 minutes" or an "estimated hours" field anywhere, because it would
   be a lie and because it invites trimming. **A day is a unit of subject, not a unit of time.** Day
   115 might take you one evening or four; both are the day being done properly. Nothing is ever cut
   short to fit a schedule — if a subject needs twenty-two documents, it gets twenty-two. `./o done
   N` is gated on a ticked checklist and green checks, never on hours elapsed.

6. **Zero prior knowledge in, production knowledge out.** *(Principle 18)*
   Every document starts where someone who has never heard of the idea can stand — jargon defined the
   first time it appears, including jargon from earlier days, with a link back. And no document stops
   at the toy example: each one ends with **In production** — what a professional writes instead of
   the teaching version, what breaks at scale or under concurrency, the comment a senior engineer
   leaves on that code, **the signal you would be paged for**, and the question an interviewer asks
   to find out whether you have really used it.

---

## What's in a day folder

```
days/day-NNN-<slug>/   # the number is the identity; the slug says what the day teaches
├── LESSON.md      # the hub — the story, the map of parts, setup, build brief, the check, the budget
├── CHECKLIST.md   # the definition of done. `./o done NNN` refuses to commit until it's ticked.
├── parts/         # THE TEACHING — one document per subtopic
│   ├── 01-<slug>/ # section 1 — its own folder, named for what the section is about
│   │   ├── 1.1-<slug>.md
│   │   └── 1.2-<slug>.md
│   └── 02-<slug>/ # section 2
│       └── 2.1-<slug>.md
└── lab/           # you create this; `./o scaffold NNN` makes the folder
```

**Read the hub first, then the parts in numerical order.** The hub's §2 map is the table of contents
and tells you what each section number means for that day.

### What `1.1`, `1.2`, `2.1` mean

The number is `<section>.<subtopic>`, both scoped to that day.

- The **section** (the digit before the dot) groups subtopics that share one mental model — usually
  one curriculum ID, one lifecycle stage, or one phase of a mechanism.
- The **subtopic** (after the dot) is the reading order inside that section.

So on a two-ID day, `1.x` is the first ID, `2.x` is the second, and a `3.x` is usually the synthesis
— the trap you can only see once both ideas are true at the same time. Whatever the grouping is, the
hub says so explicitly.

**Each section gets its own folder**, numbered with two digits and then named for what it covers:
`parts/01-what-a-probe-is/`, `parts/03-failure-modes/`. On a day with sixteen parts this is the
difference between a readable folder and a wall of filenames — and a section is exactly the chunk you
will want to sit down with at once.

**Day numbers are three digits.** `day-007-networking-for-operators`, `day-115-data-drift`. With 237
days, two-digit padding would sort Day 100 between Day 10 and Day 11 in every file listing there is.

**The number is the identity; the slug is a label on it.** `./o`, `scripts/depth_check.py`,
`scripts/tracker.py` and `scripts/trace.py` all find a day by its number and accept whatever slug
follows, so `./o start 42` works no matter what `day-042-…` is called.

### The shape of every part document

Ten sections, always in this order. They trace one path: from a reader who has never heard of the
idea, to one who could defend it in a design review at 3am. This is the depth contract (plan §17.4),
and `./o depth NNN` fails the day if any of them is missing.

| Section | What it's for |
| --- | --- |
| **frontmatter** | `day`, `part`, `title`, `ids`, `level`, `papers`, `prerequisites`, `prev`, `next` — machine-read. No duration field; see rule 5. |
| **One-line answer** | the whole claim in one sentence, before anything else |
| **The story** | a concrete scene — a person, a machine, a failure, a decision — with no jargon at all. The hook the definition hangs on. |
| **The idea in plain language** | the concept from zero, every term defined the first time it appears, no code |
| **Why Kriya needs it** | the specific later day that breaks without this |
| **The mechanism** | the runnable code, the manifest, the protocol exchange written out, or the diagram — with its real output |
| **Line by line** | every non-obvious token, and why it is that line and not another |
| **When it breaks** | the **real** error text, what it means, the smallest fix |
| **In production** | what changes in a real system: the professional's version, what degrades at scale, the senior reviewer's comment, **the signal you would alert on**, the interviewer's question |
| **Check yourself** | one command to run now, one question to answer out loud |

### `level` — where a part leaves you

Every part declares one, and a well-built day climbs through them:

| `level` | You can… |
| --- | --- |
| `foundation` | say what the thing *is*, without using the word itself |
| `working` | use it correctly on your own problem, and recognise its error messages on sight |
| `production` | say what changes when it runs in a real system — scale, concurrency, quota, failure, the page at 3am — and defend the choice |

### The shape of every hub (`LESSON.md`)

The hub orients and assembles. **It never teaches** — there is no line-by-line walkthrough in it.

| Section | What it's for |
| --- | --- |
| **frontmatter** | machine-readable tracking. **`./o` and `scripts/` read this, not you.** |
| **yesterday / today / tomorrow** | where this day sits, in one line each |
| **§1 Where we are** | the idea in plain English with an analogy, before any code |
| **§2 The map** | every part, what it answers, its `level` — the reading order |
| **§3 Setup — run this** | everything today needs, **and what to stop first** |
| **§4 Build brief** | the file list, and which parts are yours to write (`TODO(me)`) |
| **§5 The check** | the check that must be able to **fail** (Principle 11) |
| **§6 Cost & quota budget** | requests, tokens, RAM, disk, CI minutes (Principle 15) |
| **§7 Traps** | the mistakes that eat an evening |
| **§8 Verify before you build** | the live docs pages to check (Principle 8), and every paper the day teaches |
| **§9 Say it in an interview** | one paragraph, spoken voice |
| **§10 Done when** | pointer to `CHECKLIST.md` — defined by understanding, never by elapsed time |
| **§11 Ledger & commit** | the verbatim ledger rows and the commit message. Every day ends the same way. |

---

## Which shell

These documents are written for **Git Bash** on Windows (it installs with Git). macOS and Linux
users: everything works unchanged except the installer URLs. **WSL2 is assumed from Day 21**, because
that is what Docker Desktop uses and what container behaviour matches.

| Git Bash (used in these documents) | PowerShell |
| --- | --- |
| `mkdir -p a/b/c` | `New-Item -ItemType Directory -Force a/b/c` |
| `touch f.py` | `if (-not (Test-Path f.py)) { New-Item -ItemType File f.py }` |
| `cat > f <<'EOF' … EOF` | `@'…'@ \| Set-Content -Encoding utf8 f` |
| `rm -rf folder` | `Remove-Item -Recurse -Force folder` |
| `export KEY=v` | `$env:KEY = 'v'` |
| `set -a; . ./.env; set +a` | `Get-Content .env \| ForEach-Object { ... }` (see Day 9) |
| `./o status` | `bash ./o status` |
| `cmd1 && cmd2` | `cmd1; if ($?) { cmd2 }` |
| `nproc` | `(Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors` |

**`make` is not used anywhere in this project.** The `./o` script replaces it; a two-line `Makefile`
shim exists only so `make check` still reaches `./o check`.

## The daily rhythm

```bash
./o status         # where am I
./o next           # what is next, and the command that writes it
./o start 42       # open the hub, and list its parts
./o parts 42       # just the sub-topic list
./o scaffold 42    # create days/day-042-<slug>/lab/
# ... read the hub's §1 and §2, then every part in order, then implement every TODO(me) ...
./o check          # ruff + offline pytest + the depth contract + traceability
./o done 42        # refuses until the checklist is ticked and checks are green
```

## Generating the days that aren't written yet

[`../docs/TRACKER.md`](../docs/TRACKER.md) lists every day, its status, and how many sub-topic
documents it has. To write the next one:

```
/day-kriya 42
```

That skill (`.claude/skills/day-kriya/SKILL.md`) reads the plan, the ledgers, the existing days and
the current state of `pulse`, verifies every version and every API symbol live, and produces the hub,
the `parts/` documents, the lab scaffold and the checklist in the format above. It ends by running
`./o depth 42`, which is what stops a thin day from being called written.

Two more skills exist for the half a script cannot check:

```
/review-day 42        # read a written day against §17.8 — the quality half of the contract
/incident-drill       # stage a failure against the current pulse, and run the response
```
