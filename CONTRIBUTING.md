# Contributing

Thanks for improving `project-to-resume`. The project is intentionally narrow: turn software repositories into truthful, interview-defensible Chinese resume project experience.

## Good contributions

High-value contributions usually fall into one of these categories:

- a fixed public repository + commit that exposes a failure mode the current method misses;
- a false-positive / false-negative Skill trigger case;
- an ownership, metric, benchmark, release, fork or upstream boundary case;
- a packaging or Agent Skills compatibility bug;
- a deterministic validation improvement;
- an anonymized Before / After case with explicit permission to publish.

Please avoid expanding the project into an ATS, job tracker, PDF generator, offer manager, generic code-review tool, or multi-Skill career platform.

## Development

```bash
python3 scripts/lint_examples.py skills/project-to-resume/examples/*.md
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py --source .
git diff --check
```

The CI additionally exercises the official `skills` CLI against the local repository layout.

## Adding an eval case

1. Use a public repository and pin a full 40-character commit SHA.
2. Add a case under `evals/cases/` following `evals/schema.json`.
3. Separate:
   - project facts;
   - candidate ownership;
   - current implementation;
   - tests that exist;
   - tests that actually ran;
   - benchmark measurements;
   - release / production / business outcomes.
4. Include both `supports` and `does_not_support` for every evidence anchor.
5. Mark manually authored cases as `curated_gold: true` and `actual_skill_run: false` unless a real installed-skill run was actually executed and preserved.
6. Add or update tests if the case introduces a new invariant.

## Changing the Skill

Keep `skills/project-to-resume/SKILL.md` concise enough to load as runtime instructions. Put deeper domain material in `references/` and load it progressively.

A behavior change should normally include:

- the failure mode being fixed;
- the smallest instruction/reference change that fixes it;
- a deterministic regression test where possible;
- an eval case when deterministic code cannot judge the semantic behavior;
- README changes only after the underlying capability exists.

## Before / After submissions

Use the [Showcase template](.github/ISSUE_TEMPLATE/showcase.yml) or `showcase/README.md`.

Do not submit private resumes, private repositories, customer data, credentials, personal contact details, or employer-confidential information.

## Pull requests

Keep PRs reviewable. State what is implemented, what is only structurally validated, what still needs real model evaluation, and what claims must not be made.
