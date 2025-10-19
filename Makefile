PYTHON ?= python

serve:
	uvicorn src.server:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-7000}

test-llm:
	$(PYTHON) scripts/test_llm_connection.py

test-rag:
	$(PYTHON) scripts/test_rag_pipeline.py

eval:
	@echo "Running retrieval eval (hit@k) tests..."
	SKIP_API_EVAL=false API_HOST=localhost API_PORT=7000 $(PYTHON) -m pytest tests/test_clockify_rag_eval.py::test_eval_report -v -s

eval-full:
	@echo "Running full retrieval eval suite..."
	SKIP_API_EVAL=false API_HOST=localhost API_PORT=7000 $(PYTHON) -m pytest tests/test_clockify_rag_eval.py -v

eval-health:
	@echo "Checking API health..."
	@curl -s http://localhost:7000/health | $(PYTHON) -m json.tool

eval-glossary:
	@echo "Running glossary and hybrid retrieval evaluation..."
	$(PYTHON) scripts/eval_rag.py

.PHONY: serve test-llm test-rag eval eval-full eval-health eval-glossary
