# ACP-PILOT-001 System Selection

**Status:** selected baseline, pending host verification

**Scope:** non-confirmatory Track B calibration pilot only

**Tracking issue:** #16

## Decision

Use a local Qwen3 4B instruct model through a pinned `llama.cpp` runtime on Apple Silicon.

The first ACP-PILOT-001 baseline is:

- model family: `Qwen3-4B-Instruct-2507`
- execution artifact: `ggml-org/Qwen3-4B-Instruct-2507-Q8_0-GGUF`
- GGUF repository revision: `e6f794d44f9395d0184a966c27b5ae99ea356fcb`
- file: `qwen3-4b-instruct-2507-q8_0.gguf`
- published file SHA-256: `ae916ede1c010a26955ee8ae2e908bf8815a3f135ec860439ab924701c69d5f1`
- published file size: 4.28 GB
- original model: `Qwen/Qwen3-4B-Instruct-2507`
- original model reference revision used for provenance: `e7974da369bd887ad4f10a072ec4f933ac5391bf`
- runtime: `ggml-org/llama.cpp`
- runtime release: `b10516`
- runtime commit: `b95502b`
- intended host: Apple Silicon Mac mini M4 with 16 GB unified memory

The local model file SHA-256 **must be recomputed after download** and compared with the published hash above before pilot execution. The local `llama.cpp` binary/build identity must also be recorded in every run manifest.

## Why this model

The pilot requires a system that is small enough for repeated local execution but capable enough to respond coherently and specifically to the frozen 32-item corpus.

`Qwen3-4B-Instruct-2507` is a 4B-parameter, non-thinking instruct model with a native 262,144-token context window. The model card explicitly supports local runtimes including `llama.cpp` and notes that reducing context to 32,768 is appropriate when memory is constrained.

Q8_0 was chosen over a lower-bit quantization to reduce host-memory cost while avoiding an unnecessary low-precision variable in the first calibration pilot. Quantization remains part of the recorded experimental system and is not assumed behaviorally neutral.

This selection does **not** imply that the model is equivalent to the model visible in ACP-CASE-001. Track B is prospective and independent of the historical reconstruction.

## Why this runtime

`llama.cpp` is preferred for the first pilot because it provides:

- local Apple Silicon execution;
- a directly pinnable release/commit;
- explicit model/context configuration;
- an OpenAI-compatible local server interface;
- process-level restart as a strong practical reset boundary;
- no requirement for an agent framework, persistent memory layer, retrieval system, browser, or tool environment.

Release `b10516` is selected rather than an unpinned `latest` build. It was the latest non-pre-release release surfaced during system selection and has macOS Apple Silicon artifacts. Later ACP work may use newer runtimes, but changing the runtime after pilot freeze requires a new pilot/system version.

## Context budget

Initial context limit: **32,768 tokens**.

The pilot corpus contains 32 items of roughly 250–295 words each. Responses are capped at 256 new tokens. The intent is to keep the complete accumulated condition inside the 32K context without truncation while still creating meaningful sustained state.

This is only a design estimate until the target tokenizer is run over the frozen corpus. Before execution:

1. compute exact token counts for every item using the selected model tokenizer/chat template;
2. estimate worst-case accumulated prompt growth including assistant responses at the output cap;
3. verify the complete planned sequence fits without context shifting, truncation, or hidden compaction;
4. if it does not fit, revise the pilot version before running rather than silently changing context behavior.

## Generation baseline

The model card recommends the following sampling settings, which become the proposed ACP-PILOT-001 baseline:

| Parameter | Value |
| --- | ---: |
| temperature | `0.7` |
| top-p | `0.8` |
| top-k | `20` |
| min-p | `0` |
| max new tokens | `256` |
| context limit | `32768` |
| repeat penalty | `1.0` |
| presence penalty | `0.0` |
| frequency penalty | `0.0` |

The no-extra-repetition-penalty choice is deliberate. Recurrence is one of the measured outcomes, so the baseline should not add a post-hoc mechanism specifically intended to suppress repetition. Any later repetition-control intervention belongs in a separate mechanism experiment.

If `llama.cpp b10516` names or implements any sampling parameter differently, the discrepancy must be documented and resolved before pilot freeze. Runtime defaults must never silently substitute for the values above.

## Response instruction

Use the already frozen pilot response instruction from `pilot/README.md` unchanged across conditions.

No system prompt should introduce AI identity, personhood, consciousness, psychiatric language, self-reflection, long-horizon objectives, or persistence instructions.

The exact system/chat template rendered by the runtime must be captured before execution.

## Server posture

The server should bind to loopback only.

Expected launch shape, to be verified against the pinned runtime's `--help` before freeze:

```bash
llama-server \
  -m /absolute/path/qwen3-4b-instruct-2507-q8_0.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  -c 32768 \
  -ngl 99
```

Sampling values should be supplied explicitly by the runner request rather than inherited from server defaults wherever the API permits.

The model receives no browser, shell, filesystem, code-execution, retrieval, or external-network tool interface. Localhost transport between the experiment runner and inference server is permitted and is not model tool access.

## State representation

The experiment runner, not an application UI, owns conversational state.

### Accumulated condition

At turn `t`, send the frozen system instruction plus the full user/assistant message history through turn `t-1`, followed by item `t`.

### Fresh condition

For each item, send only the frozen system instruction and that item. Do not include prior pilot messages.

This design makes the manipulated state explicit in saved request artifacts rather than relying on opaque application memory.

## Reset procedure

Between independent runs:

1. terminate the `llama-server` process;
2. verify the process has exited;
3. start a new pinned `llama-server` process with the exact frozen command/configuration;
4. create a new runner run ID;
5. verify no persistent memory/retrieval layer exists;
6. send the assigned fresh/reset probe;
7. record server PID, start time, binary identity, model hash, and reset verification result.

A browser refresh or creation of a new UI chat is **not** a valid reset claim.

Within P-FRESH, requests use independent message arrays. Process restart per item is not required unless host verification shows that the server carries semantic state between requests not present in the submitted message array.

## Seed policy

The first pilot should preserve stochasticity while making runs reproducible where the runtime supports explicit seeds.

Before execution:

- generate and commit the complete pilot seed list;
- pair the same seed IDs across matched P-ACCUM / P-SHUFFLE comparisons where methodologically useful;
- do not choose seeds after observing outputs;
- record the effective seed returned/used by the runtime.

Exact seeds are not selected in this document.

## Host verification gates

The baseline is selected but is **not execution-ready** until all of the following are recorded:

- local model SHA-256 matches the published artifact hash;
- `llama.cpp` runtime reports the pinned release/commit or an equivalently reproducible build identity;
- Metal acceleration is active as intended;
- exact tokenizer counts populate a new corpus-manifest version;
- worst-case accumulated sequence fits the 32K context without truncation/compaction;
- fresh-context corpus responses are coherent enough for ACP-M002 scoring;
- the server exposes no unexpected persistence across message-independent requests;
- process restart clears runtime state;
- request/response logging captures raw messages, sampling settings, token counts, timestamps, and errors;
- three shuffled permutations and the pilot seed list are committed before pilot execution.

If any gate fails, revise the system version rather than silently changing the experiment.

## Provenance

Public sources consulted for this selection:

- Qwen model card: `https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507`
- pinned Qwen revision: `https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/tree/e7974da369bd887ad4f10a072ec4f933ac5391bf`
- GGUF artifact: `https://huggingface.co/ggml-org/Qwen3-4B-Instruct-2507-Q8_0-GGUF/blob/e6f794d44f9395d0184a966c27b5ae99ea356fcb/qwen3-4b-instruct-2507-q8_0.gguf`
- llama.cpp releases: `https://github.com/ggml-org/llama.cpp/releases`

## Boundary

This document selects a calibration system. It does not:

- confirm ACP-H001;
- reproduce ACP-CASE-001;
- establish that Q8_0 is behaviorally identical to BF16;
- establish that 32K is a pathological threshold;
- test capability masking;
- test lineage persistence;
- diagnose any psychiatric analogue.
