# langsmith-log-traces-to-project

> Source: https://docs.langchain.com/langsmith/log-traces-to-project

Set the destination project statically
As mentioned in the Tracing Concepts section, LangSmith uses the concept of aProject
to group traces. If left unspecified, the project is set to default
. You can set the LANGSMITH_PROJECT
environment variable to configure a custom project name for an entire application run. This should be done before executing your application.
The
LANGSMITH_PROJECT
flag is only supported in JS SDK versions >= 0.2.16, use LANGCHAIN_PROJECT
instead if you are using an older version.Set the destination project dynamically
You can also set the project name at program runtime in various ways, depending on how you are annotating your code for tracing. This is useful when you want to log traces to different projects within the same application.Setting the project name dynamically using one of the below methods overrides the project name set by the
LANGSMITH_PROJECT
environment variable.