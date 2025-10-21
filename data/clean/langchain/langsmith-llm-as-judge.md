---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-llm-as-judge",
  "h1": "langsmith-llm-as-judge",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.471184",
  "sha256_raw": "32d5300b3c1ebb727d1c4b60a17edd436868d360e73ebd4696f2c0cc1aaf547c"
}
---

# langsmith-llm-as-judge

> Source: https://docs.langchain.com/langsmith/llm-as-judge

LLM applications can be challenging to evaluate since they often generate conversational text with no single correct answer.This guide shows you how to define an LLM-as-a-judge evaluator for offline evaluation using either the LangSmith SDK or the UI. Note: To run evaluations in real-time on your production traces, refer to setting up online evaluations.
Pre-built evaluators are a useful starting point for setting up evaluations. Refer to pre-built evaluators for how to use pre-built evaluators with LangSmith.
For complete control of evaluator logic, create your own LLM-as-a-judge evaluator and run it using the LangSmith SDK (Python / TypeScript).Requires langsmith>=0.2.0
Copy
from langsmith import evaluate, traceable, wrappers, Clientfrom openai import OpenAI# Assumes you've installed pydanticfrom pydantic import BaseModel# Optionally wrap the OpenAI client to trace all model calls.oai_client = wrappers.wrap_openai(OpenAI())def valid_reasoning(inputs: dict, outputs: dict) -> bool: """Use an LLM to judge if the reasoning and the answer are consistent.""" instructions = """Given the following question, answer, and reasoning, determine if the reasoningfor the answer is logically valid and consistent with the question and the answer.""" class Response(BaseModel): reasoning_is_valid: bool msg = f"Question: {inputs['question']}\nAnswer: {outputs['answer']}\nReasoning: {outputs['reasoning']}" response = oai_client.beta.chat.completions.parse( model="gpt-4o", messages=[{"role": "system", "content": instructions,}, {"role": "user", "content": msg}], response_format=Response ) return response.choices[0].message.parsed.reasoning_is_valid# Optionally add the 'traceable' decorator to trace the inputs/outputs of this function.@traceabledef dummy_app(inputs: dict) -> dict: return {"answer": "hmm i'm not sure", "reasoning": "i didn't understand the question"}ls_client = Client()dataset = ls_client.create_dataset("big questions")examples = [ {"inputs": {"question": "how will the universe end"}}, {"inputs": {"question": "are we alone"}},]ls_client.create_examples(dataset_id=dataset.id, examples=examples)results = evaluate( dummy_app, data=dataset, evaluators=[valid_reasoning])
See here for more on how to write a custom evaluator.
Add specific instructions for your LLM-as-a-judge evalutor prompt and configure which parts of the input/output/reference output should be passed to the evaluator.
Create a new prompt, or choose an existing prompt from the prompt hub.
Create your own prompt: Create a custom prompt inline.
Pull a prompt from the prompt hub: Use the Select a prompt dropdown to select from an existing prompt. You can’t edit these prompts directly within the prompt editor, but you can view the prompt and the schema it uses. To make changes, edit the prompt in the playground and commit the version, and then pull in your new prompt in the evaluator.
Use variable mapping to indicate the variables that are passed into your evaluator prompt from your run or example. To aid with variable mapping, an example (or run) is provided for reference. Click on the the variables in your prompt and use the dropdown to map them to the relevant parts of the input, output, or reference output.To add prompt variables type the variable with double curly brackets {{prompt_var}} if using mustache formatting (the default) or single curly brackets {prompt_var} if using f-string formatting.You may remove variables as needed. For example if you are evaluating a metric such as conciseness, you typically don’t need a reference output so you may remove that variable.
To better align the LLM-as-a-judge evaluator to human preferences, LangSmith allows you to collect human corrections on evaluator scores. With this selection enabled, corrections are then inserted automatically as few-shot examples into your prompt.Learn how to set up few-shot examples and make corrections.
Feedback configuration is the scoring criteria that your LLM-as-a-judge evaluator will use. Think of this as the rubric that your evaluator will grade based on. Scores will be added as feedback to a run or example. Defining feedback for your evaluator:
Name the feedback key: This is the name that will appear when viewing evaluation results. Names should be unique across experiments.
Add a description: Describe what the feedback represents.
Choose a feedback type:
Boolean: True/false feedback.
Categorical: Select from predefined categories.
Continuous: Numerical scoring within a specified range.
Behind the scenes, feedback configuration is added as structured output to the LLM-as-a-judge prompt. If you’re using an existing prompt from the hub, you must add an output schema to the prompt before configuring an evaluator to use it. Each top-level key in the output schema will be treated as a separate piece of feedback.