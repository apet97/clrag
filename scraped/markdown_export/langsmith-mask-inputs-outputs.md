# langsmith-mask-inputs-outputs

> Source: https://docs.langchain.com/langsmith/mask-inputs-outputs

Client
instance. This can be done by setting the hide_inputs
and hide_outputs
parameters on the Client
object (hideInputs
and hideOutputs
in TypeScript).
For the example below, we will simply return an empty object for both hide_inputs
and hide_outputs
, but you can customize this to your needs.
Rule-based masking of inputs and outputs
This feature is available in the following LangSmith SDK versions:
- Python: 0.1.81 and above
- TypeScript: 0.1.33 and above
create_anonymizer
/ createAnonymizer
function and pass the newly created anonymizer when instantiating the client. The anonymizer can be either constructed from a list of regex patterns and the replacement values or from a function that accepts and returns a string value.
The anonymizer will be skipped for inputs if LANGSMITH_HIDE_INPUTS = true
. Same applies for outputs if LANGSMITH_HIDE_OUTPUTS = true
.
However, if inputs or outputs are to be sent to client, the anonymizer
method will take precedence over functions found in hide_inputs
and hide_outputs
. By default, the create_anonymizer
will only look at maximum of 10 nesting levels deep, which can be configured via the max_depth
parameter.
Older versions of LangSmith SDKs can use the
hide_inputs
and hide_outputs
parameters to achieve the same effect. You can also use these parameters to process the inputs and outputs more efficiently as well.
Processing Inputs & Outputs for a Single Function
The
process_outputs
parameter is available in LangSmith SDK version 0.1.98 and above for Python.process_inputs
and process_outputs
parameters of the @traceable
decorator.
These parameters accept functions that allow you to transform the inputs and outputs of a specific function before they are logged to LangSmith. This is useful for reducing payload size, removing sensitive information, or customizing how an object should be serialized and represented in LangSmith for a particular function.
Here’s an example of how to use process_inputs
and process_outputs
:
process_inputs
creates a new dictionary with processed input data, and process_outputs
transforms the output into a specific format before logging to LangSmith.
It’s recommended to avoid mutating the source objects in the processor functions. Instead, create and return new objects with the processed data.
hide_inputs
and hide_outputs
) when both are defined.
Quick starts
You can combine rule-based masking with various anonymizers to scrub sensitive information from inputs and outputs. In this how-to-guide, we’ll cover working with regex, Microsoft Presidio, and Amazon Comprehend.Regex
The implementation below is not exhaustive and may miss some formats or edge cases. Test any implementation thoroughly before using it in production.
Microsoft Presidio
The implementation below provides a general example of how to anonymize sensitive information in messages exchanged between a user and an LLM. It is not exhaustive and does not account for all cases. Test any implementation thoroughly before using it in production.
Amazon Comprehend
The implementation below provides a general example of how to anonymize sensitive information in messages exchanged between a user and an LLM. It is not exhaustive and does not account for all cases. Test any implementation thoroughly before using it in production.