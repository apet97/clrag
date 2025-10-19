# oss-javascript-langchain-guardrails

> Source: https://docs.langchain.com/oss/javascript/langchain/guardrails

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- Preventing PII leakage
- Detecting and blocking prompt injection attacks
- Blocking inappropriate or harmful content
- Enforcing business rules and compliance requirements
- Validating output quality and accuracy
Guardrails can be implemented using two complementary approaches:
Deterministic guardrails
Use rule-based logic like regex patterns, keyword matching, or explicit checks. Fast, predictable, and cost-effective, but may miss nuanced violations.
Model-based guardrails
Use LLMs or classifiers to evaluate content with semantic understanding. Catch subtle issues that rules miss, but are slower and more expensive.
Built-in guardrails
PII detection
LangChain provides built-in middleware for detecting and handling Personally Identifiable Information (PII) in conversations. This middleware can detect common PII types like emails, credit cards, IP addresses, and more. PII detection middleware is helpful for cases such as health care and financial applications with compliance requirements, customer service agents that need to sanitize logs, and generally any application handling sensitive user data. The PII middleware supports multiple strategies for handling detected PII:| Strategy | Description | Example |
|---|---|---|
redact | Replace with [REDACTED_TYPE] | [REDACTED_EMAIL] |
mask | Partially obscure (e.g., last 4 digits) | ****-****-****-1234 |
hash | Replace with deterministic hash | a8f5f167... |
block | Raise exception when detected | Error thrown |
Built-in PII types and configuration
Built-in PII types and configuration
Built-in PII types:
email
- Email addressescredit_card
- Credit card numbers (Luhn validated)ip
- IP addressesmac_address
- MAC addressesurl
- URLs
| Parameter | Description | Default |
|---|---|---|
piiType | Type of PII to detect (built-in or custom) | Required |
strategy | How to handle detected PII ("block" , "redact" , "mask" , "hash" ) | "redact" |
detector | Custom detector regex pattern | undefined (uses built-in) |
applyToInput | Check user messages before model call | true |
applyToOutput | Check AI messages after model call | false |
applyToToolResults | Check tool result messages after execution | false |
Human-in-the-loop
LangChain provides built-in middleware for requiring human approval before executing sensitive operations. This is one of the most effective guardrails for high-stakes decisions. Human-in-the-loop middleware is helpful for cases such as financial transactions and transfers, deleting or modifying production data, sending communications to external parties, and any operation with significant business impact.Custom guardrails
For more sophisticated guardrails, you can create custom middleware that runs before or after the agent executes. This gives you full control over validation logic, content filtering, and safety checks.Before agent guardrails
Use “before agent” hooks to validate requests once at the start of each invocation. This is useful for session-level checks like authentication, rate limiting, or blocking inappropriate requests before any processing begins.After agent guardrails
Use “after agent” hooks to validate final outputs once before returning to the user. This is useful for model-based safety checks, quality validation, or final compliance scans on the complete agent response.Combine multiple guardrails
You can stack multiple guardrails by adding them to the middleware array. They execute in order, allowing you to build layered protection:Additional resources
- Middleware documentation - Complete guide to custom middleware
- Middleware API reference - Complete guide to custom middleware
- Human-in-the-loop - Add human review for sensitive operations
- Testing agents - Strategies for testing safety mechanisms