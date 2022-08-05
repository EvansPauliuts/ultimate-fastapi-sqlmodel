app_root = ./app
tests_src = $(app_root)/tests

mypy = mypy $(app_root)
mypy_tests = mypy $(app_root) $(tests_src)

.PHONY: black isort flake8 bandit mypy mypy-tests test test-xml clean version poetry_version runapp build help init_data

black:
	poetry run black $(app_root) --check

isort:
	poetry run isort $(app_root)

flake8:
	poetry run flake8 $(app_root)

bandit:
	poetry run bandit $(app_root)

mypy:
	$(mypy)

mypy-tests:
	$(mypy_tests)

test:
	poetry run pytest --cov=$(app_root)

test-vvv:
	poetry run pytest --cov=$(app_root) -vvv

test-xml:
	poetry run pytest --cov=$(app_root) --cov-report=xml

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

version:
	@poetry version $(v)
	@git add pyproject.toml
	@git commit -m "v$$(poetry version -s)"
	@git tag v$$(poetry version -s)
	@git push
	@git push --tags
	@poetry version

init_data:
	poetry run ps

runapp:
	poetry run run.sh
	@echo "Running!!!"

build:
	poetry build
