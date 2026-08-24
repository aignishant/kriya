# Package & Tool Ledger — Project Kriya

Append-only. Principle 7: **never invent a version number.** Every install gets a row here with the
version actually observed, the date it was observed, the day that added it, and why. If a version
could not be looked up, the row says `TODO(<the exact lookup command>)` — never a guess.

This is not bureaucracy. On Day 232 (day-2 operations) you will upgrade something and need to know
what you had; on Day 107 you will be asked to reproduce a six-month-old prediction and this file is
half the answer.

**Also record your machine's numbers here on Day 0** (Addendum 02 §3) — RAM, disk, logical CPUs, WSL2
ceiling. Several later days ask you to reason about them.

| Package / tool | Version | Date | Day | Why |
| -------------- | ------- | ---- | --- | --- |
| git | 2.54.0.windows.1 | 2026-08-24 | 0 | Version control + Git Bash, the shell every day document is written for. Observed with `git --version`. |
| uv | 0.12.3 | 2026-08-24 | 0 | One binary owns the environment: venv + install + lock + run. Observed with `uv --version`. |
| python | 3.12.10 | 2026-08-24 | 0 | Runtime. 3.12 is the stability pick for the ML and observability libraries this plan uses. Observed with `python --version`. |
| ruff | 0.16.4 | 2026-08-24 | 0 | Lint + format, one tool. Dev dependency. `TODO(uv pip compile)` to re-verify on your own Day 0. |
| pytest | 9.1.1 | 2026-08-24 | 0 | The test runner behind `./o check`. Dev dependency. `TODO(curl -s https://pypi.org/pypi/pytest/json)` to re-verify. |
