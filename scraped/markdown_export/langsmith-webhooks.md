# langsmith-webhooks

> Source: https://docs.langchain.com/langsmith/webhooks

Webhook payload
The payload we send to your webhook endpoint contains:"rule_id"
: this is the ID of the automation that sent this payload"start_time"
and"end_time"
: these are the time boundaries where we found matching runs"runs"
: this is an array of runs, where each run is a dictionary. If you need more information about each run we suggest using our SDK in your endpoint to fetch it from our API."feedback_stats"
: this is a dictionary with the feedback statistics for the runs. An example payload for this field is shown below.
fetching from S3 URLsDepending on how recent your runs are, the
inputs_s3_urls
and outputs_s3_urls
fields may contain S3 URLs to the actual data instead of the data itself.The inputs
and outputs
can be fetched by the ROOT.presigned_url
provided in inputs_s3_urls
and outputs_s3_urls
respectively.Security
We strongly recommend you add a secret query string parameter to the webhook URL, and verify it on any incoming request. This ensures that if someone discovers your webhook URL you can distinguish those calls from authentic webhook notifications. An example would beWebhook custom HTTP headers
If you’d like to send any specific headers with your webhook, this can be configured per URL. To set this up, click on theHeaders
option next to the URL field and add your headers.
Headers are stored in encrypted format.
Webhook Delivery
When delivering events to your webhook endpoint we follow these guidelines- If we fail to connect to your endpoint, we retry the transport connection up to 2 times, before declaring the delivery failed.
- If your endpoint takes longer than 5 seconds to reply we declare the delivery failed and do not .
- If your endpoint returns a 5xx status code in less than 5 seconds we retry up to 2 times with exponential backoff.
- If your endpoint returns a 4xx status code, we declare the delivery failed and do not retry.
- Anything your endpoint returns in the body will be ignored
Example with Modal
Setup
For an example of how to set this up, we will use Modal. Modal provides autoscaling GPUs for inference and fine-tuning, secure containerization for code agents, and serverless Python web endpoints. We’ll focus on the web endpoints here. First, create a Modal account. Then, locally install the Modal SDK:Secrets
Next, you will need to set up some secrets in Modal. First, LangSmith will need to authenticate to Modal by passing in a secret. The easiest way to do this is to pass in a secret in the query parameters. To validate this secret, we will need to add a secret in Modal to validate it. We will do that by creating a Modal secret. You can see instructions for secrets here. For this purpose, let’s call our secretls-webhook
and have it set an environment variable with the name LS_WEBHOOK
.
We can also set up a LangSmith secret - luckily there is already an integration template for this!
Service
After that, you can create a Python file that will serve as your endpoint. An example is below, with comments explaining what is going on:modal deploy ...
(see docs here).
You should now get something like:
https://hwchase17--auth-example-f.modal.run
- the function we created to run.
NOTE: this is NOT the final deployment URL, make sure not to accidentally use that.
Hooking it up
We can now take the function URL we create above and add it as a webhook. We have to remember to also pass in the secret key as a query parameter. Putting it all together, it should look something like:{SECRET}
with the secret key you created to access the Modal service.