# oss-python-integrations-providers-huggingface

> Source: https://docs.langchain.com/oss/python/integrations/providers/huggingface

Skip to main content
All LangChain integrations with Hugging Face Hub and libraries like transformers , sentence transformers , and datasets .
Chat models
ChatHuggingFace
We can use the Hugging Face
LLM classes or directly use the ChatHuggingFace
class.
See a usage example .
LLMs
HuggingFaceEndpoint
We can use the HuggingFaceEndpoint
class to run open source models via serverless Inference Providers or via dedicated Inference Endpoints .
See a usage example .
HuggingFacePipeline
We can use the HuggingFacePipeline
class to run open source models locally.
See a usage example .
Embedding Models
HuggingFaceEmbeddings
We can use the HuggingFaceEmbeddings
class to run open source embedding models locally.
See a usage example .
HuggingFaceEndpointEmbeddings
We can use the HuggingFaceEndpointEmbeddings
class to run open source embedding models via a dedicated Inference Endpoint .
See a usage example .
HuggingFaceInferenceAPIEmbeddings
We can use the HuggingFaceInferenceAPIEmbeddings
class to run open source embedding models via Inference Providers .
See a usage example .
HuggingFaceInstructEmbeddings
We can use the HuggingFaceInstructEmbeddings
class to run open source embedding models locally.
See a usage example .
HuggingFaceBgeEmbeddings
BGE models on the HuggingFace are one of the best open-source embedding models .
BGE model is created by the Beijing Academy of Artificial Intelligence (BAAI) . BAAI
is a private non-profit organization engaged in AI research and development.
See a usage example .
Document loaders
Hugging Face dataset
Hugging Face Hub is home to over 75,000
datasets in more than 100 languages
that can be used for a broad range of tasks across NLP, Computer Vision, and Audio.
They used for a diverse range of tasks such as translation, automatic speech
recognition, and image classification.
We need to install datasets
python package.
See a usage example .
Hugging Face model loader
Load model information from Hugging Face Hub
, including README content.
This loader interfaces with the Hugging Face Models API
to fetch
and load model metadata and README files.
The API allows you to search and filter models based on
specific criteria such as model tags, authors, and more.
Image captions
It uses the Hugging Face models to generate image captions.
We need to install several python packages.
See a usage example .
Hugging Face Tools
support text I/O and are loaded using the load_huggingface_tool
function.
We need to install several python packages.
See a usage example .
Hugging Face Text-to-Speech Model Inference.
It is a wrapper around OpenAI Text-to-Speech API
.