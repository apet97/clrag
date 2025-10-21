---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-persistence",
  "h1": "oss-python-langgraph-persistence",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.451063",
  "sha256_raw": "dfd958188ea932f686ea4be6464b6b4107c4060f5a9a574a502ca74d3c4710c7"
}
---

# oss-python-langgraph-persistence

> Source: https://docs.langchain.com/oss/python/langgraph/persistence

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
checkpoint
of the graph state at every super-step. Those checkpoints are saved to a thread
, which can be accessed after graph execution. Because threads
allow access to graph’s state after execution, several powerful capabilities including human-in-the-loop, memory, time travel, and fault-tolerance are all possible. Below, we’ll discuss each of these concepts in more detail.
LangGraph API handles checkpointing automatically
When using the LangGraph API, you don’t need to implement or configure checkpointers manually. The API handles all persistence infrastructure for you behind the scenes.
Threads
A thread is a unique ID or thread identifier assigned to each checkpoint saved by a checkpointer. It contains the accumulated state of a sequence of runs. When a run is executed, the state of the underlying graph of the assistant will be persisted to the thread. When invoking a graph with a checkpointer, you must specify athread_id
as part of the configurable
portion of the config.
Checkpoints
The state of a thread at a particular point in time is called a checkpoint. Checkpoint is a snapshot of the graph state saved at each super-step and is represented byStateSnapshot
object with the following key properties:
config
: Config associated with this checkpoint.metadata
: Metadata associated with this checkpoint.values
: Values of the state channels at this point in time.next
A tuple of the node names to execute next in the graph.tasks
: A tuple ofPregelTask
objects that contain information about next tasks to be executed. If the step was previously attempted, it will include error information. If a graph was interrupted dynamically from within a node, tasks will contain additional data associated with interrupts.
- empty checkpoint with
START
as the next node to be executed - checkpoint with the user input
{'foo': '', 'bar': []}
andnode_a
as the next node to be executed - checkpoint with the outputs of
node_a
{'foo': 'a', 'bar': ['a']}
andnode_b
as the next node to be executed - checkpoint with the outputs of
node_b
{'foo': 'b', 'bar': ['a', 'b']}
and no next nodes to be executed
bar
channel values contain outputs from both nodes as we have a reducer for bar
channel.
Get state
When interacting with the saved graph state, you must specify a thread identifier. You can view the latest state of the graph by callinggraph.get_state(config)
. This will return a StateSnapshot
object that corresponds to the latest checkpoint associated with the thread ID provided in the config or a checkpoint associated with a checkpoint ID for the thread, if provided.
get_state
will look like this:
Get state history
You can get the full history of the graph execution for a given thread by callinggraph.get_state_history(config)
. This will return a list of StateSnapshot
objects associated with the thread ID provided in the config. Importantly, the checkpoints will be ordered chronologically with the most recent checkpoint / StateSnapshot
being the first in the list.
get_state_history
will look like this:
Replay
It’s also possible to play-back a prior graph execution. If weinvoke
a graph with a thread_id
and a checkpoint_id
, then we will re-play the previously executed steps before a checkpoint that corresponds to the checkpoint_id
, and only execute the steps after the checkpoint.
thread_id
is the ID of a thread.checkpoint_id
is an identifier that refers to a specific checkpoint within a thread.
configurable
portion of the config:
checkpoint_id
. All of the steps after checkpoint_id
will be executed (i.e., a new fork), even if they have been executed previously. See this how to guide on time-travel to learn more about replaying.
Update state
In addition to re-playing the graph from specificcheckpoints
, we can also edit the graph state. We do this using graph.update_state()
. This method accepts three different arguments:
config
The config should contain thread_id
specifying which thread to update. When only the thread_id
is passed, we update (or fork) the current state. Optionally, if we include checkpoint_id
field, then we fork that selected checkpoint.
values
These are the values that will be used to update the state. Note that this update is treated exactly as any update from a node is treated. This means that these values will be passed to the reducer functions, if they are defined for some of the channels in the graph state. This means that update_state
does NOT automatically overwrite the channel values for every channel, but only for the channels without reducers. Let’s walk through an example.
Let’s assume you have defined the state of your graph with the following schema (see full example above):
foo
key (channel) is completely changed (because there is no reducer specified for that channel, so update_state
overwrites it). However, there is a reducer specified for the bar
key, and so it appends "b"
to the state of bar
.
as_node
The final thing you can optionally specify when calling update_state
is as_node
. If you provided it, the update will be applied as if it came from node as_node
. If as_node
is not provided, it will be set to the last node that updated the state, if not ambiguous. The reason this matters is that the next steps to execute depend on the last node to have given an update, so this can be used to control which node executes next. See this how to guide on time-travel to learn more about forking state.
Memory Store
A state schema specifies a set of keys that are populated as a graph is executed. As discussed above, state can be written by a checkpointer to a thread at each graph step, enabling state persistence. But, what if we want to retain some information across threads? Consider the case of a chatbot where we want to retain specific information about the user across all chat conversations (e.g., threads) with that user! With checkpointers alone, we cannot share information across threads. This motivates the need for theStore
interface. As an illustration, we can define an InMemoryStore
to store information about a user across threads. We simply compile our graph with a checkpointer, as before, and with our new in_memory_store
variable.
LangGraph API handles stores automatically
When using the LangGraph API, you don’t need to implement or configure stores manually. The API handles all storage infrastructure for you behind the scenes.
Basic Usage
First, let’s showcase this in isolation without using LangGraph.tuple
, which in this specific example will be (<user_id>, "memories")
. The namespace can be any length and represent anything, does not have to be user specific.
store.put
method to save memories to our namespace in the store. When we do this, we specify the namespace, as defined above, and a key-value pair for the memory: the key is simply a unique identifier for the memory (memory_id
) and the value (a dictionary) is the memory itself.
store.search
method, which will return all memories for a given user as a list. The most recent memory is the last in the list.
Item
) with certain attributes. We can access it as a dictionary by converting via .dict
as above.
The attributes it has are:
value
: The value (itself a dictionary) of this memorykey
: A unique key for this memory in this namespacenamespace
: A list of strings, the namespace of this memory typecreated_at
: Timestamp for when this memory was createdupdated_at
: Timestamp for when this memory was updated
Semantic Search
Beyond simple retrieval, the store also supports semantic search, allowing you to find memories based on meaning rather than exact matches. To enable this, configure the store with an embedding model:fields
parameter or by specifying the index
parameter when storing memories:
Using in LangGraph
With this all in place, we use thein_memory_store
in LangGraph. The in_memory_store
works hand-in-hand with the checkpointer: the checkpointer saves state to threads, as discussed above, and the in_memory_store
allows us to store arbitrary information for access across threads. We compile the graph with both the checkpointer and the in_memory_store
as follows.
thread_id
, as before, and also with a user_id
, which we’ll use to namespace our memories to this particular user as we showed above.
in_memory_store
and the user_id
in any node by passing store: BaseStore
and config: RunnableConfig
as node arguments. Here’s how we might use semantic search in a node to find relevant memories:
store.search
method to get memories. Recall the memories are returned as a list of objects that can be converted to a dictionary.
user_id
is the same.
langgraph.json
file. For example:
Checkpointer libraries
Under the hood, checkpointing is powered by checkpointer objects that conform to BaseCheckpointSaver interface. LangGraph provides several checkpointer implementations, all implemented via standalone, installable libraries:langgraph-checkpoint
: The base interface for checkpointer savers (BaseCheckpointSaver) and serialization/deserialization interface (SerializerProtocol
). Includes in-memory checkpointer implementation (InMemorySaver
) for experimentation. LangGraph comes withlanggraph-checkpoint
included.langgraph-checkpoint-sqlite
: An implementation of LangGraph checkpointer that uses SQLite database (SqliteSaver
/AsyncSqliteSaver
). Ideal for experimentation and local workflows. Needs to be installed separately.langgraph-checkpoint-postgres
: An advanced checkpointer that uses Postgres database (PostgresSaver
/AsyncPostgresSaver
), used in LangSmith. Ideal for using in production. Needs to be installed separately.
Checkpointer interface
Each checkpointer conforms to BaseCheckpointSaver interface and implements the following methods:.put
- Store a checkpoint with its configuration and metadata..put_writes
- Store intermediate writes linked to a checkpoint (i.e. pending writes)..get_tuple
- Fetch a checkpoint tuple using for a given configuration (thread_id
andcheckpoint_id
). This is used to populateStateSnapshot
ingraph.get_state()
..list
- List checkpoints that match a given configuration and filter criteria. This is used to populate state history ingraph.get_state_history()
.ainvoke
, .astream
, .abatch
), asynchronous versions of the above methods will be used (.aput
, .aput_writes
, .aget_tuple
, .alist
).
Serializer
When checkpointers save the graph state, they need to serialize the channel values in the state. This is done using serializer objects.langgraph_checkpoint
defines protocol for implementing serializers provides a default implementation (JsonPlusSerializer) that handles a wide variety of types, including LangChain and LangGraph primitives, datetimes, enums and more.
Serialization with pickle
The default serializer, JsonPlusSerializer
, uses ormsgpack and JSON under the hood, which is not suitable for all types of objects.
If you want to fallback to pickle for objects not currently supported by our msgpack encoder (such as Pandas dataframes),
you can use the pickle_fallback
argument of the JsonPlusSerializer
:
Encryption
Checkpointers can optionally encrypt all persisted state. To enable this, pass an instance ofEncryptedSerializer
to the serde
argument of any BaseCheckpointSaver
implementation. The easiest way to create an encrypted serializer is via from_pycryptodome_aes
, which reads the AES key from the LANGGRAPH_AES_KEY
environment variable (or accepts a key
argument):
LANGGRAPH_AES_KEY
is present, so you only need to provide the environment variable. Other encryption schemes can be used by implementing CipherProtocol
and supplying it to EncryptedSerializer
.