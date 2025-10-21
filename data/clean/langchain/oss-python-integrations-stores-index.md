---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-integrations-stores-index",
  "h1": "oss-python-integrations-stores-index",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.490190",
  "sha256_raw": "6cd3332deac9ff47e2306f2cbbf91658ce9c88f7aa5d00e7ab1d8a5bef3f1fc5"
}
---

# oss-python-integrations-stores-index

> Source: https://docs.langchain.com/oss/python/integrations/stores/index

Overview
LangChain provides a key-value store interface for storing and retrieving data by key. The key-value store interface in LangChain is primarily used for caching embeddings.Interface
AllBaseStores
support the following interface:
mget(key: Sequence[str]) -> List[Optional[bytes]]
: get the contents of multiple keys, returningNone
if the key does not existmset(key_value_pairs: Sequence[Tuple[str, bytes]]) -> None
: set the contents of multiple keysmdelete(key: Sequence[str]) -> None
: delete multiple keysyield_keys(prefix: Optional[str] = None) -> Iterator[str]
: yield all keys in the store, optionally filtering by a prefix
Base stores are designed to work multiple key-value pairs at once for efficiency. This saves on network round-trips and may allow for more efficient batch operations in the underlying store.
Built-in stores for local development
Custom stores
You can also implement your own custom store by extending theBaseStore
class. See the store interface documentation for more details.