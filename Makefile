# provide ENV=dev to use .env.dev instead of .env
ENV_LOADED :=

ifeq ($(ENV), prod)
    ifneq (,$(wildcard ./.env))
        include .env
        export
				ENV_LOADED := Loaded config from .env
    endif
else
    ifneq (,$(wildcard ./.env.dev))
        include .env.dev
        export
				ENV_LOADED := Loaded config from .env.dev
    endif
endif

.PHONY: help
.DEFAULT_GOAL := help

help: ## get a list of all the targets, and their short descriptions
	@# source for the incantation: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[1;38;5;214m%-12s\033[0m %s\n", $$1, $$2}'

environment: ## installs required environment for deployment and corpus generation
	@if [ -z "$(ENV_LOADED)" ]; then \
			echo "Error: Configuration file not found" >&2; \
			exit 1; \
    else \
			echo "$(ENV_LOADED)"; \
	fi
	python -m pip install -qqq -r requirements.txt

run-huberman-etl: environment
	python -m etl.huberman_lab

run-fridman-etl: environment
	python -m etl.lex_fridman

chat: environment
	python cli_chat.py
