# langsmith-use-remote-graph

> Source: https://docs.langchain.com/langsmith/use-remote-graph

RemoteGraph
is a client-side interface that allows you to interact with your deployment as if it were a local graph. It provides API parity with CompiledGraph
, which means that you can use the same methods (invoke()
, stream()
, get_state()
, etc.) in your development and production environments. This page describes how to initialize a RemoteGraph
and interact with it.
RemoteGraph
is useful for the following:
- Separation of development and deployment: Build and test a graph locally with
CompiledGraph
, deploy it to LangSmith, and then useRemoteGraph
to call it in production while working with the same API interface. - Thread-level persistence: Persist and fetch the state of a conversation across calls with a thread ID.
- Subgraph embedding: Compose modular graphs for a multi-agent workflow by embedding a
RemoteGraph
as a subgraph within another graph. - Reusable workflows: Use deployed graphs as nodes or tools, so that you can reuse and expose complex logic.
Important: Avoid calling the same deployment
RemoteGraph
is designed to call graphs on other deployments. Do not use RemoteGraph
to call itself or another graph on the same deployment, as this can lead to deadlocks and resource exhaustion. Instead, use local graph composition or subgraphs for graphs within the same deployment.Prerequisites
Before getting started withRemoteGraph
, make sure you have:
- Access to LangSmith, where your graphs are developed and managed.
- A running LangGraph Server, which hosts your deployed graphs for remote interaction.
Initialize the graph
When initializing aRemoteGraph
, you must always specify:
name
: The name of the graph you want to interact with or an assistant ID. If you specify a graph name, the default assistant will be used. If you specify an assistant ID, that specific assistant will be used. The graph name is the same name you use in thelanggraph.json
configuration file for your deployment.api_key
: A valid LangSmith API key. You can set as an environment variable (LANGSMITH_API_KEY
) or pass directly in theapi_key
argument. You can also provide the API key in theclient
/sync_client
arguments, ifLangGraphClient
/SyncLangGraphClient
was initialized with theapi_key
argument.
url
: The URL of the deployment you want to interact with. If you pass theurl
argument, both sync and async clients will be created using the provided URL, headers (if provided), and default configuration values (e.g., timeout).client
: ALangGraphClient
instance for interacting with the deployment asynchronously (e.g., using.astream()
,.ainvoke()
,.aget_state()
,.aupdate_state()
).sync_client
: ASyncLangGraphClient
instance for interacting with the deployment synchronously (e.g., using.stream()
,.invoke()
,.get_state()
,.update_state()
).
If you pass both
client
or sync_client
as well as the url
argument, they will take precedence over the url
argument. If none of the client
/ sync_client
/ url
arguments are provided, RemoteGraph
will raise a ValueError
at runtime.Use a URL
Use a client
Invoke the graph
RemoteGraph
implements the same Runnable interface as CompiledGraph
, so you can use it in the same way as a compiled graph. It supports the full set of standard methods, including .invoke()
, .stream()
, .get_state()
, and .update_state()
, as well as their asynchronous variants.
Asynchronously
To use the graph asynchronously, you must provide either the
url
or client
when initializing the RemoteGraph
.Synchronously
To use the graph synchronously, you must provide either the
url
or sync_client
when initializing the RemoteGraph
.Persist state at the thread level
By default, graph runs (for example, calls made with.invoke()
or .stream()
) are stateless, which means that intermediate checkpoints and the final state are not persisted after a run.
If you want to preserve the outputs of a run—for example, to support human-in-the-loop workflows—you can create a thread and pass its ID through the config
argument. This works the same way as with a regular compiled graph:
Use as a subgraph
If you need to use a
checkpointer
with a graph that has a RemoteGraph
subgraph node, make sure to use UUIDs as thread IDs.RemoteGraph
instances as subgraph nodes. This allows for modular, scalable workflows where different responsibilities are split across separate graphs.
RemoteGraph
exposes the same interface as a regular CompiledGraph
, so you can use it directly as a subgraph inside another graph. For example: