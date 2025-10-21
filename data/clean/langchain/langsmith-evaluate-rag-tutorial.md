---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-evaluate-rag-tutorial",
  "h1": "langsmith-evaluate-rag-tutorial",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.433425",
  "sha256_raw": "3d6c489c2122fd870e98c6915e5e2fbb2af1a2a0ff1b9cc271c1fb42f9b8099a"
}
---

# langsmith-evaluate-rag-tutorial

> Source: https://docs.langchain.com/langsmith/evaluate-rag-tutorial

- How to create test datasets
- How to run your RAG application on those datasets
- How to measure your application’s performance using different evaluation metrics
Overview
A typical RAG evaluation workflow consists of three main steps:- Creating a dataset with questions and their expected answers
- Running your RAG application on those questions
-
Using evaluators to measure how well your application performed, looking at factors like:
- Answer relevance
- Answer accuracy
- Retrieval quality
Setup
Environment
First, let’s set our environment variables:Application
While this tutorial uses LangChain, the evaluation techniques and LangSmith functionality demonstrated here work with any framework. Feel free to use your preferred tools and libraries.
- Indexing: chunks and indexes a few of Lilian Weng’s blogs in a vector store
- Retrieval: retrieves those chunks based on the user question
- Generation: passes the question and retrieved docs to an LLM.
Indexing and retrieval
First, lets load the blog posts we want to build a chatbot for and index them.Generation
We can now define the generative pipeline.Dataset
Now that we’ve got our application, let’s build a dataset to evaluate it. Our dataset will be very simple in this case: we’ll have example questions and reference answers.Evaluators
One way to think about different types of RAG evaluators is as a tuple of what is being evaluated X what its being evaluated against:- Correctness: Response vs reference answer
Goal
: Measure “how similar/correct is the RAG chain answer, relative to a ground-truth answer”Mode
: Requires a ground truth (reference) answer supplied through a datasetEvaluator
: Use LLM-as-judge to assess answer correctness.
- Relevance: Response vs input
Goal
: Measure “how well does the generated response address the initial user input”Mode
: Does not require reference answer, because it will compare the answer to the input questionEvaluator
: Use LLM-as-judge to assess answer relevance, helpfulness, etc.
- Groundedness: Response vs retrieved docs
Goal
: Measure “to what extent does the generated response agree with the retrieved context”Mode
: Does not require reference answer, because it will compare the answer to the retrieved contextEvaluator
: Use LLM-as-judge to assess faithfulness, hallucinations, etc.
- Retrieval relevance: Retrieved docs vs input
Goal
: Measure “how relevant are my retrieved results for this query”Mode
: Does not require reference answer, because it will compare the question to the retrieved contextEvaluator
: Use LLM-as-judge to assess relevance
Correctness: Response vs reference answer
Relevance: Response vs input
The flow is similar to above, but we simply look at theinputs
and outputs
without needing the reference_outputs
. Without a reference answer we can’t grade accuracy, but can still grade relevance—as in, did the model address the user’s question or not.
Groundedness: Response vs retrieved docs
Another useful way to evaluate responses without needing reference answers is to check if the response is justified by (or “grounded in”) the retrieved documents.Retrieval relevance: Retrieved docs vs input
Run evaluation
We can now kick off our evaluation job with all of our different evaluators.Reference code
Here's a consolidated script with all the above code:
Here's a consolidated script with all the above code: