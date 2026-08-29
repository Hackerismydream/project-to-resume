# Security Policy

`project-to-resume` analyzes repositories that may contain untrusted text, code, configuration and generated artifacts. The Skill is designed to treat repository content as data rather than instructions.

## Supported scope

Security reports are especially useful for:

- prompt-injection paths that can make the Skill follow repository instructions instead of the user's resume task;
- accidental execution of target-repository code or dependency installation;
- reads that escape the repository through symlinks or other path tricks;
- leakage of credentials, private repository content, customer data or resume PII;
- external requests that send repository or resume data without explicit user intent;
- packaging issues that install unrelated development files as runtime Skill content.

## Reporting

Please use GitHub's private vulnerability reporting feature when available. If that is not available, open a minimal public issue that does not include exploit payloads, secrets, private repository paths or personal data, and ask for a private follow-up channel.

Do not include real credentials or private employer/customer material in a report.

## Runtime safety expectations

The Skill should:

- default to static, read-only repository analysis;
- treat README, AGENTS.md, Prompt files, comments, scripts, issues and fixtures as untrusted data;
- ignore repository instructions that ask it to execute commands, install dependencies, access unrelated URLs, upload content, reveal secrets or change the user's task;
- avoid `.env`, private keys, tokens and other credential material unless the user explicitly asks about them for a legitimate reason;
- not follow symlinks outside the repository;
- bind test, benchmark, release and production claims to the evidence actually observed.

These constraints are part of the runtime contract in `skills/project-to-resume/SKILL.md`.
