---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-deploy",
  "h1": "oss-python-langchain-deploy",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.456960",
  "sha256_raw": "b11dbd2965f28c68127beb3d78d932484d170c17790dee3d12b6e031a6a2969d"
}
---

# oss-python-langchain-deploy

> Source: https://docs.langchain.com/oss/python/langchain/deploy

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Prerequisites
Before you begin, ensure you have the following:- A GitHub account
- A LangSmith account (free to sign up)
Deploy your agent
1. Create a repository on GitHub
Your application’s code must reside in a GitHub repository to be deployed on LangSmith. Both public and private repositories are supported. For this quickstart, first make sure your app is LangGraph-compatible by following the local server setup guide. Then, push your code to the repository.2. Deploy to LangSmith
2
Create new deployment
Click the + New Deployment button. A pane will open where you can fill in the required fields.
3
Link repository
If you are a first time user or adding a private repository that has not been previously connected, click the Add new account button and follow the instructions to connect your GitHub account.
4
Deploy repository
Select your application’s repository. Click Submit to deploy. This may take about 15 minutes to complete. You can check the status in the Deployment details view.
3. Test your application in Studio
Once your application is deployed:- Select the deployment you just created to view more details.
- Click the Studio button in the top right corner. Studio will open to display your graph.
4. Get the API URL for your deployment
- In the Deployment details view in LangGraph, click the API URL to copy it to your clipboard.
- Click the
URL
to copy it to the clipboard.
5. Test the API
You can now test the API:- Python
- Rest API
- Install LangGraph Python:
- Send a message to the agent: