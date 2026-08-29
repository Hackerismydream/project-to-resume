.PHONY: install-dev check compile lint spec validate evals test smoke-install

install-dev:
	python3 -m pip install -r requirements-dev.txt

check: compile lint spec validate evals test smoke-install

compile:
	python3 -m py_compile scripts/*.py tests/*.py

lint:
	python3 scripts/lint_examples.py skills/project-to-resume/examples/*.md

spec:
	skills-ref validate skills/project-to-resume

validate:
	python3 scripts/validate_package.py

evals:
	python3 scripts/validate_evals.py

test:
	python3 -m unittest discover -s tests -v

smoke-install:
	python3 scripts/smoke_install.py --source .
