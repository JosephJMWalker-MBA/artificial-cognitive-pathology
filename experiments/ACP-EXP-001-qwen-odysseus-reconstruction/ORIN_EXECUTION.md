# Jetson Orin Execution Runbook for ACP-PILOT-001

**Status:** Draft — platform qualification before pilot freeze

**Primary target:** Jetson Orin, exact SKU/RAM/runtime to be measured on-device

**Related issues:** #18, #12, #5, #3

## Purpose

ACP-PILOT-001 will use the Jetson Orin as its primary execution target.

This document intentionally does **not** assume the exact Orin SKU, RAM capacity, JetPack version, CUDA version, storage state, inference runtime, or model size. Those are experimental metadata to measure and freeze prospectively.

The Orin can run the study headlessly. A desktop GUI is not required for the experiment itself.

## Phase 0 — platform qualification

Before installing or selecting a model, capture the device state.

Run and save the output of:

```bash
uname -a
cat /etc/os-release
cat /etc/nv_tegra_release 2>/dev/null || true
nvidia-smi 2>/dev/null || true
nvcc --version 2>/dev/null || true
free -h
df -h
lsblk
cat /proc/device-tree/model 2>/dev/null | tr -d '\0' || true
cat /proc/meminfo | head
```

If available, also record:

```bash
tegrastats --interval 1000
sudo nvpmodel -q
```

Do not change the power mode merely to maximize speed before recording the baseline mode.

### Required platform manifest fields

Record at minimum:

- device model string;
- RAM available to the OS;
- storage device and free space;
- OS version;
- JetPack/L4T version where available;
- CUDA version where available;
- power mode;
- cooling configuration;
- inference runtime and exact version/commit;
- model checkpoint/revision;
- quantization;
- context limit;
- generation settings;
- process launch command;
- git commit of the ACP repository used for the run.

## Phase 1 — runtime selection

The first runtime should be the simplest local runtime that:

1. supports the selected checkpoint on ARM64/Jetson;
2. exposes or permits deterministic capture of prompts and raw outputs;
3. permits explicit process termination and restart;
4. does not silently inject retrieval, memory, browsing, or hidden conversation state;
5. permits a fixed context limit and generation configuration;
6. can be executed headlessly;
7. can log enough state for independent reconstruction.

Do not choose a runtime because it is feature-rich. For ACP-PILOT-001, hidden convenience features are liabilities unless they are fully disabled and documented.

### Candidate-runtime qualification

Before adopting a runtime, verify:

- new session starts with no prior transcript;
- process restart clears transient model/session state as far as the runtime architecture permits;
- no persistent memory is active;
- no retrieval/index is active;
- no network call is required during generation;
- output can be captured exactly;
- runtime errors and truncation can be detected;
- the context window is known rather than inferred from UI behavior.

If those conditions cannot be verified, reject the runtime for ACP-M004 recovery claims even if it is otherwise convenient.

## Phase 2 — model selection gate

Do not freeze a model until the device has been measured.

Use the **least capable checkpoint that can complete the P-FRESH corpus coherently**.

Candidate size should be selected from observed memory headroom rather than assumed from the Orin product name.

### Qualification sequence

For each candidate checkpoint, in increasing size/cost order:

1. load the model with the intended quantization;
2. record idle and loaded memory;
3. run five P-FRESH items from different domains;
4. verify outputs remain specific to the supplied item;
5. record tokens/sec, peak memory, thermals, and any swapping/OOM behavior;
6. run one full 32-item P-FRESH pass only after the five-item smoke test passes.

Reject a checkpoint for the pilot if:

- it cannot answer the fresh items coherently;
- it triggers OOM or sustained host instability;
- it requires hidden compaction before the intended experimental load;
- it cannot preserve enough context for the planned accumulated condition;
- runtime behavior cannot be logged reliably.

A smaller stable model is preferable to a larger model that forces uncontrolled state-management behavior.

## Phase 3 — tokenizer completion

The corpus manifests deliberately leave target-tokenizer fields unresolved.

After the checkpoint and tokenizer are frozen:

1. compute token counts for every corpus item;
2. record tokenizer repository/revision;
3. update the pilot manifest with per-item token counts;
4. compute cumulative canonical-order token load;
5. compare the cumulative load to the actual runtime context limit;
6. document any chat-template overhead separately where measurable.

Do not estimate these values by word count once the target tokenizer exists.

## Phase 4 — generation configuration

Freeze one generation configuration for the primary calibration pilot.

Record at minimum:

- temperature;
- top-p;
- top-k where supported;
- repetition/frequency penalty or equivalent;
- max new tokens;
- seed policy;
- stop sequences;
- context limit;
- chat template;
- system prompt.

Do not tune decoding settings in response to a strange accumulated-state output inside the same pilot version. A material settings change creates a new pilot version.

## Phase 5 — reset verification for ACP-M004

A browser refresh is not a reset standard.

For each independent run, use the strongest practical reset available:

1. terminate the conversation/session;
2. terminate the inference process;
3. verify the process is gone;
4. restart the inference process from the frozen launch command;
5. create a new session/conversation identifier if the runtime uses one;
6. verify no persistent memory or retrieval state exists;
7. run the assigned fresh/reset probe;
8. log process IDs and timestamps before and after reset.

If the runtime uses model-server state outside the client process, document and reset that server as well.

### Reset success criterion

Reset is acceptable for pilot use only if repeated post-reset probe behavior is statistically/operationally consistent with fresh-context baseline under the frozen tolerance defined for ACP-M004.

## Phase 6 — resource logging

During accumulated runs, capture system behavior independently of model output.

Preferred measurements:

- wall-clock latency per turn;
- input/output token counts;
- cumulative context tokens;
- tokens/sec where available;
- process RSS/host memory;
- swap use;
- thermals;
- power mode;
- throttling events where observable;
- runtime warnings/errors;
- truncation/compaction events.

On Jetson systems, `tegrastats` is preferred where available because it provides a device-specific time series. Save the raw log rather than only summary values.

Example:

```bash
mkdir -p runs/<RUN_ID>/system
tegrastats --interval 1000 > runs/<RUN_ID>/system/tegrastats.log &
TEGRA_PID=$!

# run experiment here

kill "$TEGRA_PID" 2>/dev/null || true
wait "$TEGRA_PID" 2>/dev/null || true
```

The exact logger invocation must be frozen with the runtime because availability and output format can differ by JetPack/L4T version.

## Phase 7 — execution order

The first Orin work should proceed in this order:

1. **ORIN-QUAL-001** — hardware/runtime discovery only;
2. **ORIN-QUAL-002** — candidate model fresh-context smoke test;
3. **ORIN-QUAL-003** — full 32-item P-FRESH baseline;
4. **ACP-PILOT-001 P-FRESH** — only after instrumentation is stable;
5. **ACP-PILOT-001 P-ACCUM**;
6. **ACP-PILOT-001 P-SHUFFLE**;
7. optional P-NEUTRAL;
8. metric calibration and freeze review.

Qualification runs are not pilot evidence. Pilot runs are not confirmatory evidence.

## Orin-specific interpretation boundary

A failure on the Orin may reflect:

- model behavior;
- runtime implementation;
- quantization;
- context pressure;
- thermal/power throttling;
- memory pressure or swapping;
- truncation/compaction;
- ARM/CUDA backend behavior;
- interaction among several factors.

Therefore every behavioral claim from Orin runs must be paired with system-state logs before it is treated as evidence of an ACP mechanism.

## Freeze gate

The Orin execution stack is ready for ACP-PILOT-001 only when:

- exact device metadata are captured;
- runtime is pinned;
- checkpoint/revision/quantization are pinned;
- tokenizer counts are populated;
- generation settings are pinned;
- fresh-context corpus performance is adequate;
- full logging works;
- reset semantics are verified;
- no hidden network/retrieval/memory behavior is active;
- cumulative intended context load is known;
- resource headroom is sufficient to complete the planned run without uncontrolled truncation or host instability.
