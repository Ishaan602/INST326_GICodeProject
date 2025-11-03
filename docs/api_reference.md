Completed by Ishaan Patel
# API Reference

## Document Class

### Constructor

```python
Document(doc_id: str, title: str, content: str, metadata: Optional[dict] = None)
```

Creates a new Document instance.

**Parameters:**
- `doc_id` (str): Unique identifier for the document
- `title` (str): Document title  
- `content` (str): Full document content/text
- `metadata` (dict, optional): Additional document metadata

**Raises:**
- `ValueError`: If doc_id, title, or content are empty strings
- `TypeError`: If doc_id, title, or content are not strings

### Properties

#### `doc_id` (read-only)
```python
@property
def doc_id(self) -> str
```
Returns the document ID.

#### `title` (read/write)
```python
@property 
def title(self) -> str

@title.setter
def title(self, value: str) -> None
```
Gets or sets the document title with validation.

#### `content` (read/write)
```python
@property
def content(self) -> str

@content.setter  
def content(self, value: str) -> None
```
Gets or sets the document content with validation.

#### `metadata` (read-only)
```python
@property
def metadata(self) -> dict
```
Returns a copy of the document metadata dictionary.

### Methods

#### `clean_content()`
```python
def clean_content(self) -> str
```
Returns the document content in lowercase for standardized processing.

**Returns:** Lowercase version of the document content

#### `create_snippet()`
```python
def create_snippet(self, max_chars: int = 160) -> str
```
Creates a truncated snippet of the document content.

**Parameters:**
- `max_chars` (int): Maximum characters in snippet

**Returns:** Truncated content snippet with ellipsis if needed

#### `count_term_occurrences()`
```python
def count_term_occurrences(self, term: str) -> int
```
Counts occurrences of a specific term in the document content.

**Parameters:**
- `term` (str): The term to count occurrences of

**Returns:** Number of times the term appears as a complete word

#### `highlight_terms()`
```python
def highlight_terms(self, terms: List[str], pre: str = "<b>", post: str = "</b>") -> str
```
Highlights query terms in the document content.

**Parameters:**
- `terms` (List[str]): List of terms to highlight
- `pre` (str): Opening tag/text (default: "<b>")
- `post` (str): Closing tag/text (default: "</b>")

**Returns:** Content with matching terms highlighted

#### `get_word_count()`
```python
def get_word_count(self) -> int
```
Returns the total word count of the document content.

#### `add_metadata()`
```python
def add_metadata(self, key: str, value) -> None
```
Adds or updates metadata for the document.

**Parameters:**
- `key` (str): Metadata key
- `value`: Metadata value

---

## SearchQuery Class

### Constructor

```python
SearchQuery(query: str)
```

Creates a new SearchQuery instance with automatic normalization.

**Parameters:**
- `query` (str): The search query string to process

**Raises:**
- `TypeError`: If query is not a string
- `ValueError`: If query is empty after normalization

### Properties

#### `original_query` (read-only)
```python
@property
def original_query(self) -> str
```
Returns the original, unprocessed query string.

#### `normalized_query` (read-only)
```python
@property
def normalized_query(self) -> str
```
Returns the normalized query string in lowercase with standardized spacing.

#### `query_terms` (read-only)
```python
@property
def query_terms(self) -> List[str]
```
Returns a copy of the individual query terms list.

#### `search_history` (read-only)
```python
@property
def search_history(self) -> List[str]
```
Returns a copy of the search history list.

### Methods

#### `update_query()`
```python
def update_query(self, new_query: str) -> None
```
Updates the search query with a new query string.

**Parameters:**
- `new_query` (str): New query string to process

**Raises:**
- `TypeError`: If new_query is not a string
- `ValueError`: If new_query is empty after normalization

#### `build_inverted_index()`
```python
def build_inverted_index(self, documents: List[str]) -> Dict[str, Set[int]]
```
Builds an inverted index mapping terms to document IDs.

**Parameters:**
- `documents` (List[str]): List of documents to index

**Returns:** Dictionary mapping each term to set of document IDs

#### `boolean_search()`
```python
def boolean_search(self, documents: List[str]) -> Set[int]
```
Performs boolean AND retrieval on a list of documents.

**Parameters:**
- `documents` (List[str]): List of documents to search through

**Returns:** Set of document IDs that contain ALL query terms

#### `rank_documents()`
```python
def rank_documents(self, documents: List[str], top_k: int = 5) -> List[Tuple[int, float]]
```
Ranks documents based on term frequency similarity to query.

**Parameters:**
- `documents` (List[str]): List of documents to rank
- `top_k` (int): Number of top results to return (default: 5)

**Returns:** List of (doc_index, score) tuples sorted by relevance

#### `semantic_search()`
```python
def semantic_search(self, documents: List[str], model=None, top_k: int = 5) -> List[Tuple[int, float]]
```
Performs semantic search on documents (falls back to term frequency if no model).

**Parameters:**
- `documents` (List[str]): List of documents to search
- `model`: Optional semantic model (not implemented)
- `top_k` (int): Number of top results to return (default: 5)

**Returns:** List of (doc_index, score) tuples sorted by relevance

#### `get_query_statistics()`
```python
def get_query_statistics(self) -> Dict[str, int]
```
Returns statistics about the current query.

**Returns:** Dictionary containing query statistics:
- `term_count`: Number of terms in query
- `character_count`: Length of normalized query
- `original_length`: Length of original query
- `search_history_count`: Number of queries in history

#### `contains_term()`
```python
def contains_term(self, term: str) -> bool
```
Checks if the query contains a specific term.

**Parameters:**
- `term` (str): Term to search for in the query

**Returns:** True if the term is found in the query

#### `get_similar_queries()`
```python
def get_similar_queries(self, other_queries: List[str], threshold: float = 0.3) -> List[str]
```
Finds similar queries based on term overlap using Jaccard similarity.

**Parameters:**
- `other_queries` (List[str]): List of other queries to compare against
- `threshold` (float): Minimum similarity threshold (default: 0.3)

**Returns:** List of similar queries above the threshold

---

## Usage Examples

### Basic Document Operations

```python
from src.document import Document

# Create document
doc = Document("1", "AI Research", "Machine learning and neural networks")

# Text processing
cleaned = doc.clean_content()  # "machine learning and neural networks"
snippet = doc.create_snippet(20)  # "Machine learning and…"
count = doc.count_term_occurrences("learning")  # 1

# Highlighting
highlighted = doc.highlight_terms(["machine", "learning"])
# "**Machine** **learning** and neural networks"

# Metadata
doc.add_metadata("author", "Dr. Smith")
print(doc.metadata)  # {"author": "Dr. Smith"}
```

### Basic Search Operations

```python
from src.search_query import SearchQuery

# Create query
query = SearchQuery("  Machine   LEARNING  ")
print(query.normalized_query)  # "machine learning"
print(query.query_terms)  # ["machine", "learning"]

# Search documents
documents = [
    "Machine learning algorithms",
    "Deep learning neural networks", 
    "Database management systems"
]

# Boolean search (AND)
boolean_results = query.boolean_search(documents)
print(boolean_results)  # {0, 1} - docs containing both terms

# Ranked search
ranked_results = query.rank_documents(documents, top_k=2)
print(ranked_results)  # [(0, 1.0), (1, 0.5)] - (doc_id, score)
```

### Integration Example

```python
from src.document import Document
from src.search_query import SearchQuery

# Create document collection
docs = [
    Document("1", "AI Guide", "Machine learning fundamentals"),
    Document("2", "Data Science", "Statistical analysis methods"),
    Document("3", "ML Advanced", "Deep learning and neural networks")
]

# Create search query
query = SearchQuery("machine learning")

# Search and display results
doc_contents = [doc.content for doc in docs]
results = query.rank_documents(doc_contents, top_k=2)

for doc_id, score in results:
    doc = docs[doc_id]
    highlighted = doc.highlight_terms(query.query_terms)
    print(f"{doc.title} (score: {score:.2f})")
    print(f"Content: {highlighted}")
    print()
```
