---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-contributing-standard-tests-langchain",
  "h1": "oss-javascript-contributing-standard-tests-langchain",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.454055",
  "sha256_raw": "82fd7b17e616a8bfa1096b4e2fb19d62a2b4d8fe5e581d0389528722fc511a31"
}
---

# oss-javascript-contributing-standard-tests-langchain

> Source: https://docs.langchain.com/oss/javascript/contributing/standard-tests-langchain

Setup
First, install the required dependencies:langchain-core
Defines the interfaces we want to import to define our custom components
langchain-tests
Provides the standard tests and plugins necessary to run them
langchain-tests
package:
Unit tests
Unit tests
Location:
src.unit_tests
Designed to test the component in isolation and without access to external servicesIntegration tests
Integration tests
Location:
src.integration_tests
Designed to test the component with access to external services (in particular, the external service that the component is designed to interact with)Implementing standard tests
Depending on your integration type, you will need to implement either or both unit and integration tests. By subclassing the standard test suite for your integration type, you get the full collection of standard tests for that type. For a test run to be successful, the a given test should pass only if the model supports the capability being tested. Otherwise, the test should be skipped. Because different integrations offer unique sets of features, most standard tests provided by LangChain are opt-in by default to prevent false positives. Consequently, you will need to override properties to indicate which features your integration supports - see the below example for an illustration.tests/chat_models.standard.int.test.ts
You should typically organize tests in these subdirectories relative to the root of your package:
tests/unit_tests
for unit teststests/integration_tests
for integration tests
- Unit tests
- Integration tests