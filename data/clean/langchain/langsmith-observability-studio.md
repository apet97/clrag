---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-observability-studio",
  "h1": "langsmith-observability-studio",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.457564",
  "sha256_raw": "0ae0b65d123567f20816106c7d884e0af20c4fd70c52348720193ee3602de7cc"
}
---

# langsmith-observability-studio

> Source: https://docs.langchain.com/langsmith/observability-studio

- Iterate on prompts: Modify prompts inside graph nodes directly or with the LangSmith playground.
- Run experiments over a dataset: Execute your assistant over a LangSmith dataset to score and compare results.
- Debug LangSmith traces: Import traced runs into Studio and optionally clone them into your local agent.
- Add a node to a dataset: Turn parts of thread history into dataset examples for evaluation or further analysis.
Iterate on prompts
Studio supports the following methods for modifying prompts in your graph:Direct node editing
Studio allows you to edit prompts used inside individual nodes, directly from the graph interface.Graph Configuration
Define your configuration to specify prompt fields and their associated nodes usinglanggraph_nodes
and langgraph_type
keys.
langgraph_nodes
- Description: Specifies which nodes of the graph a configuration field is associated with.
- Value Type: Array of strings, where each string is the name of a node in your graph.
- Usage Context: Include in the
json_schema_extra
dictionary for Pydantic models or themetadata["json_schema_extra"]
dictionary for dataclasses. - Example:
langgraph_type
- Description: Specifies the type of configuration field, which determines how it’s handled in the UI.
- Value Type: String
- Supported Values:
"prompt"
: Indicates the field contains prompt text that should be treated specially in the UI.
- Usage Context: Include in the
json_schema_extra
dictionary for Pydantic models or themetadata["json_schema_extra"]
dictionary for dataclasses. - Example:
Full example configuration
Full example configuration
Editing prompts in the UI
- Locate the gear icon on nodes with associated configuration fields.
- Click to open the configuration modal.
- Edit the values.
- Save to update the current assistant version or create a new one.
Playground
The playground interface allows testing individual LLM calls without running the full graph:- Select a thread.
- Click View LLM Runs on a node. This lists all the LLM calls (if any) made inside the node.
- Select an LLM run to open in the playground.
- Modify prompts and test different model and tool settings.
- Copy updated prompts back to your graph.
Run experiments over a dataset
Studio lets you run evaluations by executing your assistant against a predefined LangSmith dataset. This allows you to test performance across a variety of inputs, compare outputs to reference answers, and score results with configured evaluators. This guide shows you how to run a full end-to-end experiment directly from Studio.Prerequisites
Before running an experiment, ensure you have the following:- A LangSmith dataset: Your dataset should contain the inputs you want to test and optionally, reference outputs for comparison. The schema for the inputs must match the required input schema for the assistant. For more information on schemas, see here. For more on creating datasets, refer to How to Manage Datasets.
- (Optional) Evaluators: You can attach evaluators (e.g., LLM-as-a-Judge, heuristics, or custom functions) to your dataset in LangSmith. These will run automatically after the graph has processed all inputs.
- A running application: The experiment can be run against:
- An application deployed on LangSmith.
- A locally running application started via the langgraph-cli.
Experiment setup
- Launch the experiment. Click the Run experiment button in the top right corner of the Studio page.
- Select your dataset. In the modal that appears, select the dataset (or a specific dataset split) to use for the experiment and click Start.
- Monitor the progress. All of the inputs in the dataset will now be run against the active assistant. Monitor the experiment’s progress via the badge in the top right corner.
- You can continue to work in Studio while the experiment runs in the background. Click the arrow icon button at any time to navigate to LangSmith and view the detailed experiment results.
Debug LangSmith traces
This guide explains how to open LangSmith traces in Studio for interactive investigation and debugging.Open deployed threads
- Open the LangSmith trace, selecting the root run.
- Click Run in Studio.
Testing local agents with remote traces
This section explains how to test a local agent against remote traces from LangSmith. This enables you to use production traces as input for local testing, allowing you to debug and verify agent modifications in your development environment.Prerequisites
- A LangSmith traced thread
- A locally running agent.
Local agent requirements
- langgraph>=0.3.18
- langgraph-api>=0.0.32
- Contains the same set of nodes present in the remote trace
Clone thread
- Open the LangSmith trace, selecting the root run.
- Click the dropdown next to Run in Studio.
- Enter your local agent’s URL.
- Select Clone thread locally.
- If multiple graphs exist, select the target graph.
Add node to dataset
Add examples to LangSmith datasets from nodes in the thread log. This is useful to evaluate individual steps of the agent.- Select a thread.
- Click Add to Dataset.
- Select nodes whose input/output you want to add to a dataset.
- For each selected node, select the target dataset to create the example in. By default a dataset for the specific assistant and node will be selected. If this dataset does not yet exist, it will be created.
- Edit the example’s input/output as needed before adding it to the dataset.
- Select Add to dataset at the bottom of the page to add all selected nodes to their respective datasets.