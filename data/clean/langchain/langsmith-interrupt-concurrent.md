---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-interrupt-concurrent",
  "h1": "langsmith-interrupt-concurrent",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.455875",
  "sha256_raw": "d778370404498ba2c28056e2f80c7073a7f367e73cff0297a05653a04c2c6ed0"
}
---

# langsmith-interrupt-concurrent

> Source: https://docs.langchain.com/langsmith/interrupt-concurrent

This guide assumes knowledge of what double-texting is, which you can learn about in the double-texting conceptual guide.The guide covers the interrupt option for double texting, which interrupts the prior run of the graph and starts a new one with the double-text. This option does not delete the first run, but rather keeps it in the database but sets its status to interrupted. Below is a quick example of using the interrupt option.
Now, let’s import our required packages and instantiate our client, assistant, and thread.
Python
Javascript
CURL
Copy
import asynciofrom langchain_core.messages import convert_to_messagesfrom langgraph_sdk import get_clientclient = get_client(url=<DEPLOYMENT_URL>)# Using the graph deployed with the name "agent"assistant_id = "agent"thread = await client.threads.create()
Now we can start our two runs and join the second one until it has completed:
Python
Javascript
CURL
Copy
# the first run will be interruptedinterrupted_run = await client.runs.create( thread["thread_id"], assistant_id, input={"messages": [{"role": "user", "content": "what's the weather in sf?"}]},)# sleep a bit to get partial outputs from the first runawait asyncio.sleep(2)run = await client.runs.create( thread["thread_id"], assistant_id, input={"messages": [{"role": "user", "content": "what's the weather in nyc?"}]}, multitask_strategy="interrupt",)# wait until the second run completesawait client.runs.join(thread["thread_id"], run["run_id"])
We can see that the thread has partial data from the first run + data from the second run
Python
Javascript
CURL
Copy
state = await client.threads.get_state(thread["thread_id"])for m in convert_to_messages(state["values"]["messages"]): m.pretty_print()
Output:
Copy
================================ Human Message =================================what's the weather in sf?================================== Ai Message ==================================[{'id': 'toolu_01MjNtVJwEcpujRGrf3x6Pih', 'input': {'query': 'weather in san francisco'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]Tool Calls:tavily_search_results_json (toolu_01MjNtVJwEcpujRGrf3x6Pih)Call ID: toolu_01MjNtVJwEcpujRGrf3x6PihArgs:query: weather in san francisco================================= Tool Message =================================Name: tavily_search_results_json[{"url": "https://www.wunderground.com/hourly/us/ca/san-francisco/KCASANFR2002/date/2024-6-18", "content": "High 64F. Winds W at 10 to 20 mph. A few clouds from time to time. Low 49F. Winds W at 10 to 20 mph. Temp. San Francisco Weather Forecasts. Weather Underground provides local & long-range weather ..."}]================================ Human Message =================================what's the weather in nyc?================================== Ai Message ==================================[{'id': 'toolu_01KtE1m1ifPLQAx4fQLyZL9Q', 'input': {'query': 'weather in new york city'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]Tool Calls:tavily_search_results_json (toolu_01KtE1m1ifPLQAx4fQLyZL9Q)Call ID: toolu_01KtE1m1ifPLQAx4fQLyZL9QArgs:query: weather in new york city================================= Tool Message =================================Name: tavily_search_results_json[{"url": "https://www.accuweather.com/en/us/new-york/10021/june-weather/349727", "content": "Get the monthly weather forecast for New York, NY, including daily high/low, historical averages, to help you plan ahead."}]================================== Ai Message ==================================The search results provide weather forecasts and information for New York City. Based on the top result from AccuWeather, here are some key details about the weather in NYC:* This is a monthly weather forecast for New York City for the month of June.* It includes daily high and low temperatures to help plan ahead.* Historical averages for June in NYC are also provided as a reference point.* More detailed daily or hourly forecasts with precipitation chances, humidity, wind, etc. can be found by visiting the AccuWeather page.So in summary, the search provides a convenient overview of the expected weather conditions in New York City over the next month to give you an idea of what to prepare for if traveling or making plans there. Let me know if you need any other details!
Verify that the original, interrupted run was interrupted