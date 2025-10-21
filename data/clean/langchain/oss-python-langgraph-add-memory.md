---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-add-memory",
  "h1": "oss-python-langgraph-add-memory",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.477837",
  "sha256_raw": "a14d6f607cd2513727f167dc3701f8077e9a38f6cdcfca9b8285cb760919bf2e"
}
---

# oss-python-langgraph-add-memory

> Source: https://docs.langchain.com/oss/python/langgraph/add-memory

- Add short-term memory as a part of your agent’s state to enable multi-turn conversations.
- Add long-term memory to store user-specific or application-level data across sessions.
Add short-term memory
Short-term memory (thread-level persistence) enables agents to track multi-turn conversations. To add short-term memory:Use in production
In production, use a checkpointer backed by a database:Example: using Postgres checkpointer
Example: using Postgres checkpointer
checkpointer.setup()
the first time you’re using Postgres checkpointer- Sync
- Async
Example: using [MongoDB](https://pypi.org/project/langgraph-checkpoint-mongodb/) checkpointer
Example: using [MongoDB](https://pypi.org/project/langgraph-checkpoint-mongodb/) checkpointer
Example: using [Redis](https://pypi.org/project/langgraph-checkpoint-redis/) checkpointer
Example: using [Redis](https://pypi.org/project/langgraph-checkpoint-redis/) checkpointer
checkpointer.setup()
the first time you’re using Redis checkpointer- Sync
- Async
Use in subgraphs
If your graph contains subgraphs, you only need to provide the checkpointer when compiling the parent graph. LangGraph will automatically propagate the checkpointer to the child subgraphs.Add long-term memory
Use long-term memory to store user-specific or application-specific data across conversations.Use in production
In production, use a store backed by a database:Example: using Postgres store
Example: using Postgres store
store.setup()
the first time you’re using Postgres store- Sync
- Async
Example: using [Redis](https://pypi.org/project/langgraph-checkpoint-redis/) store
Example: using [Redis](https://pypi.org/project/langgraph-checkpoint-redis/) store
store.setup()
the first time you’re using Redis store- Sync
- Async
Use semantic search
Enable semantic search in your graph’s memory store to let graph agents search for items in the store by semantic similarity.Long-term memory with semantic search
Long-term memory with semantic search
Manage short-term memory
With short-term memory enabled, long conversations can exceed the LLM’s context window. Common solutions are:- Trim messages: Remove first or last N messages (before calling LLM)
- Delete messages from LangGraph state permanently
- Summarize messages: Summarize earlier messages in the history and replace them with a summary
- Manage checkpoints to store and retrieve message history
- Custom strategies (e.g., message filtering, etc.)
Trim messages
Most LLMs have a maximum supported context window (denominated in tokens). One way to decide when to truncate messages is to count the tokens in the message history and truncate whenever it approaches that limit. If you’re using LangChain, you can use the trim messages utility and specify the number of tokens to keep from the list, as well as thestrategy
(e.g., keep the last max_tokens
) to use for handling the boundary.
To trim message history, use the trim_messages
function:
Full example: trim messages
Full example: trim messages
Delete messages
You can delete messages from the graph state to manage the message history. This is useful when you want to remove specific messages or clear the entire message history. To delete messages from the graph state, you can use theRemoveMessage
. For RemoveMessage
to work, you need to use a state key with add_messages
reducer, like MessagesState
.
To remove specific messages:
- some providers expect message history to start with a
user
message - most providers require
assistant
messages with tool calls to be followed by correspondingtool
result messages.
Full example: delete messages
Full example: delete messages
Summarize messages
The problem with trimming or removing messages, as shown above, is that you may lose information from culling of the message queue. Because of this, some applications benefit from a more sophisticated approach of summarizing the message history using a chat model. Prompting and orchestration logic can be used to summarize the message history. For example, in LangGraph you can extend theMessagesState
to include a summary
key:
summarize_conversation
node can be called after some number of messages have accumulated in the messages
state key.
Full example: summarize messages
Full example: summarize messages
- We will keep track of our running summary in the
context
field
SummarizationNode
).- Define private state that will be used only for filtering
call_model
node.- We’re passing a private input state here to isolate the messages returned by the summarization node
Manage checkpoints
You can view and delete the information stored by the checkpointer.View thread state
- Graph/Functional API
- Checkpointer API
View the history of the thread
- Graph/Functional API
- Checkpointer API