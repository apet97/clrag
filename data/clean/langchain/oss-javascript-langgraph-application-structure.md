---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-application-structure",
  "h1": "oss-javascript-langgraph-application-structure",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.466672",
  "sha256_raw": "98392e19dc3bc36599f9b41479b5cf876d5207b45efd94906650c53af67260d4"
}
---

# oss-javascript-langgraph-application-structure

> Source: https://docs.langchain.com/oss/javascript/langgraph/application-structure

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
A LangGraph application consists of one or more graphs, a configuration file (langgraph.json
), a file that specifies dependencies, and an optional .env
file that specifies environment variables.
This guide shows a typical structure of an application and shows how the required information to deploy an application using the LangSmith is specified.
Key Concepts
To deploy using the LangSmith, the following information should be provided:- A LangGraph configuration file (
langgraph.json
) that specifies the dependencies, graphs, and environment variables to use for the application. - The graphs that implement the logic of the application.
- A file that specifies dependencies required to run the application.
- Environment variables that are required for the application to run.
File Structure
Below are examples of directory structures for applications:The directory structure of a LangGraph application can vary depending on the programming language and the package manager used.
Configuration File
Thelanggraph.json
file is a JSON file that specifies the dependencies, graphs, environment variables, and other settings required to deploy a LangGraph application.
See the LangGraph configuration file reference for details on all supported keys in the JSON file.
Examples
- The dependencies will be loaded from a dependency file in the local directory (e.g.,
package.json
). - A single graph will be loaded from the file
./your_package/your_file.js
with the functionagent
. - The environment variable
OPENAI_API_KEY
is set inline.
Dependencies
A LangGraph application may depend on other TypeScript/JavaScript libraries. You will generally need to specify the following information for dependencies to be set up correctly:-
A file in the directory that specifies the dependencies (e.g.
package.json
). -
A
dependencies
key in the LangGraph configuration file that specifies the dependencies required to run the LangGraph application. -
Any additional binaries or system libraries can be specified using
dockerfile_lines
key in the LangGraph configuration file.
Graphs
Use thegraphs
key in the LangGraph configuration file to specify which graphs will be available in the deployed LangGraph application.
You can specify one or more graphs in the configuration file. Each graph is identified by a name (which should be unique) and a path for either: (1) the compiled graph or (2) a function that makes a graph is defined.
Environment Variables
If you’re working with a deployed LangGraph application locally, you can configure environment variables in theenv
key of the LangGraph configuration file.
For a production deployment, you will typically want to configure the environment variables in the deployment environment.