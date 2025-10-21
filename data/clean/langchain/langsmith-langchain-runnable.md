---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-langchain-runnable",
  "h1": "langsmith-langchain-runnable",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.462867",
  "sha256_raw": "43b624660f40844d7f1048fd8fac1e9e0b81a234600c0e8fa01a188f973dd71b"
}
---

# langsmith-langchain-runnable

> Source: https://docs.langchain.com/langsmith/langchain-runnable

Let’s define a simple chain to evaluate. First, install all the required packages:
Copy
pip install -U langsmith langchain[openai]
Now define a chain:
Copy
from langchain.chat_models import init_chat_modelfrom langchain_core.prompts import ChatPromptTemplatefrom langchain_core.output_parsers import StrOutputParserinstructions = ( "Please review the user query below and determine if it contains any form " "of toxic behavior, such as insults, threats, or highly negative comments. " "Respond with 'Toxic' if it does, and 'Not toxic' if it doesn't.")prompt = ChatPromptTemplate( [("system", instructions), ("user", "{text}")],)llm = init_chat_model("gpt-4o")chain = prompt | llm | StrOutputParser()
To evaluate our chain we can pass it directly to the evaluate() / aevaluate() method. Note that the input variables of the chain must match the keys of the example inputs. In this case, the example inputs should have the form {"text": "..."}.
Copy
from langsmith import aevaluate, Clientclient = Client()# Clone a dataset of texts with toxicity labels.# Each example input has a "text" key and each output has a "label" key.dataset = client.clone_public_dataset( "https://smith.langchain.com/public/3d6831e6-1680-4c88-94df-618c8e01fc55/d")def correct(outputs: dict, reference_outputs: dict) -> bool: # Since our chain outputs a string not a dict, this string # gets stored under the default "output" key in the outputs dict: actual = outputs["output"] expected = reference_outputs["label"] return actual == expectedresults = await aevaluate( chain, data=dataset, evaluators=[correct], experiment_prefix="gpt-4o, baseline",)
The runnable is traced appropriately for each output.