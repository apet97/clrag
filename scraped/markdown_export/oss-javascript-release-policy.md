# oss-javascript-release-policy

> Source: https://docs.langchain.com/oss/javascript/release-policy

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- LangChain
- LangGraph
The LangChain ecosystem is composed of different component packages (e.g.,
@langchain/core
, langchain
, @langchain/community
, partner packages, etc.)Release cadence
We expect to space out minor releases (e.g., from0.2.x
to 0.3.0
) of langchain
and @langchain/core
by at least 2-3 months, as such releases may contain breaking changes.Patch versions are released frequently, up to a few times per week, as they contain bug fixes and new features.API stability
The development of LLM applications is a rapidly evolving field, and we are constantly learning from our users and the community. As such, we expect that the APIs inlangchain
and @langchain/core
will continue to evolve to better serve the needs of our users.- Breaking changes to the public API will result in a minor version bump (the second digit)
- Any bug fixes or new features will result in a patch version bump (the third digit)
Stability of other packages
The stability of other packages in the LangChain ecosystem may vary:-
@langchain/community
is a community maintained package that contains 3rd party integrations. While we do our best to review and test changes in@langchain/community
,@langchain/community
is expected to experience more breaking changes thanlangchain
and@langchain/core
as it contains many community contributions. - Partner packages may follow different stability and versioning policies, and users should refer to the documentation of those packages for more information; however, in general these packages are expected to be stable.
Deprecation policy
We will generally avoid deprecating features until a better alternative is available.When a feature is deprecated, it will continue to work in the current and next minor version oflangchain
and @langchain/core
. After that, the feature will be removed.Since we’re expecting to space out minor releases by at least 2-3 months, this means that a feature can be removed within 2-6 months of being deprecated.In some situations, we may allow the feature to remain in the code base for longer periods of time, if it’s not causing issues in the packages, to reduce the burden on users.