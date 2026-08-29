# Troubleshooting

## The Skill is not discovered

- Confirm the installed directory is named `project-to-resume`.
- Confirm `SKILL.md` is at the directory root.
- Confirm the frontmatter `name` is `project-to-resume`.
- Refresh or restart the host Agent's Skill index.

## The output is generic

- Confirm the Agent can read the repository.
- Ask it to inspect the current repository before writing.
- Pin a commit for reproducibility.
- Do not preselect technologies that it must find; provide only the target role.

## The output invents a number or result

- Remove the unsupported claim.
- Provide the metric object, baseline, workload or sample, revision, and run artifact.
- Distinguish test source, test execution, benchmark, release, and production evidence.

## The output claims personal ownership of a public repository

- State whether it is your personal project, team project, fork, or upstream contribution.
- Identify the modules or changes you personally implemented or validated.
- For forks, compare against the pinned upstream revision.

## Validation fails locally

Install the development dependencies and rerun the individual stages:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m py_compile scripts/*.py tests/*.py
python3 scripts/lint_examples.py examples/*.md
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py --source .
```

Read the first failing stage before changing later checks. Structural validation does not require executing any target repository code.

## A link or fixed case is stale

Open a documentation issue with the exact file and fixed public source. Do not silently replace a pinned commit with `main`; update the case, expected behavior, and changelog together.
