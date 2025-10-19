# langsmith-evaluate-graph

> Source: https://docs.langchain.com/langsmith/evaluate-graph

langgraph
is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. Evaluating langgraph
graphs can be challenging because a single invocation can involve many LLM calls, and which LLM calls are made may depend on the outputs of preceding calls. In this guide we will focus on the mechanics of how to pass graphs and graph nodes to evaluate()
/ aevaluate()
. For evaluation techniques and best practices when building agents head to the langgraph docs.
End-to-end evaluations
The most common type of evaluation is an end-to-end one, where we want to evaluate the final graph output for each example input.Define a graph
Lets construct a simple ReACT agent to start:Create a dataset
Let’s create a simple dataset of questions and expected responses:Create an evaluator
And a simple evaluator: Requireslangsmith>=0.2.0
Run evaluations
Now we can run our evaluations and explore the results. We’ll just need to wrap our graph function so that it can take inputs in the format they’re stored on our example:If all of your graph nodes are defined as sync functions then you can use
evaluate
or aevaluate
. If any of you nodes are defined as async, you’ll need to use aevaluate
langsmith>=0.2.0
Evaluating intermediate steps
Often it is valuable to evaluate not only the final output of an agent but also the intermediate steps it has taken. What’s nice aboutlanggraph
is that the output of a graph is a state object that often already carries information about the intermediate steps taken. Usually we can evaluate whatever we’re interested in just by looking at the messages in our state. For example, we can look at the messages to assert that the model invoked the ‘search’ tool upon as a first step.
Requires langsmith>=0.2.0
Running and evaluating individual nodes
Sometimes you want to evaluate a single node directly to save time and costs.langgraph
makes it easy to do this. In this case we can even continue using the evaluators we’ve been using.
Related
Reference code
Click to see a consolidated code snippet
Click to see a consolidated code snippet