# langsmith-log-llm-trace

> Source: https://docs.langchain.com/langsmith/log-llm-trace

- Rich, structured rendering of message lists
- Token and cost tracking per LLM call, per trace and across traces over time
Messages Format
When tracing a custom model or a custom input/output format, it must either follow the LangChain format, OpenAI completions format or Anthropic messages format. For more details, refer to the OpenAI Chat Completions or Anthropic Messages documentation. The LangChain format is:Examples
Converting custom I/O formats into LangSmith compatible formats
If you’re using a custom input or output format, you can convert it to a LangSmith compatible format usingprocess_inputs
/processInputs
and process_outputs
/processOutputs
functions on the @traceable
decorator (Python) or traceable
function (TS).
process_inputs
/processInputs
and process_outputs
/processOutputs
accept functions that allow you to transform the inputs and outputs of a specific trace before they are logged to LangSmith. They have access to the trace’s inputs and outputs, and can return a new dictionary with the processed data.
Here’s a boilerplate example of how to use process_inputs
and process_outputs
to convert a custom I/O format into a LangSmith compatible format:
Identifying a custom model in traces
When using a custom model, it is recommended to also provide the followingmetadata
fields to identify the model when viewing traces and when filtering.
ls_provider
: The provider of the model, eg “openai”, “anthropic”, etc.ls_model_name
: The name of the model, eg “gpt-4o-mini”, “claude-3-opus-20240307”, etc.
If you implement a custom streaming chat_model, you can “reduce” the outputs into the same format as the non-streaming version. This is currently only supported in Python.
If
ls_model_name
is not present in extra.metadata
, other fields might be used from the extra.metadata
for estimating token counts. The following fields are used in the order of precedence:metadata.ls_model_name
inputs.model
inputs.model_name
metadata
fields, refer to the Add metadata and tags guide.
Provide token and cost information
By default, LangSmith uses tiktoken to count tokens, utilizing a best guess at the model’s tokenizer based on thels_model_name
provided. It also calculates costs automatically by using the model pricing table. To learn how LangSmith calculates token-based costs, see this guide.
However, many models already include exact token counts as part of the response. If you have this information, you can override the default token calculation in LangSmith in one of two ways:
- Extract usage within your traced function and set a
usage_metadata
field on the run’s metadata. - Return a
usage_metadata
field in your traced function outputs.
You cannot set any fields other than the ones listed below. You do not need to include all fields.
Setting run metadata
You can modify the current run’s metadata with usage information within your traced function. The advantage of this approach is that you do not need to change your traced function’s runtime outputs. Here’s an example:Requires
langsmith>=0.3.43
(Python) and langsmith>=0.3.30
(JS/TS).Setting run outputs
You can add ausage_metadata
key to the function’s response to set manual token counts and costs.
Time-to-first-token
If you are usingtraceable
or one of our SDK wrappers, LangSmith will automatically populate time-to-first-token for streaming LLM runs.
However, if you are using the RunTree
API directly, you will need to add a new_token
event to the run tree in order to properly populate time-to-first-token.
Here’s an example: