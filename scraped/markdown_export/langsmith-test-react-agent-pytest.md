# langsmith-test-react-agent-pytest

> Source: https://docs.langchain.com/langsmith/test-react-agent-pytest

Setup
This tutorial uses LangGraph for agent orchestration, OpenAI’s GPT-4o, Tavily for search, E2B’s code interpreter, and Polygon to retrieve stock data but it can be adapted for other frameworks, models and tools with minor modifications. Tavily, E2B and Polygon are free to sign up for.Installation
First, install the packages required for making the agent:Environment Variables
Set the following environment variables:Create your app
To define our React agent, we will use LangGraph/LangGraph.js for the orchestation and LangChain for the LLM and tools.Define tools
First we are going to define the tools we are going to use in our agent. There are going to be 3 tools:- A search tool using Tavily
- A code interpreter tool using E2B
- A stock information tool using Polygon
Define agent
Now that we have defined all of our tools, we can usecreate_agent
to create our agent.
Write tests
Now that we have defined our agent, let’s write a few tests to ensure basic functionality. In this tutorial we are going to test whether the agent’s tool calling abilities are working, whether the agent knows to ignore irrelevant questions, and whether it is able to answer complex questions that involve using all of the tools. We need to first set up a test file and add the imports needed at the top of the file.Test 1: Handle off-topic questions
The first test will be a simple check that the agent does not use tools on irrelevant queries.Test 2: Simple tool calling
For tool calling, we are going to verify that the agent calls the correct tool with the correct parameters.Test 3: Complex tool calling
Some tool calls are easier to test than others. With the ticker lookup, we can assert that the correct ticker is searched. With the coding tool, the inputs and outputs of the tool are much less constrained, and there are lots of ways to get to the right answer. In this case, it’s simpler to test that the tool is used correctly by running the full agent and asserting that it both calls the coding tool and that it ends up with the right answer.Test 4: LLM-as-a-judge
We are going to ensure that the agent’s answer is grounded in the search results by running an LLM-as-a-judge evaluation. In order to trace the LLM as a judge call separately from our agent, we will use the LangSmith providedtrace_feedback
context manager in Python and wrapEvaluator
function in JS/TS.
Run tests
Once you have setup your config files (if you are using Vitest or Jest), you can run your tests using the following commands:Config files for Vitest/Jest
Config files for Vitest/Jest
Reference code
Remember to also add the config files for Vitest and Jest to your project.Agent
Agent code
Agent code
Tests
Test code
Test code