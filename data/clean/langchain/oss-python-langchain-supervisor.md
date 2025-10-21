---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-supervisor",
  "h1": "oss-python-langchain-supervisor",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.462079",
  "sha256_raw": "7e2989ba1fe97f2ab18e157491600165a8a51b34660bb43ab4222ac44e4f8576"
}
---

# oss-python-langchain-supervisor

> Source: https://docs.langchain.com/oss/python/langchain/supervisor

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
The supervisor pattern is a multi-agent architecture where a central supervisor agent coordinates specialized worker agents. This approach excels when tasks require different types of expertise. Rather than building one agent that manages tool selection across domains, you create focused specialists coordinated by a supervisor who understands the overall workflow. In this tutorial, you’ll build a personal assistant system that demonstrates these benefits through a realistic workflow. The system will coordinate two specialists with fundamentally different responsibilities:- A calendar agent that handles scheduling, availability checking, and event management.
- An email agent that manages communication, drafts messages, and sends notifications.
Why use a supervisor?
Multi-agent architectures allow you to partition tools across workers, each with their own individual prompts or instructions. Consider an agent with direct access to all calendar and email APIs: it must choose from many similar tools, understand exact formats for each API, and handle multiple domains simultaneously. If performance degrades, it may be helpful to separate related tools and associated prompts into logical groups (in part to manage iterative improvements).Concepts
We will cover the following concepts:Setup
Installation
This tutorial requires thelangchain
package:
LangSmith
Set up LangSmith to inspect what is happening inside your agent. Then set the following environment variables:Components
We will need to select a chat model from LangChain’s suite of integrations:1. Define tools
Start by defining the tools that require structured inputs. In real applications, these would call actual APIs (Google Calendar, SendGrid, etc.). For this tutorial, you’ll use stubs to demonstrate the pattern.2. Create specialized sub-agents
Next, we’ll create specialized sub-agents that handle each domain.Create a calendar agent
The calendar agent understands natural language scheduling requests and translates them into precise API calls. It handles date parsing, availability checking, and event creation.create_calendar_event
, and returns a natural language confirmation.
Create an email agent
The email agent handles message composition and sending. It focuses on extracting recipient information, crafting appropriate subject lines and body text, and managing email communication.send_email
, and returns a confirmation. Each sub-agent has a narrow focus with domain-specific tools and prompts, allowing it to excel at its specific task.
3. Wrap sub-agents as tools
Now wrap each sub-agent as a tool that the supervisor can invoke. This is the key architectural step that creates the layered system. The supervisor will see high-level tools like “schedule_event”, not low-level tools like “create_calendar_event”.4. Create the supervisor agent
Now create the supervisor that orchestrates the sub-agents. The supervisor only sees high-level tools and makes routing decisions at the domain level, not the individual API level.5. Use the supervisor
Now test your complete system with complex requests that require coordination across multiple domains:Example 1: Simple single-domain request
schedule_event
, and the calendar agent handles date parsing and event creation.
Example 2: Complex multi-domain request
schedule_event
for the meeting, then calls manage_email
for the reminder. Each sub-agent completes its task, and the supervisor synthesizes both results into a coherent response.
Complete working example
Here’s everything together in a runnable script:Understanding the architecture
Your system has three layers. The bottom layer contains rigid API tools that require exact formats. The middle layer contains sub-agents that accept natural language, translate it to structured API calls, and return natural language confirmations. The top layer contains the supervisor that routes to high-level capabilities and synthesizes results. This separation of concerns provides several benefits: each layer has a focused responsibility, you can add new domains without affecting existing ones, and you can test and iterate on each layer independently.6. Add human-in-the-loop review
It can be prudent to incorporate human-in-the-loop review of sensitive actions. LangChain includes built-in middleware to review tool calls, in this case the tools invoked by sub-agents. Let’s add human-in-the-loop review to both sub-agents:- We configure the
create_calendar_event
andsend_email
tools to interrupt, permitting all response types (approve
,edit
,reject
) - We add a checkpointer only to the top-level agent. This is required to pause and resume execution.
Command
. Refer to the human-in-the-loop guide for additional details. For demonstration purposes, here we will accept the calendar event, but edit the subject of the outbound email:
7. Advanced: Control information flow
By default, sub-agents receive only the request string from the supervisor. You might want to pass additional context, such as conversation history or user preferences.Pass additional conversational context to sub-agents
Control what supervisor receives
You can also customize what information flows back to the supervisor:8. Key takeaways
The supervisor pattern creates layers of abstraction where each layer has a clear responsibility. When designing a supervisor system, start with clear domain boundaries and give each sub-agent focused tools and prompts. Write clear tool descriptions for the supervisor, test each layer independently before integration, and control information flow based on your specific needs.When to use the supervisor patternUse the supervisor pattern when you have multiple distinct domains (calendar, email, CRM, database), each domain has multiple tools or complex logic, you want centralized workflow control, and sub-agents don’t need to converse directly with users.For simpler cases with just a few tools, use a single agent. When agents need to have conversations with users, use handoffs instead. For peer-to-peer collaboration between agents, consider other multi-agent patterns.