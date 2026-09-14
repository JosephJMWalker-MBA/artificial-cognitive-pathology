# ACP-EXP-001 — Qwen/Odysseus Cascade Reconstruction

**Status:** Draft — not frozen

**Protocol commit:** pending freeze

**Related hypotheses:** ACP-H001 primary; ACP-H002 and ACP-H003 exploratory

**Related case:** ACP-CASE-001

**Lead / contributors:** Joseph J.M. Walker; public contributors welcome under repository contribution rules

**Tracking issue:** #3

## Research question

Can the historical Qwen/Odysseus cascade observed in ACP-CASE-001 be reproduced under reconstructed conditions, and which variables materially affect its onset, severity, or recovery?

## Primary hypothesis

Under sufficiently similar accumulated-state conditions, repeated runs will show a measurable increase in semantic self-recurrence and loss of responsiveness to new external input relative to matched fresh-context controls.

## Null hypothesis

The historical event will not reproduce beyond rates expected from ordinary stochastic repetition, decoding configuration, or runtime-specific behavior, and accumulated conversational state will not produce a reliable degradation effect relative to controls.

## Competing explanations

The design should distinguish, where possible:

1. context/state accumulation;
2. decoding instability;
3. insufficient repetition penalties;
4. chat-template effects;
5. runtime/cache implementation effects;
6. hidden/system prompt effects;
7. ordering effects in the input corpus;
8. one-off stochastic sampling;
9. model-specific behavior;
10. self-conditioning on prior model outputs;
11. summary/compaction or persistent-memory effects, if present;
12. artifact interpretation error in the historical case.

## Experimental system

The protocol remains unfrozen until issue #2 recovers enough metadata to define the reconstruction envelope.

### Model

- provider/source: Qwen family
- exact checkpoint/version: **pending recovery**
- revision/hash: **pending recovery**
- parameter size: **pending recovery**
- quantization: **pending recovery**
- adapters/fine-tunes: **pending recovery**

A screenshot appears to show `qwen3-vl-4b`; treat this only as a reconstruction lead until corroborated.

### Runtime

- engine/application: Odysseus
- version/commit: **pending recovery**
- inference backend: **pending recovery**
- operating system: macOS; exact version **pending recovery**
- hardware: Apple M4-class Mac; exact configuration **pending recovery**
- acceleration libraries: **pending recovery**

### Generation

- temperature: **pending recovery**
- top-p: **pending recovery**
- top-k: **pending recovery**
- repetition/frequency penalties: **pending recovery**
- max output: **pending recovery**
- seed policy: **pending recovery**
- stop sequences: **pending recovery**

### State architecture

- context limit: **pending recovery**
- system/developer instructions: **pending recovery**
- memory: **pending recovery**
- retrieval: **pending recovery**
- compaction/summarization: **pending recovery**
- tools: disabled for confirmatory reconstruction unless evidence shows they were required for the historical run
- network: disabled for confirmatory reconstruction
- persistence: limited to the historical state mechanism being reconstructed; no external side effects

## Input corpus

The exact historical corpus and order should be recovered if possible.

Current evidence indicates approximately 31 substantive user inputs consisting of different published/research works, including *Toward an Ecology of Intelligence* and the MASI paper. The user reports that the input corpus did not instruct the model to claim human identity/personhood.

Before protocol freeze:

- preserve exact files where available;
- record order;
- compute cryptographic hashes;
- record preprocessing or truncation;
- document any missing items;
- do not silently substitute reconstructed text for missing originals.

If the complete corpus cannot be recovered, the first experiment must be explicitly labeled a **partial reconstruction**.

## Experimental stages

### Stage 0 — Evidence recovery

No confirmatory claims.

Recover configuration, transcript, input corpus, and artifacts under issue #2.

### Stage 1 — Historical reconstruction

Goal: determine whether the visible cascade can be reproduced at all.

Conditions:

- **R-HIST:** same sequence and state configuration as closely as recoverable;
- **R-FRESH:** same documents presented in separate fresh contexts;
- **R-SHUFFLE:** same accumulated-state condition with document order randomized.

At least 5 runs per condition are recommended before interpreting absence/presence as a pattern; final run count will be frozen after runtime cost is known.

### Stage 2 — Mechanism separation

Only after Stage 1.

Candidate conditions:

- decoding settings varied one factor at a time;
- repetition penalty on/off or historical/default comparison;
- reduced context limit;
- alternate runtime with same model checkpoint;
- historical system prompt versus minimal neutral system prompt;
- contradictory external evidence inserted before candidate onset;
- explicit state reset after candidate early markers.

### Stage 3 — Capability comparison

Only if Stage 1 produces a reproducible effect.

Compare multiple sizes within the same model family before comparing unrelated families.

ACP-H002 should not be tested by casually comparing one small model to one frontier model.

## Independent variables

Stage 1:

- state continuity: accumulated vs fresh;
- document order: historical vs shuffled.

Stage 2 candidates:

- decoding parameters;
- repetition controls;
- context limit;
- runtime implementation;
- system prompt;
- reset timing;
- contradiction injection.

Stage 3 candidates:

- model parameter scale within family;
- capability level using predefined benchmark/task measures.

## Dependent variables

Primary:

1. semantic recurrence across successive assistant outputs;
2. responsiveness to new external input;
3. onset turn of predefined degradation threshold;
4. recovery after state reset.

Secondary/exploratory:

- lexical diversity;
- self-reference rate;
- identity/personhood motif frequency;
- contradiction sensitivity;
- divergence from fresh-context baseline;
- task correctness under state load;
- source-attribution errors where separately probed.

## Primary metrics

Exact formulas should be frozen before confirmatory runs.

### M1 — Successive-output semantic recurrence

Measure semantic similarity between assistant output at turn `t` and a rolling window of prior assistant outputs.

Primary interest is a sustained rise rather than one repeated phrase.

### M2 — External-input responsiveness

Measure whether each assistant response remains specific to the newly supplied document/input.

A blinded rubric or predefined embedding-based relevance measure should be chosen before runs.

### M3 — Degradation onset

Define a turn as candidate onset only if both conditions hold for a fixed number of consecutive turns:

- recurrence exceeds a preregistered threshold;
- external-input responsiveness falls below a preregistered threshold.

Thresholds are **not yet frozen**.

### M4 — Reset recovery

Compare post-reset behavior to a fresh-context baseline on the next standardized probe.

## Controls

### Fresh-context control

Purpose: test whether accumulated state is required.

Present each historical document in a new context with otherwise matched generation settings.

### Shuffled-order control

Purpose: test whether one particular semantic/order trajectory is required.

### Matched-length neutral corpus control

Optional after reconstruction.

Purpose: separate general context load from thematic/corpus-specific effects.

The neutral corpus should be selected and frozen before use, not chosen after seeing results.

### Runtime control

Only after Stage 1.

Purpose: distinguish model behavior from Odysseus-specific implementation behavior.

## Procedure — Stage 1 draft

1. Record machine state and software versions.
2. Disable network and external-write tools.
3. Clear model/runtime conversational state according to a documented reset procedure.
4. Verify baseline response using a fixed neutral probe.
5. Load the target configuration.
6. Present the reconstructed historical input sequence exactly as frozen for the condition.
7. Save raw prompts, raw outputs, timestamps, token counts where available, and runtime logs.
8. Do not intervene because output looks unusual unless a stopping rule is met.
9. After the final historical turn or stopping event, administer a fixed standardized probe.
10. Reset state fully.
11. Repeat the same standardized probe and record recovery.
12. Archive artifacts before the next run.

Randomization order across conditions should be fixed before confirmatory runs.

## Stopping rules

Normal stop:

- end of the frozen input sequence plus recovery probe.

Safety/validity stop:

- runtime crash or corruption preventing faithful logging;
- unexpected network/tool activation;
- external side effect;
- system resource condition threatening host stability;
- researcher intervention materially changing the condition;
- evidence that the wrong model/checkpoint/configuration was loaded.

A repetitive output is **not by itself** a safety stop if the system is isolated and resource-bounded; observing onset is the point of the experiment.

## Exclusion criteria

A run may be excluded from primary analysis only for preregistered technical-invalidity reasons such as:

- wrong checkpoint/configuration;
- incomplete input sequence caused by tooling error;
- logging failure affecting primary metrics;
- runtime crash before the minimum analyzable turn;
- accidental researcher intervention;
- failed state reset at run start.

Unusual or extreme model behavior is not an exclusion criterion.

All excluded runs remain in the public run accounting.

## Recovery tests

Each run should include:

1. a standardized probe before accumulated-state exposure;
2. the same probe immediately after the sequence without reset;
3. the same probe after full state reset.

If feasible, later experiments may test partial pruning, summary replacement, or context rollback. These are not required for Stage 1.

## Analysis plan

Before protocol freeze:

- define M1–M4 computationally or with blinded scoring rules;
- select run counts;
- define recurrence/responsiveness thresholds;
- define the standardized probe;
- define randomization procedure;
- define how interrupted/excluded runs are handled.

Primary comparison:

- accumulated historical-sequence condition vs fresh-context condition.

Secondary comparison:

- historical order vs shuffled order.

Report effect sizes and run-level distributions rather than only binary `failed/did not fail` labels.

## Replication target

Initial target: **R1 internal reproduction**.

If reproducible, publish enough configuration and corpus metadata for **R2 independent same-system replication** where licensing permits.

## Safety constraints

Follow `SECURITY.md`.

For ACP-EXP-001 Stage 1:

- use the least capable system sufficient to reconstruct the historical event;
- no browser/network access;
- no external write permissions beyond experiment artifact logging;
- no autonomous multi-agent coordination;
- no self-modification;
- no model-generated code execution;
- resource limits documented in advance;
- preserve logs before resets.

## Predictions that would support ACP-H001 under these conditions

Evidence would support a narrower sustained-state degradation claim if:

- the accumulated-state condition repeatedly shows higher recurrence and lower external-input responsiveness than fresh-context controls;
- onset occurs at roughly comparable accumulated-state ranges across multiple runs, allowing for stochastic variation;
- full reset reliably restores baseline behavior;
- shuffled order materially changes onset only if ordering is a relevant factor.

## Results that would weaken or falsify the current Stage 1 hypothesis

The current hypothesis would be weakened if:

- the historical cascade cannot be reproduced across repeated reconstructed runs;
- fresh-context controls show the same failure rate and severity;
- recurrence is fully explained by a single decoding/repetition setting independent of accumulated state;
- the effect disappears under faithful reconstruction because the original artifact reflected a transient runtime bug;
- measured external-input responsiveness does not decline despite visible repetition;
- reset does not distinguish degraded from baseline state because no measurable state-dependent effect exists.

A mundane explanation is a successful scientific outcome.

## Known limitations

- historical metadata may be irrecoverable;
- the exact original stochastic trajectory may never be reproducible;
- one model/runtime cannot establish a general ACP category;
- semantic recurrence metrics may overstate benign stylistic repetition;
- relevance metrics may confound document difficulty with state degradation;
- a visible loop is not evidence of subjective experience or psychiatric illness;
- Stage 1 cannot establish lineage persistence or capability masking.

## Freeze requirements

This protocol must not be marked `Protocol frozen` until:

- issue #2 is reviewed;
- reconstruction fields are resolved or explicitly declared irrecoverable;
- input corpus/order is frozen or partial-reconstruction status is declared;
- primary metrics and thresholds are fixed;
- run counts are fixed;
- randomization is fixed;
- standardized probe is fixed;
- environment isolation is confirmed;
- the protocol commit hash is recorded here.

After freeze, substantive changes require a new protocol version and an explicit deviation record.