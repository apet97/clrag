# langsmith-define-target-function

> Source: https://docs.langchain.com/langsmith/define-target-function

- A dataset of test inputs and expected outputs.
- A target function which is what you’re evaluating.
- Evaluators that score your target function’s outputs.
Target function signature
In order to evaluate an application in code, we need a way to run the application. When usingevaluate()
(Python/TypeScript)we’ll do this by passing in a target function argument. This is a function that takes in a dataset Example’s inputs and returns the application output as a dict. Within this function we can call our application however we’d like. We can also format the output however we’d like. The key is that any evaluator functions we define should work with the output format we return in our target function.
evaluate()
will automatically trace your target function. This means that if you run any traceable code within your target function, this will also be traced as child runs of the target trace.Example: Single LLM call
Example: Non-LLM component
Example: Application or agent
If you have a LangGraph/LangChain agent that accepts the inputs defined in your dataset and that returns the output format you want to use in your evaluators, you can pass that object in as the target directly: