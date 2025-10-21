---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-index-datasets-for-dynamic-few-shot-example-selection",
  "h1": "langsmith-index-datasets-for-dynamic-few-shot-example-selection",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.432879",
  "sha256_raw": "9ced03f8024ece4999d010898aca11fcd9a75e9c7c563d58bc9d2b79a80f7d36"
}
---

# langsmith-index-datasets-for-dynamic-few-shot-example-selection

> Source: https://docs.langchain.com/langsmith/index-datasets-for-dynamic-few-shot-example-selection

Configure your datasets so that you can search for few shot examples based on an incoming request.
Pre-conditions
- Your dataset must use the KV store data type (we do not currently support chat model or LLM type datasets)
- You must have an input schema defined for your dataset. See our docs on setting up schema validation in our UI for details.
- You must be on a paid team plan (e.g. Plus plan)
- You must be on LangSmith cloud
Index your dataset for few shot search
Navigate to the datasets UI, and click the newFew-Shot search
tab. Hit the Start sync
button, which will create a new index on your dataset to make it searchable.
By default, we sync to the latest version of your dataset. That means when new examples are added to your dataset, they will automatically be added to your index. This process runs every few minutes, so there should be a very short delay for indexing new examples. You can see whether your index is up to date under Few-shot index
on the lefthand side of the screen in the next section.
Test search quality in the few shot playground
Now that you have turned on indexing for your dataset, you will see the new few shot playground. You can type in a sample input, and check which results would be returned by our search API. Each result will have a score and a link to the example in the dataset. The scoring system works such that 0 is a completely random result, and higher scores are better. Results will be sorted in descending order according to score.Search uses a BM25-like algorithm for keyword based similarity scores. The actual score is subject to change as we improve the search algorithm, so we recommend not relying on the scores themselves, as their meaning may evolve over time. They are simply used for convenience in vibe-testing outputs in the playground.
Adding few shot search to your application
Click theGet Code Snippet
button in the previous diagram, you’ll be taken to a screen that has code snippets from our LangSmith SDK in different languages.
For code samples on using few shot search in LangChain python applications, please see our how-to guide in the LangChain docs.
Code snippets
Please ensure you are using the python SDK with version >= 1.101 or the typescript SDK with version >= 1.43