# langsmith-metric-type

> Source: https://docs.langchain.com/langsmith/metric-type

LangSmith supports both categorical and numerical metrics, and you can return either when writing a custom evaluator.For an evaluator result to be logged as a numerical metric, it must returned as:
(Python only) an int, float, or bool
a dict of the form {"key": "metric_name", "score": int | float | bool}
For an evaluator result to be logged as a categorical metric, it must be returned as:
(Python only) a str
a dict of the form {"key": "metric_name", "value": str | int | float | bool}
Here are some examples:
Python: Requires langsmith>=0.2.0
TypeScript: Support for multiple scores is available in langsmith@0.1.32 and higher