---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-vitest-jest",
  "h1": "langsmith-vitest-jest",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.444787",
  "sha256_raw": "c5a2a20ec76f210e5aadef5f55a9bcb97251485e3bb3cc5519e5fe2aaf7bdf14"
}
---

# langsmith-vitest-jest

> Source: https://docs.langchain.com/langsmith/vitest-jest

evaluate()
evaluation flow, this is useful when:
- Each example requires different evaluation logic
- You want to assert binary expectations, and both track these assertions in LangSmith and raise assertion errors locally (e.g. in CI pipelines)
- You want to take advantage of mocks, watch mode, local results, or other features of the Vitest/Jest ecosystems
Requires JS/TS SDK version
langsmith>=0.3.1
.The Vitest/Jest integrations are in beta and are subject to change in upcoming releases.
Setup
Set up the integrations as follows. Note that while you can add LangSmith evals alongside your other unit tests (as standard*.test.ts
files) using your existing test config files, the below examples will also set up a separate test config file and command to run your evals. It will assume you end your test files with .eval.ts
.
This ensures that the custom test reporter and other LangSmith touchpoints do not modify your existing test outputs.
Vitest
Install the required development dependencies if you have not already:openai
(and of course langsmith
!) as a dependency:
ls.vitest.config.ts
file with the following base config:
include
ensures that only files ending with some variation ofeval.ts
in your project are runreporters
is responsible for nicely formatting your output as shown abovesetupFiles
runsdotenv
to load environment variables before running your evals
JSDom environments are not supported at this time. You should either omit the
"environment"
field from your config or set it to "node"
.scripts
field in your package.json
to run Vitest with the config you just created:
Jest
Install the required development dependencies if you have not already:openai
(and of course langsmith
!) as a dependency:
Then create a separate config file named
ls.jest.config.cjs
:
testMatch
ensures that only files ending with some variation ofeval.js
in your project are runreporters
is responsible for nicely formatting your output as shown abovesetupFiles
runsdotenv
to load environment variables before running your evals
JSDom environments are not supported at this time. You should either omit the
"testEnvironment"
field from your config or set it to "node"
.scripts
field in your package.json
to run Jest with the config you just created:
Define and run evals
You can now define evals as tests using familiar Vitest/Jest syntax, with a few caveats:- You should import
describe
andtest
from thelangsmith/jest
orlangsmith/vitest
entrypoint - You must wrap your test cases in a
describe
block - When declaring tests, the signature is slightly different - there is an extra argument containing example inputs and expected outputs
sql.eval.ts
(or sql.eval.js
if you are using Jest without TypeScript) and pasting the below contents into it:
ls.test()
case as corresponding to a dataset example, and ls.describe()
as defining a LangSmith dataset. If you have LangSmith tracing environment variables set when you run the test suite, the SDK does the following:
- creates a dataset with the same name as the name passed to
ls.describe()
in LangSmith if it does not exist - creates an example in the dataset for each input and expected output passed into a test case if a matching one does not already exist
- creates a new experiment with one result for each test case
- collects the pass/fail rate under the
pass
feedback key for each test case
pass
boolean feedback key based on the test case passing / failing. It will also track any outputs that you log with the ls.logOutputs()
or return from the test function as “actual” result values from your app for the experiment.
Create a .env
file with your OPENAI_API_KEY
and LangSmith credentials if you don’t already have one:
eval
script we set up in the previous step to run the test:
Trace feedback
By default LangSmith collects the pass/fail rate under thepass
feedback key for each test case. You can add additional feedback with either ls.logFeedback()
or wrapEvaluator()
. To do so, try the following as your sql.eval.ts
file (or sql.eval.js
if you are using Jest without TypeScript):
ls.wrapEvaluator()
around the myEvaluator
function. This makes it so that the LLM-as-judge call is traced separately from the rest of the test case to avoid clutter, and conveniently creates feedback if the return value from the wrapped function matches { key: string; score: number | boolean }
. In this case, instead of showing up in the main test case run, the evaluator trace will instead show up in a trace associated with the correctness
feedback key.
You can see the evaluator runs in LangSmith by clicking their corresponding feedback chips in the UI.
Running multiple examples against a test case
You can run the same test case over multiple examples and parameterize your tests usingls.test.each()
. This is useful when you want to evaluate your app the same way against different inputs:
Log outputs
Every time we run a test we’re syncing it to a dataset example and tracing it as a run. To trace final outputs for the run, you can usels.logOutputs()
like this:
Trace intermediate calls
LangSmith will automatically trace any traceable intermediate calls that happen in the course of test case execution.Focusing or skipping tests
You can chain the Vitest/Jest.skip
and .only
methods on ls.test()
and ls.describe()
:
Configuring test suites
You can configure test suites with values like metadata or a custom client by passing an extra argument tols.describe()
for the full suite or by passing a config
field into ls.test()
for individual tests:
process.env.ENVIRONMENT
, process.env.NODE_ENV
and process.env.LANGSMITH_ENVIRONMENT
and set them as metadata on created experiments. You can then filter experiments by metadata in LangSmith’s UI.
See the API refs for a full list of configuration options.
Dry-run mode
If you want to run the tests without syncing the results to LangSmith, you can set omit your LangSmith tracing environment variables or setLANGSMITH_TEST_TRACKING=false
in your environment.
The tests will run as normal, but the experiment logs will not be sent to LangSmith.