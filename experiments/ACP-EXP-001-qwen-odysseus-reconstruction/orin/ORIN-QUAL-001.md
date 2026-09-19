# ORIN-QUAL-001 — Jetson Orin Hardware Qualification

**Status:** Initial hardware qualification captured

**Date:** 2026-09-14

**Target:** ACP-PILOT-001 primary execution platform

## Device identity

Observed command output identifies the device as:

- device: `NVIDIA Jetson Orin Nano Engineering Reference Developer Kit Super`
- architecture: `aarch64`
- kernel: `Linux 6.8.12-1021-tegra`
- Ubuntu: `24.04.4 LTS (Noble Numbat)`
- Jetson Linux / L4T: `R39`, revision `2.1`
- kernel variant: `oot`

## NVIDIA software stack

- NVIDIA driver: `595.78`
- CUDA runtime reported by `nvidia-smi`: `13.2`
- CUDA toolkit (`nvcc`): `13.2`, build `V13.2.86`
- GPU: `Orin (nvgpu)`

## Power mode

`nvpmodel -q` reports:

- power mode: `25 W`
- mode ID: `1`

Record this exact mode for qualification and pilot manifests. Do not silently switch power modes between matched runs.

## Memory

`free -h` at qualification time:

- total RAM: `7.3 GiB`
- used: `2.8 GiB`
- free: `2.1 GiB`
- available: `4.5 GiB`
- swap total: `15 GiB`
- swap used: `1.9 GiB`

Interpretation boundary: this is an 8 GB-class Orin Nano with approximately 7.3 GiB visible system RAM. ACP experiments must use measured available RAM and must not treat swap as equivalent to model-resident memory.

## Storage

Primary root filesystem:

- `/dev/mmcblk0p1`: `233G` size, `158G` available

NVMe experiment storage:

- `/dev/nvme0n1p1` mounted at `/mnt/ssd`
- `916G` filesystem size reported by `df -h`
- `851G` available
- block device size `931.5G`

**ACP execution choice:** prefer `/mnt/ssd` for model weights, run artifacts, logs, temporary outputs, and cached downloads so experiment storage is separated from the root filesystem where practical.

## GPU status at capture

`nvidia-smi` reported:

- no running GPU processes;
- GPU memory accounting not supported through the desktop-style `nvidia-smi` presentation on this integrated Orin device.

Therefore ACP resource logging should rely on Jetson-native telemetry such as `tegrastats` for RAM/GPU/thermal/power observations rather than assuming discrete-GPU VRAM telemetry is available.

## Qualification interpretation

The platform is suitable for proceeding to a controlled inference-runtime qualification step, with two important constraints:

1. memory, not storage, is the primary resource constraint;
2. context length, KV-cache size, and model quantization must be treated as experimental resource variables because long-context ACP work can consume substantial shared memory even when model weights themselves fit.

## Runtime-selection principle

For initial ACP qualification, prefer a direct, headless inference runtime with:

- explicit model/checkpoint identity;
- explicit context-size control;
- reproducible command-line generation settings;
- no hidden persistent memory, retrieval, or agent state;
- process-level restart semantics;
- raw prompt/output logging;
- CUDA acceleration on the Orin stack where supported.

A higher-level UI or agent framework should not be the first experimental runtime because it would introduce additional state-management variables before baseline behavior is established.

## Model-selection gate

Do not select the final pilot checkpoint only by parameter count.

A candidate model qualifies only if it can:

1. load without sustained swap thrashing;
2. retain enough RAM headroom for KV cache and logging;
3. complete the fresh-context ACP corpus coherently;
4. sustain the intended accumulated-context run without OOM or hidden truncation;
5. expose exact tokenizer/context accounting;
6. survive repeated start/stop cycles with deterministic reset semantics.

For the first runtime qualification, begin with a small instruct model in a 4-bit-class quantization and scale upward only if fresh-context performance is inadequate and measured headroom permits it.

## Required next measurements

Before freezing ACP-PILOT-001 on this device, capture:

- `tegrastats` idle baseline for at least 60 seconds;
- CPU/GPU clocks and temperatures under one short inference load;
- exact runtime build/version;
- exact checkpoint and file hash;
- tokenizer identity;
- context length;
- prompt-processing and generation throughput;
- peak RAM during model load;
- peak RAM during a short generation;
- swap delta during the run;
- process-level reset/restart result;
- one fresh-context ACP item response.

## Qualification state

**ORIN-QUAL-001 passes hardware discovery.**

It does **not** yet qualify a model/runtime pair for ACP-PILOT-001. That requires the next runtime/model qualification step.