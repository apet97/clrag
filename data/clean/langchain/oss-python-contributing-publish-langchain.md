---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-contributing-publish-langchain",
  "h1": "oss-python-contributing-publish-langchain",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.439602",
  "sha256_raw": "1c53f5ca8eba5fc36a68dc4661b0285acdc51b03f72a3c2f36f0ea0b9eadd71c"
}
---

# oss-python-contributing-publish-langchain

> Source: https://docs.langchain.com/oss/python/contributing/publish-langchain

Important: New integrations should be standalone packages, not PRs to the LangChain monorepo.While LangChain maintains a small subset of first-party and high-usage integrations (like OpenAI, Anthropic, and Ollama) in the main repository, new integrations should be published as separate PyPI packages and repositories (e.g.,
langchain-yourservice
) that users install alongside the core LangChain packages. You should not submit a PR to add your integration directly to the main LangChain repository.Publishing your package
For the purposes of this guide, we’ll be using PyPI as the package registry. You may choose to publish to other registries if you prefer; instructions will vary.
Setup credentials
First, make sure you have a PyPI account:How to create a PyPI Token
How to create a PyPI Token
2
Verify email
Verify your email address by clicking the link that PyPI emails to you
3
Enable 2FA
Go to your account settings and click “Generate Recovery Codes” to enable 2FA. To generate an API token, you must have 2FA enabled
Build and publish
How to publish a package
Helpful guide from
uv
on how to build and publish a package to PyPI.Adding documentation
To add documentation for your package to this site under the integrations tab, you will need to create the relevant documentation pages and open a PR in the LangChain docs repository.Writing docs
Depending on the type of integration you have built, you will need to create different types of documentation pages. LangChain provides templates for different types of integrations to help you get started.To reference existing documentation, you can look at the list of integrations and find similar ones to yours.To view a given documentation page in raw markdown, use the dropdown button next to “Copy page” on the top right of the page and select “View as Markdown”.
Submitting a PR
Make a fork of the LangChain docs repository under a personal GitHub account, and clone it locally. Create a new branch for your integration. Copy the template and modify them using your favorite markdown text editor. Make sure to refer to and follow the documentation guide when writing your documentation.We may reject PRs or ask for modification if:
- CI checks fail
- Severe grammatical errors or typos are present
- Mintlify components are used incorrectly
- Pages are missing a frontmatter
- Localization is missing (where applicable)
- Code examples do not run or have errors
- Quality standards are not met
Next steps
Congratulations! Your integration is now published and documented, making it available to the entire LangChain community.Co-marketing
Get in touch with the LangChain marketing team to explore co-marketing opportunities.