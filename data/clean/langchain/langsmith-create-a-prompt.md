---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-create-a-prompt",
  "h1": "langsmith-create-a-prompt",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.484196",
  "sha256_raw": "79f1f98299e799547a9d1d91ecab55a73c4f50d9bf5f651545447013e571e8d9"
}
---

# langsmith-create-a-prompt

> Source: https://docs.langchain.com/langsmith/create-a-prompt

Compose your prompt
On the left is an editable view of the prompt. The prompt is made up of messages, each of which has a “role” - includingsystem
, human
, and ai
.
Template format
The default template format isf-string
, but you can change the prompt template format to mustache
by clicking on the settings icon next to the model -> prompt format -> template format. Learn more about template formats here.
Add a template variable
The power of prompts comes from the ability to use variables in your prompt. You can use variables to add dynamic content to your prompt. Add a template variable in one of two ways:-
Add
{{variable_name}}
to your prompt (with one curly brace on each side forf-string
and two formustache
). - Highlight text you want to templatize and click the tooltip button that shows up. Enter a name for your variable, and convert.
Structured output
Adding an output schema to your prompt will get output in a structured format. Learn more about structured output here.Tools
You can also add a tool by clicking the+ Tool
button at the bottom of the prompt editor. See here for more information on how to use tools.
Run the prompt
Click “Start” to run the prompt.Save your prompt
To save your prompt, click the “Save” button, name your prompt, and decide if you want it to be “private” or “public”. Private prompts are only visible to your workspace, while public prompts are discoverable to anyone. The model and configuration you select in the Playground settings will be saved with the prompt. When you reopen the prompt, the model and configuration will automatically load from the saved version.The first time you create a public prompt, you’ll be asked to set a LangChain Hub handle. All your public prompts will be linked to this handle. In a shared workspace, this handle will be set for the whole workspace.