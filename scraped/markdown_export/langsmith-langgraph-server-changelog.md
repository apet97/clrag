# langsmith-langgraph-server-changelog

> Source: https://docs.langchain.com/langsmith/langgraph-server-changelog

LangGraph Server is an API platform for creating and managing agent-based applications. It provides built-in persistence, a task queue, and supports deploying, configuring, and running assistants (agentic workflows) at scale. This changelog documents all notable updates, features, and fixes to LangGraph Server releases.
Resolved a timezone issue in the core API, ensuring accurate time data retrieval.
Introduced a new middleware_order setting to apply authentication middleware before custom middleware, allowing finer control over protected route configurations.
Logged the Redis URL when errors occur during Redis client creation.
Improved Go engine/runtime context propagation to ensure consistent execution flow.
Removed the unnecessary assistants.put call from the executor entrypoint to streamline the process.
Added support for context when using stream_mode="events" and included new tests for this functionality.
Added support for overriding the server port using $LANGGRAPH_SERVER_PORT and removed an unnecessary Dockerfile ARG for cleaner configuration.
Applied authorization filters to all table references in thread delete CTE to enhance security.
Introduced self-hosted metrics ingestion capability, allowing metrics to be sent to an OTLP collector every minute when the corresponding environment variables are set.
Ensured that the set_latest function properly updates the name and description of the version.
Added a format parameter to the queue metrics server for enhanced customization.
Corrected MOUNT_PREFIX environment variable usage in CLI for consistency with documentation and to prevent confusion.
Added a feature to log warnings when messages are dropped due to no subscribers, controllable via a feature flag.
Added support for Bookworm and Bullseye distributions in Node images.
Consolidated executor definitions by moving them from the langgraph-go repository, improving manageability and updating the checkpointer setup method for server migrations.
Ensured correct response headers are sent for a2a, improving compatibility and communication.
Consolidated PostgreSQL checkpoint implementation, added CI testing for the /core directory, fixed RemoteStore test errors, and enhanced the Store implementation with transactions.
Added PostgreSQL migrations to the queue server to prevent errors from graphs being added before migrations are performed.
Added timeouts to specific Redis calls to prevent workers from being left active.
Updated the Golang runtime and added pytest skips for unsupported functionalities, including initial support for passing store to node and message streaming.
Introduced a reverse proxy setup for serving combined Python and Node.js graphs, with nginx handling server routing, to facilitate a Postgres/Redis backend for the Node.js API server.
Set a default 15-minute statement timeout and implemented monitoring for long-running queries to ensure system efficiency.
Stop propagating run configurable values to the thread configuration, because this can cause issues on subsequent runs if you are specifying a checkpoint_id. This is a slight breaking change in behavior, since the thread value will no longer automatically reflect the unioned configuration of the most recent run. We believe this behavior is more intuitive, however.
Enhanced compatibility with older worker versions by handling event data in channel names within ops.py.
Added a feature flag (FF_RICH_THREADS=false) to disable thread updates on run creation, reducing lock contention and simplifying thread status handling.
Utilized existing connections for aput and apwrite operations to improve performance.
Improved error handling for decoding issues to enhance data processing reliability.
Excluded headers from logs to improve security while maintaining runtime functionality.
Fixed an error that prevented mapping slots to a single node.
Added debug logs to track node execution in JS deployments for improved issue diagnosis.
Changed the default multitask strategy to enqueue, improving throughput by eliminating the need to fetch inflight runs during new run insertions.
Optimized database operations for Runs.next and Runs.sweep to reduce redundant queries and improve efficiency.
Improved run creation speed by skipping unnecessary inflight runs queries.
Restored the original streaming behavior of runs, ensuring consistent inclusion of interrupt events based on stream_mode settings.
Optimized Runs.next query to reduce average execution time from ~14.43ms to ~2.42ms, improving performance.
Added support for stream mode “tasks” and “checkpoints”, normalized the UI namespace, and upgraded @langchain/langgraph-api for enhanced functionality.
Added a composite index on threads for faster searches with owner-based authentication and updated the default sort order to updated_at for improved query performance.
Improved interoperability with the ckpt ingestion worker on the main loop to prevent task scheduling issues.
Delayed queue worker startup until after migrations are completed to prevent premature execution.
Enhanced thread state error handling by adding specific metadata and improved response codes for better clarity when state updates fail during creation.
Exposed the interrupt ID when retrieving the thread state to improve API transparency.
Reduced writes to the checkpoint_blobs table by inlining small values (null, numeric, str, etc.). This means we don’t need to store extra values for channels that haven’t been updated.
Handled CancelledError by marking tasks as ready to retry, improving error management in worker processes.
Added LG API version and request ID to metadata and logs for better tracking.
Added LG API version and request ID to metadata and logs to improve traceability.
Improved database performance by creating indexes concurrently.
Ensured postgres write is committed only after the Redis running marker is set to prevent race conditions.
Enhanced query efficiency and reliability by adding a unique index on thread_id/running, optimizing row locks, and ensuring deterministic run selection.
Resolved a race condition by ensuring Postgres updates only occur after the Redis running marker is set.