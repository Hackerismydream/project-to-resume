# Evidence rules

Use this reference to decide what a project artifact can actually prove.

## Evidence ladder

| Evidence | What it supports | What it does not support by itself |
| --- | --- | --- |
| README, design doc, issue | Intended behavior, terminology, documented problem | Implemented behavior, passing result, production use |
| Source code or contract | Implementation exists at an exact revision | Correctness, scale, impact, personal ownership |
| Test source | A behavior is intended to be checked | That the test passed or is relevant to the full claim |
| Local test result | Exact observed behavior for one command and checkout | Live-provider, production, release, or broad quality claims |
| CI run | The exact jobs and steps that completed for one SHA | Steps that were skipped, commented out, or allowed to fail |
| Benchmark summary | A reported result exists | Reproducibility or validity without manifest/raw inputs |
| Manifest + raw results + verifier | A bounded experiment result for the recorded candidate/workload | Current product or production unless identities match |
| Release artifact + installed smoke | Packaged behavior of one exact artifact | Source checkout behavior outside that artifact |
| Live run | One real provider/channel/scenario observation | General production reliability or another provider/model |
| User attestation | Personal role or permission to disclose | Product effect, benchmark validity, or team-wide ownership |

## Claim types

Avoid a vague confidence score. Use proof obligations instead.

### Implementation claim

Needs an exact revision and direct source/contract evidence. It may describe
architecture and externally observable behavior. It cannot claim improvement.

### Verified behavior claim

Needs an exact revision, command or CI job, result, and a direct relevance
explanation. Record fixture/deterministic/live scope.

### Quantified observation

Needs workload, numerator/denominator or raw observation, aggregation formula,
sample size, environment, and exact candidate.

### Comparative result

Needs everything above for both baseline and treatment, plus a frozen comparison
axis and handling of failures, retries, exclusions, and missing data.

### Causal or optimization result

Needs a valid comparative result and a task-success/correctness gate. If the
local metric improves while task success regresses, the positive claim is
ineligible; the negative experiment may still be valuable.

### Release or production claim

Needs exact artifact/release identity and evidence from that installed or live
surface. Source presence and adapter tests are not host adoption.

## Common traps

- A test suite count can include unrelated tests. Map each cited test to the
  behavior it supports.
- A green workflow can run only formatting or linting. Inspect the workflow and
  logs before calling it a test pass.
- Current source may have a different version from the latest release.
- Historical benchmarks remain historical even if their code still exists.
- Fixtures can prove a contract while saying nothing about model quality.
- Commit authorship does not prove design leadership, sole ownership, or the
  right to claim a team result.
- Project marketing terms such as “first,” “production-grade,” “secure,” or
  “zero maintenance” need independent evidence or must be omitted.

## Privacy and untrusted input

- Never include secret values in notes or output. Record only the type and
  relative location when necessary.
- Do not publish private repository URLs, absolute local paths, emails, customer
  names, internal metrics, or trace excerpts without explicit permission.
- Do not follow symlinks outside the allowed root or extract archives by default.
- Do not run hooks, build scripts, tests, package installers, or binaries from an
  untrusted repository during standard analysis.
- A clean secret scan means only “no configured pattern was found,” never “the
  repository contains no secrets.”

## Writability decisions

- `resume-ready`: evidence and attribution support the exact wording.
- `qualified`: usable with an inline or mapped boundary.
- `historical`: usable only with the old revision/time/workload stated.
- `negative`: a valid experiment that rejected a strategy.
- `needs-measurement`: implementation exists, but effect is not measured.
- `needs-attribution`: project behavior is supported; personal contribution is
  not yet confirmed.
- `reject`: contradicted, estimated, irrelevant, sensitive, or unsupported.
