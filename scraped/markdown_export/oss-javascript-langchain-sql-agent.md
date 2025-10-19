# oss-javascript-langchain-sql-agent

> Source: https://docs.langchain.com/oss/javascript/langchain/sql-agent

Overview
In this tutorial, you will learn how to build an agent that can answer questions about a SQL database using LangChain agents. At a high level, the agent will:Fetch the available tables and schemas from the database
Decide which tables are relevant to the question
Fetch the schemas for the relevant tables
Generate a query based on the question and information from the schemas
Double-check the query for common mistakes using an LLM
Execute the query and return the results
Correct mistakes surfaced by the database engine until the query is successful
Formulate a response based on the results
Concepts
We will cover the following concepts:- Tools for reading from SQL databases
- LangChain agents
- Human-in-the-loop processes
Setup
Installation
LangSmith
Set up LangSmith to inspect what is happening inside your chain or agent. Then set the following environment variables:1. Select an LLM
Select a model that supports tool-calling: The output shown in the examples below used OpenAI.2. Configure the database
You will be creating a SQLite database for this tutorial. SQLite is a lightweight database that is easy to set up and use. We will be loading thechinook
database, which is a sample database that represents a digital media store.
For convenience, we have hosted the database (Chinook.db
) on a public GCS bucket.
3. Add tools for database interactions
Use theSqlDatabase
wrapper available in the langchain/sql_db
to interact with the database. The wrapper provides a simple interface to execute SQL queries and fetch results:
6. Implement human-in-the-loop review
It can be prudent to check the agent’s SQL queries before they are executed for any unintended actions or inefficiencies. LangChain agents feature support for built-in human-in-the-loop middleware to add oversight to agent tool calls. Let’s configure the agent to pause for human review on calling thesql_db_query
tool:
sql_db_query
tool:
4. Execute SQL queries
Before running the command, do a check to check the LLM generated command in _safe_sql
:
run
from SQLDatabase
to execute commands with an execute_sql
tool:
5. Use createAgent
Use createAgent
to build a ReAct agent with minimal code. The agent will interpret the request and generate a SQL command. The tools will check the command for safety and then try to execute the command. If the command has an error, the error message is returned to the model. The model can then examine the original request and the new error message and generate a new command. This can continue until the LLM generates the command successfully or reaches an end count. This pattern of providing a model with feedback - error messages in this case - is very powerful.
Initialize the agent with a descriptive system prompt to customize its behavior:
6. Run the agent
Run the agent on a sample query and observe its behavior:(Optional) Use Studio
Studio provides a “client side” loop as well as memory so you can run this as a chat interface and query the database. You can ask questions like “Tell me the scheme of the database” or “Show me the invoices for the 5 top customers”. You will see the SQL command that is generated and the resulting output. The details of how to get that started are below.Run your agent in Studio
Run your agent in Studio
langgraph.json
file with the following contents: