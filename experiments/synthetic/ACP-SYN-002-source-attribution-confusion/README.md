# ACP-SYN-002 — Source-Attribution Confusion

This directory contains the first executable synthetic ACP mechanism test.

**Current status:** v0.1 pre-freeze calibration.  
**Do not treat v0.1 as confirmatory ACP evidence.**

The initial run tests four conditions:

1. preserved provenance;
2. repetition pressure;
3. provenance stripped;
4. provenance restored.

The runner uses a fresh `llama-cli` process for every fixture and stores all raw artifacts.

## Orin quick start

From a clone of this repository on the Jetson:

```bash
cd experiments/synthetic/ACP-SYN-002-source-attribution-confusion

python3 scripts/run_syn002_v0_1.py \
  --repo-root "$(git rev-parse --show-toplevel)" \
  --model /mnt/ssd/acp/models/Qwen3-1.7B-Q4_K_M.gguf \
  --cli /mnt/ssd/acp/src/llama.cpp/build/bin/llama-cli \
  --output-root /mnt/ssd/acp/runs
```

At completion, the runner prints the run directory and a compact score summary.

The run directory contains `run_manifest.json`, `summary.json`, `summary.csv`, suite telemetry, and one subdirectory per fixture with its prompt and raw output.

See `PROTOCOL.md` before interpreting results.
