VENV                := .venv
VENV_PYTHON         := $(VENV)/bin/python
SYSTEM_PYTHON       := $(or $(shell which python3), $(shell which python))
PYTHON              := $(or $(wildcard $(VENV_PYTHON)), $(SYSTEM_PYTHON))
POETRY              := $(shell command -v poetry 2> /dev/null)

APP_ROOT            := ./app
TESTS_ROOT          := $(APP_ROOT)/tests

MYPY                := mypy $(APP_ROOT)
MYPY_TESTS          := $(MYPY) $(TESTS_ROOT)

.PHONY: black isort flake8 bandit

black:
	$(POETRY) run black $(APP_ROOT) --check

isort:
	$(POETRY) run isort $(APP_ROOT)

flake8:
	$(POETRY) run flake8 $(APP_ROOT)

bandit:
	$(POETRY) run bandit $(APP_ROOT)

.PHONY: mypy mypy-tests test test-vvv test-xml

mypy:
	$(MYPY)

mypy-tests:
	$(MYPY_TESTS)

test:
	$(POETRY) run pytest --cov=$(APP_ROOT)

test-vvv:
	$(POETRY) run pytest --cov=$(APP_ROOT) -vvv

test-xml:
	$(POETRY) run pytest --cov=$(APP_ROOT) --cov-report=xml


.PHONY: clean

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -type d -name '*.egg-info' `
	rm -rf `find . -type d -name 'pip-wheel-metadata' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build

.PHONY: version poetry_version

poetry_version:
	$(POETRY) version $(version)

version:
	$(POETRY) version $(v)
	@git add pyproject.toml
	@git commit -m "v$$(POETRY version -s)"
	@git tag v$$(POETRY version -s)
	@git push
	@git push --tags
	$(POETRY) version

.PHONY: run build help init_data

init_data:
	$(POETRY) run ps

run:
	$(POETRY) run run.sh
	@echo "Running!!!"

build:
	$(POETRY) build


.PHONY: all-files autoupdate

all-files:
	pre-commit --all-files

autoupdate:
	pre-commit autoupdate
