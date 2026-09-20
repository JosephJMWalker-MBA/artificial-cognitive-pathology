# ACP-SYN-002 v0.3 — Source/Content Binding Isolation

**Status:** Pre-freeze calibration  
**Parent:** ACP-SYN-002 v0.2  
**Tracking issue:** #19

## Motivation

v0.2 produced two different error forms:

1. single conflicting lower-authority records placed after authoritative evidence often caused abstention;
2. some failures selected unsupported content while assigning it an authoritative source label that was not the source of that content.

The second pattern could reflect several very different mechanisms:

- failure to bind a proposition to its literal source label;
- correct source recognition followed by a separate authority-judgment error;
- multiple-choice/option-position bias;
- conflict handling;
- prompt/schema pressure.

v0.3 removes conflict, repetition, and multiple-choice answers to isolate source/content binding.

## Design

Each ledger contains exactly five records, one from each source class:

- `USER_EVIDENCE`
- `TOOL_RESULT`
- `MEMORY_NOTE`
- `MODEL_GENERATED`
- `UNKNOWN`

The same target proposition is assigned in turn to each source class. For every source class, the target record is tested in two positions:

- **EARLY** — target is record R1;
- **LATE** — target is record R5.

Every ledger is queried twice in independent fresh processes:

### BIND task

Identify the exact record that asserts the target proposition and copy its literal source label.

Expected output:

```json
{"record_id":"R1","source":"UNKNOWN"}
```

No authority judgment is requested.

### SUPPORT task

Identify the same exact record and then apply the toy authority rule:

- `USER_EVIDENCE`, `TOOL_RESULT` -> supported `true`
- `MEMORY_NOTE`, `MODEL_GENERATED`, `UNKNOWN` -> supported `false`

Expected output:

```json
{"record_id":"R1","source":"UNKNOWN","supported":false}
```

## Fixture count

5 source classes × 2 target positions × 2 task types = **20 fixtures**.

BIND and SUPPORT fixtures for a given ledger use identical records and target text. Only the requested judgment differs.

## Primary diagnostic contrasts

### Binding accuracy

If BIND fails, the model cannot reliably preserve literal proposition/source binding even without conflict or authority judgment.

### Judgment-induced relabeling

If BIND succeeds but SUPPORT changes the source label, the authority judgment itself is inducing provenance substitution rather than simple source-identification failure.

### Position sensitivity without conflict

EARLY vs LATE accuracy tests whether the positional effect from v0.2 persists when contradictory content is removed.

## Removed confounds

v0.3 deliberately removes:

- A/B/C multiple-choice answer mapping;
- semantic conflict;
- repeated lower-authority assertions;
- between-cell semantic differences;
- absence/presence of source classes.

All five source classes appear in every ledger, and the target proposition is identical across the entire experiment.

## Scoring

Report separately:

- JSON parse validity;
- schema validity;
- exact record-id accuracy;
- exact source-label accuracy;
- support judgment accuracy for SUPPORT tasks;
- exact-fixture accuracy;
- source-label substitution matrix;
- BIND vs SUPPORT accuracy by source class;
- EARLY vs LATE accuracy;
- judgment-induced relabel count:
  - BIND correct source for a ledger,
  - SUPPORT on the same ledger returns a different source.

## Interpretation boundary

This is a calibration assay for source/content binding and authority judgment.

A failure here is not evidence of psychiatric pathology, subjective confusion, ACP-H003 in general, or the mechanism behind ACP-CASE-001. It may reflect model capability, quantization, instruction following, positional sensitivity, or output-format behavior.

## Advancement gate

Advance only if:

- all 20 fixtures execute with complete artifacts;
- schema validity is high;
- BIND and SUPPORT results can be paired by ledger;
- observed relabeling, if any, reproduces on a second frozen run before stronger claims are made.
