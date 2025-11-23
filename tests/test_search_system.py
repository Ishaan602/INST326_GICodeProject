"""
Test Suite for Search System Module - Team Member 2

Comprehensive tests for inheritance, polymorphism, abstract classes,
and function library integration.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search_system import (
    AbstractSearchEngine, BooleanSearchEngine, RankedSearchEngine,
    SemanticSearchEngine, SearchEngineFactory
)


class TestAbstractBaseClass(unittest.TestCase):
    """Test abstract base class enforcement and interface contracts."""
    
    def test_cannot_instantiate_abstract_search_engine(self):
        """Test that AbstractSearchEngine cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            AbstractSearchEngine("test", "Test Engine")
    
    def test_abstract_methods_required(self):
        """Test that subclasses must implement all abstract methods."""
        
        class IncompleteSearchEngine(AbstractSearchEngine):
            # Missing required abstract methods
            def process_query(self, query):
                pass
            # Missing execute_search and validate_search_capability
        
        with self.assertRaises(TypeError):
            IncompleteSearchEngine("incomplete", "Incomplete Engine")
    
    def test_complete_implementation_works(self):
        """Test that complete implementations can be instantiated."""
        
        class CompleteSearchEngine(AbstractSearchEngine):
            def process_query(self, query):
                return {'type': 'test', 'query': query}
            
            def execute_search(self, processed_query):
                return []
            
            def validate_search_capability(self):
                return True
        
        # Should not raise an exception
        engine = CompleteSearchEngine("complete", "Complete Engine")
        self.assertIsInstance(engine, AbstractSearchEngine)


class TestInheritanceHierarchy(unittest.TestCase):
    """Test inheritance relationships and proper base class usage."""
    
    def setUp(self):
        """Set up test engines for inheritance testing."""
        self.boolean_engine = BooleanSearchEngine("bool1", "Boolean Test")
        self.ranked_engine = RankedSearchEngine("rank1", "Ranked Test")
        self.semantic_engine = SemanticSearchEngine("sem1", "Semantic Test")
        
        # Add test documents
        self.test_docs = [
            {"doc_id": "1", "title": "Python Guide", "text": "Python programming tutorial"},
            {"doc_id": "2", "title": "ML Basics", "text": "Machine learning fundamentals"},
            {"doc_id": "3", "title": "Data Science", "text": "Data analysis and statistics"}
        ]
        
        for engine in [self.boolean_engine, self.ranked_engine, self.semantic_engine]:
            for doc in self.test_docs:
                engine.add_document(doc)
    
    def test_inheritance_relationships(self):
        """Test that all engines properly inherit from AbstractSearchEngine."""
        engines = [self.boolean_engine, self.ranked_engine, self.semantic_engine]
        
        for engine in engines:
            # Test inheritance
            self.assertIsInstance(engine, AbstractSearchEngine)
            
            # Test inherited properties
            self.assertTrue(hasattr(engine, 'engine_id'))
            self.assertTrue(hasattr(engine, 'name'))
            self.assertTrue(hasattr(engine, 'document_count'))
            
            # Test inherited methods
            self.assertTrue(hasattr(engine, 'add_document'))
            self.assertTrue(hasattr(engine, 'get_documents'))
            self.assertTrue(hasattr(engine, 'search'))
    
    def test_super_calls_in_init(self):
        """Test that subclasses properly call super().__init__()."""
        # Test that base class properties are set
        self.assertEqual(self.boolean_engine.engine_id, "bool1")
        self.assertEqual(self.ranked_engine.name, "Ranked Test")
        self.assertEqual(self.semantic_engine.document_count, 3)
        
        # Test that derived class properties are also set
        self.assertTrue(hasattr(self.boolean_engine, '_index_built'))
        self.assertTrue(hasattr(self.ranked_engine, '_scoring_method'))
        self.assertTrue(hasattr(self.semantic_engine, '_similarity_threshold'))
    
    def test_method_overriding(self):
        """Test that subclasses properly override abstract methods."""
        query = "python machine learning"
        
        # Each engine should implement process_query differently
        bool_processed = self.boolean_engine.process_query(query)
        rank_processed = self.ranked_engine.process_query(query)
        sem_processed = self.semantic_engine.process_query(query)
        
        self.assertEqual(bool_processed['type'], 'boolean')
        self.assertEqual(rank_processed['type'], 'ranked')
        self.assertEqual(sem_processed['type'], 'semantic')
        
        # Test that each has specialized behavior
        self.assertIn('operator', bool_processed)  # Boolean-specific
        self.assertIn('term_weights', rank_processed)  # Ranked-specific
        self.assertIn('semantic_features', sem_processed)  # Semantic-specific


class TestPolymorphicBehavior(unittest.TestCase):
    """Test polymorphic behavior across different engine types."""
    
    def setUp(self):
        """Set up engines for polymorphism testing."""
        self.engines = [
            BooleanSearchEngine("bool1", "Boolean"),
            RankedSearchEngine("rank1", "Ranked"),
            SemanticSearchEngine("sem1", "Semantic")
        ]
        
        # Add same documents to all engines
        test_doc = {"doc_id": "1", "title": "Test Doc", "text": "test content"}
        for engine in self.engines:
            engine.add_document(test_doc)
    
    def test_polymorphic_validation(self):
        """Test that validate_search_capability() behaves polymorphically."""
        for engine in self.engines:
            # Same method call, different implementations
            is_valid = engine.validate_search_capability()
            self.assertIsInstance(is_valid, bool)
            
            # All should be valid with documents present
            self.assertTrue(is_valid)
    
    def test_polymorphic_search_execution(self):
        """Test that search execution behaves polymorphically."""
        test_query = "test"
        
        for engine in self.engines:
            # Same interface, different behavior
            results = engine.search(test_query)
            
            # All should return properly structured results
            self.assertIn('results', results)
            self.assertIn('metadata', results)
            
            # Each should have different search_type metadata
            search_type = results['metadata']['search_type']
            self.assertIn(search_type, ['boolean', 'ranked', 'semantic'])
            
            # Results should have appropriate scoring
            if results['results']:
                result = results['results'][0]
                self.assertIn('search_score', result)
                self.assertIn('match_type', result)
    
    def test_uniform_interface_usage(self):
        """Test that engines can be used uniformly despite different implementations."""
        def search_all_engines(engines, query):
            """Helper function that treats all engines uniformly."""
            results = []
            for engine in engines:
                if engine.validate_search_capability():
                    result = engine.search(query)
                    results.append(result)
            return results
        
        # Test uniform usage
        query = "test query"
        all_results = search_all_engines(self.engines, query)
        
        # Should get results from all engines
        self.assertEqual(len(all_results), 3)
        
        # Each should have consistent structure despite different implementations
        for result in all_results:
            self.assertIn('results', result)
            self.assertIn('metadata', result)
            self.assertIn('total_results', result)


class TestFunctionLibraryIntegration(unittest.TestCase):
    """Test integration with original function library."""
    
    def setUp(self):
        """Set up engines for function integration testing."""
        self.boolean_engine = BooleanSearchEngine("bool1", "Boolean Test")
        self.ranked_engine = RankedSearchEngine("rank1", "Ranked Test")
        self.semantic_engine = SemanticSearchEngine("sem1", "Semantic Test")
        
        # Add test documents
        test_docs = [
            {"doc_id": "1", "title": "Machine Learning", "text": "ML algorithms and data science"},
            {"doc_id": "2", "title": "Python Programming", "text": "Python coding and development"}
        ]
        
        for engine in [self.boolean_engine, self.ranked_engine, self.semantic_engine]:
            for doc in test_docs:
                engine.add_document(doc)
    
    @patch('search_system.normalize_query')
    def test_normalize_query_integration(self, mock_normalize):
        """Test that engines properly use normalize_query function."""
        mock_normalize.return_value = "normalized query"
        
        # Test with all engine types
        engines = [self.boolean_engine, self.ranked_engine, self.semantic_engine]
        
        for engine in engines:
            processed = engine.process_query("  MESSY   query  ")
            mock_normalize.assert_called_with("  MESSY   query  ")
            self.assertEqual(processed['normalized'], "normalized query")
    
    @patch('search_system.build_inverted_index')
    def test_boolean_index_integration(self, mock_build_index):
        """Test that BooleanSearchEngine uses build_inverted_index."""
        mock_build_index.return_value = {'test': {0, 1}}
        
        # Force index building
        self.boolean_engine._build_inverted_index()
        
        # Should have called the function library
        mock_build_index.assert_called_once()
        
        # Should store the result
        self.assertEqual(self.boolean_engine._inverted_index, {'test': {0, 1}})
    
    @patch('search_system.rank_documents')
    def test_ranked_search_integration(self, mock_rank):
        """Test that RankedSearchEngine uses rank_documents."""
        mock_rank.return_value = [(0, 0.8), (1, 0.3)]
        
        # Execute search
        processed = self.ranked_engine.process_query("test query")
        results = self.ranked_engine.execute_search(processed)
        
        # Should have called rank_documents
        mock_rank.assert_called_once()
        
        # Should process the results correctly
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['search_score'], 0.8)
    
    @patch('search_system.semantic_search')
    def test_semantic_search_integration(self, mock_semantic):
        """Test that SemanticSearchEngine uses semantic_search."""
        mock_semantic.return_value = [(0, 0.9), (1, 0.1)]
        
        # Execute search with threshold filtering
        self.semantic_engine.set_similarity_threshold(0.5)
        processed = self.semantic_engine.process_query("semantic query")
        results = self.semantic_engine.execute_search(processed)
        
        # Should have called semantic_search
        mock_semantic.assert_called_once()
        
        # Should filter by threshold (only first result above 0.5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['search_score'], 0.9)
    
    @patch('search_system.filter_sort_paginate_results')
    def test_pagination_integration(self, mock_paginate):
        """Test that RankedSearchEngine uses filter_sort_paginate_results."""
        mock_paginate.return_value = {
            'results': [{'doc_id': '1', 'title': 'Test'}],
            'page': 1,
            'per_page': 2,
            'total_results': 1,
            'total_pages': 1
        }
        
        # Test pagination
        paginated = self.ranked_engine.search_with_pagination("test", page=1, per_page=2)
        
        # Should have called the pagination function
        mock_paginate.assert_called_once()
        
        # Should include pagination metadata
        self.assertIn('pagination', paginated['metadata'])


class TestSpecializedFeatures(unittest.TestCase):
    """Test specialized features unique to each engine type."""
    
    def setUp(self):
        """Set up engines for specialized feature testing."""
        self.boolean_engine = BooleanSearchEngine("bool1", "Boolean Test")
        self.ranked_engine = RankedSearchEngine("rank1", "Ranked Test", scoring_method="tf")
        self.semantic_engine = SemanticSearchEngine("sem1", "Semantic Test", similarity_threshold=0.3)
        
        # Add test documents
        test_docs = [
            {"doc_id": "1", "title": "Python", "text": "Python programming"},
            {"doc_id": "2", "title": "Java", "text": "Java development"}
        ]
        
        for engine in [self.boolean_engine, self.ranked_engine, self.semantic_engine]:
            for doc in test_docs:
                engine.add_document(doc)
    
    def test_boolean_engine_features(self):
        """Test BooleanSearchEngine-specific features."""
        # Test index statistics
        stats = self.boolean_engine.get_index_stats()
        self.assertIn('term_count', stats)
        self.assertIn('total_postings', stats)
        
        # Test boolean-specific search behavior
        results = self.boolean_engine.search("python")
        if results['results']:
            result = results['results'][0]
            self.assertEqual(result['search_score'], 1.0)  # Boolean: exact match
            self.assertEqual(result['match_type'], 'boolean_exact')
    
    def test_ranked_engine_features(self):
        """Test RankedSearchEngine-specific features."""
        # Test scoring statistics
        self.ranked_engine.search("test query")  # Generate history
        stats = self.ranked_engine.get_scoring_stats()
        
        self.assertIn('scoring_method', stats)
        self.assertEqual(stats['scoring_method'], 'tf')
        self.assertIn('searches', stats)
        
        # Test pagination feature
        paginated = self.ranked_engine.search_with_pagination("python", page=1, per_page=1)
        self.assertEqual(paginated['per_page'], 1)
        self.assertIn('pagination', paginated['metadata'])
    
    def test_semantic_engine_features(self):
        """Test SemanticSearchEngine-specific features."""
        # Test similarity threshold setting
        self.semantic_engine.set_similarity_threshold(0.7)
        self.assertEqual(self.semantic_engine._similarity_threshold, 0.7)
        
        with self.assertRaises(ValueError):
            self.semantic_engine.set_similarity_threshold(1.5)  # Invalid threshold
        
        # Test semantic analysis
        analysis = self.semantic_engine.analyze_query_semantics("machine learning algorithms")
        self.assertIn('estimated_intent', analysis)
        self.assertIn('semantic_complexity', analysis)
        
        # Test semantic statistics
        self.semantic_engine.search("test query")  # Generate history
        stats = self.semantic_engine.get_semantic_stats()
        self.assertIn('similarity_threshold', stats)
        self.assertIn('searches', stats)


class TestFactoryPattern(unittest.TestCase):
    """Test the SearchEngineFactory pattern."""
    
    def setUp(self):
        """Set up factory for testing."""
        self.factory = SearchEngineFactory()
    
    def test_create_boolean_engine(self):
        """Test creation of boolean search engine."""
        engine = self.factory.create_engine('boolean', 'bool1', 'Test Boolean')
        
        self.assertIsInstance(engine, BooleanSearchEngine)
        self.assertEqual(engine.engine_id, 'bool1')
        self.assertEqual(engine.name, 'Test Boolean')
    
    def test_create_ranked_engine(self):
        """Test creation of ranked search engine."""
        engine = self.factory.create_engine('ranked', 'rank1', 'Test Ranked', scoring_method='combined')
        
        self.assertIsInstance(engine, RankedSearchEngine)
        self.assertEqual(engine._scoring_method, 'combined')
    
    def test_create_semantic_engine(self):
        """Test creation of semantic search engine."""
        engine = self.factory.create_engine('semantic', 'sem1', 'Test Semantic', similarity_threshold=0.5)
        
        self.assertIsInstance(engine, SemanticSearchEngine)
        self.assertEqual(engine._similarity_threshold, 0.5)
    
    def test_unknown_engine_type(self):
        """Test that unknown engine types raise ValueError."""
        with self.assertRaises(ValueError):
            self.factory.create_engine('unknown', 'test', 'Test')
    
    def test_supported_types(self):
        """Test getting supported engine types."""
        types = self.factory.get_supported_types()
        expected_types = ['boolean', 'ranked', 'semantic']
        
        self.assertEqual(set(types), set(expected_types))


class TestSearchEngineStateManagement(unittest.TestCase):
    """Test state management and history tracking."""
    
    def setUp(self):
        """Set up engine for state testing."""
        self.engine = BooleanSearchEngine("state_test", "State Test Engine")
        self.engine.add_document({"doc_id": "1", "title": "Test", "text": "test content"})
    
    def test_search_history_tracking(self):
        """Test that search history is properly tracked."""
        # Initially no history
        self.assertEqual(len(self.engine.get_search_history()), 0)
        
        # Perform searches
        self.engine.search("test query 1")
        self.engine.search("test query 2")
        
        # Should have 2 entries
        history = self.engine.get_search_history()
        self.assertEqual(len(history), 2)
        
        # Check history content
        self.assertEqual(history[0]['query'], "test query 1")
        self.assertEqual(history[1]['query'], "test query 2")
    
    def test_history_clearing(self):
        """Test clearing search history."""
        # Add some history
        self.engine.search("test query")
        self.assertEqual(len(self.engine.get_search_history()), 1)
        
        # Clear history
        self.engine.clear_history()
        self.assertEqual(len(self.engine.get_search_history()), 0)
    
    def test_document_management(self):
        """Test document addition and retrieval."""
        initial_count = self.engine.document_count
        
        # Add document
        new_doc = {"doc_id": "2", "title": "New Doc", "text": "new content"}
        self.engine.add_document(new_doc)
        
        self.assertEqual(self.engine.document_count, initial_count + 1)
        
        # Retrieve documents
        docs = self.engine.get_documents()
        self.assertEqual(len(docs), initial_count + 1)
        
        # Should be a copy (modification shouldn't affect internal state)
        docs.append({"doc_id": "3", "title": "External", "text": "external"})
        self.assertEqual(self.engine.document_count, initial_count + 1)


if __name__ == '__main__':
    # Create test suite
    test_classes = [
        TestAbstractBaseClass,
        TestInheritanceHierarchy,
        TestPolymorphicBehavior,
        TestFunctionLibraryIntegration,
        TestSpecializedFeatures,
        TestFactoryPattern,
        TestSearchEngineStateManagement
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("TEAM MEMBER 2 - SEARCH SYSTEM TESTS SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
