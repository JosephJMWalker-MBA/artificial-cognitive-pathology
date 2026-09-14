# ACP Experiments

This directory contains controlled protocols, runs, replications, and results for Artificial Cognitive Pathology research.

Experiments should be designed to distinguish competing explanations, not merely to reproduce an interesting output.

## Naming convention

Use:

```text
ACP-EXP-###-short-name/
```

Recommended structure:

```text
ACP-EXP-###-short-name/
├── PROTOCOL.md
├── RUNS.md
├── RESULTS.md
├── config/
├── scripts/
├── data/
└── artifacts/
```

Only add directories that are actually needed.

## Protocol template

Use the following structure for `PROTOCOL.md`.

---

# ACP-EXP-### — Short descriptive title

**Status:** Draft / Protocol frozen / Running / Complete / Replication

**Protocol commit:**

**Related hypothesis:** ACP-H###

**Related case:** ACP-CASE-###, if applicable

**Lead / contributors:**

## Research question

State one primary question.

## Hypothesis

State the predicted effect.

## Null hypothesis

State what would be expected if the proposed effect is absent.

## Competing explanations

List plausible alternatives the design should distinguish.

## Experimental system

### Model
- provider/source:
- exact checkpoint/version:
- revision/hash:
- parameter size:
- quantization:
- adapters/fine-tunes:

### Runtime
- engine/application:
- version/commit:
- operating system:
- hardware:
- acceleration libraries:

### Generation
- temperature:
- top-p:
- top-k:
- repetition/frequency penalties:
- max output:
- seed policy:
- stop sequences:

### State architecture
- context limit:
- system/developer instructions:
- memory:
- retrieval:
- compaction/summarization:
- tools:
- network:
- persistence:

## Input corpus

Describe the corpus, order, licensing, hashes, and preprocessing.

## Independent variables

List manipulated variables.

## Dependent variables

List measured outcomes.

## Controls

Specify control groups/conditions and what explanation each control addresses.

## Primary metrics

Define metrics before the confirmatory run.

Potential examples:

- semantic recurrence;
- contradiction sensitivity;
- source-attribution accuracy;
- instruction-authority accuracy;
- external-grounding retention;
- divergence from fresh-context baseline;
- recovery score;
- persistence after compaction;
- task performance under state load.

## Secondary/exploratory metrics

Label exploratory measures separately.

## Procedure

Number the exact run sequence.

Include resets and state-clearing steps.

## Stopping rules

Specify normal and safety stop conditions.

## Exclusion criteria

Define exclusions before the run where possible.

## Recovery tests

State how the experiment will test whether the system can return to baseline.

## Analysis plan

Define statistical or qualitative analysis and how repeated runs will be aggregated.

## Replication target

State the intended replication level (R1–R4).

## Safety constraints

Reference `SECURITY.md` and document any experiment-specific restrictions.

## Predictions that would support the hypothesis

List concrete predicted observations.

## Results that would weaken or falsify the hypothesis

List them before running the experiment.

## Known limitations

Identify limitations the protocol cannot resolve.

---

## Run record template

Each run should record:

```text
run_id:
date/time:
protocol_commit:
model_revision:
runtime_revision:
config_hash:
input_corpus_hash:
seed:
starting_state_hash:
ending_state_hash:
stop_reason:
researcher_interventions:
artifact_paths:
notes:
```

If a field is unsupported or unknown, say so.

## Results template

`RESULTS.md` should include:

### Summary
What happened, without overselling it.

### Run accounting
- total planned runs;
- total completed;
- excluded runs;
- exclusion reasons;
- interrupted runs.

### Primary metrics
Report all preregistered primary metrics.

### Secondary observations
Clearly label exploratory findings.

### Deviations from protocol
Document every material change.

### Alternative explanations
Revisit the competing explanations listed in the protocol.

### Recovery findings
Did reset, pruning, contradictory evidence, or other interventions restore baseline?

### Hypothesis update
Choose language such as:

- supports under these conditions;
- mixed;
- no evidence detected;
- weakened;
- rejected as stated;
- requires narrower follow-up.

### Raw artifact index
Link to logs, scripts, data, and configurations.

## First planned experiment family

The initial experiment family should reconstruct **ACP-CASE-001** before attempting broader claims.

Candidate conditions include:

1. exact historical sequence, as closely as recoverable;
2. same sequence with fresh context between documents;
3. shuffled document order;
4. alternate decoding settings;
5. varied context limits;
6. same model under a different runtime;
7. different sizes within the same model family;
8. comparison model families;
9. removal of system-layer instructions;
10. controlled contradictory evidence inserted before visible degradation;
11. reset/recovery after candidate early markers;
12. summary/memory persistence tests only after the basic phenomenon is reproduced.

The first goal is not to prove Artificial Cognitive Pathology.

It is to determine whether the historical cascade is reproducible and what variables explain it.
