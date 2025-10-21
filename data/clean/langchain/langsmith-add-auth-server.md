---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-add-auth-server",
  "h1": "langsmith-add-auth-server",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.436432",
  "sha256_raw": "c39e896b11f2dfddee192c8f7d6e62b48248a89d8c6fe1aaf73bea1d825e2b27"
}
---

# langsmith-add-auth-server

> Source: https://docs.langchain.com/langsmith/add-auth-server

Auth
object and resource-level access control, but upgrade authentication to use Supabase as your identity provider. While Supabase is used in this tutorial, the concepts apply to any OAuth2 provider. You’ll learn how to:
- Replace test tokens with real JWT tokens
- Integrate with OAuth2 providers for secure user authentication
- Handle user sessions and metadata while maintaining our existing authorization logic
Background
OAuth2 involves three main roles:- Authorization server: The identity provider (e.g., Supabase, Auth0, Google) that handles user authentication and issues tokens
- Application backend: Your LangGraph application. This validates tokens and serves protected resources (conversation data)
- Client application: The web or mobile app where users interact with your service
Prerequisites
Before you start this tutorial, ensure you have:- The bot from the second tutorial running without errors.
- A Supabase project to use its authentication server.
1. Install dependencies
Install the required dependencies. Start in yourcustom-auth
directory and ensure you have the langgraph-cli
installed:
2. Set up the authentication provider
Next, fetch the URL of your auth server and the private key for authentication. Since you’re using Supabase for this, you can do this in the Supabase dashboard:- In the left sidebar, click on t️⚙ Project Settings” and then click “API”
- Copy your project URL and add it to your
.env
file
- Copy your service role secret key and add it to your
.env
file:
- Copy your “anon public” key and note it down. This will be used later when you set up our client code.
3. Implement token validation
In the previous tutorials, you used theAuth
object to validate hard-coded tokens and add resource ownership.
Now you’ll upgrade your authentication to validate real JWT tokens from Supabase. The main changes will all be in the @auth.authenticate
decorated function:
- Instead of checking against a hard-coded list of tokens, you’ll make an HTTP request to Supabase to validate the token.
- You’ll extract real user information (ID, email) from the validated token.
- The existing resource authorization logic remains unchanged.
src/security/auth.py
to implement this:
src/security/auth.py
4. Test authentication flow
Let’s test out the new authentication flow. You can run the following code in a file or notebook. You will need to provide:- A valid email address
- A Supabase project URL (from above)
- A Supabase anon public key (also from above)
/login
requests until after you have confirmed your users’ email.
Now test that users can only see their own data. Make sure the server is running (run langgraph dev
) before proceeding. The following snippet requires the “anon public” key that you copied from the Supabase dashboard while setting up the auth provider previously.
- Users must log in to access the bot
- Each user can only see their own threads
Next steps
You’ve successfully built a production-ready authentication system for your LangGraph application! Let’s review what you’ve accomplished:- Set up an authentication provider (Supabase in this case)
- Added real user accounts with email/password authentication
- Integrated JWT token validation into your LangGraph server
- Implemented proper authorization to ensure users can only access their own data
- Created a foundation that’s ready to handle your next authentication challenge 🚀
- Building a web UI with your preferred framework (see the Custom Auth template for an example)
- Learn more about the other aspects of authentication and authorization in the conceptual guide on authentication.
- Customize your handlers and setup further after reading the reference docs.