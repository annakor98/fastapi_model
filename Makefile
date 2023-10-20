.DEFAULT_GOAL := help
PYTHONPATH = ./
TEST = pytest --verbosity=2 --showlocals --log-level=DEBUG --strict-markers $(arg)
CODE = app tests

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Lint code
		flake8 --jobs 4 --statistics --show-source $(CODE)

.PHONY: test
test: ## Runs pytest with coverage
		$(TEST) --cov