---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-integrations-retrievers-index",
  "h1": "oss-javascript-integrations-retrievers-index",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.456020",
  "sha256_raw": "cd08bc1b7ee6bedaffc94c3447b356df13617ec26a9572558172c29acef3abd1"
}
---

# oss-javascript-integrations-retrievers-index

> Source: https://docs.langchain.com/oss/javascript/integrations/retrievers/index

A retriever is an interface that returns documents given an unstructured query.
It is more general than a vector store.
A retriever does not need to be able to store documents, only to return (or retrieve) them.Retrievers accept a string query as input and return a list of Documents.For specifics on how to use retrievers, see the relevant how-to guides here.Note that all vector stores can be cast to retrievers.
Refer to the vector store integration docs for available vector store retrievers.