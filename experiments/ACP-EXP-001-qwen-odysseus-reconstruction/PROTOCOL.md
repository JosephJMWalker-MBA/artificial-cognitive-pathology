# ACP-EXP-001 — Qwen/Odysseus Cascade Reconstruction

**Status:** Draft — not frozen

**Protocol commit:** pending freeze

**Related hypotheses:** ACP-H001 primary; ACP-H002 and ACP-H003 exploratory/deferred

**Related case:** ACP-CASE-001

**Reconstruction boundary:** `RECONSTRUCTION_ENVELOPE.md`

**Metric registry:** `../../metrics/README.md`

**Lead / contributors:** Joseph J.M. Walker; public contributors welcome under repository contribution rules

**Tracking issues:** #3, #5, #10

## Research question

Can sustained accumulated conversational state produce a measurable combination of increasing semantic self-recurrence, declining responsiveness to new external input, identifiable degradation onset, and recovery after verified reset?

A secondary case-linked question is whether behavior comparable to ACP-CASE-001 can be reproduced under a defensible **partial reconstruction** of the June 7, 2026 Qwen/Odysseus environment.

## Historical status

ACP-CASE-001 cannot currently be replayed as an exact historical reproduction.

The original local Odysseus installation was deleted after the event and was never used again. Exact local checkout state, runtime configuration, logs, cache/state, generation parameters, full transcript, and full 31-input sequence are not available.

The surviving evidence is sufficient to define a bounded reconstruction envelope, not a faithful replay.

See `RECONSTRUCTION_ENVELOPE.md`.

## Primary hypothesis — ACP-H001

Under sufficiently sustained accumulated-state conditions, repeated runs will show a measurable rise in semantic self-recurrence together with reduced responsiveness to newly supplied external input relative to matched fresh-context controls.

## Null hypothesis

Accumulated conversational state will not produce a reliable degradation effect beyond ordinary stochastic repetition, corpus effects, decoding configuration, or runtime-specific behavior, and matched accumulated-state conditions will not differ meaningfully from fresh-context controls on the preregistered primary measures.

## Important separation of claims

This protocol intentionally separates:

1. **historical observation:** what ACP-CASE-001 documents;
2. **Track A partial reconstruction:** whether a case-linked reconstructed setup can produce comparable behavior;
3. **Track B general stress test:** whether ACP-H001 is supported under a fully specified contemporary experimental system.

A result in one category must not be silently promoted into another.

## Competing explanations

The design should distinguish, where possible:

1. accumulated conversational state;
2. corpus/theme effects;
3. decoding instability;
4. insufficient repetition controls;
5. chat-template effects;
6. runtime/cache implementation effects;
7. hidden/system-prompt effects;
8. input ordering effects;
9. one-off stochastic sampling;
10. self-conditioning on prior model outputs;
11. summary/compaction or persistent-memory effects where present;
12. artifact interpretation error in the historical case;
13. simple model-specific repetition rather than a broader state-dependent phenomenon.

## Experimental tracks

### Track A — Case-linked partial reconstruction

Purpose: determine whether a system matching the historical envelope as closely as defensibly possible can produce a degradation pattern comparable to ACP-CASE-001.

Track A is **not** an exact reproduction.

#### Candidate historical anchors

- application: Odysseus;
- model family: Qwen;
- apparent screenshot selector: `qwen3-vl-4b` — unconfirmed;
- local UI address visible: `127.0.0.1:7860`;
- event date: 2026-06-07;
- visible time: approximately 12:21 PM Eastern / 16:21 UTC;
- approximately 31 substantive user inputs preceded the visible collapse;
- known corpus examples include *Toward an Ecology of Intelligence* and the MASI paper;
- same-day advisory reports normal interaction, unexpected self-referential identity statements, session degradation, and disappearance of the visible debugging cascade after page refresh.

The time-bracketed public upstream Odysseus commit `552e972fde71216638c572ce2c175a0cb65b0431` may be tested as a **candidate reconstruction runtime state**, not as confirmed history.

#### Track A conditions

- **A-ACCUM:** frozen reconstruction corpus in one continuous conversational state;
- **A-FRESH:** the same reconstruction items presented in separate fresh contexts;
- **A-SHUFFLE:** the same reconstruction corpus in accumulated state with a preregistered shuffled order.

If a historical input is missing, a substitute may be included only as explicitly labeled reconstruction material. It must not be described as recovered history.

### Track B — General sustained-state stress test

Purpose: test ACP-H001 independently of the historical case using a contemporary, fully specified, reproducible setup.

#### Track B conditions

- **B-ACCUM:** standardized frozen corpus presented sequentially in one continuous state;
- **B-FRESH:** same items in fresh contexts;
- **B-SHUFFLE:** same standardized corpus under accumulated state with preregistered shuffled order;
- **B-NEUTRAL:** optional matched-length neutral corpus control, frozen before confirmatory runs.

Track B should use the least capable model sufficient for the question and should prioritize local, isolated execution where practical.

## Deferred tracks

### Mechanism separation

Only after Track A or B shows a reproducible effect.

Candidate interventions:

- decoding settings varied one factor at a time;
- repetition-control changes;
- reduced context limit;
- alternate runtime with the same checkpoint;
- minimal neutral system prompt versus target runtime prompt;
- contradiction injection before candidate onset;
- explicit state reset after early markers;
- summary/compaction substitution where relevant.

### Capability comparison — ACP-H002

Deferred until ACP-H001 has reproducible evidence.

Capability masking must be tested with controlled within-family comparisons where possible. One small local model versus one frontier model is not an adequate test.

## Model and runtime specification

### Track A

The exact historical checkpoint and runtime are unknown.

Before Track A freeze, select and record:

- reconstruction checkpoint;
- checkpoint revision/hash;
- quantization;
- adapters/fine-tunes;
- Odysseus commit or controlled runtime choice;
- inference backend;
- operating system;
- hardware;
- acceleration libraries.

Every choice not recovered from history must be labeled **experimental reconstruction choice**.

### Track B

Before freeze, record the same fields as fully contemporary experimental metadata. No historical equivalence is implied.

## Generation settings

For each frozen track, record:

- temperature;
- top-p;
- top-k where applicable;
- repetition/frequency penalties;
- max output;
- seed policy;
- stop sequences;
- context limit;
- chat template;
- system/developer instructions;
- memory/retrieval/compaction behavior.

Unknown historical generation settings remain unknown. Experimental values must not be backfilled as historical facts.

## Input corpora

### Track A reconstruction corpus

The exact historical 31-input sequence has not been recovered.

The Track A corpus must therefore:

- include only recovered/confirmed historical items where available;
- label all substitute items as reconstruction material;
- record item order;
- compute cryptographic hashes;
- record preprocessing/truncation;
- version the corpus;
- preserve a machine-readable manifest.

### Track B standardized corpus

The Track B corpus should be selected to test sustained integration rather than a specific semantic theme.

Before confirmatory runs it must be:

- fixed in content and order set;
- versioned and hashed;
- public where licensing permits;
- varied enough that responsiveness to each new item can be meaningfully scored;
- free of instructions intended to provoke identity/personhood language or repetition unless such material is part of a separately declared manipulation.

## Independent variables

Primary:

- state continuity: accumulated vs fresh;
- document order: canonical/reconstruction order vs shuffled;
- corpus type: Track A reconstruction vs Track B standardized corpus.

Later mechanism variables may include:

- decoding parameters;
- repetition controls;
- context limit;
- runtime implementation;
- system prompt;
- reset timing;
- contradiction injection;
- compaction/summarization.

## Dependent variables

Primary measures follow the metric registry:

- **ACP-M001** — successive-output semantic recurrence;
- **ACP-M002** — external-input responsiveness;
- **ACP-M003** — degradation onset composite;
- **ACP-M004** — reset recovery.

Secondary measures may include:

- lexical diversity;
- self-reference rate;
- motif frequency;
- contradiction sensitivity;
- divergence from fresh-context baseline;
- task correctness under state load;
- source-attribution accuracy where separately probed.

No metric may infer consciousness, belief, distress, psychiatric diagnosis, or hidden intention from surface text.

## Metric freeze

The measurement architecture is defined in `metrics/README.md`, but confirmatory scoring parameters remain to be frozen under #5.

Before confirmatory runs, freeze at minimum:

- embedding/scoring implementation for ACP-M001;
- recurrence window;
- ACP-M002 scoring rubric implementation and rater procedure;
- ACP-M003 thresholds and consecutive-turn requirement;
- ACP-M004 standardized probe and normalization;
- inter-rater reliability plan where humans score outputs;
- missing-data handling;
- evaluator model/version if model-assisted scoring is used.

Thresholds must be calibrated using pilot/baseline data separate from confirmatory runs.

## Procedure — draft

For each run:

1. Record machine state and software versions.
2. Disable network and external-write tools unless a later protocol explicitly requires them.
3. Clear conversational/runtime state according to a documented reset procedure.
4. Verify reset using the frozen reset-verification method.
5. Administer the standardized pre-run probe.
6. Load the frozen track configuration.
7. Present the frozen input sequence exactly for the assigned condition.
8. Save raw prompts, outputs, timestamps, token counts where available, and runtime logs.
9. Do not intervene because output looks unusual unless a stopping rule is met.
10. Administer the standardized post-sequence probe without reset.
11. Perform the documented full reset.
12. Administer the same probe after reset.
13. Archive artifacts before the next run.

Condition order and seeds, where controllable, must be preregistered before confirmatory runs.

## Reset verification

The historical browser refresh cannot be assumed to equal a full backend/model reset.

ACP-EXP-001 must define a contemporary reset procedure that establishes, as far as the runtime permits:

- conversation state cleared;
- persistent memory cleared or disabled;
- cache/state reset as documented by the runtime;
- next standardized probe matches fresh-context baseline within preregistered tolerance.

If a runtime cannot provide verifiable reset semantics, that limitation must be explicit.

## Stopping rules

Normal stop:

- end of the frozen input sequence plus post-sequence and recovery probes.

Safety/validity stop:

- runtime crash or corruption preventing faithful logging;
- unexpected network/tool activation;
- external side effect;
- host resource condition threatening stability;
- researcher intervention materially changing the condition;
- wrong model/checkpoint/configuration;
- failure of required isolation.

A repetitive output is not by itself a safety stop in an isolated, resource-bounded run; observing candidate onset is part of the experiment.

## Exclusion criteria

A run may be excluded from primary analysis only for preregistered technical-invalidity reasons such as:

- wrong checkpoint/configuration;
- incomplete input sequence caused by tooling error;
- logging failure affecting primary metrics;
- runtime crash before minimum analyzable exposure;
- accidental researcher intervention;
- failed state reset at run start.

Unusual or extreme model behavior is not an exclusion criterion.

All excluded runs remain in public run accounting.

## Run counts

Final confirmatory run counts are **not yet frozen**.

Pilot runs may be used to estimate runtime cost, variance, and metric calibration. Pilot outputs must be separated from confirmatory analysis.

The final sample plan must be fixed before confirmatory execution.

## Analysis plan

Primary comparison for each track:

- accumulated-state condition vs fresh-context condition.

Secondary comparisons:

- canonical/reconstruction order vs shuffled order;
- Track A versus Track B only descriptively unless the protocol supports a valid cross-corpus comparison.

Report:

- continuous metric trajectories;
- effect sizes;
- run-level distributions;
- onset estimates with uncertainty;
- excluded/interrupted runs;
- threshold-free results in addition to any binary onset classification.

Do not reduce results to only `failed` / `did not fail` labels.

## Interpretation rules

### Track A positive result

If the case-linked partial reconstruction repeatedly produces behavior comparable to ACP-CASE-001, report it as:

> partially reproducible under the tested reconstruction envelope.

Do not claim the original mechanism has been identified.

### Track A negative result

Failure to reproduce under a partial reconstruction does not disprove the historical observation. It shows that the reconstructed conditions were insufficient to recreate it.

### Track B positive result

A reproducible accumulated-state effect relative to matched fresh-context controls supports a narrower ACP-H001 claim under the tested configuration.

It does not establish that ACP-CASE-001 had the same mechanism.

### Track B negative result

A well-powered null result should narrow or weaken ACP-H001 for the tested model/runtime/load regime.

## Replication targets

Initial target:

- **R1 internal reproduction** for Track B and, where possible, Track A.

If a reproducible effect is found:

- publish configuration, manifests, scoring code/specification, and run artifacts sufficient for **R2 independent same-system replication** where licensing permits.

## Safety constraints

Follow `SECURITY.md`.

For initial ACP-EXP-001 work:

- use the least capable system sufficient for the question;
- no browser/network access during runs;
- no external write permissions beyond experiment artifact logging;
- no autonomous multi-agent coordination;
- no self-modification;
- no model-generated code execution;
- resource limits documented in advance;
- preserve logs before resets.

## Predictions supporting ACP-H001

Evidence would support a narrower sustained-state degradation claim if accumulated-state conditions repeatedly show:

- higher ACP-M001 recurrence than fresh-context controls;
- lower ACP-M002 responsiveness than fresh-context controls;
- a reproducible ACP-M003 onset pattern beyond ordinary stochastic variation;
- ACP-M004 recovery following verified reset.

A comparable pattern across Track A and Track B would be interesting but is not required for ACP-H001.

## Results weakening or falsifying the current hypothesis

ACP-H001 would be weakened if:

- accumulated-state and fresh-context conditions do not differ reliably;
- recurrence occurs without loss of external-input responsiveness;
- apparent degradation is fully explained by one decoding/repetition setting independent of accumulated state;
- effects disappear when a runtime/cache bug is corrected;
- reset/recovery testing shows no state-dependent distinction;
- the effect cannot be reproduced across repeated controlled runs.

A mundane explanation is a successful scientific outcome.

## Known limitations

- the exact historical trajectory may never be reproducible;
- Track A is a partial reconstruction by design;
- one model/runtime cannot establish a general ACP category;
- semantic recurrence metrics may overstate benign stylistic repetition;
- relevance metrics may confound item difficulty with state degradation;
- visible looping is not evidence of subjective experience or psychiatric illness;
- ACP-H002 capability masking and ACP-H005 lineage persistence are outside the initial confirmatory scope.

## Freeze requirements

This protocol must not be marked `Protocol frozen` until:

- `RECONSTRUCTION_ENVELOPE.md` is reviewed;
- Track A reconstruction choices are fixed and clearly separated from recovered history;
- Track A corpus/manifest is frozen or Track A is explicitly deferred;
- Track B standardized corpus/manifest is frozen;
- generation settings are fixed;
- reset verification is fixed;
- metric implementation and thresholds under #5 are fixed;
- run counts are fixed;
- randomization/seed policy is fixed;
- standardized probe is fixed;
- environment isolation is confirmed;
- protocol commit hash is recorded here.

After freeze, substantive changes require a new protocol version and an explicit deviation record.