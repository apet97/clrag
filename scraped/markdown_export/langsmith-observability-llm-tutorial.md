# langsmith-observability-llm-tutorial

> Source: https://docs.langchain.com/langsmith/observability-llm-tutorial

Prototyping
Having observability set up from the start can help you iterate much more quickly than you would otherwise be able to. It allows you to have great visibility into your application as you are rapidly iterating on the prompt, or changing the data and models you are using. In this section we’ll walk through how to set up observability so you can have maximal observability as you are prototyping.Set up your environment
First, create an API key by navigating to the settings page. Next, install the LangSmith SDK:default
project (though you can easily change that).
You may see these variables referenced as
LANGCHAIN_*
in other places. These are all equivalent, however the best practice is to use LANGSMITH_TRACING
, LANGSMITH_API_KEY
, LANGSMITH_PROJECT
.The LANGSMITH_PROJECT
flag is only supported in JS SDK versions >= 0.2.16, use LANGCHAIN_PROJECT
instead if you are using an older version.Trace your LLM calls
The first thing you might want to trace is all your OpenAI calls. After all, this is where the LLM is actually being called, so it is the most important part! We’ve tried to make this as easy as possible with LangSmith by introducing a dead-simple OpenAI wrapper. All you have to do is modify your code to look something like:from langsmith.wrappers import wrap_openai
and use it to wrap the OpenAI client (openai_client = wrap_openai(OpenAI())
).
What happens if you call it in the following way?
Trace the whole chain
Great - we’ve traced the LLM call. But it’s often very informative to trace more than that. LangSmith is built for tracing the entire LLM pipeline - so let’s do that! We can do this by modifying the code to now look something like this:from langsmith import traceable
and use it decorate the overall function (@traceable
).
What happens if you call it in the following way?
Beta Testing
The next stage of LLM application development is beta testing your application. This is when you release it to a few initial users. Having good observability set up here is crucial as often you don’t know exactly how users will actually use your application, so this allows you get insights into how they do so. This also means that you probably want to make some changes to your tracing set up to better allow for that. This extends the observability you set up in the previous sectionCollecting Feedback
A huge part of having good observability during beta testing is collecting feedback. What feedback you collect is often application specific - but at the very least a simple thumbs up/down is a good start. After logging that feedback, you need to be able to easily associate it with the run that caused that. Luckily LangSmith makes it easy to do that. First, you need to log the feedback from your app. An easy way to do this is to keep track of a run ID for each run, and then use that to log feedback. Keeping track of the run ID would look something like:Metadata
tab when inspecting the run. It should look something like this
You can also query for all runs with positive (or negative) feedback by using the filtering logic in the runs table. You can do this by creating a filter like the following:
Logging Metadata
It is also a good idea to start logging metadata. This allows you to start keep track of different attributes of your app. This is important in allowing you to know what version or variant of your app was used to produce a given result. For this example, we will log the LLM used. Oftentimes you may be experimenting with different LLMs, so having that information as metadata can be useful for filtering. In order to do that, we can add it as such:@traceable(metadata={"llm": "gpt-4o-mini"})
to the rag
function.
Keeping track of metadata in this way assumes that it is known ahead of time. This is fine for LLM types, but less desirable for other types of information - like a User ID. In order to log information that, we can pass it in at run time with the run ID.
Production
Great - you’ve used this newfound observability to iterate quickly and gain confidence that your app is performing well. Time to ship it to production! What new observability do you need to add? First of all, let’s note that the same observability you’ve already added will keep on providing value in production. You will continue to be able to drill down into particular runs. In production you likely have a LOT more traffic. So you don’t really want to be stuck looking at datapoints one at a time. Luckily, LangSmith has a set of tools to help with observability in production.Monitoring
If you click on theMonitor
tab in a project, you will see a series of monitoring charts. Here we track lots of LLM specific statistics - number of traces, feedback, time-to-first-token, etc. You can view these over time across a few different time bins.
A/B Testing
Group-by functionality for A/B testing requires at least 2 different values to exist for a given metadata key.
llm
. We can group the monitoring charts by ANY metadata attribute, and instantly get grouped charts over time. This allows us to experiment with different LLMs (or prompts, or other) and track their performance over time.
In order to do this, we just need to click on the Metadata
button at the top. This will give us a drop down of options to choose from to group by:
Once we select this, we will start to see charts grouped by this attribute: