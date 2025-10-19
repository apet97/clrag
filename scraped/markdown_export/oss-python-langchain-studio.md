# oss-python-langchain-studio

> Source: https://docs.langchain.com/oss/python/langchain/studio

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Prerequisites
Before you begin, ensure you have the following:- An API key for LangSmith (free to sign up)
Setup local LangGraph server
1. Install the LangGraph CLI
2. Prepare your agent
We’ll use the following simple agent as an example:agent.py
3. Environment variables
Create a.env
file in the root of your project and fill in the necessary API keys. We’ll need to set the LANGSMITH_API_KEY
environment variable to the API key you get from LangSmith.
Be sure not to commit your
.env
to version control systems such as Git!.env
4. Create a LangGraph config file
Inside your app’s directory, create a configuration filelanggraph.json
:
langgraph.json
create_agent
automatically returns a compiled LangGraph graph that we can pass to the graphs
key in our configuration file.
So far, our project structure looks like this:
5. Install dependencies
In the root of your new LangGraph app, install the dependencies:6. View your agent in Studio
Start your LangGraph server:Safari blocks
localhost
connections to Studio. To work around this, run the above command with --tunnel
to access Studio via a secure tunnel.http://127.0.0.1:2024
) and the Studio UI https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
: