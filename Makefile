.PHONY: install clean lint format test run

install:
	pip install -e ".[dev]"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

lint:
	ruff check .

format:
	ruff format .

test:
	pytest tests/

run:
	uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
