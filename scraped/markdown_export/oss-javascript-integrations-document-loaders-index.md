# oss-javascript-integrations-document-loaders-index

> Source: https://docs.langchain.com/oss/javascript/integrations/document_loaders/index

Interface
Each document loader may define its own parameters, but they share a common API:.load()
: Loads all documents at once..loadAndSplit()
: Loads all documents at once and splits them into smaller documents.
By category
LangChain.js categorizes document loaders in two different ways:- File loaders, which load data into LangChain formats from your local filesystem.
- Web loaders, which load data from remote sources.
File loaders
PDFs
| Document Loader | Description | Package/API |
|---|---|---|
| PDFLoader | Load and parse PDF files using pdf-parse | Package |
Common File Types
| Document Loader | Description | Package/API |
|---|---|---|
| CSV | Load data from CSV files with configurable column extraction | Package |
| JSON | Load JSON files using JSON pointer to target specific keys | Package |
| JSONLines | Load data from JSONLines/JSONL files | Package |
| Text | Load plain text files | Package |
| DOCX | Load Microsoft Word documents (.docx and .doc formats) | Package |
| EPUB | Load EPUB files with optional chapter splitting | Package |
| PPTX | Load PowerPoint presentations | Package |
| Subtitles | Load subtitle files (.srt format) | Package |
Specialized File Loaders
| Document Loader | Description | Package/API |
|---|---|---|
| DirectoryLoader | Load all files from a directory with custom loader mappings | Package |
| UnstructuredLoader | Load multiple file types using Unstructured API | API |
| MultiFileLoader | Load data from multiple individual file paths | Package |
| ChatGPT | Load ChatGPT conversation exports | Package |
| Notion Markdown | Load Notion pages exported as Markdown | Package |
| OpenAI Whisper Audio | Transcribe audio files using OpenAI Whisper API | API |
Web loaders
Webpages
| Document Loader | Description | Web Support | Package/API |
|---|---|---|---|
| Cheerio | Load webpages using Cheerio (lightweight, no JavaScript execution) | ✅ | Package |
| Playwright | Load dynamic webpages using Playwright (supports JavaScript rendering) | ❌ | Package |
| Puppeteer | Load dynamic webpages using Puppeteer (headless Chrome) | ❌ | Package |
| FireCrawl | Crawl and convert websites into LLM-ready markdown | ✅ | API |
| Spider | Fast crawler that converts websites into HTML, markdown, or text | ✅ | API |
| RecursiveUrlLoader | Recursively load webpages following links | ❌ | Package |
| Sitemap | Load all pages from a sitemap.xml | ✅ | Package |
| Browserbase | Load webpages using managed headless browsers with stealth mode | ✅ | API |
| WebPDFLoader | Load PDF files in web environments | ✅ | Package |
Cloud Providers
| Document Loader | Description | Web Support | Package/API |
|---|---|---|---|
| S3 | Load files from AWS S3 buckets | ❌ | Package |
| Azure Blob Storage Container | Load all files from Azure Blob Storage container | ❌ | Package |
| Azure Blob Storage File | Load individual files from Azure Blob Storage | ❌ | Package |
| Google Cloud Storage | Load files from Google Cloud Storage buckets | ❌ | Package |
| Google Cloud SQL for PostgreSQL | Load documents from Cloud SQL PostgreSQL databases | ✅ | Package |
Productivity Tools
| Document Loader | Description | Web Support | Package/API |
|---|---|---|---|
| Notion API | Load Notion pages and databases via API | ✅ | API |
| Figma | Load Figma file data | ✅ | API |
| Confluence | Load pages from Confluence spaces | ❌ | API |
| GitHub | Load files from GitHub repositories | ✅ | API |
| GitBook | Load GitBook documentation pages | ✅ | Package |
| Jira | Load issues from Jira projects | ❌ | API |
| Airtable | Load records from Airtable bases | ✅ | API |
| Taskade | Load Taskade project data | ✅ | API |
Search & Data APIs
| Document Loader | Description | Web Support | Package/API |
|---|---|---|---|
| SearchAPI | Load web search results from SearchAPI (Google, YouTube, etc.) | ✅ | API |
| SerpAPI | Load web search results from SerpAPI | ✅ | API |
| Apify Dataset | Load scraped data from Apify platform | ✅ | API |
Audio & Video
| Document Loader | Description | Web Support | Package/API |
|---|---|---|---|
| YouTube | Load YouTube video transcripts | ✅ | Package |
| AssemblyAI | Transcribe audio and video files using AssemblyAI API | ✅ | API |
| Sonix | Transcribe audio files using Sonix API | ❌ | API |
Other
| Document Loader | Description | Web Support | Package/API |
|---|---|---|---|
| Couchbase | Load documents from Couchbase database using SQL++ queries | ✅ | Package |
| LangSmith | Load datasets and traces from LangSmith | ✅ | API |
| Hacker News | Load Hacker News threads and comments | ✅ | Package |
| IMSDB | Load movie scripts from Internet Movie Script Database | ✅ | Package |
| College Confidential | Load college information from College Confidential | ✅ | Package |
| Blockchain Data | Load blockchain data (NFTs, transactions) via Sort.xyz API | ✅ | API |