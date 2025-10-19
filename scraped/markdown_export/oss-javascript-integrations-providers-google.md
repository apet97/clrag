# oss-javascript-integrations-providers-google

> Source: https://docs.langchain.com/oss/javascript/integrations/providers/google

Chat models
Gemini Models
Access Gemini models such asgemini-1.5-pro
and gemini-2.0-flex
through the ChatGoogleGenerativeAI
,
or if using VertexAI, via the ChatVertexAI
class.
- GenAI
- VertexAI
image_url
must be a base64 encoded image (e.g., data:image/png;base64,abcd124
).
Gemma
Access thegemma-3-27b-it
model through AI Studio using the ChatGoogle
class.
(This class is a superclass of the ChatVertexAI
class that works with both Vertex AI and the AI Studio APIs.)
npm
Third Party Models
See above for setting up authentication through Vertex AI to use these models. Anthropic Claude models are also available through the Vertex AI platform. See here for more information about enabling access to the models and the model names to use. PaLM models are no longer supported.Vector Store
Vertex AI Vector Search
Vertex AI Vector Search, formerly known as Vertex AI Matching Engine, provides the industry’s leading high-scale low latency vector database. These vector databases are commonly referred to as vector similarity-matching or an approximate nearest neighbor (ANN) service.
Postgres Vector Store
The PostgresVectorStore module from the@langchain/google-cloud-sql-pg
package provides a way to use the CloudSQL for PostgresSQL to store
vector embeddings using the class.
Tools
Google Search
- Set up a Custom Search Engine, following these instructions
- Get an API Key and Custom Search Engine ID from the previous step, and set them as environment variables
GOOGLE_API_KEY
andGOOGLE_CSE_ID
respectively
GoogleCustomSearch
utility which wraps this API. To import this utility: