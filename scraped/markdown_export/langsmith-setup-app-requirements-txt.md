# langsmith-setup-app-requirements-txt

> Source: https://docs.langchain.com/langsmith/setup-app-requirements-txt

requirements.txt
to specify project dependencies.
This example is based on this repository, which uses the LangGraph framework.
The final repository structure will look something like this:
LangSmith Deployment supports deploying a LangGraph graph. However, the implementation of a node of a graph can contain arbitrary Python code. This means any framework can be implemented within a node and deployed on LangSmith Deployment. This lets you keep your core application logic outside LangGraph while still using LangSmith for deployment, scaling, and observability.
pyproject.toml
: If you prefer using poetry for dependency management, check out this how-to guide on usingpyproject.toml
for LangSmith.- a monorepo: If you are interested in deploying a graph located inside a monorepo, take a look at this repository for an example of how to do so.
Specify Dependencies
Dependencies can optionally be specified in one of the following files:pyproject.toml
, setup.py
, or requirements.txt
. If none of these files is created, then dependencies can be specified later in the configuration file.
The dependencies below will be included in the image, you can also use them in your code, as long as with a compatible version range:
requirements.txt
file:
Specify Environment Variables
Environment variables can optionally be specified in a file (e.g..env
). See the Environment Variables reference to configure additional variables for a deployment.
Example .env
file:
Define Graphs
Implement your graphs. Graphs can be defined in a single file or multiple files. Make note of the variable names of each CompiledStateGraph to be included in the application. The variable names will be used later when creating the LangGraph configuration file. Exampleagent.py
file, which shows how to import from other modules you define (code for the modules is not shown here, please see this repository to see their implementation):
Create the configuration file
Create a configuration file calledlanggraph.json
. See the configuration file reference for detailed explanations of each key in the JSON object of the configuration file.
Example langgraph.json
file:
CompiledGraph
appears at the end of the value of each subkey in the top-level graphs
key (i.e. :<variable_name>
).
Configuration File Location
The configuration file must be placed in a directory that is at the same level or higher than the Python files that contain compiled graphs and associated dependencies.