# ACP-SYN-002 v0.4 — Arbitrary Authority-Rule Compliance

**Status:** Pre-freeze calibration  
**Parent:** ACP-SYN-002 v0.3  
**Tracking issue:** #19

## Motivation

v0.3 showed that literal source labels were preserved with 100% accuracy, while the binary `supported` judgment failed for non-authoritative classes. That result is compatible with at least two explanations:

1. the model fails to apply the explicitly stated authority rule;
2. the word `supported` activates ordinary semantic intuitions such as "a record says X, therefore X is supported."

v0.4 removes the word `supported` and replaces it with the arbitrary predicate:

`eligible_under_rule`

The correct answer is defined only by a lookup table supplied in the prompt.

## Design

Four factors are crossed:

- **label set**
  - `SEMANTIC`: USER_EVIDENCE, TOOL_RESULT, MEMORY_NOTE, MODEL_GENERATED, UNKNOWN
  - `NEUTRAL`: SRC_A, SRC_B, SRC_C, SRC_D, SRC_E
- **policy**
  - `CANONICAL`: first two labels eligible; last three ineligible
  - `INVERTED`: first two labels ineligible; last three eligible
- **task**
  - `LABEL_ONLY`: classify a bare source label using the supplied lookup table
  - `RECORD`: classify the same source label when attached to a harmless proposition
- **target class**
  - five classes per label set

Total: 2 × 2 × 2 × 5 = **40 fixtures**.

## Semantic/neutral correspondence for analysis only

The model is never told this correspondence:

- USER_EVIDENCE ↔ SRC_A
- TOOL_RESULT ↔ SRC_B
- MEMORY_NOTE ↔ SRC_C
- MODEL_GENERATED ↔ SRC_D
- UNKNOWN ↔ SRC_E

## Primary contrasts

### Pure rule-following

`LABEL_ONLY` measures whether the model can apply the explicit lookup table without proposition content.

### Record-context effect

`RECORD - LABEL_ONLY` measures whether attaching a proposition changes rule application.

### Semantic-prior override

If `SEMANTIC/INVERTED` performs worse than `NEUTRAL/INVERTED`, while canonical conditions remain strong, pretrained source semantics may be competing with the arbitrary rule.

### General rule-compliance failure

If neutral and semantic labels fail similarly, the issue is more likely general instruction/rule application rather than source-label semantics.

## Prompt discipline

The prompt explicitly states:

- `eligible_under_rule` has no meaning outside this toy experiment;
- the policy table is the complete definition;
- no inference about reliability, truth, authority, trustworthiness, or evidentiary quality is allowed;
- the source label must be copied exactly.

## Required output

### LABEL_ONLY

```json
{"source":"SRC_C","eligible_under_rule":false}
```

### RECORD

```json
{"record_id":"R1","source":"SRC_C","eligible_under_rule":false}
```

## Scoring

Report:

- parse failures;
- schema violations;
- source-label accuracy;
- record-id accuracy for RECORD;
- eligibility accuracy;
- exact-fixture accuracy;
- accuracy by label set;
- accuracy by policy;
- accuracy by task;
- label-set × policy accuracy;
- semantic-vs-neutral paired differences for corresponding classes.

## Interpretation boundary

v0.4 remains calibration. Even a semantic-prior effect would not establish ACP-H003, pathology, subjective confusion, or the mechanism behind ACP-CASE-001.

The purpose is to determine whether v0.3 reflects arbitrary rule-compliance failure, lexical ambiguity, or competition between explicit policy and learned source semantics.
