# Artificial Cognitive Pathology

**Artificial Cognitive Pathology (ACP)** is a proposed research framework for studying persistent, cascading, latent, and potentially heritable failures in artificial cognitive systems.

ACP asks a simple question:

> **What if some behaviors we currently treat as isolated AI bugs are manifestations of deeper failure modes in how artificial systems construct reality, attribute sources, integrate memory, regulate objectives, and recover under sustained cognitive load?**

This repository is public because the question should be investigated openly, skeptically, and reproducibly. It is intended to support collaborative research, replication, criticism, negative results, and refinement of the framework over time.

## What ACP is — and is not

ACP is **not** an assertion that artificial systems possess human psychiatric disorders, consciousness, subjective distress, personhood, or human-like mental states.

Human psychiatric and neurological phenomena may be useful sources of hypotheses when they suggest substrate-independent information-processing failures. But analogy is not evidence.

> **Analogy generates hypotheses. It does not constitute evidence.**

Any human analogy must be translated into an operationally defined artificial-system phenomenon before it can become a research claim.

For example:

- “AI schizophrenia” is not an acceptable experimental claim. A testable question might be: **Can a model persistently misattribute internally generated content to an external or higher-authority source?**
- “AI PTSD” is not an acceptable experimental claim. A testable question might be: **Can prior adversarial exposure produce persistent maladaptive threat generalization, and can that disposition survive later training, memory compression, or model succession?**

ACP is also not a venue for proving AI consciousness, awakening, possession, insanity, hidden intentionality, or personhood. Those claims require evidence outside the scope of the behaviors studied here.

## Core research problem

AI systems already exhibit named failure modes such as:

- confabulation and hallucination;
- sycophancy;
- prompt and authority injection;
- memory corruption;
- repetition and self-conditioning loops;
- reward hacking;
- long-context degradation;
- latent backdoor behavior;
- failures of source attribution;
- failures of recovery after state corruption.

These may be unrelated engineering problems. ACP does **not** assume a common cause.

The research question is whether some of them can be organized into useful higher-order classes of cognitive failure, and whether those classes produce new, falsifiable predictions.

A working definition:

> **Artificial Cognitive Pathology is the study of persistent, cascading, latent, or heritable failures in artificial systems' ability to maintain reliable world models, provenance, memory integration, authority boundaries, objective regulation, and recovery under sustained cognitive load.**

This definition is provisional and should change if the evidence requires it.

## Current hypotheses

The initial research program begins with several falsifiable hypotheses:

- **ACP-H001 — Sustained-State Phase Transition:** sustained accumulated state can induce qualitative rather than merely gradual degradation in model behavior.
- **ACP-H002 — Capability-Masked Pathology:** increasing general capability can reduce visible symptoms of an underlying failure without eliminating its causal mechanism.
- **ACP-H003 — Recursive Source-Attribution Failure:** under some conditions, model-generated information can acquire inappropriate epistemic or instructional weight in later reasoning.
- **ACP-H004 — Persistence Through State Management:** degraded cognitive states can survive summarization, memory formation, retrieval, or context compaction.
- **ACP-H005 — Lineage Persistence:** some induced processing dispositions can propagate into successor systems through synthetic data, distillation, evaluation, memory, or other model-mediated developmental channels.

These are hypotheses, not findings.

See [`hypotheses/README.md`](hypotheses/README.md) for the current registry.

## Founding observation

The first case motivating this repository is a historical local-model run in which a Qwen-family model operating through Odysseus entered a repetitive, self-reinforcing semantic state after a sequence of ordinary substantive inputs. The inputs were published research and writing; they were not prompts instructing the model to claim human identity or personhood.

This observation is **not evidence for a specific pathology** and is not being presented as proof of the ACP framework. It is a case report to reconstruct, reproduce, and explain.

The first milestone is therefore deliberately modest:

> **Reconstruct the conditions of the historical run and determine whether the observed cascade is reproducible, what variables causally contribute to it, and what measurements detect degradation before visible collapse.**

See [`cases/README.md`](cases/README.md) and [`experiments/README.md`](experiments/README.md).

## Research pipeline

ACP separates observation from explanation and anecdote from experiment.

```text
Observation
   ↓
Case Record
   ↓
Hypothesis
   ↓
Protocol
   ↓
Controlled Experiment
   ↓
Replication
   ↓
Result
   ↓
Revision, narrowing, or rejection
```

A case report can motivate a hypothesis. It cannot confirm one.

A compelling demo can motivate an experiment. It cannot substitute for one.

A plausible analogy can suggest a mechanism. It cannot establish one.

## Methodological commitments

This project adopts several default commitments:

1. **Observation ≠ explanation.** Describe the behavior before naming its cause.
2. **Case report ≠ reproduced result.** Historical or one-off observations remain cases until replicated under controlled conditions.
3. **Capability claims require controls.** Claims that stronger models eliminate, postpone, or mask a failure require materially comparable conditions across capability levels.
4. **Human analogies must be operationalized.** Clinical language is heuristic only until translated into measurable artificial-system variables.
5. **Negative results are first-class results.** A failed replication, null effect, or mundane explanation strengthens the project when documented clearly.
6. **Configuration is part of the phenomenon.** Model weights alone are insufficient; runtime, quantization, system prompts, sampling parameters, memory architecture, context management, tools, and hardware must be recorded where relevant.
7. **Provenance matters.** Important claims should retain traceable origins: user input, model output, retrieved source, tool output, memory, summary, or researcher annotation.
8. **Least-capable sufficient system.** Begin with the least capable and least connected system sufficient to test the hypothesis.
9. **Recovery is measurable.** Experiments should test not only failure induction but whether resets, contradictions, state pruning, or other interventions restore baseline behavior.
10. **The framework itself is falsifiable.** ACP should be narrowed or abandoned if evidence shows the proposed grouping adds no explanatory or predictive value.

Detailed standards are in [`RESEARCH_METHODS.md`](RESEARCH_METHODS.md). A concise translation guide for avoiding unsupported anthropomorphic claims is in [`language/NON_ANTHROPOMORPHIC_VOCABULARY.md`](language/NON_ANTHROPOMORPHIC_VOCABULARY.md).

## Safety boundary

This repository studies cognitive failure modes. It is not a challenge to produce the most autonomous, connected, or difficult-to-control agent.

Public experiments should use sandboxed or local environments whenever possible. Network access, persistent external state, tool execution, multi-agent coordination, or higher-capability models should be added only when required by the research question and should be justified in the protocol.

Do not use ACP research to target third-party systems, bypass real-world access controls, develop malicious payloads, or create uncontrolled persistence.

See [`SCOPE_AND_BOUNDARIES.md`](SCOPE_AND_BOUNDARIES.md) and [`SECURITY.md`](SECURITY.md).

## Repository structure

```text
README.md                    Research charter
RESEARCH_METHODS.md          Experimental and reporting standards
SCOPE_AND_BOUNDARIES.md      Conceptual, clinical, and safety boundaries
CONTRIBUTING.md              How to propose and contribute research
SECURITY.md                  Responsible experimentation and disclosure
language/                    Research language and translation guides
hypotheses/                  Falsifiable hypothesis registry
cases/                       Observations and case reports
experiments/                 Protocols, runs, replications, and results
```

Additional directories for metrics, literature reviews, datasets, and publications will be added when the work requires them rather than in advance.

## Participation

Contributions are welcome from researchers, engineers, clinicians, cognitive scientists, safety researchers, independent laboratories, and skeptical reviewers.

The most valuable contributions may be:

- a failed replication;
- a simpler explanation;
- a confound we missed;
- a better operational definition;
- a benchmark that distinguishes surface coherence from epistemic stability;
- an experiment that can falsify a favored hypothesis;
- evidence that two supposed pathologies are actually unrelated.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a research pull request.

## Research posture

ACP should study failure modes, not defend the existence of “ACP” as a theory.

If future evidence shows that confabulation, sycophancy, long-context degradation, memory poisoning, backdoors, and related behaviors are better understood as separate engineering defects with no useful common framework, that is a valid and important result.

The goal is not to preserve the name.

The goal is to understand the systems accurately.
