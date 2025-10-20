# Clockify RAG - Documentation Index

**Start here!** Choose a guide based on your goal.

---

## 🚀 Getting Started (Pick One)

### ⏱️ I have 5 minutes - **[QUICKSTART.md](QUICKSTART.md)**
Copy-paste Docker commands, get running immediately with web UI.

### 📖 I have 30 minutes - **[STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md)**
Comprehensive terminal walkthrough covering:
- Prerequisites installation
- Local LLM setup (Ollama/vLLM/LM Studio)
- Full pipeline (crawl → preprocess → chunk → embed → hybrid)
- API testing
- Docker deployment
- Performance tuning

### 📚 I want to understand the system - **[README.md](README.md)**
Architecture overview, features, file structure, and technical concepts.

---

## 🔍 API Reference

### **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** (500+ lines)
- Complete endpoint reference
- Query parameters and response formats
- Error handling
- Performance benchmarks
- Code examples (Python, JavaScript, cURL)

---

## 🏭 Operations & Deployment

### **[PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)**
- Production setup and configuration
- Docker/Docker Compose deployment
- Kubernetes manifests
- Performance tuning (FAISS optimization, caching, scaling)
- Backup & recovery strategies
- Security best practices
- Systemd service configuration
- Monitoring and logging

### **[OPERATOR_GUIDE.md](OPERATOR_GUIDE.md)**
- System tuning and optimization
- Troubleshooting procedures
- Performance monitoring
- Maintenance tasks
- Incremental updates

### **[DEPLOY_TO_GITHUB.md](DEPLOY_TO_GITHUB.md)**
- GitHub repository setup
- Branch protection and CI/CD
- GitHub Actions workflow
- Release management
- Deployment options (Releases, Container Registry, Pages)

---

## 🛠️ Development & Technical

### **[ARCHITECTURE_MAPPING.md](ARCHITECTURE_MAPPING.md)**
System components, data flow, and integration points.

### **[SEARCH_ARCHITECTURE_DIAGRAM.md](SEARCH_ARCHITECTURE_DIAGRAM.md)**
Visual diagrams of search pipeline and retrieval process.

### **[BFS_SITEMAP_SCRAPER_RESULTS.md](BFS_SITEMAP_SCRAPER_RESULTS.md)**
Web scraper results, article counts, and coverage statistics.

---

## 📋 Feature Documentation

### **[SEARCH_QUICK_REFERENCE.md](SEARCH_QUICK_REFERENCE.md)**
Quick reference for search features and query optimization.

### **[SEARCH_IMPROVEMENTS_IMPLEMENTED.md](SEARCH_IMPROVEMENTS_IMPLEMENTED.md)**
List of implemented search enhancements.

---

## 🔧 Setup Variations

### **[FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md)**
Detailed first-time setup from scratch.

### **[COMPANY_OLLAMA_SETUP.md](COMPANY_OLLAMA_SETUP.md)**
Company/enterprise-specific Ollama setup.

---

## 📊 Status & Progress

### **[COMPLETION_STATUS.md](COMPLETION_STATUS.md)**
Project completion status and checklist.

### **[CHANGELOG.md](CHANGELOG.md)**
Version history and release notes.

### **[SESSION_SUMMARY.md](SESSION_SUMMARY.md)**
Summary of work completed in this session.

---

## 🚨 Troubleshooting

### **[DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md)**
Docker-specific issues and solutions.

### **[CRITICAL_FIXES.md](CRITICAL_FIXES.md)**
Known issues and their fixes.

### **[DOCKER_BUILD_FIX.md](DOCKER_BUILD_FIX.md)**
Docker build troubleshooting.

---

## 📈 Quick Command Reference

### Docker
```bash
# Quick start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

### Python
```bash
# Setup
python3.9 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Run full pipeline
make crawl preprocess chunk embed hybrid

# Start API
make serve
```

### API Testing
```bash
# Health check
curl http://localhost:7000/health

# Search
curl 'http://localhost:7000/search?q=timesheet&namespace=clockify&k=5'

# Chat with citations
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"How do I create a project?","namespace":"clockify","k":5}'
```

---

## 🎯 Common Workflows

### "I want to run this locally"
1. Read: [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md)
2. Follow each step sequentially

### "I want to deploy to production"
1. Read: [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)
2. Choose deployment option (Docker Compose, Kubernetes, or manual)

### "I want to understand how search works"
1. Read: [README.md](README.md) - Overview
2. Read: [SEARCH_ARCHITECTURE_DIAGRAM.md](SEARCH_ARCHITECTURE_DIAGRAM.md) - Diagrams
3. Read: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Endpoints

### "I want to optimize performance"
1. Read: [OPERATOR_GUIDE.md](OPERATOR_GUIDE.md) - Tuning section
2. Read: [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) - Performance tuning

### "I need to troubleshoot an issue"
1. Check: [CRITICAL_FIXES.md](CRITICAL_FIXES.md)
2. Check: [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md) (if Docker)
3. Read: [OPERATOR_GUIDE.md](OPERATOR_GUIDE.md) - Troubleshooting section

### "I want to contribute or modify"
1. Read: [DEPLOY_TO_GITHUB.md](DEPLOY_TO_GITHUB.md) - Git workflow
2. Read: [ARCHITECTURE_MAPPING.md](ARCHITECTURE_MAPPING.md) - System design

---

## 🗂️ File Organization

```
├── INDEX.md (THIS FILE)
├── README.md (System overview)
├── QUICKSTART.md (5-min Docker setup)
├── STEP_BY_STEP_GUIDE.md (Comprehensive guide)
├── API_DOCUMENTATION.md (API reference)
├── PRODUCTION_DEPLOYMENT.md (Deployment guide)
├── OPERATOR_GUIDE.md (Operations guide)
├── DEPLOY_TO_GITHUB.md (GitHub guide)
│
├── ARCHITECTURE_MAPPING.md (System architecture)
├── SEARCH_ARCHITECTURE_DIAGRAM.md (Diagrams)
├── BFS_SITEMAP_SCRAPER_RESULTS.md (Scraper stats)
├── SEARCH_QUICK_REFERENCE.md (Quick ref)
├── SEARCH_IMPROVEMENTS_IMPLEMENTED.md (Improvements)
│
├── FIRST_TIME_SETUP.md (First-time setup)
├── COMPANY_OLLAMA_SETUP.md (Enterprise setup)
├── DOCKER.md (Docker reference)
├── DOCKER_TROUBLESHOOTING.md (Docker issues)
├── DOCKER_BUILD_FIX.md (Build issues)
│
├── COMPLETION_STATUS.md (Project status)
├── CHANGELOG.md (Version history)
├── SESSION_SUMMARY.md (Work summary)
├── CRITICAL_FIXES.md (Known issues)
│
├── Makefile (Automation targets)
├── requirements.txt (Python dependencies)
├── .env.sample (Configuration template)
├── docker-compose.yml (Docker setup)
│
├── src/ (Python source code)
│   ├── server.py (FastAPI server)
│   ├── scrape.py (Web scraper)
│   ├── preprocess.py (HTML to Markdown)
│   ├── chunk.py (Parent-child chunking)
│   ├── embed.py (FAISS indexing)
│   ├── hybrid.py (BM25 indexing)
│   ├── rewrites.py (Query rewriting)
│   ├── rerank.py (Cross-encoder reranking)
│   └── prompt.py (RAG templates)
│
├── data/ (Pipeline data)
│   ├── raw/{clockify,langchain}/ (Scraped HTML)
│   ├── clean/{clockify,langchain}/ (Markdown)
│   └── chunks/ (*.jsonl chunks)
│
├── index/ (Vector/BM25 indexes)
│   ├── faiss/{clockify,langchain}/ (FAISS indexes)
│   └── hybrid/{clockify,langchain}/ (BM25 indexes)
│
└── tests/ (Test suite)
    └── test_pipeline.py (E2E tests)
```

---

## 📞 Support

- **Issues**: https://github.com/apet97/clrag/issues
- **Discussions**: https://github.com/apet97/clrag/discussions
- **Email**: Check repository README

---

## ✅ Status

- **Version**: Advanced Multi-Corpus RAG Stack 2.0
- **Status**: Production Ready
- **Last Updated**: October 20, 2025
- **Tested On**: macOS 12+, Ubuntu 20.04+, Docker, Kubernetes

---

**Ready to start?** → [QUICKSTART.md](QUICKSTART.md) (5 min) or [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md) (30 min)
