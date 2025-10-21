---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-rate-limiting",
  "h1": "langsmith-rate-limiting",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.451212",
  "sha256_raw": "84a33caa7c16745e292cec604e1ad2a16a50bfc23c2fe611e60aa516062c76c2"
}
---

# langsmith-rate-limiting

> Source: https://docs.langchain.com/langsmith/rate-limiting

A common issue when running large evaluation jobs is running into third-party API rate limits, usually from model providers. There are a few ways to deal with rate limits.
If you’re using langchain Python ChatModels in your application or evaluators, you can add rate limiters to your model(s) that will add client-side control of the frequency with which requests are sent to the model provider API to avoid rate limit errors.
Copy
from langchain.chat_models import init_chat_modelfrom langchain_core.rate_limiters import InMemoryRateLimiterrate_limiter = InMemoryRateLimiter( requests_per_second=0.1, # <-- Super slow! We can only make a request once every 10 seconds!! check_every_n_seconds=0.1, # Wake up every 100 ms to check whether allowed to make a request, max_bucket_size=10, # Controls the maximum burst size.)llm = init_chat_model("gpt-4o", rate_limiter=rate_limiter)def app(inputs: dict) -> dict: response = llm.invoke(...) ...def evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> dict: response = llm.invoke(...) ...
See the langchain documentation for more on how to configure rate limiters.
A very common way to deal with rate limit errors is retrying with exponential backoff. Retrying with exponential backoff means repeatedly retrying failed requests with an (exponentially) increasing wait time between each retry. This continues until either the request succeeds or a maximum number of requests is made.
If you’re not using langchain you can use other libraries like tenacity (Python) or backoff (Python) to implement retries with exponential backoff, or you can implement it from scratch. See some examples of how to do this in the OpenAI docs.
Limiting the number of concurrent calls you’re making to your application and evaluators is another way to decrease the frequency of model calls you’re making, and in that way avoid rate limit errors. max_concurrency can be set directly on the evaluate() / aevaluate() functions. This parallelizes evaluation by effectively splitting the dataset across threads.
Copy
from langsmith import aevaluateresults = await aevaluate( ... max_concurrency=4,)