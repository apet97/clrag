# oss-javascript-langgraph-thinking-in-langgraph

> Source: https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph

Start with the process you want to automate
Imagine that you need to build an AI agent that handles customer support emails. Your product team has given you these requirements: The agent should:- Read incoming customer emails
- Classify them by urgency and topic
- Search relevant documentation to answer questions
- Draft appropriate responses
- Escalate complex issues to human agents
- Schedule follow-ups when needed
- Simple product question: “How do I reset my password?”
- Bug report: “The export feature crashes when I select PDF format”
- Urgent billing issue: “I was charged twice for my subscription!”
- Feature request: “Can you add dark mode to the mobile app?”
- Complex technical issue: “Our API integration fails intermittently with 504 errors”
Step 1: Map out your workflow as discrete steps
Start by identifying the distinct steps in your process. Each step will become a node (a function that does one specific thing). Then sketch how these steps connect to each other. The arrows show possible paths, but the actual decision of which path to take happens inside each node. Now that you’ve identified the components in your workflow, let’s understand what each node needs to do:- Read Email: Extract and parse the email content
- Classify Intent: Use an LLM to categorize urgency and topic, then route to appropriate action
- Doc Search: Query your knowledge base for relevant information
- Bug Track: Create or update issue in tracking system
- Draft Reply: Generate an appropriate response
- Human Review: Escalate to human agent for approval or handling
- Send Reply: Dispatch the email response
Step 2: Identify what each step needs to do
For each node in your graph, determine what type of operation it represents and what context it needs to work properly.LLM Steps
Data Steps
Action Steps
User Input Steps
LLM Steps
When a step needs to understand, analyze, generate text, or make reasoning decisions:Classify Intent Node
Classify Intent Node
- Static context (prompt): Classification categories, urgency definitions, response format
- Dynamic context (from state): Email content, sender information
- Desired outcome: Structured classification that determines routing
Draft Reply Node
Draft Reply Node
- Static context (prompt): Tone guidelines, company policies, response templates
- Dynamic context (from state): Classification results, search results, customer history
- Desired outcome: Professional email response ready for review
Data Steps
When a step needs to retrieve information from external sources:Doc Search Node
Doc Search Node
- Parameters: Query built from intent and topic
- Retry strategy: Yes, with exponential backoff for transient failures
- Caching: Could cache common queries to reduce API calls
Customer History Lookup
Customer History Lookup
- Parameters: Customer email or ID from state
- Retry strategy: Yes, but with fallback to basic info if unavailable
- Caching: Yes, with time-to-live to balance freshness and performance
Action Steps
When a step needs to perform an external action:Send Reply Node
Send Reply Node
- When to execute: After approval (human or automated)
- Retry strategy: Yes, with exponential backoff for network issues
- Should not cache: Each send is a unique action
Bug Track Node
Bug Track Node
- When to execute: Always when intent is “bug”
- Retry strategy: Yes, critical to not lose bug reports
- Returns: Ticket ID to include in response
User Input Steps
When a step needs human intervention:Human Review Node
Human Review Node
- Context for decision: Original email, draft response, urgency, classification
- Expected input format: Approval boolean plus optional edited response
- When triggered: High urgency, complex issues, or quality concerns
Step 3: Design your state
State is the shared memory accessible to all nodes in your agent. Think of it as the notebook your agent uses to keep track of everything it learns and decides as it works through the process.What belongs in state?
Ask yourself these questions about each piece of data:Include in State
Don't Store
- The original email and sender info (can’t reconstruct these)
- Classification results (needed by multiple downstream nodes)
- Search results and customer data (expensive to re-fetch)
- The draft response (needs to persist through review)
- Execution metadata (for debugging and recovery)
Keep state raw, format prompts on-demand
- Different nodes can format the same data differently for their needs
- You can change prompt templates without modifying your state schema
- Debugging is clearer - you see exactly what data each node received
- Your agent can evolve without breaking existing state
Step 4: Build your nodes
Now we implement each step as a function. A node in LangGraph is just a JavaScript function that takes the current state and returns updates to it.Handle errors appropriately
Different errors need different handling strategies:| Error Type | Who Fixes It | Strategy | When to Use |
|---|---|---|---|
| Transient errors (network issues, rate limits) | System (automatic) | Retry policy | Temporary failures that usually resolve on retry |
| LLM-recoverable errors (tool failures, parsing issues) | LLM | Store error in state and loop back | LLM can see the error and adjust its approach |
| User-fixable errors (missing information, unclear instructions) | Human | Pause with interrupt() | Need user input to proceed |
| Unexpected errors | Developer | Let them bubble up | Unknown issues that need debugging |
- Transient errors
- LLM-recoverable
- User-fixable
- Unexpected
Implementing our email agent nodes
We’ll implement each node as a simple function. Remember: nodes take state, do work, and return updates.Read and classify nodes
Read and classify nodes
Search and tracking nodes
Search and tracking nodes
Response nodes
Response nodes
Step 5: Wire it together
Now we connect our nodes into a working graph. Since our nodes handle their own routing decisions, we only need a few essential edges. To enable human-in-the-loop withinterrupt()
, we need to compile with a checkpointer to save state between runs:
Graph compilation code
Graph compilation code
Command
objects. Each node declares where it can go, making the flow explicit and traceable.
Try out your agent
Let’s run our agent with an urgent billing issue that needs human review:Testing the agent
Testing the agent
interrupt()
, saves everything to the checkpointer, and waits. It can resume days later, picking up exactly where it left off. The thread_id ensures all state for this conversation is preserved together.
Summary and next steps
Key Insights
Building this email agent has shown us the LangGraph way of thinking:Break into discrete steps
State is shared memory
Nodes are functions
Errors are part of the flow
Human input is first-class
interrupt()
function pauses execution indefinitely, saves all state, and resumes exactly where it left off when you provide input. When combined with other operations in a node, it must come first.Graph structure emerges naturally
Advanced considerations
Node granularity trade-offs
Node granularity trade-offs
- Isolation of external services: Doc Search and Bug Track are separate nodes because they call external APIs. If the search service is slow or fails, we want to isolate that from the LLM calls. We can add retry policies to these specific nodes without affecting others.
- Intermediate visibility: Having Classify Intent as its own node lets us inspect what the LLM decided before taking action. This is valuable for debugging and monitoring—you can see exactly when and why the agent routes to human review.
- Different failure modes: LLM calls, database lookups, and email sending have different retry strategies. Separate nodes let you configure these independently.
- Reusability and testing: Smaller nodes are easier to test in isolation and reuse in other workflows.
"async"
mode writes checkpoints in the background for good performance while maintaining durability. Use "exit"
mode to checkpoint only at completion (faster for long-running graphs where mid-execution recovery isn’t needed), or "sync"
mode to guarantee checkpoints are written before proceeding to the next step (useful when you need to ensure state is persisted before continuing execution).