# langsmith-semantic-search

> Source: https://docs.langchain.com/langsmith/semantic-search

How to add semantic search to your agent deployment
This guide explains how to add semantic search to your deployment’s cross-thread store, so that your agent can search for memories and other documents by semantic similarity.
Once configured, you can use semantic search in your nodes. The store requires a namespace tuple to organize memories:
Copy
def search_memory(state: State, *, store: BaseStore): # Search the store using semantic similarity # The namespace tuple helps organize different types of memories # e.g., ("user_facts", "preferences") or ("conversation", "summaries") results = store.search( namespace=("memory", "facts"), # Organize memories by type query="your search query", limit=3 # number of results to return ) return results
The deployment will look for the function in the specified path. The function must be async and accept a list of strings:
Copy
# path/to/embedding_function.pyfrom openai import AsyncOpenAIclient = AsyncOpenAI()async def aembed_texts(texts: list[str]) -> list[list[float]]: """Custom embedding function that must: 1. Be async 2. Accept a list of strings 3. Return a list of float arrays (embeddings) """ response = await client.embeddings.create( model="text-embedding-3-small", input=texts ) return [e.embedding for e in response.data]