# oss-python-integrations-splitters-index

> Source: https://docs.langchain.com/oss/python/integrations/splitters/index

For most use cases, start with the RecursiveCharacterTextSplitter. It provides a solid balance between keeping context intact and managing chunk size. This default strategy works well out of the box, and you should only consider adjusting it if you need to fine-tune performance for your specific application.
Text structure-based
Text is naturally organized into hierarchical units such as paragraphs, sentences, and words. We can leverage this inherent structure to inform our splitting strategy, creating split that maintain natural language flow, maintain semantic coherence within split, and adapts to varying levels of text granularity. LangChain’sRecursiveCharacterTextSplitter
implements this concept:
- The RecursiveCharacterTextSplitter attempts to keep larger units (e.g., paragraphs) intact.
- If a unit exceeds the chunk size, it moves to the next level (e.g., sentences).
- This process continues down to the word level if necessary.
Length-based
An intuitive strategy is to split documents based on their length. This simple yet effective approach ensures that each chunk doesn’t exceed a specified size limit. Key benefits of length-based splitting:- Straightforward implementation
- Consistent chunk sizes
- Easily adaptable to different model requirements
- Token-based: Splits text based on the number of tokens, which is useful when working with language models.
- Character-based: Splits text based on the number of characters, which can be more consistent across different types of text.
Document structure-based
Some documents have an inherent structure, such as HTML, Markdown, or JSON files. In these cases, it’s beneficial to split the document based on its structure, as it often naturally groups semantically related text. Key benefits of structure-based splitting:- Preserves the logical organization of the document
- Maintains context within each chunk
- Can be more effective for downstream tasks like retrieval or summarization
- Markdown: Split based on headers (e.g., #, ##, ###)
- HTML: Split using tags
- JSON: Split by object or array elements
- Code: Split by functions, classes, or logical blocks