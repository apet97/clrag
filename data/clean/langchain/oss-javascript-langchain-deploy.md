---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-deploy",
  "h1": "oss-javascript-langchain-deploy",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.457711",
  "sha256_raw": "c89ecc679394c0791c0f394f91b5d4314ff6f718eb9455a82677fe2c62be8d2c"
}
---

# oss-javascript-langchain-deploy

> Source: https://docs.langchain.com/oss/javascript/langchain/deploy

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