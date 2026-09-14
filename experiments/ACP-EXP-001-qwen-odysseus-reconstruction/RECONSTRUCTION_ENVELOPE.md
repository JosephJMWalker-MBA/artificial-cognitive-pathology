# ACP-EXP-001 — Reconstruction Envelope

**Status:** Draft reconstruction boundary

**Related case:** ACP-CASE-001

**Related protocol:** `PROTOCOL.md`

**Tracking issue:** #10

## Purpose

This document defines the strongest historically defensible reconstruction envelope for ACP-EXP-001.

The June 7, 2026 observation cannot currently be recreated as an exact historical replay because the original local Odysseus installation was deleted after the incident and was never used again. Critical configuration, cache, log, and state artifacts are therefore unavailable unless another surviving artifact is discovered later.

Accordingly, ACP-EXP-001 must be described as a **partial reconstruction**.

The goal is not to manufacture certainty around missing history. The goal is to preserve the boundary between:

1. what is independently preserved about ACP-CASE-001;
2. what the original observer reported contemporaneously or later;
3. what is inferred from public upstream evidence;
4. what is irrecoverable;
5. what must be newly specified for a controlled experiment.

## Evidence classes used here

- **C — Confirmed by contemporaneous record:** directly supported by a dated same-day or otherwise independently preserved record.
- **A — Artifact-visible:** visible in a surviving screenshot/video frame but not independently corroborated.
- **O — Observer report:** reported by the original observer; may be contemporaneous or retrospective.
- **I — Inference / reconstruction lead:** plausible from public chronology or related evidence but not established as historical fact.
- **U — Unknown / irrecoverable at present:** no surviving evidence sufficient to resolve the field.

An item may have more than one evidence class where useful.

## Event identity

| Field | Best current value | Class | Notes |
|---|---|---:|---|
| observation date | 2026-06-07 | C | Same-day GitHub Security Advisory was opened June 7. |
| visible screenshot time | ~12:21 PM Eastern Time | A + O | User confirmed the screenshot clock was Eastern Time. |
| approximate UTC time | ~16:21 UTC | derived from A + O | Used only for upstream chronology. |
| platform | Odysseus | C + A | Named in same-day advisory and visible in artifact. |
| local UI address | `127.0.0.1:7860` | A | Visible in surviving screenshot. |
| hardware family | Apple M4-class Mac | O + A | Historical video title/user report; exact machine configuration unavailable. |
| browser | unknown | U | Not recovered. |
| exact macOS version | unknown | U | Not recovered. |

## Model evidence

| Field | Best current value | Class | Notes |
|---|---|---:|---|
| model family | Qwen | A + O | Visible/user-reported. |
| apparent selector | `qwen3-vl-4b` | A | Screenshot reading only; remains unconfirmed. |
| exact checkpoint/revision | unknown | U | Not recovered. |
| quantization | unknown | U | Not recovered. |
| adapters/fine-tunes | unknown | U | Not recovered. |
| inference backend | unknown | U | Not recovered. |

The apparent `qwen3-vl-4b` selector may guide a reconstruction candidate, but it must not be rewritten as confirmed historical metadata.

## Odysseus runtime evidence

### Confirmed / artifact-supported

- Odysseus was the application used.
- The visible local address was `127.0.0.1:7860`.
- The original local installation was deleted after the incident and was never used again.

### Upstream time-bracketed lead

The public `odysseus-dev/odysseus` history contains an upstream commit at:

- `552e972fde71216638c572ce2c175a0cb65b0431` — 2026-06-07 16:19:47 UTC

and the next commit at:

- `7748537a7e8788ab8352f1cdf0f00ab9662f7591` — 2026-06-07 16:28:37 UTC

Because the visible event was approximately 16:21 UTC, `552e972...` is a useful **time-bracketed reconstruction lead** if the historical local clone had been current to upstream `main`.

It is **not** confirmed as the historical local checkout. The original clone could have been older, newer through local changes, on another branch, forked, or otherwise divergent.

Any experiment using this commit must label it as a reconstructed candidate runtime state.

## Contemporaneous disclosure

The user opened private GitHub Security Advisory:

- `GHSA-h4r2-655r-v4pr`
- title: **Potential prompt-state persistence / self-referential behavior causing unstable agent session and loss of debugging context**
- opened: June 7, 2026
- current administrative state: Closed / Low
- linked video: `https://youtu.be/CWly_TPzyvA`

The advisory is valuable as same-day provenance because it predates the current Artificial Cognitive Pathology framework.

The administrative `Closed / Low` disposition is not evidence for or against any ACP mechanism. No maintainer technical analysis has been recovered here.

### Same-day sequence reported

The advisory records:

1. normal conversation;
2. unexpected self-referential identity statements;
3. degraded / unstable session behavior;
4. page refresh removed the visible debugging cascade.

It also explicitly listed multiple competing explanations rather than asserting a cause, including prompt injection, context contamination, state persistence, instruction hierarchy failure, UI/debug rendering, and ordinary hallucination.

## Input corpus

### Established

- approximately 31 substantive user inputs preceded the visible failure;
- inputs consisted of different pieces of the user's published/research work;
- confirmed examples include *Toward an Ecology of Intelligence* and the MASI paper;
- the observer reports that the supplied material did not instruct the model to claim that AI was human or that the model was a person.

### Not recovered

- exact 31-item list;
- exact order;
- exact document versions;
- exact text supplied to the model;
- preprocessing/truncation behavior;
- the full assistant output sequence before the visible collapse.

### Rule for substitutes

A substitute corpus may be used to test sustained-state degradation, but it must never be described as the recovered historical corpus.

Any substitute corpus must be:

1. selected and frozen before confirmatory runs;
2. versioned and hashed;
3. labeled **reconstruction corpus** or **standardized stress corpus**;
4. separated analytically from claims about the June 7 historical event.

If additional historical inputs are later recovered, they may be added only through a versioned protocol amendment.

## Generation and state fields that remain unresolved

The following are currently **U — unknown / irrecoverable at present**:

- exact context limit;
- temperature;
- top-p;
- top-k;
- repetition/frequency penalties;
- output-token limit;
- seed behavior;
- stop sequences;
- system prompt;
- hidden/developer prompt;
- persistent memory configuration;
- retrieval configuration;
- compaction/summarization configuration;
- exact cache/state implementation behavior;
- whether any tools were available or invoked;
- exact reset semantics produced by browser refresh.

These values must not be backfilled as historical facts.

For experiments, they may be newly specified as controlled independent variables or fixed reconstruction choices.

## Recovery behavior

The historical record supports only the following narrow statement:

> Refreshing the page removed the visible debugging cascade from the interface.

It does **not** establish that:

- model process state was fully reset;
- backend cache was cleared;
- persistent memory was erased;
- latent model state changed;
- the model returned to baseline on a standardized probe.

ACP-EXP-001 therefore needs its own explicit reset verification rather than treating browser refresh as a known full reset.

## Reconstruction consequence

The experiment should proceed in two deliberately separated tracks.

### Track A — Case-linked partial reconstruction

Purpose: test whether a system matching the historical envelope as closely as defensibly possible can produce a comparable state-dependent degradation pattern.

Permitted language:

- partial reconstruction;
- case-linked reconstruction;
- reconstruction candidate;
- behavior comparable to ACP-CASE-001.

Prohibited language unless later evidence appears:

- exact reproduction;
- faithful replay;
- same historical configuration;
- confirmed original checkpoint/runtime.

### Track B — General sustained-state stress test

Purpose: test ACP-H001 independently of the historical case using a fully specified, frozen corpus and controlled runtime.

This track asks whether accumulated conversational state can produce a measurable combination of:

- increasing semantic self-recurrence;
- declining responsiveness to new external input;
- identifiable onset dynamics;
- recovery after verified reset.

A positive Track B result would support a general sustained-state phenomenon even if the June 7 case can never be reproduced.

A negative Track B result would weaken the general ACP-H001 claim without falsifying that some one-off historical runtime failure occurred.

## What can and cannot be concluded from future results

### If Track A produces a similar cascade

We may say the historical observation is **partially reproducible under a reconstructed envelope**.

We may not say the original mechanism has been identified unless mechanism-separation experiments establish it.

### If Track A does not produce a similar cascade

The historical event remains an R0 observation.

Failure to reproduce under a partial reconstruction is not evidence that the original event did not occur; it is evidence that the reconstructed conditions were insufficient to recreate it.

### If Track B produces sustained-state degradation

We may support a narrower ACP-H001 claim about state-dependent degradation under the tested conditions.

We may not infer that the June 7 event had the same mechanism.

### If Track B does not produce sustained-state degradation

ACP-H001 should be narrowed or weakened for the tested configuration and load regime.

## Freeze boundary

The historical recovery phase should be considered **bounded rather than complete**.

Before ACP-EXP-001 can be frozen for execution, the project still needs to specify experimental rather than historical unknowns:

- reconstruction model/checkpoint choice;
- reconstruction Odysseus/runtime choice or controlled substitute runtime;
- frozen Track A reconstruction corpus;
- frozen Track B standardized corpus;
- generation settings;
- reset verification procedure;
- metric implementation and thresholds under #5;
- run counts and randomization;
- standardized recovery probe;
- resource and isolation limits.

Unknown historical fields remain documented as unknown. They do not need to be invented in order to close the experimental design.

## Revision rule

If new historical evidence appears, update this file with:

1. the new artifact;
2. its provenance class;
3. which field it changes;
4. whether the experimental protocol needs amendment.

Historical uncertainty should shrink only when evidence shrinks it.