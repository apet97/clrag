# langsmith-use-webhooks

> Source: https://docs.langchain.com/langsmith/use-webhooks

webhook
parameter. If this parameter is specified by an endpoint that can accept POST requests, LangSmith will send a request at the completion of a run.
When working with LangSmith, you may want to use webhooks to receive updates after an API call completes. Webhooks are useful for triggering actions in your service once a run has finished processing. To implement this, you need to expose an endpoint that can accept POST
requests and pass this endpoint as a webhook
parameter in your API request.
Currently, the SDK does not provide built-in support for defining webhook endpoints, but you can specify them manually using API requests.
Supported endpoints
The following API endpoints accept awebhook
parameter:
| Operation | HTTP Method | Endpoint |
|---|---|---|
| Create Run | POST | /thread/{thread_id}/runs |
| Create Thread Cron | POST | /thread/{thread_id}/runs/crons |
| Stream Run | POST | /thread/{thread_id}/runs/stream |
| Wait Run | POST | /thread/{thread_id}/runs/wait |
| Create Cron | POST | /runs/crons |
| Stream Run Stateless | POST | /runs/stream |
| Wait Run Stateless | POST | /runs/wait |
Set up your assistant and thread
Before making API calls, set up your assistant and thread.- Python
- JavaScript
- CURL
Use a webhook with a graph run
To use a webhook, specify thewebhook
parameter in your API request. When the run completes, LangSmith sends a POST
request to the specified webhook URL.
For example, if your server listens for webhook events at https://my-server.app/my-webhook-endpoint
, include this in your request:
- Python
- JavaScript
- CURL
Webhook payload
LangSmith sends webhook notifications in the format of a Run. See the API Reference for details. The request payload includes run input, configuration, and other metadata in thekwargs
field.
Secure webhooks
To ensure only authorized requests hit your webhook endpoint, consider adding a security token as a query parameter:Disable webhooks
As oflanggraph-api>=0.2.78
, developers can disable webhooks in the langgraph.json
file:
Test webhooks
You can test your webhook using online services like:- Beeceptor – Quickly create a test endpoint and inspect incoming webhook payloads.
- Webhook.site – View, debug, and log incoming webhook requests in real time.