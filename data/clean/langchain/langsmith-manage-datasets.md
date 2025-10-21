---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-manage-datasets",
  "h1": "langsmith-manage-datasets",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.457324",
  "sha256_raw": "7c36af1a7f4a275112894e901c432858be9282433506ffdffe720ad1a8a3a90b"
}
---

# langsmith-manage-datasets

> Source: https://docs.langchain.com/langsmith/manage-datasets

- Versioning datasets to track changes over time.
- Filtering and splitting datasets for evaluation.
- Sharing datasets publicly.
- Exporting datasets in various formats.
Version a dataset
In LangSmith, datasets are versioned. This means that every time you add, update, or delete examples in your dataset, a new version of the dataset is created.Create a new version of a dataset
Any time you add, update, or delete examples in your dataset, a new version of your dataset is created. This allows you to track changes to your dataset over time and understand how your dataset has evolved. By default, the version is defined by the timestamp of the change. When you click on a particular version of a dataset (by timestamp) in the Examples tab, you will find the state of the dataset at that point in time. Note that examples are read-only when viewing a past version of the dataset. You will also see the operations that were between this version of the dataset and the latest version of the dataset.By default, the latest version of the dataset is shown in the Examples tab and experiments from all versions are shown in the Tests tab.
Tag a version
You can also tag versions of your dataset to give them a more human-readable name, which can be useful for marking important milestones in your dataset’s history. For example, you might tag a version of your dataset as “prod” and use it to run tests against your LLM pipeline. You can tag a version of your dataset in the UI by clicking on + Tag this version in the Examples tab. You can also tag versions of your dataset using the SDK. Here’s an example of how to tag a version of a dataset using the Python SDK:Evaluate on a specific dataset version
Use list_examples
You can use evaluate
/ aevaluate
to pass in an iterable of examples to evaluate on a particular version of a dataset. Use list_examples
/ listExamples
to fetch examples from a particular version tag using as_of
/ asOf
and pass that into the data
argument.
Evaluate on a split / filtered view of a dataset
Evaluate on a filtered view of a dataset
You can use thelist_examples
/ listExamples
method to fetch a subset of examples from a dataset to evaluate on.
One common workflow is to fetch examples that have a certain metadata key-value pair.
Evaluate on a dataset split
You can use thelist_examples
/ listExamples
method to evaluate on one or multiple splits of your dataset. The splits
parameter takes a list of the splits you would like to evaluate.
Share a dataset
Share a dataset publicly
Sharing a dataset publicly will make the dataset examples, experiments and associated runs, and feedback on this dataset accessible to anyone with the link, even if they don’t have a LangSmith account. Make sure you’re not sharing sensitive information.This feature is only available in the cloud-hosted version of LangSmith.
Unshare a dataset
- Click on Unshare by clicking on Public in the upper right hand corner of any publicly shared dataset, then Unshare in the dialog.
- Navigate to your organization’s list of publicly shared datasets, by clicking on Settings -> Shared URLs or this link, then click on Unshare next to the dataset you want to unshare.