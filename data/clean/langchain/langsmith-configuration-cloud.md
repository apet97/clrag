---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-configuration-cloud",
  "h1": "langsmith-configuration-cloud",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.441369",
  "sha256_raw": "d2c76c189fc6d18b868f1ed3e540b9138837e09e04ad3a4d9ae747027903648a"
}
---

# langsmith-configuration-cloud

> Source: https://docs.langchain.com/langsmith/configuration-cloud

call_model
node and context schema.
Observe that this node tries to read and use the model_name
as defined by the context
object’s model_name
field.
- Python
- Javascript
Create an assistant
LangGraph SDK
To create an assistant, use the LangGraph SDKcreate
method. See the Python and JS SDK reference docs for more information.
This example uses the same context schema as above, and creates an assistant with model_name
set to openai
.
- Python
- Javascript
- CURL
LangSmith UI
You can also create assistants from the LangSmith UI. Inside your deployment, select the “Assistants” tab. This will load a table of all of the assistants in your deployment, across all graphs. To create a new assistant, select the ”+ New assistant” button. This will open a form where you can specify the graph this assistant is for, as well as provide a name, description, and the desired configuration for the assistant based on the configuration schema for that graph. To confirm, click “Create assistant”. This will take you to Studio where you can test the assistant. If you go back to the “Assistants” tab in the deployment, you will see the newly created assistant in the table.Use an assistant
LangGraph SDK
We have now created an assistant called “Open AI Assistant” that hasmodel_name
defined as openai
. We can now use this assistant with this configuration:
- Python
- Javascript
- CURL
LangSmith UI
Inside your deployment, select the “Assistants” tab. For the assistant you would like to use, click the Studio button. This will open Studio with the selected assistant. When you submit an input (either in Graph or Chat mode), the selected assistant and its configuration will be used.Create a new version for your assistant
LangGraph SDK
To edit the assistant, use theupdate
method. This will create a new version of the assistant with the provided edits. See the Python and JS SDK reference docs for more information.
Note
You must pass in the ENTIRE context (and metadata if you are using it). The update endpoint creates new versions completely from scratch and does not rely on previous versions.
- Python
- Javascript
- CURL
LangSmith UI
You can also edit assistants from the LangSmith UI. Inside your deployment, select the “Assistants” tab. This will load a table of all of the assistants in your deployment, across all graphs. To edit an existing assistant, select the “Edit” button for the specified assistant. This will open a form where you can edit the assistant’s name, description, and configuration. Additionally, if using Studio, you can edit the assistants and create new versions via the “Manage Assistants” button.Use a previous assistant version
LangGraph SDK
You can also change the active version of your assistant. To do so, use thesetLatest
method.
In the example above, to rollback to the first version of the assistant:
- Python
- Javascript
- CURL
LangSmith UI
If using Studio, to set the active version of your assistant, click the “Manage Assistants” button and locate the assistant you would like to use. Select the assistant and the version, and then click the “Active” toggle. This will update the assistant to make the selected version active.Deleting Assistants
Deleting as assistant will delete ALL of its versions. There is currently no way to delete a single version, but by pointing your assistant to the correct version you can skip any versions that you don’t wish to use.