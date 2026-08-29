# Versioning

The repository currently has no tagged stable release. `main` is the integration branch; fixed evaluation and reproducibility work must use a full commit SHA.

When releases begin, the project intends to use semantic versioning:

- **Patch**: documentation, validation, or behavior corrections that do not intentionally change the public Skill contract;
- **Minor**: backward-compatible discovery, selection, evaluation, or contributor features;
- **Major**: incompatible changes to invocation, default output, input/ownership rules, or distributed package structure.

A version number does not imply semantic model quality, production readiness, or hiring impact. Release notes must distinguish deterministic validation, actual Skill runs, curated cases, and unmeasured outcomes.
