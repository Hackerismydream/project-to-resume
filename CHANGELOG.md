# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The project intends to use semantic versioning when tagged releases begin. Until then, changes remain under `Unreleased` and must not be represented as a published version.

## [Unreleased]

### Added

- Repository-first discovery with a role-agnostic Repository Map.
- Behavior-chain tracing from entry through state, side effects, failure, recovery, and terminal output.
- Test-guided story discovery and explicit evidence ceilings.
- Conditional history, PR, issue, and upstream analysis.
- Story Hypothesis and Story Card competition with counterevidence and elimination reasons.
- Fixed-revision eval contracts and positive/negative invocation fixtures.
- Isolated installation smoke test and package validator.
- Pico empty-response recovery curated case and reproducible SVG overview.
- Apache-2.0 licensing, contribution, security, conduct, installation, evaluation, and maintenance documentation.

### Changed

- Target roles and JDs are applied only after repository facts and initial story candidates are established.
- Resume projects may contain 1–5 bullets; generation stops when an additional bullet adds no independent role signal.
- JD-only input no longer permits generation without project evidence.
- Package validation uses real YAML parsing and Draft 2020-12 JSON Schema validation.
- CI checks the submitted diff with full Git history instead of silently falling back to the working tree.

### Fixed

- Removed merge-time README text that would become stale on the default branch.
- Aligned isolated installation with recursive Skill directory copying.
- Clarified that tests, benchmarks, curated cases, releases, and production outcomes are distinct evidence levels.

## Release process

When a release is prepared:

1. Move relevant entries from `Unreleased` into a dated version section.
2. Run `make check` and verify the default-branch CI.
3. Confirm installation from the tagged revision.
4. Create a GitHub release whose notes match this changelog.
5. Do not claim semantic model quality or user outcomes unless a corresponding evaluation artifact exists.
