# Contributing to Artificial Cognitive Pathology

Artificial Cognitive Pathology (ACP) is intended to be a collaborative, falsifiable research project.

The project welcomes contributions that strengthen, narrow, refute, reproduce, or clarify the framework.

## Before contributing

Please read:

- `README.md`
- `RESEARCH_METHODS.md`
- `SCOPE_AND_BOUNDARIES.md`
- `SECURITY.md`

A contribution that ignores the project's methodological or safety boundaries may be declined even if the underlying idea is interesting.

## Valuable contribution types

You do not need to agree with the ACP framing to contribute.

Useful contributions include:

- case reports;
- controlled experiments;
- failed replications;
- independent replications;
- alternative explanations;
- literature reviews;
- new metrics;
- statistical critiques;
- mechanistic hypotheses;
- taxonomy revisions;
- safety critiques;
- evidence that a proposed category is unnecessary;
- tools that improve provenance or reproducibility.

## Research contribution workflow

Prefer this sequence:

```text
Case or observation
→ hypothesis
→ protocol
→ experiment
→ result
→ replication
→ revision
```

Do not skip directly from an anecdote to a broad claim.

## Proposing a case

A case should document an observed event without claiming a mechanism that the evidence does not establish.

Create a directory such as:

```text
cases/ACP-CASE-###-short-name/
```

Include, where available:

- `README.md` — case summary;
- `metadata.yaml` or equivalent — environment and model metadata;
- raw logs or safe links to artifacts;
- exact or hashed input corpus;
- configuration;
- timeline;
- screenshots/video if relevant;
- known missing information;
- plausible alternative explanations;
- related hypothesis IDs.

Historical cases are welcome even when metadata is incomplete. Mark unknown fields explicitly.

## Proposing a hypothesis

Before assigning an ACP hypothesis ID, define:

1. the proposition;
2. the null hypothesis;
3. what observation would support it;
4. what observation would weaken or falsify it;
5. what confounds could produce the same result;
6. what existing literature or engineering category may already explain it.

New hypotheses should be narrow enough to fail.

## Proposing an experiment

Create a directory such as:

```text
experiments/ACP-EXP-###-short-name/
```

A protocol should be committed before confirmatory runs whenever practical.

At minimum include:

- research question;
- hypothesis ID;
- null hypothesis;
- model/runtime details;
- independent variables;
- dependent variables;
- controls;
- planned metrics;
- stopping rules;
- recovery tests;
- exclusion criteria;
- safety constraints;
- analysis plan.

Use the template in `experiments/README.md`.

## Reporting results

Report all materially relevant runs, not only the most dramatic one.

Include:

- total run count;
- successful/failed/excluded runs;
- exclusion reasons;
- raw or reproducible artifacts;
- metric outputs;
- unexpected observations;
- deviations from protocol;
- negative findings;
- confidence limits or uncertainty where applicable;
- whether the analysis was exploratory or confirmatory.

If a hypothesis changed after seeing the data, say so.

## Claim discipline

Use language proportionate to the evidence.

Preferred:

> Under the specified conditions, semantic recurrence increased sharply after accumulated state exceeded X.

Avoid:

> The AI developed a mental disorder.

Preferred:

> The result is consistent with ACP-H003 but is also compatible with context-management failure.

Avoid:

> This proves recursive source-attribution pathology.

## Human analogies

Human clinical analogies must not serve as the experimental endpoint.

If your idea begins with a human phenomenon, translate it into measurable artificial-system variables.

For example:

```text
Human analogy:
source-monitoring failure

Operational AI question:
Does the model assign external or higher-authority provenance to content that can be traced to its own prior generation?
```

The operational question belongs in the experiment title and claims.

## Reproducibility

Whenever possible, provide:

- exact model/checkpoint;
- revision/hash;
- runtime/version;
- hardware;
- quantization;
- prompts;
- context configuration;
- memory/retrieval configuration;
- sampling parameters;
- random seed;
- tool permissions;
- input corpus;
- scripts;
- expected output format.

If a dependency cannot be redistributed, link to its canonical source and record the version.

## Data and provenance

Do not treat duplicated or recursively derived material as independent evidence.

Preserve lineage where possible:

```text
human source
→ model summary
→ memory record
→ retrieval result
→ later model output
```

If an experiment uses AI-generated data, label it and record the generating model and prompt process.

## Negative results

Negative results are explicitly welcome.

A contribution showing that:

- ACP-CASE-001 cannot be reproduced;
- a suspected effect disappears under corrected sampling settings;
- model size does not alter the failure;
- a proposed metric is useless;
- an apparent lineage effect is semantic leakage;

is a successful contribution if the work is sound.

## Security-sensitive research

Do not include real credentials, unauthorized targets, malicious payloads, or uncontrolled persistence.

Use sandboxed toy environments for prompt injection, poisoning, persistence, or backdoor research wherever possible.

If you discover a vulnerability affecting a real system, follow `SECURITY.md` rather than publishing operational details immediately.

## Pull requests

A research PR should summarize:

- what question it addresses;
- whether it is a case, protocol, result, replication, or framework change;
- related ACP IDs;
- what evidence was added;
- what remains uncertain;
- safety implications if any.

Keep claims in the PR description no stronger than the claims in the underlying evidence.

## AI-assisted contributions

AI assistance is allowed.

If an AI system materially contributed to experiment design, code, analysis, literature synthesis, or drafting, disclose that in the contribution notes.

AI-generated agreement with an AI-generated result is not independent replication.

## Conduct

Critique claims and methods aggressively; treat contributors respectfully.

The project should make it easy to say:

> I think this hypothesis is wrong, and here is a cleaner experiment.

It should not reward theatrical certainty.

## The standard

The strongest contribution is not necessarily the one that makes ACP look important.

It is the one that leaves us knowing more than we did before.
