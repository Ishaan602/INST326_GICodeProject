# Function Reference

This document provides detailed documentation for all functions in the INST326 Information Retrieval Function Library.

## Core Information Retrieval Functions (`src/library_name.py`)

### `filter_sort_paginate_results(results, query_terms, page=1, per_page=10, sort_by="score", min_score=0.0)`

Filter, score, sort, and paginate search results based on query terms.

**Parameters:**
- `results` (list[dict]): List of documents to search through. Each document should have keys: "doc_id", "title", "text", and optionally "date"
- `query_terms` (list[str]): List of search terms to match against
- `page` (int, optional): Page number to return (1-indexed). Defaults to 1.
- `per_page` (int, optional): Number of results per page. Defaults to 10.
- `sort_by` (str, optional): Sort method - "score" or "date". Defaults to "score".
- `min_score` (float, optional): Minimum score threshold for inclusion. Defaults to 0.0.

**Returns:**
- `dict`: Dictionary containing "results", "page", "per_page", "total_results", "total_pages"

**Example:**
```python
docs = [{"doc_id": "1", "title": "Data Mining", "text": "About data"}]
result = filter_sort_paginate_results(docs, ["data"], page=1, per_page=5)
# Returns: {'results': [{'doc_id': '1', 'title': 'Data Mining', 'text': 'About data', 'score': 3}], 'page': 1, 'per_page': 5, 'total_results': 1, 'total_pages': 1}
```

---

### `highlight_query_terms(text, terms, pre="<b>", post="</b>")`

Highlight matching query terms in text by wrapping them with specified tags.

**Parameters:**
- `text` (str): The text to search and highlight within
- `terms` (list[str]): List of terms to highlight in the text
- `pre` (str, optional): Opening tag/text to wrap matches. Defaults to "<b>".
- `post` (str, optional): Closing tag/text to wrap matches. Defaults to "</b>".

**Returns:**
- `str`: Text with matching terms wrapped in pre/post tags

**Example:**
```python
highlight_query_terms("Intro to data mining", ["data", "mining"])
# Returns: 'Intro to <b>data</b> <b>mining</b>'
```

---

### `normalize_query(query)`

Normalize a search query by standardizing case and whitespace.

**Parameters:**
- `query` (str): The search query string to normalize

**Returns:**
- `str`: Normalized query string in lowercase with standardized spacing

**Raises:**
- `AttributeError`: If query is not a string type

**Example:**
```python
normalize_query("  Hello   WORLD  ")
# Returns: 'hello world'
```

---

### `truncate_snippet(text, max_chars=160)`

Truncate text at word boundaries with ellipsis when over character limit.

**Parameters:**
- `text` (str): The text to potentially truncate
- `max_chars` (int, optional): Maximum allowed characters. Defaults to 160.

**Returns:**
- `str`: Original text if under limit, or truncated text with ellipsis

**Example:**
```python
truncate_snippet("This is a very long sentence that needs truncating", 20)
# Returns: 'This is a very long…'
```

---

### `count_term_frequency(text, term)`

Count occurrences of a specific term in text (case-insensitive, whole words).

**Parameters:**
- `text` (str): The text to search within
- `term` (str): The specific term to count occurrences of

**Returns:**
- `int`: Number of times the term appears as a complete word

**Example:**
```python
count_term_frequency("Data mining is about mining data", "mining")
# Returns: 2
```

---

### `clean_text(text)`

Clean and normalize text by converting to lowercase.

**Parameters:**
- `text` (str): Text to clean and normalize

**Returns:**
- `str`: Lowercase version of the input text

**Example:**
```python
clean_text("Hello WORLD!")
# Returns: 'hello world!'
```

---

### `build_inverted_index(documents)`

Build an inverted index mapping terms to document IDs.

**Parameters:**
- `documents` (List[str]): List of documents to index

**Returns:**
- `Dict[str, Set[int]]`: Dictionary mapping each term to set of document IDs containing it

**Example:**
```python
docs = ["cat dog", "dog bird", "cat bird"]
index = build_inverted_index(docs)
# Returns: {'cat': {0, 2}, 'dog': {0, 1}, 'bird': {1, 2}}
```

---

### `boolean_retrieval(query, inverted_index)`

Perform boolean AND retrieval using an inverted index.

**Parameters:**
- `query` (str): Query string with terms to search for
- `inverted_index` (Dict[str, Set[int]]): Inverted index mapping terms to document IDs

**Returns:**
- `Set[int]`: Set of document IDs that contain ALL query terms

**Example:**
```python
docs = ["cat dog", "dog bird", "cat bird"]
index = build_inverted_index(docs)
boolean_retrieval("cat dog", index)
# Returns: {0}
```

---

### `rank_documents(query, documents, top_k=5)`

Rank documents based on term frequency similarity to query.

**Parameters:**
- `query` (str): Search query string
- `documents` (List[str]): List of documents to rank
- `top_k` (int, optional): Number of top results to return. Defaults to 5.

**Returns:**
- `List[tuple]`: List of (doc_index, score) tuples sorted by relevance

**Example:**
```python
docs = ["data mining algorithms", "machine learning methods", "database systems"]
rank_documents("data mining", docs, top_k=2)
# Returns: [(0, 0.6666666666666666), (2, 0.0)]
```

---

### `semantic_search(query, documents, model=None, top_k=5)`

Perform semantic search on documents (falls back to term frequency ranking).

**Parameters:**
- `query` (str): Search query string
- `documents` (List[str]): List of documents to search
- `model`: Optional semantic model (not implemented)
- `top_k` (int, optional): Number of top results to return. Defaults to 5.

**Returns:**
- `List[tuple]`: List of (doc_index, score) tuples sorted by relevance

**Example:**
```python
docs = ["machine learning algorithms", "data science methods", "web development"]
semantic_search("AI techniques", docs, top_k=2)
# Returns: [(0, 0.5), (1, 0.25)]
```

## Utility Functions

### `validate_information(name, address)`

Validate and format name and address information.

**Parameters:**
- `name` (str): Name of person
- `address` (str): Address of person

**Returns:**
- `str`: Formatted string as "Name - Address"

**Raises:**
- `ValueError`: If name and address are empty strings

**Example:**
```python
validate_information("Tim  ,  Cook", "23 Candy Lane")
# Returns: 'Tim Cook - 23 Candy Lane'
```

---

### `format_query(name, age, country)`

Format person information as a query string.

**Parameters:**
- `name` (str): Name of person
- `age` (int): Age of person
- `country` (str): Country of origin

**Returns:**
- `str`: Formatted string as "Name, Age (Country)"

**Example:**
```python
format_query(" Bonnie  ", 28, "United States")
# Returns: 'Bonnie, 28 (United States)'
```

---

### `calculate_user_distance(distance1, distance2)`

Calculate the difference between two distances.

**Parameters:**
- `distance1` (int): First distance number
- `distance2` (int): Second distance number

**Returns:**
- `str`: Difference with "km" unit

**Raises:**
- `ValueError`: If either distance is less than 0

**Example:**
```python
calculate_user_distance(200, 150)
# Returns: '50 km'
```

---

### `parse_user_order(food_items, user_order)`

Parse and validate a user's food order against a menu.

**Parameters:**
- `food_items` (list[str]): List of foods available on the menu
- `user_order` (str): Comma-separated order items

**Returns:**
- `str`: Validated order string

**Raises:**
- `ValueError`: If any item is not on the menu

**Example:**
```python
parse_user_order(['sushi', 'ice cream', 'fish'], 'sushi, ice cream')
# Returns: 'sushi, ice cream'
```

---

### `process_multiple_order_data(order_data)`

Process order data from multiple people.

**Parameters:**
- `order_data` (list[str]): List of order strings in format "Name, Item, Quantity"

**Returns:**
- `str`: Formatted order summary for all people

**Raises:**
- `ValueError`: If order list length < 3 or quantity not between 1-5

**Example:**
```python
order_data = ["Adrian, cheeseburger, 2", "Bob, snack wrap, 1", "Cory, pizza, 2"]
process_multiple_order_data(order_data)
# Returns: 'Adrian: 2 cheeseburgers\nBob: 1 snack wrap\nCory: 2 pizzas'
```
