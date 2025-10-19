# langsmith-attach-user-feedback

> Source: https://docs.langchain.com/langsmith/attach-user-feedback

Child runs
You can attach user feedback to ANY child run of a trace, not just the trace (root run) itself.
This is useful for critiquing specific steps of the LLM application, such as the retrieval step or generation step of a RAG pipeline.
Non-blocking creation (Python only)
The Python client will automatically background feedback creation if you pass
trace_id=
to create_feedback().
This is essential for low-latency environments, where you want to make sure your application isn’t blocked on feedback creation.create_feedback() / createFeedback()
. See this guide for how to get the run ID of an in-progress run.
To learn more about how to filter traces based on various attributes, including user feedback, see this guide.