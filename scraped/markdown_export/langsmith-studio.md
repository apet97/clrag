# langsmith-studio

> Source: https://docs.langchain.com/langsmith/studio

Studio is a specialized agent IDE that enables visualization, interaction, and debugging of agentic systems that implement the LangGraph Server API protocol. Studio also integrates with tracing, evaluation, and prompt engineering.
Graph mode exposes the full feature-set and is useful when you would like as many details about the execution of your agent, including the nodes traversed, intermediate states, and LangSmith integrations (such as adding to datasets and playground).
Chat mode is a simpler UI for iterating on and testing chat-specific agents. It is useful for business users and those who want to test overall agent behavior. Chat mode is only supported for graph’s whose state includes or extends MessagesState.