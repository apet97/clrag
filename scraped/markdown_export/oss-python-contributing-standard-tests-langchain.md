# oss-python-contributing-standard-tests-langchain

> Source: https://docs.langchain.com/oss/python/contributing/standard-tests-langchain

Setup
First, install the required dependencies:langchain-core
Defines the interfaces we want to import to define our custom components
langchain-tests
Provides the standard tests and
pytest
plugins necessary to run themlangchain-tests
package:
Unit tests
Unit tests
Location:
langchain_tests.unit_tests
Designed to test the component in isolation and without access to external servicesIntegration tests
Integration tests
Location:
langchain_tests.integration_tests
Designed to test the component with access to external services (in particular, the external service that the component is designed to interact with)pytest
class-based test suites.
Implementing standard tests
Depending on your integration type, you will need to implement either or both unit and integration tests. By subclassing the standard test suite for your integration type, you get the full collection of standard tests for that type. For a test run to be successful, the a given test should pass only if the model supports the capability being tested. Otherwise, the test should be skipped. Because different integrations offer unique sets of features, most standard tests provided by LangChain are opt-in by default to prevent false positives. Consequently, you will need to override properties to indicate which features your integration supports - see the below example for an illustration.tests/integration_tests/test_standard.py
You should typically organize tests in these subdirectories relative to the root of your package:
tests/unit_tests
for unit teststests/integration_tests
for integration tests
Running tests
If bootstrapping an integration from a template, aMakefile
is provided that includes targets for running unit and integration tests:
Troubleshooting
For a full list of the standard test suites that are available, as well as information on which tests are included and how to troubleshoot common issues, see the Standard Tests API Reference. You can find troubleshooting guides under the individual test suites listed in that API Reference. For example, here is the guide forChatModelIntegrationTests.test_usage_metadata
.