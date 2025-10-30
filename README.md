# INST326 Information Retrieval Function Library

A comprehensive Python library for information retrieval, text processing, and data validation operations. Developed for INST326 coursework, this library provides essential functions for building search systems, processing user data, and managing information retrieval workflows.

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
│   ├── __init__.py            # Package initialization
│   └── library_name.py        # All functions (IR and utility functions)
├── docs/                        # Documentation directory
│   ├── function_reference.md   # Detailed function documentation
│   └── usage_examples.md       # Usage examples and tutorials
├── examples/                    # Example usage scripts
│   └── demo_script.py          # Comprehensive demonstration script
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

# Example: Validate information
clean_info = validate_information("John Doe", "123 Main St")
print(clean_info)  # Output: John Doe - 123 Main St
```

### Run the Demo

To see all features in action:

```bash
python examples/demo_script.py
```

##  Documentation

### Function Reference
- **[Complete Function Reference](docs/function_reference.md)** - Detailed documentation for all functions
- **[Usage Examples](docs/usage_examples.md)** - Practical examples and tutorials

### Core Functions Overview

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


