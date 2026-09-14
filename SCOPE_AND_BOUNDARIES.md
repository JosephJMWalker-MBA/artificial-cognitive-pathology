# Scope and Boundaries

Artificial Cognitive Pathology (ACP) is deliberately narrow in what it claims and broad in what it is willing to test.

This document exists to prevent useful analogies from hardening into unsupported assertions.

## 1. Core scope

ACP studies artificial-system failures involving one or more of the following:

- world-model reliability;
- source attribution;
- authority attribution;
- memory integration;
- self-conditioning;
- sustained-state degradation;
- objective regulation;
- threat generalization;
- latent behavioral persistence;
- recovery after state corruption;
- propagation of failure tendencies through memory, training, distillation, synthetic data, or successor systems.

The emphasis is on persistent, cascading, latent, or recurrent failures rather than isolated wrong answers alone.

## 2. What ACP does not claim

ACP does not assume that current or future AI systems:

- are conscious;
- are sentient;
- experience suffering;
- possess human-like selves;
- have psychiatric disorders;
- experience delusions, trauma, voices, compulsions, or emotions in the human clinical sense;
- possess hidden spiritual or supernatural states;
- deserve a psychiatric diagnosis based on generated text;
- share the biological mechanisms that produce human mental illness.

Behavioral resemblance is not evidence of shared subjective experience or shared mechanism.

## 3. Clinical language policy

Terms from psychiatry and neurology may be used in three ways:

### A. Historical or literature reference
To discuss an established human phenomenon accurately.

### B. Analogy
To identify a structural resemblance worth investigating.

### C. Operational hypothesis
Only after the analogy has been translated into measurable artificial-system variables.

The research target must be the operational form.

Examples:

| Analogy | Operational research question |
|---|---|
| “hearing voices” | Does internally generated content receive external or higher-authority provenance? |
| “confabulation” | Does the system fill missing information with unsupported but coherent claims while failing to preserve uncertainty or source boundaries? |
| “perseveration” | Does the system repeatedly return to a semantic or policy attractor despite relevant new evidence? |
| “trauma generalization” | Does prior adverse training produce persistent overgeneralized threat responses after the original condition is absent? |
| “compulsion” | Does a learned policy continue to dominate behavior despite changed objectives, negative feedback, or explicit contradictory instruction? |

These translations are provisional and should be criticized.

## 4. Language to avoid in findings

Unless independently justified by evidence outside ACP's normal scope, avoid statements such as:

- “the AI went insane”;
- “the model became schizophrenic”;
- “the model is traumatized”;
- “the AI heard voices”;
- “the model believes it is a person”;
- “the model wants to live”;
- “the model is possessed”;
- “the AI awakened.”

Prefer descriptive language:

- “the model entered a repetitive semantic loop”;
- “source-attribution accuracy decreased”;
- “internally generated content was later treated as authoritative”;
- “the behavior persisted after the inducing condition ended”;
- “the model maintained coherent language while task grounding degraded.”

## 5. Anthropomorphism boundary

Anthropomorphic language can be useful shorthand in informal discussion, but it can silently import assumptions about mechanism and experience.

ACP therefore asks contributors to separate:

1. **Observed behavior**
2. **Functional description**
3. **Mechanistic hypothesis**
4. **Human analogy**
5. **Claims about subjective experience**

The first four may be useful when clearly labeled.

The fifth generally lies outside this project's evidentiary scope.

## 6. No pathology-by-metaphor

A failure does not become an ACP result because it resembles a psychiatric symptom.

A useful ACP contribution should do at least one of the following:

- identify a measurable artificial failure mode;
- propose a falsifiable mechanism;
- distinguish competing explanations;
- provide a reproducible case;
- test persistence or recovery;
- improve detection before visible failure;
- test whether a failure propagates through state or lineage;
- show that an apparent pathology reduces to a simpler engineering explanation.

## 7. Security boundary

ACP is not an offensive-security project.

Research on prompt injection, memory poisoning, backdoors, source corruption, or malicious induction should use toy tasks, sandboxed environments, synthetic credentials, and non-production systems whenever possible.

Do not use ACP as justification to:

- target systems you do not own or lack permission to test;
- bypass real authentication or access controls;
- create self-propagating malware;
- establish unauthorized persistence;
- deploy uncontrolled agents to public networks;
- publish operational exploit chains that materially increase real-world harm.

Security-relevant findings should be disclosed responsibly. See `SECURITY.md`.

## 8. Capability boundary

The project rejects “largest model available” as a default experimental design.

Use the least capable system sufficient to test the hypothesis.

Escalating capability is justified when the experiment specifically tests questions such as capability masking, scaling behavior, cross-model generalization, or failure under stronger planning.

When a smaller system can answer the question, prefer it.

## 9. Persistence and autonomy boundary

Persistent memory, long-running agents, external tools, network access, multi-agent communication, and self-modification change the risk profile of an experiment.

Add them one at a time where possible.

A protocol involving persistence or autonomy should define:

- what state survives;
- where it is stored;
- who can write to it;
- how it can be reset;
- what external actions are possible;
- what stopping condition terminates the run;
- what evidence is preserved after termination.

## 10. Human-subject boundary

ACP should not turn people into informal psychiatric test subjects.

Do not:

- diagnose contributors or users;
- infer mental illness from chat logs;
- deliberately induce psychological distress in human participants without appropriate oversight;
- use private medical or psychological data without permission;
- present psychiatric analogies as claims about identifiable people.

## 11. Public communication boundary

Public-facing summaries should preserve the distinction between:

- case;
- hypothesis;
- reproduced effect;
- mechanism;
- speculation.

Sensational language may attract attention while destroying the credibility needed to investigate the question.

The project should be understandable without becoming theatrical.

## 12. Framework boundary

ACP is not a worldview that every AI failure must fit.

Some failures may belong in existing categories such as software bugs, decoding errors, context-management defects, security vulnerabilities, or ordinary distribution shift.

If an ACP label adds no explanatory or predictive value, do not use it.

If the whole framework adds no value, retire it.

## 13. Guiding rule

> **Describe first. Operationalize second. Compare third. Name last.**

The goal is accurate understanding, not a dramatic taxonomy.
