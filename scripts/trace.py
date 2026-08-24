#!/usr/bin/env python
"""Regenerate docs/TRACEABILITY.md and docs/CURRICULUM_INDEX.md.

Sources of truth:
  - master plan §14: which IDs each day must close
  - days/day-NNN-<slug>/LESSON.md frontmatter: which IDs a day hub claims
  - docs/PROGRESS.md: which days are actually green (only those count as closed)

Never edit either output by hand - the next `./o check` overwrites you.

    uv run python scripts/trace.py
    # prints e.g.:  traceability: 0/279 closed, 0 problem(s); index: 279 IDs
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "00_MASTER_PLAN.md"
DOCS = ROOT / "docs"
DAYS = ROOT / "days"

# One pattern matches every concept ID this plan uses: FND-01, PLT-42, OBS-27, MLO-41, LLM-34,
# AIO-23, AGO-23, MCO-16, SEC-33, FIN-16.
ID_RE = re.compile(r"\b(?:FND|PLT|OBS|MLO|LLM|AIO|AGO|MCO|SEC|FIN)-\d{2}\b")

CURRICULA = {
    "FND": "A — Foundations & the production mental model",
    "PLT": "B — Platform: containers, Kubernetes, IaC, delivery",
    "OBS": "C — Observability & SRE practice",
    "MLO": "D — MLOps",
    "LLM": "E — LLMOps",
    "AIO": "F — AIOps",
    "AGO": "G — AgenticOps",
    "MCO": "H — MCPOps",
    "SEC": "I — Security, governance & compliance",
    "FIN": "J — Cost, capacity & FinOps",
}


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


def plan_map() -> dict[int, dict]:
    """Read §14 of the master plan into {day: {'phase': int, 'ids': [...]}}."""
    out: dict[int, dict] = {}
    phase, in_map = None, False
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        if line.startswith("## 14"):
            in_map = True
        elif in_map and line.startswith("## "):
            break
        elif in_map:
            if m := re.match(r"### Phase (\d+)", line):
                phase = int(m.group(1))
            elif (m := re.match(r"\|\s*(\d+)\s*\|", line)) and phase is not None:
                out[int(m.group(1))] = {"phase": phase, "ids": ID_RE.findall(line)}
    return out


def green_days() -> set[int]:
    """The day numbers that have a row in docs/PROGRESS.md (i.e. finished days)."""
    progress = DOCS / "PROGRESS.md"
    if not progress.exists():
        return set()
    text = progress.read_text(encoding="utf-8")
    return {int(m.group(1)) for m in re.finditer(r"^\|\s*(\d+)\s*\|", text, re.M)}


def day_folder(day: int) -> Path | None:
    """The folder for a day, whatever slug follows its number (plan §17.2)."""
    for pattern in (f"day-{day:03d}-*", f"day-{day:02d}-*", f"day-{day}-*"):
        matches = sorted(p for p in DAYS.glob(pattern) if p.is_dir())
        if matches:
            return matches[0]
    for bare in (DAYS / f"day-{day:03d}", DAYS / f"day-{day:02d}", DAYS / f"day-{day}"):
        if bare.is_dir():
            return bare
    return None


def hub_link(day: int) -> str:
    """A docs-relative link to a day's hub.

    Uses the real folder name when the day exists, so the link carries the day's subject. Days that
    are not written yet have no slug to use, so the link falls back to the bare `day-NNN` form and
    becomes exact the moment that day is created.
    """
    folder = day_folder(day)
    name = folder.name if folder is not None else f"day-{day:03d}"
    return f"../days/{name}/LESSON.md"


def hub(day: int) -> Path | None:
    """The hub file for a day, or None when the day is not written."""
    folder = day_folder(day)
    if folder is not None and (folder / "LESSON.md").is_file():
        return folder / "LESSON.md"
    return None


def doc_claims(day: int) -> list[str]:
    """The IDs a day hub's frontmatter claims to close (empty if the day is not written)."""
    path = hub(day)
    if path is None:
        return []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    front = text[3:end] if end != -1 else text[3:]
    for line in front.splitlines():
        if line.strip().lower().startswith("ids:"):
            return ID_RE.findall(line)
    return []


def day_titles() -> dict[int, str]:
    """Day number -> title, read from the same §14 rows the ID map comes from."""
    out: dict[int, str] = {}
    in_map = False
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        if line.startswith("## 14"):
            in_map = True
        elif in_map and line.startswith("## "):
            break
        elif in_map and (m := re.match(r"\|\s*(\d+)\s*\|\s*(.+?)\s*\|", line)):
            title = m.group(2).replace("**", "")
            out[int(m.group(1))] = title if len(title) <= 90 else title[:87] + "…"
    return out


def write_index(plan: dict[int, dict]) -> int:
    """Write docs/CURRICULUM_INDEX.md - the reverse of §14, ID -> day, grouped by curriculum.

    §14 answers "what does day 115 teach?". This answers "where do I learn `MLO-34`?", which is the
    question you have when a later day cites an ID you do not remember.
    """
    day_of = {cid: day for day, row in plan.items() for cid in row["ids"]}
    titles = day_titles()
    lines = [
        "# 📇 Curriculum index — Project Kriya",
        "",
        f"_Generated {date.today().isoformat()} by `scripts/trace.py` from the master plan's §14._",
        "**Do not edit by hand.**",
        "",
        "§14 answers *what does day 115 teach?* This file answers the reverse — *where do I learn",
        "`MLO-34`?* — which is the question you have when a later day cites an ID you no longer",
        "remember. Every ID appears exactly once; a duplicate or a missing ID is a plan bug.",
        "",
    ]
    for prefix, name in CURRICULA.items():
        ids = sorted(
            (cid for cid in day_of if cid.split("-")[0] == prefix),
            key=lambda c: int(c.split("-")[1]),
        )
        lines += [
            f"## Curriculum {name} (`{prefix}-`) — {len(ids)} IDs",
            "",
            "| ID | Day | Day title |",
            "| --- | --- | --- |",
        ]
        for cid in ids:
            day = day_of[cid]
            lines.append(f"| `{cid}` | [{day}]({hub_link(day)}) | {titles.get(day, '')} |")
        lines.append("")
    lines += [f"**{len(day_of)} IDs across {len(CURRICULA)} curricula.**", ""]
    (DOCS / "CURRICULUM_INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    return len(day_of)


def main() -> int:
    """Cross-check plan vs hubs vs progress; rewrite docs/TRACEABILITY.md."""
    _utf8_stdout()
    plan, green = plan_map(), green_days()
    if not plan:
        sys.exit(f"could not read §14 out of {PLAN} - the traceability check has nothing to check")
    lines = [
        "# Traceability (regenerated; do not edit by hand)",
        f"_Generated {date.today().isoformat()} by scripts/trace.py_",
        "",
        "Plan §14 assigns each ID to exactly one day. An ID counts as **closed** only when that",
        "day has a row in `docs/PROGRESS.md` *and* its hub's frontmatter claims the ID.",
        "**An open ID from a completed phase is a bug.**",
        "",
        "| ID | Phase | Planned day | Status |",
        "| --- | --- | --- | --- |",
    ]
    total = closed = 0
    problems: list[str] = []
    for day in sorted(plan):
        claimed = set(doc_claims(day))
        for cid in plan[day]["ids"]:
            total += 1
            if day in green and cid in claimed:
                closed += 1
                status = f"✅ closed day {day}"
            elif day in green:
                status = "🐛 green day, ID missing from hub"
                problems.append(f"{cid}: day {day} is green but its hub does not claim it")
            else:
                status = "⬜ open"
            lines.append(f"| {cid} | {plan[day]['phase']} | {day} | {status} |")
        if day in green and (extra := claimed - set(plan[day]["ids"])):
            problems.append(f"day {day} claims IDs not assigned by the plan: {sorted(extra)}")

    lines += ["", f"**{closed} / {total} IDs closed.**"]
    if problems:
        lines += ["", "## 🐛 Problems", *[f"- {p}" for p in problems]]
    (DOCS / "TRACEABILITY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    indexed = write_index(plan)
    print(
        f"traceability: {closed}/{total} closed, {len(problems)} problem(s); index: {indexed} IDs"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
