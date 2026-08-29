# Maintainer Guide

## Merge discipline

1. Review factual and ownership boundaries before wording quality.
2. Require `make check` and a green default CI workflow.
3. Keep pull requests single-purpose where possible.
4. Do not merge documentation that describes a temporary branch as the default product.
5. Do not rewrite public history after review unless a security incident requires it.

## Release discipline

The project currently has no tagged stable release. Before creating one:

1. Confirm `main` contains the intended Skill and installation documentation.
2. Run the full deterministic suite from a clean checkout.
3. Perform an actual installation test from the candidate tag.
4. Run documented model forward evaluations or explicitly state that they were not run.
5. Move changelog entries from `Unreleased` to a dated version.
6. Publish only Claims supported by the release artifacts.

## Dependency updates

Dependabot proposes monthly updates for Python validation dependencies and GitHub Actions. Review changelogs and run the full suite; do not auto-merge major-version updates.

## Eval maintenance

- Keep public repositories pinned to 40-character commits.
- Preserve `supports` and `does_not_support` for every evidence anchor.
- Never change a curated gold case to `actual_skill_run: true` without saved run metadata.
- Add cases for new failure classes rather than only increasing prose in `SKILL.md`.
- Retire stale cases explicitly in the changelog instead of silently repointing them to `main`.

## Community data

Issues and showcase submissions are public. Remove personal data, private repository material, credentials, and unverifiable hiring outcomes. Close or redact unsafe submissions as soon as they are noticed.
