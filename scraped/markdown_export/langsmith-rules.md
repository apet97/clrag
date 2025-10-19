# langsmith-rules

> Source: https://docs.langchain.com/langsmith/rules

While you can manually sift through and process production logs from your LLM application, it often becomes difficult as your application scales to more users.
LangSmith provides a powerful feature called Automations that allow you to trigger certain actions on your trace data.
At a high level, automations are defined by a filter, sampling rate, and action.Automation rules can trigger actions such as: adding traces to a dataset, adding to an annotation queue, triggering a webhook (e.g. for remote evaluations) or extending data retention. Some examples of automations you can set up:
Send all traces with negative feedback to an annotation queue for human review
Send 10% of all traces to an annotation queue for human review to spot check for issues
Upgrade all traces with errors for extended data retention
Head to the Tracing Projects tab and select a tracing project. To view existing automation rules for that tracing project, click on the Automations tab.
Head to the Tracing Projects tab and select a tracing project. Click on + New in the top right corner of the tracing project page, then click on New Automation.
Configure a sampling rate to control the percentage of filtered runs that trigger the automation action.You can specify a sampling rate between 0 and 1 for automations. This will control the percent of the filtered runs that are sent to an automation action. For example, if you set the sampling rate to 0.5, then 50% of the traces that pass the filter will be sent to the action.
Apply rule to past runs by toggling the Apply to past runs and entering a “Backfill from” date. This is only possible upon rule creation. Note: the backfill is processed as a background job, so you will not see the results immediately. In order to track progress of the backfill, you can view logs for your automations
Trigger webhook: Trigger a webhook with the trace data. For more information on webhooks, you can refer to this guide.
Extend data retention: Extends the data retention period on matching traces that use base retention (see data retention docs for more details).
Note that all other rules will also extend data retention on matching traces through the
auto-upgrade mechanism described in the aforementioned data retention docs,
but this rule takes no additional action.
Logs allow you to gain confidence that your rules are working as expected. You can view logs for your automations by heading to the Automations tab within a tracing project and clicking the Logs button for the rule you created.The logs tab allows you to:
View all runs processed by a given rule for the time period selected
If a particular rule execution has triggered an error, you can view the error message by hovering over the error icon
You can monitor the progress of a backfill job by filtering to the rule’s creation timestamp. This is because the backfill starts from when the rule was created.
Inspect the run that the automation rule applied to using the View run button. For rules that add runs as examples to datasets, you can view the example produced.