---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-nest-traces",
  "h1": "langsmith-nest-traces",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.454958",
  "sha256_raw": "829461832472b4b272bae985d88956cac0fe6388f54ac05c1f1c96c18124c26e"
}
---

# langsmith-nest-traces

> Source: https://docs.langchain.com/langsmith/nest-traces

When tracing with the LangSmith SDK, LangGraph, and LangChain, tracing should automatically propagate the correct context so that code executed within a parent trace will be rendered in the expected location in the UI.If you see a child run go to a separate trace (and appear on the top level), it may be caused by one of the following known “edge cases”.
When using async calls (especially with streaming) in Python versions < 3.11, you may encounter issues with trace nesting. This is because Python’s asyncio only added full support for passing context in version 3.11.
LangChain and LangSmith SDK use contextvars to propagate tracing information implicitly. In Python 3.11 and above, this works seamlessly. However, in earlier versions (3.8, 3.9, 3.10), asyncio tasks lack proper contextvar support, which can lead to disconnected traces.
Upgrade Python Version (Recommended) If possible, upgrade to Python 3.11 or later for automatic context propagation.
Manual Context Propagation If upgrading isn’t an option, you’ll need to manually propagate the tracing context. The method varies depending on your setup:a) Using LangGraph or LangChain Pass the parent config to the child call:
Copy
import asynciofrom langchain_core.runnables import RunnableConfig, RunnableLambda@RunnableLambdaasync def my_child_runnable( inputs: str, # The config arg (present in parent_runnable below) is optional): yield "A" yield "response"@RunnableLambdaasync def parent_runnable(inputs: str, config: RunnableConfig): async for chunk in my_child_runnable.astream(inputs, config): yield chunkasync def main(): return [val async for val in parent_runnable.astream("call")]asyncio.run(main())
b) Using LangSmith Directly Pass the run tree directly:
Copy
import asyncioimport langsmith as ls@ls.traceableasync def my_child_function(inputs: str): yield "A" yield "response"@ls.traceableasync def parent_function( inputs: str, # The run tree can be auto-populated by the decorator run_tree: ls.RunTree,): async for chunk in my_child_function(inputs, langsmith_extra={"parent": run_tree}): yield chunkasync def main(): return [val async for val in parent_function("call")]asyncio.run(main())
c) Combining Decorated Code with LangGraph/LangChain Use a combination of techniques for manual handoff:
Copy
import asyncioimport langsmith as lsfrom langchain_core.runnables import RunnableConfig, RunnableLambda@RunnableLambdaasync def my_child_runnable(inputs: str): yield "A" yield "response"@ls.traceableasync def my_child_function(inputs: str, run_tree: ls.RunTree): with ls.tracing_context(parent=run_tree): async for chunk in my_child_runnable.astream(inputs): yield chunk@RunnableLambdaasync def parent_runnable(inputs: str, config: RunnableConfig): # @traceable decorated functions can directly accept a RunnableConfig when passed in via "config" async for chunk in my_child_function(inputs, langsmith_extra={"config": config}): yield chunk@ls.traceableasync def parent_function(inputs: str, run_tree: ls.RunTree): # You can set the tracing context manually with ls.tracing_context(parent=run_tree): async for chunk in parent_runnable.astream(inputs): yield chunkasync def main(): return [val async for val in parent_function("call")]asyncio.run(main())
It’s common to start tracing and want to apply some parallelism on child tasks all within a single trace. Python’s stdlib ThreadPoolExecutor by default breaks tracing.
Using LangSmith’s ContextThreadPoolExecutorLangSmith provides a ContextThreadPoolExecutor that automatically handles context propagation:
Copy
from langsmith.utils import ContextThreadPoolExecutorfrom langsmith import traceable@traceabledef outer_func(): with ContextThreadPoolExecutor() as executor: inputs = [1, 2] r = list(executor.map(inner_func, inputs))@traceabledef inner_func(x): print(x)outer_func()
Manually providing the parent run treeAlternatively, you can manually pass the parent run tree to the inner function:
Copy
from langsmith import traceable, get_current_run_treefrom concurrent.futures import ThreadPoolExecutor@traceabledef outer_func(): rt = get_current_run_tree() with ThreadPoolExecutor() as executor: r = list( executor.map( lambda x: inner_func(x, langsmith_extra={"parent": rt}), [1, 2] ) )@traceabledef inner_func(x): print(x)outer_func()
In this approach, we use get_current_run_tree() to obtain the current run tree and pass it to the inner function using the langsmith_extra parameter.Both methods ensure that the inner function calls are correctly aggregated under the initial trace stack, even when executed in separate threads.