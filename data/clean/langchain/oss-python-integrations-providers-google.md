---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-integrations-providers-google",
  "h1": "oss-python-integrations-providers-google",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.446838",
  "sha256_raw": "5dd7e6b94df118224bb5020decef959c779e4d14709d4bb6eeb9f7fd0dcf2d86"
}
---

# oss-python-integrations-providers-google

> Source: https://docs.langchain.com/oss/python/integrations/providers/google

Google Generative AI (Gemini API & AI Studio): Access Google Gemini models directly via the Gemini API. Use Google AI Studio for rapid prototyping and get started quickly with the langchain-google-genai package. This is often the best starting point for individual developers.
Google Cloud (Vertex AI & other services): Access Gemini models, Vertex AI Model Garden and a wide range of cloud services (databases, storage, document AI, etc.) via the Google Cloud Platform. Use the langchain-google-vertexai package for Vertex AI models and specific packages (e.g., langchain-google-cloud-sql-pg, langchain-google-community) for other cloud services. This is ideal for developers already using Google Cloud or needing enterprise features like MLOps, specific model tuning or enterprise support.
See Google’s guide on migrating from the Gemini API to Vertex AI for more details on the differences.Integration packages for Gemini models and the Vertex AI platform are maintained in the langchain-google repository. You can find a host of LangChain integrations with other Google APIs and services in the googleapisGithub organization and the langchain-google-community package.
Access Google Gemini models directly using the Gemini API, best suited for rapid development and experimentation. Gemini models are available in Google AI Studio.
Use the ChatGoogleGenerativeAI class to interact with Gemini models. See
details in this guide.
Copy
from langchain_google_genai import ChatGoogleGenerativeAIfrom langchain.messages import HumanMessagellm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")# Simple text invocationresult = llm.invoke("Sing a ballad of LangChain.")print(result.content)# Multimodal invocation with gemini-pro-visionmessage = HumanMessage( content=[ { "type": "text", "text": "What's in this image?", }, {"type": "image_url", "image_url": "https://picsum.photos/seed/picsum/200/300"}, ])result = llm.invoke([message])print(result.content)
The image_url can be a public URL, a GCS URI (gs://...), a local file path, a base64 encoded image string (data:image/png;base64,...), or a PIL Image object.
Generate text embeddings using models like gemini-embedding-001 with the GoogleGenerativeAIEmbeddings class.See a usage example.
Copy
from langchain_google_genai import GoogleGenerativeAIEmbeddingsembeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")vector = embeddings.embed_query("What are embeddings?")print(vector[:5])
Access the same Gemini models using the (legacy) LLM
interface with the GoogleGenerativeAI class.See a usage example.
Copy
from langchain_google_genai import GoogleGenerativeAIllm = GoogleGenerativeAI(model="gemini-2.5-flash")result = llm.invoke("Sing a ballad of LangChain.")print(result)
Access Gemini models, Vertex AI Model Garden and other Google Cloud services via Vertex AI and specific cloud integrations.Vertex AI models require the langchain-google-vertexai package. Other services might require additional packages like langchain-google-community, langchain-google-cloud-sql-pg, etc.
Copy
pip install langchain-google-vertexai# pip install langchain-google-community[...] # For other services
Google Cloud integrations typically use Application Default Credentials (ADC). Refer to the Google Cloud authentication documentation for setup instructions (e.g., using gcloud auth application-default login).
Google Cloud Document AI is a Google Cloud
service that transforms unstructured data from documents into structured data, making it easier
to understand, analyze, and consume.
We need to set up a GCS bucket and create your own OCR processor
The GCS_OUTPUT_PATH should be a path to a folder on GCS (starting with gs://)
and a processor name should look like projects/PROJECT_NUMBER/locations/LOCATION/processors/PROCESSOR_ID.
We can get it either programmatically or copy from the Prediction endpoint section of the Processor details
tab in the Google Cloud Console.
Google Translate is a multilingual neural machine
translation service developed by Google to translate text, documents and websites
from one language into another.
The GoogleTranslateTransformer allows you to translate text and HTML with the Google Cloud Translation API.First, we need to install the langchain-google-community with translate dependencies.
Google Cloud AlloyDB is a fully managed relational database service that offers high performance, seamless integration, and impressive scalability on Google Cloud. AlloyDB is 100% compatible with PostgreSQL.
Google Cloud BigQuery,
BigQuery is a serverless and cost-effective enterprise data warehouse in Google Cloud.Google Cloud BigQuery Vector Search
BigQuery vector search lets you use GoogleSQL to do semantic search, using vector indexes for fast but approximate results, or using brute force for exact results.
It can calculate Euclidean or Cosine distance. With LangChain, we default to use Euclidean distance.
# Note: BigQueryVectorSearch might be in langchain or langchain_community depending on version# Check imports in the usage example.from langchain.vectorstores import BigQueryVectorSearch # Or langchain_community.vectorstores
Google Cloud Vertex AI Vector Search from Google Cloud,
formerly known as Vertex AI Matching Engine, provides the industry’s leading high-scale
low latency vector database. These vector databases are commonly
referred to as vector similarity-matching or an approximate nearest neighbor (ANN) service.
Build generative AI powered search engines using Vertex AI Search.
from Google Cloud allows developers to quickly build generative AI powered search engines for customers and employees.
See a usage example.Note: GoogleVertexAISearchRetriever is deprecated. Use the components below from langchain-google-community.Install the google-cloud-discoveryengine package for underlying access.
from langchain_google_community import VertexAIMultiTurnSearchRetriever
VertexAISearchRetriever
Copy
# Note: The example code shows VertexAIMultiTurnSearchRetriever, confirm if VertexAISearchRetriever is separate or related.# Assuming it might be related or a typo in the original doc:from langchain_google_community import VertexAISearchRetriever # Verify class name if needed
VertexAISearchSummaryTool
Copy
from langchain_google_community import VertexAISearchSummaryTool
Note: GoogleDocumentAIWarehouseRetriever (from langchain) is deprecated. Use DocumentAIWarehouseRetriever from langchain-google-community.Requires installation of relevant Document AI packages (check specific docs).
Copy
pip install langchain-google-community # Add specific docai dependencies if needed
Copy
from langchain_google_community.documentai_warehouse import DocumentAIWarehouseRetriever
Google Cloud Text-to-Speech is a Google Cloud service that enables developers to
synthesize natural-sounding speech with 100+ voices, available in multiple languages and variants.
It applies DeepMind’s groundbreaking research in WaveNet and Google’s powerful neural networks
to deliver the highest fidelity possible.
from langchain_community.tools.google_jobs import GoogleJobsQueryRun# Note: Utilities might be shared, e.g., GoogleFinanceAPIWrapper was listed, verify correct utility# from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper # If exists
# Note: GooglePlacesTool might be in langchain or langchain_community depending on versionfrom langchain.tools import GooglePlacesTool # Or langchain_community.tools
MCP Toolbox provides a simple and efficient way to connect to your databases, including those on Google Cloud like Cloud SQL and AlloyDB. With MCP Toolbox, you can seamlessly integrate your database with LangChain to build powerful, data-driven applications.
Evaluate a single prediction string using Vertex AI models.
Copy
# Note: Original doc listed VertexPairWiseStringEvaluator twice. Assuming this class exists.from langchain_google_vertexai.evaluators.evaluation import VertexStringEvaluator # Verify class name if needed
Google ScaNN
(Scalable Nearest Neighbors) is a python package.ScaNN is a method for efficient vector similarity search at scale.
ScaNN includes search space pruning and quantization for Maximum Inner
Product Search and also supports other distance functions such as
Euclidean distance. The implementation is optimized for x86 processors
with AVX2 support. See its Google Research github
for more details.
from langchain_community.tools.google_jobs import GoogleJobsQueryRun# Note: Utilities might be shared, e.g., GoogleFinanceAPIWrapper was listed, verify correct utility# from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper # If exists
# Note: GooglePlacesTool might be in langchain or langchain_community depending on versionfrom langchain.tools import GooglePlacesTool # Or langchain_community.tools
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader# Often used with whisper parsers:# from langchain_community.document_loaders.parsers import OpenAIWhisperParser, OpenAIWhisperParserLocal