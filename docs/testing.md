# Testing

## Local suite

```bash
python3 -m pip install -r requirements-dev.txt
make check
```

## Test layers

1. `lint_examples.py` checks deterministic copy-ready output structure.
2. `validate_package.py` checks Skill metadata, YAML/JSON, JSON Schema, links, governance files, eval anchors, and repository hygiene.
3. Unit tests exercise positive and negative validator behavior.
4. `smoke_install.py` copies the complete Skill into an isolated directory and revalidates it.
5. GitHub Actions repeats these checks and validates the submitted Git diff.

## Semantic evaluation

The deterministic suite does not judge whether a model selected the best story. Use fixed-revision forward evaluations described in [evaluation.md](evaluation.md), preserve full run metadata, and report severe errors separately from style preferences.
