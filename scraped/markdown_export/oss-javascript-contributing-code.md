# oss-javascript-contributing-code

> Source: https://docs.langchain.com/oss/javascript/contributing/code

Philosophy
Aim to follow these core principles for all code contributions:Backwards compatibility
Testing first
Code quality
Security focused
Getting started
Quick fix: submit a bugfix
For simple bugfixes, you can get started immediately:Clone and setup
Create a branch
Run build
Run tests
Full development setup
For ongoing development or larger contributions:Development environment
- LangChain
- LangGraph
Repository structure
- LangChain
- LangGraph
Core packages
Core packages
Partner packages
Partner packages
libs/providers/
, these are independently versioned packages for specific integrations. For example:@langchain/openai
: OpenAI integrations@langchain/anthropic
: Anthropic integrations@langchain/google-genai
: Google Generative AI integrations
Development workflow
Testing requirements
Unit tests
src/tests/FILENAME_BEING_TESTED.test.ts
Requirements:- No network calls allowed
- Test all code paths including edge cases
- Use mocks for external dependencies
Integration tests
src/tests/FILENAME_BEING_TESTED.int.test.ts
Requirements:- Test real integrations with external services
- Use environment variables for API keys
- Skip gracefully if credentials unavailable
Test quality checklist
- Tests fail when your code is broken
- Edge cases and error conditions are tested
- Proper use of fixtures and mocks
Code quality standards
Quality requirements:- Type hints
- Documentation
- Code style
Contribution guidelines
Backwards compatibility
Stable interfaces
Stable interfaces
- Function signatures and parameter names
- Class interfaces and method names
- Return value structure and types
- Import paths for public APIs
Safe changes
Safe changes
- Adding new optional parameters/type parameters
- Adding new methods to classes
- Improving performance without changing behavior
- Adding new modules or functions
Before making changes
Before making changes
- Would this break existing user code?
- Check if your target is public
- Are there existing usage patterns in tests?
Bugfixes
For bugfix contributions:Reproduce the issue
Write failing tests
Implement the fix
Verify the fix
Document the change
New features
We aim to keep the bar high for new features. We generally don’t accept new core abstractions, changes to infra, changes to dependencies, or new agents/chains from outside contributors without an existing issue that demonstrates an acute need for them. In general, feature contribution requirements include:Design discussion
- The problem you’re solving
- Proposed API design
- Expected usage patterns
Implementation
- Follow existing code patterns
- Include comprehensive tests and documentation
- Consider security implications
Integration considerations
- How does this interact with existing features?
- Are there performance implications?
- Does this introduce new dependencies?
Security guidelines
Input validation
Input validation
- Validate and sanitize all user inputs
- Properly escape data in templates and queries
-
Never use
eval()
, as this can lead to arbitrary code execution vulnerabilities
Error handling
Error handling
- Use specific exception types
- Don’t expose sensitive information in error messages
- Implement proper resource cleanup
Dependencies
Dependencies
- Avoid adding hard dependencies
- Keep optional dependencies minimal
- Review third-party packages for security issues
Testing and validation
Running tests locally
Before submitting your PR, ensure you have completed the following steps. Note that the requirements differ slightly between LangChain and LangGraph.- LangChain
- LangGraph
Unit tests
Integration tests
Formatting
PR submission
Test writing guidelines
In order to write effective tests, there’s a few good practices to follow:- Encapsulate the test in a
describe
block that describes the component being tested - Use natural language to describe the test name
- Be exhaustive with assertions
- Only use snapshots for reasonably sized data objects
- Unit tests
- Integration tests
- Mock usage