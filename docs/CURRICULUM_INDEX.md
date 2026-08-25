# 📇 Curriculum index — Project Kriya

_Generated 2026-08-26 by `scripts/trace.py` from the master plan's §14._
**Do not edit by hand.**

§14 answers *what does day 115 teach?* This file answers the reverse — *where do I learn
`MLO-34`?* — which is the question you have when a later day cites an ID you no longer
remember. Every ID appears exactly once; a duplicate or a missing ID is a plan bug.

## Curriculum A — Foundations & the production mental model (`FND-`) — 24 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `FND-01` | [1](../days/day-001-what-operations-actually-is/LESSON.md) | What operations actually is — the day the code met real traffic, and the repo that reme… |
| `FND-02` | [1](../days/day-001-what-operations-actually-is/LESSON.md) | What operations actually is — the day the code met real traffic, and the repo that reme… |
| `FND-03` | [2](../days/day-002-shape-of-production-system/LESSON.md) | The shape of a production system — the request path, the dependencies, the state, and t… |
| `FND-04` | [3](../days/day-003-pulse-v0/LESSON.md) | `pulse` v0 — the service you will operate for the next two hundred days |
| `FND-05` | [4](../days/day-004-linux-for-operators-i/LESSON.md) | Linux for operators I — processes, signals, exit codes, and what "the service died" rea… |
| `FND-06` | [5](../days/day-005-linux-for-operators-ii/LESSON.md) | Linux for operators II — the filesystem, permissions, the disk that fills, the log that… |
| `FND-07` | [6](../days/day-006-resources-and-the-oom-killer/LESSON.md) | Resources — CPU, memory, the OOM killer, and why your process was simply `Killed` |
| `FND-08` | [7](../days/day-007-networking-for-operators/LESSON.md) | Networking for operators — ports, sockets, DNS, TCP, and the timeout that saves the system |
| `FND-09` | [7](../days/day-007-networking-for-operators/LESSON.md) | Networking for operators — ports, sockets, DNS, TCP, and the timeout that saves the system |
| `FND-10` | [8](../days/day-008-http-and-tls/LESSON.md) | HTTP and TLS in production — status codes that mean something, keep-alive, and the cert… |
| `FND-11` | [9](../days/day-009-configuration-and-secrets/LESSON.md) | Configuration and secrets — the twelve-factor service, `.env`, and code that refuses to… |
| `FND-12` | [9](../days/day-009-configuration-and-secrets/LESSON.md) | Configuration and secrets — the twelve-factor service, `.env`, and code that refuses to… |
| `FND-13` | [10](../days/day-010-environments-and-promotion/LESSON.md) | Environments and promotion — what the word "production" actually promises |
| `FND-14` | [11](../days/day-011-version-control-for-operators/LESSON.md) | Version control for operators — the history you will read at 2am, and the commit that e… |
| `FND-15` | [12](../days/day-012/LESSON.md) | Branching, review and the change that can be reverted |
| `FND-16` | [20](../days/day-020/LESSON.md) | Measuring change — the four delivery metrics, computed from your own repository |
| `FND-17` | [229](../days/day-229/LESSON.md) | The production readiness review — the checklist you now actually understand |
| `FND-18` | [230](../days/day-230/LESSON.md) | Documentation that survives you — architecture, runbooks, decisions |
| `FND-19` | [231](../days/day-231/LESSON.md) | The handover — operating a system somebody else built |
| `FND-20` | [232](../days/day-232/LESSON.md) | Day-2 operations — upgrades, migrations, deprecations, and the long tail |
| `FND-21` | [233](../days/day-233/LESSON.md) | Capstone I — the full stack, deployed, observed and defended |
| `FND-22` | [234](../days/day-234/LESSON.md) | Capstone II — a staged incident that crosses the ML, LLM, agent and tool layers |
| `FND-23` | [235](../days/day-235/LESSON.md) | Capstone III — the audit: prove every claim in the readiness review from the repo alone |
| `FND-24` | [236](../days/day-236/LESSON.md) | What you can now say in an interview, and an honest map of what you have not learned |

## Curriculum B — Platform: containers, Kubernetes, IaC, delivery (`PLT-`) — 42 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `PLT-01` | [13](../days/day-013/LESSON.md) | The first pipeline — continuous integration that can genuinely fail |
| `PLT-02` | [13](../days/day-013/LESSON.md) | The first pipeline — continuous integration that can genuinely fail |
| `PLT-03` | [14](../days/day-014/LESSON.md) | Quality gates — lint, format, types, tests, and a gate that refuses rather than warns |
| `PLT-04` | [15](../days/day-015/LESSON.md) | Build artifacts and reproducibility — the lockfile, the hash, and the first SBOM |
| `PLT-05` | [16](../days/day-016/LESSON.md) | Versioning and releases — semantic versions, tags, changelogs, and the artifact that *i… |
| `PLT-06` | [18](../days/day-018/LESSON.md) | Deployment strategies on paper — recreate, rolling, blue/green, canary, and what each o… |
| `PLT-07` | [19](../days/day-019/LESSON.md) | Rollback is a feature — the undo you rehearse before you need it |
| `PLT-08` | [21](../days/day-021/LESSON.md) | Why containers — the "works on my machine" bug, solved and not solved |
| `PLT-09` | [22](../days/day-022/LESSON.md) | Images and layers — what is actually inside a container, and what a layer really costs |
| `PLT-10` | [23](../days/day-023/LESSON.md) | Writing the Dockerfile for `pulse` |
| `PLT-11` | [24](../days/day-024/LESSON.md) | Multi-stage builds, small images and a build cache that actually hits |
| `PLT-12` | [25](../days/day-025/LESSON.md) | Running a container — flags, volumes, networks, and `compose` for the whole local stack |
| `PLT-13` | [25](../days/day-025/LESSON.md) | Running a container — flags, volumes, networks, and `compose` for the whole local stack |
| `PLT-14` | [26](../days/day-026/LESSON.md) | Healthchecks, restart policies, and the container that lies about being up |
| `PLT-15` | [27](../days/day-027/LESSON.md) | Registries, tags and the digest you should deploy instead of `:latest` |
| `PLT-16` | [30](../days/day-030/LESSON.md) | The container failure lab — exit 137, CrashLoopBackOff, a full disk, a build that will … |
| `PLT-17` | [31](../days/day-031/LESSON.md) | Why an orchestrator — the problems `compose` stops solving |
| `PLT-18` | [32](../days/day-032/LESSON.md) | A cluster on your laptop — kind, `kubectl`, contexts, and not breaking the real one |
| `PLT-19` | [33](../days/day-033/LESSON.md) | Pods — the unit of scheduling, and why you never create one directly |
| `PLT-20` | [34](../days/day-034/LESSON.md) | Deployments and ReplicaSets — declarative desired state, and the controller that argues… |
| `PLT-21` | [35](../days/day-035/LESSON.md) | Services and cluster DNS — how a request finds a pod that keeps being replaced |
| `PLT-22` | [36](../days/day-036/LESSON.md) | ConfigMaps, Secrets and the twelve-factor service inside a cluster |
| `PLT-23` | [37](../days/day-037/LESSON.md) | Ingress — getting outside traffic in, and terminating TLS |
| `PLT-24` | [38](../days/day-038/LESSON.md) | Namespaces, labels and selectors — how a cluster stays legible at three hundred objects |
| `PLT-25` | [39](../days/day-039/LESSON.md) | `pulse` on Kubernetes — the first real deploy, from image digest to served request |
| `PLT-26` | [40](../days/day-040/LESSON.md) | The Kubernetes failure lab — ImagePullBackOff, Pending, CrashLoopBackOff, Evicted |
| `PLT-27` | [41](../days/day-041/LESSON.md) | Probes — liveness, readiness, startup, and the liveness probe that took production down |
| `PLT-28` | [42](../days/day-042/LESSON.md) | Requests, limits and quality of service — the four numbers everybody guesses |
| `PLT-29` | [43](../days/day-043/LESSON.md) | Rollouts, revisions and `rollout undo` — deployment as a state machine |
| `PLT-30` | [44](../days/day-044/LESSON.md) | Horizontal autoscaling, and why more replicas do not fix a slow model |
| `PLT-31` | [45](../days/day-045/LESSON.md) | Disruption budgets, drains, and surviving a node that goes away |
| `PLT-32` | [46](../days/day-046/LESSON.md) | Jobs and CronJobs — the batch half of every ML system |
| `PLT-33` | [47](../days/day-047/LESSON.md) | Persistent storage and StatefulSets — because models and indexes are not stateless |
| `PLT-34` | [50](../days/day-050/LESSON.md) | The resource-pressure lab — throttling, evictions and a noisy neighbour |
| `PLT-35` | [51](../days/day-051/LESSON.md) | Infrastructure as code — the idea, and the drift it exists to kill |
| `PLT-36` | [52](../days/day-052/LESSON.md) | Terraform I — providers, resources, state, and `plan` before `apply` |
| `PLT-37` | [53](../days/day-053/LESSON.md) | Terraform II — modules, variables, and the state file you must not lose |
| `PLT-38` | [54](../days/day-054/LESSON.md) | Helm — templating, values, releases, and when templating is the wrong answer |
| `PLT-39` | [55](../days/day-055/LESSON.md) | Kustomize — overlays, and one manifest set for three environments |
| `PLT-40` | [56](../days/day-056/LESSON.md) | GitOps — the cluster reconciles itself to the repository |
| `PLT-41` | [57](../days/day-057/LESSON.md) | Promotion between environments, GitOps-style — and the pull request that is a deploy |
| `PLT-42` | [60](../days/day-060/LESSON.md) | Drift and reconciliation — the `kubectl edit` you will regret, caught by the system |

## Curriculum C — Observability & SRE practice (`OBS-`) — 27 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `OBS-01` | [20](../days/day-020/LESSON.md) | Measuring change — the four delivery metrics, computed from your own repository |
| `OBS-02` | [61](../days/day-061/LESSON.md) | Observability versus monitoring — the question you cannot think of in advance |
| `OBS-03` | [62](../days/day-062/LESSON.md) | Metrics I — counters, gauges, histograms, and Prometheus' data model |
| `OBS-04` | [63](../days/day-063/LESSON.md) | Metrics II — PromQL, `rate()`, quantiles, and the lie told by an average |
| `OBS-05` | [64](../days/day-064/LESSON.md) | Instrumenting `pulse` — RED and USE, done properly and only once |
| `OBS-06` | [64](../days/day-064/LESSON.md) | Instrumenting `pulse` — RED and USE, done properly and only once |
| `OBS-07` | [65](../days/day-065/LESSON.md) | Cardinality — the label that killed the metrics backend |
| `OBS-08` | [66](../days/day-066/LESSON.md) | Dashboards that answer a question instead of showing everything |
| `OBS-09` | [67](../days/day-067/LESSON.md) | Logs I — structured logging, levels, and the correlation id that ties a request together |
| `OBS-10` | [68](../days/day-068/LESSON.md) | Logs II — shipping, indexing, retention, and what one log line actually costs |
| `OBS-11` | [69](../days/day-069/LESSON.md) | Traces I — spans, context propagation and OpenTelemetry |
| `OBS-12` | [70](../days/day-070/LESSON.md) | Traces II — sampling, tail sampling, and finding the dependency that is slow |
| `OBS-13` | [71](../days/day-071/LESSON.md) | One pipeline for everything — the collector as the single telemetry seam |
| `OBS-14` | [72](../days/day-072/LESSON.md) | The observability failure lab — the outage your dashboards cannot see |
| `OBS-15` | [73](../days/day-073/LESSON.md) | Reliability is a number — indicators, objectives and the error budget |
| `OBS-16` | [73](../days/day-073/LESSON.md) | Reliability is a number — indicators, objectives and the error budget |
| `OBS-17` | [74](../days/day-074/LESSON.md) | Choosing indicators for an ML service — and why model accuracy is not one of them |
| `OBS-18` | [75](../days/day-075/LESSON.md) | Error budget policy — the rule that ends the argument between shipping and stability |
| `OBS-19` | [76](../days/day-076/LESSON.md) | Alert on symptoms, not on causes |
| `OBS-20` | [77](../days/day-077/LESSON.md) | Alert quality — precision, recall, fatigue, and the courage to delete an alert |
| `OBS-21` | [78](../days/day-078/LESSON.md) | On-call — rotation, escalation, handover, and being humane about all three |
| `OBS-22` | [79](../days/day-079/LESSON.md) | Runbooks that work at 3am for someone who did not write the service |
| `OBS-23` | [80](../days/day-080/LESSON.md) | Incident command — roles, communication, and the timeline that writes itself |
| `OBS-24` | [81](../days/day-081/LESSON.md) | Your first incident, staged for real, on `pulse` |
| `OBS-25` | [82](../days/day-082/LESSON.md) | Postmortems without blame, and action items that actually get done |
| `OBS-26` | [83](../days/day-083/LESSON.md) | Game days — breaking it on purpose, on a schedule |
| `OBS-27` | [84](../days/day-084/LESSON.md) | Capacity and load testing — knowing your limit before your traffic finds it |

## Curriculum D — MLOps (`MLO-`) — 41 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `MLO-01` | [85](../days/day-085/LESSON.md) | What MLOps actually is — three things that change independently: code, data, model |
| `MLO-02` | [86](../days/day-086/LESSON.md) | The failure modes an ML system has that ordinary software does not |
| `MLO-03` | [87](../days/day-087/LESSON.md) | Data versioning — content addressing, and the dataset that quietly changed |
| `MLO-04` | [88](../days/day-088/LESSON.md) | Data contracts — the schema agreement at the boundary, enforced |
| `MLO-05` | [89](../days/day-089/LESSON.md) | Data quality — expectations, validation, and failing a pipeline on the data |
| `MLO-06` | [90](../days/day-090/LESSON.md) | Splits, leakage, and the evaluation number you are allowed to believe |
| `MLO-07` | [91](../days/day-091/LESSON.md) | Feature engineering as code — and the training/serving skew it creates |
| `MLO-08` | [92](../days/day-092/LESSON.md) | Feature stores — what they solve, and when a table is genuinely enough |
| `MLO-09` | [93](../days/day-093/LESSON.md) | Pipelines — DAGs, orchestration, idempotency and backfills |
| `MLO-10` | [93](../days/day-093/LESSON.md) | Pipelines — DAGs, orchestration, idempotency and backfills |
| `MLO-11` | [94](../days/day-094/LESSON.md) | Scheduling and dependencies — the nightly job that must never run twice |
| `MLO-12` | [95](../days/day-095/LESSON.md) | `pulse`'s data pipeline, end to end and re-runnable |
| `MLO-13` | [96](../days/day-096/LESSON.md) | The data failure lab — silent corruption, late data, duplicates, a changed unit |
| `MLO-14` | [97](../days/day-097/LESSON.md) | Reproducible training — seeds, environments, and a run you can run again in a year |
| `MLO-15` | [98](../days/day-098/LESSON.md) | Experiment tracking — runs, parameters, metrics, artifacts, and one place to compare them |
| `MLO-16` | [99](../days/day-099/LESSON.md) | The model registry — stages, lineage, and a single answer to "what is in production?" |
| `MLO-17` | [100](../days/day-100/LESSON.md) | Model cards, and the questions a reviewer asks before they approve |
| `MLO-18` | [101](../days/day-101/LESSON.md) | Offline evaluation — the metric that matches the business, slices, and an honest baseline |
| `MLO-19` | [101](../days/day-101/LESSON.md) | Offline evaluation — the metric that matches the business, slices, and an honest baseline |
| `MLO-20` | [102](../days/day-102/LESSON.md) | Validation gates — the check that refuses to promote a worse model |
| `MLO-21` | [103](../days/day-103/LESSON.md) | Continuous training — what should trigger a retrain, and what should not |
| `MLO-22` | [104](../days/day-104/LESSON.md) | CI for models — testing the data, the training code, and the model itself |
| `MLO-23` | [105](../days/day-105/LESSON.md) | Packaging a model — formats, artifacts, and the pickle that will not load next month |
| `MLO-24` | [106](../days/day-106/LESSON.md) | Model versioning, and staying compatible with the code that calls it |
| `MLO-25` | [107](../days/day-107/LESSON.md) | Reproducing a six-month-old prediction — the audit request, answered |
| `MLO-26` | [108](../days/day-108/LESSON.md) | The training failure lab — non-determinism, a drifted dependency, a lost run |
| `MLO-27` | [109](../days/day-109/LESSON.md) | Serving patterns — batch, online, streaming, and choosing between them on purpose |
| `MLO-28` | [110](../days/day-110/LESSON.md) | Online serving — the latency budget, p99, and the model that is simply too slow |
| `MLO-29` | [111](../days/day-111/LESSON.md) | Batch scoring — the pipeline that writes predictions nobody is waiting for |
| `MLO-30` | [112](../days/day-112/LESSON.md) | Shipping a model — shadow, canary and A/B for something that has no single right answer |
| `MLO-31` | [112](../days/day-112/LESSON.md) | Shipping a model — shadow, canary and A/B for something that has no single right answer |
| `MLO-32` | [113](../days/day-113/LESSON.md) | Rollback for models — the version you can always go back to |
| `MLO-33` | [114](../days/day-114/LESSON.md) | Monitoring a model in production — inputs, outputs, and the ground truth you do not hav… |
| `MLO-34` | [115](../days/day-115/LESSON.md) | Data drift — detection, thresholds, and the drift alert that cried wolf |
| `MLO-35` | [116](../days/day-116/LESSON.md) | Concept drift and model decay — when the world changes instead of the data |
| `MLO-36` | [117](../days/day-117/LESSON.md) | Feedback loops, delayed labels, and the loop that trains on its own output |
| `MLO-37` | [118](../days/day-118/LESSON.md) | Wiring model monitoring into the alerting you already built |
| `MLO-38` | [119](../days/day-119/LESSON.md) | The retraining loop, automated and gated |
| `MLO-39` | [120](../days/day-120/LESSON.md) | Skew — the training/serving difference that only ever shows up in production |
| `MLO-40` | [121](../days/day-121/LESSON.md) | Multi-model serving, ensembles, and routing between them |
| `MLO-41` | [122](../days/day-122/LESSON.md) | The serving failure lab — cold start, memory blow-up, thundering herd, stale features |

## Curriculum E — LLMOps (`LLM-`) — 34 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `LLM-01` | [123](../days/day-123/LESSON.md) | What changes when the model is an LLM — and what does not change at all |
| `LLM-02` | [124](../days/day-124/LESSON.md) | Tokens and context windows — the units your latency, your quota and your bill are measu… |
| `LLM-03` | [125](../days/day-125/LESSON.md) | Hosted model APIs — quotas, rate limits, and reading a 429 properly |
| `LLM-04` | [126](../days/day-126/LESSON.md) | Running a model on your own machine — quantization, and what actually fits in your RAM |
| `LLM-05` | [127](../days/day-127/LESSON.md) | Inference servers — continuous batching, the KV cache, and throughput against latency |
| `LLM-06` | [127](../days/day-127/LESSON.md) | Inference servers — continuous batching, the KV cache, and throughput against latency |
| `LLM-07` | [128](../days/day-128/LESSON.md) | GPUs for operators — what they change, and how to do this without one |
| `LLM-08` | [129](../days/day-129/LESSON.md) | Streaming responses, and the operational cost of a generation that takes forty seconds |
| `LLM-09` | [130](../days/day-130/LESSON.md) | Routing and fallback — surviving one provider having a bad day |
| `LLM-10` | [131](../days/day-131/LESSON.md) | Caching — exact, semantic, and provider-side prompt caching |
| `LLM-11` | [132](../days/day-132/LESSON.md) | Timeouts, retries, backoff and idempotency for a call that costs money |
| `LLM-12` | [133](../days/day-133/LESSON.md) | `pulse`'s assistant behind the same service level as the rest of the system |
| `LLM-13` | [134](../days/day-134/LESSON.md) | The inference failure lab — a 429 storm, a context overflow, a silent truncation, a dea… |
| `LLM-14` | [135](../days/day-135/LESSON.md) | The prompt is code — versioned, reviewed and diffed like anything else that changes beh… |
| `LLM-15` | [136](../days/day-136/LESSON.md) | A prompt registry, and rolling out a prompt change safely |
| `LLM-16` | [137](../days/day-137/LESSON.md) | Structured output in production — schemas, validation and repair |
| `LLM-17` | [138](../days/day-138/LESSON.md) | Retrieval in production I — ingestion is a data pipeline, with everything that implies |
| `LLM-18` | [139](../days/day-139/LESSON.md) | Retrieval in production II — chunking, embeddings, and the reindex you must schedule |
| `LLM-19` | [139](../days/day-139/LESSON.md) | Retrieval in production II — chunking, embeddings, and the reindex you must schedule |
| `LLM-20` | [140](../days/day-140/LESSON.md) | Vector store operations — recall, latency, updates, and the delete that must actually d… |
| `LLM-21` | [141](../days/day-141/LESSON.md) | Embedding model versioning, and the day you have to re-embed everything |
| `LLM-22` | [142](../days/day-142/LESSON.md) | Retrieval evaluation — measuring the half of the system that fails silently |
| `LLM-23` | [143](../days/day-143/LESSON.md) | Context as a budget — truncation, compaction, and what gets dropped first |
| `LLM-24` | [144](../days/day-144/LESSON.md) | Freshness, deletion, and the right to be forgotten inside an index |
| `LLM-25` | [145](../days/day-145/LESSON.md) | The retrieval failure lab — a stale index, a poisoned document, an empty result treated… |
| `LLM-26` | [146](../days/day-146/LESSON.md) | Fine-tuning as an operations problem — the lifecycle, and why you probably should not yet |
| `LLM-27` | [147](../days/day-147/LESSON.md) | Why evaluating an LLM is different — there is no single right answer |
| `LLM-28` | [148](../days/day-148/LESSON.md) | Building an evalset that can actually fail |
| `LLM-29` | [149](../days/day-149/LESSON.md) | A model judging a model — the operational version, and its own failure modes |
| `LLM-30` | [150](../days/day-150/LESSON.md) | Regression testing prompts and models in the pipeline |
| `LLM-31` | [151](../days/day-151/LESSON.md) | Online evaluation — sampling live traffic and scoring it |
| `LLM-32` | [152](../days/day-152/LESSON.md) | Human review — annotation as an operational pipeline with a queue and a cost |
| `LLM-33` | [153](../days/day-153/LESSON.md) | Groundedness and hallucination monitoring |
| `LLM-34` | [158](../days/day-158/LESSON.md) | The evaluation failure lab — a green evalset that shipped a broken assistant |

## Curriculum F — AIOps (`AIO-`) — 23 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `AIO-01` | [159](../days/day-159/LESSON.md) | What AIOps is — and the four things it is regularly sold as and is not |
| `AIO-02` | [160](../days/day-160/LESSON.md) | Your telemetry is a dataset — collection, retention, labelling, and the ground truth pr… |
| `AIO-03` | [161](../days/day-161/LESSON.md) | Time series for operators — trend, seasonality, change points, and what "normal" means |
| `AIO-04` | [162](../days/day-162/LESSON.md) | Anomaly detection I — thresholds and baselines, and exactly why static thresholds fail |
| `AIO-05` | [163](../days/day-163/LESSON.md) | Anomaly detection II — statistical and learned detectors on real `pulse` metrics |
| `AIO-06` | [163](../days/day-163/LESSON.md) | Anomaly detection II — statistical and learned detectors on real `pulse` metrics |
| `AIO-07` | [164](../days/day-164/LESSON.md) | Evaluating a detector honestly — precision, recall, and alert fatigue as a measurable cost |
| `AIO-08` | [165](../days/day-165/LESSON.md) | Log parsing — templates, and turning free text into countable events |
| `AIO-09` | [166](../days/day-166/LESSON.md) | Log clustering — finding the error that is new rather than the error that is loud |
| `AIO-10` | [167](../days/day-167/LESSON.md) | Forecasting — saturation, capacity, and predicting the wall before you hit it |
| `AIO-11` | [168](../days/day-168/LESSON.md) | The detector failure lab — the model that alerts on every deploy and nothing else |
| `AIO-12` | [169](../days/day-169/LESSON.md) | Events, alerts and incidents — the data model underneath all of it |
| `AIO-13` | [170](../days/day-170/LESSON.md) | Correlation and grouping — from four hundred alerts to one incident |
| `AIO-14` | [171](../days/day-171/LESSON.md) | Topology — knowing what talks to what, and deriving it rather than drawing it |
| `AIO-15` | [172](../days/day-172/LESSON.md) | Root cause analysis, honestly — ranked candidates, not an oracle |
| `AIO-16` | [172](../days/day-172/LESSON.md) | Root cause analysis, honestly — ranked candidates, not an oracle |
| `AIO-17` | [173](../days/day-173/LESSON.md) | Change intelligence — attributing an incident to the deploy that caused it |
| `AIO-18` | [174](../days/day-174/LESSON.md) | Automated remediation I — the safe actions, and the ladder of trust you climb slowly |
| `AIO-19` | [175](../days/day-175/LESSON.md) | Automated remediation II — brakes, rate limits, and the remediator that made it worse |
| `AIO-20` | [175](../days/day-175/LESSON.md) | Automated remediation II — brakes, rate limits, and the remediator that made it worse |
| `AIO-21` | [176](../days/day-176/LESSON.md) | Closing the loop — responder feedback that improves the system instead of vanishing |
| `AIO-22` | [177](../days/day-177/LESSON.md) | Measuring the AIOps system itself — acknowledgement, resolution, noise, false confidence |
| `AIO-23` | [178](../days/day-178/LESSON.md) | The AIOps failure lab — beautifully correlated nonsense during a real outage |

## Curriculum G — AgenticOps (`AGO-`) — 23 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `AGO-01` | [179](../days/day-179/LESSON.md) | What AgenticOps is — operating a system that decides its own next step |
| `AGO-02` | [180](../days/day-180/LESSON.md) | The agent as a production workload — runtime, concurrency, and where the state lives |
| `AGO-03` | [181](../days/day-181/LESSON.md) | Tracing an agent — the span tree that explains a run you did not watch |
| `AGO-04` | [182](../days/day-182/LESSON.md) | Metrics for agents — task success, steps per task, cost per task, and time to answer |
| `AGO-05` | [182](../days/day-182/LESSON.md) | Metrics for agents — task success, steps per task, cost per task, and time to answer |
| `AGO-06` | [183](../days/day-183/LESSON.md) | Non-determinism in production — testing something that does not repeat |
| `AGO-07` | [184](../days/day-184/LESSON.md) | Agent evaluation in the pipeline — trajectories, rubrics, and a gate that can go red |
| `AGO-08` | [184](../days/day-184/LESSON.md) | Agent evaluation in the pipeline — trajectories, rubrics, and a gate that can go red |
| `AGO-09` | [185](../days/day-185/LESSON.md) | Versioning an agent — prompt, tools, model, and the compatibility matrix between them |
| `AGO-10` | [186](../days/day-186/LESSON.md) | Shipping an agent change — canary, shadow, and what rollback means for a conversation |
| `AGO-11` | [187](../days/day-187/LESSON.md) | Sessions, state and memory as operational surfaces with a lifecycle |
| `AGO-12` | [188](../days/day-188/LESSON.md) | Containment — step caps, budgets, timeouts, and a kill switch that has been tested |
| `AGO-13` | [188](../days/day-188/LESSON.md) | Containment — step caps, budgets, timeouts, and a kill switch that has been tested |
| `AGO-14` | [189](../days/day-189/LESSON.md) | Least privilege for a non-human actor — tool permissions and the identity behind them |
| `AGO-15` | [190](../days/day-190/LESSON.md) | The agent failure lab — the loop that spent the entire day's quota in nine minutes |
| `AGO-16` | [191](../days/day-191/LESSON.md) | The runbook agent — turning `runbooks/` into something a machine can execute |
| `AGO-17` | [192](../days/day-192/LESSON.md) | Read-only first — the diagnosis agent that is structurally unable to change anything |
| `AGO-18` | [193](../days/day-193/LESSON.md) | Approval gates and human-in-the-loop for an operational action |
| `AGO-19` | [194](../days/day-194/LESSON.md) | Action tiers and blast radius — read, suggest, act, act-with-approval |
| `AGO-20` | [195](../days/day-195/LESSON.md) | Audit trails — who did what, and proving afterwards that it was the agent |
| `AGO-21` | [196](../days/day-196/LESSON.md) | Dry run — the plan you review before anything happens |
| `AGO-22` | [197](../days/day-197/LESSON.md) | The incident co-pilot, wired to telemetry you built yourself |
| `AGO-23` | [198](../days/day-198/LESSON.md) | The agentic operations failure lab — a confident agent, a wrong action, a real outage |

## Curriculum H — MCPOps (`MCO-`) — 16 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `MCO-01` | [199](../days/day-199/LESSON.md) | What MCP is, and the exact moment it stops being a protocol and becomes an operations p… |
| `MCO-02` | [200](../days/day-200/LESSON.md) | MCP servers as services — lifecycle, transports and health |
| `MCO-03` | [200](../days/day-200/LESSON.md) | MCP servers as services — lifecycle, transports and health |
| `MCO-04` | [201](../days/day-201/LESSON.md) | Stateless scaling and session semantics at the tool boundary |
| `MCO-05` | [202](../days/day-202/LESSON.md) | Deploying an MCP server exactly the way you deploy everything else |
| `MCO-06` | [203](../days/day-203/LESSON.md) | Authentication and authorization at the boundary |
| `MCO-07` | [204](../days/day-204/LESSON.md) | Versioning tools and schemas without breaking every client at once |
| `MCO-08` | [205](../days/day-205/LESSON.md) | Observability for MCP — tracing one tool call from agent to database and back |
| `MCO-09` | [206](../days/day-206/LESSON.md) | `pulse`'s data boundary — the servers your agents are actually allowed to use |
| `MCO-10` | [207](../days/day-207/LESSON.md) | Registries and discovery — a catalogue of tools that is true today |
| `MCO-11` | [208](../days/day-208/LESSON.md) | Allowlists and scopes — per-agent tool policy, enforced at the boundary |
| `MCO-12` | [209](../days/day-209/LESSON.md) | The supply chain of a third-party MCP server |
| `MCO-13` | [210](../days/day-210/LESSON.md) | Rate limits and quotas — the tool that hammered the production database |
| `MCO-14` | [212](../days/day-212/LESSON.md) | Incident response for a bad tool — revoke, roll back, audit, and tell people |
| `MCO-15` | [213](../days/day-213/LESSON.md) | Multi-tenant tool serving — isolating one caller from another |
| `MCO-16` | [214](../days/day-214/LESSON.md) | The MCP failure lab — a poisoned tool description and a perfectly compliant agent |

## Curriculum I — Security, governance & compliance (`SEC-`) — 33 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `SEC-01` | [9](../days/day-009-configuration-and-secrets/LESSON.md) | Configuration and secrets — the twelve-factor service, `.env`, and code that refuses to… |
| `SEC-02` | [15](../days/day-015/LESSON.md) | Build artifacts and reproducibility — the lockfile, the hash, and the first SBOM |
| `SEC-03` | [17](../days/day-017/LESSON.md) | Secrets in CI — the token that must never be printed, and the scan that proves it was not |
| `SEC-04` | [28](../days/day-028/LESSON.md) | Container security — non-root, read-only root filesystem, dropped capabilities |
| `SEC-05` | [28](../days/day-028/LESSON.md) | Container security — non-root, read-only root filesystem, dropped capabilities |
| `SEC-06` | [29](../days/day-029/LESSON.md) | The supply chain of your image — base image provenance, scanning and signing |
| `SEC-07` | [48](../days/day-048/LESSON.md) | RBAC and service accounts — least privilege for the things that are not people |
| `SEC-08` | [48](../days/day-048/LESSON.md) | RBAC and service accounts — least privilege for the things that are not people |
| `SEC-09` | [49](../days/day-049/LESSON.md) | Network policy — the blast radius of one compromised pod |
| `SEC-10` | [58](../days/day-058/LESSON.md) | Secrets management — SOPS, sealed secrets, and a development Vault |
| `SEC-11` | [58](../days/day-058/LESSON.md) | Secrets management — SOPS, sealed secrets, and a development Vault |
| `SEC-12` | [59](../days/day-059/LESSON.md) | Policy as code — admission control, and a guardrail that says no before the cluster say… |
| `SEC-13` | [100](../days/day-100/LESSON.md) | Model cards, and the questions a reviewer asks before they approve |
| `SEC-14` | [144](../days/day-144/LESSON.md) | Freshness, deletion, and the right to be forgotten inside an index |
| `SEC-15` | [154](../days/day-154/LESSON.md) | Guardrails — input filters, output filters, and defence in depth |
| `SEC-16` | [154](../days/day-154/LESSON.md) | Guardrails — input filters, output filters, and defence in depth |
| `SEC-17` | [155](../days/day-155/LESSON.md) | Prompt injection against a production system — and the three capabilities you must neve… |
| `SEC-18` | [155](../days/day-155/LESSON.md) | Prompt injection against a production system — and the three capabilities you must neve… |
| `SEC-19` | [156](../days/day-156/LESSON.md) | Personal data, redaction, and the boundary your model traffic crosses |
| `SEC-20` | [189](../days/day-189/LESSON.md) | Least privilege for a non-human actor — tool permissions and the identity behind them |
| `SEC-21` | [195](../days/day-195/LESSON.md) | Audit trails — who did what, and proving afterwards that it was the agent |
| `SEC-22` | [203](../days/day-203/LESSON.md) | Authentication and authorization at the boundary |
| `SEC-23` | [208](../days/day-208/LESSON.md) | Allowlists and scopes — per-agent tool policy, enforced at the boundary |
| `SEC-24` | [209](../days/day-209/LESSON.md) | The supply chain of a third-party MCP server |
| `SEC-25` | [211](../days/day-211/LESSON.md) | Secrets at the boundary — what the tool sees, and what it must never see |
| `SEC-26` | [215](../days/day-215/LESSON.md) | Threat modelling an AI system — assets, actors, and the diagram that finds the hole |
| `SEC-27` | [216](../days/day-216/LESSON.md) | Identity for workloads — what a service is, and how it proves it |
| `SEC-28` | [217](../days/day-217/LESSON.md) | Supply chain — SBOMs, signing, provenance, and dependency risk you can actually act on |
| `SEC-29` | [218](../days/day-218/LESSON.md) | Data governance — classification, retention, lineage, and deletion that is real |
| `SEC-30` | [219](../days/day-219/LESSON.md) | Model governance — approval, documentation, and a register that is not theatre |
| `SEC-31` | [220](../days/day-220/LESSON.md) | Regulation without the panic — what the frameworks actually require of an operator |
| `SEC-32` | [221](../days/day-221/LESSON.md) | Auditability — proving what ran, on which data, at what time, under which version |
| `SEC-33` | [222](../days/day-222/LESSON.md) | The security failure lab — a leaked key and an exposed endpoint, rehearsed on purpose |

## Curriculum J — Cost, capacity & FinOps (`FIN-`) — 16 IDs

| ID | Day | Day title |
| --- | --- | --- |
| `FIN-01` | [42](../days/day-042/LESSON.md) | Requests, limits and quality of service — the four numbers everybody guesses |
| `FIN-02` | [44](../days/day-044/LESSON.md) | Horizontal autoscaling, and why more replicas do not fix a slow model |
| `FIN-03` | [68](../days/day-068/LESSON.md) | Logs II — shipping, indexing, retention, and what one log line actually costs |
| `FIN-04` | [84](../days/day-084/LESSON.md) | Capacity and load testing — knowing your limit before your traffic finds it |
| `FIN-05` | [124](../days/day-124/LESSON.md) | Tokens and context windows — the units your latency, your quota and your bill are measu… |
| `FIN-06` | [131](../days/day-131/LESSON.md) | Caching — exact, semantic, and provider-side prompt caching |
| `FIN-07` | [157](../days/day-157/LESSON.md) | Token budgets and cost attribution — the number finance will eventually ask you for |
| `FIN-08` | [157](../days/day-157/LESSON.md) | Token budgets and cost attribution — the number finance will eventually ask you for |
| `FIN-09` | [167](../days/day-167/LESSON.md) | Forecasting — saturation, capacity, and predicting the wall before you hit it |
| `FIN-10` | [210](../days/day-210/LESSON.md) | Rate limits and quotas — the tool that hammered the production database |
| `FIN-11` | [223](../days/day-223/LESSON.md) | FinOps for AI systems — the unit economics of one prediction and one generation |
| `FIN-12` | [224](../days/day-224/LESSON.md) | Cost attribution — tagging, and answering "which feature spent that?" |
| `FIN-13` | [225](../days/day-225/LESSON.md) | The cost of training against the cost of serving, measured rather than assumed |
| `FIN-14` | [226](../days/day-226/LESSON.md) | Making serving cheaper without breaking the service level |
| `FIN-15` | [227](../days/day-227/LESSON.md) | Budgets, alerts, and the guardrail that stops a runaway spend at 3am |
| `FIN-16` | [228](../days/day-228/LESSON.md) | Capacity planning for quota-shaped and GPU-shaped resources |

**279 IDs across 10 curricula.**
