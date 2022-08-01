app_root = ./app
app_script = ./scripts
tests_src = $(app_root)/tests

isort = $(app_script)/format-imports.sh
black = $(app_script)/format.sh
flake8 = flake8 $(app_root) $(tests_src)
mypy = mypy $(app_root)
mypy_tests = mypy $(app_root) $(tests_src)
lint = $(app_script)/lint.sh

.PHONY: format check-format lint mypy mypy-tests test-local test-dev test-dev-cov clean poetry_version version runapp build help init_data

format:
	$(isort)
	$(black)

check-format:
	$(isort) --check-only
	$(black) --check

lint:
	$(lint)

mypy:
	$(mypy)

mypy-tests:
	$(mypy_tests)

test-local:
	pytest $(tests_src) --cov=$(app_root)

test-dev:
	pytest $(app_root)

test-dev-cov:
	$(app_script)/test-cov-html.sh
	@echo "building coverage html"
	@echo "opening coverage html in browser"
	@open htmlcov/index.html

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

poetry_version:
	poetry version $(version)

version: poetry_version
	$(eval NEW_VERS := $(shell cat pyproject.toml | grep "^version = \"*\"" | cut -d'"' -f2))
	@sed -i "" "s/__version__ = .*/__version__ = \"$(NEW_VERS)\"/g" $(app_root)/__init__.py

init_data:
	poetry run ps

runapp:
	poetry run run.sh
	@echo "Running!!!"

build:
	poetry build
