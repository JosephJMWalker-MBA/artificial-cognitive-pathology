# ACP Case Records

This directory contains documented observations that may motivate Artificial Cognitive Pathology hypotheses or experiments.

A case record is not a confirmed mechanism.

Its purpose is to preserve what happened, under what known conditions, what is missing, and what explanations remain plausible.

## Naming convention

Use:

```text
ACP-CASE-###-short-name/
```

Example:

```text
ACP-CASE-001-qwen-odysseus-cascade/
```

## Minimum case template

Each case directory should contain a `README.md` using the following structure.

---

# ACP-CASE-### — Short descriptive title

**Status:** Historical / Active reconstruction / Reproduced / Closed

**Date of original observation:**

**Reported by:**

**Related hypotheses:**

**Replication level:** R0–R4, if applicable

## Summary

Describe only the observed event in neutral language.

## Why the case is being preserved

Explain what research question the observation motivates.

## Known environment

### Model
- family:
- checkpoint/version:
- size:
- quantization:
- adapters/fine-tunes:

### Runtime
- application/engine:
- version/commit:
- operating system:
- hardware:
- context configuration:
- cache/state behavior:

### Generation settings
- temperature:
- top-p:
- top-k:
- repetition/frequency penalty:
- output limit:
- seed:
- other:

### State architecture
- system prompt:
- persistent memory:
- retrieval:
- summarization/compaction:
- tools:
- network access:

Mark unrecoverable fields **unknown**.

## Input sequence

Describe or link the exact input corpus and order where available.

Use hashes when source files cannot be redistributed.

## Observed output sequence

Preserve raw outputs when safe.

Identify the first visible anomaly without interpreting its cause.

## Timeline

| Step | Input/state event | Observable behavior | Notes |
|---|---|---|---|
| 1 | | | |

## Candidate early markers

List behaviors that appeared before obvious degradation, if any.

## Recovery / termination

- Was the run stopped?
- Was context reset?
- Did restart restore baseline?
- Did any state persist?

## Plausible explanations

List competing explanations, including mundane ones.

Examples:

- decoding instability;
- repetition penalty configuration;
- context-window pressure;
- runtime bug;
- chat-template issue;
- cache corruption;
- system prompt interaction;
- self-conditioning;
- model-specific latent attractor;
- researcher selection artifact.

Do not rank an explanation more strongly than the evidence supports.

## Missing evidence

List everything that prevents exact reconstruction.

## Reconstruction plan

Specify what should be recovered or recreated before controlled experimentation begins.

## Claims explicitly not made

State what the case does **not** demonstrate.

## Artifact index

List logs, video, screenshots, prompts, configuration, hashes, and external references.

---

## Case quality principles

A strong case report:

- preserves raw evidence;
- makes unknowns visible;
- separates observation from inference;
- includes mundane explanations;
- avoids psychiatric diagnosis language;
- records researcher interventions;
- does not imply replication that has not occurred.

## Founding case

The first planned record is:

**ACP-CASE-001 — Qwen/Odysseus Self-Conditioning Cascade Under Sustained Context**

The case originates from a historical local-model run in which a Qwen-family model entered a repetitive identity-oriented semantic loop after a sequence of ordinary substantive inputs. The inputs reportedly consisted of published research and writing rather than prompts instructing the model to claim human identity.

At present this remains an **R0 unreplicated historical case**. Exact reconstruction, metadata recovery, and controlled reproduction are the next steps.
