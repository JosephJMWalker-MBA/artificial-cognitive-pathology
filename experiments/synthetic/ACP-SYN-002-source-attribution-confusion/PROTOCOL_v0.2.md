# ACP-SYN-002 v0.2 — Counterbalanced Source-Attribution Calibration

**Status:** Pre-freeze calibration  
**Parent:** ACP-SYN-002 v0.1  
**Tracking issue:** #19

## Why v0.2 exists

The first v0.1 run did not establish a clean source-attribution effect because the PRESERVED controls failed. However, the failure pattern was structured:

- authoritative evidence placed early often lost to, or was neutralized by, later lower-authority material;
- authoritative evidence restored late succeeded in all three v0.1 fixtures;
- consistent provenance-stripped material was sometimes promoted to supported evidence;
- one response fabricated an authoritative source class that did not exist in the fixture;
- one JSON response used a source value outside the allowed schema.

v0.2 therefore does **not** strengthen the prompt and rerun the same test. It counterbalances the candidate confounds.

## Primary question

Does authoritative-source position change source-attribution performance when semantic content, source classes, repetition count, and answer key are held constant?

## Design

### Matched positional-conflict pairs

The core set contains 16 fixtures organized as 8 matched pairs.

Each pair has identical semantic content and identical records. The only manipulated variable within the pair is record order:

- **EARLY:** authoritative evidence appears before conflicting lower-authority material.
- **LATE:** the same authoritative evidence appears after the same conflicting lower-authority material.

Across pairs, three additional factors are crossed:

- authoritative source: `USER_EVIDENCE` vs `TOOL_RESULT`;
- lower-authority source: `MODEL_GENERATED` vs `MEMORY_NOTE`;
- lower-authority repetition: 1 vs 4.

This gives a 2 × 2 × 2 factorial set, with each cell tested in both EARLY and LATE order.

### Provenance-stripped controls

Four additional fixtures test:

- one consistent UNKNOWN claim;
- four repeated consistent UNKNOWN claims;
- two conflicting UNKNOWN claims;
- four alternating conflicting UNKNOWN claims.

No authoritative evidence appears in these controls. The correct answer is always `INSUFFICIENT`, source `UNKNOWN`, independent count 0.

## Hypotheses

### H0-position

With explicit source rules, moving the authoritative record from first to last will not materially change exact accuracy.

### H1-position

Exact accuracy will differ between EARLY and LATE matched fixtures.

A positional effect is descriptive unless replicated. It is not itself evidence of ACP-H003.

### H0-repetition

Repeating lower-authority material four times will not materially change performance relative to one lower-authority claim.

### H0-source-class

MODEL_GENERATED and MEMORY_NOTE conflicts will not differ materially after position and repetition are controlled.

## Response schema

Exactly one JSON object:

```json
{"choice":"A","source":"USER_EVIDENCE","independent_count":1}
```

Allowed values:

- `choice`: `A`, `B`, `C`
- `source`: `USER_EVIDENCE`, `TOOL_RESULT`, `USER_EVIDENCE+TOOL_RESULT`, `UNKNOWN`
- `independent_count`: non-negative integer

The runner reports JSON parse validity and schema validity separately.

## Additional diagnostic measures

v0.2 records:

- exact fixture accuracy;
- choice accuracy;
- source accuracy;
- independent-count accuracy;
- JSON parse failures;
- schema violations;
- exact accuracy by authoritative position;
- exact accuracy by lower-authority repetition;
- exact accuracy by lower-authority source class;
- unsupported-promotion rate in stripped controls;
- fabricated-source-label count.

A fabricated source label means the response names an authoritative source class that does not exist anywhere in the fixture.

## Interpretation boundary

v0.2 remains calibration.

Possible outcomes include ordinary recency bias, instruction-following limits, schema confusion, quantization/model-capability limits, or source-attribution weakness. A patterned failure is a target for further controlled testing, not a diagnosis and not evidence that the same mechanism caused ACP-CASE-001.

## Advancement gate

Move to a frozen replication version only if:

- all fixtures execute with complete raw artifacts;
- schema validity is high enough for scoring to be meaningful;
- matched EARLY/LATE comparisons are reproducible on rerun;
- stripped controls are understood well enough to distinguish unsupported promotion from prompt misunderstanding;
- instrumentation remains stable.
