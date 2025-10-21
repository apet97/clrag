---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-rollback-concurrent",
  "h1": "langsmith-rollback-concurrent",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.451840",
  "sha256_raw": "739225385f27cf406d2b0b6f6baad9b9e8968e2f9eed969379eb73c6b66b63e7"
}
---

# langsmith-rollback-concurrent

> Source: https://docs.langchain.com/langsmith/rollback-concurrent

This guide assumes knowledge of what double-texting is, which you can learn about in the double-texting conceptual guide.The guide covers the rollback option for double texting, which interrupts the prior run of the graph and starts a new one with the double-text. This option is very similar to the interrupt option, but in this case the first run is completely deleted from the database and cannot be restarted. Below is a quick example of using the rollback option.
Now, let’s import our required packages and instantiate our client, assistant, and thread.
Python
Javascript
CURL
Copy
import asyncioimport httpxfrom langchain_core.messages import convert_to_messagesfrom langgraph_sdk import get_clientclient = get_client(url=<DEPLOYMENT_URL>)# Using the graph deployed with the name "agent"assistant_id = "agent"thread = await client.threads.create()
Now let’s run a thread with the multitask parameter set to “rollback”:
Python
Javascript
CURL
Copy
# the first run will be rolled backrolled_back_run = await client.runs.create( thread["thread_id"], assistant_id, input={"messages": [{"role": "user", "content": "what's the weather in sf?"}]},)run = await client.runs.create( thread["thread_id"], assistant_id, input={"messages": [{"role": "user", "content": "what's the weather in nyc?"}]}, multitask_strategy="rollback",)# wait until the second run completesawait client.runs.join(thread["thread_id"], run["run_id"])
We can see that the thread has data only from the second run
Python
Javascript
CURL
Copy
state = await client.threads.get_state(thread["thread_id"])for m in convert_to_messages(state["values"]["messages"]): m.pretty_print()
Output:
Copy
================================ Human Message =================================what's the weather in nyc?================================== Ai Message ==================================[{'id': 'toolu_01JzPqefao1gxwajHQ3Yh3JD', 'input': {'query': 'weather in nyc'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]Tool Calls:tavily_search_results_json (toolu_01JzPqefao1gxwajHQ3Yh3JD)Call ID: toolu_01JzPqefao1gxwajHQ3Yh3JDArgs:query: weather in nyc================================= Tool Message =================================Name: tavily_search_results_json[{"url": "https://www.weatherapi.com/", "content": "{'location': {'name': 'New York', 'region': 'New York', 'country': 'United States of America', 'lat': 40.71, 'lon': -74.01, 'tz_id': 'America/New_York', 'localtime_epoch': 1718734479, 'localtime': '2024-06-18 14:14'}, 'current': {'last_updated_epoch': 1718733600, 'last_updated': '2024-06-18 14:00', 'temp_c': 29.4, 'temp_f': 84.9, 'is_day': 1, 'condition': {'text': 'Sunny', 'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png', 'code': 1000}, 'wind_mph': 2.2, 'wind_kph': 3.6, 'wind_degree': 158, 'wind_dir': 'SSE', 'pressure_mb': 1025.0, 'pressure_in': 30.26, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 63, 'cloud': 0, 'feelslike_c': 31.3, 'feelslike_f': 88.3, 'windchill_c': 28.3, 'windchill_f': 82.9, 'heatindex_c': 29.6, 'heatindex_f': 85.3, 'dewpoint_c': 18.4, 'dewpoint_f': 65.2, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 7.0, 'gust_mph': 16.5, 'gust_kph': 26.5}}"}]================================== Ai Message ==================================The weather API results show that the current weather in New York City is sunny with a temperature of around 85°F (29°C). The wind is light at around 2-3 mph from the south-southeast. Overall it looks like a nice sunny summer day in NYC.
Verify that the original, rolled back run was deleted
Python
Javascript
Copy
try: await client.runs.get(thread["thread_id"], rolled_back_run["run_id"])except httpx.HTTPStatusError as _: print("Original run was correctly deleted")