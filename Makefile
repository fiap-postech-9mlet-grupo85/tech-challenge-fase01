.PHONY: install clean lint format download-data test train

install:
	pip install -e ".[dev]"

download-data:
	bash tools/scripts/download_data.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

lint:
	ruff check .

format:
	ruff format .

test:
	PYTHONPATH=. pytest tests/ -v

train:
	PYTHONPATH=. python src/models/train_model.py
