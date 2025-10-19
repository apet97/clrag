# oss-javascript-langgraph-use-graph-api

> Source: https://docs.langchain.com/oss/javascript/langgraph/use-graph-api

Setup
Installlanggraph
:
Define and update state
Here we show how to define and update state in LangGraph. We will demonstrate:- How to use state to define a graph’s schema
- How to use reducers to control how state updates are processed.
Define state
State in LangGraph can be defined using Zod schemas. Below we will use Zod. See this section for detail on using alternative approaches. By default, graphs will have the same input and output schema, and the state determines that schema. See this section for how to define distinct input and output schemas. Let’s consider a simple example using messages. This represents a versatile formulation of state for many LLM applications. See our concepts page for more detail.Update state
Let’s build an example graph with a single node. Our node is just a TypeScript function that reads our graph’s state and makes updates to it. The first argument to this function will always be the state:- We kicked off invocation by updating a single key of the state.
- We receive the entire state in the invocation result.
Process state updates with reducers
Each key in the state can have its own independent reducer function, which controls how updates from nodes are applied. If no reducer function is explicitly specified then it is assumed that all updates to the key should override it. For Zod state schemas, we can define reducers by using the special.langgraph.reducer()
method on the schema field.
In the earlier example, our node updated the "messages"
key in the state by appending a message to it. Below, we add a reducer to this key, such that updates are automatically appended:
MessagesState
In practice, there are additional considerations for updating lists of messages:- We may wish to update an existing message in the state.
- We may want to accept short-hands for message formats, such as OpenAI format.
MessagesZodMeta
that handles these considerations:
MessagesZodMeta
for convenience, so that we can have:
Define input and output schemas
By default,StateGraph
operates with a single schema, and all nodes are expected to communicate using that schema. However, it’s also possible to define distinct input and output schemas for a graph.
When distinct schemas are specified, an internal schema will still be used for communication between nodes. The input schema ensures that the provided input matches the expected structure, while the output schema filters the internal data to return only the relevant information according to the defined output schema.
Below, we’ll see how to define distinct input and output schema.
Pass private state between nodes
In some cases, you may want nodes to exchange information that is crucial for intermediate logic but doesn’t need to be part of the main schema of the graph. This private data is not relevant to the overall input/output of the graph and should only be shared between certain nodes. Below, we’ll create an example sequential graph consisting of three nodes (node_1, node_2 and node_3), where private data is passed between the first two steps (node_1 and node_2), while the third step (node_3) only has access to the public overall state.Alternative state definitions
While Zod schemas are the recommended approach, LangGraph also supports other ways to define state schemas:Add runtime configuration
Sometimes you want to be able to configure your graph when calling it. For example, you might want to be able to specify what LLM or system prompt to use at runtime, without polluting the graph state with these parameters. To add runtime configuration:- Specify a schema for your configuration
- Add the configuration to the function signature for nodes or conditional edges
- Pass the configuration into the graph.
Extended example: specifying LLM at runtime
Extended example: specifying LLM at runtime
Extended example: specifying model and system message at runtime
Extended example: specifying model and system message at runtime
Add retry policies
There are many use cases where you may wish for your node to have a custom retry policy, for example if you are calling an API, querying a database, or calling an LLM, etc. LangGraph lets you add retry policies to nodes. To configure a retry policy, pass theretryPolicy
parameter to the addNode. The retryPolicy
parameter takes in a RetryPolicy
object. Below we instantiate a RetryPolicy
object with the default parameters and associate it with a node:
TypeError
SyntaxError
ReferenceError
Extended example: customizing retry policies
Extended example: customizing retry policies
Create a sequence of steps
Here we demonstrate how to construct a simple sequence of steps. We will show:- How to build a sequential graph
- Built-in short-hand for constructing similar graphs.
.addNode
and .addEdge
methods of our graph:
Why split application steps into a sequence with LangGraph?
Why split application steps into a sequence with LangGraph?
- How state updates are checkpointed
- How interruptions are resumed in human-in-the-loop workflows
- How we can “rewind” and branch-off executions using LangGraph’s time travel features
- Populate a value in a key of the state
- Update the same value
- Populate a different value
.addNode
:.addEdge
takes the names of nodes, which for functions defaults tonode.name
.- We must specify the entry point of the graph. For this we add an edge with the START node.
- The graph halts when there are no more nodes to execute.
- We kicked off invocation by providing a value for a single state key. We must always provide a value for at least one key.
- The value we passed in was overwritten by the first node.
- The second node updated the value.
- The third node populated a different value.
Create branches
Parallel execution of nodes is essential to speed up overall graph operation. LangGraph offers native support for parallel execution of nodes, which can significantly enhance the performance of graph-based workflows. This parallelization is achieved through fan-out and fan-in mechanisms, utilizing both standard edges and conditional_edges. Below are some examples showing how to add create branching dataflows that work for you.Run graph nodes in parallel
In this example, we fan out fromNode A
to B and C
and then fan in to D
. With our state, we specify the reducer add operation. This will combine or accumulate values for the specific key in the State, rather than simply overwriting the existing value. For lists, this means concatenating the new list with the existing list. See the above section on state reducers for more detail on updating state with reducers.
"b"
and "c"
are executed concurrently in the same superstep. Because they are in the same step, node "d"
executes after both "b"
and "c"
are finished.Importantly, updates from a parallel superstep may not be ordered consistently. If you need a consistent, predetermined ordering of updates from a parallel superstep, you should write the outputs to a separate field in the state together with a value with which to order them.Exception handling?
Exception handling?
- You can write regular python code within your node to catch and handle exceptions.
- You can set a retry_policy to direct the graph to retry nodes that raise certain types of exceptions. Only failing branches are retried, so you needn’t worry about performing redundant work.
Conditional branching
If your fan-out should vary at runtime based on the state, you can use addConditionalEdges to select one or more paths using the graph state. See example below, where nodea
generates a state update that determines the following node.
Map-Reduce and the Send API
LangGraph supports map-reduce and other advanced branching patterns using the Send API. Here is an example of how to use it:Create and control loops
When creating a graph with a loop, we require a mechanism for terminating execution. This is most commonly done by adding a conditional edge that routes to the END node once we reach some termination condition. You can also set the graph recursion limit when invoking or streaming the graph. The recursion limit sets the number of supersteps that the graph is allowed to execute before it raises an error. Read more about the concept of recursion limits here. Let’s consider a simple graph with a loop to better understand how these mechanisms work."recursionLimit"
in the config. This will raise a GraphRecursionError
, which you can catch and handle:
"a"
is a tool-calling model, and node "b"
represents the tools.
In our route
conditional edge, we specify that we should end after the "aggregate"
list in the state passes a threshold length.
Invoking the graph, we see that we alternate between nodes "a"
and "b"
before terminating once we reach the termination condition.
Impose a recursion limit
In some applications, we may not have a guarantee that we will reach a given termination condition. In these cases, we can set the graph’s recursion limit. This will raise aGraphRecursionError
after a given number of supersteps. We can then catch and handle this exception:
Combine control flow and state updates with Command
It can be useful to combine control flow (edges) and state updates (nodes). For example, you might want to BOTH perform state updates AND decide which node to go to next in the SAME node. LangGraph provides a way to do so by returning a Command object from node functions:
StateGraph
with the above nodes. Notice that the graph doesn’t have conditional edges for routing! This is because control flow is defined with Command
inside nodeA
.
ends
to specify which nodes nodeA
can navigate to. This is necessary for the graph rendering and tells LangGraph that nodeA
can navigate to nodeB
and nodeC
.Navigate to a node in a parent graph
If you are using subgraphs, you might want to navigate from a node within a subgraph to a different subgraph (i.e. a different node in the parent graph). To do so, you can specifygraph=Command.PARENT
in Command
:
nodeA
in the above example into a single-node graph that we’ll add as a subgraph to our parent graph.
Command.PARENT
When you send updates from a subgraph node to a parent graph node for a key that’s shared by both parent and subgraph state schemas, you must define a reducer for the key you’re updating in the parent graph state. See the example below.Use inside tools
A common use case is updating graph state from inside a tool. For example, in a customer support application you might want to look up customer information based on their account number or ID in the beginning of the conversation. To update the graph state from the tool, you can returnCommand(update={"my_custom_key": "foo", "messages": [...]})
from the tool:
messages
(or any state key used for the message history) in Command.update
when returning Command
from a tool and the list of messages in messages
MUST contain a ToolMessage
. This is necessary for the resulting message history to be valid (LLM providers require AI messages with tool calls to be followed by the tool result messages).Command
, we recommend using prebuilt ToolNode
which automatically handles tools returning Command
objects and propagates them to the graph state. If you’re writing a custom node that calls tools, you would need to manually propagate Command
objects returned by the tools as the update from the node.
Visualize your graph
Here we demonstrate how to visualize the graphs you create. You can visualize any arbitrary Graph, including StateGraph. Let’s create a simple example graph to demonstrate visualization.Mermaid
We can also convert a graph class into Mermaid syntax.PNG
If preferred, we could render the Graph into a.png
. This uses the Mermaid.ink API to generate the diagram.