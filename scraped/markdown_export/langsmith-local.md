# langsmith-local

> Source: https://docs.langchain.com/langsmith/local

upload_results=False
to evaluate()
/ aevaluate()
.
This will run you application and evaluators exactly as it always does and return the same output, but nothing will be recorded to LangSmith. This includes not just the experiment results but also the application and evaluator traces.
Example
Let’s take a look at an example: Requireslangsmith>=0.2.0
. Example also uses pandas
.
| inputs.question | outputs.answer | reference.answer | feedback.is_concise | |
|---|---|---|---|---|
| 0 | What is the largest mammal? | What is the largest mammal? is a good question. I don’t know the answer. | The blue whale | False |
| 1 | What do mammals and birds have in common? | What do mammals and birds have in common? is a good question. I don’t know the answer. | They are both warm-blooded | False |