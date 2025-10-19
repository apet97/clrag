# oss-javascript-langgraph-agentic-rag

> Source: https://docs.langchain.com/oss/javascript/langgraph/agentic-rag

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
In this tutorial we will build a retrieval agent using LangGraph. LangChain offers built-in agent implementations, implemented using LangGraph primitives. If deeper customization is required, agents can be implemented directly in LangGraph. This guide demonstrates an example implementation of a retrieval agent. Retrieval agents are useful when you want an LLM to make a decision about whether to retrieve context from a vectorstore or respond to the user directly. By the end of the tutorial we will have done the following:- Fetch and preprocess documents that will be used for retrieval.
- Index those documents for semantic search and create a retriever tool for the agent.
- Build an agentic RAG system that can decide when to use the retriever tool.
Concepts
We will cover the following concepts:- Retrieval using document loaders, text splitters, embeddings, and vector stores
- The LangGraph Graph API, including state, nodes, edges, and conditional edges.
Setup
Let’s download the required packages and set our API keys:1. Preprocess documents
- Fetch documents to use in our RAG system. We will use three of the most recent pages from Lilian Weng’s excellent blog. We’ll start by fetching the content of the pages using
CheerioWebBaseLoader
:
- Split the fetched documents into smaller chunks for indexing into our vectorstore:
2. Create a retriever tool
Now that we have our split documents, we can index them into a vector store that we’ll use for semantic search.- Use an in-memory vector store and OpenAI embeddings:
- Create a retriever tool using LangChain’s prebuilt
createRetrieverTool
:
3. Generate query
Now we will start building components (nodes and edges) for our agentic RAG graph.- Build a
generateQueryOrRespond
node. It will call an LLM to generate a response based on the current graph state (list of messages). Given the input messages, it will decide to retrieve using the retriever tool, or respond directly to the user. Note that we’re giving the chat model access to thetools
we created earlier via.bindTools
:
- Try it on a random input:
- Ask a question that requires semantic search:
4. Grade documents
- Add a node —
gradeDocuments
— to determine whether the retrieved documents are relevant to the question. We will use a model with structured output using Zod for document grading. We’ll also add a conditional edge —checkRelevance
— that checks the grading result and returns the name of the node to go to (generate
orrewrite
):
- Run this with irrelevant documents in the tool response:
- Confirm that the relevant documents are classified as such:
5. Rewrite question
- Build the
rewrite
node. The retriever tool can return potentially irrelevant documents, which indicates a need to improve the original user question. To do so, we will call therewrite
node:
- Try it out:
6. Generate an answer
- Build
generate
node: if we pass the grader checks, we can generate the final answer based on the original question and the retrieved context:
- Try it:
7. Assemble the graph
Now we’ll assemble all the nodes and edges into a complete graph:- Start with a
generateQueryOrRespond
and determine if we need to call the retriever tool - Route to next step using a conditional edge:
- If
generateQueryOrRespond
returnedtool_calls
, call the retriever tool to retrieve context - Otherwise, respond directly to the user
- If
- Grade retrieved document content for relevance to the question (
gradeDocuments
) and route to next step:- If not relevant, rewrite the question using
rewrite
and then callgenerateQueryOrRespond
again - If relevant, proceed to
generate
and generate final response using the @[ToolMessage
] with the retrieved document context
- If not relevant, rewrite the question using