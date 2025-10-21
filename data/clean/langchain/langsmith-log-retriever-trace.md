---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-log-retriever-trace",
  "h1": "langsmith-log-retriever-trace",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.468272",
  "sha256_raw": "385ca31a76bd1e9be96c2e907018349b5e8b2ee696b67a3b8ef7e7ad5f9506b9"
}
---

# langsmith-log-retriever-trace

> Source: https://docs.langchain.com/langsmith/log-retriever-trace

Nothing will break if you don’t log retriever traces in the correct format and data will still be logged. However, the data will not be rendered in a way that is specific to retriever steps.
Many LLM applications require looking up documents from vector databases, knowledge graphs, or other types of indexes. Retriever traces are a way to log the documents that are retrieved by the retriever. LangSmith provides special rendering for retrieval steps in traces to make it easier to understand and diagnose retrieval issues. In order for retrieval steps to be rendered correctly, a few small steps need to be taken.
-
Annotate the retriever step with
run_type="retriever"
.
-
Return a list of Python dictionaries or TypeScript objects from the retriever step. Each dictionary should contain the following keys:
page_content
: The text of the document.
type
: This should always be “Document”.
metadata
: A python dictionary or TypeScript object containing metadata about the document. This metadata will be displayed in the trace.
The following code snippets show how to log a retrieval steps in Python and TypeScript.
The following image shows how a retriever step is rendered in a trace. The contents along with the metadata are displayed with each document.