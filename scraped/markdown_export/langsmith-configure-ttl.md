# langsmith-configure-ttl

> Source: https://docs.langchain.com/langsmith/configure-ttl

LangSmith persists both checkpoints (thread state) and cross-thread memories (store items). Configure Time-to-Live (TTL) policies in
langgraph.json
to automatically manage the lifecycle of this data, preventing indefinite accumulation.
Configuring Checkpoint TTL
Checkpoints capture the state of conversation threads. Setting a TTL ensures old checkpoints and threads are automatically deleted. Add acheckpointer.ttl
configuration to your langgraph.json
file:
strategy
: Specifies the action taken on expiration. Currently, only"delete"
is supported, which deletes all checkpoints in the thread upon expiration.sweep_interval_minutes
: Defines how often, in minutes, the system checks for expired checkpoints.default_ttl
: Sets the default lifespan of threads (and corresponding checkpoints) in minutes (e.g., 43200 minutes = 30 days). Applies only to checkpoints created after this configuration is deployed; existing checkpoints/threads are not changed. To clear older data, delete it explicitly.
Configuring Store Item TTL
Store items allow cross-thread data persistence. Configuring TTL for store items helps manage memory by removing stale data. Add astore.ttl
configuration to your langgraph.json
file:
refresh_on_read
: (Optional, defaulttrue
) Iftrue
, accessing an item viaget
orsearch
resets its expiration timer. Iffalse
, TTL only refreshes onput
.sweep_interval_minutes
: (Optional) Defines how often, in minutes, the system checks for expired items. If omitted, no sweeping occurs.default_ttl
: (Optional) Sets the default lifespan of store items in minutes (e.g., 10080 minutes = 7 days). Applies only to items created after this configuration is deployed; existing items are not changed. If you need to clear older items, delete them manually. If omitted, items do not expire by default.
Combining TTL Configurations
You can configure TTLs for both checkpoints and store items in the samelanggraph.json
file to set different policies for each data type. Here is an example:
Runtime Overrides
The defaultstore.ttl
settings from langgraph.json
can be overridden at runtime by providing specific TTL values in SDK method calls like get
, put
, and search
.
Deployment Process
After configuring TTLs inlanggraph.json
, deploy or restart your LangGraph application for the changes to take effect. Use langgraph dev
for local development or langgraph up
for Docker deployment.
See the langgraph.json CLI reference for more details on the other configurable options.