# oss-javascript-integrations-retrievers-index

> Source: https://docs.langchain.com/oss/javascript/integrations/retrievers/index

A retriever is an interface that returns documents given an unstructured query.
It is more general than a vector store.
A retriever does not need to be able to store documents, only to return (or retrieve) them.Retrievers accept a string query as input and return a list of Documents.For specifics on how to use retrievers, see the relevant how-to guides here.Note that all vector stores can be cast to retrievers.
Refer to the vector store integration docs for available vector store retrievers.