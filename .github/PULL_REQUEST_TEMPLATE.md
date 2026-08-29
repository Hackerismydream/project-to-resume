## Problem

What failure mode or user problem does this PR address?

## Change

What changed in the Skill, references, evals or tooling?

## Evidence boundary

- What is implemented and deterministically validated?
- What still depends on model behavior or real-user evaluation?
- What claims must not be made from this PR alone?

## Validation

- [ ] `python3 scripts/lint_examples.py skills/project-to-resume/examples/*.md`
- [ ] `python3 scripts/validate_package.py`
- [ ] `python3 -m unittest discover -s tests -v`
- [ ] `python3 scripts/smoke_install.py --source .`
- [ ] `git diff --check`

## Safety

- [ ] No private repository data, resume PII, credentials or customer data added.
- [ ] README/product claims do not exceed implemented or measured capability.
