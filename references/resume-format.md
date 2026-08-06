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
