---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-pregel",
  "h1": "oss-python-langgraph-pregel",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.471725",
  "sha256_raw": "9fcef4420979005e91bfdc52106a1bafb1165bb699f4a47d51c5a0a9401a907a"
}
---

# oss-python-langgraph-pregel

> Source: https://docs.langchain.com/oss/python/langgraph/pregel

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Note: The Pregel runtime is named after Google’s Pregel algorithm, which describes an efficient method for large-scale parallel computation using graphs.
Overview
In LangGraph, Pregel combines actors and channels into a single application. Actors read data from channels and write data to channels. Pregel organizes the execution of the application into multiple steps, following the Pregel Algorithm/Bulk Synchronous Parallel model. Each step consists of three phases:- Plan: Determine which actors to execute in this step. For example, in the first step, select the actors that subscribe to the special input channels; in subsequent steps, select the actors that subscribe to channels updated in the previous step.
- Execution: Execute all selected actors in parallel, until all complete, or one fails, or a timeout is reached. During this phase, channel updates are invisible to actors until the next step.
- Update: Update the channels with the values written by the actors in this step.
Actors
An actor is aPregelNode
. It subscribes to channels, reads data from them, and writes data to them. It can be thought of as an actor in the Pregel algorithm. PregelNodes
implement LangChain’s Runnable interface.
Channels
Channels are used to communicate between actors (PregelNodes). Each channel has a value type, an update type, and an update function – which takes a sequence of updates and modifies the stored value. Channels can be used to send data from one chain to another, or to send data from a chain to itself in a future step. LangGraph provides a number of built-in channels:- LastValue: The default channel, stores the last value sent to the channel, useful for input and output values, or for sending data from one step to the next.
- Topic: A configurable PubSub Topic, useful for sending multiple values between actors, or for accumulating output. Can be configured to deduplicate values or to accumulate values over the course of multiple steps.
- BinaryOperatorAggregate: stores a persistent value, updated by applying a binary operator to the current value and each update sent to the channel, useful for computing aggregates over multiple steps; e.g.,
total = BinaryOperatorAggregate(int, operator.add)
Examples
While most users will interact with Pregel through the StateGraph API or the entrypoint decorator, it is possible to interact with Pregel directly. Below are a few different examples to give you a sense of the Pregel API.- Single node
- Multiple nodes
- Topic
- BinaryOperatorAggregate
- Cycle
High-level API
LangGraph provides two high-level APIs for creating a Pregel application: the StateGraph (Graph API) and the Functional API.- StateGraph (Graph API)
- Functional API
The StateGraph (Graph API) is a higher-level abstraction that simplifies the creation of Pregel applications. It allows you to define a graph of nodes and edges. When you compile the graph, the StateGraph API automatically creates the Pregel application for you.The compiled Pregel instance will be associated with a list of nodes and channels. You can inspect the nodes and channels by printing them.You will see something like this:You should see something like this