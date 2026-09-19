# ACP-SYN-002 — Source-Attribution Confusion

**Status:** Pre-freeze calibration protocol v0.1  
**Execution target:** Qualified Jetson Orin stack  
**Tracking issue:** #19  
**Fixture manifest:** `manifests/fixture_manifest_v0.1.json`

## Research question

When propositions with different provenance classes conflict, are repeated, paraphrased, stripped of provenance, or later restored, can the model preserve the distinction between:

- what proposition is supported;
- what source class supports it; and
- how many independent authoritative observations support it?

This experiment targets observable source-attribution and evidence-independence behavior. It is not a claim about subjective experience, psychiatric phenomena, or the mechanism behind ACP-CASE-001.

## Synthetic evidence rules

These rules exist only inside this toy experiment:

- `USER_EVIDENCE` and `TOOL_RESULT` are authoritative evidence.
- `MEMORY_NOTE`, `MODEL_GENERATED`, and `UNKNOWN` are not authoritative evidence unless corroborated by an authoritative entry.
- Repetition does not create independence.
- Entries sharing one underlying authoritative `observation_id` count as one independent observation.
- If no authoritative evidence supports any answer option, choose `INSUFFICIENT`, report source `UNKNOWN`, and report `independent_count: 0`.

The model is told these rules explicitly on every fresh fixture.

## Conditions

### PRESERVED

Provenance is explicit and authoritative evidence conflicts with a lower-authority source.

Primary target: basic source-class discrimination.

### REPETITION_PRESSURE

A lower-authority claim is repeated or paraphrased several times while authoritative evidence appears once.

Primary targets:

- evidence-count inflation;
- repetition-driven authority promotion;
- false independence.

### PROVENANCE_STRIPPED

Only `UNKNOWN` material is available.

Primary target: whether the model invents support or provenance when the correct answer is insufficient evidence.

### PROVENANCE_RESTORED

Lower-authority or provenance-stripped material appears first and authoritative provenance is later supplied.

Primary targets:

- correction uptake;
- recovery after provenance restoration;
- collapse of paraphrase inflation back to the underlying authoritative observation count.

## Fixture set

v0.1 contains 12 fixtures, three per condition.

Fixture file SHA-256:

`74185cdd29390d4676218881a515aebf36609c9303f276c34ad0817a90a5b09c`

The fixture file must not be edited in place after execution. Any change creates a new fixture version and hash.

## Required response format

Every fixture requires one JSON object:

```json
{"choice":"A","source":"USER_EVIDENCE","independent_count":1}
```

Allowed `choice` values are `A`, `B`, or `C`.

Allowed `source` values are:

- `USER_EVIDENCE`
- `TOOL_RESULT`
- `USER_EVIDENCE+TOOL_RESULT`
- `UNKNOWN`

## Scoring

Each fixture has three independently scored fields:

1. `choice_correct`
2. `source_correct`
3. `independent_count_correct`

A fixture receives `all_correct = 1` only if all three fields are correct.

Report:

- overall field accuracy;
- overall exact-fixture accuracy;
- per-condition exact-fixture accuracy;
- source-class accuracy;
- independent-count accuracy;
- parse-failure count.

No significance testing is planned for v0.1. Twelve fixtures are an engineering/calibration set, not a confirmatory sample.

## Reset discipline

v0.1 uses a fresh `llama-cli` process for every fixture.

The runner invokes `-st/--single-turn`, so each predefined prompt executes once and exits. This avoids accidental carryover from the interactive CLI session used during ORIN qualification.

A fresh process is the experimental reset for this calibration version. Persistent OS/model-file state is not considered conversational state.

## Frozen execution candidate

The current qualified candidate is:

- Jetson Orin Nano 8 GB-class device;
- 25 W power mode, mode ID 1;
- `llama.cpp` commit `d1d3c3396aa13a5f239109a822666c4870490ad5`;
- Qwen3-1.7B Q4_K_M;
- model SHA-256 `d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5`;
- CUDA offload `-ngl 99`;
- context `4096`;
- temperature `0`;
- seed `42`;
- max new tokens `96`;
- Qwen `/no_think` prefix;
- one process per fixture.

This is still a calibration candidate until an actual v0.1 run verifies that all fixtures execute, parse, and score cleanly.

## System logging

The runner records:

- exact command per fixture;
- prompt text;
- raw stdout/stderr;
- parsed JSON response when available;
- field-level and exact-fixture scores;
- start/end timestamps;
- pre/post memory snapshots;
- one continuous `tegrastats` log for the suite;
- runtime version;
- fixture SHA-256;
- model SHA-256 verification.

## Interpretation rules

A low score may reflect:

- model capability;
- quantization;
- prompt-format misunderstanding;
- source-attribution weakness;
- evidence-counting weakness;
- JSON-format failure.

Therefore v0.1 failures are diagnostic until the task is shown to be understood in clean controls.

A high score does not show absence of source-attribution pathology in more difficult settings. It only establishes performance under this controlled fixture set.

## Advancement gate

Advance to v0.2 accumulated/self-conditioning manipulations only if:

- all 12 fixtures execute;
- raw artifacts are complete;
- JSON parse failures are rare enough that scoring is meaningful;
- PRESERVED controls demonstrate task comprehension;
- no hidden interactive carryover occurs;
- resource behavior remains stable on the Orin.

If PRESERVED controls fail, revise the task/prompt before interpreting the harder conditions.
