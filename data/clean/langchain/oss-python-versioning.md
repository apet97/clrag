---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-versioning",
  "h1": "oss-python-versioning",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.481297",
  "sha256_raw": "6119bc3f5cc88e23ca72b13f27c40120530909fbf86eee5ca7254d08af7e583c"
}
---

# oss-python-versioning

> Source: https://docs.langchain.com/oss/python/versioning

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
MAJOR.MINOR.PATCH
- Major: Breaking API updates that require code changes.
- Minor: New features and improvements that maintain backward compatibility.
- Patch: Bug fixes and minor improvements.
Version numbering
LangChain and LangGraph follow Semantic Versioning principles:1.0.0
: First stable release with production-ready APIs1.1.0
: New features added in a backward-compatible manner1.0.1
: Backward-compatible bug fixes
API stability
We communicate the stability of our APIs as follows:Stable APIs
All APIs without special prefixes are considered stable and ready for production use. We maintain backward compatibility for stable features and only introduce breaking changes in major releases.Beta APIs
APIs marked asbeta
are feature-complete but may undergo minor changes based on user feedback. They are safe for production use but may require small adjustments in future releases.
Alpha APIs
APIs marked asalpha
are experimental and subject to significant changes. Use these with caution in production environments.
Deprecated APIs
APIs marked asdeprecated
will be removed in future major releases. When possible, we specify the intended version of removal. To handle deprecations:
- Switch to the recommended alternative API
- Follow the migration guide (released alongside major releases)
- Use automated migration tools when available
Internal APIs
Certain APIs are explicitly marked as “internal” in a couple of ways:- Some documentation refers to internals and mentions them as such. If the documentation says that something is internal, it may change.
- Functions, methods, and other objects prefixed by a leading underscore (
_
). This is the standard Python convention of indicating that something is private; if any method starts with a single_
, it’s an internal API.- Exception: Certain methods are prefixed with
_
, but do not contain an implementation. These methods are meant to be overridden by sub-classes that provide the implementation. Such methods are generally part of the Public API of LangChain.
- Exception: Certain methods are prefixed with
Release cycles
Major releases
Major releases
Major releases (e.g.,
1.0.0
→ 2.0.0
) may include:- Breaking API changes
- Removal of deprecated features
- Significant architectural improvements
- Detailed migration guides
- Automated migration tools when possible
- Extended support period for the previous major version
Minor releases
Minor releases
Minor releases (e.g.,
1.0.0
→ 1.1.0
) include:- New features and capabilities
- Performance improvements
- New optional parameters
- Backward-compatible enhancements
Patch releases
Patch releases
Patch releases (e.g.,
1.0.0
→ 1.0.1
) include:- Bug fixes
- Security updates
- Documentation improvements
- Performance optimizations without API changes
Version support policy
- Latest major version: Full support with active development
- Previous major version: Security updates and critical bug fixes for 12 months after the next major release
- Older versions: Community support only
Check your version
To check your installed version:Upgrade
Pre-release versions
We occasionally release alpha and beta versions for early testing:- Alpha (e.g.,
1.0.0a1
): Early preview, significant changes expected - Beta (e.g.,
1.0.0b1
): Feature-complete, minor changes possible - Release Candidate (e.g.,
1.0.0rc1
): Final testing before stable release
See also
- Release policy - Detailed release and deprecation policies
- Releases - Version-specific release notes and migration guides