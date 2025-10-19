PYTHON ?= python

serve:
	uvicorn src.server:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-7000}

test-llm:
	$(PYTHON) scripts/test_llm_connection.py

test-rag:
	$(PYTHON) scripts/test_rag_pipeline.py

.PHONY: serve test-llm test-rag
