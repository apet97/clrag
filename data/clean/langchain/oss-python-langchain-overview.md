---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-overview",
  "h1": "oss-python-langchain-overview",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.451331",
  "sha256_raw": "99177d0420d214019f6fe8774cc378a4b75c7a7fdebe3a7d9ceb40807aa291e8"
}
---

# oss-python-langchain-overview

> Source: https://docs.langchain.com/oss/python/langchain/overview

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Install
Create an agent
Core benefits
Standard model interface
Different providers have unique APIs for interacting with models, including the format of responses. LangChain standardizes how you interact with models so that you can seamlessly swap providers and avoid lock-in.
Easy to use, highly flexible agent
LangChain’s agent abstraction is designed to be easy to get started with, letting you build a simple agent in under 10 lines of code. But it also provides enough flexibility to allow you to do all the context engineering your heart desires.
Built on top of LangGraph
LangChain’s agents are built on top of LangGraph. This allows us to take advantage of LangGraph’s durable execution, human-in-the-loop support, persistence, and more.
Debug with LangSmith
Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.