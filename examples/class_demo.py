
"""
Demonstration Script for Document and SearchQuery Classes

This script demonstrates the functionality of the Document and SearchQuery classes
created from the Project 1 function library. It shows how the classes integrate
the original functions in an object-oriented design.
"""

import sys
import os

from src.document import Document
from src.search_query import SearchQuery


def demo_document_class():
    """Demonstrate Document class functionality."""
    print("=== Document Class Demonstration ===\n")
    
    # Create a sample document
    doc = Document(
        doc_id="1",
        title="Introduction to Data Mining",
        content="Data mining is the process of discovering patterns in large data sets. "
                "It involves methods at the intersection of machine learning, statistics, "
                "and database systems. Data mining techniques are used to extract "
                "useful information from data warehouses.",
        metadata={"author": "John Smith", "year": 2024}
    )
    
    print("1. Document Creation:")
    print(f"   Document ID: {doc.doc_id}")
    print(f"   Title: {doc.title}")
    print(f"   Content Length: {doc.get_word_count()} words")
    print(f"   Metadata: {doc.metadata}")
    print()
    
    print("2. Text Cleaning:")
    print(f"   Original: {doc.content[:50]}...")
    print(f"   Cleaned:  {doc.clean_content()[:50]}...")
    print()
    
    print("3. Snippet Creation:")
    print(f"   Short snippet (50 chars): {doc.create_snippet(50)}")
    print(f"   Medium snippet (100 chars): {doc.create_snippet(100)}")
    print()
    
    print("4. Term Frequency Counting:")
    print(f"   'data' appears {doc.count_term_occurrences('data')} times")
    print(f"   'mining' appears {doc.count_term_occurrences('mining')} times")
    print(f"   'machine' appears {doc.count_term_occurrences('machine')} times")
    print()
    
    print("5. Query Term Highlighting:")
    highlighted = doc.highlight_terms(['data', 'mining', 'machine'], pre='**', post='**')
    print(f"   Highlighted: {highlighted}")
    print()
    
    print("6. String Representations:")
    print(f"   str(): {str(doc)}")
    print(f"   repr(): {repr(doc)}")
    print()


def demo_search_query_class():
    """Demonstrate SearchQuery class functionality."""
    print("=== SearchQuery Class Demonstration ===\n")
    
    # Create a sample query
    query = SearchQuery("  Data   MINING   techniques  ")
    
    print("1. Query Creation and Normalization:")
    print(f"   Original: '{query.original_query}'")
    print(f"   Normalized: '{query.normalized_query}'")
    print(f"   Terms: {query.query_terms}")
    print()
    
    # Sample documents for search
    documents = [
        "Data mining is a powerful technique for extracting patterns from large datasets",
        "Machine learning algorithms can be used for predictive data analysis",
        "Database systems store and manage large amounts of structured data",
        "Data mining techniques include clustering, classification, and association rules",
        "Statistical analysis helps in understanding data distributions and patterns"
    ]
    
    print("2. Document Collection:")
    for i, doc in enumerate(documents):
        print(f"   Doc {i}: {doc}")
    print()
    
    print("3. Boolean Search (AND operation):")
    boolean_results = query.boolean_search(documents)
    print(f"   Documents containing ALL terms {query.query_terms}: {sorted(boolean_results)}")
    for doc_id in sorted(boolean_results):
        print(f"   → Doc {doc_id}: {documents[doc_id]}")
    print()
    
    print("4. Ranked Search (Term Frequency):")
    ranked_results = query.rank_documents(documents, top_k=3)
    print(f"   Top 3 documents by relevance:")
    for i, (doc_id, score) in enumerate(ranked_results):
        print(f"   {i+1}. Doc {doc_id} (score: {score:.3f}): {documents[doc_id]}")
    print()
    
    print("5. Semantic Search (fallback to TF ranking):")
    semantic_results = query.semantic_search(documents, top_k=2)
    print(f"   Top 2 documents by semantic similarity:")
    for i, (doc_id, score) in enumerate(semantic_results):
        print(f"   {i+1}. Doc {doc_id} (score: {score:.3f}): {documents[doc_id]}")
    print()
    
    print("6. Query Statistics:")
    stats = query.get_query_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    print("7. Query Updates and History:")
    query.update_query("machine learning algorithms")
    print(f"   Updated query: '{query.normalized_query}'")
    print(f"   Search history: {query.search_history}")
    print()
    
    print("8. Similar Query Finding:")
    other_queries = ["deep learning methods", "data analysis techniques", "web development"]
    similar = query.get_similar_queries(other_queries, threshold=0.2)
    print(f"   Similar queries: {similar}")
    print()
    
    print("9. String Representations:")
    print(f"   str(): {str(query)}")
    print(f"   repr(): {repr(query)}")
    print()


def demo_integration():
    """Demonstrate integration between Document and SearchQuery classes."""
    print("=== Integration Demonstration ===\n")
    
    # Create documents
    docs = [
        Document("1", "AI Research", "Artificial intelligence and machine learning research"),
        Document("2", "Data Science", "Data science techniques for business analytics"),
        Document("3", "Database Design", "Relational database design and optimization")
    ]
    
    # Create search query
    query = SearchQuery("data machine")
    
    print("1. Document Collection:")
    for doc in docs:
        print(f"   {doc}")
    print()
    
    print("2. Search Integration:")
    
    # Extract document contents for search
    doc_contents = [doc.content for doc in docs]
    
    # Perform boolean search
    boolean_results = query.boolean_search(doc_contents)
    print(f"   Boolean search results: {sorted(boolean_results)}")
    
    # Perform ranked search
    ranked_results = query.rank_documents(doc_contents, top_k=2)
    print(f"   Top ranked documents:")
    
    for rank, (doc_id, score) in enumerate(ranked_results):
        doc = docs[doc_id]
        highlighted_content = doc.highlight_terms(query.query_terms)
        snippet = doc.create_snippet(80)
        print(f"   {rank+1}. {doc.title} (score: {score:.3f})")
        print(f"      Snippet: {snippet}")
        print(f"      Highlighted: {highlighted_content}")
        print()


if __name__ == "__main__":
    """Run all demonstrations."""
    demo_document_class()
    print("\n" + "="*60 + "\n")
    demo_search_query_class()
    print("\n" + "="*60 + "\n")
    demo_integration()
