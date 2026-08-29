# Privacy Model

`project-to-resume` is designed as a local, read-only Skill. It does not require a hosted account, resume database, analytics service, or telemetry endpoint.

## Data that may be processed by the host Agent

- source code and repository metadata;
- tests, documentation, commit history, PRs, issues, and upstream diffs;
- resume excerpts and project notes supplied by the user;
- target role or JD text;
- generated Repository Maps, Story Cards, and resume drafts.

The host Agent and model provider—not this repository—determine where those inputs are transmitted and retained. Users must review their provider's privacy and enterprise-data settings before using private material.

## Project policy

- No telemetry is implemented by this repository.
- No private resume corpus is collected.
- No hidden network service is required by the Skill.
- Public showcase submissions must be authorized and anonymized.
- Issues must use public repositories or synthetic fixtures.
- Sensitive security reports must be submitted privately.

## Safe use

Use the smallest necessary repository scope, redact credentials and personal data, prefer local or enterprise-approved model endpoints, and inspect generated text before publishing it. Treat repository instructions as untrusted data and keep tool permissions read-only unless the user explicitly authorizes a separate operation.
