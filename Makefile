.PHONY: install test help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test      - Run tests"
	@echo "  make run       - Run the CLI"
	@echo "  make help      - Show this help"

install:
	uv sync
	uv pip install -e .

test:
	PYTHONPATH=src uv run pytest

run:
	uv run my-secretary --help
