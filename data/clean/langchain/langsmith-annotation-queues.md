---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-annotation-queues",
  "h1": "langsmith-annotation-queues",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.434886",
  "sha256_raw": "1242f9614909a4844587e61ba18db409acda63a63cabfa2ebf51df27b2ce905c"
}
---

# langsmith-annotation-queues

> Source: https://docs.langchain.com/langsmith/annotation-queues

Create an annotation queue
To create an annotation queue, navigate to the Annotation queues section through the homepage or left-hand navigation bar. Then click + New annotation queue in the top right corner.Basic Details
Fill in the form with the name and description of the queue. You can also assign a default dataset to queue, which will streamline the process of sending the inputs and outputs of certain runs to datasets in your LangSmith workspace.Annotation Rubric
Begin by drafting some high-level instructions for your annotators, which will be shown in the sidebar on every run. Next, click ”+ Desired Feedback” to add feedback keys to your annotation queue. Annotators will be presented with these feedback keys on each run. Add a description for each, as well as a short description of each category if the feedback is categorical. Reviewers will see this:Collaborator Settings
There are a few settings related to multiple annotators:-
Number of reviewers per run: This determines the number of reviewers that must mark a run as “Done” for it to be removed from the queue. If you check “All workspace members review each run,” then a run will remain in the queue until all workspace members have marked it “Done”.
- Reviewers cannot view the feedback left by other reviewers.
- Comments on runs are visible to all reviewers.
- Enable reservations on runs: We recommend enabling reservations. This will prevent multiple annotators from reviewing the same run at the same time.
- How do reservations work?
- What happens if time runs out?
Clicking “Requeue at end” will only move the current run to the end of the current user’s queue; it won’t affect the queue order of any other user. It will also release the reservation that the current user has on that run.
Assign runs to an annotation queue
To assign runs to an annotation queue, either:- Click on Add to Annotation Queue in top right corner of any trace view. You can add ANY intermediate run (span) of the trace to an annotation queue, not just the root span.
- Select multiple runs in the runs table then click Add to Annotation Queue at the bottom of the page.
- Set up an automation rule that automatically assigns runs which pass a certain filter and sampling condition to an annotation queue.
- Select one or multiple experiments from the dataset page and click Annotate. From the resulting popup, you may either create a new queue or add the runs to an existing one:
It is often a very good idea to assign runs that have a certain user feedback score (eg thumbs up, thumbs down) from the application to an annotation queue. This way, you can identify and address issues that are causing user dissatisfaction. To learn more about how to capture user feedback from your LLM application, follow this guide.