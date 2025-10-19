# langsmith-observability-quickstart

> Source: https://docs.langchain.com/langsmith/observability-quickstart

Observability is a critical requirement for applications built with large language models (LLMs). LLMs are non-deterministic, which means that the same prompt can produce different responses. This behavior makes debugging and monitoring more challenging than with traditional software.LangSmith addresses this by providing end-to-end visibility into how your application handles a request. Each request generates a trace, which captures the full record of what happened. Within a trace are individual runs, the specific operations your application performed, such as an LLM call or a retrieval step. Tracing runs allows you to inspect, debug, and validate your application’s behavior.In this quickstart, you will set up a minimal Retrieval Augmented Generation (RAG) application and add tracing with LangSmith. You will:
Configure your environment.
Create an application that retrieves context and calls an LLM.
Enable tracing to capture both the retrieval step and the LLM call.
View the resulting traces in the LangSmith UI.
If you prefer to watch a video on getting started with tracing, refer to the quickstart Video guide.
The example app in this quickstart will use OpenAI as the LLM provider. You can adapt the example for your app’s LLM provider.
If you’re building an application with LangChain or LangGraph, you can enable LangSmith tracing with a single environment variable. Get started by reading the guides for tracing with LangChain or tracing with LangGraph.
You can use the example app code outlined in this step to instrument a RAG application. Or, you can use your own application code that includes an LLM call.This is a minimal RAG app that uses the OpenAI SDK directly without any LangSmith tracing added yet. It has three main parts:
Retriever function: Simulates document retrieval that always returns the same string.
OpenAI client: Instantiates a plain OpenAI client to send a chat completion request.
RAG function: Combines the retrieved documents with the user’s question to form a system prompt, calls the chat.completions.create() endpoint with gpt-4o-mini, and returns the assistant’s response.
Add the following code into your app file (e.g., app.py or app.ts):
Copy
from openai import OpenAIdef retriever(query: str): # Minimal example retriever return ["Harrison worked at Kensho"]# OpenAI client call (no wrapping yet)client = OpenAI()def rag(question: str) -> str: docs = retriever(question) system_message = ( "Answer the user's question using only the provided information below:\n" + "\n".join(docs) ) # This call is not traced yet resp = client.chat.completions.create( model="gpt-4o-mini", messages=[ {"role": "system", "content": system_message}, {"role": "user", "content": question}, ], ) return resp.choices[0].message.contentif __name__ == "__main__": print(rag("Where did Harrison work?"))
This snippet wraps the OpenAI client so that every subsequent model call is logged automatically as a traced child run in LangSmith.
Include the highlighted lines in your app file:
Copy
from openai import OpenAIfrom langsmith.wrappers import wrap_openai # traces openai callsdef retriever(query: str): return ["Harrison worked at Kensho"]client = wrap_openai(OpenAI()) # log traces by wrapping the model callsdef rag(question: str) -> str: docs = retriever(question) system_message = ( "Answer the user's question using only the provided information below:\n" + "\n".join(docs) ) resp = client.chat.completions.create( model="gpt-4o-mini", messages=[ {"role": "system", "content": system_message}, {"role": "user", "content": question}, ], ) return resp.choices[0].message.contentif __name__ == "__main__": print(rag("Where did Harrison work?"))
Call your application:
Copy
python app.py
You’ll receive the following output:
Copy
Harrison worked at Kensho.
In the LangSmith UI, navigate to the default Tracing Project for your workspace (or the workspace you specified in Step 2). You’ll see the OpenAI call you just instrumented.
You can also use the traceable decorator for Python or TypeScript to trace your entire application instead of just the LLM calls.
Include the highlighted code in your app file:
Copy
from openai import OpenAIfrom langsmith.wrappers import wrap_openaifrom langsmith import traceabledef retriever(query: str): return ["Harrison worked at Kensho"]client = wrap_openai(OpenAI()) # keep this to capture the prompt and response from the LLM@traceabledef rag(question: str) -> str: docs = retriever(question) system_message = ( "Answer the user's question using only the provided information below:\n" + "\n".join(docs) ) resp = client.chat.completions.create( model="gpt-4o-mini", messages=[ {"role": "system", "content": system_message}, {"role": "user", "content": question}, ], ) return resp.choices[0].message.contentif __name__ == "__main__": print(rag("Where did Harrison work?"))
Call the application again to create a run:
Copy
python app.py
Return to the LangSmith UI, navigate to the default Tracing Project for your workspace (or the workspace you specified in Step 2). You’ll find a trace of the entire app pipeline with the rag step and the ChatOpenAI LLM call.