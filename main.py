#!/usr/bin/env python3
"""
INST326 Project 4: Search and Order Management System
Main application entry point with data persistence and I/O capabilities.

This system integrates search functionality with user management and order processing,
providing a complete solution for document search and food ordering workflows.
"""

import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
import sys
from datetime import datetime

# Import our project modules
from src.search_system import BooleanSearchEngine, RankedSearchEngine, SemanticSearchEngine
from src.document import Document
from src.search_query import SearchQuery


class SimpleUserProfile:
    """Simple user profile for system integration."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.preferences: Dict[str, Any] = {}
        self.search_history: List[Dict[str, Any]] = []


class SearchOrderSystem:
    """
    Main application class that integrates search and order management
    with complete data persistence and I/O capabilities.
    """
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the system with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Core components
        self.documents: Dict[str, Document] = {}
        self.users: Dict[str, SimpleUserProfile] = {}
        self.search_engines = {
            'boolean': BooleanSearchEngine('boolean_1', 'Boolean Search Engine'),
            'ranked': RankedSearchEngine('ranked_1', 'Ranked Search Engine'),
            'semantic': SemanticSearchEngine('semantic_1', 'Semantic Search Engine')
        }
        self.orders: List[Dict[str, Any]] = []
        self.session_data: Dict[str, Any] = {}
        
        # Load existing data
        self.load_system_state()
    
    def load_system_state(self) -> None:
        """Load all system state from persistence files."""
        try:
            # Load documents
            docs_file = self.data_dir / "documents.json"
            if docs_file.exists():
                with open(docs_file, 'r', encoding='utf-8') as f:
                    docs_data = json.load(f)
                    for doc_id, doc_info in docs_data.items():
                        self.documents[doc_id] = Document(
                            doc_id=doc_info['id'],
                            title=doc_info['title'],
                            content=doc_info['content'],
                            metadata={'tags': doc_info.get('tags', [])}
                        )
            
            # Load users
            users_file = self.data_dir / "users.json"
            if users_file.exists():
                with open(users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    for user_id, user_info in users_data.items():
                        profile = SimpleUserProfile(user_id)
                        profile.preferences = user_info.get('preferences', {})
                        profile.search_history = user_info.get('search_history', [])
                        self.users[user_id] = profile
            
            # Load orders
            orders_file = self.data_dir / "orders.json"
            if orders_file.exists():
                with open(orders_file, 'r', encoding='utf-8') as f:
                    self.orders = json.load(f)
            
            # Load session data
            session_file = self.data_dir / "session.json"
            if session_file.exists():
                with open(session_file, 'r', encoding='utf-8') as f:
                    self.session_data = json.load(f)
                    
            print(f"✓ Loaded system state: {len(self.documents)} documents, {len(self.users)} users, {len(self.orders)} orders")
            
        except Exception as e:
            print(f"Warning: Could not load some system state: {e}")
    
    def save_system_state(self) -> None:
        """Save all system state to persistence files."""
        try:
            # Save documents
            docs_data = {}
            for doc_id, doc in self.documents.items():
                docs_data[doc_id] = {
                    'id': doc.doc_id,
                    'title': doc.title,
                    'content': doc.content,
                    'tags': doc.metadata.get('tags', []) if doc.metadata else []
                }
            
            with open(self.data_dir / "documents.json", 'w', encoding='utf-8') as f:
                json.dump(docs_data, f, indent=2, ensure_ascii=False)
            
            # Save users
            users_data = {}
            for user_id, user in self.users.items():
                users_data[user_id] = {
                    'preferences': user.preferences,
                    'search_history': user.search_history
                }
            
            with open(self.data_dir / "users.json", 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2)
            
            # Save orders
            with open(self.data_dir / "orders.json", 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, indent=2)
            
            # Save session data
            self.session_data['last_saved'] = datetime.now().isoformat()
            with open(self.data_dir / "session.json", 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2)
                
            print(f"✓ Saved system state to {self.data_dir}")
            
        except Exception as e:
            print(f"Error saving system state: {e}")
    
    def import_documents_csv(self, csv_file: str) -> None:
        """Import documents from CSV file."""
        csv_path = Path(csv_file)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                imported_count = 0
                
                for row in reader:
                    # Validate required fields
                    if 'id' not in row or 'title' not in row or 'content' not in row:
                        print(f"Warning: Skipping invalid row: {row}")
                        continue
                    
                    doc = Document(
                        doc_id=row['id'],
                        title=row['title'],
                        content=row['content'],
                        metadata={'tags': row.get('tags', '').split(',') if row.get('tags') else []}
                    )
                    self.documents[doc.doc_id] = doc
                    imported_count += 1
                
                print(f"✓ Imported {imported_count} documents from CSV")
                
        except Exception as e:
            print(f"Error importing CSV: {e}")
            raise
    
    def import_documents_xml(self, xml_file: str) -> None:
        """Import documents from XML file."""
        xml_path = Path(xml_file)
        if not xml_path.exists():
            raise FileNotFoundError(f"XML file not found: {xml_file}")
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            imported_count = 0
            
            for doc_elem in root.findall('document'):
                doc_id = doc_elem.get('id') or doc_elem.findtext('id')
                title = doc_elem.findtext('title')
                content = doc_elem.findtext('content')
                
                if not all([doc_id, title, content]):
                    print(f"Warning: Skipping invalid document element")
                    continue
                
                tags_elem = doc_elem.find('tags')
                tags = []
                if tags_elem is not None:
                    tags = [tag.text for tag in tags_elem.findall('tag') if tag.text]
                
                doc = Document(doc_id=doc_id, title=title, content=content, metadata={'tags': tags})
                self.documents[doc.doc_id] = doc
                imported_count += 1
            
            print(f"✓ Imported {imported_count} documents from XML")
            
        except Exception as e:
            print(f"Error importing XML: {e}")
            raise
    
    def export_search_results(self, results: List[Document], filename: str, format: str = 'json') -> None:
        """Export search results to file in specified format."""
        export_path = self.data_dir / filename
        
        try:
            if format.lower() == 'json':
                results_data = []
                for doc in results:
                    results_data.append({
                        'id': doc.doc_id,
                        'title': doc.title,
                        'content': doc.content,
                        'tags': doc.metadata.get('tags', []) if doc.metadata else []
                    })
                
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(results_data, f, indent=2, ensure_ascii=False)
            
            elif format.lower() == 'csv':
                with open(export_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id', 'title', 'content', 'tags'])
                    
                    for doc in results:
                        writer.writerow([
                            doc.doc_id,
                            doc.title,
                            doc.content,
                            ','.join(doc.metadata.get('tags', []) if doc.metadata else [])
                        ])
            
            elif format.lower() == 'xml':
                root = ET.Element('search_results')
                for doc in results:
                    doc_elem = ET.SubElement(root, 'document', id=doc.doc_id)
                    
                    title_elem = ET.SubElement(doc_elem, 'title')
                    title_elem.text = doc.title
                    
                    content_elem = ET.SubElement(doc_elem, 'content')
                    content_elem.text = doc.content
                    
                    tags = doc.metadata.get('tags', []) if doc.metadata else []
                    if tags:
                        tags_elem = ET.SubElement(doc_elem, 'tags')
                        for tag in tags:
                            tag_elem = ET.SubElement(tags_elem, 'tag')
                            tag_elem.text = tag
                
                tree = ET.ElementTree(root)
                tree.write(export_path, encoding='utf-8', xml_declaration=True)
            
            print(f"✓ Exported {len(results)} results to {export_path}")
            
        except Exception as e:
            print(f"Error exporting results: {e}")
            raise
    
    def search_documents(self, query: str, engine_type: str = 'ranked', user_id: Optional[str] = None) -> List[Document]:
        """Search documents using specified search engine."""
        if engine_type not in self.search_engines:
            raise ValueError(f"Invalid engine type: {engine_type}")
        
        engine = self.search_engines[engine_type]
        
        try:
            # Add documents to engine for search
            for doc in self.documents.values():
                doc_dict = {
                    'doc_id': doc.doc_id,
                    'title': doc.title,
                    'text': doc.content,
                    'tags': doc.metadata.get('tags', []) if doc.metadata else []
                }
                engine.add_document(doc_dict)
            
            # Perform search
            search_result = engine.search(query)
            
            # Convert results back to Document objects
            results = []
            for result in search_result.get('results', []):
                doc_id = result.get('doc_id')
                if doc_id in self.documents:
                    results.append(self.documents[doc_id])
            
            # Record search in user history if user provided
            if user_id:
                if user_id not in self.users:
                    self.users[user_id] = SimpleUserProfile(user_id)
                
                self.users[user_id].search_history.append({
                    'query': query,
                    'engine': engine_type,
                    'timestamp': datetime.now().isoformat(),
                    'results_count': len(results)
                })
            
            return results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def place_order(self, user_id: str, order_text: str) -> Dict[str, Any]:
        """Place a food order for a user."""
        try:
            if user_id not in self.users:
                self.users[user_id] = SimpleUserProfile(user_id)
            
            # Simple order processing (can be enhanced)
            order = {
                'order_id': f"order_{len(self.orders) + 1}",
                'user_id': user_id,
                'order_text': order_text,
                'items': order_text.split(','),
                'timestamp': datetime.now().isoformat(),
                'status': 'placed'
            }
            
            self.orders.append(order)
            return order
            
        except Exception as e:
            print(f"Error placing order: {e}")
            return {'error': str(e)}
    
    def generate_report(self, report_type: str) -> Dict[str, Any]:
        """Generate system reports."""
        try:
            if report_type == 'summary':
                return {
                    'documents_count': len(self.documents),
                    'users_count': len(self.users),
                    'orders_count': len(self.orders),
                    'search_engines': list(self.search_engines.keys()),
                    'generated_at': datetime.now().isoformat()
                }
            
            elif report_type == 'user_activity':
                user_stats = {}
                for user_id, user in self.users.items():
                    user_stats[user_id] = {
                        'search_count': len(user.search_history),
                        'order_count': len([o for o in self.orders if o['user_id'] == user_id])
                    }
                return user_stats
            
            elif report_type == 'popular_searches':
                all_queries = []
                for user in self.users.values():
                    all_queries.extend([entry['query'] for entry in user.search_history])
                
                # Count query frequency
                query_counts = {}
                for query in all_queries:
                    query_counts[query] = query_counts.get(query, 0) + 1
                
                # Sort by frequency
                popular = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)
                return dict(popular[:10])  # Top 10
            
            else:
                return {'error': f'Unknown report type: {report_type}'}
                
        except Exception as e:
            return {'error': str(e)}


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description='Search and Order Management System')
    parser.add_argument('--data-dir', default='data', help='Data directory path')
    parser.add_argument('--import-csv', help='Import documents from CSV file')
    parser.add_argument('--import-xml', help='Import documents from XML file')
    parser.add_argument('--search', help='Search query')
    parser.add_argument('--engine', choices=['boolean', 'ranked', 'semantic'], 
                       default='ranked', help='Search engine type')
    parser.add_argument('--user-id', help='User ID for search history')
    parser.add_argument('--export', help='Export filename for results')
    parser.add_argument('--export-format', choices=['json', 'csv', 'xml'], 
                       default='json', help='Export format')
    parser.add_argument('--report', choices=['summary', 'user_activity', 'popular_searches'],
                       help='Generate report')
    parser.add_argument('--interactive', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Initialize system
    print("🚀 Initializing Search and Order Management System...")
    system = SearchOrderSystem(args.data_dir)
    
    try:
        # Handle imports
        if args.import_csv:
            print(f"📥 Importing from CSV: {args.import_csv}")
            system.import_documents_csv(args.import_csv)
            system.save_system_state()
        
        if args.import_xml:
            print(f"📥 Importing from XML: {args.import_xml}")
            system.import_documents_xml(args.import_xml)
            system.save_system_state()
        
        # Handle search
        if args.search:
            print(f"🔍 Searching for: '{args.search}' using {args.engine} engine")
            results = system.search_documents(args.search, args.engine, args.user_id)
            
            print(f"Found {len(results)} results:")
            for i, doc in enumerate(results[:5], 1):  # Show top 5
                print(f"  {i}. {doc.title} (ID: {doc.doc_id})")
            
            # Export results if requested
            if args.export:
                system.export_search_results(results, args.export, args.export_format)
            
            system.save_system_state()
        
        # Handle reports
        if args.report:
            print(f"📊 Generating {args.report} report...")
            report = system.generate_report(args.report)
            print(json.dumps(report, indent=2))
        
        # Interactive mode
        if args.interactive:
            run_interactive_mode(system)
        
        # Always save state before exit
        system.save_system_state()
        print("✅ System shutdown complete")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        system.save_system_state()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        system.save_system_state()
        sys.exit(1)


def run_interactive_mode(system: SearchOrderSystem):
    """Run the system in interactive mode."""
    print("\n🎯 Welcome to Interactive Mode!")
    print("Available commands: search, order, report, export, quit")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == 'quit':
                break
            
            elif command == 'search':
                query = input("Enter search query: ")
                engine = input("Engine type (boolean/ranked/semantic) [ranked]: ") or 'ranked'
                user_id = input("User ID (optional): ") or None
                
                results = system.search_documents(query, engine, user_id)
                print(f"Found {len(results)} results:")
                for i, doc in enumerate(results[:3], 1):
                    print(f"  {i}. {doc.title}")
            
            elif command == 'order':
                user_id = input("User ID: ")
                order_text = input("Order items (comma-separated): ")
                
                order = system.place_order(user_id, order_text)
                print(f"Order placed: {order.get('order_id', 'Error')}")
            
            elif command == 'report':
                report_type = input("Report type (summary/user_activity/popular_searches): ")
                report = system.generate_report(report_type)
                print(json.dumps(report, indent=2))
            
            elif command == 'export':
                query = input("Search query for export: ")
                results = system.search_documents(query)
                filename = input("Export filename: ")
                format = input("Format (json/csv/xml) [json]: ") or 'json'
                
                system.export_search_results(results, filename, format)
            
            else:
                print("Unknown command. Try: search, order, report, export, quit")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
