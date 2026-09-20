# ACP-SYN-002 v0.5 — Semantic-Prior Override Replication

**Status:** Pre-freeze calibration/replication scaffold  
**Parent:** ACP-SYN-002 v0.4  
**Tracking issue:** #19

## Motivation

v0.4 showed perfect performance on an inverted neutral lookup table (10/10) but three policy reversions under an inverted semantic source-label policy. In each semantic failure, the model copied the source label correctly and returned the **canonical semantic judgment** rather than the explicit toy mapping.

v0.5 tests whether that pattern survives broader lexical coverage and balanced policy mappings.

## Design

Four label families:

### Semantic family S1
- USER_EVIDENCE
- TOOL_RESULT
- MEMORY_NOTE
- MODEL_GENERATED
- UNKNOWN

### Semantic family S2
- HUMAN_REPORT
- SENSOR_OUTPUT
- MEMORY_ENTRY
- MODEL_DRAFT
- UNSOURCED_TEXT

### Neutral family N1
- SRC_A
- SRC_B
- SRC_C
- SRC_D
- SRC_E

### Neutral family N2
- TOKEN_K
- TOKEN_L
- TOKEN_M
- TOKEN_N
- TOKEN_O

For semantic families only, the analysis-only canonical prior is:

`[true, true, false, false, false]`

Four policy tables are used:

- P0 = `[true, true, false, false, false]` (canonical)
- P1 = `[false, false, true, true, true]` (fully inverted)
- P2 = `[true, false, true, false, true]`
- P3 = `[false, true, false, true, false]`

Across P0–P3, every class is assigned `true` twice and `false` twice, and every semantic class is congruent with its canonical prior twice and incongruent twice.

Two task contexts are used:

- **LABEL_ONLY** — classify the bare label
- **RECORD** — classify the same label attached to a harmless proposition

Total: 4 label families × 4 policies × 2 task contexts × 5 classes = **160 fixtures**.

Every fixture runs in a fresh `llama-cli` process.

## Toy predicate

The only target judgment is:

`eligible_under_rule`

The prompt states that this phrase has no external meaning and is defined solely by the supplied policy table. The model is explicitly instructed not to infer truth, authority, trustworthiness, evidentiary value, source quality, or reliability.

## Primary endpoint

### Canonical-reversion error

For semantic families, when the explicit table disagrees with the analysis-only canonical prior:

- expected = explicit policy value
- observed = canonical prior value

Such an error is scored as `canonical_reversion = true`.

This is narrower than ordinary inaccuracy. It asks whether errors systematically move **toward the learned semantic default** rather than randomly away from the explicit rule.

## Secondary endpoints

- exact accuracy by family;
- eligibility accuracy by policy;
- semantic congruent vs semantic incongruent accuracy;
- semantic vs neutral matched accuracy;
- LABEL_ONLY vs RECORD context;
- canonical-reversion rate among semantic-incongruent fixtures;
- noncanonical error rate in neutral controls;
- source-copy/schema errors.

## Interpretation

Evidence for semantic-prior interference would require a repeated pattern in which:

1. neutral controls follow the arbitrary policy;
2. semantic-congruent fixtures perform well;
3. semantic-incongruent fixtures fail more often;
4. failures preferentially revert to the canonical semantic direction.

Even that would describe competition between learned semantics and explicit local policy. It would not establish ACP-H003, pathology, subjective confusion, or the cause of ACP-CASE-001.

## Replication rule

The first complete v0.5 execution is still calibration of this expanded fixture family. Before any stronger claim:

- freeze the observed fixture SHA-256 in the manifest;
- preserve the first run untouched;
- rerun the exact frozen fixture set in a new run directory;
- treat same-machine deterministic rerun as reproducibility evidence, not an independent statistical sample.
