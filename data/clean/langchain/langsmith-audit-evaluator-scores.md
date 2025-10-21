---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-audit-evaluator-scores",
  "h1": "langsmith-audit-evaluator-scores",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.453675",
  "sha256_raw": "ce560b564bd82c8ac2d0d963e139b96258e14a6346a38c85ccfd1a1a44cea2cf"
}
---

# langsmith-audit-evaluator-scores

> Source: https://docs.langchain.com/langsmith/audit-evaluator-scores

LLM-as-a-judge evaluators don’t always get it right. Because of this, it is often useful for a human to manually audit the scores left by an evaluator and correct them where necessary. LangSmith allows you to make corrections on evaluator scores in the UI or SDK.
In the comparison view, you may click on any feedback tag to bring up the feedback details. From there, click the “edit” icon on the right to bring up the corrections view. You may then type in your desired score in the text box under “Make correction”. If you would like, you may also attach an explanation to your correction. This is useful if you are using a few-shot evaluator and will be automatically inserted into your few-shot examples in place of the few_shot_explanation prompt variable.
In the runs table, find the “Feedback” column and click on the feedback tag to bring up the feedback details. Again, click the “edit” icon on the right to bring up the corrections view.
Corrections can be made via the SDK’s update_feedback function, with the correction dict. You must specify a score key which corresponds to a number for it to be rendered in the UI.