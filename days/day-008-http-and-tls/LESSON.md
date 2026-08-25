---
day: 8
phase: 1
phase_name: "The production mental model and the machine"
title: "HTTP and TLS in production"
ids: [FND-10]
principles: [1, 2, 4, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18]
kind: lab
plan_version: "v1.1.0"
parts: 20
generated: "2026-08-25"
status: written
lab_scaffolded: false
commit: "pending"
---

# Day 8 — HTTP and TLS in production — the message, the connection, the certificate, and the date that ends it

> **Yesterday (Day 7):** how one program reaches another — ports, names, connections — and the single most
> consequential number in distributed systems: how long you are willing to wait. It ended with `pulse`
> completely unreachable, killed by forty requests to a dependency that was up and silent, with every
> signal green.
> **Today:** the protocol that actually rides on those connections. What a request *is*, what a status code
> *promises*, what a connection *costs*, and then the layer underneath it that decides whether anyone is
> willing to talk to you at all — ending with `pulse` unreachable again, by a completely different
> mechanism, with every signal green again.
> **Tomorrow (Day 9):** configuration and secrets — the twelve-factor service, `.env`, and code that
> refuses to start rather than failing late.

---

## §1 Where we are

For seven days you have been looking at pipes. Today you look at what goes down them.

Here is the whole day in one image. Imagine a building where every request is a paper form dropped through
a slot. The form has a fixed shape: what you want on the first line, some notes underneath, a gap, then
anything bulky. That shape is the only reason a request can be forwarded, logged, cached, counted or argued
about by six people who never met — and it is the first half of today.

The second half is the door.

Before the form goes through the slot, there is a ritual. The visitor says who they are here to see. The
building produces a card proving it is the building it claims to be, signed by somebody the visitor already
trusts. They agree on a code for the rest of the conversation. Only then does the slot open.

The ritual costs a little time on the way in and nothing afterwards, which is why you do it once per
visitor rather than once per form. **And the card has a date on it.**

That date is the whole of the last section. Not an expiry that degrades, not a warning that gets louder —
a date, after which every visitor on earth turns around at the door simultaneously. **The building is fine.
The people inside are fine. The forms would be processed perfectly.** And nobody can get in.

Today ends with that happening to `pulse`, on purpose, while the health check reports `200` — because the
health check was set up by somebody helpful who added one flag to make a certificate warning go away.

**This is the fourth day running that ends with the service down and the dashboard green.** Day 5's disk
that did not free, Day 6's silent kill, Day 7's exhausted connections, and today's expired date. Four
unrelated mechanisms, one dashboard, and by now that should be irritating rather than surprising. **The
irritation is the point**, and Day 12 and Day 62 are where you start closing it.

---

## §2 The map

**Section 1 — `01-the-message`.** What one HTTP exchange actually is: the bytes, the verbs, the verdicts and
the metadata. The layer everything else in this plan produces or consumes.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A request is text with a shape](parts/01-the-message/1.1-a-request-is-text-with-a-shape.md) | TCP has no message boundaries — so how does a server know where your request ends? | foundation |
| 1.2 | [Methods, safety and idempotency](parts/01-the-message/1.2-methods-safety-and-idempotency.md) | your request timed out — is it safe to send it again? | foundation |
| 1.3 | [The status codes an operator reads](parts/01-the-message/1.3-the-status-codes-an-operator-reads.md) | `500`, `502`, `503`, `504` — which of those is your problem and which is somebody else's? | working |
| 1.4 | [Headers are the contract](parts/01-the-message/1.4-headers-are-the-contract.md) | which of these values did you observe, and which did the caller simply type? | working |
| 1.5 | [The status code that lied](parts/01-the-message/1.5-the-status-code-that-lied.md) | your availability says 100% and the product is down — how? | production |

**Section 2 — `02-the-connection`.** HTTP as something that runs over a connection with a lifetime, a pool
and two independent opinions about when to close.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Keep-alive and the connection you reuse](parts/02-the-connection/2.1-keep-alive-and-the-connection-you-reuse.md) | what does a handshake per request actually cost, and what does reuse spend instead? | foundation |
| 2.2 | [The connection pool and its limits](parts/02-the-connection/2.2-the-connection-pool-and-its-limits.md) | your p99 doubled and the downstream is unchanged — where did the time go? | working |
| 2.3 | [HTTP/2 multiplexing and what it does not fix](parts/02-the-connection/2.3-http2-multiplexing-and-what-it-does-not-fix.md) | you enabled HTTP/2 and one pod is doing all the work — why? | working |
| 2.4 | [The idle timeout race and the phantom 502](parts/02-the-connection/2.4-the-idle-timeout-race-and-the-phantom-502.md) | a steady 0.1% of `502`s that nobody can reproduce — what is the shape of that bug? | production |

**Section 3 — `03-tls`.** The layer underneath: what it promises, what it costs, and how a stranger's
certificate ever means anything.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [What TLS actually promises](parts/03-tls/3.1-what-tls-actually-promises.md) | the padlock is showing — what exactly has been proved to you? | foundation |
| 3.2 | [The handshake and what it costs](parts/03-tls/3.2-the-handshake-and-what-it-costs.md) | how much of a fresh HTTPS request is setup rather than work? | working |
| 3.3 | [The certificate and the chain of trust](parts/03-tls/3.3-the-certificate-and-the-chain-of-trust.md) | why is a self-signed root at the top of the chain not circular reasoning? | foundation |
| 3.4 | [SNI — one address, many certificates](parts/03-tls/3.4-sni-one-address-many-certificates.md) | one address serves forty names — how does the server know which certificate to send? | working |
| 3.5 | [Verification, and the flag that turns it off](parts/03-tls/3.5-verification-and-the-flag-that-turns-it-off.md) | one flag makes four different failures disappear — what did you actually give up? | production |

**Section 4 — `04-certificates-in-time`.** A certificate is a promise with an end date. What that date does,
what renews it, and the three ways one gets rejected.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [Expiry is a date, not a warning](parts/04-certificates-in-time/4.1-expiry-is-a-date-not-a-warning.md) | why is this the one outage whose exact timestamp you can know months ahead? | working |
| 4.2 | [Renewal, and the automation that must not fail](parts/04-certificates-in-time/4.2-renewal-and-the-automation-that-must-not-fail.md) | renewal succeeded and the site went down anyway — which step failed? | production |
| 4.3 | [The three ways a certificate is rejected](parts/04-certificates-in-time/4.3-the-three-ways-a-certificate-is-rejected.md) | three causes, three fixes, and one flag that hides all of them — which do you have? | production |

**Section 5 — `05-pulse-on-tls`.** Putting it on the service. Where the encryption stops, how to serve it
honestly, and the drill that takes `pulse` down with a date.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 5.1 | [Where TLS terminates, and what you stop seeing](parts/05-pulse-on-tls/5.1-where-tls-terminates-and-what-you-stop-seeing.md) | which facts about a request become claims once a proxy decrypts it? | production |
| 5.2 | [Serving `pulse` over TLS on purpose](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md) | how do you trust your own certificate without disabling verification? | production |
| 5.3 | [The certificate that expired on a Sunday](parts/05-pulse-on-tls/5.3-the-certificate-that-expired-on-a-sunday.md) | the service is unreachable and the error rate is zero — how are both true? | production |

---

## §3 Setup — run this

**Profile:** `core` only (Addendum 02 §4) — `pulse` plus this day's lab servers, which are all plain uvicorn
processes. **Nothing else may be running.**

**Stop first.** Today runs up to three uvicorn processes at once, and this machine has four logical CPUs
(`docs/PACKAGES.md`, Day 0). Anything left over from Days 4–7 will make the handshake timings in
[3.2](parts/03-tls/3.2-the-handshake-and-what-it-costs.md) meaningless:

```bash
# 1 — nothing from previous days survives
pgrep -af 'uvicorn|blackhole|hangy|hungry|burn|allocate|holder|slow_resolver' || echo "clean"
pkill -f 'blackhole|hangy|hungry|burn|allocate|holder|slow_resolver' 2>/dev/null

# 2 — the ports this day uses must be free, confirmed rather than assumed
netstat -ano | grep -E ':(8000|8021|8022|8023|8024|8025|8026|8443|8444).*LISTENING' || echo "all ports free"

# 3 — this day's scratch folder
./o scaffold 8
mkdir -p days/day-008-http-and-tls/lab/certs
```

**Secrets before the secret exists (Principle 9).** Section 4 generates a certificate authority **private
key**. It must never be committable, and the ignore rule goes in *before* the file:

```bash
# 4 — CONFIRM the ignore covers the key BEFORE the key exists. Do not skip this.
sed -n '1,15p' .gitignore
git check-ignore -v days/day-008-http-and-tls/lab/certs/ca.key \
  && echo "✅ covered by a rule written on Day 0, before any of today's files existed" \
  || echo "⚠️ NOT IGNORED — stop and fix .gitignore before generating anything"
```

**Day 0 already wrote `*.pem` and `*.key` into `.gitignore`, before either kind of file existed anywhere in
this repository.** Today is the first day those rules protect a real private key, and confirming that a rule
written nine days ago covers a file invented today is the whole of Principle 9 — **not adding the rule now,
which would be too late by the width of one `git add -A`.** If the check above fails, fix `.gitignore` and
re-run it before continuing; do not generate a key against an unverified ignore.

**Name resolution for the Python client.** `curl --resolve` handles the shell examples; `httpx2` has no
equivalent, so [5.2](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md)'s client needs
`pulse.local` to resolve. Either add the hosts entry, **or** use `https://localhost:8443` throughout — the
certificate covers both:

```bash
# 5 — OPTIONAL. Requires an elevated editor on Windows; skip it and use localhost instead.
#     C:\Windows\System32\drivers\etc\hosts   ->   127.0.0.1  pulse.local
ping -n 1 pulse.local >/dev/null 2>&1 && echo "pulse.local resolves" || echo "pulse.local does NOT resolve — use https://localhost:8443 in 5.2"
```

**Tools, verified live on 2026-08-25** (Principle 7 — look them up yourself rather than copying):

```bash
# 6 — what you actually have
openssl version
curl --version | head -1
uv run python -c "import httpx2, ssl; print('httpx2', httpx2.__version__); print(ssl.OPENSSL_VERSION)"
```

| Tool | Observed here | How | Why today needs it |
| --- | --- | --- | --- |
| openssl | `3.5.6 7 Apr 2026` | `openssl version` | already installed with Git for Windows — **no package is added today** |
| curl | `8.16.0` | `curl --version` | the phase-timing instrument in [3.2](parts/03-tls/3.2-the-handshake-and-what-it-costs.md) |
| httpx2 | `2.12.0` | pinned on [Day 3](../day-003-pulse-v0/LESSON.md) | the verifying client throughout section 5 |

⚠️ **`uv add` is not run today.** Everything uses the standard library's `ssl` module, `openssl` that
already exists, and the three packages Day 3 pinned. `git diff pyproject.toml uv.lock` must be empty at the
end — **the fifth consecutive day with no new dependency.**

---

## §4 Build brief

No project code. **`pulse/api.py` is not modified today — not one line**, and that is the argument
[5.2](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md) makes: TLS is a deployment concern.
Everything you write lives in this day's `lab/` and is deleted at the end.

| File | Explained in | What it is |
| --- | --- | --- |
| `lab/by_hand.py` · `lab/by_hand_post.py` | [1.1](parts/01-the-message/1.1-a-request-is-text-with-a-shape.md) | **Yours to write** — an HTTP request as literal bytes, with no HTTP library |
| `lab/methods.py` | [1.2](parts/01-the-message/1.2-methods-safety-and-idempotency.md) | **Yours to write** — three endpoints, one character apart, three contracts |
| `lab/codes.py` | [1.3](parts/01-the-message/1.3-the-status-codes-an-operator-reads.md) | **Yours to write** — one endpoint per status code worth knowing |
| `lab/headers.py` | [1.4](parts/01-the-message/1.4-headers-are-the-contract.md) | **Yours to write** — an echo endpoint with a redaction denylist |
| `lab/liar.py` | [1.5](parts/01-the-message/1.5-the-status-code-that-lied.md) | **Yours to write** — the same failure, reported two ways |
| `lab/two_on_one.py` | [2.1](parts/02-the-connection/2.1-keep-alive-and-the-connection-you-reuse.md) | **Yours to write** — two requests, one connection, one port number |
| `lab/slowdep.py` · `lab/pool.py` | [2.2](parts/02-the-connection/2.2-the-connection-pool-and-its-limits.md) | **Yours to write** — a bounded pool, and the queue nobody measures |
| `lab/race.py` | [2.4](parts/02-the-connection/2.4-the-idle-timeout-race-and-the-phantom-502.md) | **Yours to write** — the idle window, produced on purpose |
| `lab/certcheck.py` | [4.1](parts/04-certificates-in-time/4.1-expiry-is-a-date-not-a-warning.md) | **Yours to write** — days remaining, read from the wire, exit code as the interface |
| `lab/check_renewal.py` | [4.2](parts/04-certificates-in-time/4.2-renewal-and-the-automation-that-must-not-fail.md) | **Yours to write** — the renewal decision as a fraction of the lifetime |
| `lab/certs/*` | [4.3](parts/04-certificates-in-time/4.3-the-three-ways-a-certificate-is-rejected.md) | **Yours to generate** — a CA, one good certificate, three broken ones |
| `lab/reject_drill.sh` | [4.3](parts/04-certificates-in-time/4.3-the-three-ways-a-certificate-is-rejected.md) | **Yours to write** — four certificates, one verifying client, red gate one |
| `lab/terminator.py` | [5.1](parts/05-pulse-on-tls/5.1-where-tls-terminates-and-what-you-stop-seeing.md) | **Yours to write** — a minimal TLS-terminating proxy that strips before it adds |
| `lab/tls_client.py` | [5.2](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md) | **Yours to write** — a client that trusts your CA and nothing more |
| `lab/expiry_drill.sh` | [5.3](parts/05-pulse-on-tls/5.3-the-certificate-that-expired-on-a-sunday.md) | **Yours to write** — six observations, red gate two |
| `docs/PACKAGES.md` rows | §11 | **Yours to write** — three measurement rows |
| `docs/INCIDENTS.md` rows | §11 | **Yours to write** — three rows, first symptom before cause |

**`TODO(me)` — the reps this day leaves you:**

- `TODO(me)` In [1.1](parts/01-the-message/1.1-a-request-is-text-with-a-shape.md), send a request with a
  `Content-Length` **larger** than the body and hold the connection open. Record what the server does and
  how long it waits, and say which timeout on Day 7's list would have bounded it.
- `TODO(me)` In [1.2](parts/01-the-message/1.2-methods-safety-and-idempotency.md), audit `pulse`'s three
  routes: for each, state whether it is safe, whether it is idempotent, and whether a retry layer should be
  allowed to repeat it. **Write the answers into `docs/ARCHITECTURE.md`** — this is the table Day 19's
  rollback plan will need.
- `TODO(me)` In [1.3](parts/01-the-message/1.3-the-status-codes-an-operator-reads.md), find a fifth status
  code `pulse` could legitimately return that the part does not list. Produce it deliberately and record
  which of the four `5xx` distinctions it belongs on the other side of.
- `TODO(me)` In [1.5](parts/01-the-message/1.5-the-status-code-that-lied.md), compute the availability each
  endpoint implies over twenty requests and write **both numbers** into `docs/INCIDENTS.md`. Day 76 builds
  an error budget on one of them.
- `TODO(me)` In [2.2](parts/02-the-connection/2.2-the-connection-pool-and-its-limits.md), predict all three
  end-to-end numbers **before** running the pool comparison. Write your predictions down first; a
  prediction made afterwards is not one.
- `TODO(me)` In [2.4](parts/02-the-connection/2.4-the-idle-timeout-race-and-the-phantom-502.md), find the
  idle timeout of one client library you did not write. State whether it is longer or shorter than
  uvicorn's default of 5, and therefore whether that pairing has the window.
- `TODO(me)` In [3.2](parts/03-tls/3.2-the-handshake-and-what-it-costs.md), record the TLS handshake cost
  across the internet **and** against your own local server from
  [5.2](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md). **Both numbers go in
  `docs/PACKAGES.md`** — the gap between them is the latency-versus-CPU split, measured rather than read.
- `TODO(me)` In [3.3](parts/03-tls/3.3-the-certificate-and-the-chain-of-trust.md), open `certifi`'s bundle
  and count the roots your code trusts. Name three of the organisations. Then say what it would mean if one
  of them issued a certificate for your domain.
- `TODO(me)` In [4.1](parts/04-certificates-in-time/4.1-expiry-is-a-date-not-a-warning.md), decide the two
  alert thresholds you would set for a certificate with the **current** two-hundred-day maximum lifetime,
  and the two you would set at forty-seven days. Justify each with arithmetic rather than habit.
- `TODO(me)` In [5.1](parts/05-pulse-on-tls/5.1-where-tls-terminates-and-what-you-stop-seeing.md), write the
  header contract for `pulse`: what the edge must strip, what it must add, what it must forward untouched.
  **Three lists.** Day 37 will implement it.
- `TODO(me)` After [5.3](parts/05-pulse-on-tls/5.3-the-certificate-that-expired-on-a-sunday.md), write one
  paragraph on what Days 5, 6, 7 and 8 have in common. Four mechanisms, one dashboard. **Name the property
  they share and the kind of check that would have caught all four.**

---

## §5 The check that must be able to fail

**Two red gates today**, and they fail in opposite directions — one loudly, one silently. That contrast is
the day.

**Gate one — the three rejections** ([4.3](parts/04-certificates-in-time/4.3-the-three-ways-a-certificate-is-rejected.md)):

```bash
bash days/day-008-http-and-tls/lab/reject_drill.sh
```

Four certificates through one verifying client. **The `verify=ON` column must show one `200` and three
*different* refusal reasons.** If any two reasons match, you built two certificates with the same defect and
the drill has not covered all three. Making it go red on purpose is the whole exercise — and **the
`verify=OFF` column showing four identical `200`s is the gate that proves a flag can delete a gate.**

**Gate two — the Sunday drill** ([5.3](parts/05-pulse-on-tls/5.3-the-certificate-that-expired-on-a-sunday.md)):

```bash
bash days/day-008-http-and-tls/lab/expiry_drill.sh
```

| Observation | Broken state | Healthy state |
| --- | --- | --- |
| a verified client | `http=000`, `exit=60` | `http=200`, `exit=0` |
| the health check with `-k` | **`http=200`** | `http=200` |
| the process | `LISTENING` | `LISTENING` |
| application log lines mentioning failure | **`0`** | `0` |
| requests that reached the application | **only the health check** | all of them |
| the served certificate's `notAfter` | `Feb 1 2025` | in the future |

**Rows two through five are identical in both columns.** That is the gate: a total outage in which only
*one* of six observations changed, and it is the one nobody was watching.

**And the green half you must also see:** restart with `good.pem`, re-run, and confirm rows one and two now
agree. **A drill that only goes red has proved the failure, not the fix.**

---

## §6 Cost & quota budget

| Resource | Today | Note |
| --- | --- | --- |
| Model calls | **`0`** | no provider is contacted; no key is used |
| Tokens | **`0`** | — |
| CI minutes | **`0`** | nothing pushed today runs in CI |
| New packages | **`0`** | fifth consecutive day. `ssl` is standard library; `openssl` already exists |
| Disk | **~100 KB** | thirteen PEM files in `lab/certs/`, plus `/tmp/pulse-tls.log` |
| RAM | **~180 MB peak** | up to three uvicorn processes at roughly 60 MB each |
| CPU | six RSA key generations | a second or two each on four cores (Addendum 02 §3) |
| Network | **a few hundred KB** | `rfc-editor.org`, `iana.org`, `badssl.com` — documentation and public test hosts only. **Sections 4 and 5 are entirely offline.** |

**If you would rather send nothing outside this machine at all:** every failure in
[3.5](parts/03-tls/3.5-verification-and-the-flag-that-turns-it-off.md) is reproduced offline in
[4.3](parts/04-certificates-in-time/4.3-the-three-ways-a-certificate-is-rejected.md), and the handshake
measurement in [3.2](parts/03-tls/3.2-the-handshake-and-what-it-costs.md) can be re-run against
[5.2](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md)'s local endpoint. **You lose the
transatlantic latency number and nothing else.**

---

## §7 Traps

| # | Trap | What it looks like | Where it is covered |
| --- | --- | --- | --- |
| 1 | **`MSYS_NO_PATHCONV`** — Git Bash rewrites `/CN=...` into a Windows path | *"subject name is expected to be in the format /type0=value0/..."* | [4.3](parts/04-certificates-in-time/4.3-the-three-ways-a-certificate-is-rejected.md) · §3 |
| 2 | **`verify=False` / `-k`** — the flag that makes every certificate error vanish | four different failures become four identical `200`s | [3.5](parts/03-tls/3.5-verification-and-the-flag-that-turns-it-off.md) |
| 3 | **`openssl s_client` without `-servername`** | you debug a certificate that was never sent to you | [3.4](parts/03-tls/3.4-sni-one-address-many-certificates.md) |
| 4 | **The key in git** | `.gitignore` written *after* `ca.key` exists is too late | §3 · Principle 9 |
| 5 | **Reading `curl`'s timings as durations** | they are cumulative; TLS looks free | [3.2](parts/03-tls/3.2-the-handshake-and-what-it-costs.md) |
| 6 | **`import httpx`** instead of `httpx2` | `ModuleNotFoundError` — the naming trap from Day 3 | [Day 3, 1.3](../day-003-pulse-v0/parts/01-what-we-are-building/1.3-choosing-the-pieces-and-pinning-them.md) |
| 7 | **A stale lab server on a port** | the "new" behaviour is the old process, and you measure it three times | [2.2](parts/02-the-connection/2.2-the-connection-pool-and-its-limits.md) |
| 8 | **`x509 -subject` looks right, client still rejects** | the name must be in `subjectAltName`; `CN` is ignored | [3.3](parts/03-tls/3.3-the-certificate-and-the-chain-of-trust.md) |

**And the named trap from the plan's §5.1 that today touches: #1, the tutorial that runs on `:latest` with
no limits.** Its certificate cousin is `verify=False` — the tutorial shortcut that works immediately, teaches
nothing, survives into production, and cannot be detected afterwards because it produces no signal. **Trap 2
above is that trap, in this day's clothing.**

---

## §8 Verify before you build

Every page below was fetched on **2026-08-25**, the day this was written (Principle 8). Fetch them again on
the day you run it — **the CA/Browser Forum row in particular moves on a published schedule.**

| Fact used | Source page | What was checked |
| --- | --- | --- |
| status code definitions, safe/idempotent, `Retry-After` | `https://httpwg.org/specs/rfc9110.html` | the verbatim one-sentence definitions in [1.2](parts/01-the-message/1.2-methods-safety-and-idempotency.md) and [1.3](parts/01-the-message/1.3-the-status-codes-an-operator-reads.md) |
| CRLF, `Host`, persistent connections, framing | `https://httpwg.org/specs/rfc9112.html` | [1.1](parts/01-the-message/1.1-a-request-is-text-with-a-shape.md), [2.1](parts/02-the-connection/2.1-keep-alive-and-the-connection-you-reuse.md) |
| HTTP/2 framing and streams | `https://www.rfc-editor.org/rfc/rfc9113.html` | [2.3](parts/02-the-connection/2.3-http2-multiplexing-and-what-it-does-not-fix.md) |
| TLS 1.3 phases, the three promises, 0-RTT replay | `https://www.rfc-editor.org/rfc/rfc8446.html` | [3.1](parts/03-tls/3.1-what-tls-actually-promises.md), [3.2](parts/03-tls/3.2-the-handshake-and-what-it-costs.md) |
| X.509 validity, `basicConstraints` | `https://www.rfc-editor.org/rfc/rfc5280.html` | [3.3](parts/03-tls/3.3-the-certificate-and-the-chain-of-trust.md), [4.1](parts/04-certificates-in-time/4.1-expiry-is-a-date-not-a-warning.md) |
| **CN must not be used for hostname matching** | `https://www.rfc-editor.org/rfc/rfc9525.html` | [3.3](parts/03-tls/3.3-the-certificate-and-the-chain-of-trust.md) |
| **maximum certificate validity is 200 days as of 2026-03-15** | `https://cabforum.org/working-groups/server/baseline-requirements/requirements/` | [4.1](parts/04-certificates-in-time/4.1-expiry-is-a-date-not-a-warning.md) — the Relevant Dates table |
| `create_default_context` defaults, `CERT_*`, `load_cert_chain` | `https://docs.python.org/3/library/ssl.html` | [3.1](parts/03-tls/3.1-what-tls-actually-promises.md), [3.5](parts/03-tls/3.5-verification-and-the-flag-that-turns-it-off.md) |
| `verify=`, `SSLContext`, exception classes | `https://www.python-httpx.org/advanced/ssl/` | [3.5](parts/03-tls/3.5-verification-and-the-flag-that-turns-it-off.md), [5.2](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md) |
| `--ssl-*`, `--timeout-keep-alive` (default 5), `--proxy-headers`, `--forwarded-allow-ips` (default `127.0.0.1`) | uvicorn settings documentation | [2.4](parts/02-the-connection/2.4-the-idle-timeout-race-and-the-phantom-502.md), [5.1](parts/05-pulse-on-tls/5.1-where-tls-terminates-and-what-you-stop-seeing.md), [5.2](parts/05-pulse-on-tls/5.2-serving-pulse-over-tls-on-purpose.md) |
| `-checkend`, `-not_after`, `-addext`, `-CA`, `-noenc` | `openssl req -help` · `openssl x509 -help` · `openssl s_client -help`, run locally on 3.5.6 | sections 4 and 5 throughout |

---

## §9 Say it in an interview

*"The thing I actually learned on the HTTP and TLS day was not the protocol — it was where the observability
ends. I broke a service by giving it an expired certificate and then wrote down what six instruments said.
The process was listening, the application log had zero error lines, there were no restarts, processor and
memory were flat, and the health check returned 200 — because somebody had put `-k` on it months earlier
when a staging certificate was broken. Meanwhile every real client got no HTTP response at all: the
handshake fails before HTTP exists, so there is no status code to count and no access log line to record.
The error rate stayed at zero during a hundred percent outage.*

*What that taught me is that some failures are structurally undetectable from inside the process, because
the information never reaches it. You need an outside-in probe that verifies properly, and a days-remaining
check read from the wire rather than from the file on disk — because the failure I have seen written up most
often is a renewal that succeeded and a server that was never reloaded, where the file is correct and the
served certificate is stale. I would treat any `-k` in a monitoring path as a defect, because it removes the
only detector for the exact failure that check exists to catch.*

*And the pattern is bigger than certificates. That was the fourth day running where I took the service down
and the dashboard stayed green — a disk that did not free, a process killed by the kernel, connections
exhausted by a silent dependency, and a date passing. Four unrelated mechanisms, one blind dashboard. I have
not run a fleet at scale, but I can tell you exactly which four things my monitoring would have missed,
because I broke them myself and wrote down what I saw before I knew the cause."*

---

## §10 Done when

`days/day-008-http-and-tls/CHECKLIST.md` — every box ticked honestly. `./o done 8` counts them and refuses
to commit while any remain, and it **cannot** detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part
is yours.

**Done is defined by understanding and green checks, not by anything else.** In particular: both red gates
must have been seen red *and* green, the certificate directory must be deleted, and `git diff pulse/` must
be empty.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — paste this row verbatim, with the commit hash filled in:

```text
| 8 | 2026-08-25 | FND-10 | 20 | <hash> | ✅ |
```

**`docs/PACKAGES.md`** — three rows, with the values *you* observed:

```text
| openssl | 3.5.6 7 Apr 2026 | 2026-08-25 | 8 | Certificate generation and inspection. Ships with Git for Windows — no package added. Observed with `openssl version`. |
| measurement: TLS handshake cost | <internet>ms across the internet / <local>ms on loopback | 2026-08-25 | 8 | The latency-versus-CPU split, measured. `curl -w '%{time_appconnect}'` minus `%{time_connect}`. Day 111 compares serving latency against this baseline. |
| measurement: uvicorn keep-alive default | 5 seconds | 2026-08-25 | 8 | `--timeout-keep-alive` default, from uvicorn's settings documentation. Every client idle timeout in this project must be strictly below it (part 2.4). |
```

**`docs/INCIDENTS.md`** — three rows. **Write the first symptom before you investigate**, not after:

```text
| 11 | 2026-08-25 | 8 | Returned `200` with `{"ok": false}` on a failed dependency (part 1.5) | ... | ... | ... | ... |
| 12 | 2026-08-25 | 8 | Client keep-alive longer than the server's, then reused an idle connection (part 2.4) | ... | ... | ... | ... |
| 13 | 2026-08-25 | 8 | Served an expired certificate while the `-k` health check stayed green (part 5.3) | ... | ... | ... | ... |
```

**Row 13 must explicitly link Day 7's row, Day 6's row and Day 5's row** — four consecutive days of a service
down with a green dashboard, with Day 12 and Day 62 named as where that gap starts closing.

**`docs/DECISIONS.md`** — an ADR **if** the header-contract `TODO(me)` from
[5.1](parts/05-pulse-on-tls/5.1-where-tls-terminates-and-what-you-stop-seeing.md) reached a conclusion about
where `pulse` terminates TLS. That is a decision Day 37 will inherit and a stranger will want the reasoning
for.

**The commit:**

```text
day 008: HTTP and TLS in production — the message, the connection, the certificate — closes FND-10
```
