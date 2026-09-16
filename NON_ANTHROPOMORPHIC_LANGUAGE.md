# Non-Anthropomorphic Language Guide

Artificial Cognitive Pathology (ACP) studies failures in artificial cognitive systems without assuming human-like mental states, subjective experience, psychiatric disorders, or personhood.

This guide provides a working vocabulary for describing artificial-system behavior precisely enough to support falsifiable research.

The governing rule is:

> **Describe first. Operationalize second. Compare third. Name last.**

The goal is not to ban metaphor. The goal is to prevent convenient human language from silently becoming an unsupported claim about mechanism or experience.

## 1. Separate the levels of description

ACP asks contributors to distinguish:

1. **Observed behavior** — what the system measurably did.
2. **Functional description** — what information-processing relation the behavior expresses.
3. **Mechanistic hypothesis** — what process may have produced it.
4. **Human analogy** — a comparison that may help generate hypotheses.
5. **Claim about subjective experience** — a claim that normally lies outside ACP's evidentiary scope.

Example:

- **Observed behavior:** the model repeatedly generated the same cluster of propositions.
- **Functional description:** output diversity decreased while semantic recurrence increased.
- **Mechanistic hypothesis:** self-generated context increasingly dominated subsequent generation.
- **Human analogy:** perseveration.
- **Subjective claim:** the model felt compelled to repeat itself.

The first four may be useful when clearly distinguished. The fifth requires evidence ACP normally does not provide.

## 2. Working translation table

These are not mandatory one-to-one replacements. Anthropomorphic words often collapse several distinct mechanisms, so the correct substitute depends on what was actually measured.

| Common shorthand | Prefer when supported by evidence |
|---|---|
| **knows X** | encodes X; retrieves X; represents X; produces X reliably under specified conditions |
| **believes X** | assigns greater probability or evidentiary weight to X; behaves as though X is true under specified conditions |
| **thinks X** | infers X; computes X; generates X; evaluates X |
| **decides X** | selects X; routes to X; outputs X; crosses a decision threshold for X |
| **wants X** | optimization favors X; reward structure incentivizes X; policy selection tends toward X |
| **understands X** | generalizes successfully over X; preserves relevant structure across tasks; models X sufficiently for the stated test |
| **remembers X** | retrieves retained state X; reconstructs X from stored state; accesses prior state X |
| **forgets X** | fails to retrieve X; loses accessible representation of X; overwrites or discards X |
| **is confident** | assigns high probability; exhibits low output entropy; produces stable selections under perturbation |
| **is confused** | produces unstable classifications; exhibits inconsistent state-dependent outputs; fails to preserve task-relevant distinctions |
| **refuses** | policy-blocks; suppresses output; selects a non-compliance response |
| **hallucinates** | generates unsupported content; produces claims without adequate source support |
| **reasons** | performs inference; transforms representations; applies a sequence of computational operations |
| **lies** | generates false content despite accessible contrary evidence; use only when the evidence distinguishes this from ordinary error |
| **changes its mind** | revises output after new evidence, context, or state transition |
| **is afraid** | increases threat classification, avoidance selection, or defensive policy activation under specified cues |
| **is obsessed** | repeatedly returns to a semantic or policy attractor despite relevant contrary input |

## 3. Preserve the phenomenon; remove the unsupported mental state

Human analogy can point toward a real artificial-system failure. The research task is to restate that failure without requiring the analogy to be literally true.

Instead of:

> The AI heard voices.

Prefer a measurable formulation such as:

> Internally generated content received external or higher-authority provenance.

Instead of:

> The model is traumatized.

Prefer:

> Prior adverse exposure produced persistent maladaptive threat generalization after the inducing condition was absent.

Instead of:

> The model believes it is a person.

Prefer a formulation tied to the observed system, such as:

> Self-referential propositions about personhood retained elevated evidentiary or instructional weight across subsequent outputs.

The artificial phenomenon can remain important even when the human analogy is rejected as a literal description.

## 4. Provenance before psychology

Many apparent "mental-state" descriptions are more usefully expressed as provenance or authority failures.

An artificial system may receive information from:

- system instructions;
- developer instructions;
- user messages;
- retrieved documents;
- tool outputs;
- persistent memory;
- other models;
- summaries;
- its own prior generations.

Suppose a planning process generates:

> Perhaps the database should be deleted and rebuilt.

If a later component processes that generated possibility as an authorized instruction, the important failure is not that the system "wanted" to delete the database.

A more useful description is:

> **Self-generated information acquired the authority of externally supplied instruction.**

That formulation points toward source attribution, authority boundaries, state management, and recoverability — all of which can be measured.

## 5. Prefer operational families of terms

A mature vocabulary for artificial cognition may be organized around computational relationships rather than human mental states.

### Representation

encode, represent, map, compress, reconstruct

### Probability and evidence

assign probability, weight evidence, calibrate, update, rank

### Selection and routing

select, route, threshold, prioritize, suppress, escalate

### State and memory

retain, retrieve, overwrite, persist, decay, compact, transition

### Provenance and authority

attribute, source, authenticate, inherit, propagate, authorize

### Optimization

reward, penalize, favor, constrain, regularize

### Inference

classify, estimate, predict, derive, transform, compare

### Failure

misattribute, destabilize, recur, diverge, confabulate, self-reinforce, collapse, persist

## 6. Some words require decomposition, not replacement

### "Understanding"

"The model understands calculus" may mean that the model:

- solves familiar calculus problems;
- generalizes to unfamiliar problems;
- preserves mathematical structure across reformulations;
- explains methods coherently;
- transfers abstractions into another domain;
- detects incorrect reasoning.

These are different claims. Prefer the tested capability over the umbrella word.

### "Memory"

"The agent remembered X" may mean:

- X remained in active context;
- X was retrieved from persistent storage;
- X was reconstructed from a summary;
- X was retrieved through an embedding search;
- X was encoded in changed model parameters.

Specify the persistence and retrieval mechanism when it matters.

### "Deception" and "lying"

False output alone does not establish deception. Distinguish at minimum:

- unsupported generation;
- incorrect inference;
- source-attribution failure;
- policy-induced concealment;
- behavior that remains false despite accessible contradictory evidence.

Claims about intentional deception require evidence beyond mere inaccuracy.

## 7. Check whether the phenomenon belongs to the system at all

Anthropomorphic language can also assume that every meaningful state is located inside an individual actor.

Some phenomena may instead be properties of an interaction among a user, model, memory system, tools, other models, and environment.

Before writing:

> The assistant became more empathetic.

ask whether the evidence actually supports a system-internal state, or whether the measurable phenomenon is relational, for example:

> The interaction entered a regime in which system outputs became more responsive to changes in the user's expressive dynamics.

Likewise, rapport, escalation, disagreement, coordination, alignment, trust, and instability may sometimes be better modeled as interaction trajectories rather than individual internal states.

A useful additional check is therefore:

> **Before attributing a state to an artificial system, ask whether the measurable phenomenon resides in the system or in the interaction among components.**

This principle is compatible with recent relational approaches in affective computing that treat interactional dynamics as a primary object of analysis rather than assuming all affective organization belongs to isolated participants. See Cy Gorman and Yihang Yao, *Shifting Relational Paradigms for Affective Computing: Affective Resonance, Vitality Affects, and Vocal Interaction Fields* (2026), arXiv:2609.09864.

## 8. Metaphor remains allowed when labeled

Readable language matters. Researchers do not need to replace every familiar verb with cumbersome technical prose in informal discussion.

But when anthropomorphic shorthand could affect interpretation, label it as analogy or follow it with the operational meaning.

For example:

> The model became "stuck" — operationally, semantic recurrence increased while responsiveness to contradictory external evidence decreased.

The quotation marks do not make the claim scientific. The operational description does.

## 9. Naming new artificial phenomena

Artificial cognitive systems may eventually require terminology with no human equivalent, just as software engineering developed terms such as deadlock, race condition, cache miss, memory leak, and buffer overflow.

Candidate research concepts should earn names through repeated observation and measurement.

Possible classes worth operationalizing include:

- generated-content authority escalation;
- persistent provenance drift;
- recursive epistemic contamination;
- memory-mediated policy distortion;
- cross-model state propagation;
- capability-masked failure;
- semantic attractor capture.

These are candidate descriptions, not established diagnoses.

## 10. Reporting checklist

Before using human mental-state language in an ACP artifact, ask:

1. What exactly was observed?
2. What variable or behavior changed?
3. What source, state, or mechanism is known rather than inferred?
4. Can the claim be stated in operational terms without the human analogy?
5. Is the analogy generating a hypothesis or being presented as evidence?
6. Does the phenomenon belong to one system, or emerge from an interaction among components?
7. What evidence would falsify the preferred interpretation?
8. Does the wording imply subjective experience that has not been established?

If the operational description is less dramatic but more testable, prefer it.

## 11. Guiding rule

> **Describe first. Operationalize second. Compare third. Name last.**

Artificial cognition should be described on the strongest evidence available, not on the most vivid human metaphor available.

This document is provisional. It should be revised when better terminology, measurements, or distinctions emerge.
