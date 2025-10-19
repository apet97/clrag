# langsmith-manage-datasets-programmatically

> Source: https://docs.langchain.com/langsmith/manage-datasets-programmatically

Create a dataset
Create a dataset from list of values
The most flexible way to make a dataset using the client is by creating examples from a list of inputs and optional outputs. Below is an example. Note that you can add arbitrary metadata to each example, such as a note or a source. The metadata is stored as a dictionary.If you have many examples to create, consider using the
create_examples
/createExamples
method to create multiple examples in a single request. If creating a single example, you can use the create_example
/createExample
method.Create a dataset from traces
To create datasets from the runs (spans) of your traces, you can use the same approach. For many more examples of how to fetch and filter runs, see the export traces guide. Below is an example:Create a dataset from a CSV file
In this section, we will demonstrate how you can create a dataset by uploading a CSV file. First, ensure your CSV file is properly formatted with columns that represent your input and output keys. These keys will be utilized to map your data properly during the upload. You can specify an optional name and description for your dataset. Otherwise, the file name will be used as the dataset name and no description will be provided.Create a dataset from pandas DataFrame (Python only)
The python client offers an additional convenience method to upload a dataset from a pandas dataframe.Fetch datasets
You can programmatically fetch datasets from LangSmith using thelist_datasets
/listDatasets
method in the Python and TypeScript SDKs. Below are some common calls.
Initialize the client before running the below code snippets.
Query all datasets
List datasets by name
If you want to search by the exact name, you can do the following:List datasets by type
You can filter datasets by type. Below is an example querying for chat datasets.Fetch examples
You can programmatically fetch examples from LangSmith using thelist_examples
/listExamples
method in the Python and TypeScript SDKs. Below are some common calls.
Initialize the client before running the below code snippets.
List all examples for a dataset
You can filter by dataset ID:List examples by id
You can also list multiple examples all by ID.List examples by metadata
You can also filter examples by metadata. Below is an example querying for examples with a specific metadata key-value pair. Under the hood, we check to see if the example’s metadata contains the key-value pair(s) you specify. For example, if you have an example with metadata{"foo": "bar", "baz": "qux"}
, both {foo: bar}
and {baz: qux}
would match, as would {foo: bar, baz: qux}
.
List examples by structured filter
Similar to how you can use the structured filter query language to fetch runs, you can use it to fetch examples.This is currently only available in v0.1.83 and later of the Python SDK and v0.1.35 and later of the TypeScript SDK.Additionally, the structured filter query language is only supported for
metadata
fields.has
operator to fetch examples with metadata fields that contain specific key/value pairs and the exists
operator to fetch examples with metadata fields that contain a specific key. Additionally, you can also chain multiple filters together using the and
operator and negate a filter using the not
operator.
Update examples
Update single example
You can programmatically update examples from LangSmith using theupdate_example
/updateExample
method in the Python and TypeScript SDKs. Below is an example.
Bulk update examples
You can also programmatically update multiple examples in a single request with theupdate_examples
/updateExamples
method in the Python and TypeScript SDKs. Below is an example.