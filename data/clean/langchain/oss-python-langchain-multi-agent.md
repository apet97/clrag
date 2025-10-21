---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-multi-agent",
  "h1": "oss-python-langchain-multi-agent",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.475379",
  "sha256_raw": "b63dc7ac81e060096dfff6cbfbda73d9297bc7d6d810bb0cb2a6261804ae1ef4"
}
---

# oss-python-langchain-multi-agent

> Source: https://docs.langchain.com/oss/python/langchain/multi-agent

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- A single agent has too many tools and makes poor decisions about which to use.
- Context or memory grows too large for one agent to track effectively.
- Tasks require specialization (e.g., a planner, researcher, math expert).
Multi-agent patterns
| Pattern | How it works | Control flow | Example use case |
|---|---|---|---|
| Tool Calling | A supervisor agent calls other agents as tools. The “tool” agents don’t talk to the user directly — they just run their task and return results. | Centralized: all routing passes through the calling agent. | Task orchestration, structured workflows. |
| Handoffs | The current agent decides to transfer control to another agent. The active agent changes, and the user may continue interacting directly with the new agent. | Decentralized: agents can change who is active. | Multi-domain conversations, specialist takeover. |
Tutorial: Build a supervisor agent
Learn how to build a personal assistant using the supervisor pattern, where a central supervisor agent coordinates specialized worker agents.
This tutorial demonstrates:
- Creating specialized sub-agents for different domains (calendar and email)
- Wrapping sub-agents as tools for centralized orchestration
- Adding human-in-the-loop review for sensitive actions
Choosing a pattern
| Question | Tool Calling | Handoffs |
|---|---|---|
| Need centralized control over workflow? | ✅ Yes | ❌ No |
| Want agents to interact directly with the user? | ❌ No | ✅ Yes |
| Complex, human-like conversation between specialists? | ❌ Limited | ✅ Strong |
You can mix both patterns — use handoffs for agent switching, and have each agent call subagents as tools for specialized tasks.
Customizing agent context
At the heart of multi-agent design is context engineering - deciding what information each agent sees. LangChain gives you fine-grained control over:- Which parts of the conversation or state are passed to each agent.
- Specialized prompts tailored to subagents.
- Inclusion/exclusion of intermediate reasoning.
- Customizing input/output formats per agent.
Tool calling
In tool calling, one agent (the “controller”) treats other agents as tools to be invoked when needed. The controller manages orchestration, while tool agents perform specific tasks and return results. Flow:- The controller receives input and decides which tool (subagent) to call.
- The tool agent runs its task based on the controller’s instructions.
- The tool agent returns results to the controller.
- The controller decides the next step or finishes.
Agents used as tools are generally not expected to continue conversation with the user.
Their role is to perform a task and return results to the controller agent.
If you need subagents to be able to converse with the user, use handoffs instead.
Implementation
Below is a minimal example where the main agent is given access to a single subagent via a tool definition:- The main agent invokes
call_subagent1
when it decides the task matches the subagent’s description. - The subagent runs independently and returns its result.
- The main agent receives the result and continues orchestration.
Where to customize
There are several points where you can control how context is passed between the main agent and its subagents:- Subagent name (
"subagent1_name"
): This is how the main agent refers to the subagent. Since it influences prompting, choose it carefully. - Subagent description (
"subagent1_description"
): This is what the main agent “knows” about the subagent. It directly shapes how the main agent decides when to call it. - Input to the subagent: You can customize this input to better shape how the subagent interprets tasks. In the example above, we pass the agent-generated
query
directly. - Output from the subagent: This is the response passed back to the main agent. You can adjust what is returned to control how the main agent interprets results. In the example above, we return the final message text, but you could return additional state or metadata.
Control the input to the subagent
There are two main levers to control the input that the main agent passes to a subagent:- Modify the prompt – Adjust the main agent’s prompt or the tool metadata (i.e., sub-agent’s name and description) to better guide when and how it calls the subagent.
- Context injection – Add input that isn’t practical to capture in a static prompt (e.g., full message history, prior results, task metadata) by adjusting the tool call to pull from the agent’s state.
Control the output from the subagent
Two common strategies for shaping what the main agent receives back from a subagent:- Modify the prompt – Refine the subagent’s prompt to specify exactly what should be returned.
- Useful when outputs are incomplete, too verbose, or missing key details.
- A common failure mode is that the subagent performs tool calls or reasoning but does not include the results in its final message. Remind it that the controller (and user) only see the final output, so all relevant info must be included there.
- Custom output formatting – adjust or enrich the subagent’s response in code before handing it back to the main agent.
- Example: pass specific state keys back to the main agent in addition to the final text.
- This requires wrapping the result in a
Command
(or equivalent structure) so you can merge custom state with the subagent’s response.
Handoffs
In handoffs, agents can directly pass control to each other. The “active” agent changes, and the user interacts with whichever agent currently has control. Flow:- The current agent decides it needs help from another agent.
- It passes control (and state) to the next agent.
- The new agent interacts directly with the user until it decides to hand off again or finish.