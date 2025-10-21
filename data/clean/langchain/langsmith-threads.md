---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-threads",
  "h1": "langsmith-threads",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.472212",
  "sha256_raw": "f01c9aad74125374a94a6353401d192275568893d0237e71be61866c04f29fab"
}
---

# langsmith-threads

> Source: https://docs.langchain.com/langsmith/threads

Many LLM applications have a chatbot-like interface in which the user and the LLM application engage in a multi-turn conversation. In order to track these conversations, you can use the
Threads
feature in LangSmith.
Group traces into threads
AThread
is a sequence of traces representing a single conversation. Each response is represented as its own trace, but these traces are linked together by being part of the same thread.
To associate traces together, you need to pass in a special metadata
key where the value is the unique identifier for that thread.
The key value is the unique identifier for that conversation.
The key name should be one of:
session_id
thread_id
conversation_id
.
f47ac10b-58cc-4372-a567-0e02b2c3d479
.
Code example
This example demonstrates how to log and retrieve conversation history from LangSmith to maintain long-running chats. You can add metadata to your traces in LangSmith in a variety of ways, this code will show how to do so dynamically, but read the previously linked guide to learn about all the ways you can add thread identifier metadata to your traces.getChatHistory: true
,
you can continue the conversation from where it left off. This means that the LLM will receive the entire message history and respond to it,
instead of just responding to the latest message.
View threads
You can view threads by clicking on theThreads
tab in any project details page. You will then see a list of all threads, sorted by the most recent activity.
You can then click into a particular thread. This will open the history for a particular thread. If your threads are formatted as chat messages, you will a chatbot-like UI where you can see a history of inputs and outputs.
You can open up the trace or annotate the trace in a side panel by clicking on Annotate
and Open trace
, respectively.