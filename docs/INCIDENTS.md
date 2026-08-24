# Incident Ledger — Project Kriya

Append-only. **The most valuable file in this repository.**

Every failure lab and every real failure gets a row. Ninety of these 237 days end with something
deliberately broken; this is where what you saw — *before you knew the cause* — gets written down.

## Why the "first symptom" column is the important one

Debugging is a mapping problem: from the symptom you can see to the cause you cannot. Nobody is born
knowing that `CrashLoopBackOff` usually means the process exited, not that Kubernetes is broken; or
that a p99 latency spike with flat CPU is usually a lock or a downstream call; or that a drift alert
that fires the morning after a deploy is usually a broken feature pipeline rather than a changed
world.

You learn that mapping by building it, one row at a time. In six months this table is also the most
convincing document you own: a list of failures you personally caused and diagnosed beats any
certificate in any interview.

## How to fill a row

Write the **first symptom** before you investigate. Not after. The whole value is in recording what
was actually visible at the start, including the wrong thing you thought it was.

| # | Date | Day | What I broke | First symptom I saw | What it actually was | The smallest fix | What I changed so it cannot happen silently again |
| - | ---- | --- | ------------ | ------------------- | -------------------- | ---------------- | ------------------------------------------------- |
