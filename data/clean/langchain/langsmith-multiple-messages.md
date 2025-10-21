---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-multiple-messages",
  "h1": "langsmith-multiple-messages",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.463501",
  "sha256_raw": "66ad25c302aecaf96cae921ae66a6255e304825d470da397d86f1d27eb1cda61"
}
---

# langsmith-multiple-messages

> Source: https://docs.langchain.com/langsmith/multiple-messages

This how-to guide walks you through the various ways you can set up the playground for multi-turn conversations, which will allow you to test different tool configurations and system prompts against longer threads of messages.
First, ensure you have properly traced a multi-turn conversation, and then navigate to your tracing project. Once you get to your tracing project simply open the run, select the LLM call, and open it in the playground as follows:You can then edit the system prompt, tweak the tools and/or output schema and observe how the output of the multi-turn conversation changes.
Before starting, make sure you have set up your dataset. Since you want to evaluate multi-turn conversations, make sure there is a key in your inputs that contains a list of messages.Once you have created your dataset, head to the playground and load your dataset to evaluate.Then, add a messages list variable to your prompt, making sure to name it the same as the key in your inputs that contains the list of messages:When you run your prompt, the messages from each example will be added as a list in place of the ‘Messages List’ variable.
There are two ways to manually create multi-turn conversations. The first way is by simply appending messages to the prompt:This is helpful for quick iteration, but is rigid since the multi-turn conversation is hardcoded. Instead, if you want your prompt to work with any multi-turn conversation you can add a ‘Messages List’ variable and add your multi-turn conversation there:This allows you to just tweak the system prompt or the tools, while allowing any multi-turn conversation to take the place of the Messages List variable, allowing you to reuse this prompt across various runs.
Now that you know how to set up the playground for multi-turn interactions, you can either manually inspect and judge the outputs, or you can add evaluators to classify results.You can also read these how-to guides to learn more about how to use the playground to run evaluations.