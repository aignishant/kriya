# Day 8 — Checklist

**Definition of done.** `./o done 8` reads this file and refuses to commit while any `- [ ]` remains. It
counts boxes; it cannot detect a dishonest tick (`docs/INCIDENTS.md` row 6). That part is yours.

**Demo command** — what you can do at the end of today that you could not do yesterday:

```bash
cd days/day-008-http-and-tls && CERTS=lab/certs && \
uv run uvicorn pulse.api:app --host 127.0.0.1 --port 8443 --ssl-certfile "$CERTS/expired.pem" --ssl-keyfile "$CERTS/expired.key" --log-level info > /tmp/pulse-tls.log 2>&1 & \
sleep 3; \
echo "a real, verifying client:"; curl -sS --cacert "$CERTS/ca.pem" --resolve pulse.local:8443:127.0.0.1 -o /dev/null -w '  http=%{http_code}\n' https://pulse.local:8443/healthz; echo "  curl exit=$?"; \
echo "the health check somebody 'fixed' with -k:"; curl -sSk --resolve pulse.local:8443:127.0.0.1 -o /dev/null -w '  http=%{http_code}\n' https://pulse.local:8443/healthz; \
echo "error lines in the application log:"; grep -icE 'error|expired|certificate|fail' /tmp/pulse-tls.log; \
pkill -f "port 8443"
```

A service that is completely unreachable to every real user on earth, with a health check returning `200`,
zero error lines in its log, no restarts, and a process that is listening happily. Yesterday you could
explain why a service dies with every signal green. Today you can explain why a *perfectly healthy* one is
unreachable with every signal green — and name the one flag that blinded the only instrument that could
have seen it.

---

## Setup

- [ ] **nothing from Days 4–7 still running** — `pgrep -af 'uvicorn|blackhole|hangy|hungry|burn|allocate|holder|slow_resolver'`
- [ ] **ports 8000, 8021–8026, 8443, 8444 confirmed free** before starting, not assumed
- [ ] `openssl version`, `curl --version` and `ssl.OPENSSL_VERSION` all recorded — **three separate
      versions, and they need not agree**
- [ ] **`git check-ignore -v` run against `lab/certs/ca.key` BEFORE the key exists**, and confirmed covered by the Day 0 rule (Principle 9)
- [ ] `pulse.local` either resolves, **or** the decision to use `https://localhost:8443` throughout is
      written down
- [ ] `./o check` green and `git status --short` clean before breaking anything
- [ ] `./o scaffold 8` has created the day's `lab/`, and `lab/certs/` exists
- [ ] no packages added, and `git diff pyproject.toml uv.lock` confirms it — **fifth day running**

---

## Section 1 — `01-the-message`

- [ ] **1.1** read · `lab/by_hand.py` written · **an HTTP request typed as literal bytes, with no HTTP
      library anywhere**
- [ ] **1.1** `lab/by_hand_post.py` written · `Content-Length` computed from the **encoded** bytes
- [ ] **1.1** the blank line understood as **the frame boundary**, and the response's `content-length`
      counted against the actual body length
- [ ] **1.1** all four failures produced: **wrong length · missing `Host` · bare `\n` · nothing sent at all**
- [ ] **1.1** `TODO(me)` — a `Content-Length` larger than the body sent, and what the server did recorded
- [ ] **1.1** answered out loud: *name the two framing mechanisms, say which needs the size in advance, and
      say what a server does with leftover bytes*
- [ ] **1.2** read · `lab/methods.py` written · **`PUT` three times and `POST` three times, compared**
- [ ] **1.2** the state reset between the two loops — **an unreset drill measures the previous drill**
- [ ] **1.2** `3 3 3` versus `3 6 9` seen, not assumed
- [ ] **1.2** the idempotency-key version written, and **the key changed on the third request** to prove
      per-attempt keys de-duplicate nothing
- [ ] **1.2** `TODO(me)` — `pulse`'s three routes audited for safe / idempotent / retryable, **written into
      `docs/ARCHITECTURE.md`**
- [ ] **1.2** answered out loud: *define both terms without using either in its own definition, and explain
      why `DELETE` returning `404` on the second call is still idempotent*
- [ ] **1.3** read · `lab/codes.py` written · **six paths, six codes**
- [ ] **1.3** confirmed that **only `/boom` produced a traceback** — the other five were decisions
- [ ] **1.3** `Retry-After` and `WWW-Authenticate` both seen in the response headers, not just described
- [ ] **1.3** the `502` / `504` distinction stated as **"the proxy said it, not you"**
- [ ] **1.3** `TODO(me)` — a fifth status code `pulse` could legitimately return, produced deliberately
- [ ] **1.3** answered out loud: *the difference between `502` and `504`, and why grepping your own log for
      "502" finds nothing*
- [ ] **1.4** read · `lab/headers.py` written · **with the redaction denylist, before running it once**
- [ ] **1.4** the raw request `curl` sends seen on the wire — **three headers you did not write**
- [ ] **1.4** `client` and `x-forwarded-for` observed **disagreeing**, and which is the fact identified
- [ ] **1.4** `authorization` confirmed `<redacted>` in the echoed output
- [ ] **1.4** `Cache-Control: no-store` understood as **the containment for this endpoint's capability**
- [ ] **1.4** answered out loud: *three headers a proxy must not forward and what they share; why
      `X-Forwarded-For` is safe to log and unsafe to authorise on*
- [ ] **1.5** read · `lab/liar.py` written · **both endpoints, one shared failure**
- [ ] **1.5** twenty requests to each, **counted by status code the way an exporter counts**
- [ ] **1.5** `TODO(me)` — **both availability figures computed and written into `docs/INCIDENTS.md`**
- [ ] **1.5** `raise_for_status()` seen raising on one and not the other
- [ ] **1.5** understood that **the fix cannot be made in the metrics layer** — the information is destroyed
      at the boundary
- [ ] **1.5** answered out loud: *name four systems blinded by a lying `200`, and the one signal that would
      still have caught it*

---

## Section 2 — `02-the-connection`

- [ ] **2.1** read · `lab/two_on_one.py` written · **two requests, one local port, printed both times**
- [ ] **2.1** `time_connect=0.000000` confirmed on the second request — **the proof, not the claim**
- [ ] **2.1** the connection watched **outliving the request** and then closing on its own after
      `--timeout-keep-alive`
- [ ] **2.1** the framing consequence understood: **persistent connections make `Content-Length`
      mandatory**
- [ ] **2.1** answered out loud: *what resource keep-alive spends, what its exhaustion looks like, and why a
      new healthy replica can receive no traffic at all*
- [ ] **2.2** read · `lab/slowdep.py` and `lab/pool.py` written
- [ ] **2.2** `TODO(me)` — **all three end-to-end numbers predicted in writing before running them**
- [ ] **2.2** pools of 20, 5 and 2 run against identical load, and `ceil(20 ÷ pool) × delay` confirmed
- [ ] **2.2** the third line's `0.00s` understood as **the library cannot separate the wait from the work**
- [ ] **2.2** the downstream-slowdown direction run too (0.1 · 0.5 · 2.0), and the amplification seen
- [ ] **2.2** `PoolTimeout` recognised as **the good outcome** — the queue becoming visible
- [ ] **2.2** answered out loud: *where the latency is spent, and which half appears in your traces*
- [ ] **2.3** read · head-of-line blocking demonstrated with `MAX_CONNECTIONS=1`
- [ ] **2.3** ALPN watched deciding the version — `version=2` over TLS, `version=1.1` on plain HTTP
- [ ] **2.3** eight requests over **one** HTTP/2 connection, versus eight over HTTP/1.1
- [ ] **2.3** understood that **`SETTINGS_MAX_CONCURRENT_STREAMS` is a limit the server sets and your client
      does not expose**
- [ ] **2.3** the load-balancing consequence stated: **connection-level balancing cannot balance HTTP/2**
- [ ] **2.3** answered out loud: *the head-of-line blocking HTTP/2 removes and the one it does not, and why
      it can be worse on a lossy network*
- [ ] **2.4** read · `lab/race.py` written · **`pulse` started with `--timeout-keep-alive 2`**
- [ ] **2.4** the race run **six times with the wrong ordering** — at least one failure seen
- [ ] **2.4** the race run **six times with the right ordering** — zero failures
- [ ] **2.4** `CLOSE_WAIT` found on the client side, and understood as *"the pool is holding a dead socket"*
- [ ] **2.4** the ordering rule stated in one sentence, **as a rule and not a value**
- [ ] **2.4** `TODO(me)` — one client library's idle timeout looked up and compared against uvicorn's 5
- [ ] **2.4** answered out loud: *why your application log has no evidence, whose log does, and what
      correlation distinguishes this from a capacity problem*

---

## Section 3 — `03-tls`

- [ ] **3.1** read · a real TLS connection made, and **protocol · cipher · bits · subject · issuer** all
      printed
- [ ] **3.1** the integrity check seen **refusing tampered bytes**, injected into the underlying socket
- [ ] **3.1** the three promises stated, **and three things TLS does not provide named**
- [ ] **3.1** understood that **the credential leaked to a log was still safe in transit** — Day 9's boundary
- [ ] **3.1** answered out loud: *why encryption without authentication is worth almost nothing*
- [ ] **3.2** read · the phase breakdown measured with `curl`'s `%{time_*}` variables
- [ ] **3.2** **the values read as cumulative, not as durations**, and `appconnect − connect` computed
- [ ] **3.2** a reused connection confirmed at `tcp=0 tls=0`
- [ ] **3.2** five separate handshakes timed, and `session_reused` observed as `False` every time
- [ ] **3.2** `TODO(me)` — **the internet number and the loopback number both written into
      `docs/PACKAGES.md`**
- [ ] **3.2** answered out loud: *the three phases, the round-trip count, and why 0-RTT must be restricted
      to idempotent requests*
- [ ] **3.3** read · a real chain pulled apart with `-showcerts`, and **`s:` / `i:` read as links**
- [ ] **3.3** confirmed that **the server does not send the root**, and where the root came from instead
- [ ] **3.3** `subjectAltName`, `basicConstraints` and the dates read out of one certificate
- [ ] **3.3** `certifi.where()` located, **and the bundle actually opened**
- [ ] **3.3** `TODO(me)` — **roots counted, three organisations named**, and what it would mean if one issued
      for your domain
- [ ] **3.3** answered out loud: *what a signature proves; why a self-signed root is not circular; which
      field matches a hostname and which is ignored*
- [ ] **3.4** read · the same address queried **with and without SNI**, two different certificates seen
- [ ] **3.4** `--resolve` used correctly, and **the IP-in-the-URL failure produced deliberately**
- [ ] **3.4** the two independent hostnames distinguished: **SNI picks the certificate, `Host` picks the
      route**
- [ ] **3.4** the wildcard rule stated: **one wildcard, one label, leftmost only**
- [ ] **3.4** answered out loud: *why the `Host` header cannot select a certificate, and what happens when
      the two names disagree*
- [ ] **3.5** read · **each of the two checks failed independently** — valid chain with wrong name, right
      name with no chain
- [ ] **3.5** all four badssl endpoints run **both ways**, and the four identical `200`s seen
- [ ] **3.5** the silence confirmed with `-W all` and `DEBUG` logging — **no warning exists**
- [ ] **3.5** the correct alternative read and understood **before** section 5 needs it
- [ ] **3.5** the three situations that produce the temptation named, **with the right answer to each**
- [ ] **3.5** answered out loud: *two checks, an example that passes one and fails the other, and why this
      is worse than an ordinary bug*

---

## Section 4 — `04-certificates-in-time`

- [ ] **4.1** read · `notBefore` and `notAfter` read off a real certificate
- [ ] **4.1** `-checkend` used at four horizons, **and the remaining lifetime located by bisection**
- [ ] **4.1** `lab/certcheck.py` written · **the exit code is the interface**, not the printed text
- [ ] **4.1** an **already-expired** host included, and confirmed that it **errors rather than reporting a
      number**
- [ ] **4.1** understood that **"could not check" must fail, not go blank** (Principle 10)
- [ ] **4.1** the CA/Browser Forum schedule read **live**, and today's maximum confirmed as 200 days
- [ ] **4.1** `TODO(me)` — **two threshold pairs decided, with arithmetic**, for 200 days and for 47
- [ ] **4.1** answered out loud: *why this is a correct cause-based alert; the failure where renewal
      succeeds and the site still goes down*
- [ ] **4.2** read · `lab/check_renewal.py` written · **the decision uses the certificate's own declared
      lifetime**
- [ ] **4.2** two certificates generated with different lifetimes, and **both exit codes seen**
- [ ] **4.2** the four steps named, **and the two that fail silently identified**
- [ ] **4.2** HTTP-01 and DNS-01 distinguished, **including which one works for an internal service and
      which gets wildcards**
- [ ] **4.2** the DNS-01 propagation race connected back to **Day 7's negative caching**
- [ ] **4.2** the reload failure reproduced: **file on disk and served certificate confirmed different**
- [ ] **4.2** the DNS-credential blast radius read and understood, **including what `CAA` records bound**
- [ ] **4.2** answered out loud: *the four steps, which two are silent, and why the check must not read the
      file on disk*
- [ ] **4.3** read · `MSYS_NO_PATHCONV=1` exported **before** the first `openssl req`
- [ ] **4.3** a CA built, and `subject == issuer` observed as the definition of self-signed
- [ ] **4.3** the good certificate issued with **three SANs**, and `openssl verify` returning `OK`
- [ ] **4.3** **all three broken certificates generated**: expired · wrong name · untrusted issuer
- [ ] **4.3** `openssl verify` seen returning **`OK` for the name-mismatch certificate** — and why understood
- [ ] **4.3** error **10** and error **20** noted as distinct numeric codes
- [ ] **4.3** `lab/reject_drill.sh` written **with `set -uo pipefail` and not `-e`**, and why understood
- [ ] **4.3** the `PEM lib` failure produced on purpose, and **the public-key hash comparison used to
      diagnose it**
- [ ] **4.3** `fullchain.pem` built by concatenation, and the certificate count compared with the leaf-only
      file
- [ ] **4.3** answered out loud: *the three causes and their three different fixes; the one command that
      separates a missing intermediate from a missing root*

---

## Section 5 — `05-pulse-on-tls`

- [ ] **5.1** read · `lab/terminator.py` written · **`STRIP_INBOUND` present before it was ever run**
- [ ] **5.1** the two-hop arrangement started, and both ports confirmed listening
- [ ] **5.1** a **spoofed** `X-Forwarded-For` sent through the proxy and confirmed **stripped and replaced**
- [ ] **5.1** the same header sent **directly to the upstream** and confirmed **accepted untouched**
- [ ] **5.1** understood that **the header is not the control — the trust list is**
- [ ] **5.1** the four facts that become claims listed, **with what each becomes**
- [ ] **5.1** `--forwarded-allow-ips` default of `127.0.0.1` read from the official documentation, not
      assumed
- [ ] **5.1** `TODO(me)` — **the header contract for `pulse` written: strip / add / forward, three lists**
- [ ] **5.1** answered out loud: *the two-part trust rule, and why the half people forget is the one that
      matters*
- [ ] **5.2** read · `pulse` started with `--ssl-certfile` and `--ssl-keyfile`
- [ ] **5.2** `https://` confirmed in uvicorn's startup line — **read, not skipped**
- [ ] **5.2** **all three wrong ways tried first**: plain HTTP to a TLS port · HTTPS with no CA · the right
      name with no CA
- [ ] **5.2** the right way run with `--cacert`, and the **loopback handshake cost** measured
- [ ] **5.2** `lab/tls_client.py` written with `create_default_context(cafile=...)` and **all four timeouts
      named**
- [ ] **5.2** **all four certificates served in turn against the same trusted CA** — one `200`, three
      refusals
- [ ] **5.2** `grep -rn "verify=False\|--insecure" lab/` run and **returning nothing**
- [ ] **5.2** confirmed `pulse/api.py` unchanged — `git diff pulse/` empty
- [ ] **5.2** answered out loud: *why no application code changed; the three ways to trust a certificate and
      what the other two would have cost*
- [ ] **5.3** read · **Act 1 baseline recorded** with a verified client before anything was broken
- [ ] **5.3** Act 2 run · **uvicorn confirmed starting cleanly with a certificate expired over a year ago**
- [ ] **5.3** `lab/expiry_drill.sh` written · **all six observations recorded before any conclusion drawn**
- [ ] **5.3** observation 1: `http=000`, `exit=60` — **and understood as "no HTTP response at all"**
- [ ] **5.3** observation 2: `http=200` from the `-k` health check
- [ ] **5.3** observation 3: process `LISTENING`
- [ ] **5.3** observation 4: **zero** matching log lines
- [ ] **5.3** observation 5: **only the health check** in the access log
- [ ] **5.3** observation 6: the expired `notAfter`, read with a tool that deliberately does not verify
- [ ] **5.3** **the fix run and the drill re-run** — rows 1 and 2 now agreeing
- [ ] **5.3** `SIGHUP` tried, **and confirmed NOT to reload the certificate** — a restart is required
- [ ] **5.3** the two-line `-checkend` detector built and seen **exiting 0 then 1**
- [ ] **5.3** answered out loud: *how a service can be unreachable with a zero error rate; the flag that
      blinded the check; why the detector must live outside the process*

---

## Both red gates

- [ ] **Gate one** — `reject_drill.sh` produced **one `200` and three DIFFERENT refusal reasons** under
      `verify=ON`
- [ ] **Gate one, the dark half** — the same four produced **four identical `200`s** under `verify=OFF`
- [ ] **Gate two** — the expiry drill produced **`http=000` / `exit=60` for a real client while the `-k`
      health check returned `200`**
- [ ] **Gate two, green half** — after restarting with `good.pem`, **observations 1 and 2 agree**
- [ ] neither gate produced a false pass: the certificates genuinely differ in one variable each, and
      nothing else on this machine was listening on 8443

---

## The pattern across four days

- [ ] `TODO(me)` — **one paragraph written** on what Day 5's disk, Day 6's OOM kill, Day 7's connection
      exhaustion and today's expired certificate have in common
- [ ] the shared property named: **four unrelated mechanisms, one dashboard that stayed green**
- [ ] the kind of check that would have caught **all four** named, and **Day 12 and Day 62 identified as
      where that gap starts closing**

---

## Cost & cleanup

- [ ] `0` model calls, `0` tokens, `0` CI minutes confirmed, not assumed
- [ ] **`0` packages added** — `git diff pyproject.toml uv.lock` empty, fifth day running
- [ ] **no request was ever pointed at anything but loopback, `rfc-editor.org`, `iana.org` or `badssl.com`**
      — checked, not remembered
- [ ] **`netstat -ano | grep -E ':(80(0[0-9]|2[0-6])|844[34]).*LISTENING'` returns nothing** — no server
      survives
- [ ] `pkill -f` verified with `netstat` rather than trusted
- [ ] `/tmp/pulse-tls.log` and `/tmp/body.json` removed
- [ ] **`days/day-008-http-and-tls/lab/certs/` DELETED** — the CA private key does not survive the day
- [ ] `git status --short` clean, and **`git log --all -- '*ca.key'` returns nothing** — the key never
      reached history
- [ ] **`pulse` confirmed unmodified** — `git diff pulse/` is empty

---

## Ledger & commit

- [ ] `docs/PACKAGES.md` — **three rows appended** (openssl version · the two handshake measurements ·
      uvicorn's keep-alive default)
- [ ] `docs/INCIDENTS.md` — **three rows appended, first symptom written before the cause** (rows 11, 12, 13)
- [ ] **row 13 explicitly linked to Day 7's row 22, Day 6's row 19 and Day 5's row 16** — four consecutive
      days of a green dashboard over a dead service
- [ ] `docs/DECISIONS.md` — an ADR written **if** the header-contract `TODO(me)` reached a conclusion about
      where `pulse` terminates TLS
- [ ] `docs/PROGRESS.md` — the Day 8 row pasted from the hub's §11
- [ ] `./o check` green
- [ ] `./o depth 8` green
- [ ] `./o trace` shows **FND-10** closed and nothing else newly closed
- [ ] committed: `day 008: HTTP and TLS in production — the message, the connection, the certificate — closes FND-10`
- [ ] the commit hash written back into `docs/PROGRESS.md` and the hub's frontmatter `commit:` field
