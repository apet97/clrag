.PHONY: setup crawl preprocess chunk embed hybrid serve test clean help all import-langchain reindex-langchain

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
PYTEST := $(VENV)/bin/pytest

help:
	@echo "Clockify + LangChain RAG Stack - Advanced Multi-Corpus Setup"
	@echo ""
	@echo "Targets:"
	@echo "  make setup            - Create venv and install dependencies"
	@echo "  make crawl            - Scrape Clockify help (configurable in .env)"
	@echo "  make preprocess       - Extract and clean HTML → Markdown"
	@echo "  make import-langchain - Import pre-scraped LangChain markdown"
	@echo "  make chunk            - Split markdown into parent-child chunks (all namespaces)"
	@echo "  make embed            - Build multi-namespace FAISS indexes"
	@echo "  make hybrid           - Build BM25 full-text indexes"
	@echo "  make serve            - Start FastAPI server on :7000"
	@echo "  make test             - Run E2E smoke tests"
	@echo "  make clean            - Remove venv, data, indexes"
	@echo ""
	@echo "Quick start (first time):"
	@echo "  1. make setup"
	@echo "  2. cp .env.sample .env && nano .env  # set MODEL_BASE_URL"
	@echo "  3. make crawl preprocess import-langchain chunk embed hybrid"
	@echo "  4. make serve"
	@echo "  5. In another terminal: make test"
	@echo ""
	@echo "Multi-corpus search endpoints:"
	@echo "  curl 'http://localhost:7000/search?q=timesheet&namespace=clockify&k=5'"
	@echo "  curl 'http://localhost:7000/search?q=retrievers&namespace=langchain&k=5'"
	@echo ""
	@echo "Chat with namespaces:"
	@echo "  curl -X POST http://localhost:7000/chat \\"
	@echo "    -H 'Content-Type: application/json' \\"
	@echo "    -d '{\"question\":\"How do I create a project?\",\"namespace\":\"clockify\",\"k\":5}'"

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "✓ Virtual environment ready!"
	@echo "  Activate with: source $(VENV)/bin/activate"

crawl: $(VENV)
	$(PYTHON) -m src.scrape

preprocess: $(VENV)
	$(PYTHON) -m src.preprocess

import-langchain: $(VENV)
	$(PYTHON) -m src.preprocess --import-dir "$${LANGCHAIN_SCRAPED_DIR:=./scraped/markdown_export}" --namespace "$${NAMESPACE_LANGCHAIN:=langchain}"

chunk: $(VENV)
	$(PYTHON) -m src.chunk

embed: $(VENV)
	$(PYTHON) -m src.embed

hybrid: $(VENV)
	$(PYTHON) -m src.hybrid

serve: $(VENV)
	$(UVICORN) src.server:app --host 0.0.0.0 --port 7000 --reload

test: $(VENV)
	$(PYTEST) tests/ -v

clean:
	rm -rf $(VENV) data/raw data/clean data/chunks index/faiss traces __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned up"

all: setup crawl preprocess chunk embed hybrid

.PHONY: $(VENV)
$(VENV):
	@if [ ! -d "$(VENV)" ]; then make setup; fi
