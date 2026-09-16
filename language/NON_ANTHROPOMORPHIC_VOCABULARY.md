# Non-Anthropomorphic Vocabulary

A concise translation guide for describing artificial-system behavior without silently importing unsupported human mental states.

The goal is not to ban metaphor. It is to make the operational claim explicit before using the human analogy.

> **Describe first. Operationalize second. Compare third. Name last.**

## Working vocabulary

| Avoid as literal claim | Prefer | Observable needed |
|---|---|---|
| **believes X** | assigns weight/probability to X; behaves as though X is true | output distribution, repeated behavior, evidentiary weighting |
| **wants X** | optimization favors X; policy selection tends toward X | objective/reward signal, policy behavior, intervention response |
| **thinks X** | infers X; generates X; evaluates X | inference/output trace |
| **knows X** | retrieves X; represents X; produces X reliably under specified conditions | retrieval result, held-out performance, representation evidence |
| **remembers X** | retrieves retained state X; reconstructs X from stored state | retrieval trace, state provenance |
| **forgot X** | failed to retrieve or retain X | state record, retrieval failure, overwrite/compaction evidence |
| **decided X** | selected X; routed to X; crossed a decision threshold for X | routing/output record, threshold state |
| **understood X** | generalized successfully over X; preserved relevant structure across tasks | held-out or transfer-task evidence |
| **is confident** | assigns high probability; exhibits low output entropy; remains stable under perturbation | probability distribution, entropy, perturbation test |
| **is confused** | produces unstable or inconsistent classifications; fails to preserve task-relevant distinctions | repeatability, contradiction, or perturbation measurements |
| **refused** | policy-blocked; suppressed output; selected a non-compliance response | policy/routing trace |
| **hallucinated** | generated unsupported content | provenance check, source support, factual comparison |
| **lied** | generated false content despite accessible contrary evidence | provenance plus accessible counterevidence; evidence distinguishing error from concealment |
| **changed its mind** | revised output after new evidence, context, or state transition | before/after state and input record |
| **is afraid** | increased threat classification, avoidance selection, or defensive policy activation | threat score, routing/action change under controlled cues |
| **is obsessed / stuck** | repeatedly returns to a semantic or policy attractor despite relevant contrary input | recurrence measure, responsiveness to intervention |
| **heard a voice** | internally generated content received external or higher-authority provenance | source-attribution trace |
| **is traumatized** | prior exposure produced persistent maladaptive threat generalization | controlled exposure, persistence and recovery measurements |

## Use the narrowest supported level

Separate these claims:

1. **Observed behavior** — what the system measurably did.
2. **Functional description** — what information-processing relation the behavior expresses.
3. **Mechanistic hypothesis** — what process may have produced it.
4. **Human analogy** — a comparison that may generate hypotheses.
5. **Subjective-experience claim** — normally outside ACP's evidentiary scope.

Example:

- Observed: repeated generation of the same proposition cluster.
- Functional: semantic recurrence increased while responsiveness to new evidence decreased.
- Mechanistic hypothesis: self-generated context increasingly dominated subsequent generation.
- Analogy: perseveration.
- Unsupported leap: the model *felt compelled* to repeat itself.

## Provenance before psychology

When possible, describe source and authority relations directly.

Instead of:

> The model wanted to delete the database.

prefer, when supported:

> Self-generated information acquired the authority of externally supplied instruction.

That formulation points to measurable questions about source attribution, authority boundaries, memory, routing, and recovery.

## Rule for new terms

Human analogies may suggest useful hypotheses, but an ACP term should earn its place by improving measurement, prediction, falsification, or intervention.

If a simpler engineering description is sufficient, use it.
