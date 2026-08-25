#!/usr/bin/env python
"""Enforce the master plan's §17 depth contract on a day folder.

A day is written when it is a hub plus one document per subtopic (Principle 16), each taken from
zero prior knowledge through to production (Principle 18), with no clock anywhere (Principle 17).
This script is the machine-readable half of that contract. It cannot judge whether an explanation
is any good - that is what §17.8 and reading are for - but it can refuse a day that has no parts,
a numbering gap, a missing required section, a code block nobody walked through, a smuggled-in time
estimate, a part loose outside its section folder, a folder whose name is a bare number with no slug
saying what is in it, a command that would put a card on file, a paper cited without the part that
teaches it, or a hub that quietly went back to teaching.

    uv run python scripts/depth_check.py          # every day that has a parts/ directory
    uv run python scripts/depth_check.py 0        # just day 0
    uv run python scripts/depth_check.py 4 5 6    # several days

Exit code 0 means every checked day satisfies the contract. Anything else is a failure list.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAYS = ROOT / "days"

# parts/<NN>-<slug>/<section>.<subtopic>-<kebab-slug>.md
#   ->  "parts/02-images/2.3-the-layer-that-cost-two-gigabytes.md"
PART_NAME_RE = re.compile(r"^(\d+)\.(\d+)-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")

# A section folder is the section number zero-padded to two digits, then what the section is about:
# 01-processes, 02-images, ... (plan §17.2). The number is the identity; the slug is a label on it,
# so nothing downstream reads the slug and a folder can be renamed to a better one freely.
SECTION_DIR_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")

# days/day-<NNN>-<slug>/  ->  "day-023-the-dockerfile-for-pulse". Same rule, one level up.
# Three digits, not two: this plan runs to Day 236, and two-digit names sort day 100 between
# day 10 and day 11 in every file tree, every `ls` and every editor tab bar.
DAY_DIR_RE = re.compile(r"^day-(\d{3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")

# The ten required sections of a part document (plan §17.4). Section 1 is the frontmatter, checked
# separately; these are the nine that appear in the body, and they must appear in this order.
PART_SECTIONS = [
    ("one-line answer", re.compile(r"^#{2,3}\s.*one[- ]line answer", re.I | re.M)),
    ("the story", re.compile(r"^#{2,3}\s.*the story", re.I | re.M)),
    ("the idea in plain language", re.compile(r"^#{2,3}\s.*idea in plain language", re.I | re.M)),
    ("why Kriya needs it", re.compile(r"^#{2,3}\s.*why kriya needs it", re.I | re.M)),
    ("the mechanism", re.compile(r"^#{2,3}\s.*mechanism", re.I | re.M)),
    ("line by line", re.compile(r"^#{2,3}\s.*line by line|^\*\*Line by line:?\*\*", re.I | re.M)),
    ("when it breaks", re.compile(r"^#{2,3}\s.*when it breaks", re.I | re.M)),
    ("in production", re.compile(r"^#{2,3}\s.*in production", re.I | re.M)),
    ("check yourself", re.compile(r"^#{2,3}\s.*check yourself", re.I | re.M)),
]

# "Line by line" explains code, so a part with no code to explain cannot have one. A `concept`
# part (plan §17.7) may legitimately carry no runnable block at all. This is the only conditional
# section in the contract: it is required exactly when the part contains a fence that would need a
# walkthrough, and never otherwise. Every other required section is unconditional.
CONDITIONAL_SECTIONS = {"line by line"}

# A paper is taught in a part of its own (plan §17.4.2), holding the ordinary ten sections plus
# three, keyed here by the section each one follows: the citation, the demo - a small end-to-end
# project implementing only the paper's feature - and what the paper did NOT claim, which is the one
# that earns the part, because most of the damage a famous result does is done by the sentence it
# never contained.
PAPER_SECTIONS = {
    "one-line answer": ("the citation", re.compile(r"^#{2,3}\s.*citation", re.I | re.M)),
    "the mechanism": ("the demo", re.compile(r"^#{2,3}\s.*the demo", re.I | re.M)),
    "line by line": (
        "what it did not claim",
        re.compile(r"^#{2,3}\s.*did\s+not\s+claim", re.I | re.M),
    ),
}

# "Line by line" sits immediately after each code block, which the walkthrough check already
# enforces precisely - so the position of its *first* occurrence carries no information, and
# comparing it would fail a part whose first walkthrough belongs to a section later than the
# one this list puts it in. Presence is required; position is not.
ORDER_EXEMPT_SECTIONS = {"line by line"}

# The citation block names a paper the writer actually opened: a link to a copy that is free to
# read, the year, and the date it was read - the same convention Principle 8 already uses for a
# documentation page. What it cannot check is whether the title is real, which is why §17.4.1
# rule 6 exists and is read.
CITATION_URL_RE = re.compile(r"https?://\S+")
CITATION_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
READ_DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

# §18.4: this curriculum names no people. A paper is cited by title, year and identifier - so the
# one construction that can only be an author list is rejected outright.
AUTHOR_CITE_RE = re.compile(r"\bet\s+al\b\.?", re.I)

# papers: [a-slug, another-slug]  ->  ["a-slug", "another-slug"]; papers: [] -> []
PAPER_SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

PART_FRONTMATTER_KEYS = [
    "day",
    "part",
    "title",
    "ids",
    "level",
    "papers",
    "prerequisites",
    "prev",
    "next",
]

# Principle 18: every part declares where it leaves the reader.
LEVELS = {"foundation", "working", "production"}

# Principle 17: a day is a unit of subject, not a unit of time. Nothing in a day folder may suggest
# a duration or a pace - not "takes 20 minutes", not an "estimated hours" field, not a pace.
TIME_BANS = [
    (
        re.compile(
            r"^\s*(reading_minutes|duration|time_estimate|minutes|est_time|estimated_hours"
            r"|estimated hours)\s*:",
            re.I | re.M,
        ),
        "a duration field in frontmatter",
    ),
    (
        re.compile(r"\b\d+\s*[-–]?\s*\d*\s*(minutes?|mins?|hours?|hrs?)\b(?!\s*(of |the ))", re.I),
        "a time estimate in the prose",
    ),
    (re.compile(r"\*\*(Time|Estimated hours):?\*\*", re.I), "a **Time:** line"),
    (re.compile(r"should take (about |around |roughly )?\w+", re.I), "a 'should take ...' pace"),
]

# Principle 15 / Addendum 01: the whole curriculum runs at zero cost. A command that provisions a
# billable cloud resource must never appear as a step the reader is told to run. It may appear as
# awareness-level reading, which is marked 🅿️ on or just above the fence - the same convention the
# day documents use in prose. Anything else fails the day here rather than on a credit card.
BILLABLE_RE = re.compile(
    r"^\s*(?:\$\s*)?(?:aws|az|gcloud|eksctl|doctl|databricks|sagemaker)\s+\S", re.M
)
PARKED_MARK = "🅿️"

HUB_FRONTMATTER_KEYS = [
    "day",
    "phase",
    "phase_name",
    "title",
    "ids",
    "principles",
    "kind",
    "plan_version",
    "parts",
    "generated",
    "status",
    "lab_scaffolded",
    "commit",
]

# The eleven numbered hub sections (plan §17.5). Frontmatter and the yesterday/today/tomorrow
# blockquote are checked separately.
HUB_SECTIONS = [
    (1, "Where we are"),
    (2, "The map"),
    (3, "Setup"),
    (4, "Build brief"),
    (5, "The check that must be able to fail"),
    (6, "Cost & quota budget"),
    (7, "Traps"),
    (8, "Verify before you build"),
    (9, "Say it in an interview"),
    (10, "Done when"),
    (11, "Ledger & commit"),
]

# Fences whose contents are output, a diagram or a config dump - they need no walkthrough.
NO_WALKTHROUGH_LANGS = {"", "text", "console", "traceback", "mermaid", "json", "log", "csv"}

# Headings under which a code block is evidence, not teaching, so no walkthrough is required.
EXEMPT_HEADINGS = re.compile(
    r"when it breaks|check yourself|verify|budget|ledger|the map|traps|citation", re.I
)

PLAN_VERSION = "v1.1.0"


def _utf8_stdout() -> None:
    """Print UTF-8 whatever the console claims to be.

    Windows terminals default to cp1252, which cannot encode an em dash, a box-drawing character
    or the 🅿️ this script names in one of its failure messages. Without this the tool crashes
    with UnicodeEncodeError while reporting a problem, which is a spectacularly unhelpful way to
    fail. `errors="replace"` means a console that genuinely cannot render a glyph prints a
    placeholder instead of taking the run down with it.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


@dataclass
class Report:
    day: int
    failures: list[str] = field(default_factory=list)
    parts: int = 0
    # (slug, where) for every papers: entry in the day, and the slugs this day's paper parts teach
    papers_declared: list[tuple[str, str]] = field(default_factory=list)
    papers_taught: set[str] = field(default_factory=set)

    @property
    def ok(self) -> bool:
        return not self.failures

    def fail(self, where: str, message: str) -> None:
        self.failures.append(f"{where}: {message}")


def frontmatter(text: str) -> dict[str, str] | None:
    """Return the YAML-ish frontmatter as a flat dict, or None when there is none."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip()
    return out


def body(text: str) -> str:
    """The document with its frontmatter removed, so heading checks cannot match inside it."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


def find_day(number: int) -> Path | None:
    """The folder for a day, whatever slug follows its number (plan §17.2).

    The number is the identity, so `day-023-...`, `day-23-...` and a bare `day-23` all resolve to
    day 23 and a folder may be renamed to a better slug without breaking anything that reads it.
    """
    patterns = [f"day-{number:03d}-*", f"day-{number:02d}-*", f"day-{number}-*"]
    for pattern in patterns:
        matches = sorted(p for p in DAYS.glob(pattern) if p.is_dir())
        if matches:
            return matches[0]
    for bare in (DAYS / f"day-{number:03d}", DAYS / f"day-{number:02d}", DAYS / f"day-{number}"):
        if bare.is_dir():
            return bare
    return None


def unexplained_code_blocks(text: str) -> list[int]:
    """Line numbers of code fences that no 'Line by line' walkthrough follows.

    Walks the document once, tracking the current heading. A fence is exempt when its language
    carries no logic (plain output, a diagram, a log dump) or when it sits under a heading whose
    job is showing evidence rather than teaching.
    """
    lines = text.splitlines()
    offenders: list[int] = []
    heading = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line
            i += 1
            continue
        fence = re.match(r"^(`{3,})([\w+-]*)\s*$", line)
        if not fence:
            i += 1
            continue

        # A fence may be longer than three backticks so it can contain a shorter one - which is how
        # a lesson shows the contents of a Markdown file. The closing fence must be at least as long
        # as the opening one, so a nested block cannot end the outer one.
        ticks = len(fence.group(1))
        closing = re.compile(rf"^`{{{ticks},}}\s*$")
        lang = fence.group(2).lower()
        start = i
        i += 1
        while i < len(lines) and not closing.match(lines[i]):
            i += 1
        i += 1  # step over the closing fence

        if lang in NO_WALKTHROUGH_LANGS or EXEMPT_HEADINGS.search(heading):
            continue

        # Look ahead for a walkthrough before the next fence or the next heading of the same rank.
        j = i
        explained = False
        while j < len(lines):
            nxt = lines[j]
            if re.search(r"line by line", nxt, re.I):
                explained = True
                break
            if re.match(r"^`{3,}\w", nxt) or nxt.startswith("## "):
                break
            j += 1
        if not explained:
            offenders.append(start + 1)
    return offenders


def has_explainable_code(text: str) -> bool:
    """True when the body holds at least one fence the contract expects a walkthrough for.

    Mirrors the exemptions in unexplained_code_blocks: a language that carries no logic (plain
    output, a diagram, a log dump) does not need explaining, and neither does a fence under a
    heading whose job is showing evidence rather than teaching.
    """
    lines = text.splitlines()
    heading = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line
            i += 1
            continue
        fence = re.match(r"^(`{3,})([\w+-]*)\s*$", line)
        if not fence:
            i += 1
            continue
        ticks = len(fence.group(1))
        closing = re.compile(rf"^`{{{ticks},}}\s*$")
        lang = fence.group(2).lower()
        i += 1
        while i < len(lines) and not closing.match(lines[i]):
            i += 1
        i += 1
        if lang not in NO_WALKTHROUGH_LANGS and not EXEMPT_HEADINGS.search(heading):
            return True
    return False


def check_no_clocks(text: str, where: str, report: Report) -> None:
    """Principle 17: no time estimates anywhere in a day folder.

    Content is never trimmed to fit a schedule, so no document may imply one. Code fences are
    stripped first - a real command may legitimately mention a timeout, and a probe absolutely will.
    """
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    for pattern, description in TIME_BANS:
        hit = pattern.search(prose)
        if hit:
            snippet = hit.group(0).strip().replace("\n", " ")
            report.fail(where, f"{description} ({snippet!r}) - a day has no clock (Principle 17)")


def check_no_billing(text: str, where: str, report: Report) -> None:
    """Principle 15: nothing the reader is told to run may require a card on file.

    A billable command is allowed only as awareness-level reading, which the day documents mark
    with 🅿️. The mark must be on the command's line or in the three lines above it, so a reader
    scrolling past a fence cannot mistake a demonstration for an instruction.
    """
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not BILLABLE_RE.match(line):
            continue
        window = lines[max(0, index - 3) : index + 1]
        if any(PARKED_MARK in w for w in window):
            continue
        report.fail(
            where,
            f"line {index + 1} runs a billable cloud command ({line.strip()[:48]!r}) that is not "
            f"marked {PARKED_MARK} parked - the curriculum never puts a card on file (Addendum 01)",
        )


def declared_papers(meta: dict[str, str] | None) -> list[str]:
    """The paper slugs a part says its idea rests on (plan §17.4.2).

    `papers: []` is the common case and a real answer - there is no research behind `chmod`, and a
    field invented to look scholarly would break Principle 8 in the most embarrassing way available.
    The value is a flow list of kebab-case slugs, which is why it needs no YAML parser: a slug never
    contains a colon, a comma or a space.
    """
    if not meta:
        return []
    raw = meta.get("papers", "").strip()
    if not raw.startswith("["):
        return []
    return PAPER_SLUG_RE.findall(raw[1:].partition("]")[0])


@lru_cache(maxsize=1)
def paper_part_index() -> dict[str, Path]:
    """Every `kind: paper` part in the curriculum, by slug.

    A paper is explained once (§17.4.2) and linked forever after, so this index spans `days/` rather
    than one day: Day 190 may rest on a paper Day 125 taught, and re-explaining it would be the same
    mistake as re-explaining a process. Cached because it reads every part in the repository and a
    full run checks every written day.
    """
    index: dict[str, Path] = {}
    for part in DAYS.glob("day-*/parts/*/*.md"):
        meta = frontmatter(part.read_text(encoding="utf-8"))
        if not meta or meta.get("kind", "").strip('"') != "paper":
            continue
        slug = meta.get("paper", "").strip('"')
        if slug:
            index[slug] = part
    return index


def check_paper_part(
    path: Path, meta: dict[str, str], content: str, where: str, report: Report
) -> None:
    """The extra contract a `kind: paper` part carries (plan §17.4.2).

    Its two extra sections are checked for presence in `check_part`, alongside the ordinary ten, so
    that ordering is judged once against one list. What is left here is what only a paper part can
    get wrong: an identity that disagrees with its filename, and a citation nobody could follow.
    """
    slug = meta.get("paper", "").strip('"')
    if not slug:
        report.fail(where, "kind: paper but no paper: <slug> - a paper's slug is its identity")
        return
    name_match = PART_NAME_RE.match(path.name)
    if name_match and name_match.group(3) != slug:
        report.fail(
            where,
            f"paper: {slug!r} but the filename slug is {name_match.group(3)!r} - a paper part is "
            f"named after its paper, so the two are the same string",
        )
    if slug not in declared_papers(meta):
        report.fail(where, f"a paper part declares its own slug in papers: [{slug}]")

    # §17.4.2: the demo is a project, not a paragraph about one - so it has something to run.
    demo = section_text(content, PAPER_SECTIONS["the mechanism"][1])
    if demo is not None and not re.search(r"^`{3,}", demo, re.M):
        report.fail(
            where,
            "the demo has no code block - it is a small end-to-end project implementing only the "
            "paper's feature, with the command that runs it and its real output (§17.4.2)",
        )

    citation = section_text(content, PAPER_SECTIONS["one-line answer"][1])
    if citation is None:
        return  # the missing-section failure was already reported
    if not CITATION_URL_RE.search(citation):
        report.fail(where, "the citation has no link to a copy that is free to read (§17.4.2)")
    if not CITATION_YEAR_RE.search(citation):
        report.fail(where, "the citation names no year (§17.4.2)")
    if not READ_DATE_RE.search(citation):
        report.fail(
            where,
            "the citation has no YYYY-MM-DD date it was read - a paper you did not open is an "
            "invented fact (§17.4.1 rule 6)",
        )


def section_text(content: str, pattern: re.Pattern[str]) -> str | None:
    """The body of one `##` section: from its heading to the next heading of the same rank."""
    found = pattern.search(content)
    if not found:
        return None
    rest = content[found.end() :]
    nxt = re.search(r"^#{1,3}\s", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def part_sections(is_paper: bool) -> list[tuple[str, re.Pattern[str]]]:
    """The required sections for this part, in contract order (plan §17.4, §17.4.2).

    An ordinary part carries the ten. A paper part carries the same ten with two spliced in at fixed
    positions, so one ordering check covers both and a citation cannot drift to the bottom of the
    page where nobody reads it.
    """
    if not is_paper:
        return PART_SECTIONS
    out: list[tuple[str, re.Pattern[str]]] = []
    for name, pattern in PART_SECTIONS:
        out.append((name, pattern))
        if name in PAPER_SECTIONS:
            out.append(PAPER_SECTIONS[name])
    return out


def check_part(path: Path, day: int, report: Report) -> tuple[int, int] | None:
    """Validate one parts/<NN>-<slug>/ document. Returns its (section, subtopic) numbers."""
    where = f"parts/{path.parent.name}/{path.name}"
    match = PART_NAME_RE.match(path.name)
    if not match:
        report.fail(where, "filename must be <section>.<subtopic>-<kebab-slug>.md")
        return None
    section, subtopic = int(match.group(1)), int(match.group(2))

    folder = path.parent.name
    folder_match = SECTION_DIR_RE.match(folder)
    if folder_match and int(folder_match.group(1)) != section:
        report.fail(
            where,
            f"lives in parts/{folder}/ but its number says section {section} - "
            f"it belongs in parts/{section:02d}-<slug>/",
        )

    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail(where, "no YAML frontmatter")
    else:
        missing = [k for k in PART_FRONTMATTER_KEYS if k not in meta]
        if missing:
            report.fail(where, f"frontmatter missing {', '.join(missing)}")
        if meta.get("day") not in {str(day), f'"{day}"'}:
            report.fail(where, f"frontmatter day is {meta.get('day')!r}, expected {day}")
        if meta.get("part", "").strip('"') != f"{section}.{subtopic}":
            report.fail(where, f"frontmatter part should be {section}.{subtopic}")
        level = meta.get("level", "").strip('"').lower()
        if level and level not in LEVELS:
            report.fail(where, f"level is {level!r}, must be one of {sorted(LEVELS)}")

    content = body(text)
    is_paper = bool(meta) and meta.get("kind", "").strip('"') == "paper"
    explainable = has_explainable_code(content)
    seen_at: list[int] = []
    expected = 0
    for name, pattern in part_sections(is_paper):
        if name in CONDITIONAL_SECTIONS and not explainable:
            continue  # nothing to explain, so the walkthrough would be empty ceremony
        ordered = name not in ORDER_EXEMPT_SECTIONS
        expected += ordered
        found = pattern.search(content)
        if not found:
            report.fail(where, f"missing required section: {name}")
        elif ordered:
            seen_at.append(found.start())
    if len(seen_at) == expected and seen_at != sorted(seen_at):
        report.fail(where, "required sections are out of contract order (plan §17.4)")

    for line_no in unexplained_code_blocks(content):
        report.fail(where, f"code block at line {line_no} has no 'Line by line' walkthrough")

    check_papers(path, meta, content, where, is_paper, report)
    check_no_clocks(text, where, report)
    check_no_billing(text, where, report)
    return section, subtopic


def check_papers(
    path: Path,
    meta: dict[str, str] | None,
    content: str,
    where: str,
    is_paper: bool,
    report: Report,
) -> None:
    """Plan §17.4.2: what a part says about the research it rests on.

    Three things are checkable here. That a citation is a title rather than a person (§18.4). That a
    part naming a paper links the part which teaches it, so the slug is a route and not a label. And
    that a paper part is itself well formed. Whether the slug resolves to a paper part at all is a
    curriculum-wide question, so `check_day` answers it.
    """
    author = AUTHOR_CITE_RE.search(content)
    if author:
        report.fail(
            where,
            f"cites by author name ({author.group(0)!r}) - a paper is cited by title, year and "
            f"identifier, and this curriculum names no people (§18.4)",
        )

    slugs = declared_papers(meta)
    if is_paper and meta:
        check_paper_part(path, meta, content, where, report)
        report.papers_taught.add(meta.get("paper", "").strip('"'))

    for slug in slugs:
        report.papers_declared.append((slug, where))
        if is_paper and meta and slug == meta.get("paper", "").strip('"'):
            continue  # the paper part is the explanation; it does not link to itself
        if f"-{slug}.md" not in content:
            report.fail(
                where,
                f"declares papers: [{slug}] but links no paper part teaching it - a slug is a "
                f"route to the document that explains it, not a label (§17.4.2)",
            )


def check_numbering(numbers: list[tuple[int, int]], report: Report) -> None:
    """Sections start at 1 and are contiguous; so are the subtopics inside each section."""
    if not numbers:
        return
    sections = sorted({s for s, _ in numbers})
    if sections[0] != 1:
        report.fail("parts/", f"section numbering starts at {sections[0]}, must start at 1")
    expected = list(range(1, len(sections) + 1))
    if sections != expected:
        report.fail("parts/", f"section numbering has a gap: {sections} (expected {expected})")
    for section in sections:
        subs = sorted(sub for s, sub in numbers if s == section)
        if subs != list(range(1, len(subs) + 1)):
            report.fail(
                "parts/", f"section {section} subtopics are {subs}, expected 1..{len(subs)}"
            )


def check_hub(folder: Path, part_count: int, report: Report) -> None:
    hub = folder / "LESSON.md"
    if not hub.is_file():
        report.fail("LESSON.md", "missing - every day needs a hub")
        return

    text = hub.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail("LESSON.md", "no YAML frontmatter")
    else:
        missing = [k for k in HUB_FRONTMATTER_KEYS if k not in meta]
        if missing:
            report.fail("LESSON.md", f"frontmatter missing {', '.join(missing)}")
        declared = meta.get("parts", "").strip('"')
        if declared.isdigit() and int(declared) != part_count:
            report.fail(
                "LESSON.md", f"frontmatter says parts: {declared}, parts/ holds {part_count}"
            )
        if meta.get("plan_version", "").strip('"') != PLAN_VERSION:
            report.fail("LESSON.md", f"plan_version must be {PLAN_VERSION}")

    content = body(text)
    for number, name in HUB_SECTIONS:
        if not re.search(rf"^##\s*§{number}\b", content, re.M):
            report.fail("LESSON.md", f"missing section §{number} ({name})")

    if not re.search(r"^>\s*\*\*Yesterday", content, re.M | re.I):
        report.fail("LESSON.md", "missing the yesterday / today / tomorrow blockquote")

    if re.search(r"line by line", content, re.I):
        report.fail("LESSON.md", "the hub must not teach - move the walkthrough into a part")

    # §17.5: a day that teaches a paper names it in §8, next to the docs it verified, so the day's
    # reading is visible from the hub rather than only from a filename in the tree.
    verify = section_text(content, re.compile(r"^##\s*§8\b", re.M))
    for slug in sorted(report.papers_taught):
        if verify is not None and slug not in verify:
            report.fail(
                "LESSON.md",
                f"§8 does not name the paper this day teaches ({slug}) - the hub lists every paper "
                f"with its identifier and the date it was read (§17.5)",
            )

    check_no_clocks(text, "LESSON.md", report)
    check_no_billing(text, "LESSON.md", report)

    linked = set(re.findall(r"parts/([\w.\-]+/[\w.\-]+\.md)", content))
    on_disk = {
        f"{d.name}/{f.name}"
        for d in (folder / "parts").iterdir()
        if d.is_dir()
        for f in d.glob("*.md")
    }
    for name in sorted(on_disk - linked):
        report.fail("LESSON.md", f"§2 map does not link parts/{name}")


def check_day(number: int) -> Report:
    report = Report(day=number)
    folder = find_day(number)
    if folder is None:
        report.fail("days/", f"no folder for day {number}")
        return report

    if not DAY_DIR_RE.match(folder.name):
        report.fail(
            f"days/{folder.name}/",
            "a day folder is day-NNN (three digits) then a kebab-case slug saying what it "
            "teaches, e.g. days/day-023-the-dockerfile-for-pulse/ (plan §17.2)",
        )

    parts_dir = folder / "parts"
    if not parts_dir.is_dir():
        report.fail("parts/", "missing - a day with no parts/ is not written (plan §17.2)")
        return report

    for stray in sorted(parts_dir.glob("*.md")):
        report.fail(
            f"parts/{stray.name}",
            "loose in parts/ - every part lives in its section folder, e.g. parts/01-<slug>/",
        )

    for entry in sorted(parts_dir.iterdir()):
        if entry.is_dir() and not SECTION_DIR_RE.match(entry.name):
            report.fail(
                f"parts/{entry.name}/",
                "a section folder is the section number zero-padded to two digits, then a "
                "kebab-case slug saying what the section is about, e.g. parts/02-images/",
            )

    files = sorted(
        (f for d in parts_dir.iterdir() if d.is_dir() for f in d.glob("*.md")),
        key=lambda f: (f.parent.name, f.name),
    )
    if not files:
        report.fail("parts/", "empty - no section folders holding part documents")
        return report

    report.parts = len(files)
    numbers = [n for f in files if (n := check_part(f, number, report)) is not None]
    check_numbering(numbers, report)

    # A paper slug must resolve to the part that teaches it - in this day, or in an earlier one that
    # already taught it (§17.4.2). A slug that resolves nowhere is a citation with no paper behind
    # it, which is the failure Principle 8 cares about most.
    index = paper_part_index()
    for slug, where in report.papers_declared:
        if slug not in index:
            report.fail(
                where,
                f"papers: [{slug}] names no paper part - a paper worth citing is taught in a part "
                f"of its own, and one that is not worth a part is not cited (§17.4.2)",
            )

    check_hub(folder, len(files), report)

    checklist = folder / "CHECKLIST.md"
    if not checklist.is_file():
        report.fail("CHECKLIST.md", "missing")
    else:
        text = checklist.read_text(encoding="utf-8")
        check_no_clocks(text, "CHECKLIST.md", report)
        check_no_billing(text, "CHECKLIST.md", report)
    return report


def written_days() -> list[int]:
    """Every day that has attempted the hub + parts/ shape, so an unwritten day is not a failure."""
    found: list[int] = []
    for folder in sorted(DAYS.glob("day-*")):
        if not (folder / "parts").is_dir():
            continue
        digits = re.search(r"day-(\d+)", folder.name)
        if digits:
            found.append(int(digits.group(1)))
    return sorted(found)


def main(argv: list[str]) -> int:
    _utf8_stdout()
    requested = [int(a) for a in argv if a.isdigit()]
    days = requested or written_days()
    if not days:
        print("no day has a parts/ directory yet - nothing to check")
        return 0

    reports = [check_day(d) for d in days]
    failed = [r for r in reports if not r.ok]

    for report in reports:
        if report.ok:
            print(f"OK   day {report.day:>3}  {report.parts} parts")
        else:
            print(f"FAIL day {report.day:>3}  {len(report.failures)} problems")
            for failure in report.failures:
                print(f"       - {failure}")

    print()
    if failed:
        print(f"depth contract: {len(reports) - len(failed)}/{len(reports)} days pass")
        return 1
    print(f"depth contract: all {len(reports)} checked days pass")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
