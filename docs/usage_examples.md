# Usage Examples and Tutorials

# Import specific functions
from src.library_name import filter_sort_paginate_results, highlight_query_terms, normalize_query
from src.library_name import validate_information, format_query

# Or import the entire module
import src.library_name as lib
```

### Normalizing and Processing Queries

```python
from src.library_name import normalize_query, count_term_frequency

# Clean up user input
user_query = "  Data    Mining   ALGORITHMS  "
clean_query = normalize_query(user_query)
print(f"Original: '{user_query}'")
print(f"Normalized: '{clean_query}'")
# Output: 'data mining algorithms'

# Count term occurrences
text = "Data mining is a process of mining data from large datasets using data mining algorithms"
count = count_term_frequency(text, "mining")
print(f"'mining' appears {count} times")
# Output: 'mining' appears 3 times
```

### Text Highlighting

```python
from src.library_name import highlight_query_terms

document_text = "Introduction to data mining and machine learning algorithms"
search_terms = ["data", "mining", "algorithms"]

# Basic HTML highlighting
highlighted = highlight_query_terms(document_text, search_terms)
print(highlighted)
# Output: Introduction to <b>data</b> <b>mining</b> and machine learning <b>algorithms</b>

# Custom highlighting with brackets
highlighted_custom = highlight_query_terms(document_text, search_terms, pre="[", post="]")
print(highlighted_custom)
# Output: Introduction to [data] [mining] and machine learning [algorithms]
```

## Tutorial 2: Document Search and Pagination

### Setting Up Document Collection

```python
from src.library_name import filter_sort_paginate_results, truncate_snippet

# Sample document collection
documents = [
    {
        "doc_id": "doc1",
        "title": "Introduction to Data Mining",
        "text": "Data mining is the process of discovering patterns in large datasets using machine learning algorithms.",
        "date": "2024-01-15"
    },
    {
        "doc_id": "doc2", 
        "title": "Machine Learning Fundamentals",
        "text": "Machine learning algorithms can automatically learn and improve from data without explicit programming.",
        "date": "2024-02-20"
    },
    {
        "doc_id": "doc3",
        "title": "Database Management Systems",
        "text": "Database systems store and organize data efficiently for quick retrieval and analysis.",
        "date": "2024-01-30"
    },
    {
        "doc_id": "doc4",
        "title": "Statistical Analysis Methods", 
        "text": "Statistical methods help analyze data patterns and draw meaningful conclusions from datasets.",
        "date": "2024-03-10"
    }
]
```

### Performing Search with Pagination

```python
# Search for documents containing "data" and "analysis"
search_terms = ["data", "analysis"]
results = filter_sort_paginate_results(
    results=documents,
    query_terms=search_terms,
    page=1,
    per_page=2,
    sort_by="score",
    min_score=1.0
)

print(f"Found {results['total_results']} results across {results['total_pages']} pages")
print(f"Showing page {results['page']}:")

for doc in results['results']:
    print(f"- {doc['title']} (Score: {doc['score']})")
    snippet = truncate_snippet(doc['text'], 80)
    print(f"  {snippet}")
    print()
```

### Advanced Search with Date Sorting

```python
# Search and sort by date
recent_results = filter_sort_paginate_results(
    results=documents,
    query_terms=["machine", "learning"],
    page=1,
    per_page=3,
    sort_by="date",
    min_score=0.5
)

print("Recent documents about machine learning:")
for doc in recent_results['results']:
    print(f"- {doc['title']} ({doc['date']}) - Score: {doc['score']}")
```

## Tutorial 3: Advanced Information Retrieval

### Building an Inverted Index

```python
from src.library_name import clean_text, build_inverted_index, boolean_retrieval

# Sample document collection
documents = [
    "machine learning algorithms for data analysis",
    "data mining techniques and algorithms", 
    "statistical methods for machine learning",
    "database systems and data management",
    "information retrieval and search algorithms"
]

# Build an inverted index
print("Building inverted index...")
index = build_inverted_index(documents)

# Display some index entries
print("Sample index entries:")
for term in ["data", "algorithms", "machine"]:
    if term in index:
        print(f"  '{term}' appears in documents: {sorted(index[term])}")
```

### Boolean Retrieval

```python
# Perform boolean AND searches
search_queries = [
    "data algorithms",
    "machine learning", 
    "statistical methods",
    "database systems"
]

print("\nBoolean retrieval results:")
for query in search_queries:
    results = boolean_retrieval(query, index)
    print(f"  Query '{query}': documents {sorted(results)}")
    
    # Show which documents match
    for doc_id in sorted(results):
        snippet = documents[doc_id][:50] + "..." if len(documents[doc_id]) > 50 else documents[doc_id]
        print(f"    Doc {doc_id}: {snippet}")
```

### Document Ranking

```python
from src.library_name import rank_documents

# Rank documents by relevance to queries
ranking_queries = [
    "machine learning algorithms",
    "data mining analysis", 
    "information retrieval systems"
]

print("\nDocument ranking results:")
for query in ranking_queries:
    ranked_docs = rank_documents(query, documents, top_k=3)
    print(f"\nQuery: '{query}'")
    
    for doc_id, score in ranked_docs:
        if score > 0:  # Only show relevant documents
            snippet = documents[doc_id][:60] + "..." if len(documents[doc_id]) > 60 else documents[doc_id]
            print(f"  Doc {doc_id} (score: {score:.3f}): {snippet}")
```

### Semantic Search

```python
from src.library_name import semantic_search

# Perform semantic search (falls back to term frequency)
semantic_queries = [
    "artificial intelligence methods",
    "knowledge discovery techniques",
    "computational algorithms"
]

print("\nSemantic search results:")
for query in semantic_queries:
    results = semantic_search(query, documents, top_k=2)
    print(f"\nQuery: '{query}'")
    
    for doc_id, score in results:
        if score > 0:
            snippet = documents[doc_id][:60] + "..." if len(documents[doc_id]) > 60 else documents[doc_id]
            print(f"  Doc {doc_id} (score: {score:.3f}): {snippet}")
```

### Complete Retrieval Pipeline

```python
def complete_search_pipeline(query: str, documents: list, use_boolean: bool = False):
    """Demonstrate a complete search pipeline with multiple methods."""
    print(f"🔍 Searching for: '{query}'")
    print("-" * 50)
    
    # Step 1: Clean the query
    clean_query = clean_text(query)
    print(f"📝 Cleaned query: '{clean_query}'")
    
    # Step 2: Build index for boolean search
    index = build_inverted_index(documents)
    
    if use_boolean:
        # Boolean retrieval
        bool_results = boolean_retrieval(query, index)
        print(f"🔎 Boolean search found {len(bool_results)} documents: {sorted(bool_results)}")
    
    # Step 3: Ranked retrieval
    ranked_results = rank_documents(query, documents, top_k=3)
    print(f"📊 Top ranked documents:")
    
    for i, (doc_id, score) in enumerate(ranked_results, 1):
        if score > 0:
            snippet = documents[doc_id][:80] + "..." if len(documents[doc_id]) > 80 else documents[doc_id]
            print(f"  {i}. Doc {doc_id} (score: {score:.3f})")
            print(f"     {snippet}")
    
    print()

# Run complete pipeline examples
example_queries = [
    "machine learning",
    "data analysis", 
    "algorithms"
]

for query in example_queries:
    complete_search_pipeline(query, documents, use_boolean=True)
```

## Tutorial 4: Data Validation and Processing

### Information Validation

```python
from src.library_name import validate_information, format_query

# Clean and validate user information
raw_name = "  John   ,   Doe  "
raw_address = "123   Main    Street"

try:
    clean_info = validate_information(raw_name, raw_address)
    print(f"Validated: {clean_info}")
    # Output: John Doe - 123 Main Street
except ValueError as e:
    print(f"Validation error: {e}")

# Format person query
person_info = format_query("Alice Johnson", 28, "Canada")
print(f"Formatted: {person_info}")
# Output: Alice Johnson, 28 (Canada)
```

### Distance Calculations

```python
from src.library_name import calculate_user_distance

try:
    # Calculate distance difference
    distance = calculate_user_distance(150, 75)
    print(f"Distance difference: {distance}")
    # Output: Distance difference: 75 km
    
    # This will raise an error
    invalid_distance = calculate_user_distance(-10, 50)
except ValueError as e:
    print(f"Error: {e}")
```

## Tutorial 4: Order Processing System

### Menu Validation and Order Processing

```python
from src.library_name import parse_user_order, process_multiple_order_data

# Restaurant menu
menu_items = [
    "cheeseburger", "pizza", "salad", "pasta", 
    "chicken sandwich", "fries", "ice cream"
]

# Process individual order
try:
    user_order = "cheeseburger, fries, ice cream"
    validated_order = parse_user_order(menu_items, user_order)
    print(f"Valid order: {validated_order}")
    
    # This will raise an error for invalid item
    invalid_order = "cheeseburger, tacos, fries"
    parse_user_order(menu_items, invalid_order)
except ValueError as e:
    print(f"Order error: {e}")
```

### Bulk Order Processing

```python
# Process multiple customer orders
order_data = [
    "Alice, cheeseburger, 2",
    "Bob, pizza, 1", 
    "Carol, pasta, 3",
    "David, salad, 1"
]

try:
    processed_orders = process_multiple_order_data(order_data)
    print("Processed orders:")
    print(processed_orders)
    # Output:
    # Alice: 2 cheeseburgers
    # Bob: 1 pizza
    # Carol: 3 pastas
    # David: 1 salad
except ValueError as e:
    print(f"Processing error: {e}")
```

## Tutorial 5: Complete Search Application

Here's a complete example combining multiple functions:

```python
from src.library_name import *

def search_application():
    # Sample documents
    docs = [
        {"doc_id": "1", "title": "Python Programming", "text": "Learn Python programming fundamentals"},
        {"doc_id": "2", "title": "Data Science Guide", "text": "Complete guide to data science with Python"},
        {"doc_id": "3", "title": "Web Development", "text": "Building web applications with modern frameworks"}
    ]
    
    # User search
    user_input = "  PYTHON   programming  "
    query = normalize_query(user_input)
    print(f"Searching for: '{query}'")
    
    # Perform search
    results = filter_sort_paginate_results(docs, query.split(), page=1, per_page=5)
    
    print(f"\\nFound {results['total_results']} results:")
    for doc in results['results']:
        title = highlight_query_terms(doc['title'], query.split())
        snippet = truncate_snippet(doc['text'], 50)
        highlighted_snippet = highlight_query_terms(snippet, query.split())
        
        print(f"\\n{title} (Score: {doc['score']})")
        print(f"  {highlighted_snippet}")

# Run the application
if __name__ == "__main__":
    search_application()
```

## Best Practices

1. **Always normalize queries** before processing to ensure consistent results
2. **Use appropriate pagination** to handle large result sets efficiently  
3. **Validate input data** before processing to avoid errors
4. **Handle exceptions** appropriately in production code
5. **Set reasonable minimum scores** to filter out irrelevant results
6. **Use descriptive variable names** and add comments for clarity

## Common Patterns

### Pattern 1: Search Pipeline
```python
query = normalize_query(user_input)
terms = query.split()
results = filter_sort_paginate_results(documents, terms)
for doc in results['results']:
    highlighted_text = highlight_query_terms(doc['text'], terms)
    # Display results...
```

### Pattern 2: Data Validation Pipeline  
```python
try:
    validated_info = validate_information(name, address)
    formatted_query = format_query(name, age, country)
    # Process validated data...
except ValueError as e:
    # Handle validation errors...
```

### Pattern 3: Order Processing Pipeline
```python
try:
    validated_order = parse_user_order(menu, order)
    processed_orders = process_multiple_order_data(order_list)
    # Complete order processing...
except ValueError as e:
    # Handle order errors...
```
