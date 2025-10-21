---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-dataset-transformations",
  "h1": "langsmith-dataset-transformations",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.470602",
  "sha256_raw": "112a5021d62b6e15f7bbb9b5001722af731bb6af18b91cea165dc27a2a579b30"
}
---

# langsmith-dataset-transformations

> Source: https://docs.langchain.com/langsmith/dataset-transformations

Transformation types
| Transformation Type | Target Types | Functionality |
|---|---|---|
| remove_system_messages | Array[Message] | Filters a list of messages to remove any system messages. |
| convert_to_openai_message | Message Array[Message] | Converts any incoming data from LangChain’s internal serialization format to OpenAI’s standard message format using langchain’s convert_to_openai_messages. If the target field is marked as required, and no matching message is found upon entry, it will attempt to extract a message (or list of messages) from several well-known LangSmith tracing formats (e.g., any traced LangChain BaseChatModel run or traced run from the LangSmith OpenAI wrapper), and remove the original key containing the message. |
| convert_to_openai_tool | Array[Tool] Only available on top level fields in the inputs dictionary. | Converts any incoming data into OpenAI standard tool formats here using langchain’s convert_to_openai_tool Will extract tool definitions from a run’s invocation parameters if present / no tools are found at the specified key. This is useful because LangChain chat models trace tool definitions to the extra.invocation_params field of the run rather than inputs. |
| remove_extra_fields | Object | Removes any field not defined in the schema for this target object. |
Chat Model prebuilt schema
The main use case for transformations is to simplify collecting production traces into datasets in a format that can be standardized across model providers for usage in evaluations / few shot prompting / etc downstream. To simplify setup of transformations for our end users, LangSmith offers a pre-defined schema that will do the following:- Extract messages from your collected runs and transform them into the openai standard format, which makes them compatible all LangChain ChatModels and most model providers’ SDK for downstream evaluation and experimentation
- Extract any tools used by your LLM and add them to your example’s input to be used for reproducability in downstream evaluation
Users who want to iterate on their system prompts often also add the Remove System Messages transformation on their input messages when using our Chat Model schema, which will prevent you from saving the system prompt to your dataset.