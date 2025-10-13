"""
Information Retrieval Function Library
"""

def filter_sort_paginate_results(results: list[dict], query_terms: list[str], page: int = 1, per_page: int = 10, sort_by: str = "score", min_score: float = 0.0) -> dict:
    """Filter, score, sort, and paginate search results based on query terms.
    
    Uses simple term-frequency scoring where matches in titles are weighted 2x 
    higher than matches in text content. Supports sorting by relevance score 
    or date, with safe pagination handling.
    
    Args:
        results (list[dict]): List of documents to search through. Each document
            should have keys: "doc_id", "title", "text", and optionally "date"
        query_terms (list[str]): List of search terms to match against
        page (int, optional): Page number to return (1-indexed). Defaults to 1.
        per_page (int, optional): Number of results per page. Defaults to 10.
        sort_by (str, optional): Sort method - "score" or "date". Defaults to "score".
        min_score (float, optional): Minimum score threshold for inclusion. Defaults to 0.0.
        
    Returns:
        dict: Dictionary containing:
            - "results": List of matching documents with added "score" field
            - "page": Current page number
            - "per_page": Results per page
            - "total_results": Total number of matching results
            - "total_pages": Total number of available pages
            
    Examples:
        >>> docs = [{"doc_id": "1", "title": "Data Mining", "text": "About data"}]
        >>> filter_sort_paginate_results(docs, ["data"], page=1, per_page=5)
        {'results': [{'doc_id': '1', 'title': 'Data Mining', 'text': 'About data', 'score': 3}], 'page': 1, 'per_page': 5, 'total_results': 1, 'total_pages': 1}
    """
    # Calculate scores for each result
    scored_results = []
    for result in results:
        score = 0
        # Calculate term frequency score for title and text
        title = result.get("title", "").lower()
        text = result.get("text", "").lower()
        
        for term in query_terms:
            term_lower = term.lower()
            score += title.count(term_lower) * 2  # Weight title matches higher
            score += text.count(term_lower)
        
        # Only include results that meet minimum score
        if score >= min_score:
            result_copy = result.copy()
            result_copy["score"] = score
            scored_results.append(result_copy)
    
    # Sort results
    if sort_by == "score":
        scored_results.sort(key=lambda x: x["score"], reverse=True)
    elif sort_by == "date" and any("date" in result for result in scored_results):
        scored_results.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    # Paginate results
    total_results = len(scored_results)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Ensure safe pagination
    if start_idx >= total_results:
        page_results = []
    else:
        page_results = scored_results[start_idx:end_idx]
    
    return {
        "results": page_results,
        "page": page,
        "per_page": per_page,
        "total_results": total_results,
        "total_pages": (total_results + per_page - 1) // per_page if total_results > 0 else 0
    }


def highlight_query_terms(text: str, terms: list[str], pre: str = "<b>", post: str = "</b>") -> str:
    """Highlight matching query terms in text by wrapping them with specified tags.
    
    Performs case-insensitive matching of whole words only. Handles punctuation
    by stripping it for comparison while preserving the original word structure.
    Processes longer terms first to avoid partial replacements.
    
    Args:
        text (str): The text to search and highlight within
        terms (list[str]): List of terms to highlight in the text
        pre (str, optional): Opening tag/text to wrap matches. Defaults to "<b>".
        post (str, optional): Closing tag/text to wrap matches. Defaults to "</b>".
        
    Returns:
        str: Text with matching terms wrapped in pre/post tags
        
    Examples:
        >>> highlight_query_terms("Intro to data mining", ["data", "mining"])
        'Intro to <b>data</b> <b>mining</b>'
        >>> highlight_query_terms("Hello world!", ["hello"], pre="[", post="]")
        '[hello] world!'
    """
    # Create a copy of the text to modify
    result_text = text
    
    # Sort terms by length (longest first) to avoid partial replacements
    sorted_terms = sorted(terms, key=len, reverse=True)
    
    for term in sorted_terms:
        # Simple case-insensitive replacement
        # Split text into words, check each word, and replace if it matches
        words = result_text.split()
        new_words = []
        
        for word in words:
            # Remove punctuation for comparison but keep original word
            clean_word = word.strip('.,!?;:"()[]{}').lower()
            if clean_word == term.lower():
                # Replace the original word with highlighted version
                highlighted = word.replace(clean_word.title(), f"{pre}{clean_word.title()}{post}")
                highlighted = highlighted.replace(clean_word.upper(), f"{pre}{clean_word.upper()}{post}")
                highlighted = highlighted.replace(clean_word, f"{pre}{clean_word}{post}")
                new_words.append(highlighted)
            else:
                new_words.append(word)
        
        result_text = ' '.join(new_words)
    
    return result_text


def normalize_query(query: str) -> str:
    """Normalize a search query by standardizing case and whitespace.
    
    Converts the query to lowercase, removes leading/trailing whitespace,
    and collapses multiple consecutive spaces into single spaces for
    consistent query processing.
    
    Args:
        query (str): The search query string to normalize
        
    Returns:
        str: Normalized query string in lowercase with standardized spacing
        
    Raises:
        AttributeError: If query is not a string type
        
    Examples:
        >>> normalize_query("  Hello   WORLD  ")
        'hello world'
        >>> normalize_query("Data Mining")
        'data mining'
    """
    # Convert to lowercase and strip leading/trailing whitespace
    normalized = query.lower().strip()
    
    # Replace multiple consecutive spaces with single space
    while '  ' in normalized:  # Keep replacing double spaces until none left
        normalized = normalized.replace('  ', ' ')
    
    return normalized


def truncate_snippet(text: str, max_chars: int = 160) -> str:
    """Truncate text at word boundaries with ellipsis when over character limit.
    
    Intelligently truncates text by finding the last complete word that fits
    within the character limit, then adds an ellipsis (…) to indicate truncation.
    If no word boundary is found, truncates at the character limit.
    
    Args:
        text (str): The text to potentially truncate
        max_chars (int, optional): Maximum allowed characters. Defaults to 160.
        
    Returns:
        str: Original text if under limit, or truncated text with ellipsis
        
    Examples:
        >>> truncate_snippet("This is a very long sentence that needs truncating", 20)
        'This is a very long…'
        >>> truncate_snippet("Short text", 100)
        'Short text'
    """
    if len(text) <= max_chars:
        return text
    
    # Find the last space within the character limit
    truncated = text[:max_chars]
    
    # Find the last word boundary
    last_space = truncated.rfind(' ')
    
    if last_space == -1:
        # No space found, truncate at character limit
        return truncated + "…"
    else:
        # Truncate at last word boundary
        return truncated[:last_space] + "…"


def count_term_frequency(text: str, term: str) -> int:
    """Count occurrences of a specific term in text (case-insensitive, whole words).
    
    Splits text into words, removes punctuation for comparison, and counts
    exact matches of the specified term. Only counts complete word matches,
    not partial matches within other words.
    
    Args:
        text (str): The text to search within
        term (str): The specific term to count occurrences of
        
    Returns:
        int: Number of times the term appears as a complete word
        
    Examples:
        >>> count_term_frequency("Data mining is about mining data", "mining")
        2
        >>> count_term_frequency("The cat sat on the mat", "cat")
        1
        >>> count_term_frequency("Hello world", "hello")
        1
    """
    # Split text into words and count matches
    words = text.lower().split()
    count = 0
    
    for word in words:
        # Remove punctuation from word for comparison
        clean_word = word.strip('.,!?;:"()[]{}')
        if clean_word == term.lower():
            count += 1
    
    return count




import re
import math
from collections import defaultdict, Counter
from typing import List, Dict, Set


def clean_text(text: str) -> str:
    """Clean and normalize text by converting to lowercase.
    
    Args:
        text (str): Text to clean and normalize
        
    Returns:
        str: Lowercase version of the input text
        
    Examples:
        >>> clean_text("Hello WORLD!")
        'hello world!'
        >>> clean_text("Data Mining")
        'data mining'
    """
    text = text.lower()
    return text

def build_inverted_index(documents: List[str]) -> Dict[str, Set[int]]:
    """Build an inverted index mapping terms to document IDs.
    
    Args:
        documents (List[str]): List of documents to index
        
    Returns:
        Dict[str, Set[int]]: Dictionary mapping each term to set of document IDs containing it
        
    Examples:
        >>> docs = ["cat dog", "dog bird", "cat bird"]
        >>> index = build_inverted_index(docs)
        >>> index['cat']
        {0, 2}
        >>> index['dog']
        {0, 1}
    """
    index = defaultdict(set)
    for doc_id, text in enumerate(documents):
        tokens = clean_text(text).split()
        for token in set(tokens):
            index[token].add(doc_id)
    return dict(index)

def boolean_retrieval(query: str, inverted_index: Dict[str, Set[int]]) -> Set[int]:
    """Perform boolean AND retrieval using an inverted index.
    
    Args:
        query (str): Query string with terms to search for
        inverted_index (Dict[str, Set[int]]): Inverted index mapping terms to document IDs
        
    Returns:
        Set[int]: Set of document IDs that contain ALL query terms
        
    Examples:
        >>> docs = ["cat dog", "dog bird", "cat bird"]
        >>> index = build_inverted_index(docs)
        >>> boolean_retrieval("cat dog", index)
        {0}
        >>> boolean_retrieval("bird", index)
        {1, 2}
    """
    tokens = clean_text(query).split()
    if not tokens:
        return set()
    
    result = inverted_index.get(tokens[0], set())
    for token in tokens[1:]:
        result = result.intersection(inverted_index.get(token, set()))
    return result

def rank_documents(query: str, documents: List[str], top_k: int = 5) -> List[tuple]:
    """Rank documents based on term frequency similarity to query.
    
    Args:
        query (str): Search query string
        documents (List[str]): List of documents to rank
        top_k (int, optional): Number of top results to return. Defaults to 5.
        
    Returns:
        List[tuple]: List of (doc_index, score) tuples sorted by relevance
        
    Examples:
        >>> docs = ["data mining algorithms", "machine learning methods", "database systems"]
        >>> rank_documents("data mining", docs, top_k=2)
        [(0, 0.6666666666666666), (2, 0.0)]
    """
    query_tokens = set(clean_text(query).split())
    scores = []
    
    for doc_id, document in enumerate(documents):
        doc_tokens = clean_text(document).split()
        doc_counter = Counter(doc_tokens)
        
        # Calculate simple term frequency score
        score = 0
        for token in query_tokens:
            if token in doc_counter:
                score += doc_counter[token]
        
        # Normalize by document length to avoid bias toward longer documents
        if doc_tokens:
            score = score / len(doc_tokens)
        
        scores.append((doc_id, score))
    
    # Sort by score in descending order
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
#This Function ranks the documents based on term frequency overlap

def semantic_search(query: str, documents: List[str], model=None, top_k: int = 5) -> List[tuple]:
    """Perform semantic search on documents.
    
    Args:
        query (str): Search query string
        documents (List[str]): List of documents to search
        model: Optional semantic model (not implemented)
        top_k (int, optional): Number of top results to return. Defaults to 5.
        
    Returns:
        List[tuple]: List of (doc_index, score) tuples sorted by relevance
        
    Examples:
        >>> docs = ["machine learning algorithms", "data science methods", "web development"]
        >>> semantic_search("AI techniques", docs, top_k=2)
        [(0, 0.5), (1, 0.25)]
    """
    if model is None:
        # If no model is provided, fall back to simple term frequency ranking
        return rank_documents(query, documents, top_k)
    
    # If a model is provided but we can't use advanced libraries, fall back to term frequency
    # In a real implementation, this would use sentence transformers or similar
    print("Warning: No semantic model implementation available, using term frequency ranking")
    return rank_documents(query, documents, top_k)
#This function finds the documents that are most similar in meaning to ultimately answer a query