---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-query-syntax",
  "h1": "langsmith-trace-query-syntax",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.491993",
  "sha256_raw": "83ce50aad50e21f056ac033cef6493bd05e43bf49a29209843dd803ddc19be38"
}
---

# langsmith-trace-query-syntax

> Source: https://docs.langchain.com/langsmith/trace-query-syntax

project_id / project_name | The project(s) to fetch runs from - can be a single project or a list of projects. |
trace_id | Fetch runs that are part of a specific trace. |
run_type | The type of run to get, such as llm , chain , tool , retriever , etc. |
dataset_name / dataset_id | Fetch runs that are associated with an example row in the specified dataset. This is useful for comparing prompts or models over a given dataset. |
reference_example_id | Fetch runs that are associated with a specific example row. This is useful for comparing prompts or models on a given input. |
parent_run_id | Fetch runs that are children of a given run. This is useful for fetching runs grouped together using the context manager or for fetching an agent trajectory. |
error | Fetch runs that errored or did not error. |
run_ids | Fetch runs with a given list of run ids. Note: This will ignore all other filtering arguments. |
filter | Fetch runs that match a given structured filter statement. See the guide below for more information. |
trace_filter | Filter to apply to the ROOT run in the trace tree. This is meant to be used in conjunction with the regular filter parameter to let you filter runs by attributes of the root run within a trace. |
tree_filter | Filter to apply to OTHER runs in the trace tree, including sibling and child runs. This is meant to be used in conjunction with the regular filter parameter to let you filter runs by attributes of any run within a trace. |
is_root | Only return root runs. |
select | Select the fields to return in the response. By default, all fields are returned. |
query (experimental) | Natural language query, which translates your query into a filter statement. |