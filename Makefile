.PHONY: help install install-tools install-dev install-wheel submodules check ci-check test test-verbose lint lint-fix format format-check type-check build check-build check-install wheels publish-test publish ci-publish validate-version release-metadata release-select-commit release docs docs-serve examples-check notebooks-check hooks-check clean
.DEFAULT_GOAL := help

# Prefer the existing environment; CI and callers may override explicitly.
PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,$(if $(wildcard .venv/Scripts/python.exe),.venv/Scripts/python.exe,python))
INSTALL_ARGS ?=
TEST_PATH ?= tests/
PYTEST_ARGS ?=
VALIDATE_VERSION_ARGS ?= --offline
TWINE_UPLOAD_ARGS ?=
CHECK ?= test
CHECK_BUILD_ARGS ?=
GROUP ?= dev
INSTALL_HOOKS ?= 1
WHEEL_ARGS ?=
export PYTHON VALIDATE_VERSION_ARGS

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-24s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

submodules: ## Initialize the pinned upstream dependency (without SFML)
	git submodule update --init external/agent-harmony

install: ## Install an editable native build
	$(PYTHON) -m pip install -e . $(INSTALL_ARGS)

install-tools: ## Install tools only (override GROUP, defaults to dev)
	$(PYTHON) -m pip install 'pip>=25.1'
	$(PYTHON) -m pip install --group $(GROUP)

install-dev: install-tools ## Install editable package and development dependency groups
	$(PYTHON) -m pip install --no-build-isolation -e . $(INSTALL_ARGS)
ifeq ($(INSTALL_HOOKS),1)
	$(PYTHON) -m pre_commit install
endif

install-wheel: ## Install a compatible wheel from dist without compiling
	$(PYTHON) -m pip install --no-index --no-deps --only-binary=:all: --find-links dist agent-harmony

check: lint format-check type-check test validate-version docs examples-check notebooks-check hooks-check ## Run local quality checks without publishing

ci-check: ## Run a check with a CI summary
	@bash scripts/ci/run_check.sh "$(CHECK)"

test: ## Run tests (override TEST_PATH or PYTEST_ARGS to select)
	$(PYTHON) -m pytest $(TEST_PATH) $(PYTEST_ARGS)

test-verbose: ## Run tests with verbose output
	$(PYTHON) -m pytest $(TEST_PATH) $(PYTEST_ARGS) -v

lint: ## Check Python lint rules
	$(PYTHON) -m ruff check src/ tests/ scripts/ examples/

lint-fix: ## Apply Python lint fixes
	$(PYTHON) -m ruff check --fix src/ tests/ scripts/ examples/

format: ## Format Python code
	$(PYTHON) -m ruff format src/ tests/ scripts/ examples/

format-check: ## Check Python formatting
	$(PYTHON) -m ruff format --diff src/ tests/ scripts/ examples/

type-check: ## Run strict Python type checks
	$(PYTHON) -m mypy src/agent_harmony/ tests/ scripts/ examples/

build: ## Build an sdist, then build its wheel
	$(PYTHON) -m build

check-build: ## Check distribution metadata and archive contents
	$(PYTHON) -m twine check dist/*
	$(PYTHON) scripts/check_dist.py $(CHECK_BUILD_ARGS)

check-install: ## Verify wheel installation and offline sdist rebuilding
	$(PYTHON) scripts/check_install.py

wheels: ## Build and test platform wheels with cibuildwheel
	$(PYTHON) -m cibuildwheel --output-dir wheelhouse $(WHEEL_ARGS)

publish-test: ## Upload distributions to TestPyPI (publishing operation)
	$(PYTHON) -m twine upload --repository testpypi $(TWINE_UPLOAD_ARGS) dist/*

publish: ## Upload distributions to PyPI (publishing operation)
	$(PYTHON) -m twine upload $(TWINE_UPLOAD_ARGS) dist/*

ci-publish: ## Upload to PyPI and produce a CI summary (publishing operation)
	@bash scripts/ci/publish.sh

release-metadata: ## Record checkout identity without publishing
	$(PYTHON) scripts/release.py metadata --output "$(or $(RELEASE_METADATA),release-metadata.json)"

release-select-commit: ## Select the deployed commit from validated metadata
	$(PYTHON) scripts/release.py select-commit --metadata "$(or $(RELEASE_METADATA),release-metadata.json)"

release: ## Create a GitHub release (publishing operation)
	$(PYTHON) scripts/release.py publish --metadata "$(or $(RELEASE_METADATA),release-metadata.json)" --project "$(or $(RELEASE_PROJECT),.)" --repository "$(or $(RELEASE_REPOSITORY),$(GITHUB_REPOSITORY))"

validate-version: ## Validate installed version and notes (offline by default)
	@bash scripts/validate_version.sh $(VALIDATE_VERSION_ARGS)

docs: ## Build documentation with strict checks
	$(PYTHON) -m mkdocs build --strict

docs-serve: ## Preview documentation locally
	$(PYTHON) -m mkdocs serve --dev-addr 127.0.0.1:8000

examples-check: ## Run the minimal package example
	$(PYTHON) examples/basic_usage.py

notebooks-check: ## Validate saved notebook structure and outputs without executing cells
	@bash scripts/validate_notebooks.sh

hooks-check: ## Validate the pre-commit configuration without installing hooks
	$(PYTHON) -m pre_commit validate-config

clean: ## Remove generated artifacts while preserving sources and .venv
	$(PYTHON) scripts/clean.py
