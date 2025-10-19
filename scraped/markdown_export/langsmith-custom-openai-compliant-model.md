# langsmith-custom-openai-compliant-model

> Source: https://docs.langchain.com/langsmith/custom-openai-compliant-model

Connect to an OpenAI compliant model provider/proxy
The LangSmith playground allows you to use any model that is compliant with the OpenAI API. You can utilize your model by setting the Proxy Provider for in the playground.
You can use these providers to deploy your model and get an API endpoint that is compliant with the OpenAI API.Take a look at the full specification for more information.
Once you have deployed a model server, you can use it in the LangSmith Playground.To access the Prompt Settings menu:
Under the Prompts heading select the gear icon next to the model name.
In the Model Configuration tab, select the model to edit in the dropdown.
For the Provider dropdown, select OpenAI Compatible Endpoint.
Add your OpenAI Compatible Endpoint to the Base URL input.
If everything is set up correctly, you should see the model’s response in the playground. You can also use this functionality to invoke downstream pipelines as well.For information on how to store your model configuration , refer to Configure prompt settings.