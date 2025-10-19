# oss-python-langchain-long-term-memory

> Source: https://docs.langchain.com/oss/python/langchain/long-term-memory

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
LangChain agents use LangGraph persistence to enable long-term memory. This is a more advanced topic and requires knowledge of LangGraph to use.Memory storage
LangGraph stores long-term memories as JSON documents in a store. Each memory is organized under a customnamespace
(similar to a folder) and a distinct key
(like a file name). Namespaces often include user or org IDs or other labels that makes it easier to organize information.
This structure enables hierarchical organization of memories. Cross-namespace searching is then supported through content filters.
Read long-term memory in tools
A tool the agent can use to look up user information
Write long-term memory from tools
Example of a tool that updates user information