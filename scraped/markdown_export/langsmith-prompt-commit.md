# langsmith-prompt-commit

> Source: https://docs.langchain.com/langsmith/prompt-commit

- Version Control: Keep your prompts versioned alongside your application code in a familiar system.
- CI/CD Integration: Trigger automated staging or production deployments when critical prompts change.
Prerequisites
Before we begin, ensure you have the following set up:- GitHub Account: A standard GitHub account.
- GitHub Repository: Create a new (or choose an existing) repository where your LangSmith prompt manifests will be stored. This could be the same repository as your application code or a dedicated one for prompts.
-
GitHub Personal Access Token (PAT):
- LangSmith webhooks don’t directly interact with GitHub—they call an intermediary server that you create.
- This server requires a GitHub PAT to authenticate and make commits to your repository.
- Must include the
repo
scope (public_repo
is sufficient for public repositories). - Go to GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic).
- Click Generate new token (classic).
- Name it (e.g., “LangSmith Prompt Sync”), set an expiration, and select the required scopes.
- Click Generate token and copy it immediately — it won’t be shown again.
- Store the token securely and provide it as an environment variable to your server.
Understanding LangSmith “Prompt Commits” and Webhooks
In LangSmith, when you save changes to a prompt, you’re essentially creating a new version or a “Prompt Commit.” These commits are what can trigger webhooks. The webhook will send a JSON payload containing the new prompt manifest.Sample Webhook Payload
Sample Webhook Payload
It’s important to understand that LangSmith webhooks for prompt commits are generally triggered at the workspace level. This means if any prompt within your LangSmith workspace is modified and a “prompt commit” is saved, the webhook will fire and send the updated manifest of the prompt. The payloads are identifiable by prompt id. Your receiving server should be designed with this in mind.
Implementing a FastAPI Server for Webhook Reception
To effectively process webhook notifications from LangSmith when prompts are updated, an intermediary server application is necessary. This server will act as the receiver for HTTP POST requests sent by LangSmith. For demonstration purposes in this guide, we will outline the creation of a simple FastAPI application to fulfill this role. This publicly accessible server will be responsible for:- Receiving Webhook Requests: Listening for incoming HTTP POST requests.
- Parsing Payloads: Extracting and interpreting the JSON-formatted prompt manifest from the request body.
- Committing to GitHub: Programmatically creating a new commit in your specified GitHub repository, containing the updated prompt manifest. This ensures your prompts remain version-controlled and synchronized with changes made in LangSmith.
Minimal FastAPI Server Code ()
Minimal FastAPI Server Code ()
main.py
This server will listen for incoming webhooks from LangSmith and commit the received prompt manifest to your GitHub repository.- Configuration (
.env
): It expects a.env
file with yourGITHUB_TOKEN
,GITHUB_REPO_OWNER
, andGITHUB_REPO_NAME
. You can also customizeGITHUB_FILE_PATH
(default:LangSmith_prompt_manifest.json
) andGITHUB_BRANCH
(default:main
). - GitHub Interaction: The
commit_manifest_to_github
function handles the logic of fetching the current file’s SHA (to update it) and then committing the new manifest content. - Webhook Endpoint (
/webhook/commit
): This is the URL path your LangSmith webhook will target. - Error Handling: Basic error handling for GitHub API interactions is included.
https://prompt-commit-webhook.onrender.com
).Configuring the Webhook in LangSmith
Once your FastAPI server is deployed and you have its public URL, you can configure the webhook in LangSmith:- Navigate to your LangSmith workspace.
- Go to the Prompts section. Here you’ll see a list of your prompts.
- On the top right of the Prompts page, click the + Webhook button.
-
You’ll be presented with a form to configure your webhook:
- Webhook URL: Enter the full public URL of your deployed FastAPI server’s endpoint. For our example server, this would be
https://prompt-commit-webhook.onrender.com/webhook/commit
. - Headers (Optional):
- You can add custom headers that LangSmith will send with each webhook request.
- Webhook URL: Enter the full public URL of your deployed FastAPI server’s endpoint. For our example server, this would be
- Test the Webhook: LangSmith provides a “Send Test Notification” button. Use this to send a sample payload to your server. Check your server logs (e.g., on Render) to ensure it receives the request and processes it successfully (or to debug any issues).
- Save the webhook configuration.
The Workflow in Action
Now, with everything set up, here’s what happens:- Prompt Modification: A user (developer or non-technical team member) modifies a prompt in the LangSmith UI and saves it, creating a new “prompt commit.”
- Webhook Trigger: LangSmith detects this new prompt commit and triggers the configured webhook.
-
HTTP Request: LangSmith sends an HTTP POST request to the public URL of your FastAPI server (e.g.,
https://prompt-commit-webhook.onrender.com/webhook/commit
). The body of this request contains the JSON prompt manifest for the entire workspace. - Server Receives Payload: Your FastAPI server’s endpoint receives the request.
-
GitHub Commit: The server parses the JSON manifest from the request body. It then uses the configured GitHub Personal Access Token, repository owner, repository name, file path, and branch to:
- Check if the manifest file already exists in the repository on the specified branch to get its SHA (this is necessary for updating an existing file).
- Create a new commit with the latest prompt manifest, either creating the file or updating it if it already exists. The commit message will indicate that it’s an update from LangSmith.
- Confirmation: You should see the new commit appear in your GitHub repository.
Beyond a Simple Commit
Our example FastAPI server performs a direct commit of the entire prompt manifest. However, this is just the starting point. You can extend the server’s functionality to perform more sophisticated actions:- Granular Commits: Parse the manifest and commit changes to individual prompt files if you prefer a more granular structure in your repository.
- Trigger CI/CD: Instead of (or in addition to) committing, have the server trigger a CI/CD pipeline (e.g., Jenkins, GitHub Actions, GitLab CI) to deploy a staging environment, run tests, or build new application versions.
- Update Databases/Caches: If your application loads prompts from a database or cache, update these stores directly.
- Notifications: Send notifications to Slack, email, or other communication channels about prompt changes.
- Selective Processing: Based on metadata within the LangSmith payload (if available, e.g., which specific prompt changed or by whom), you could apply different logic.