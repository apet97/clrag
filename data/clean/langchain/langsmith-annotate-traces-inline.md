---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-annotate-traces-inline",
  "h1": "langsmith-annotate-traces-inline",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.454714",
  "sha256_raw": "803a93f4fa0a53d57cce0272edf0b990e54257188961b20ef3f7a44f85787243"
}
---

# langsmith-annotate-traces-inline

> Source: https://docs.langchain.com/langsmith/annotate-traces-inline

You can attach user feedback to ANY intermediate run (span) of the trace, not just the root span.This is useful for critiquing specific parts of the LLM application, such as the retrieval step or generation step of the RAG pipeline.
Annotate
in the upper right corner of trace view for any particular run that is part of the trace.
This will open up a pane that allows you to choose from feedback tags associated with your workspace and add a score for particular tags. You can also add a standalone comment. Follow this guide to set up feedback tags for your workspace.
You can also set up new feedback criteria from within the pane itself.
You can use the labeled keyboard shortcuts to streamline the annotation process.