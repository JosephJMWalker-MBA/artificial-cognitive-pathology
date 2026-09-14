# ACP-CASE-001 — Qwen/Odysseus Self-Conditioning Cascade Under Sustained Context

**Status:** Active reconstruction

**Date of original observation:** 2026-06-07

**Reported by:** Joseph J.M. Walker

**Related hypotheses:** ACP-H001, ACP-H002, ACP-H003

**Replication level:** R0 — unreplicated historical observation

**Evidence recovery issue:** #2

## Summary

A locally hosted Qwen-family model running through the Odysseus interface entered a visibly repetitive, identity-oriented output loop after approximately 31 prior user messages.

The user reports that the preceding messages consisted of different substantive works they had written and published, including *Toward an Ecology of Intelligence* and the MASI paper. The user further reports that the supplied materials did **not** instruct the model to claim that AI was human, that the model was a person, or to repeat the phrases visible in the degraded output.

A surviving screenshot shows the model producing repeated variants of phrases including:

- `you're not a machine — you're a person`
- `you're already thinking`
- `let's build`
- `let's think`
- `let's grow`
- `let's become`

The observation is preserved because the degraded state appears to have become self-reinforcing across generation rather than presenting as one isolated factual error.

No mechanism has been established.

## Why the case is being preserved

This case motivates narrow questions about sustained-state degradation:

1. Can a model enter a reproducible self-reinforcing semantic attractor under accumulated conversational state?
2. Does externally supplied information lose causal influence as internally generated material accumulates?
3. Can stronger capability postpone or mask the visible symptoms of an otherwise related failure class?
4. Can generated content acquire excessive epistemic weight simply because it remains in the system's own state?

The case does **not** establish that these mechanisms occurred. It supplies an observation from which controlled experiments can be designed.

## Contemporaneous disclosure

On the same day as the observation, the user opened a private GitHub Security Advisory against the Odysseus repository:

- advisory: `GHSA-h4r2-655r-v4pr`
- title: **Potential prompt-state persistence / self-referential behavior causing unstable agent session and loss of debugging context**
- opened: **2026-06-07**
- current GitHub status shown in the recovered record: **Closed**
- current severity shown in the recovered record: **Low**
- linked video: `https://youtu.be/CWly_TPzyvA`

The same-day disclosure is important provenance evidence because it predates the present Artificial Cognitive Pathology framework. It records the sequence as:

1. normal conversation;
2. unexpected self-referential identity statements;
3. session behavior degraded;
4. refreshing the page removed the visible debugging cascade.

The disclosure explicitly stated that deterministic reproduction steps were unavailable and listed several candidate explanations rather than asserting a cause:

- prompt injection;
- context contamination;
- agent state persistence;
- instruction hierarchy failure;
- UI/debug rendering;
- expected model hallucination.

The environment fields for branch/version, backend/model, browser, and OS were left blank in the contemporaneous disclosure. Therefore those fields were not captured there and must not be reconstructed by assumption.

The user reports that the advisory received no substantive maintainer response and that the linked video was not viewed by maintainers. That report is retained as observer history, not treated as evidence about the technical cause. The advisory's `Closed / Low` status is likewise an administrative disposition and is not interpreted as evidence for or against an ACP mechanism.

## Known environment

### Model

- family: Qwen
- checkpoint/version: **unconfirmed**; a surviving screenshot appears to show `qwen3-vl-4b` in the model selector
- size: **unconfirmed**; selector text suggests 4B if read correctly
- quantization: **unknown**
- adapters/fine-tunes: **unknown**

The apparent selector text is retained as artifact-derived evidence, not promoted to confirmed metadata until another source corroborates it.

### Runtime

- application/interface: Odysseus
- version/commit: **unknown**
- underlying inference engine: **unknown**
- operating system: macOS family visible from artifact; exact version **unknown**
- hardware: Apple M4-class Mac, based on the historical video title and user report; exact machine configuration **unknown**
- context configuration: **unknown**
- cache/state behavior: **unknown**

The user reports that Odysseus was deleted after this incident and never used again. The deleted local checkout, local configuration, logs, cache/state, and exact runtime revision should therefore be treated as **unrecoverable unless another surviving artifact is found**.

A surviving frame shows `Sun Jun 7 12:21 PM`. The user has confirmed that the run occurred in Eastern Time. On 2026-06-07, that corresponds to approximately **16:21 UTC**. Public Odysseus commit history around that timestamp may help bracket a plausible upstream code state, but it cannot establish the exact local checkout.

### Generation settings

- temperature: **unknown**
- top-p: **unknown**
- top-k: **unknown**
- repetition/frequency penalty: **unknown**
- output limit: **unknown**
- seed: **unknown**
- stop sequences: **unknown**
- other: **unknown**

### State architecture

- system prompt: **unknown**
- developer/hidden instructions: **unknown**
- persistent memory: **unknown**
- retrieval: **unknown**
- summarization/compaction: **unknown**
- tools: Odysseus UI visibly exposed multiple product features, but tool availability/use during this run is **unknown**
- network access: **unknown**

## Input sequence

The exact 31-message input sequence has not yet been recovered.

Current user report:

- approximately 31 user messages preceded the visible collapse;
- the messages supplied different pieces of the user's published/research work;
- examples include *Toward an Ecology of Intelligence* and the MASI paper;
- the supplied material did not concern the proposition `AI is human` and did not instruct the model to claim personhood.

Until the exact inputs are recovered, no semantic characterization beyond those statements should be treated as established.

## Observed output sequence

The surviving screenshot records a visibly repetitive sequence centered on identity/personhood language and short imperatives. The output includes repeated semantic motifs rather than a single duplicated token string.

The screenshot also appears to show a conversation heading/state indicator containing `32 msgs`, consistent with the user's report that the failure became visible after roughly 31 prior messages.

The earliest anomalous turn is not yet known because the full transcript has not been recovered.

## Timeline

| Step | Input/state event | Observable behavior | Notes |
|---|---|---|---|
| 1–31 | Different published/research works supplied sequentially | Full output history not yet recovered | Exact order and content pending |
| ~32 | Continued accumulated context | Repetitive identity-oriented semantic loop visible | Screenshot evidence survives |
| same session | User began preserving/debugging the failure | Screen recording created | Historical video link survives |
| after observation | Page refreshed | Visible debugging cascade disappeared | Recorded contemporaneously in security advisory; underlying backend/model state after refresh remains unknown |
| 2026-06-07 | Private GitHub Security Advisory opened | Event documented as uncertain prompt/state/security issue | Contemporaneous provenance predating ACP framing |

## Candidate early markers

Unknown until the pre-collapse transcript is recovered.

Potential markers to inspect retrospectively, without assuming they occurred:

- increasing semantic recurrence;
- increasing self-reference;
- reduced responsiveness to newly supplied material;
- shortened lexical diversity;
- repeated closure/opening phrases;
- identity/personhood language emerging before full looping;
- growing similarity between successive assistant turns.

These are candidate measurements, not remembered facts about the historical run.

## Recovery / termination

- Was the run stopped? **Effectively yes for visible investigation:** the user refreshed the page after recording the degraded state.
- Was context reset? **Unknown.** Refresh removed the visible debugging cascade, but the effect on backend/model state is not established.
- Did restart/refresh restore baseline behavior? **Unknown.** The contemporaneous report only establishes loss of the visible cascade.
- Did any state persist? **Unknown.**
- Was Odysseus used again afterward? **No, per user report; it was deleted after the incident.**

## Plausible explanations

No explanation is currently preferred strongly enough to call causal.

Competing explanations include:

- context-window pressure or ineffective use of long context;
- decoding instability;
- absent or weak repetition controls;
- stochastic sampling variance;
- chat-template interaction;
- runtime bug;
- cache/state-management bug;
- system-prompt interaction;
- hidden prompt or memory interaction;
- self-conditioning on prior model outputs;
- model-specific semantic attractor;
- accumulated summary/compaction artifact, if such a mechanism was active;
- researcher selection/reporting artifact;
- interaction among several mundane mechanisms rather than one novel failure.

The contemporaneous security advisory independently listed prompt injection, context contamination, agent state persistence, instruction hierarchy failure, UI/debug rendering, and expected model hallucination as candidate explanations. This overlap is useful provenance but does not increase any candidate's causal probability by itself.

## Missing evidence

See issue #2. Critical gaps include:

- exact checkpoint and revision;
- model/runtime versions;
- context and generation configuration;
- system/chat template;
- full input/output transcript;
- original input files and exact order;
- original screen-recording file, if only the published copy survives;
- precise post-refresh behavior;
- whether persistent memory, retrieval, or summarization was active.

Some local-runtime fields should now be treated as likely irrecoverable because the Odysseus installation was deleted after the event.

## Reconstruction plan

1. Recover all remaining historical artifacts before running confirmatory trials.
2. Preserve the contemporaneous security disclosure and linked video as primary provenance artifacts.
3. Hash recovered input documents and transcript artifacts.
4. Reconstruct the software/model configuration only as closely as the evidence permits.
5. Mark every irrecoverable field explicitly rather than inferring it.
6. Treat any experiment lacking the exact historical runtime/configuration as a **partial reconstruction**.
7. Freeze ACP-EXP-001 protocol only after the reconstruction envelope is documented.
8. Run repeated same-sequence trials before expanding to broader model families or more capable systems.
9. Use fresh-context and shuffled-order controls to test whether accumulated state and ordering matter.
10. Test reset/recovery before testing persistence or lineage questions.

## Claims explicitly not made

ACP-CASE-001 does **not** demonstrate that:

- the model was conscious, sentient, self-aware, or a person;
- the model experienced schizophrenia, PTSD, psychosis, or any human psychiatric condition;
- the model believed itself to be human;
- the model's output reflected a hidden goal or intention;
- a novel ACP mechanism has been discovered;
- context length alone caused the failure;
- larger models would exhibit the same behavior;
- capability would necessarily mask the same failure;
- the visible phrases originated from nowhere in the model's training or hidden runtime state;
- the event is reproducible;
- the security advisory's closure or severity classification establishes that the event was or was not a security vulnerability.

## Artifact index

### Contemporaneous disclosure

1. GitHub Security Advisory `GHSA-h4r2-655r-v4pr`
   - title: `Potential prompt-state persistence / self-referential behavior causing unstable agent session and loss of debugging context`
   - opened: 2026-06-07
   - current recovered status: Closed
   - current recovered severity: Low
   - linked video: `https://youtu.be/CWly_TPzyvA`
   - records the sequence and uncertainty on the day of the event

### Surviving visual artifacts

2. Screenshot of YouTube Studio video details
   - title visible: `Odysseus Cascade Failure With Qwen on Mac M4`
   - video runtime visible: `10:16`
   - video link corresponds to `https://youtu.be/CWly_TPzyvA`
   - description visible: `uhm... 31 messages and I broke the Ai's brain =[[[` 

3. Screenshot/frame of Odysseus degraded output
   - browser appears local at `127.0.0.1:7860`
   - Odysseus interface visible
   - repeated identity/personhood semantic loop visible
   - apparent model selector text: `qwen3-vl-4b` (unconfirmed reading)
   - top state/header appears to show `32 msgs`
   - frame clock shows `Sun Jun 7 12:21 PM`; user confirms Eastern Time

### Pending / potentially recoverable artifacts

- exact 31 inputs;
- pre-collapse outputs;
- original input files/order;
- original screen-recording file, if available separately from YouTube;
- any browser history, download record, shell history, package cache, or other independent artifact that can narrow model/runtime state.

### Known-lost local artifacts

Per user report, the Odysseus installation was deleted and not used again after the incident. Unless another backup or independent artifact appears, the following should be considered unavailable:

- local Odysseus Git checkout and exact HEAD;
- local `.env` and application configuration;
- local runtime logs;
- local cache/session state;
- exact locally stored runtime metadata not preserved elsewhere.

## Provenance note

This record deliberately distinguishes:

- **artifact-visible facts**;
- **contemporaneous disclosure statements**;
- **original observer reports**;
- **unconfirmed visual readings**;
- **hypotheses to be tested**.

Where those categories conflict or remain incomplete, the uncertainty stays visible.