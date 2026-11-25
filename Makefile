.PHONY: init sync test check

init:
	uv sync
	uv run pre-commit install

sync:
	uv sync --all-groups

test:
    uv run pytest

check:
    uv run ruff check
    uv run pytest