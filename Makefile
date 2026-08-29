PYTHON ?= python3

.PHONY: install-dev compile lint validate test smoke check

install-dev:
	$(PYTHON) -m pip install --disable-pip-version-check -r requirements-dev.txt

compile:
	$(PYTHON) -m py_compile scripts/*.py tests/*.py

lint:
	$(PYTHON) scripts/lint_examples.py examples/*.md

validate:
	$(PYTHON) scripts/validate_package.py

test:
	$(PYTHON) -m unittest discover -s tests -v

smoke:
	$(PYTHON) scripts/smoke_install.py --source .

check: compile lint validate test smoke
