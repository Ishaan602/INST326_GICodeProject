"""
Comprehensive test suite for Project 4: Search and Order Management System
Tests all major functionality including persistence, I/O, and system integration.
"""

import unittest
import tempfile
import shutil
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import SearchOrderSystem
from src.document import Document
from src.search_query import SearchQuery


class TestSearchOrderSystem(unittest.TestCase):
    """Test the main SearchOrderSystem class."""
    
    def setUp(self):
        """Set up test environment with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.system = SearchOrderSystem(self.test_dir)
        
        # Add some test documents
        self.test_docs = [
            Document("test1", "Python Programming", "Learn Python basics", {"tags": ["python", "programming"]}),
            Document("test2", "Data Science", "Data analysis with Python", {"tags": ["data", "python"]}),
            Document("test3", "Pizza Recipe", "How to make pizza", {"tags": ["food", "recipe"]})
        ]
        
        for doc in self.test_docs:
            self.system.documents[doc.doc_id] = doc
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_system_initialization(self):
        """Test system initializes correctly."""
        self.assertIsInstance(self.system, SearchOrderSystem)
        self.assertEqual(len(self.system.search_engines), 3)
        self.assertIn('boolean', self.system.search_engines)
        self.assertIn('ranked', self.system.search_engines)
        self.assertIn('semantic', self.system.search_engines)
    
    def test_save_load_system_state(self):
        """Test saving and loading system state."""
        # Add test data
        self.system.orders = [{'order_id': 'test_order', 'user_id': 'test_user', 'items': ['pizza']}]
        self.system.session_data = {'test_key': 'test_value'}
        
        # Save state
        self.system.save_system_state()
        
        # Verify files exist
        self.assertTrue((Path(self.test_dir) / "documents.json").exists())
        self.assertTrue((Path(self.test_dir) / "orders.json").exists())
        self.assertTrue((Path(self.test_dir) / "session.json").exists())
        
        # Create new system and load
        new_system = SearchOrderSystem(self.test_dir)
        
        # Verify data loaded correctly
        self.assertEqual(len(new_system.documents), len(self.test_docs))
        self.assertEqual(len(new_system.orders), 1)
        self.assertEqual(new_system.orders[0]['order_id'], 'test_order')
        self.assertEqual(new_system.session_data['test_key'], 'test_value')
    
    def test_csv_import(self):
        """Test importing documents from CSV."""
        # Create test CSV file
        csv_file = Path(self.test_dir) / "test_docs.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'content', 'tags'])
            writer.writerow(['csv1', 'Test Document', 'Test content', 'tag1,tag2'])
            writer.writerow(['csv2', 'Another Document', 'More content', 'tag3'])
        
        # Import CSV
        initial_count = len(self.system.documents)
        self.system.import_documents_csv(str(csv_file))
        
        # Verify import
        self.assertEqual(len(self.system.documents), initial_count + 2)
        self.assertIn('csv1', self.system.documents)
        self.assertIn('csv2', self.system.documents)
        
        csv_doc = self.system.documents['csv1']
        self.assertEqual(csv_doc.title, 'Test Document')
        self.assertEqual(csv_doc.metadata.get('tags', []), ['tag1', 'tag2'])
    
    def test_xml_import(self):
        """Test importing documents from XML."""
        # Create test XML file
        xml_file = Path(self.test_dir) / "test_docs.xml"
        root = ET.Element('documents')
        
        doc_elem = ET.SubElement(root, 'document', id='xml1')
        title_elem = ET.SubElement(doc_elem, 'title')
        title_elem.text = 'XML Test Document'
        content_elem = ET.SubElement(doc_elem, 'content')
        content_elem.text = 'XML test content'
        
        tags_elem = ET.SubElement(doc_elem, 'tags')
        tag_elem = ET.SubElement(tags_elem, 'tag')
        tag_elem.text = 'xml'
        
        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
        
        # Import XML
        initial_count = len(self.system.documents)
        self.system.import_documents_xml(str(xml_file))
        
        # Verify import
        self.assertEqual(len(self.system.documents), initial_count + 1)
        self.assertIn('xml1', self.system.documents)
        
        xml_doc = self.system.documents['xml1']
        self.assertEqual(xml_doc.title, 'XML Test Document')
        self.assertEqual(xml_doc.metadata.get('tags', []), ['xml'])
    
    def test_search_functionality(self):
        """Test document search functionality."""
        # Test search with different engines
        results = self.system.search_documents("Python", "boolean")
        self.assertGreater(len(results), 0)
        
        results = self.system.search_documents("Python", "ranked")
        self.assertGreater(len(results), 0)
        
        results = self.system.search_documents("nonexistent", "boolean")
        self.assertEqual(len(results), 0)
    
    def test_search_with_user_history(self):
        """Test search with user history tracking."""
        user_id = "test_user"
        
        # Perform search with user tracking
        results = self.system.search_documents("Python", "ranked", user_id)
        
        # Verify user was created and history recorded
        self.assertIn(user_id, self.system.users)
        user = self.system.users[user_id]
        self.assertEqual(len(user.search_history), 1)
        self.assertEqual(user.search_history[0]['query'], "Python")
        self.assertEqual(user.search_history[0]['engine'], "ranked")
    
    def test_order_placement(self):
        """Test order placement functionality."""
        user_id = "test_user"
        order_text = "pizza, soda, salad"
        
        order = self.system.place_order(user_id, order_text)
        
        # Verify order was created
        self.assertIn('order_id', order)
        self.assertEqual(order['user_id'], user_id)
        self.assertEqual(order['order_text'], order_text)
        self.assertEqual(len(self.system.orders), 1)
        
        # Verify user was created
        self.assertIn(user_id, self.system.users)
    
    def test_export_json(self):
        """Test exporting search results to JSON."""
        results = list(self.system.documents.values())[:2]
        filename = "test_export.json"
        
        self.system.export_search_results(results, filename, 'json')
        
        # Verify export file exists
        export_file = Path(self.test_dir) / filename
        self.assertTrue(export_file.exists())
        
        # Verify export content
        with open(export_file, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], results[0].doc_id)
        self.assertEqual(data[0]['title'], results[0].title)
    
    def test_export_csv(self):
        """Test exporting search results to CSV."""
        results = list(self.system.documents.values())[:1]
        filename = "test_export.csv"
        
        self.system.export_search_results(results, filename, 'csv')
        
        # Verify export file exists
        export_file = Path(self.test_dir) / filename
        self.assertTrue(export_file.exists())
        
        # Verify export content
        with open(export_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 2)  # Header + 1 data row
        self.assertEqual(rows[0], ['id', 'title', 'content', 'tags'])
        self.assertEqual(rows[1][0], results[0].doc_id)
    
    def test_export_xml(self):
        """Test exporting search results to XML."""
        results = list(self.system.documents.values())[:1]
        filename = "test_export.xml"
        
        self.system.export_search_results(results, filename, 'xml')
        
        # Verify export file exists
        export_file = Path(self.test_dir) / filename
        self.assertTrue(export_file.exists())
        
        # Verify export content
        tree = ET.parse(export_file)
        root = tree.getroot()
        
        self.assertEqual(root.tag, 'search_results')
        doc_elements = root.findall('document')
        self.assertEqual(len(doc_elements), 1)
        self.assertEqual(doc_elements[0].get('id'), results[0].doc_id)
    
    def test_generate_summary_report(self):
        """Test generating system summary report."""
        report = self.system.generate_report('summary')
        
        self.assertIn('documents_count', report)
        self.assertIn('users_count', report)
        self.assertIn('orders_count', report)
        self.assertIn('search_engines', report)
        self.assertEqual(report['documents_count'], len(self.test_docs))
    
    def test_generate_user_activity_report(self):
        """Test generating user activity report."""
        # Add some user activity
        self.system.search_documents("test", "ranked", "user1")
        self.system.place_order("user1", "pizza")
        
        report = self.system.generate_report('user_activity')
        
        self.assertIn('user1', report)
        self.assertEqual(report['user1']['search_count'], 1)
        self.assertEqual(report['user1']['order_count'], 1)
    
    def test_generate_popular_searches_report(self):
        """Test generating popular searches report."""
        # Add some search activity
        self.system.search_documents("Python", "ranked", "user1")
        self.system.search_documents("Python", "ranked", "user2")
        self.system.search_documents("Data", "ranked", "user1")
        
        report = self.system.generate_report('popular_searches')
        
        self.assertIn('Python', report)
        self.assertIn('Data', report)
        self.assertEqual(report['Python'], 2)
        self.assertEqual(report['Data'], 1)
    
    def test_error_handling_missing_files(self):
        """Test error handling for missing import files."""
        with self.assertRaises(FileNotFoundError):
            self.system.import_documents_csv("nonexistent.csv")
        
        with self.assertRaises(FileNotFoundError):
            self.system.import_documents_xml("nonexistent.xml")
    
    def test_error_handling_invalid_csv(self):
        """Test error handling for invalid CSV data."""
        # Create CSV with missing required fields
        csv_file = Path(self.test_dir) / "invalid.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title'])  # Missing content field
            writer.writerow(['test1', 'Test Title'])
        
        initial_count = len(self.system.documents)
        self.system.import_documents_csv(str(csv_file))
        
        # Should not import invalid rows
        self.assertEqual(len(self.system.documents), initial_count)
    
    def test_invalid_search_engine(self):
        """Test error handling for invalid search engine."""
        with self.assertRaises(ValueError):
            self.system.search_documents("test", "invalid_engine")


class TestSystemIntegration(unittest.TestCase):
    """Test system integration and workflows."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.system = SearchOrderSystem(self.test_dir)
    
    def tearDown(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_complete_workflow(self):
        """Test complete workflow from import to export."""
        # 1. Import sample data
        csv_file = Path(self.test_dir) / "sample.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'content', 'tags'])
            writer.writerow(['flow1', 'Integration Test', 'Testing workflow', 'test,integration'])
        
        self.system.import_documents_csv(str(csv_file))
        
        # 2. Perform search
        results = self.system.search_documents("Integration", "ranked", "test_user")
        self.assertGreater(len(results), 0)
        
        # 3. Place order
        order = self.system.place_order("test_user", "test_order")
        self.assertIn('order_id', order)
        
        # 4. Export results
        self.system.export_search_results(results, "workflow_results.json", "json")
        
        # 5. Generate report
        report = self.system.generate_report("summary")
        self.assertGreater(report['documents_count'], 0)
        self.assertGreater(report['users_count'], 0)
        self.assertGreater(report['orders_count'], 0)
        
        # 6. Save and reload state
        self.system.save_system_state()
        new_system = SearchOrderSystem(self.test_dir)
        
        # Verify state persistence
        self.assertEqual(len(new_system.documents), len(self.system.documents))
        self.assertEqual(len(new_system.orders), len(self.system.orders))
        self.assertEqual(len(new_system.users), len(self.system.users))


def run_tests():
    """Run all tests and print results."""
    print("🧪 Running Project 4 Test Suite...")
    print("=" * 60)
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSearchOrderSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemIntegration))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"🎯 Test Results Summary:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"   {test}: {failure}")
    
    if result.errors:
        print("\n⚠️  ERRORS:")
        for test, error in result.errors:
            print(f"   {test}: {error}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
