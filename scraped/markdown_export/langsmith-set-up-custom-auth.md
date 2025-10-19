# langsmith-set-up-custom-auth

> Source: https://docs.langchain.com/langsmith/set-up-custom-auth

- Set up custom authentication (you are here) - Control who can access your bot
- Make conversations private - Let users have private conversations
- Connect an authentication provider - Add real user accounts and validate using OAuth2 for production
Custom auth is only available for LangSmith SaaS deployments or Enterprise Self-Hosted deployments.
1. Create your app
Create a new chatbot using the LangGraph starter template:2. Add authentication
Now that you have a base LangGraph app, add authentication to it.In this tutorial, you will start with a hard-coded token for example purposes. You will get to a “production-ready” authentication scheme in the third tutorial.
Auth
object lets you register an authentication function that the LangGraph platform will run on every request. This function receives each request and decides whether to accept or reject.
Create a new file src/security/auth.py
. This is where your code will live to check if users are allowed to access your bot:
src/security/auth.py
- Checks if a valid token is provided in the request’s Authorization header
- Returns the user’s identity
langgraph.json
configuration:
langgraph.json
3. Test your bot
Start the server again to test everything out:--no-browser
, the Studio UI will open in the browser. By default, we also permit access from Studio, even when using custom auth. This makes it easier to develop and test your bot in Studio. You can remove this alternative authentication option by setting disable_studio_auth: "true"
in your auth configuration:
4. Chat with your bot
You should now only be able to access the bot if you provide a valid token in the request header. Users will still, however, be able to access each other’s resources until you add resource authorization handlers in the next section of the tutorial. Run the following code in a file or notebook:- Without a valid token, we can’t access the bot
- With a valid token, we can create threads and chat
Next steps
Now that you can control who accesses your bot, you might want to:- Continue the tutorial by going to Make conversations private to learn about resource authorization.
- Read more about authentication concepts.
- Check out the API reference for more authentication details.