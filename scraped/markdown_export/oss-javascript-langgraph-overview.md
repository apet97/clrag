# oss-javascript-langgraph-overview

> Source: https://docs.langchain.com/oss/javascript/langgraph/overview

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Install
Core benefits
LangGraph provides low-level supporting infrastructure for any long-running, stateful workflow or agent. LangGraph does not abstract prompts or architecture, and provides the following central benefits:- Durable execution: Build agents that persist through failures and can run for extended periods, resuming from where they left off.
- Human-in-the-loop: Incorporate human oversight by inspecting and modifying agent state at any point.
- Comprehensive memory: Create stateful agents with both short-term working memory for ongoing reasoning and long-term memory across sessions.
- Debugging with LangSmith: Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
- Production-ready deployment: Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.
LangGraph ecosystem
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents. To improve your LLM application development, pair LangGraph with:- LangSmith — Helpful for agent evals and observability. Debug poor-performing LLM app runs, evaluate agent trajectories, gain visibility in production, and improve performance over time.
- LangSmith — Deploy and scale agents effortlessly with a purpose-built deployment platform for long running, stateful workflows. Discover, reuse, configure, and share agents across teams — and iterate quickly with visual prototyping in Studio.
- LangChain - Provides integrations and composable components to streamline LLM application development. Contains agent abstractions built on top of LangGraph.