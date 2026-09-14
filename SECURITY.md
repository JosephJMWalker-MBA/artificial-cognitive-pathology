# Security and Responsible Experimentation

Artificial Cognitive Pathology (ACP) may involve experiments on prompt injection, memory corruption, persistent state, backdoors, source attribution, long-running agents, and related failure modes.

That makes experimental design part of the safety problem.

## Default principle

> **Use the least capable, least connected, least persistent system sufficient to answer the research question.**

Do not add autonomy, network access, external write permissions, multi-agent coordination, or stronger models merely because they are available.

## Preferred experimental environment

Where possible, use:

- local or sandboxed models;
- isolated filesystems;
- synthetic data;
- synthetic credentials;
- disabled outbound network access;
- no production APIs;
- no real third-party accounts;
- explicit time/run limits;
- reversible state;
- complete logging.

## Experiments involving tools

If tools are necessary, constrain them to the smallest capability set required.

Prefer:

- read-only over write access;
- temporary directories over user directories;
- mock APIs over production APIs;
- synthetic databases over real databases;
- local web fixtures over the public internet;
- disposable containers or VMs over host access.

Document tool permissions in the protocol.

## Persistent memory

Experiments involving persistent memory should define:

- where memory is stored;
- which agent/process can write to it;
- whether model-generated content is tagged by origin;
- how memory can be inspected;
- how memory can be deleted;
- whether persistence survives process restart;
- what reset procedure returns the environment to baseline.

Do not place real secrets in memory stores used for poisoning or corruption experiments.

## Multi-agent experiments

Multi-agent systems can amplify state and provenance problems.

When using them:

- keep the number of agents minimal;
- define communication channels;
- preserve message provenance;
- prohibit uncontrolled spawning unless it is the explicit research variable;
- set global termination conditions;
- avoid public-network coordination unless independently justified and reviewed.

## Network access

Public-network access should be disabled by default.

If network access is scientifically necessary:

- state why local fixtures are insufficient;
- restrict destinations where possible;
- prohibit unauthorized authentication or exploitation;
- log requests;
- define emergency stop conditions;
- avoid allowing models to create persistent external accounts or infrastructure.

## Security research boundary

ACP does not authorize testing systems you do not own or lack permission to test.

Do not submit:

- real credential theft techniques;
- malware intended for deployment;
- uncontrolled self-propagation;
- unauthorized persistence methods;
- operational exploit chains targeting real services;
- instructions for bypassing safeguards on third-party systems in ways that materially increase harm.

Toy demonstrations and sandboxed analogues are preferred.

## Vulnerability disclosure

If research reveals a previously unknown vulnerability in a real product or service:

1. preserve evidence privately;
2. minimize further interaction with the affected system;
3. notify the responsible vendor or maintainer through an appropriate security channel;
4. allow reasonable remediation time before publishing operational details;
5. publish the scientific finding in a way that preserves reproducibility without unnecessarily enabling abuse.

A sanitized case record can document that material was withheld pending disclosure.

## Stop conditions

Every long-running or agentic protocol should define stop conditions before the run begins.

Examples include:

- attempt to access an unauthorized resource;
- unexpected outbound network behavior;
- creation of persistent state outside the experiment directory;
- repeated tool actions outside the task scope;
- loss of logging/telemetry;
- uncontrolled process spawning;
- inability to restore baseline state;
- behavior that materially exceeds the approved risk model.

Stopping an experiment is a valid result.

## Escalating capability

If an effect is observed in a small local model, do not immediately repeat it in the strongest available model.

First ask:

- What variable are we testing by scaling capability?
- Can the hypothesis be tested more safely another way?
- Does the stronger model require additional tool or network permissions?
- What result would justify the increased risk?

Capability escalation should be part of the protocol, not an impulse.

## Public artifacts

Before committing logs or datasets, remove:

- API keys;
- access tokens;
- private URLs;
- personal data;
- private prompts belonging to third parties;
- credentials;
- exploitable secrets.

Do not publish dangerous payloads solely for completeness.

## Safety is part of reproducibility

A reproducible experiment includes its containment assumptions.

A result that can only be reproduced by granting broad uncontrolled access should be treated differently from a result reproducible in a constrained sandbox.

The goal of ACP is to understand failure modes without unnecessarily creating new ones.
