# Decision Index — Project Kriya

Append-only. One line per architecture decision record in `docs/adr/`, so a cold reader finds the
decision without grepping for it.

**An ADR is written when a choice would be expensive to reverse and non-obvious to a stranger.**
Not for every choice — for the ones where someone six months from now will look at the code and ask
*"why on earth is it like this?"* and deserve an answer better than a shrug.

Every ADR carries six sections, and `./o check` does not enforce that — reading does:

| Section | The question it answers |
| --- | --- |
| **Context** | What was true when we decided? Include the numbers. |
| **Options considered** | What else was on the table, with honest pros and cons? |
| **Decision** | What we chose, in one unambiguous sentence. |
| **Consequences** | What is now easier, what is now harder, what we are committed to. |
| **What would make us change our minds** | At least one **number** or observable condition. |
| **Cold read** | Re-read it later with a reviewer's hat on, and sign it. |

The last two are what separate an ADR that ages well from a paragraph of self-justification.

| ADR | Date | Status | Decision |
| --- | ---- | ------ | -------- |
| [ADR-0001](adr/ADR-0001-project-charter.md) | 2026-08-24 | accepted | Kriya exists as a distinct curriculum: ops for AI systems, five disciplines, one operated service. |
| [ADR-0002](adr/ADR-0002-depth-contract.md) | 2026-08-24 | accepted | A day is a hub plus one document per subtopic, machine-checked, with no clocks anywhere. |
| [ADR-0003](adr/ADR-0003-zero-cost-and-local-first.md) | 2026-08-24 | accepted | Zero cost, local-first, open-source-only stack; managed services are 🅿️ parked. |
| [ADR-0004](adr/ADR-0004-fundamentals-before-ai.md) | 2026-08-24 | accepted | Eighty-four days of platform, observability and SRE come before the first model is trained. |
| [ADR-0005](adr/ADR-0005-the-paper-part.md) | 2026-08-25 | accepted | Research is taught as a part of its own — `kind: paper`, a citation block and *What it did not claim* — never as a footnote. |
