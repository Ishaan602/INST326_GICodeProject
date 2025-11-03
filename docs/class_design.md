# Class Design Documentation

## Architecture Overview

This project transforms the Project 1 function library into an object-oriented system with two core classes that encapsulate related data and behavior for information retrieval operations.

## Class Design

### 1. Document Class (`src/document.py`)

**Purpose**: Represents a single document in an information retrieval system.

**Core Responsibilities**:
- Store and manage document metadata (ID, title, content)
- Provide text processing capabilities
- Enable content analysis and manipulation

**Integrated Functions**:
- `clean_text()` → `clean_content()` method
- `truncate_snippet()` → `create_snippet()` method  
- `count_term_frequency()` → `count_term_occurrences()` method
- `highlight_query_terms()` → `highlight_terms()` method

**Key Features**:
- **Encapsulation**: Private attributes (`_doc_id`, `_title`, `_content`, `_metadata`) with property accessors
- **Validation**: Parameter validation in constructor and setters
- **Immutable ID**: Document ID cannot be changed after creation
- **Metadata Support**: Flexible metadata storage and retrieval
- **String Representations**: Both `__str__()` and `__repr__()` methods

### 2. SearchQuery Class (`src/search_query.py`)

**Purpose**: Represents and processes search queries for information retrieval.

**Core Responsibilities**:
- Normalize and process query strings
- Maintain search history
- Execute different types of searches (boolean, ranked, semantic)

**Integrated Functions**:
- `normalize_query()` → `_normalize_query_string()` method
- `boolean_retrieval()` → `boolean_search()` method
- `semantic_search()` → `semantic_search()` method

**Key Features**:
- **Query Processing**: Automatic normalization upon creation/update
- **Search History**: Tracks previous queries
- **Multiple Search Types**: Boolean AND, term frequency ranking, semantic search
- **Query Analysis**: Statistics and similarity comparison methods
- **Inverted Index**: Efficient document indexing for boolean operations

## Object-Oriented Design Principles

### Encapsulation
- Both classes use private attributes with controlled access through properties
- Internal methods (e.g., `_normalize_query_string()`) are marked as private
- Copies of mutable data are returned to prevent external modification

### Single Responsibility Principle
- **Document**: Manages individual document data and text operations
- **SearchQuery**: Handles query processing and search execution

### Data Validation
- Constructor validation ensures objects are created in valid states
- Property setters validate new values before assignment
- Meaningful error messages for invalid inputs

### Documentation
- Comprehensive docstrings for classes and methods
- Usage examples in docstrings
- Type hints for better code clarity

## Integration Benefits

### Cohesive Design
- Related functions are grouped together in logical classes
- Each class has a clear, focused purpose
- Methods work together to provide complete functionality

### Reusability
- Classes can be instantiated multiple times with different data
- Methods can be called repeatedly with different parameters
- Object state is maintained between method calls

### Extensibility
- New methods can be easily added to existing classes
- Additional document types or search algorithms can be implemented
- Metadata system allows for flexible document properties

### State Management
- Document objects maintain their data consistently
- SearchQuery objects track history and statistics
- Object state enables more sophisticated operations

## Usage Patterns

### Document Workflow
```python
# Create document
doc = Document("1", "Title", "Content")

# Process content
cleaned = doc.clean_content()
snippet = doc.create_snippet(100)
count = doc.count_term_occurrences("term")
highlighted = doc.highlight_terms(["term1", "term2"])

# Manage metadata
doc.add_metadata("author", "John Doe")
```

### SearchQuery Workflow  
```python
# Create and process query
query = SearchQuery("search terms")

# Execute searches
documents = ["doc1 content", "doc2 content"]
boolean_results = query.boolean_search(documents)
ranked_results = query.rank_documents(documents)

# Analyze query
stats = query.get_query_statistics()
similar = query.get_similar_queries(other_queries)
```

### Integration Pattern
```python
# Create document collection
docs = [Document(id, title, content) for ...]

# Create search query
query = SearchQuery("search terms")

# Extract content for search
contents = [doc.content for doc in docs]

# Search and highlight results
results = query.rank_documents(contents)
for doc_id, score in results:
    highlighted = docs[doc_id].highlight_terms(query.query_terms)
```

This object-oriented design provides a clean, maintainable, and extensible foundation for information retrieval operations while preserving all the functionality of the original Project 1 functions.
