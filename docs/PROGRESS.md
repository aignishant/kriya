# Progress Ledger — Project Kriya

Append-only. **The last row is where we actually are.** One row per *completed* day, pasted from
that day's hub §11 before `./o done N` will commit. A day with no row here is not finished, whatever
the folder looks like.

`scripts/trace.py` reads this file: an ID only counts as closed when its day has a row here **and**
that day's hub claims the ID. So this ledger is not decoration — it is what makes
`docs/TRACEABILITY.md` true.

| Day | Date | IDs closed | Parts | Commit | Gates green? |
| --- | ---- | ---------- | ----- | ------ | ------------ |
| 0 | 2026-08-24 | — | 19 | pending | ✅ |
