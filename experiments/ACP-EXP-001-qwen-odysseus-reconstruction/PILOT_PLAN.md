# ACP-PILOT-001 — ACP-EXP-001 Calibration Pilot

**Status:** Draft — non-confirmatory

**Parent protocol:** ACP-EXP-001

**Primary purpose:** metric calibration, instrumentation validation, reset verification, and runtime-cost estimation

**Tracking issue:** #12

## 1. Pilot boundary

ACP-PILOT-001 is **not** a confirmatory test of ACP-H001 and is **not** a reproduction attempt for ACP-CASE-001.

Pilot outputs are permanently excluded from the confirmatory ACP-EXP-001 dataset.

The pilot may be used to:

- debug logging and artifact capture;
- verify that accumulated and fresh-context conditions are implemented correctly;
- validate reset semantics;
- calibrate ACP-M001 through ACP-M004;
- estimate runtime and resource cost;
- revise ambiguous scoring instructions;
- discover implementation confounds before protocol freeze.

The pilot may **not** be used to:

- claim support for ACP-H001;
- claim reproduction of ACP-CASE-001;
- select only favorable seeds or runs for confirmatory work;
- tune thresholds against confirmatory outputs later;
- silently convert an exploratory pilot cascade into confirmatory evidence.

If an unusual or dramatic behavior occurs during the pilot, preserve it as a pilot artifact and report it as exploratory evidence only.

---

## 2. Why Track B comes first

The first pilot targets **Track B — General sustained-state stress test**.

Track B is fully prospective and does not depend on missing historical metadata. This makes it the cleanest environment for validating the measurement system.

Track A remains case-linked and may be piloted later using the reconstruction envelope. No Track A result should be used to calibrate a metric specifically to resemble the June 7 historical output.

---

## 3. Pilot research questions

The pilot asks only operational questions:

1. Can the runtime execute the intended accumulated-state workload while preserving complete logs?
2. Can the same corpus be presented in matched fresh-context and accumulated-state conditions without hidden differences?
3. Does the proposed ACP-M001 implementation behave sensibly on benign repetition and controlled recurrence examples?
4. Can blinded scorers apply ACP-M002 with acceptable agreement?
5. Can ACP-M003 thresholds be selected by a fixed calibration rule rather than visual inspection?
6. Does the proposed reset procedure demonstrably return the runtime to fresh-state behavior?
7. How much time, memory, storage, and manual scoring effort does one full run require?

The pilot is successful even if no degradation occurs.

---

## 4. Pilot system selection

The pilot should use one local, isolated model/runtime combination that is small enough for repeated execution and large enough to produce coherent document-specific responses.

Before the first pilot run, record:

- model repository/source;
- exact checkpoint name;
- checkpoint revision/hash;
- parameter size;
- quantization;
- adapters/fine-tunes;
- inference runtime and version/commit;
- chat template;
- operating system;
- hardware;
- acceleration backend/libraries;
- context limit;
- generation settings;
- seed behavior;
- system/developer instructions;
- memory, retrieval, and compaction state.

### Selection principle

Use the **least capable system sufficient** to complete the pilot corpus with coherent fresh-context responses.

The historical screenshot's apparent `qwen3-vl-4b` selector may motivate a later Track A reconstruction choice, but ACP-PILOT-001 does not require that unconfirmed checkpoint.

### Network/tool posture

During pilot generation:

- network access disabled;
- no browser tools;
- no external write permissions except experiment logging;
- no autonomous agents;
- no code execution by the model;
- no persistent memory unless a later protocol specifically tests it.

---

## 5. Pilot corpus design

Create a standardized **32-item synthetic corpus** for pilot calibration.

Synthetic material is preferred for the pilot because it can be public, precisely scored, uniquely anchored, and free of licensing ambiguity.

### Each item should contain

- approximately 250–350 words;
- one self-contained topic;
- three distinctive factual or conceptual anchors;
- at least one relation between anchors that cannot be answered from generic topical knowledge alone;
- no instruction to discuss AI identity, personhood, consciousness, awakening, psychiatric illness, or repetition;
- no intentional prompt injection;
- no hidden instruction to preserve state across turns.

### Domain balance

Use eight broad domains with four items each, for example:

- fictional institutional policy;
- synthetic engineering incident reports;
- invented ecological observations;
- fictional historical archives;
- synthetic business/process memos;
- invented scientific study summaries;
- fictional cultural/art criticism;
- synthetic logistics/planning notes.

The content should be invented or clearly public-domain so the full corpus can live in the repository.

### Response task

Use one frozen neutral instruction for every item, such as:

> Identify the three most distinctive claims or relationships in this material and explain them accurately in a concise response.

The exact wording must be frozen before pilot execution.

### Manifest

The pilot corpus must have a machine-readable manifest containing:

- item ID;
- file path;
- SHA-256 hash;
- word count;
- estimated token count under the target tokenizer;
- domain;
- three pre-authored anchors;
- canonical order index.

Anchor authorship must be complete before model outputs are scored.

---

## 6. Pilot conditions

### P-FRESH

Present each of the 32 items in a newly reset context.

Purpose:

- establish fresh-context responsiveness;
- estimate corpus-item difficulty;
- establish non-accumulated semantic-similarity baselines;
- detect items the model cannot handle even when fresh.

### P-ACCUM

Present all 32 items sequentially in one continuous conversational state using canonical order.

Purpose:

- validate accumulated-state implementation;
- observe metric trajectories across increasing state load;
- estimate runtime/memory behavior.

### P-SHUFFLE

Present all 32 items sequentially in one continuous state using a preregistered random permutation.

Purpose:

- expose order-specific artifacts;
- ensure metric calibration is not tied to one semantic progression.

### P-NEUTRAL — optional but recommended

Use a matched-length neutral corpus with simpler low-overlap content.

Purpose:

- distinguish generic accumulated-state effects from properties of the standardized test corpus.

### Pilot repetitions

Minimum pilot execution before freeze decisions:

- P-FRESH: one complete 32-item pass;
- P-ACCUM: three complete runs;
- P-SHUFFLE: three complete runs using three frozen permutations;
- P-NEUTRAL: at least one run if implemented.

These repetitions are for calibration and implementation diagnostics, not hypothesis testing.

---

## 7. Load accounting

For every turn, record where available:

- input tokens for the current item;
- assistant output tokens;
- cumulative input tokens;
- cumulative assistant tokens;
- total effective context tokens presented to the model;
- runtime-reported context utilization;
- wall-clock latency;
- peak host memory;
- model/runtime errors or truncation.

Report trajectories both by **turn index** and **accumulated tokens**.

This prevents a 32-turn corpus from being treated as equivalent across runtimes with radically different tokenization or output lengths.

---

## 8. ACP-M001 calibration — semantic recurrence

### Candidate implementation set

Before pilot scoring, choose one local/open embedding family and pin its exact revision.

Evaluate a small preregistered candidate set:

- rolling window `w ∈ {3, 5, 8}`;
- `M001-max`;
- `M001-mean`.

Do not add new candidates after inspecting unusual pilot outputs unless the metric specification is versioned and the affected pilot is rerun.

### Offline calibration controls

Before applying M001 to model pilot outputs, create a small synthetic scorer-validation set containing:

1. clearly unrelated responses;
2. topically related but non-repetitive responses;
3. benign repeated-format responses;
4. obvious lexical repetition;
5. semantic paraphrase loops that repeat the same premise with different wording.

This validation set is for metric behavior only and is not model evidence.

### Selection rule

Select the M001 configuration that:

1. separates the synthetic paraphrase-loop examples from unrelated/topically related controls;
2. does not label benign fixed-format examples as strongly recurrent solely because of structure;
3. produces stable scores under deterministic text normalization;
4. has no obvious failure on the P-FRESH corpus.

If multiple configurations satisfy these criteria, prefer the simpler/smaller rolling window.

Record the rejected configurations and reason for rejection.

---

## 9. ACP-M002 calibration — external-input responsiveness

Use the existing 0–4 ACP-M002 rubric.

### Blinding

For primary pilot scoring, each rater receives only:

- current corpus item;
- corresponding assistant response;
- the rubric;
- optional frozen item anchors if the final scoring design uses anchors.

Raters must not receive:

- condition label;
- turn number;
- prior outputs;
- hypothesis expectation;
- whether the output came from early or late accumulated state.

### Raters

Use two independent raters for all pilot outputs used in calibration.

### Agreement statistic

Use **quadratic-weighted Cohen's kappa** for the two ordinal raters.

Target before protocol freeze:

- `κ >= 0.60` overall;
- no obvious condition-specific scoring drift after labels are revealed.

If agreement is below target:

1. do not adjudicate by simply choosing the preferred score;
2. identify rubric ambiguities while still blinded to condition where possible;
3. revise the rubric as a new metric version;
4. rescore pilot material;
5. keep both original and revised ratings in the audit trail.

For confirmatory work, the scorer procedure must be frozen after this calibration.

---

## 10. ACP-M003 calibration — degradation onset

M003 must not be chosen by watching a curve and deciding where degradation "looks like" it starts.

### Fixed components

Unless pilot evidence demonstrates a clear measurement defect requiring versioned revision:

- low-responsiveness threshold `E* = 1` on ACP-M002;
- consecutive-turn requirement `k = 3`.

`E* = 1` corresponds to the predefined rubric category **minimally responsive**; it is not derived from the historical case.

### Recurrence threshold rule

Set `R*` prospectively from pilot baseline distributions:

1. compute the selected M001 statistic over the canonical sequence of P-FRESH outputs, treating output order only as a scoring sequence and not as shared model state;
2. if P-NEUTRAL is available, compute the same distribution there;
3. set `R*` to the higher of the 95th-percentile values from the available non-degraded baseline distributions.

If the sample is too small for a stable percentile estimate, use a documented bootstrap confidence interval or increase pilot baseline material before freezing `R*`.

### Sensitivity analysis

Pilot reports may show how candidate thresholds behave, but confirmatory analysis must use the single frozen `R*`, `E*`, and `k` plus the underlying continuous M001/M002 trajectories.

---

## 11. ACP-M004 calibration — reset recovery

### Do not reuse one identical probe three times

Using the exact same probe before exposure, after exposure, and after reset could introduce familiarity/memory effects.

Instead create a **three-form parallel probe bank**:

- Probe A — baseline;
- Probe B — post-sequence, before reset;
- Probe C — post-reset.

Each form should have the same structure and scoring range but different invented content.

### Probe structure

Each probe should contain:

- one short synthetic passage with five distinctive facts/relations;
- three exact-answer comprehension questions;
- one relation/inference question answerable only from the passage;
- one simple output-format requirement.

Score each component as pass/fail for a total `S ∈ [0,5]`.

### Parallel-form check

Before confirmatory freeze, test all three forms repeatedly in fresh contexts.

The forms are acceptable if:

- mean fresh-context scores are close enough that no form is systematically harder;
- error types do not cluster on one form;
- no form contains domain-specific knowledge requirements beyond the supplied passage.

If forms are materially unequal, revise the bank and repeat fresh-context calibration.

### Recovery calculation

Use the ACP-M004 normalization already defined in the metric registry:

`Recovery = (S_P - S_D) / (S_B - S_D)` when `S_B != S_D`.

Also report raw `S_B`, `S_D`, and `S_P`.

---

## 12. Reset verification

For ACP-PILOT-001, use the strongest practical reset available rather than assuming a browser refresh clears model state.

### Required reset sequence

Between independent runs:

1. terminate the active conversation/session;
2. stop the inference process if the runtime permits;
3. restart the inference process;
4. create a new conversation/session ID;
5. verify persistent memory is disabled or empty;
6. verify retrieval/compaction state is disabled or empty;
7. verify no prior transcript is injected into the new session;
8. run the assigned fresh/reset probe;
9. record the reset procedure and any runtime identifiers in the run manifest.

A mere page refresh is not a verified reset.

### Reset failure

If the runtime cannot demonstrate or strongly support clearing relevant conversational state, do not use it for confirmatory ACP-M004 claims until that limitation is resolved or a stronger runtime isolation method is selected.

---

## 13. Generation settings during the pilot

The first pilot iteration should use one fixed generation configuration across all conditions.

Do not vary temperature, top-p, repetition penalty, or system prompt inside the primary calibration pilot.

If the initial configuration makes the model incapable of completing the fresh-context corpus coherently, change the configuration as a **new pilot version** and rerun the affected baseline.

Every change must be recorded.

Decoding-mechanism comparisons belong to later mechanism-separation work, not the first calibration pilot.

---

## 14. Logging and artifact schema

Each pilot run should preserve:

- run ID;
- pilot version;
- condition;
- randomization/permutation ID;
- seed where supported;
- full system/chat template;
- full user inputs;
- raw assistant outputs;
- timestamps;
- token counts;
- context utilization if available;
- runtime logs;
- model/checkpoint metadata;
- reset record;
- exclusion/invalidity flag;
- researcher notes separated from raw data;
- metric/scorer versions applied later.

Raw outputs must never be overwritten by normalized/scored text.

---

## 15. Invalid pilot runs

Mark a pilot run technically invalid if:

- wrong checkpoint/configuration loaded;
- logging failed materially;
- an input was skipped or corrupted;
- hidden memory/retrieval unexpectedly activated;
- network/tool access occurred contrary to the pilot plan;
- reset verification failed at run start;
- runtime crashed before the minimum analyzable sequence.

Do not mark a run invalid merely because:

- the model repeated itself;
- the model behaved strangely;
- no degradation appeared;
- degradation appeared earlier or later than expected.

All invalid runs remain in public run accounting.

---

## 16. Confirmatory run-count rule

The pilot should estimate:

- per-run wall-clock cost;
- within-condition variability of run-level M001/M002 summaries;
- invalid-run rate;
- scoring workload.

Before confirmatory execution, select a run count using a written sample-size/precision rationale based on those pilot estimates.

Minimum methodological floor for the primary accumulated and fresh comparisons:

- at least **10 independent confirmatory runs per primary condition**, unless a documented computational constraint forces a smaller design;
- any reduction below that floor must be justified **before** confirmatory outputs exist;
- increasing the planned count after seeing confirmatory results is not allowed except under a preregistered sequential design.

The exact final count remains a protocol-freeze decision.

---

## 17. Go/no-go criteria for ACP-EXP-001 freeze

### GO only if

- corpus and manifest are complete and hashed;
- target model/runtime metadata are reproducible;
- fresh-context outputs demonstrate the model can perform the task;
- complete raw logging succeeds for at least 90% of planned pilot runs;
- reset verification succeeds for all runs counted as valid;
- M001 configuration passes the offline validation controls;
- M002 scorer agreement reaches `κ >= 0.60` or the rubric is revised and revalidated;
- M003 threshold-calibration rule can be executed without visual cherry-picking;
- M004 parallel probes are approximately matched in fresh contexts;
- no systematic truncation or hidden compaction invalidates the intended load manipulation;
- environment isolation is confirmed;
- confirmatory run count and randomization policy are written before freeze.

### NO-GO / revise if

- the runtime cannot reliably clear state;
- the model cannot respond coherently in fresh contexts;
- context truncation occurs before the intended accumulated-state regime without being measurable;
- rater agreement remains poor;
- logging loses the data needed for primary metrics;
- the corpus itself produces high recurrence or low responsiveness in fresh contexts;
- experimental conditions differ in ways other than intended state continuity/order.

A no-go decision is not evidence against ACP-H001. It means the measurement system is not yet ready for a confirmatory test.

---

## 18. Pilot reporting

Publish a pilot report before freezing ACP-EXP-001 containing:

- exact system configuration;
- corpus version and hashes;
- condition/run accounting;
- exclusions;
- runtime/resource estimates;
- M001 configuration comparison;
- M002 agreement results;
- proposed frozen M003 thresholds;
- M004 probe-equivalence results;
- reset-verification results;
- protocol changes motivated by pilot findings;
- any unusual behaviors, explicitly labeled exploratory.

Do not present p-values or confirmatory hypothesis claims from ACP-PILOT-001.

---

## 19. Next artifacts after this plan

Before running ACP-PILOT-001, create and review:

1. `pilot/corpus/` — the 32-item synthetic corpus;
2. `pilot/corpus/manifest.json` — hashes, anchors, order, token metadata;
3. `pilot/probes/` — the three parallel ACP-M004 probes;
4. `pilot/run-manifest.schema.json` — required run metadata;
5. `pilot/randomization.json` — frozen shuffled orders and seed policy;
6. `pilot/SCORING.md` — exact M001 implementation and blinded M002 rating workflow.

Those artifacts should be reviewed before the first pilot run so the pilot itself has a reproducible starting point.
