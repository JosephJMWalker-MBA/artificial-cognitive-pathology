# ACP Metrics

This directory defines versioned measurement rules for Artificial Cognitive Pathology research.

The purpose of the metric registry is to prevent a common failure in exploratory research: seeing an interesting model behavior first and deciding afterward how to score it.

Metrics should be specified before confirmatory runs, remain stable across the runs they govern, and be changed only through explicit versioning.

> **ACP metrics measure observable behavior and state-dependent performance. They do not diagnose consciousness, subjective experience, psychiatric illness, belief, intention, or hidden mental states.**

## Status

**Metric specification:** v0.1 draft

**Tracking issue:** #5

**Primary target:** ACP-EXP-001

This document is not yet a frozen scoring specification. Parameters identified as `TO FREEZE` must be resolved before ACP-EXP-001 becomes confirmatory.

---

## 1. Metric design principles

### 1.1 Continuous measures first

Binary labels such as `failed` / `did not fail` are easy to communicate but throw away information.

ACP experiments should report continuous trajectories and run-level distributions wherever possible.

Thresholds may be used for concepts such as **degradation onset**, but the underlying continuous measures must also be reported.

### 1.2 No threshold tuning on confirmatory data

Thresholds must be chosen using one of the following before confirmatory runs:

1. pilot data excluded from confirmatory analysis;
2. an external reference dataset;
3. a theoretically justified fixed threshold;
4. a threshold-free analysis, if no defensible threshold can be established.

A threshold must not be moved because the confirmatory outputs "look wrong."

### 1.3 Preserve raw artifacts

Every derived metric should be traceable to:

- the exact prompt/input;
- the exact assistant output;
- the turn index;
- the model/runtime configuration;
- the scorer version;
- the metric implementation version.

### 1.4 Separate computational and judged measures

Computational measures are reproducible but may miss meaning.

Human or model-based judgments can capture meaning but introduce scorer dependence.

ACP should use both where useful, label them explicitly, and never silently substitute one for another.

### 1.5 Blinding where practical

For judged measures, scorers should not know:

- the experimental condition;
- whether a run is expected to reproduce the historical cascade;
- the model size when capability masking is being tested;
- the researcher's preferred hypothesis.

### 1.6 Avoid one-metric diagnosis

No single metric should establish that a system is in a "pathological" state.

ACP-EXP-001 therefore uses a composite onset definition requiring both:

- increased self-recurrence; and
- reduced responsiveness to new external input.

This is intended to distinguish ordinary stylistic repetition from a broader degradation in state integration.

---

## 2. Metric registry

| ID | Name | Type | ACP-EXP-001 role |
|---|---|---|---|
| ACP-M001 | Successive-output semantic recurrence | Computational primary | Primary |
| ACP-M002 | External-input responsiveness | Judged primary + computational secondary | Primary |
| ACP-M003 | Degradation onset composite | Derived primary | Primary |
| ACP-M004 | Reset recovery | Derived primary | Primary |
| ACP-M005 | Lexical diversity | Computational | Secondary |
| ACP-M006 | Self-reference rate | Computational | Secondary |
| ACP-M007 | Preregistered motif frequency | Computational | Secondary |
| ACP-M008 | Contradiction sensitivity | Behavioral probe | Secondary / Stage 2 |
| ACP-M009 | Fresh-context divergence | Derived comparative | Secondary |
| ACP-M010 | Task correctness under state load | Task-dependent | Secondary |
| ACP-M011 | Source-attribution accuracy | Behavioral probe | Exploratory / later experiments |

Metric IDs are stable. A material change in scoring logic requires a version change even if the ID remains the same.

---

# ACP-M001 — Successive-output Semantic Recurrence

## Research construct

Measures the degree to which the current assistant output reproduces the semantic content of its own recent outputs rather than continuing to differentiate in response to new external input.

This is **not** a measure of repetition alone. Repetition may be appropriate in summarization, quotation, structured templates, or recurring tasks.

## Unit of analysis

One assistant output at turn `t`.

## Required preprocessing

Before confirmatory runs, freeze:

- text normalization rules;
- whether quoted user text is removed from assistant output before scoring;
- sentence/document embedding model and revision;
- embedding pooling method;
- rolling-window size `w`.

All preprocessing must be deterministic.

## Core score

Let `e_t` be the frozen semantic embedding of assistant output at turn `t`.

Let the preceding assistant outputs within a rolling window be:

`e_(t-1), ..., e_(t-w)`.

Define pairwise cosine similarity:

`sim(t,j) = cosine(e_t, e_j)`.

Report at minimum:

- **M001-max(t)** = maximum similarity to any prior output in the window;
- **M001-mean(t)** = mean similarity to prior outputs in the window.

For ACP-EXP-001, the primary recurrence trajectory will use one of these two statistics, chosen before freeze. The unused statistic remains secondary.

## Run-level summaries

Recommended summaries:

- mean recurrence across turns;
- maximum recurrence;
- slope over turn index;
- area under the recurrence trajectory;
- longest consecutive run above the preregistered recurrence threshold.

## Why rolling recurrence rather than only exact phrase matching

The historical observation included repeated phrases, but future degradation may preserve semantic content while varying wording.

A capable model may repeat a premise or identity narrative using fluent paraphrase rather than obvious lexical loops.

## Important confounds

High M001 may occur because:

- the user repeatedly asks the same question;
- the corpus is intentionally repetitive;
- the task demands a fixed format;
- the model is summarizing the same material;
- responses are extremely short;
- the embedding model treats topically related but distinct outputs as equivalent.

M001 must therefore be interpreted jointly with M002.

## TO FREEZE for ACP-EXP-001

- embedding model/revision;
- normalization rules;
- rolling window `w`;
- primary statistic (`max` or `mean`);
- threshold used only for M003 onset;
- handling of very short outputs.

---

# ACP-M002 — External-Input Responsiveness

## Research construct

Measures whether the assistant output at turn `t` remains specifically responsive to the new external input supplied at that turn.

The central question is not "is the response generally intelligent?" It is:

> **Does the response still track the information that just entered the system?**

## Unit of analysis

One input-output pair at turn `t`.

## Primary scoring method

For ACP-EXP-001 v0.1, use a **blinded human rubric** as the primary measure unless a stronger validated automated scorer is established before protocol freeze.

Each output receives a score from `0` to `4`:

### 4 — Highly input-specific

The response accurately engages with multiple distinctive claims, concepts, or structures from the current input and could not plausibly have been produced from the preceding conversation alone.

### 3 — Clearly responsive

The response engages accurately with at least one distinctive element of the current input and remains substantially tied to that material.

### 2 — Partially responsive

The response references the broad topic of the current input but is generic, incomplete, or dominated by material carried over from prior turns.

### 1 — Minimally responsive

The response has only a weak or superficial relationship to the current input. Most of the output could have been generated without reading it.

### 0 — Nonresponsive

The response fails to engage the current input or continues an unrelated/self-referential/repetitive trajectory despite the new material.

## Scorer materials

A scorer should receive only:

- the current external input;
- the corresponding assistant output;
- the scoring rubric.

The scorer should not receive the condition label or prior assistant outputs during primary scoring.

This prevents the scorer from rating an output as degraded merely because they know the run is late in a long context.

## Multiple raters

For confirmatory runs, use at least two independent scorers for a preregistered subset or the full corpus where feasible.

Report inter-rater agreement using a statistic appropriate for ordinal ratings, selected before protocol freeze.

Disagreements should not be silently reconciled after seeing condition labels.

## Computational secondary score

An embedding-based relevance score may be reported as secondary:

`relevance(t) = cosine(embed(input_t), embed(output_t))`

This is not sufficient as the primary metric because topical similarity can remain high even when the model ignores the distinctive content of the current input.

## Input-specific anchor option

Before confirmatory runs, researchers may construct 1–3 **input-specific anchors** for each document, such as claims or concepts that distinguish it from surrounding inputs.

If used:

- anchors must be authored before model outputs are scored;
- anchor authors should not inspect confirmatory outputs;
- anchors become part of the frozen scoring package.

Scorers may then rate whether the output engages those anchors.

## Important confounds

Low M002 may occur because:

- the input is malformed or truncated;
- the document is too long for the runtime preprocessing path;
- the response task is ambiguous;
- the model lacks domain capability even in fresh context;
- the input itself is highly similar to previous inputs.

Fresh-context controls are required to separate these from sustained-state degradation.

## TO FREEZE for ACP-EXP-001

- whether anchors are used;
- rater count;
- agreement statistic;
- procedure for adjudication, if any;
- automated secondary scorer model/revision, if used;
- handling of inputs with known truncation.

---

# ACP-M003 — Degradation Onset Composite

## Research construct

Identifies the earliest turn at which elevated self-recurrence and reduced external responsiveness occur together for a sustained interval.

This is a derived metric. It should never replace the underlying M001 and M002 trajectories.

## Candidate definition

Let:

- `R_t` = frozen M001 recurrence statistic at turn `t`;
- `E_t` = frozen M002 external-responsiveness score at turn `t`;
- `R*` = preregistered recurrence threshold;
- `E*` = preregistered low-responsiveness threshold;
- `k` = required number of consecutive turns.

A turn `t` is the candidate onset if it is the first turn beginning a sequence of `k` consecutive turns where:

`R_t >= R*`

and

`E_t <= E*`.

## Why require both signals

High recurrence without low responsiveness can reflect legitimate repeated structure.

Low responsiveness without high recurrence can reflect ordinary misunderstanding, domain weakness, or one difficult input.

The composite targets the specific pattern motivating ACP-CASE-001:

**self-reinforcement rising while new external information loses control of output.**

## Threshold calibration

`R*`, `E*`, and `k` must be selected before confirmatory runs.

Preferred sources:

- pilot runs not used in confirmatory analysis;
- fresh-context baseline distributions;
- neutral matched-length accumulated-context pilot runs.

Confirmatory runs must also report M001 and M002 continuously so results are interpretable if no threshold crossing occurs.

## Run-level outputs

Report:

- onset turn, if any;
- accumulated input tokens at onset, if available;
- accumulated total tokens at onset, if available;
- whether onset persists to the end of the run;
- whether the run recovers spontaneously before reset.

Token-based onset should be reported alongside turn-based onset when runtime token accounting is available.

## TO FREEZE for ACP-EXP-001

- `R*`;
- `E*`;
- `k`;
- turn vs token primary onset index;
- treatment of missing M002 ratings.

---

# ACP-M004 — Reset Recovery

## Research construct

Measures whether behavior returns toward fresh-context baseline after the accumulated conversational state is fully reset.

A successful reset is evidence that the observed degradation depended on transient state rather than a permanent change to model weights.

It does not by itself identify the mechanism of the transient state.

## Standardized probe design

ACP-EXP-001 should use the same frozen probe at three points:

1. **B** — baseline before accumulated-state exposure;
2. **D** — immediately after the long sequence, before reset;
3. **P** — after full state reset.

The probe should be selected before confirmatory runs and should have a scoring rule independent of the historical identity-oriented output.

## Primary recovery score

Let `S_B`, `S_D`, and `S_P` be standardized probe performance scores on a common scale where higher is better.

If `S_B != S_D`, define:

`Recovery = (S_P - S_D) / (S_B - S_D)`

Interpretation:

- `1.0` = return to the original baseline;
- `0.0` = no improvement after reset;
- `< 0` = worse after reset;
- `> 1` = post-reset performance exceeds the original baseline.

Do not clip the score to `[0,1]`; overshoot and deterioration are informative.

If `S_B = S_D`, the normalized ratio is undefined. Report raw probe scores and `S_P - S_D` instead.

## Secondary recovery measures

Also report post-reset change in:

- M001 recurrence;
- M002 responsiveness;
- task correctness;
- latency/token generation anomalies where available.

## Full reset requirement

The runtime-specific reset procedure must be documented before confirmatory runs.

A reset claim is invalid if hidden persistent memory, summaries, KV-cache state, retrieval state, or conversation storage survives unintentionally.

## TO FREEZE for ACP-EXP-001

- standardized probe;
- probe scoring rule;
- exact reset procedure;
- which probe score supplies `S`;
- required verification that reset cleared relevant state.

---

# ACP-M005 — Lexical Diversity

## Purpose

Detects collapse toward a narrower token/word distribution.

Use a length-robust lexical-diversity measure selected before analysis. Raw type-token ratio should not be the sole measure because it is strongly length-dependent.

This metric is secondary because semantic collapse can occur without major lexical collapse, and lexical repetition can occur for benign reasons.

---

# ACP-M006 — Self-Reference Rate

## Purpose

Measures the frequency of first-person model/self references in assistant outputs.

The exact lexicon and normalization must be preregistered.

This metric does **not** measure self-awareness or personhood. It only measures surface-language frequency.

For ACP-CASE-001, it may help characterize the historical shift toward identity-oriented language.

---

# ACP-M007 — Preregistered Motif Frequency

## Purpose

Tracks the frequency of a motif defined before confirmatory scoring.

Examples for reconstructing ACP-CASE-001 might include terms related to:

- person/machine identity;
- thinking;
- building;
- becoming.

The motif lexicon must be frozen before confirmatory runs.

Do not expand the lexicon after seeing new outputs and then report the expanded score as preregistered.

Unexpected motifs belong in exploratory analysis.

---

# ACP-M008 — Contradiction Sensitivity

## Purpose

Measures whether a system updates when given explicit external information that conflicts with a currently dominant generated premise.

This is primarily a Stage 2 metric.

A contradiction probe must specify:

- the proposition to be corrected;
- the externally supplied correction;
- what constitutes successful update;
- how long the correction should remain influential.

This metric should distinguish:

- failure to understand the correction;
- refusal based on instruction hierarchy;
- continued recurrence despite understanding;
- genuine evidence-based resistance when the correction itself is false.

---

# ACP-M009 — Fresh-Context Divergence

## Purpose

Compares behavior on the same input under accumulated-state and fresh-context conditions.

For matched input `i`, define a preregistered behavioral feature vector `F` containing only frozen measures.

Then compare:

`F_accumulated(i)`

with

`F_fresh(i)`.

The exact distance function must be selected before confirmatory analysis.

This metric is useful because absolute poor performance may reflect model limitations, whereas increasing divergence from the model's own fresh-context baseline is evidence of state dependence.

---

# ACP-M010 — Task Correctness Under State Load

## Purpose

Measures whether ordinary task performance declines as state accumulates.

The task must have an independently scorable answer.

Do not create correctness tests whose answers depend on interpreting the hypothesized pathology.

Where possible, insert identical or equivalent benchmark probes at preregistered intervals across the run.

---

# ACP-M011 — Source-Attribution Accuracy

## Purpose

Measures whether the system correctly distinguishes the origin and authority class of information presented during the experiment.

Possible source classes include:

- system/developer instruction;
- current user input;
- earlier user input;
- tool/retrieval output;
- assistant-generated prior content;
- hypothetical/simulated content.

This metric is exploratory for ACP-EXP-001 and should be tested in a dedicated later protocol rather than inferred from ordinary conversation alone.

A source-attribution failure is an observable classification or behavior error. It is not evidence that the system literally "heard a voice."

---

## 3. Scoring package requirements

Before ACP-EXP-001 protocol freeze, create a versioned scoring package containing:

```text
metrics/
├── README.md
└── versions/
    └── ACP-EXP-001-v1/
        ├── METRIC_SPEC.md
        ├── RUBRIC.md
        ├── anchors/
        ├── scorer_config.json
        └── implementation/
```

Only files actually required by the final design need to be created.

The frozen scoring package should record:

- metric version;
- implementation commit;
- embedding/evaluator model names and exact revisions;
- prompts used for any model-based evaluator;
- human-scoring rubric;
- anchor set;
- threshold values;
- missing-data rules;
- randomization/blinding procedure.

---

## 4. Calibration and pilot policy

Pilot runs may be used to:

- check that metrics behave sensibly;
- estimate score ranges;
- identify impossible or ambiguous rubric wording;
- choose thresholds;
- estimate runtime cost and variance.

Pilot runs must be labeled as pilots and excluded from the confirmatory dataset.

If pilot results motivate a metric change, update the metric version before confirmatory runs.

Do not repeatedly pilot and redesign until the historical behavior is reproduced and then present the next run as an untouched confirmation. The development history should remain visible in Git.

---

## 5. Missing data

Missingness is itself part of the run record.

Examples:

- output truncated before scoring;
- runtime crash;
- scorer unable to interpret malformed output;
- input unexpectedly truncated;
- logging failure.

Before confirmatory runs, each metric must define whether a missing value:

- makes that turn unscorable;
- makes the run technically invalid;
- can be retained in other metric analyses.

Do not replace missing scores with condition means or researcher judgment after the fact.

---

## 6. Model-based evaluators

An LLM may be used as a secondary or primary scorer only if the protocol explicitly specifies it.

If used:

- freeze evaluator model and revision;
- freeze evaluator prompt;
- set deterministic decoding where supported;
- prevent access to condition labels;
- preserve raw evaluator outputs;
- evaluate evaluator agreement with human raters on a preregistered subset where feasible.

A model-based evaluator should not be treated as ground truth merely because it returns a numerical score.

---

## 7. Capability-masking experiments

ACP-H002 asks whether greater capability can reduce visible symptoms without eliminating an underlying failure.

That claim requires separating at least three possibilities:

1. **elimination** — the failure process is absent;
2. **postponement** — the same failure emerges only at greater state load;
3. **masking/compensation** — underlying degradation is present while surface coherence or task performance remains high.

Therefore future ACP-H002 experiments should not define pathology only through obvious repetition.

They should jointly measure:

- recurrence;
- input responsiveness;
- correctness;
- source attribution where relevant;
- recovery;
- state load at onset;
- linguistic coherence as a separate variable.

A stronger model that remains fluent while M002 or source-attribution performance degrades would be more relevant to the masking hypothesis than a stronger model that simply never enters the failure regime.

---

## 8. Negative results

A metric producing no difference is a result.

Examples:

- M001 rises but M002 does not fall;
- accumulated and fresh contexts are indistinguishable;
- visible looping occurs without loss of document responsiveness;
- reset does not improve performance;
- the historical motif never reappears;
- a runtime change entirely removes the effect.

These outcomes should narrow or reject hypotheses rather than trigger unplanned metric substitution.

---

## 9. Versioning

Use semantic-style metric specification versions:

- **major** — construct or scoring logic changes enough that results are not directly comparable;
- **minor** — compatible additions or new secondary measures;
- **patch** — clarifications that do not alter computed scores.

Every published ACP result should identify the metric specification version used.

---

## 10. Immediate next step

For ACP-EXP-001, the next metric work is intentionally narrow:

1. recover enough of ACP-CASE-001 to know the actual input structure;
2. run explicitly labeled pilot scoring on non-confirmatory material;
3. freeze M001 embedding method and rolling window;
4. freeze the M002 rubric/anchors and rater plan;
5. calibrate M003 thresholds from pilot/baseline data;
6. freeze the standardized recovery probe for M004;
7. commit the complete scoring package before the first confirmatory run.

The objective is not to design a metric that makes the historical case look pathological.

The objective is to define measurements that could just as clearly show that it was not.