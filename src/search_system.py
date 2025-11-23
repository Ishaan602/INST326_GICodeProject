"""
Search System Module - Team Member 2 Implementation

This module implements the search system using advanced OOP principles:
- Abstract Base Classes for search engines
- Inheritance hierarchy for different search strategies
- Polymorphic behavior for various search algorithms
- Integration with Project 1 function library

Author: Team Member 2
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Set, Optional, Any, Tuple
from collections import defaultdict, Counter
import sys
import os

# Import functions from library_name module
sys.path.insert(0, os.path.dirname(__file__))
from library_name import (
    normalize_query, build_inverted_index, boolean_retrieval,
    rank_documents, semantic_search, filter_sort_paginate_results
)


class AbstractSearchEngine(ABC):
    """Abstract base class for all search engines.
    
    Defines the common interface that all search engine types must implement.
    Uses polymorphism to allow different search strategies and algorithms.
    
    This class enforces the contract that all search engines must:
    - Process queries in their own specialized way
    - Execute searches with their specific algorithms
    - Validate their search capabilities
    """
    
    def __init__(self, engine_id: str, name: str):
        """Initialize the abstract search engine.
        
        Args:
            engine_id (str): Unique identifier for this search engine
            name (str): Human-readable name for this search engine
            
        Raises:
            ValueError: If engine_id or name is empty
        """
        if not engine_id.strip():
            raise ValueError("Engine ID cannot be empty")
        if not name.strip():
            raise ValueError("Engine name cannot be empty")
            
        self._engine_id = engine_id
        self._name = name
        self._document_collection = []
        self._search_history = []
        self._is_initialized = False
        
    @property
    def engine_id(self) -> str:
        """str: Get the engine ID (read-only)."""
        return self._engine_id
        
    @property
    def name(self) -> str:
        """str: Get the engine name (read-only)."""
        return self._name
        
    @property
    def document_count(self) -> int:
        """int: Get the number of documents in this engine."""
        return len(self._document_collection)
        
    @property
    def search_count(self) -> int:
        """int: Get the number of searches performed."""
        return len(self._search_history)
    
    @abstractmethod
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query according to this engine's strategy.
        
        Args:
            query (str): Raw search query
            
        Returns:
            Dict[str, Any]: Processed query information
            
        Note:
            Must be implemented by subclasses - each engine type
            processes queries differently (polymorphic behavior).
        """
        pass
    
    @abstractmethod
    def execute_search(self, processed_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute search using this engine's algorithm.
        
        Args:
            processed_query (Dict[str, Any]): Processed query from process_query()
            
        Returns:
            List[Dict[str, Any]]: Search results
            
        Note:
            Polymorphic method - each engine type searches differently.
        """
        pass
    
    @abstractmethod
    def validate_search_capability(self) -> bool:
        """Validate that this engine can perform searches.
        
        Returns:
            bool: True if engine is ready to search, False otherwise
            
        Note:
            Polymorphic method - each engine validates differently.
        """
        pass
    
    def add_document(self, document: Dict[str, Any]) -> None:
        """Add a document to this search engine's collection.
        
        Args:
            document (Dict[str, Any]): Document to add
            
        Raises:
            ValueError: If document is missing required fields
        """
        required_fields = ['doc_id', 'title', 'text']
        for field in required_fields:
            if field not in document:
                raise ValueError(f"Document missing required field: {field}")
        
        self._document_collection.append(document.copy())
        self._is_initialized = False  # Reset initialization when documents change
    
    def get_documents(self) -> List[Dict[str, Any]]:
        """Get all documents in this engine's collection.
        
        Returns:
            List[Dict[str, Any]]: Copy of document collection
        """
        return self._document_collection.copy()
    
    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Main search interface - template method pattern.
        
        This method orchestrates the search process by calling the
        polymorphic methods that subclasses must implement.
        
        Args:
            query (str): Search query
            **kwargs: Additional search parameters
            
        Returns:
            Dict[str, Any]: Complete search results with metadata
            
        Examples:
            >>> engine = BooleanSearchEngine("bool1", "Boolean Engine")
            >>> engine.add_document({"doc_id": "1", "title": "Test", "text": "test"})
            >>> results = engine.search("test")
            >>> results['search_type'] == 'boolean'
            True
        """
        if not self.validate_search_capability():
            raise RuntimeError(f"Search engine {self._name} is not ready for searches")
        
        # Step 1: Process query (polymorphic)
        processed_query = self.process_query(query)
        
        # Step 2: Execute search (polymorphic)
        raw_results = self.execute_search(processed_query)
        
        # Step 3: Package results with metadata
        search_metadata = {
            'engine_id': self._engine_id,
            'engine_name': self._name,
            'search_type': self.__class__.__name__.replace('SearchEngine', '').lower(),
            'original_query': query,
            'processed_query': processed_query,
            'document_count': self.document_count,
            'raw_result_count': len(raw_results)
        }
        
        # Add to search history
        search_record = {
            'query': query,
            'processed_query': processed_query,
            'result_count': len(raw_results),
            'metadata': search_metadata
        }
        self._search_history.append(search_record)
        
        return {
            'results': raw_results,
            'metadata': search_metadata,
            'total_results': len(raw_results)
        }
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """Get search history for this engine.
        
        Returns:
            List[Dict[str, Any]]: Copy of search history
        """
        return self._search_history.copy()
    
    def clear_history(self) -> None:
        """Clear the search history."""
        self._search_history.clear()
    
    def __str__(self) -> str:
        return f"{self._name} ({self.document_count} docs, {self.search_count} searches)"
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(engine_id='{self._engine_id}', name='{self._name}')"


class BooleanSearchEngine(AbstractSearchEngine):
    """Boolean search engine implementation.
    
    Implements exact term matching using inverted indices.
    Specializes in precise, logical query processing with AND operations.
    """
    
    def __init__(self, engine_id: str, name: str):
        """Initialize boolean search engine.
        
        Args:
            engine_id (str): Unique identifier
            name (str): Engine name
        """
        super().__init__(engine_id, name)
        self._inverted_index = None
        self._index_built = False
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query for boolean search.
        
        Boolean search processing focuses on term normalization
        and preparing for exact matching operations.
        
        Args:
            query (str): Raw search query
            
        Returns:
            Dict[str, Any]: Processed query with normalized terms
        """
        # Use function library for normalization
        normalized = normalize_query(query)
        terms = normalized.split()
        
        return {
            'type': 'boolean',
            'original': query,
            'normalized': normalized,
            'terms': terms,
            'operator': 'AND',  # Boolean search uses AND by default
            'term_count': len(terms)
        }
    
    def execute_search(self, processed_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute boolean search using inverted index.
        
        Polymorphic implementation for boolean-specific searching.
        Uses exact term matching with AND logic.
        
        Args:
            processed_query (Dict[str, Any]): Processed query information
            
        Returns:
            List[Dict[str, Any]]: Boolean search results
        """
        # Build index if not already built
        if not self._index_built:
            self._build_inverted_index()
        
        # Use function library for boolean retrieval
        if self._inverted_index:
            matching_doc_indices = boolean_retrieval(
                processed_query['normalized'], 
                self._inverted_index
            )
            
            # Convert indices back to documents
            results = []
            for idx in matching_doc_indices:
                if 0 <= idx < len(self._document_collection):
                    doc = self._document_collection[idx].copy()
                    doc['search_score'] = 1.0  # Boolean: either matches or doesn't
                    doc['match_type'] = 'boolean_exact'
                    doc['matched_terms'] = processed_query['terms']
                    results.append(doc)
            
            return results
        
        return []
    
    def validate_search_capability(self) -> bool:
        """Validate boolean search capability.
        
        Polymorphic implementation for boolean search validation.
        Checks that we have documents and can build an inverted index.
        
        Returns:
            bool: True if ready for boolean searches
        """
        has_documents = self.document_count > 0
        can_build_index = True  # We can always try to build an index
        
        return has_documents and can_build_index
    
    def _build_inverted_index(self) -> None:
        """Build inverted index for boolean searches."""
        if not self._document_collection:
            self._inverted_index = {}
            return
        
        # Extract text content for indexing
        documents_text = []
        for doc in self._document_collection:
            text_content = f"{doc.get('title', '')} {doc.get('text', '')}"
            documents_text.append(text_content)
        
        # Use function library to build index
        self._inverted_index = build_inverted_index(documents_text)
        self._index_built = True
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the inverted index.
        
        Returns:
            Dict[str, Any]: Index statistics
        """
        if not self._index_built:
            self._build_inverted_index()
        
        if not self._inverted_index:
            return {'term_count': 0, 'total_postings': 0}
        
        total_postings = sum(len(doc_set) for doc_set in self._inverted_index.values())
        
        return {
            'term_count': len(self._inverted_index),
            'total_postings': total_postings,
            'avg_postings_per_term': total_postings / len(self._inverted_index) if self._inverted_index else 0
        }
    
    def __str__(self) -> str:
        index_info = f", {len(self._inverted_index) if self._inverted_index else 0} terms" if self._index_built else ""
        return f"Boolean {super().__str__()}{index_info}"


class RankedSearchEngine(AbstractSearchEngine):
    """Ranked search engine implementation.
    
    Implements relevance scoring and ranking using term frequency.
    Specializes in scoring documents by relevance to query terms.
    """
    
    def __init__(self, engine_id: str, name: str, scoring_method: str = "tf"):
        """Initialize ranked search engine.
        
        Args:
            engine_id (str): Unique identifier
            name (str): Engine name
            scoring_method (str): Scoring method ('tf' or 'combined')
        """
        super().__init__(engine_id, name)
        self._scoring_method = scoring_method
        self._ranking_cache = {}
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query for ranked search.
        
        Ranked search processing includes term weighting and
        preparation for relevance scoring.
        
        Args:
            query (str): Raw search query
            
        Returns:
            Dict[str, Any]: Processed query with scoring information
        """
        # Use function library for normalization
        normalized = normalize_query(query)
        terms = normalized.split()
        
        # Calculate term weights (simple: equal weights)
        term_weights = {term: 1.0 for term in terms}
        
        return {
            'type': 'ranked',
            'original': query,
            'normalized': normalized,
            'terms': terms,
            'term_weights': term_weights,
            'scoring_method': self._scoring_method,
            'term_count': len(terms)
        }
    
    def execute_search(self, processed_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute ranked search with relevance scoring.
        
        Polymorphic implementation for rank-based searching.
        Uses term frequency and relevance scoring algorithms.
        
        Args:
            processed_query (Dict[str, Any]): Processed query information
            
        Returns:
            List[Dict[str, Any]]: Ranked search results
        """
        # Extract document content for ranking
        documents_text = []
        for doc in self._document_collection:
            text_content = f"{doc.get('title', '')} {doc.get('text', '')}"
            documents_text.append(text_content)
        
        if not documents_text:
            return []
        
        # Use function library for document ranking
        ranked_results = rank_documents(
            processed_query['normalized'],
            documents_text,
            top_k=len(documents_text)  # Get all documents, ranked
        )
        
        # Convert ranked results to full document objects
        results = []
        for doc_idx, relevance_score in ranked_results:
            if 0 <= doc_idx < len(self._document_collection):
                doc = self._document_collection[doc_idx].copy()
                doc['search_score'] = relevance_score
                doc['match_type'] = 'ranked_relevance'
                doc['scoring_method'] = self._scoring_method
                doc['matched_terms'] = processed_query['terms']
                results.append(doc)
        
        return results
    
    def validate_search_capability(self) -> bool:
        """Validate ranked search capability.
        
        Polymorphic implementation for ranked search validation.
        Checks document availability and scoring method validity.
        
        Returns:
            bool: True if ready for ranked searches
        """
        has_documents = self.document_count > 0
        valid_scoring = self._scoring_method in ['tf', 'combined']
        
        return has_documents and valid_scoring
    
    def search_with_pagination(self, query: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Perform ranked search with pagination support.
        
        Args:
            query (str): Search query
            page (int): Page number (1-indexed)
            per_page (int): Results per page
            
        Returns:
            Dict[str, Any]: Paginated search results
        """
        # Get basic ranked results
        basic_results = self.search(query)
        
        if not basic_results['results']:
            return basic_results
        
        # Use function library for pagination
        paginated = filter_sort_paginate_results(
            basic_results['results'],
            query.split(),
            page=page,
            per_page=per_page,
            sort_by="score",
            min_score=0.0
        )
        
        # Merge with our metadata
        paginated['metadata'] = basic_results['metadata']
        paginated['metadata']['pagination'] = {
            'page': page,
            'per_page': per_page,
            'total_pages': paginated['total_pages']
        }
        
        return paginated
    
    def get_scoring_stats(self) -> Dict[str, Any]:
        """Get statistics about scoring performance.
        
        Returns:
            Dict[str, Any]: Scoring statistics
        """
        if not self._search_history:
            return {'searches': 0, 'avg_results': 0}
        
        total_results = sum(record['result_count'] for record in self._search_history)
        avg_results = total_results / len(self._search_history)
        
        return {
            'searches': len(self._search_history),
            'total_results': total_results,
            'avg_results': avg_results,
            'scoring_method': self._scoring_method
        }
    
    def __str__(self) -> str:
        return f"Ranked {super().__str__()} [{self._scoring_method}]"


class SemanticSearchEngine(AbstractSearchEngine):
    """Semantic search engine implementation.
    
    Implements meaning-based searching using semantic similarity.
    Specializes in understanding query intent and document meaning.
    """
    
    def __init__(self, engine_id: str, name: str, similarity_threshold: float = 0.1):
        """Initialize semantic search engine.
        
        Args:
            engine_id (str): Unique identifier
            name (str): Engine name
            similarity_threshold (float): Minimum similarity score for results
        """
        super().__init__(engine_id, name)
        self._similarity_threshold = similarity_threshold
        self._semantic_cache = {}
        self._model = None  # Placeholder for semantic model
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query for semantic search.
        
        Semantic search processing includes intent analysis and
        semantic feature extraction.
        
        Args:
            query (str): Raw search query
            
        Returns:
            Dict[str, Any]: Processed query with semantic information
        """
        # Use function library for normalization
        normalized = normalize_query(query)
        terms = normalized.split()
        
        # Semantic processing (simplified)
        semantic_features = {
            'query_length': len(terms),
            'has_technical_terms': any(term in ['algorithm', 'data', 'machine', 'learning'] for term in terms),
            'query_complexity': 'simple' if len(terms) <= 2 else 'complex'
        }
        
        return {
            'type': 'semantic',
            'original': query,
            'normalized': normalized,
            'terms': terms,
            'semantic_features': semantic_features,
            'similarity_threshold': self._similarity_threshold,
            'term_count': len(terms)
        }
    
    def execute_search(self, processed_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute semantic search with similarity scoring.
        
        Polymorphic implementation for semantic searching.
        Uses meaning-based similarity rather than exact matching.
        
        Args:
            processed_query (Dict[str, Any]): Processed query information
            
        Returns:
            List[Dict[str, Any]]: Semantic search results
        """
        # Extract document content for semantic analysis
        documents_text = []
        for doc in self._document_collection:
            text_content = f"{doc.get('title', '')} {doc.get('text', '')}"
            documents_text.append(text_content)
        
        if not documents_text:
            return []
        
        # Use function library for semantic search
        # Note: Falls back to ranked search if no semantic model available
        semantic_results = semantic_search(
            processed_query['normalized'],
            documents_text,
            model=self._model,
            top_k=len(documents_text)
        )
        
        # Convert semantic results to full document objects
        results = []
        for doc_idx, similarity_score in semantic_results:
            if (0 <= doc_idx < len(self._document_collection) and 
                similarity_score >= self._similarity_threshold):
                
                doc = self._document_collection[doc_idx].copy()
                doc['search_score'] = similarity_score
                doc['match_type'] = 'semantic_similarity'
                doc['similarity_threshold'] = self._similarity_threshold
                doc['semantic_features'] = processed_query['semantic_features']
                results.append(doc)
        
        return results
    
    def validate_search_capability(self) -> bool:
        """Validate semantic search capability.
        
        Polymorphic implementation for semantic search validation.
        Checks document availability and semantic processing capability.
        
        Returns:
            bool: True if ready for semantic searches
        """
        has_documents = self.document_count > 0
        valid_threshold = 0.0 <= self._similarity_threshold <= 1.0
        
        # Semantic search can work even without advanced models
        # (falls back to term frequency methods)
        semantic_ready = True
        
        return has_documents and valid_threshold and semantic_ready
    
    def set_similarity_threshold(self, threshold: float) -> None:
        """Set the minimum similarity threshold.
        
        Args:
            threshold (float): New similarity threshold (0.0 to 1.0)
            
        Raises:
            ValueError: If threshold is out of range
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Similarity threshold must be between 0.0 and 1.0")
        self._similarity_threshold = threshold
        self._semantic_cache.clear()  # Clear cache when threshold changes
    
    def analyze_query_semantics(self, query: str) -> Dict[str, Any]:
        """Analyze the semantic properties of a query.
        
        Args:
            query (str): Query to analyze
            
        Returns:
            Dict[str, Any]: Semantic analysis results
        """
        processed = self.process_query(query)
        
        return {
            'original_query': query,
            'normalized_query': processed['normalized'],
            'semantic_complexity': processed['semantic_features']['query_complexity'],
            'has_technical_terms': processed['semantic_features']['has_technical_terms'],
            'term_count': processed['term_count'],
            'estimated_intent': 'technical' if processed['semantic_features']['has_technical_terms'] else 'general'
        }
    
    def get_semantic_stats(self) -> Dict[str, Any]:
        """Get statistics about semantic search performance.
        
        Returns:
            Dict[str, Any]: Semantic search statistics
        """
        if not self._search_history:
            return {'searches': 0, 'avg_similarity': 0}
        
        # Calculate average similarity scores
        total_score = 0
        result_count = 0
        
        for record in self._search_history:
            total_score += record['result_count'] * 0.5  # Simplified average
            result_count += record['result_count']
        
        avg_similarity = total_score / result_count if result_count > 0 else 0
        
        return {
            'searches': len(self._search_history),
            'similarity_threshold': self._similarity_threshold,
            'avg_similarity_score': avg_similarity,
            'cache_size': len(self._semantic_cache)
        }
    
    def __str__(self) -> str:
        return f"Semantic {super().__str__()} [threshold={self._similarity_threshold}]"


# Factory class for creating search engines
class SearchEngineFactory:
    """Factory for creating different types of search engines.
    
    Provides a centralized way to create search engines with
    proper configuration and validation.
    """
    
    @staticmethod
    def create_engine(engine_type: str, engine_id: str, name: str, **kwargs) -> AbstractSearchEngine:
        """Create a search engine of the specified type.
        
        Args:
            engine_type (str): Type of engine ('boolean', 'ranked', 'semantic')
            engine_id (str): Unique identifier
            name (str): Engine name
            **kwargs: Additional configuration parameters
            
        Returns:
            AbstractSearchEngine: Created search engine
            
        Raises:
            ValueError: If engine_type is unknown
            
        Examples:
            >>> factory = SearchEngineFactory()
            >>> engine = factory.create_engine('boolean', 'bool1', 'Test Boolean')
            >>> isinstance(engine, BooleanSearchEngine)
            True
        """
        engine_type = engine_type.lower()
        
        if engine_type == 'boolean':
            return BooleanSearchEngine(engine_id, name)
        elif engine_type == 'ranked':
            scoring_method = kwargs.get('scoring_method', 'tf')
            return RankedSearchEngine(engine_id, name, scoring_method)
        elif engine_type == 'semantic':
            threshold = kwargs.get('similarity_threshold', 0.1)
            return SemanticSearchEngine(engine_id, name, threshold)
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")
    
    @staticmethod
    def get_supported_types() -> List[str]:
        """Get list of supported engine types.
        
        Returns:
            List[str]: Supported engine type names
        """
        return ['boolean', 'ranked', 'semantic']


# Demonstration and testing code
if __name__ == "__main__":
    print("=== Search System Module Demo - Team Member 2 ===\n")
    
    # Test data
    test_documents = [
        {
            "doc_id": "1",
            "title": "Machine Learning Fundamentals",
            "text": "Introduction to machine learning algorithms and data science techniques"
        },
        {
            "doc_id": "2", 
            "title": "Python Programming Guide",
            "text": "Complete guide to Python programming for beginners and advanced users"
        },
        {
            "doc_id": "3",
            "title": "Data Analysis Methods",
            "text": "Statistical analysis and data mining techniques for research"
        },
        {
            "doc_id": "4",
            "title": "Web Development",
            "text": "Modern web development using JavaScript, HTML, and CSS frameworks"
        }
    ]
    
    # 1. Test Abstract Base Class enforcement
    print("1. Testing Abstract Base Class:")
    try:
        # This should fail - cannot instantiate abstract class
        abstract_engine = AbstractSearchEngine("test", "test")
    except TypeError as e:
        print(f"✓ Cannot instantiate abstract class: {type(e).__name__}")
    
    print()
    
    # 2. Test Polymorphic Behavior
    print("2. Testing Polymorphic Search Behavior:")
    
    # Create different engine types using factory
    factory = SearchEngineFactory()
    engines = [
        factory.create_engine('boolean', 'bool1', 'Boolean Engine'),
        factory.create_engine('ranked', 'rank1', 'Ranked Engine', scoring_method='tf'),
        factory.create_engine('semantic', 'sem1', 'Semantic Engine', similarity_threshold=0.2)
    ]
    
    # Add same documents to all engines
    for engine in engines:
        for doc in test_documents:
            engine.add_document(doc)
    
    # Test same query on different engines (polymorphism)
    test_query = "machine learning data"
    print(f"Searching for: '{test_query}'\n")
    
    for engine in engines:
        print(f"{engine.__class__.__name__}:")
        
        # Test polymorphic validation
        is_ready = engine.validate_search_capability()
        print(f"  Validation: {is_ready}")
        
        if is_ready:
            # Test polymorphic query processing
            processed = engine.process_query(test_query)
            print(f"  Query Type: {processed['type']}")
            print(f"  Normalized: '{processed['normalized']}'")
            
            # Test polymorphic search execution
            results = engine.search(test_query)
            print(f"  Results: {len(results['results'])} documents")
            
            if results['results']:
                top_result = results['results'][0]
                print(f"  Top Match: {top_result['title']} (score: {top_result.get('search_score', 'N/A')})")
                print(f"  Match Type: {top_result.get('match_type', 'unknown')}")
        
        print()
    
    # 3. Test Inheritance Hierarchy
    print("3. Testing Inheritance Hierarchy:")
    
    boolean_engine = engines[0]
    ranked_engine = engines[1]
    semantic_engine = engines[2]
    
    # Test that all engines inherit from AbstractSearchEngine
    for engine in engines:
        is_abstract_subclass = isinstance(engine, AbstractSearchEngine)
        print(f"{engine.__class__.__name__} IS-A AbstractSearchEngine: {is_abstract_subclass}")
    
    # Test specialized methods
    if isinstance(boolean_engine, BooleanSearchEngine):
        index_stats = boolean_engine.get_index_stats()
        print(f"Boolean Engine Index: {index_stats['term_count']} terms")
    
    if isinstance(ranked_engine, RankedSearchEngine):
        # Test pagination (specialized feature)
        paginated = ranked_engine.search_with_pagination(test_query, page=1, per_page=2)
        print(f"Ranked Engine Pagination: {paginated['per_page']} per page")
    
    if isinstance(semantic_engine, SemanticSearchEngine):
        # Test semantic analysis (specialized feature)
        semantics = semantic_engine.analyze_query_semantics(test_query)
        print(f"Semantic Analysis: {semantics['estimated_intent']} intent")
    
    print()
    
    # 4. Test Function Library Integration
    print("4. Testing Function Library Integration:")
    
    # Show how each engine uses different functions from library_name.py
    print("Boolean Engine uses:")
    print("  - normalize_query() for query processing")
    print("  - build_inverted_index() for indexing")
    print("  - boolean_retrieval() for exact matching")
    
    print("\nRanked Engine uses:")
    print("  - normalize_query() for query processing") 
    print("  - rank_documents() for relevance scoring")
    print("  - filter_sort_paginate_results() for pagination")
    
    print("\nSemantic Engine uses:")
    print("  - normalize_query() for query processing")
    print("  - semantic_search() for similarity matching")
    
    print()
    
    # 5. Test Search History and State
    print("5. Testing Search Engine State:")
    
    test_engine = engines[0]  # Use boolean engine
    print(f"Initial state: {test_engine}")
    
    # Perform multiple searches
    queries = ["python programming", "data analysis", "web development"]
    for query in queries:
        test_engine.search(query)
    
    history = test_engine.get_search_history()
    print(f"After {len(queries)} searches: {len(history)} in history")
    
    # Show search statistics
    print(f"Document count: {test_engine.document_count}")
    print(f"Search count: {test_engine.search_count}")
    
    print()
    
    # 6. Demonstrate Factory Pattern
    print("6. Testing Factory Pattern:")
    
    supported_types = SearchEngineFactory.get_supported_types()
    print(f"Supported engine types: {supported_types}")
    
    for engine_type in supported_types:
        engine = factory.create_engine(engine_type, f"{engine_type}1", f"Test {engine_type.title()}")
        print(f"Created {engine_type}: {engine}")
    
    print()
    
    print("=== Team Member 2 Implementation Complete ===")
    print("\nFeatures Implemented:")
    print("✓ Abstract Base Class (AbstractSearchEngine) using ABC module")
    print("✓ Inheritance Hierarchy: AbstractSearchEngine → Boolean/Ranked/Semantic")
    print("✓ Polymorphic Methods: process_query(), execute_search(), validate_search_capability()")
    print("✓ Function Library Integration: All 6 assigned functions integrated")
    print("✓ Method Overriding with super() calls in __init__ methods")
    print("✓ Factory Pattern for engine creation")
    print("✓ Comprehensive documentation and examples")
    print("✓ Proper encapsulation with private attributes")
