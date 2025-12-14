# INST326 Search and Order Management System

A comprehensive Python system that integrates document search capabilities with user management and order processing. Features complete data persistence, multiple import/export formats, and a sophisticated object-oriented architecture with inheritance and polymorphism.

## � Project 4: Complete System Integration

This project has evolved through multiple phases:
- **Project 1**: Core function library for text processing and information retrieval
- **Project 2**: Object-oriented design with Document and SearchQuery classes
- **Project 3**: Advanced OOP with inheritance, polymorphism, and abstract base classes
- **Project 4**: Complete system integration with data persistence and I/O capabilities

## Team Members

- **Ishaan Patel**: System architecture, persistence layer, and integration
- **Rushan Heaven**: Search engine implementation and text processing
- **Zachary Tong**: User management and order processing system

## Domain Problem

Our system addresses the dual needs of:
1. **Information Retrieval**: Sophisticated document search with multiple search engines
2. **Order Management**: Food ordering and user management system

This combination serves educational institutions, restaurants, or businesses that need both knowledge management and ordering capabilities.

## Key Features

### 🔍 Advanced Search System
- **Multiple Search Engines**: Boolean, Ranked, and Semantic search with polymorphic design
- **Abstract Base Classes**: Enforced interface contracts through ABC
- **Inheritance Hierarchy**: Specialized search engines with shared functionality
- **Query Processing**: Sophisticated normalization and term analysis

### 📊 Data Persistence & I/O
- **State Management**: Save/load complete system state between sessions
- **Import Capabilities**: CSV, JSON, and XML document import
- **Export Features**: Multiple format export for search results and reports
- **Error Handling**: Robust file I/O with graceful error management

### 👤 User & Order Management
- **User Profiles**: Persistent user preferences and search history
- **Order Processing**: Complete food ordering workflow
- **Session Tracking**: User activity monitoring and analytics
## Installation & Setup

### Requirements
- Python 3.8+
- No external dependencies required (uses only standard library)

### Setup Instructions

1. **Clone the repository**:
```bash
git clone <repository-url>
cd INST326_GICodeProject
```

2. **No installation needed** - the system uses only Python standard library

3. **Initialize with sample data**:
```bash
# Import sample documents
python main.py --import-csv data/sample_documents.csv
python main.py --import-xml data/sample_documents.xml
```

## Usage Guide

### Command Line Interface

**Basic search**:
```bash
python main.py --search "Python programming" --engine ranked
```

**Search with user tracking**:
```bash
python main.py --search "data science" --user-id "student123" --engine semantic
```

**Import and export**:
```bash
# Import from CSV
python main.py --import-csv your_documents.csv

# Search and export results
python main.py --search "machine learning" --export results.json --export-format json
```

**Generate reports**:
```bash
python main.py --report summary
python main.py --report user_activity
python main.py --report popular_searches
```

**Interactive mode**:
```bash
python main.py --interactive
```

### Python API Usage

```python
from main import SearchOrderSystem

# Initialize system
system = SearchOrderSystem("data")

# Search documents
results = system.search_documents("Python", "ranked", "user123")

# Place order
order = system.place_order("user123", "pizza, soda")

# Generate reports
report = system.generate_report("summary")

# Save state
system.save_system_state()
```

## Testing

### Run the complete test suite:
```bash
python tests/test_project4.py
```

### Run specific component tests:
```bash
# Test search system (inheritance/polymorphism)
python tests/test_search_system.py

# Test Team 3 composition patterns
python tests/Team_member_3_Summary.py
```

### Test Coverage
- **System Integration**: Complete workflows from import to export
- **Data Persistence**: Save/load state functionality
- **I/O Operations**: CSV, JSON, XML import/export
- **Search Engines**: All three engines with various queries
- **Error Handling**: File errors, invalid data, edge cases
- **User Management**: Profile creation, history tracking
- **Order Processing**: Complete order lifecycle

## Architecture Overview

### Core Components

1. **SearchOrderSystem**: Main application class coordinating all functionality
2. **Search Engine Hierarchy**: Abstract base class with concrete implementations
3. **Document Management**: Document class with text processing capabilities
4. **User Management**: UserProfile with preferences and history
5. **Persistence Layer**: JSON-based state management with error handling

### Design Patterns Used

- **Abstract Base Classes**: Enforced interfaces for search engines
- **Inheritance**: Specialized search engine implementations
- **Polymorphism**: Unified search interface with engine-specific behavior
- **Composition**: System components working together
- **Context Managers**: Proper file handling with `with` statements

## File Structure

```
INST326_GICodeProject/
├── main.py                 # Main application entry point
├── data/                   # Data storage directory
│   ├── documents.json      # Persisted documents
│   ├── users.json          # User profiles and history
│   ├── orders.json         # Order history
│   ├── session.json        # Session data
│   ├── sample_documents.csv # Sample CSV import
│   └── sample_documents.xml # Sample XML import
├── src/                    # Source code modules
│   ├── search_system.py    # Search engine hierarchy
│   ├── document.py         # Document class
│   ├── search_query.py     # Query processing
│   ├── userprofile.py      # User management
│   └── library_name.py     # Original function library
├── tests/                  # Test suite
│   ├── test_project4.py    # Comprehensive system tests
│   ├── test_search_system.py # Search engine tests
│   └── Team_member_3_Summary.py # Composition demo
├── docs/                   # Documentation
└── README.md              # This file
```

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


