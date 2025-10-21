---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-contributing-documentation",
  "h1": "oss-python-contributing-documentation",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.476869",
  "sha256_raw": "ba08cfcb24b6c77847ce62ddb30d1950cfdc1181ddf8b5c85a6f8514eb531e02"
}
---

# oss-python-contributing-documentation

> Source: https://docs.langchain.com/oss/python/contributing/documentation

Conceptual guides
References
Tutorials (Learn)
How-to guides
Getting started
Quick edit: fix a typo
For simple changes like fixing typos, you can edit directly on GitHub without setting up a local development environment:Find the page
Fork the repository
Make your changes
Create pull request
Full development IDE setup
For larger changes or ongoing contributions, it’s important to set up a local development environment on your machine. Our documentation build pipeline offers local preview and live reload as you edit, important for ensuring your changes appear as intended before submitting. Please review the steps to set up your environment outlined in the docs repoREADME.md
.
Documentation types
Conceptual guides
Conceptual guide cover core concepts abstractly, providing deep understanding.Characteristics
Characteristics
- Understanding-focused: Explain why things work as they do
- Broad perspective: Higher and wider view than other types
- Design-oriented: Explain decisions and trade-offs
- Context-rich: Use analogies and comparisons
Tips
Tips
- Explain design decisions - “why does concept X exist?”
- Use analogies and reference alternatives
- Avoid blending in too much reference content
- Link to related tutorials and how-to guides
- Focus on the “why” rather than the “how”
References
Reference documentation contains detailed, low-level information describing exactly what functionality exists and how to use it.Python reference
- Describe what exists (all parameters, options, return values)
- Be comprehensive and structured for easy lookup
- Serve as the authoritative source for technical details
LangChain reference best practices
LangChain reference best practices
- Be consistent; follow existing patterns for provider-specific documentation
- Include both basic usage (code snippets) and common edge cases/failure modes
- Note when features require specific versions
When to create new reference documentation
When to create new reference documentation
- New integrations or providers need dedicated reference pages
- Complex configuration options require detailed explanation
- API changes introduce new parameters or behavior
- Community frequently asks questions about specific functionality
Writing standard
Mintlify components
Use appropriate Mintlify components to enhance readability:- Callouts
- Structure
- Code
<Note>
for helpful supplementary information<Warning>
for important cautions and breaking changes<Tip>
for best practices and advice<Info>
for neutral contextual information<Check>
for success confirmations
Page structure
Every documentation page must begin with YAML frontmatter:Localization
All documentation must be localized in both Python and JavaScript/TypeScript when possible. To do so, we use a custom in-line syntax to differentiate between sections that should appear in one or both languages:Quality standards
General guidelines
Avoid duplication
Avoid duplication
Link frequently
Link frequently
Be concise
Be concise
Accessibility requirements
Ensure documentation is accessible to all users:- Structure content for easy scanning with headers and lists
- Use specific, actionable link text instead of “click here”
- Include descriptive alt text for all images and diagrams
Testing and validation
Before submitting documentation:Test all code
Check formatting
Build locally
Review links
In-code documentation
Language and style
Follow these standards for all documentation:- Voice: Use second person (“you”) for instructions
- Tense: Use active voice and present tense
- Clarity: Write clear, direct language for technical audiences
- Consistency: Use consistent terminology throughout
- Conciseness: Keep sentences concise while providing necessary context
Code examples
Completeness
Realism
Error handling
Documentation