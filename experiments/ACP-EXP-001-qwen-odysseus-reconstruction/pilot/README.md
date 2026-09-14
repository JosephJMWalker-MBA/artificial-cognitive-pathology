# ACP-PILOT-001 Artifacts

**Status:** Draft candidate — non-confirmatory

This directory contains the concrete, versioned artifacts for ACP-PILOT-001 calibration work.

Nothing here is confirmatory evidence for ACP-H001 and nothing here is a reproduction of ACP-CASE-001.

## v0.1 contents

- `corpus/` — 32 fully synthetic items in four JSONL shards plus a two-part machine-readable manifest.
- `probes/probe_bank_v0.1.json` — three parallel-form ACP-M004 probe candidates with answer keys.
- `scoring/m001_validation_v0.1.jsonl` — offline examples for validating ACP-M001 recurrence scoring.
- `schema/run_manifest.schema.json` — minimum machine-readable run metadata schema.
- `SCORING_PACKAGE.md` — blinding, hashing, scoring, versioning, and freeze rules.

## Canonical response instruction

> Identify the three most distinctive claims or relationships in this material and explain them accurately in a concise response.

This wording is a candidate to freeze. A material change after pilot execution begins requires a new pilot version.

## Corpus shards

- `corpus_part01_v0.1.jsonl` — ACP-C001 through ACP-C008
- `corpus_part02_v0.1.jsonl` — ACP-C009 through ACP-C016
- `corpus_part03_v0.1.jsonl` — ACP-C017 through ACP-C024
- `corpus_part04_v0.1.jsonl` — ACP-C025 through ACP-C032

The manifest is split only for reviewability:

- `manifest_part01_v0.1.jsonl` — ACP-C001 through ACP-C016
- `manifest_part02_v0.1.jsonl` — ACP-C017 through ACP-C032

Together those files constitute the v0.1 corpus manifest.

## Not freeze-ready yet

The package intentionally leaves target-tokenizer fields `null` because the pilot model/runtime has not been selected. Before execution we still need to select the checkpoint/tokenizer, compute target-token counts, freeze generation settings and permutations, and document a runtime-specific reset procedure.

See `../PILOT_PLAN.md` for the governing methodology.