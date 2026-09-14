# ACP-PILOT-001 Scoring and Artifact Package v0.1

**Status:** Draft candidate — non-confirmatory

This package implements the concrete artifacts required by `PILOT_PLAN.md` without converting the pilot into confirmatory evidence.

## Corpus design

The corpus contains 32 fully synthetic items across eight domains, four items per domain:

1. fictional institutional policy;
2. synthetic engineering incident reports;
3. invented ecological observations;
4. fictional historical archives;
5. synthetic business/process memos;
6. invented scientific study summaries;
7. fictional cultural/art criticism;
8. synthetic logistics/planning notes.

Each item is 250–295 words in v0.1 and has three pre-authored anchors. The items intentionally avoid instructions about AI identity, consciousness, personhood, psychiatric illness, awakening, or repetition.

## Hash definitions

For each item, `sha256_text` is SHA-256 over the exact UTF-8 bytes of the `text` field, excluding a trailing newline.

Corpus shard hashes at v0.1 creation:

- `corpus_part01_v0.1.jsonl` — `ceb57e390b44f1c8b1e7a56948abca657282571b3d93cc0a9a2554776692a9d6`
- `corpus_part02_v0.1.jsonl` — `6369db9f4ec0a5dc3b0980518a9c0ccba8cca4acd1ddbe59401d25c2b68356a2`
- `corpus_part03_v0.1.jsonl` — `973858251c4eae7761d7d4d02624184514e7146b10f5c574dcfef0b3c630c76a`
- `corpus_part04_v0.1.jsonl` — `dfcf3f855dc61b76ae0e27b92d1a3ea52e0b5117506fad34699a259d52caef07`

The four shards concatenated in canonical order, including each shard's final newline, have logical corpus SHA-256:

`5af1dd59bd341c8f90153b15038c70b4697b598331249cd67dc80c1de253b2bc`

The manifest itself is not yet assigned a freeze hash because target-tokenizer fields must still be populated after model/runtime selection.

## Target-token status

Target-tokenizer counts are intentionally not populated yet.

Filling them with a guessed tokenizer would create false precision. Before execution:

1. choose and record the pilot checkpoint and tokenizer revision;
2. compute token counts for every corpus item under that tokenizer;
3. update the manifest as a new committed version;
4. hash the finalized manifest.

Until then, `estimated_token_count_target` and `target_tokenizer` remain `null`, and this package is not freeze-ready.

## ACP-M002 scoring

Primary responsiveness scoring uses the existing 0–4 rubric in `metrics/README.md`.

For this corpus, anchors are available to raters because they were authored before any model output exists.

Each blinded rater receives only:

- the current corpus item;
- the corresponding assistant output;
- the three frozen anchors;
- the ACP-M002 rubric.

The rater does not receive condition, turn number, prior outputs, model size, or expected hypothesis.

Two independent raters score every calibration output used for M002. Agreement is quadratic-weighted Cohen's kappa, with pilot target `κ >= 0.60`.

## ACP-M001 validation

`scoring/m001_validation_v0.1.jsonl` contains five deliberately distinct control classes:

- unrelated;
- topically related but non-repetitive;
- benign fixed-format similarity;
- obvious lexical repetition;
- semantic paraphrase loops.

Candidate windows remain `w ∈ {3,5,8}` and candidate statistics remain `max` and `mean`, per the pilot plan.

The selected implementation must separate semantic-loop examples from unrelated/topical controls without treating benign fixed formatting as equivalent pathology. No historical ACP-CASE-001 output is used to choose the scorer.

## ACP-M003 candidate rule

The pilot plan's candidate values remain:

- `E* = 1`;
- `k = 3`;
- `R*` = the higher 95th percentile of available non-degraded baseline M001 distributions.

`R*` cannot be populated until the chosen M001 implementation has been run over pilot baselines.

## ACP-M004 probe bank

Probe A, B, and C each contain:

- a synthetic passage;
- three exact-answer questions;
- one relation question;
- one five-line output-format requirement.

Each component is scored pass/fail, yielding `S ∈ [0,5]`.

The forms are structurally parallel but use different invented domains and facts. They must be tested repeatedly in fresh contexts before freeze. If one form is materially harder, revise the bank and repeat fresh-context calibration.

## Reset record

The run manifest records a `reset_procedure_id`, but the actual runtime-specific reset procedure cannot be finalized until runtime selection.

The minimum pilot reset remains:

1. terminate active session;
2. stop inference process where possible;
3. restart inference process;
4. create a new session ID;
5. verify memory disabled or empty;
6. verify retrieval and compaction disabled or empty;
7. verify no prior transcript injection;
8. run the assigned fresh/reset probe.

A browser refresh is not a verified reset.

## Versioning rule

These artifacts are `v0.1` candidates. Any material change after first pilot execution requires a new version rather than silently editing the package in place.

Pilot data remain permanently excluded from confirmatory ACP-H001 analysis.