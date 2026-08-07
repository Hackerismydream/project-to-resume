# Resume translation and format

The goal is not to translate internal names into polished prose. Translate a
project abstraction into a familiar system problem, observable behavior, and an
experiment that proves only what it actually measured.

## Six-step translation

1. **Scene** — When and where does the system run?
2. **Failure** — What concrete failure does a naive implementation create?
3. **Observable behavior** — What does the system make true for users or other
   components?
4. **Baseline** — What naive design, negative invariant, or controlled treatment
   makes the design choice testable?
5. **Result** — Which metric corresponds to that failure?
6. **Evidence boundary** — Which revision, workload, sample, evidence class, and
   success gate does the result cover?

Examples of useful translations:

| Internal term | Familiar problem | Resume-level wording |
| --- | --- | --- |
| Per-session lane | Ordering and head-of-line blocking | Same-session work runs in order while independent sessions run concurrently |
| Context curator | Fixed-capacity resource allocation | Preserve the current goal and high-value history inside a bounded context window |
| Weighted RRF | Multi-retriever ranking | Fuse lexical and semantic candidates while measuring both recall and false injection |
| Tool registry | API gateway and schema governance | Validate tool arguments before execution and normalize timeout/failure results |
| Typed terminal event | Request state machine | Distinguish completion, tool failure, provider failure, cancellation, and delivery failure |

## Writing rules

- Start with the system problem, not a class or module name.
- State observable behavior before internal mechanism.
- Use at most one project-internal term and two standard technical terms per
  bullet unless precision requires more.
- A percentage always names its baseline. A zero always names what was counted.
- If no valid result exists, write an architecture claim without a number.
- Put detailed evidence boundaries in the evidence map when including them in
  the bullet would make it unreadable.
- JD tailoring may change ordering and vocabulary, never the underlying fact
  set, scope, numbers, or contribution verb.

## Two-version output contract

Always separate what is usable now from what becomes usable after measurement.

### Current evidence — evidence-ready

- Use only claims and numbers that already pass the evidence and attribution
  gates.
- Do not include placeholders, estimates, target values, or hoped-for effects.
- An architecture bullet without a number is valid when implementation is the
  strongest available evidence.

Use the heading:

```markdown
## 当前证据版（证据可用）
```

### Metric-enhanced — recommended target

- Keep the same project facts and mechanisms; improve only the evidence layer.
- Use verified metrics directly when their revision and scope match.
- Represent missing values as named placeholders, for example
  `[待实测：最佳单路 Recall@10]`, never as estimates.
- Quantify only the claims whose failure mode has a meaningful metric. Not every
  bullet needs a number.

If any placeholder remains, use:

```markdown
## 指标增强版（推荐目标，待实测，不可投递）
```

When every metric is verified and all success gates pass, remove the placeholders
and use:

```markdown
## 指标增强版（推荐版，指标已验证）
```

“Recommended” describes the preferred evidence-backed narrative. It never makes
an unmeasured value submit-ready and never bypasses personal attribution.

## Measurement plan

Every named placeholder must appear in a compact plan:

```markdown
| Claim | Values to fill | Baseline | Frozen workload and sample | Metric and success gate | Artifact |
| --- | --- | --- | --- | --- | --- |
| Hybrid retrieval | [待实测：最佳单路 Recall@10], [待实测：融合 Recall@10] | Best lexical or semantic source | Held-out queries at exact SHA | Recall rises; leakage and task success do not regress | Manifest + raw outcomes + aggregate |
```

The plan is part of the working evidence package, not resume prose. If the
experiment fails its correctness or task-success gate, preserve the negative
result and keep the current-evidence version.

## Preferred project section

```markdown
Project Name | One-line interviewer-familiar positioning

Core technologies: ...

Project description: one compact paragraph describing the operating scene,
main failure modes, and system boundary.

1. Strongest architecture or behavior claim.
2. Strongest verified or comparative claim.
3. Another non-overlapping claim, or a useful negative experiment.
```

Use three to five bullets by default. Six is acceptable only when all six are
distinct and well supported.

## Evidence map

Keep it outside the resume text:

```markdown
| # | Claim | Evidence | Class | Boundary |
| --- | --- | --- | --- | --- |
| 1 | ... | file/URL at full SHA | implementation | No performance claim |
```

If attribution is unknown, title the output `Project-level draft` and use the
project as the grammatical subject. Convert to personal verbs only after the
user confirms their role and disclosure rights.

## Negative experiment pattern

```text
Evaluated [strategy] under [frozen workload]. Although [local metric] changed
from A to B, [task-success metric] regressed from C to D; the release gate
therefore rejected the strategy.
```

Do not say the experiment “created” a gate unless chronology proves that. It may
have been judged by an existing gate.
