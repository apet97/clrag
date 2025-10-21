---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-setup-javascript",
  "h1": "langsmith-setup-javascript",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.481184",
  "sha256_raw": "ab31fa038dded1931f21f68948bd1a10ef4a5d6a3895bfc0da6c50ea88ed6b28"
}
---

# langsmith-setup-javascript

> Source: https://docs.langchain.com/langsmith/setup-javascript

package.json
to specify project dependencies.
This walkthrough is based on this repository, which you can play around with to learn more about how to set up your application for deployment.
The final repository structure will look something like this:
LangSmith Deployment supports deploying a LangGraph graph. However, the implementation of a node of a graph can contain arbitrary Python code. This means any framework can be implemented within a node and deployed on LangSmith Deployment. This lets you keep your core application logic outside LangGraph while still using LangSmith for deployment, scaling, and observability.
Specify Dependencies
Dependencies can be specified in apackage.json
. If none of these files is created, then dependencies can be specified later in the configuration file.
Example package.json
file:
Specify Environment Variables
Environment variables can optionally be specified in a file (e.g..env
). See the Environment Variables reference to configure additional variables for a deployment.
Example .env
file:
Define Graphs
Implement your graphs. Graphs can be defined in a single file or multiple files. Make note of the variable names of each compiled graph to be included in the application. The variable names will be used later when creating the configuration file. Here is an exampleagent.ts
:
Create the API Config
Create a configuration file calledlanggraph.json
. See the configuration file reference for detailed explanations of each key in the JSON object of the configuration file.
Example langgraph.json
file:
CompiledGraph
appears at the end of the value of each subkey in the top-level graphs
key (i.e. :<variable_name>
).
Configuration Location
The configuration file must be placed in a directory that is at the same level or higher than the TypeScript files that contain compiled graphs and associated dependencies.