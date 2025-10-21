---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-auth",
  "h1": "langsmith-auth",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.486917",
  "sha256_raw": "a8282c5211ac694f03514a431f8e8383ec01f17e68cf4fe7a58fac968b73da59"
}
---

# langsmith-auth

> Source: https://docs.langchain.com/langsmith/auth

Core Concepts
Authentication vs Authorization
While often used interchangeably, these terms represent distinct security concepts:- Authentication (“AuthN”) verifies who you are. This runs as middleware for every request.
- Authorization (“AuthZ”) determines what you can do. This validates the user’s privileges and roles on a per-resource basis.
@auth.authenticate
handler, and authorization is handled by your @auth.on
handlers.
Default Security Models
LangSmith provides different security defaults:LangSmith
- Uses LangSmith API keys by default
- Requires valid API key in
x-api-key
header - Can be customized with your auth handler
Custom auth
Custom auth is supported for all plans in LangSmith.
Self-Hosted
- No default authentication
- Complete flexibility to implement your security model
- You control all aspects of authentication and authorization
System Architecture
A typical authentication setup involves three main components:- Authentication Provider (Identity Provider/IdP)
- A dedicated service that manages user identities and credentials
- Handles user registration, login, password resets, etc.
- Issues tokens (JWT, session tokens, etc.) after successful authentication
- Examples: Auth0, Supabase Auth, Okta, or your own auth server
- LangGraph Backend (Resource Server)
- Your LangGraph application that contains business logic and protected resources
- Validates tokens with the auth provider
- Enforces access control based on user identity and permissions
- Doesn’t store user credentials directly
- Client Application (Frontend)
- Web app, mobile app, or API client
- Collects time-sensitive user credentials and sends to auth provider
- Receives tokens from auth provider
- Includes these tokens in requests to LangGraph backend
@auth.authenticate
handler in LangGraph handles steps 4-6, while your @auth.on
handlers implement step 7.
Authentication
Authentication in LangGraph runs as middleware on every request. Your@auth.authenticate
handler receives request information and should:
- Validate the credentials
- Return user info containing the user’s identity and user information if valid
- Raise an HTTP exception or AssertionError if invalid
- To your authorization handlers via
ctx.user
- In your application via
config["configuration"]["langgraph_auth_user"]
Supported Parameters
Supported Parameters
The
@auth.authenticate
handler can accept any of the following parameters by name:- request (Request): The raw ASGI request object
- body (dict): The parsed request body
- path (str): The request path, e.g.,
"/threads/abcd-1234-abcd-1234/runs/abcd-1234-abcd-1234/stream"
- method (str): The HTTP method, e.g.,
"GET"
- path_params (dict[str, str]): URL path parameters, e.g.,
{"thread_id": "abcd-1234-abcd-1234", "run_id": "abcd-1234-abcd-1234"}
- query_params (dict[str, str]): URL query parameters, e.g.,
{"stream": "true"}
- headers (dict[bytes, bytes]): Request headers
- authorization (str | None): The Authorization header value (e.g.,
"Bearer <token>"
)
Agent authentication
Custom authentication permits delegated access. The values you return in@auth.authenticate
are added to the run context, giving agents user-scoped credentials lets them access resources on the user’s behalf.
After authentication, the platform creates a special configuration object that is passed to your graph and all nodes via the configurable context.
This object contains information about the current user, including any custom fields you return from your @auth.authenticate
handler.
To enable an agent to act on behalf of the user, use custom authentication middleware. This will allow the agent to interact with external systems like MCP servers, external databases, and even other agents on behalf of the user.
For more information, see the Use custom auth guide.
Agent authentication with MCP
For information on how to authenticate an agent to an MCP server, see the MCP conceptual guide.Authorization
After authentication, LangGraph calls your@auth.on
handlers to control access to specific resources (e.g., threads, assistants, crons). These handlers can:
- Add metadata to be saved during resource creation by mutating the
value["metadata"]
dictionary directly. See the supported actions table for the list of types the value can take for each action. - Filter resources by metadata during search/list or read operations by returning a filter dictionary.
- Raise an HTTP exception if access is denied.
@auth.on
handler for all resources and actions. If you want to have different control depending on the resource and action, you can use resource-specific handlers. See the Supported Resources section for a full list of the resources that support access control.
Resource-Specific Handlers
You can register handlers for specific resources and actions by chaining the resource and action names together with the@auth.on
decorator.
When a request is made, the most specific handler that matches that resource and action is called. Below is an example of how to register handlers for specific resources and actions. For the following setup:
- Authenticated users are able to create threads, read threads, and create runs on threads
- Only users with the “assistants:create” permission are allowed to create new assistants
- All other endpoints (e.g., e.g., delete assistant, crons, store) are disabled for all users.
thread
would match the on_thread_create
handler but NOT the reject_unhandled_requests
handler. A request to update
a thread, however would be handled by the global handler, since we don’t have a more specific handler for that resource and action.
Filter Operations
Authorization handlers can returnNone
, a boolean, or a filter dictionary.
None
andTrue
mean “authorize access to all underling resources”False
means “deny access to all underling resources (raises a 403 exception)”- A metadata filter dictionary will restrict access to resources
- The default value is a shorthand for exact match, or “$eq”, below. For example,
{"owner": user_id}
will include only resources with metadata containing{"owner": user_id}
$eq
: Exact match (e.g.,{"owner": {"$eq": user_id}}
) - this is equivalent to the shorthand above,{"owner": user_id}
$contains
: List membership (e.g.,{"allowed_users": {"$contains": user_id}}
) or list containment (e.g.,{"allowed_users": {"$contains": [user_id_1, user_id_2]}}
). The value here must be an element of the list or a subset of the elements of the list, respectively. The metadata in the stored resource must be a list/container type.
AND
filter. For example, {"owner": org_id, "allowed_users": {"$contains": user_id}}
will only match resources with metadata whose “owner” is org_id
and whose “allowed_users” list contains user_id
.
See the reference here for more information.
Common Access Patterns
Here are some typical authorization patterns:Single-Owner Resources
This common pattern lets you scope all threads, assistants, crons, and runs to a single user. It’s useful for common single-user use cases like regular chatbot-style apps.Permission-based Access
This pattern lets you control access based on permissions. It’s useful if you want certain roles to have broader or more restricted access to resources.Supported Resources
LangGraph provides three levels of authorization handlers, from most general to most specific:- Global Handler (
@auth.on
): Matches all resources and actions - Resource Handler (e.g.,
@auth.on.threads
,@auth.on.assistants
,@auth.on.crons
): Matches all actions for a specific resource - Action Handler (e.g.,
@auth.on.threads.create
,@auth.on.threads.read
): Matches a specific action on a specific resource
@auth.on.threads.create
takes precedence over @auth.on.threads
for thread creation.
If a more specific handler is registered, the more general handler will not be called for that resource and action.
“Type Safety”
Each handler has type hints available for its More specific handlers provide better type hints since they handle fewer action types.
value
parameter at Auth.types.on.<resource>.<action>.value
. For example:Supported actions and types
Here are all the supported action handlers:| Resource | Handler | Description | Value Type |
|---|---|---|---|
| Threads | @auth.on.threads.create | Thread creation | ThreadsCreate |
@auth.on.threads.read | Thread retrieval | ThreadsRead | |
@auth.on.threads.update | Thread updates | ThreadsUpdate | |
@auth.on.threads.delete | Thread deletion | ThreadsDelete | |
@auth.on.threads.search | Listing threads | ThreadsSearch | |
@auth.on.threads.create_run | Creating or updating a run | RunsCreate | |
| Assistants | @auth.on.assistants.create | Assistant creation | AssistantsCreate |
@auth.on.assistants.read | Assistant retrieval | AssistantsRead | |
@auth.on.assistants.update | Assistant updates | AssistantsUpdate | |
@auth.on.assistants.delete | Assistant deletion | AssistantsDelete | |
@auth.on.assistants.search | Listing assistants | AssistantsSearch | |
| Crons | @auth.on.crons.create | Cron job creation | CronsCreate |
@auth.on.crons.read | Cron job retrieval | CronsRead | |
@auth.on.crons.update | Cron job updates | CronsUpdate | |
@auth.on.crons.delete | Cron job deletion | CronsDelete | |
@auth.on.crons.search | Listing cron jobs | CronsSearch |
“About Runs”Runs are scoped to their parent thread for access control. This means permissions are typically inherited from the thread, reflecting the conversational nature of the data model. All run operations (reading, listing) except creation are controlled by the thread’s handlers.
There is a specific
create_run
handler for creating new runs because it had more arguments that you can view in the handler.Next Steps
For implementation details:- Check out the introductory tutorial on setting up authentication
- See the how-to guide on implementing a custom auth handlers