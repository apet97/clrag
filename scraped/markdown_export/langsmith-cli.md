# langsmith-cli

> Source: https://docs.langchain.com/langsmith/cli

LangGraph CLI is a command-line tool for building and running the LangGraph API server locally. The resulting server exposes all API endpoints for runs, threads, assistants, etc., and includes supporting services such as a managed database for checkpointing and storage.
Installation
-
Ensure Docker is installed (e.g.,
docker --version
).
-
Install the CLI:
-
Verify the install
Quick commands
| Command | What it does |
|---|
langgraph dev | Starts a lightweight local dev server (no Docker required), ideal for rapid testing. |
langgraph build | Builds a Docker image of your LangGraph API server for deployment. |
langgraph dockerfile | Emits a Dockerfile derived from your config for custom builds. |
langgraph up | Starts the LangGraph API server locally in Docker. Requires Docker running; LangSmith API key for local dev; license for production. |
For JS, use npx @langchain/langgraph-cli <command>
(or langgraphjs
if installed globally).
Configuration file
The LangGraph CLI requires a JSON configuration file that follows this schema. It contains the following properties:
The LangGraph CLI defaults to using the configuration file langgraph.json in the current directory.
| Key | Description |
|---|
dependencies | Required. Array of dependencies for LangSmith API server. Dependencies can be one of the following: - A single period (
"." ), which will look for local Python packages. - The directory path where
pyproject.toml , setup.py or requirements.txt is located. For example, if requirements.txt is located in the root of the project directory, specify "./" . If it’s located in a subdirectory called local_package , specify "./local_package" . Do not specify the string "requirements.txt" itself. - A Python package name.
|
graphs | Required. Mapping from graph ID to path where the compiled graph or a function that makes a graph is defined. Example: ./your_package/your_file.py:variable , where variable is an instance of langgraph.graph.state.CompiledStateGraph ./your_package/your_file.py:make_graph , where make_graph is a function that takes a config dictionary (langchain_core.runnables.RunnableConfig ) and returns an instance of langgraph.graph.state.StateGraph or langgraph.graph.state.CompiledStateGraph . See how to rebuild a graph at runtime for more details.
|
auth | (Added in v0.0.11) Auth configuration containing the path to your authentication handler. Example: ./your_package/auth.py:auth , where auth is an instance of langgraph_sdk.Auth . See authentication guide for details. |
base_image | Optional. Base image to use for the LangGraph API server. Defaults to langchain/langgraph-api or langchain/langgraphjs-api . Use this to pin your builds to a particular version of the langgraph API, such as "langchain/langgraph-server:0.2" . See https://hub.docker.com/r/langchain/langgraph-server/tags for more details. (added in langgraph-cli==0.2.8 ) |
image_distro | Optional. Linux distribution for the base image. Must be one of "debian" , "wolfi" , "bookworm" , or "bullseye" . If omitted, defaults to "debian" . Available in langgraph-cli>=0.2.11 . |
env | Path to .env file or a mapping from environment variable to its value. |
store | Configuration for adding semantic search and/or time-to-live (TTL) to the BaseStore. Contains the following fields: index (optional): Configuration for semantic search indexing with fields embed , dims , and optional fields .ttl (optional): Configuration for item expiration. An object with optional fields: refresh_on_read (boolean, defaults to true ), default_ttl (float, lifespan in minutes; applied to newly created items only; existing items are unchanged; defaults to no expiration), and sweep_interval_minutes (integer, how often to check for expired items, defaults to no sweeping).
|
ui | Optional. Named definitions of UI components emitted by the agent, each pointing to a JS/TS file. (added in langgraph-cli==0.1.84 ) |
python_version | 3.11 , 3.12 , or 3.13 . Defaults to 3.11 . |
node_version | Specify node_version: 20 to use LangGraph.js. |
pip_config_file | Path to pip config file. |
pip_installer | (Added in v0.3) Optional. Python package installer selector. It can be set to "auto" , "pip" , or "uv" . From version 0.3 onward the default strategy is to run uv pip , which typically delivers faster builds while remaining a drop-in replacement. In the uncommon situation where uv cannot handle your dependency graph or the structure of your pyproject.toml , specify "pip" here to revert to the earlier behaviour. |
keep_pkg_tools | (Added in v0.3.4) Optional. Control whether to retain Python packaging tools (pip , setuptools , wheel ) in the final image. Accepted values: true : Keep all three tools (skip uninstall).false / omitted : Uninstall all three tools (default behaviour).list[str] : Names of tools to retain. Each value must be one of “pip”, “setuptools”, “wheel”. . By default, all three tools are uninstalled. |
dockerfile_lines | Array of additional lines to add to Dockerfile following the import from parent image. |
checkpointer | Configuration for the checkpointer. Contains a ttl field which is an object with the following keys: strategy : How to handle expired checkpoints (e.g., "delete" ).sweep_interval_minutes : How often to check for expired checkpoints (integer).default_ttl : Default time-to-live for checkpoints in minutes (integer); applied to newly created checkpoints/threads only (existing data is unchanged). Defines how long checkpoints are kept before the specified strategy is applied.
|
http | HTTP server configuration with the following fields: app : Path to custom Starlette/FastAPI app (e.g., "./src/agent/webapp.py:app" ). See custom routes guide.cors : CORS configuration with fields for allow_origins , allow_methods , allow_headers , etc.configurable_headers : Define which request headers to exclude or include as a run’s configurable values.disable_assistants : Disable /assistants routesdisable_mcp : Disable /mcp routesdisable_meta : Disable /ok , /info , /metrics , and /docs routesdisable_runs : Disable /runs routesdisable_store : Disable /store routesdisable_threads : Disable /threads routesdisable_ui : Disable /ui routesdisable_webhooks : Disable webhooks calls on run completion in all routesmount_prefix : Prefix for mounted routes (e.g., “/my-deployment/api”)
|
api_version | (Added in v0.3.7) Which semantic version of the LangGraph API server to use (e.g., "0.3" ). Defaults to latest. Check the server changelog for details on each release. |
Examples
Basic Configuration
Using Wolfi Base Images
You can specify the Linux distribution for your base image using the image_distro
field. Valid options are debian
, wolfi
, bookworm
, or bullseye
. Wolfi is the recommended option as it provides smaller and more secure images. This is available in langgraph-cli>=0.2.11
.Adding semantic search to the store
All deployments come with a DB-backed BaseStore. Adding an “index” configuration to your langgraph.json
will enable semantic search within the BaseStore of your deployment.The index.fields
configuration determines which parts of your documents to embed:
- If omitted or set to
["$"]
, the entire document will be embedded
- To embed specific fields, use JSON path notation:
["metadata.title", "content.text"]
- Documents missing specified fields will still be stored but won’t have embeddings for those fields
- You can still override which fields to embed on a specific item at
put
time using the index
parameter
Common model dimensions
openai:text-embedding-3-large
: 3072
openai:text-embedding-3-small
: 1536
openai:text-embedding-ada-002
: 1536
cohere:embed-english-v3.0
: 1024
cohere:embed-english-light-v3.0
: 384
cohere:embed-multilingual-v3.0
: 1024
cohere:embed-multilingual-light-v3.0
: 384
Semantic search with a custom embedding function
If you want to use semantic search with a custom embedding function, you can pass a path to a custom embedding function:The embed
field in store configuration can reference a custom function that takes a list of strings and returns a list of embeddings. Example implementation:Adding custom authentication
See the authentication conceptual guide for details, and the setting up custom authentication guide for a practical walk through of the process.Configuring Store Item Time-to-Live
You can configure default data expiration for items/memories in the BaseStore using the store.ttl
key. This determines how long items are retained after they are last accessed (with reads potentially refreshing the timer based on refresh_on_read
). Note that these defaults can be overwritten on a per-call basis by modifying the corresponding arguments in get
, search
, etc.The ttl
configuration is an object containing optional fields:
refresh_on_read
: If true
(the default), accessing an item via get
or search
resets its expiration timer. Set to false
to only refresh TTL on writes (put
).
default_ttl
: The default lifespan of an item in minutes. Applies only to newly created items; existing items are not modified. If not set, items do not expire by default.
sweep_interval_minutes
: How frequently (in minutes) the system should run a background process to delete expired items. If not set, sweeping does not occur automatically.
Here is an example enabling a 7-day TTL (10080 minutes), refreshing on reads, and sweeping every hour:Configuring Checkpoint Time-to-Live
You can configure the time-to-live (TTL) for checkpoints using the checkpointer
key. This determines how long checkpoint data is retained before being automatically handled according to the specified strategy (e.g., deletion). The ttl
configuration is an object containing:
strategy
: The action to take on expired checkpoints (currently "delete"
is the only accepted option).
sweep_interval_minutes
: How frequently (in minutes) the system checks for expired checkpoints.
default_ttl
: The default lifespan of a checkpoint in minutes. Applies only to checkpoints/threads created after deployment; existing data is not modified.
Here’s an example setting a default TTL of 30 days (43200 minutes):In this example, checkpoints older than 30 days will be deleted, and the check runs every 10 minutes.Pinning API Version
(Added in v0.3.7)You can pin the API version of the LangGraph server by using the api_version
key. This is useful if you want to ensure that your server uses a specific version of the API.
By default, builds in Cloud deployments use the latest stable version of the server. This can be pinned by setting the api_version
key to a specific version.
Commands
Usage
The base command for the LangGraph CLI is langgraph
.
dev
Run LangGraph API server in development mode with hot reloading and debugging capabilities. This lightweight server requires no Docker installation and is suitable for development and testing. State is persisted to a local directory.Currently, the CLI only supports Python >= 3.11.
InstallationThis command requires the “inmem” extra to be installed:UsageOptions| Option | Default | Description |
|---|
-c, --config FILE | langgraph.json | Path to configuration file declaring dependencies, graphs and environment variables |
--host TEXT | 127.0.0.1 | Host to bind the server to |
--port INTEGER | 2024 | Port to bind the server to |
--no-reload | | Disable auto-reload |
--n-jobs-per-worker INTEGER | | Number of jobs per worker. Default is 10 |
--debug-port INTEGER | | Port for debugger to listen on |
--wait-for-client | False | Wait for a debugger client to connect to the debug port before starting the server |
--no-browser | | Skip automatically opening the browser when the server starts |
--studio-url TEXT | | URL of the Studio instance to connect to. Defaults to https://smith.langchain.com |
--allow-blocking | False | Do not raise errors for synchronous I/O blocking operations in your code (added in 0.2.6 ) |
--tunnel | False | Expose the local server via a public tunnel (Cloudflare) for remote frontend access. This avoids issues with browsers like Safari or networks blocking localhost connections |
--help | | Display command documentation |
build
Build LangSmith API server Docker image.UsageOptions| Option | Default | Description |
|---|
--platform TEXT | | Target platform(s) to build the Docker image for. Example: langgraph build --platform linux/amd64,linux/arm64 |
-t, --tag TEXT | | Required. Tag for the Docker image. Example: langgraph build -t my-image |
--pull / --no-pull | --pull | Build with latest remote Docker image. Use --no-pull for running the LangSmith API server with locally built images. |
-c, --config FILE | langgraph.json | Path to configuration file declaring dependencies, graphs and environment variables. |
--build-command TEXT * | | Build command to run. Runs from the directory where your langgraph.json file lives. Example: langgraph build --build-command "yarn run turbo build" |
--install-command TEXT * | | Install command to run. Runs from the directory where you call langgraph build from. Example: langgraph build --install-command "yarn install" |
--help | | Display command documentation. |
*Only supported for JS deployments, will have no impact on Python deployments.
Start LangGraph API server. For local testing, requires a LangSmith API key with access to LangSmith. Requires a license key for production use.UsageOptions| Option | Default | Description |
|---|
--wait | | Wait for services to start before returning. Implies —detach |
--base-image TEXT | langchain/langgraph-api | Base image to use for the LangGraph API server. Pin to specific versions using version tags. |
--image TEXT | | Docker image to use for the langgraph-api service. If specified, skips building and uses this image directly. |
--postgres-uri TEXT | Local database | Postgres URI to use for the database. |
--watch | | Restart on file changes |
--debugger-base-url TEXT | http://127.0.0.1:[PORT] | URL used by the debugger to access LangGraph API. |
--debugger-port INTEGER | | Pull the debugger image locally and serve the UI on specified port |
--verbose | | Show more output from the server logs. |
-c, --config FILE | langgraph.json | Path to configuration file declaring dependencies, graphs and environment variables. |
-d, --docker-compose FILE | | Path to docker-compose.yml file with additional services to launch. |
-p, --port INTEGER | 8123 | Port to expose. Example: langgraph up --port 8000 |
--pull / --no-pull | pull | Pull latest images. Use --no-pull for running the server with locally-built images. Example: langgraph up --no-pull |
--recreate / --no-recreate | no-recreate | Recreate containers even if their configuration and image haven’t changed |
--help | | Display command documentation. |
dockerfile
Generate a Dockerfile for building a LangSmith API server Docker image.UsageOptions| Option | Default | Description |
|---|
-c, --config FILE | langgraph.json | Path to the configuration file declaring dependencies, graphs and environment variables. |
--help | | Show this message and exit. |
Example:This generates a Dockerfile that looks similar to:The langgraph dockerfile
command translates all the configuration in your langgraph.json
file into Dockerfile commands. When using this command, you will have to re-run it whenever you update your langgraph.json
file. Otherwise, your changes will not be reflected when you build or run the dockerfile.