# Completed by Ishaan Patel
"""
SearchQuery Class Module

This module contains the SearchQuery class for representing and managing search
queries in an information retrieval system. The class encapsulates query processing
and provides methods for normalization, boolean retrieval, and semantic search.
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, Counter
import re


class SearchQuery:
    """Represents a search query in an information retrieval system.
    
    This class encapsulates search query data and provides methods for query
    processing, normalization, boolean retrieval, and semantic search operations.
    It maintains query history and provides various search capabilities.
    
    Attributes:
        _original_query (str): The original, unprocessed query string
        _normalized_query (str): The normalized version of the query
        _query_terms (List[str]): List of individual query terms
        _search_history (List[str]): History of previous queries
    
    Examples:
        >>> query = SearchQuery("  Data MINING  techniques  ")
        >>> query.normalized_query
        'data mining techniques'
        >>> query.query_terms
        ['data', 'mining', 'techniques']
    """
    
    def __init__(self, query: str):
        """Initialize a SearchQuery instance.
        
        Args:
            query (str): The search query string to process
            
        Raises:
            TypeError: If query is not a string
            ValueError: If query is empty after normalization
            
        Examples:
            >>> query = SearchQuery("machine learning")
            >>> query.original_query
            'machine learning'
            >>> query = SearchQuery("  AI   techniques  ")
            >>> query.normalized_query
            'ai techniques'
        """
        # Parameter validation
        if not isinstance(query, str):
            raise TypeError("query must be a string")
            
        # Store original query
        self._original_query = query
        
        # Normalize the query
        self._normalized_query = self._normalize_query_string(query)
        
        if not self._normalized_query:
            raise ValueError("query cannot be empty after normalization")
            
        # Extract query terms
        self._query_terms = self._normalized_query.split()
        
        # Initialize search history
        self._search_history = [self._normalized_query]
    
    @property
    def original_query(self) -> str:
        """Get the original query string.
        
        Returns:
            str: Original, unprocessed query string
        """
        return self._original_query
    
    @property
    def normalized_query(self) -> str:
        """Get the normalized query string.
        
        Returns:
            str: Normalized query string in lowercase with standardized spacing
        """
        return self._normalized_query
    
    @property
    def query_terms(self) -> List[str]:
        """Get the individual query terms.
        
        Returns:
            List[str]: List of normalized query terms
        """
        return self._query_terms.copy()  # Return copy to prevent external modification
    
    @property
    def search_history(self) -> List[str]:
        """Get the search history.
        
        Returns:
            List[str]: List of previous normalized queries
        """
        return self._search_history.copy()  # Return copy to prevent external modification
    
    def _normalize_query_string(self, query: str) -> str:
        """Normalize a search query by standardizing case and whitespace.
        
        Integrates the normalize_query() function to convert the query to lowercase,
        remove leading/trailing whitespace, and collapse multiple spaces.
        
        Args:
            query (str): The search query string to normalize
            
        Returns:
            str: Normalized query string in lowercase with standardized spacing
        """
        # Convert to lowercase and strip leading/trailing whitespace
        normalized = query.lower().strip()
        
        # Replace multiple consecutive spaces with single space
        while '  ' in normalized:  # Keep replacing double spaces until none left
            normalized = normalized.replace('  ', ' ')
        
        return normalized
    
    def update_query(self, new_query: str) -> None:
        """Update the search query with a new query string.
        
        Args:
            new_query (str): New query string to process
            
        Raises:
            TypeError: If new_query is not a string
            ValueError: If new_query is empty after normalization
            
        Examples:
            >>> query = SearchQuery("old query")
            >>> query.update_query("new search terms")
            >>> query.normalized_query
            'new search terms'
        """
        if not isinstance(new_query, str):
            raise TypeError("new_query must be a string")
            
        # Store original query
        self._original_query = new_query
        
        # Normalize the new query
        self._normalized_query = self._normalize_query_string(new_query)
        
        if not self._normalized_query:
            raise ValueError("new_query cannot be empty after normalization")
            
        # Update query terms
        self._query_terms = self._normalized_query.split()
        
        # Add to search history
        if self._normalized_query not in self._search_history:
            self._search_history.append(self._normalized_query)
    
    def build_inverted_index(self, documents: List[str]) -> Dict[str, Set[int]]:
        """Build an inverted index mapping terms to document IDs.
        
        Creates a mapping from each unique term to the set of document IDs
        that contain that term, enabling efficient boolean retrieval.
        
        Args:
            documents (List[str]): List of documents to index
            
        Returns:
            Dict[str, Set[int]]: Dictionary mapping each term to set of document IDs
            
        Examples:
            >>> query = SearchQuery("test")
            >>> docs = ["cat dog", "dog bird", "cat bird"]
            >>> index = query.build_inverted_index(docs)
            >>> index['cat']
            {0, 2}
            >>> index['dog']
            {0, 1}
        """
        index = defaultdict(set)
        for doc_id, text in enumerate(documents):
            tokens = self._normalize_query_string(text).split()
            for token in set(tokens):
                index[token].add(doc_id)
        return dict(index)
    
    def boolean_search(self, documents: List[str]) -> Set[int]:
        """Perform boolean AND retrieval on a list of documents.
        
        Integrates the boolean_retrieval() function to find documents that
        contain ALL query terms using an inverted index approach.
        
        Args:
            documents (List[str]): List of documents to search through
            
        Returns:
            Set[int]: Set of document IDs that contain ALL query terms
            
        Examples:
            >>> query = SearchQuery("cat dog")
            >>> docs = ["cat dog bird", "dog mouse", "cat bird"]
            >>> results = query.boolean_search(docs)
            >>> 0 in results  # First document contains both "cat" and "dog"
            True
        """
        # Build inverted index
        inverted_index = self.build_inverted_index(documents)
        
        # Perform boolean AND retrieval
        if not self._query_terms:
            return set()
        
        result = inverted_index.get(self._query_terms[0], set())
        for term in self._query_terms[1:]:
            result = result.intersection(inverted_index.get(term, set()))
        return result
    
    def rank_documents(self, documents: List[str], top_k: int = 5) -> List[Tuple[int, float]]:
        """Rank documents based on term frequency similarity to query.
        
        Calculates relevance scores based on term frequency overlap between
        the query and documents, normalized by document length.
        
        Args:
            documents (List[str]): List of documents to rank
            top_k (int, optional): Number of top results to return. Defaults to 5.
            
        Returns:
            List[Tuple[int, float]]: List of (doc_index, score) tuples sorted by relevance
            
        Examples:
            >>> query = SearchQuery("data mining")
            >>> docs = ["data mining algorithms", "machine learning", "database systems"]
            >>> results = query.rank_documents(docs, top_k=2)
            >>> results[0][1] > results[1][1]  # First result has higher score
            True
        """
        query_tokens = set(self._query_terms)
        scores = []
        
        for doc_id, document in enumerate(documents):
            doc_tokens = self._normalize_query_string(document).split()
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
    
    def semantic_search(self, documents: List[str], model=None, top_k: int = 5) -> List[Tuple[int, float]]:
        """Perform semantic search on documents.
        
        Integrates the semantic_search() function to find semantically similar
        documents. Falls back to term frequency ranking if no model is provided.
        
        Args:
            documents (List[str]): List of documents to search
            model: Optional semantic model (not implemented)
            top_k (int, optional): Number of top results to return. Defaults to 5.
            
        Returns:
            List[Tuple[int, float]]: List of (doc_index, score) tuples sorted by relevance
            
        Examples:
            >>> query = SearchQuery("AI techniques")
            >>> docs = ["machine learning algorithms", "data science methods", "web development"]
            >>> results = query.semantic_search(docs, top_k=2)
            >>> len(results) <= 2
            True
        """
        if model is None:
            # If no model is provided, fall back to term frequency ranking
            return self.rank_documents(documents, top_k)
        
        # If a model is provided but we can't use advanced libraries, fall back to term frequency
        # In a real implementation, this would use sentence transformers or similar
        print("Warning: No semantic model implementation available, using term frequency ranking")
        return self.rank_documents(documents, top_k)
    
    def get_query_statistics(self) -> Dict[str, int]:
        """Get statistics about the current query.
        
        Returns:
            Dict[str, int]: Dictionary containing query statistics
            
        Examples:
            >>> query = SearchQuery("machine learning algorithms")
            >>> stats = query.get_query_statistics()
            >>> stats['term_count']
            3
            >>> stats['character_count']
            26
        """
        return {
            'term_count': len(self._query_terms),
            'character_count': len(self._normalized_query),
            'original_length': len(self._original_query),
            'search_history_count': len(self._search_history)
        }
    
    def contains_term(self, term: str) -> bool:
        """Check if the query contains a specific term.
        
        Args:
            term (str): Term to search for in the query
            
        Returns:
            bool: True if the term is found in the query, False otherwise
            
        Examples:
            >>> query = SearchQuery("machine learning algorithms")
            >>> query.contains_term("learning")
            True
            >>> query.contains_term("database")
            False
        """
        return term.lower() in self._query_terms
    
    def get_similar_queries(self, other_queries: List[str], threshold: float = 0.3) -> List[str]:
        """Find similar queries based on term overlap.
        
        Args:
            other_queries (List[str]): List of other queries to compare against
            threshold (float, optional): Minimum similarity threshold. Defaults to 0.3.
            
        Returns:
            List[str]: List of similar queries above the threshold
            
        Examples:
            >>> query = SearchQuery("machine learning")
            >>> others = ["deep learning", "machine vision", "web development"]
            >>> similar = query.get_similar_queries(others, threshold=0.3)
            >>> "deep learning" in similar
            True
        """
        similar_queries = []
        query_terms_set = set(self._query_terms)
        
        for other_query in other_queries:
            other_normalized = self._normalize_query_string(other_query)
            other_terms_set = set(other_normalized.split())
            
            # Calculate Jaccard similarity
            if query_terms_set and other_terms_set:
                intersection = len(query_terms_set.intersection(other_terms_set))
                union = len(query_terms_set.union(other_terms_set))
                similarity = intersection / union if union > 0 else 0.0
                
                if similarity >= threshold:
                    similar_queries.append(other_query)
        
        return similar_queries
    
    def __str__(self) -> str:
        """Return a human-readable string representation of the search query.
        
        Returns:
            str: Formatted string showing normalized query and term count
            
        Examples:
            >>> query = SearchQuery("  Machine   Learning  ")
            >>> str(query)
            'SearchQuery: "machine learning" (2 terms)'
        """
        term_count = len(self._query_terms)
        return f'SearchQuery: "{self._normalized_query}" ({term_count} term{"s" if term_count != 1 else ""})'
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging.
        
        Returns:
            str: Detailed representation with key attributes
            
        Examples:
            >>> query = SearchQuery("test query")
            >>> repr(query)
            'SearchQuery(original="test query", normalized="test query", terms=2)'
        """
        return f'SearchQuery(original="{self._original_query}", normalized="{self._normalized_query}", terms={len(self._query_terms)})'
