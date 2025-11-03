# INST326 Information Retrieval System

A comprehensive Python library for information retrieval, text processing, and data validation operations. Now featuring object-oriented design with Document and SearchQuery classes that encapsulate related functionality for building sophisticated search systems.

## 🆕 Project 2 Update: Object-Oriented Design

This project has been transformed from a function-based library into an object-oriented system with two core classes:

- **Document Class**: Represents individual documents with integrated text processing capabilities
- **SearchQuery Class**: Handles query processing, normalization, and various search operations

The original Project 1 functions are now integrated into these classes while remaining available as standalone functions.

# Team Memebr Names
Ishaan Patel, Rushan Heaven, Zachary Tong
# Contribution
### Ishaan Patel
Functions: 
1. filter_sort_paginate_results
2. highlight_query_terms
3. normalize_query
4. truncate_snippet 
5. count_term_frequency
- Formated all files
- Created docs, demo_scripts, init, read me, and requirments

### Rushan Heaven
Funtions: 
1. clean_text
2. build_inverted_index 
3. boolean_retrieval
4. rank_documents
5. semantic_search

### Zachary Tong
Functions:
1) validate_information
2) format_query
3) calculate_user_distance
4) parse_user_order
5) process_order_data
##  Features

### Core Information Retrieval Functions
- **Search & Ranking**: Filter, score, and rank documents based on query terms
- **Text Processing**: Normalize queries, count term frequencies, and process text
- **Highlighting**: Highlight search terms in results with customizable tags
- **Pagination**: Handle large result sets with safe pagination
- **Text Truncation**: Intelligently truncate text at word boundaries

### Utility Functions  
- **Data Validation**: Validate and format user information
- **Distance Calculations**: Calculate distances between points
- **Order Processing**: Process and validate food orders
- **Query Formatting**: Format user data into structured queries

## Project Structure

```
INST326_GICodeProject/
├── README.md                    # Project overview and setup instructions
├── src/
│   ├── __init__.py             # Package initialization
│   ├── library_name.py         # Original Project 1 functions
│   ├── document.py             # Document class (NEW)
│   └── search_query.py         # SearchQuery class (NEW)
├── docs/                        # Documentation directory
│   ├── function_reference.md   # Detailed function documentation
│   ├── usage_examples.md       # Usage examples and tutorials
│   ├── class_design.md         # OOP architecture documentation (NEW)
│   └── api_reference.md        # Class API documentation (NEW)
├── examples/                    # Example usage scripts
│   ├── demo_script.py          # Function library demonstration
│   └── class_demo.py           # Class-based demonstration (NEW)
└── requirements.txt             # Python dependencies
```

##  Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ishaan602/INST326_GICodeProject.git
cd INST326_GICodeProject
```

2. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

### Basic Usage

#### Object-Oriented Approach (Recommended)

```python
from src.document import Document
from src.search_query import SearchQuery

# Create documents
doc1 = Document("1", "Python Programming", "Learn Python basics and advanced concepts")
doc2 = Document("2", "Data Science", "Python for data analysis and machine learning")

# Create search query
query = SearchQuery("Python programming")

# Perform searches
documents_content = [doc1.content, doc2.content] 
search_results = query.rank_documents(documents_content, top_k=2)

# Display results with highlighting
for doc_id, score in search_results:
    if doc_id == 0:
        highlighted = doc1.highlight_terms(query.query_terms)
        snippet = doc1.create_snippet(50)
        print(f"{doc1.title} (Score: {score:.2f})")
        print(f"Snippet: {snippet}")
        print(f"Highlighted: {highlighted}")
```

#### Function-Based Approach (Original)

```python
# Import the functions you need
from src.library_name import filter_sort_paginate_results, highlight_query_terms
from src.library_name import validate_information

# Example: Search documents
documents = [
    {"doc_id": "1", "title": "Python Programming", "text": "Learn Python basics"},
    {"doc_id": "2", "title": "Data Science", "text": "Python for data analysis"}
]

results = filter_sort_paginate_results(documents, ["python"], page=1, per_page=5)
print(f"Found {results['total_results']} results")

# Example: Highlight search terms
text = "Learn Python programming fundamentals"
highlighted = highlight_query_terms(text, ["python", "programming"])
print(highlighted)  # Output: Learn <b>Python</b> <b>programming</b> fundamentals
```

### Run the Demos

To see all features in action:

```bash
# Run the new object-oriented class demonstration
python examples/class_demo.py

# Run the original function library demonstration  
python examples/demo_script.py
```

##  Documentation

### Class Documentation (NEW)
- **[Class Design Architecture](docs/class_design.md)** - Object-oriented design principles and architecture
- **[API Reference](docs/api_reference.md)** - Complete class and method documentation

### Function Reference (Original)
- **[Complete Function Reference](docs/function_reference.md)** - Detailed documentation for all functions
- **[Usage Examples](docs/usage_examples.md)** - Practical examples and tutorials

### Core Classes Overview (NEW)

#### Document Class (`src/document.py`)

| Method | Description |
|--------|-------------|
| `__init__(doc_id, title, content, metadata)` | Initialize document with validation |
| `clean_content()` | Get normalized lowercase content |
| `create_snippet(max_chars)` | Create truncated text snippet |
| `count_term_occurrences(term)` | Count term frequency in document |
| `highlight_terms(terms, pre, post)` | Highlight search terms in content |
| `get_word_count()` | Get total word count |
| `add_metadata(key, value)` | Add document metadata |

#### SearchQuery Class (`src/search_query.py`)

| Method | Description |
|--------|-------------|
| `__init__(query)` | Initialize and normalize query |
| `update_query(new_query)` | Update query and add to history |
| `boolean_search(documents)` | Find documents containing ALL terms |
| `rank_documents(documents, top_k)` | Rank by term frequency similarity |
| `semantic_search(documents, model, top_k)` | Semantic search (fallback to TF) |
| `get_query_statistics()` | Get query analysis statistics |
| `contains_term(term)` | Check if query contains term |
| `get_similar_queries(queries, threshold)` | Find similar queries by overlap |

### Core Functions Overview (Original)

#### Information Retrieval (`src/library_name.py`)

| Function | Description |
|----------|-------------|
| `filter_sort_paginate_results()` | Search, score, and paginate document results |
| `highlight_query_terms()` | Highlight search terms in text |
| `normalize_query()` | Clean and standardize search queries |  
| `truncate_snippet()` | Truncate text at word boundaries |
| `count_term_frequency()` | Count term occurrences in text |
| `clean_text()` | Clean and normalize text by converting to lowercase |
| `build_inverted_index()` | Build inverted index mapping terms to document IDs |
| `boolean_retrieval()` | Perform boolean AND retrieval using inverted index |
| `rank_documents()` | Rank documents by term frequency similarity |
| `semantic_search()` | Perform semantic search (falls back to term frequency) |

#### Utility Functions

| Function | Description |
|----------|-------------|
| `validate_information()` | Validate and format name/address data |
| `format_query()` | Format person information queries |
| `calculate_user_distance()` | Calculate distance between points |
| `parse_user_order()` | Validate food orders against menu |
| `process_multiple_order_data()` | Process bulk order data |

##  Usage Examples

### Basic Search System

```python
from src.library_name import *

# Sample documents
docs = [
    {"doc_id": "1", "title": "Machine Learning", "text": "AI and ML algorithms"},
    {"doc_id": "2", "title": "Data Mining", "text": "Mining data from databases"}
]

# Normalize user query
query = normalize_query("  MACHINE    learning  ")  # Returns: "machine learning"

# Search and rank
results = filter_sort_paginate_results(docs, query.split(), min_score=1.0)

# Display results with highlighting
for doc in results['results']:
    highlighted_title = highlight_query_terms(doc['title'], query.split())
    print(f"{highlighted_title} (Score: {doc['score']})")
```

### Advanced Information Retrieval

```python
from src.library_name import build_inverted_index, boolean_retrieval, rank_documents

# Document collection for advanced IR
documents = [
    "machine learning algorithms for data analysis",
    "data mining techniques and methods", 
    "statistical analysis and machine learning",
    "database systems for data management"
]

# Build inverted index
index = build_inverted_index(documents)
print("Index built:", dict(index))

# Boolean retrieval - find documents containing ALL terms
results = boolean_retrieval("data machine", index)
print(f"Documents containing 'data' AND 'machine': {results}")

# Rank documents by relevance
ranked = rank_documents("machine learning", documents, top_k=3)
for doc_id, score in ranked:
    if score > 0:
        print(f"Doc {doc_id} (score: {score:.3f}): {documents[doc_id][:50]}...")
```

### Data Validation Pipeline

```python
from src.library_name import *

# Validate user information
try:
    user_info = validate_information("John, Doe", "123 Main Street")
    formatted = format_query("John Doe", 25, "USA")
    distance = calculate_user_distance(100, 25)
    
    print(f"User: {user_info}")
    print(f"Query: {formatted}")  
    print(f"Distance: {distance}")
except ValueError as e:
    print(f"Validation error: {e}")
```

### Order Processing System

```python
from src.library_name import parse_user_order, process_multiple_order_data

menu = ["pizza", "burger", "salad", "fries"]

# Process individual order
order = parse_user_order(menu, "pizza, fries")  # Returns: "pizza, fries"

# Process multiple orders
orders = ["Alice, pizza, 2", "Bob, burger, 1", "Carol, salad, 3"]
result = process_multiple_order_data(orders)
print(result)  # Returns formatted order summary
```

##  Testing

Run the test functions included in each module:

```bash
# Test core functions
python src/library_name.py

# Test utility functions  
python src/library_name.py

# Run comprehensive demo
python examples/demo_script.py
```
##  Requirements

- Python 3.7+
- No external dependencies required for core functionality

##  Use Cases

This library is perfect for:

- **Course Projects**: Information retrieval and search system assignments
- **Text Processing**: Basic NLP and text analysis tasks
- **Data Validation**: User input validation and formatting
- **Search Applications**: Building simple search interfaces
- **Learning**: Understanding IR concepts and implementations

##  Key Features in Detail

### Smart Search Scoring
- Title matches weighted 2x higher than body text
- Configurable minimum score thresholds
- Support for date-based sorting

### Robust Text Processing  
- Case-insensitive matching
- Punctuation handling
- Word boundary detection
- Intelligent text truncation

### Comprehensive Validation
- Input sanitization and cleaning
- Error handling with descriptive messages
- Type checking and conversion

### Flexible Pagination
- Safe bounds checking
- Metadata for navigation
- Configurable page sizes


---


