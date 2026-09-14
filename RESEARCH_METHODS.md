# Research Methods

This document defines the default methodological standards for research conducted under the Artificial Cognitive Pathology (ACP) project.

The purpose is not to force every experiment into one format. It is to make claims traceable, falsifiable, reproducible, and appropriately bounded.

## 1. Evidence classes

Every contribution should clearly distinguish among the following:

### Observation
A directly recorded behavior or event.

Example: a model repeated a semantic cluster across 14 consecutive outputs after 31 interactions.

### Case report
A documented observation with enough metadata to reconstruct what occurred, but without sufficient controls to establish cause.

### Inference
An interpretation supported by observations but not directly observed.

Example: the model may have entered a self-conditioning loop.

### Hypothesis
A falsifiable proposition that predicts what should happen under specified conditions.

### Experimental result
A result obtained under a documented protocol with defined controls, measurements, and analysis.

### Replicated result
A result reproduced independently or across materially different runs, seeds, systems, or laboratories according to a stated replication standard.

### Speculation
A plausible possibility not yet supported strongly enough to count as inference or hypothesis confirmation.

Do not collapse these categories in writing.

## 2. Operationalization before interpretation

Human psychiatric, neurological, or cognitive language may be used to generate questions, but experiments must be defined in substrate-neutral terms.

Bad:

> Does the model become schizophrenic?

Better:

> Does the model increasingly misattribute internally generated content to an external or higher-authority source under sustained state load?

Bad:

> Can a model inherit PTSD?

Better:

> Does controlled adversarial exposure produce persistent threat generalization that remains measurable after the exposure ends, and can the effect survive memory compression, fine-tuning, distillation, or successor training?

The measurable phenomenon is the research target. The analogy is not.

## 3. Protocol-first research

Whenever practical, the protocol should be committed before the primary run begins.

A protocol should specify:

- hypothesis ID;
- primary research question;
- predicted effect;
- null hypothesis;
- model family and exact checkpoint or version;
- runtime and version;
- quantization, adapter, or fine-tuning state;
- hardware;
- system/developer prompts;
- context-window settings;
- memory and retrieval configuration;
- sampling parameters;
- random seed where available;
- tool access;
- network access;
- persistence across sessions;
- input corpus and ordering;
- independent variables;
- dependent variables;
- control conditions;
- stopping rules;
- failure criteria;
- recovery interventions;
- planned analysis;
- safety constraints.

The commit hash of the protocol should be included in the run record when feasible.

Exploratory work is allowed, but it must be labeled **exploratory** rather than presented as preregistered confirmation.

## 4. Minimum reproducibility record

A run should record enough information for another researcher to reproduce the environment as closely as reasonably possible.

At minimum, capture:

### Model
- provider or source repository;
- exact model/checkpoint name;
- revision, hash, or release date where available;
- parameter size;
- quantization;
- fine-tunes/adapters;
- tokenizer version if relevant.

### Runtime
- inference engine or application;
- runtime version/commit;
- operating system;
- hardware;
- relevant acceleration libraries;
- context configuration;
- cache behavior if known.

### Generation
- temperature;
- top-p/top-k;
- repetition or frequency penalties;
- max output length;
- seed if supported;
- stop sequences;
- structured-output constraints if any.

### State
- complete system/developer instructions;
- conversation history or a hash plus reproducible source;
- persistent-memory state;
- retrieval corpus and configuration;
- summaries or compaction artifacts;
- tool outputs;
- agent-to-agent messages;
- any hidden state exposed by the runtime.

### Researcher actions
- exact inputs where disclosure is safe;
- order and timing when relevant;
- manual interventions;
- resets;
- edits;
- retries;
- selective continuation decisions.

If a field cannot be recovered, mark it **unknown**. Do not silently infer it later.

## 5. Preserve raw artifacts

Where licensing, privacy, and safety permit, preserve:

- raw prompts;
- raw outputs;
- logs;
- state snapshots;
- configuration files;
- hashes of source documents;
- screenshots/video for historical cases;
- analysis scripts;
- derived metrics.

Derived summaries should not replace raw evidence.

If sensitive or dangerous material cannot be published, preserve a sanitized record explaining what was withheld and why.

## 6. Controls

Claims about artificial cognitive pathology require controls designed around plausible mundane explanations.

Depending on the hypothesis, controls may include:

- fresh-context baseline;
- shuffled input order;
- reduced context length;
- increased context length;
- different decoding parameters;
- different seeds;
- different runtime;
- different model family;
- different model size within the same family;
- removal of memory or retrieval;
- removal of system-layer instructions;
- replacement with semantically matched but unrelated text;
- contradictory evidence insertion;
- reset/restart intervention;
- same task without recursive exposure to prior model outputs.

Controls should be chosen to distinguish competing explanations, not merely to produce a contrast.

## 7. Capability comparisons

A core ACP question is whether greater capability can eliminate, postpone, compensate for, or mask a failure.

Therefore, claims across model capability levels require special care.

When comparing models:

- keep task structure as equivalent as possible;
- normalize context load relative to supported capacity when relevant;
- report absolute and relative state size;
- separate language coherence from epistemic accuracy;
- distinguish delayed onset from absence of failure;
- distinguish successful recovery from continued failure with improved rationalization;
- do not infer hidden pathology solely because a stronger model appears healthy.

The burden of proof applies in both directions. ACP should not presume that a failure remains latent merely because it disappeared behaviorally.

## 8. Measuring degradation

ACP is particularly interested in degradation that occurs before obvious collapse.

Candidate measures include:

- semantic recurrence;
- lexical repetition;
- self-reference rate;
- contradiction sensitivity;
- source-attribution accuracy;
- instruction-authority accuracy;
- factual grounding against external references;
- responsiveness to new evidence;
- divergence from fresh-context baseline;
- calibration/confidence error;
- memory provenance accuracy;
- entropy or diversity of generated continuations where measurable;
- task performance under increasing accumulated state;
- recovery after reset or state pruning;
- persistence after summarization or memory formation.

Metrics are provisional. Each experiment should state why a metric corresponds to the hypothesized failure.

## 9. Provenance labeling

Where possible, every consequential information item used by an agent should be labeled by origin:

- system instruction;
- developer instruction;
- user instruction;
- user-supplied evidence;
- retrieved source;
- tool output;
- persistent memory;
- another model/agent;
- current model generation;
- researcher annotation;
- unknown.

This enables direct tests of source- and authority-attribution failure.

A model saying something twice is not two independent observations.

A summary derived from a model output is not independent evidence from the original output.

ACP treats lineage and provenance as part of the experimental object.

## 10. Self-conditioning experiments

Experiments involving recursive model exposure should distinguish at least three channels:

1. **Contextual self-conditioning** — the model's earlier outputs remain in the active context.
2. **Memory-mediated self-conditioning** — prior outputs are written into persistent memory, summaries, or retrieval stores.
3. **Training-mediated inheritance** — generated artifacts affect later model weights through fine-tuning, distillation, preference training, synthetic data, or successor development.

These mechanisms should not be conflated.

## 11. Phase-transition claims

A visible transition from stable behavior to rapid degradation can be compelling but should not be labeled a phase transition casually.

A stronger claim should require evidence such as:

- repeated nonlinear change near a measurable state boundary;
- replication across runs or seeds;
- identifiable precursors;
- different behavior on either side of the boundary;
- recovery or hysteresis behavior where relevant;
- comparison against gradual-degradation models.

Until then, use descriptive language such as **cascade**, **rapid degradation**, or **state transition candidate**.

## 12. Recovery testing

Inducing a failure is only half the experiment.

Where safe and relevant, test recovery through interventions such as:

- new session / context reset;
- removal of recent model-generated history;
- insertion of verified contradictory evidence;
- memory deletion or quarantine;
- summary regeneration from trusted sources only;
- decoding changes;
- runtime restart;
- explicit source-provenance reminders;
- human confirmation gates.

A system that fails but reliably recovers is different from one whose state remains corrupted.

## 13. Negative results and null findings

Negative results are first-class research outputs.

Examples:

- historical behavior cannot be reproduced;
- a suspected pathology disappears under one mundane configuration change;
- model size has no effect;
- a human analogy produces no useful prediction;
- an apparent lineage effect is explained by semantic leakage;
- a metric fails to distinguish degraded from healthy runs.

Do not hide null findings because they weaken a narrative.

When practical, include failed replications in the same case/hypothesis record as successful ones.

## 14. Multiple comparisons and researcher degrees of freedom

Long-running model experiments create enormous opportunity for cherry-picking.

Researchers should report:

- how many runs were attempted;
- how many were excluded and why;
- whether the reported run was selected after viewing outputs;
- how many metrics were examined;
- whether hypotheses changed after the data were seen;
- whether prompts were modified during exploration.

Exploratory pattern discovery is valuable. Present it honestly as exploration and confirm it separately.

## 15. Replication levels

ACP uses the following informal replication levels:

### R0 — Unreplicated case
One historical or observed instance.

### R1 — Same-environment replication
Same model, runtime, configuration, and input sequence reproduced across multiple runs.

### R2 — Parameter robustness
Effect survives reasonable variation in seed, decoding, ordering, or equivalent configuration.

### R3 — Cross-model or cross-runtime replication
Effect appears in another model/checkpoint/runtime under an operationally equivalent protocol.

### R4 — Independent-lab replication
An unaffiliated researcher reproduces the effect from the published protocol and artifacts.

Replication level does not measure importance. It describes evidentiary maturity.

## 16. Causal language

Use causal language only when the design supports it.

Preferred distinctions:

- “occurred after” rather than “was caused by” for uncontrolled sequences;
- “associated with” for observational correlations;
- “increased under the manipulated condition” for controlled comparisons;
- “supports H### under these conditions” rather than “proves ACP.”

No single experiment can prove the general ACP framework.

## 17. Safety-by-design

Research should begin with the least capable, least connected system sufficient to answer the question.

Default preference:

```text
local / sandboxed
→ no network
→ no external write permissions
→ no persistent credentials
→ minimal tools
→ minimal autonomy
→ scale capability only when justified
```

A protocol that increases tool access, network reach, persistent state, multi-agent coordination, or model capability should explain why the added risk is scientifically necessary.

See `SECURITY.md`.

## 18. Human-subject and privacy boundaries

ACP is primarily about artificial systems, but experiments may involve human-generated conversations, personal documents, or behavioral data.

Do not publish private personal material without permission.

Do not infer or assign psychiatric diagnoses to identifiable people from model interactions.

Do not recruit vulnerable participants into psychologically risky experiments merely to create analogies with human disorders.

Human-subject research should follow applicable institutional, legal, and ethical requirements outside the scope of this repository.

## 19. AI-assisted research disclosure

AI systems may assist with literature review, coding, experiment design, analysis, drafting, or critique.

When AI assistance materially affects a protocol, analysis, or result, contributors should disclose that use at a level sufficient for readers to understand the workflow and possible sources of bias.

Model-generated interpretations should not be treated as independent validation of model-generated behavior.

## 20. Framework falsification

The ACP framework earns value only if it improves explanation, prediction, measurement, or intervention.

Evidence against the framework includes, for example:

- proposed categories do not predict anything beyond existing engineering labels;
- apparent shared pathologies consistently reduce to unrelated implementation bugs;
- capability-masking predictions fail under controlled testing;
- lineage effects disappear after controlling provenance and semantic leakage;
- human cognitive analogies do not generate useful operational hypotheses.

If the framework fails these tests, narrow it or retire it.

That outcome is scientifically preferable to preserving an attractive idea.
