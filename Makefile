VENV = .venv
VENV_BIN = $(VENV)/bin
PYTHON = $(VENV_BIN)/python
PIP = $(VENV_BIN)/pip
PYTEST = $(VENV_BIN)/pytest
RUFF = $(VENV_BIN)/ruff

.PHONY: venv install clean lint format download-data test train run-api docker-build docker-run tf-init tf-plan tf-apply tf-destroy

# Regra para criar o ambiente virtual caso não exista
$(VENV)/bin/activate:
	python3 -m venv $(VENV)

venv: $(VENV)/bin/activate

install: venv
	$(PIP) install -e ".[dev]"

download-data:
	bash tools/scripts/download_data.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

lint: venv
	$(RUFF) check .

format: venv
	$(RUFF) format .

test: venv
	PYTHONPATH=. $(PYTEST) tests/ -v

train: venv
	PYTHONPATH=. $(PYTHON) src/models/train_model.py

run-api: venv
	PYTHONPATH=. $(VENV_BIN)/uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t telco-churn-api:latest .

docker-run:
	docker run -p 8000:8000 telco-churn-api:latest

# --- Nuvem AWS (Terraform) ---
tf-init:
	cd terraform && terraform init

tf-plan:
	cd terraform && terraform plan

tf-apply:
	cd terraform && terraform apply -auto-approve

tf-destroy:
	cd terraform && terraform destroy -auto-approve
