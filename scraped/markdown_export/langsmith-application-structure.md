# langsmith-application-structure

> Source: https://docs.langchain.com/langsmith/application-structure

langgraph.json
), a file that specifies dependencies, and an optional .env
file that specifies environment variables.
This page explains how a LangSmith application is organized and how to provide the configuration details required for deployment.
Key Concepts
To deploy using LangSmith, provide the following information:- A configuration file (
langgraph.json
) that specifies the dependencies, graphs, and environment variables to use for the application. - The graphs that implement the logic of the application.
- A file that specifies dependencies required to run the application.
- Environment variables that are required for the application to run.
Framework agnosticLangSmith Deployment supports deploying a LangGraph graph. However, the implementation of a node of a graph can contain arbitrary Python code. This means any framework can be implemented within a node and deployed on LangSmith Deployment. This lets you keep your core application logic outside LangGraph while still using LangSmith for deployment, scaling, and observability.
File Structure
The following are examples of directory structures for Python and JavaScript applications:- Python (requirements.txt)
- Python (pyproject.toml)
- JS (package.json)
The directory structure of an application can vary depending on the programming language and the package manager used.
Configuration File
Thelanggraph.json
file is a JSON file that specifies the dependencies, graphs, environment variables, and other settings required to deploy an application.
For details on all supported keys in the JSON file, refer to the LangGraph configuration file reference.
Examples
- Python
- JavaScript
- The dependencies involve a custom local package and the
langchain_openai
package. - A single graph will be loaded from the file
./your_package/your_file.py
with the variablevariable
. - The environment variables are loaded from the
.env
file.
Dependencies
An application may depend on other Python packages or JavaScript libraries (depending on the programming language in which the application is written). You will generally need to specify the following information for dependencies to be set up correctly:- A file in the directory that specifies the dependencies (e.g.,
requirements.txt
,pyproject.toml
, orpackage.json
). - A
dependencies
key in the configuration file that specifies the dependencies required to run the application. - Any additional binaries or system libraries can be specified using
dockerfile_lines
key in the LangGraph configuration file.
Graphs
Use thegraphs
key in the configuration file to specify which graphs will be available in the deployed application.
You can specify one or more graphs in the configuration file. Each graph is identified by a unique name and a path to either (1) a compiled graph or (2) a function that defines a graph.
Environment Variables
If you’re working with a deployed LangGraph application locally, you can configure environment variables in theenv
key of the configuration file.
For a production deployment, you will typically want to configure the environment variables in the deployment environment.