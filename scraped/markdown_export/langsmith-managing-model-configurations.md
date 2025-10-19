# langsmith-managing-model-configurations

> Source: https://docs.langchain.com/langsmith/managing-model-configurations

Model configurations define the parameters your prompt runs against. In the LangSmith Playground, you can save and manage these configurations, which allows you to reuse your preferred settings across prompts and sessions. For details on specific settings, refer to your model provider’s documentation (for example, Anthropic, OpenAI).
In the Model Configurations tab, adjust the model configuration as needed—you can select a saved configuration to edit.
Click the Save As button in the top bar.
Enter a name and optional description for your configuration and confirm.
Now that you’ve saved the configuration, anyone in your organization’s workspace can access it. All saved configurations are available in the Model Configuration dropdown.
Once you have created a saved configuration, you can set it as your default, so any new prompt you create will automatically use this configuration. To set a configuration as your default, click the Set as default icon next to the model name in the dropdown.
The Extra Parameters field allows you to pass additional model parameters that aren’t directly supported in the LangSmith interface. This is particularly useful in two scenarios:
When model providers release new parameters that haven’t yet been integrated into the LangSmith interface. You can specify these parameters in JSON format to use them right away. For example:
Copy
{ "reasoning_effort": "medium"}
When troubleshooting parameter-related errors in the playground, such as:
Copy
TypeError: AsyncCompletions.create() got an unexpected keyword argument 'max_concurrency'
If you receive an error about unnecessary parameters (which is more common when using LangChain JS for run tracing), you can use this field to remove the extra parameters.
Tools enable your LLM to perform tasks like searching the web, looking up information, and so on. In the Tools Settings tab, you can manage the ways your LLM uses and accesses the tools you have defined in your prompt, including:
Parallel Tool Calls: Calling multiple tools in parallel when appropriate. This allows the model to gather information from different sources simultaneously. (Dependent on model support for parallel execution.)
Tool Choice: Select the tools that the model can access. For more details, refer to Use tools in a prompt.