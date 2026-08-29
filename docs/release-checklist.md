# Release Checklist

- [ ] `main` contains the intended Skill and documentation.
- [ ] `make check` passes from a clean checkout.
- [ ] GitHub Actions is green on the release commit.
- [ ] Installation is tested from the exact candidate tag or commit.
- [ ] `SKILL.md` frontmatter name, description, and license are correct.
- [ ] README commands and screenshots match default-branch behavior.
- [ ] Eval cases use fixed public commits and satisfy the schema.
- [ ] Curated gold is not labeled as an actual Skill run.
- [ ] Any forward evaluation records host Agent, model, configuration, repository revision, input, output, and reviewer.
- [ ] Claims in release notes do not exceed deterministic checks or saved evaluation artifacts.
- [ ] `CHANGELOG.md` moves relevant items out of `Unreleased` into a dated version.
- [ ] Security, privacy, contribution, and support links are valid.
- [ ] No private resumes, internal code, credentials, customer data, caches, or temporary branch text are included.
