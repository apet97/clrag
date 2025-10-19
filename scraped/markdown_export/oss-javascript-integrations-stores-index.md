# oss-javascript-integrations-stores-index

> Source: https://docs.langchain.com/oss/javascript/integrations/stores/index

Overview
LangChain provides a key-value store interface for storing and retrieving data by key. The key-value store interface in LangChain is primarily used for caching embeddings.Interface
AllBaseStores
are generic and support the following interface, where K
represents the key type and V
represents the value type:
mget(keys: K[]): Promise<(V | undefined)[]>
: get the values for multiple keys, returningundefined
if a key does not existmset(keyValuePairs: [K, V][]): Promise<void>
: set the values for multiple keysmdelete(keys: K[]): Promise<void>
: delete multiple keysyieldKeys(prefix?: string): AsyncGenerator<K | string>
: asynchronously yield all keys in the store, optionally filtering by a prefix
BaseStore<string, BaseMessage>
would store messages with string keys, while BaseStore<string, number[]>
would store arrays of numbers.
Base stores are designed to work with multiple key-value pairs at once for efficiency. This saves on network round-trips and may allow for more efficient batch operations in the underlying store.
Built-in stores for local development
Custom stores
You can also implement your own custom store by extending theBaseStore
class. See the store interface documentation for more details.