#!/usr/bin/env python3
"""
Demo script for the Search and Order Management System
Demonstrates all major functionality with example workflows
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import SearchOrderSystem


def demo_header(title: str):
    """Print a formatted header for demo sections."""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)


def demo_basic_functionality():
    """Demonstrate basic system functionality."""
    demo_header("Basic System Functionality")
    
    print("📚 Initializing Search and Order Management System...")
    system = SearchOrderSystem("demo_data")
    
    print(f"✅ System initialized with {len(system.documents)} documents")
    print(f"🔍 Available search engines: {list(system.search_engines.keys())}")
    print(f"👥 Current users: {len(system.users)}")
    print(f"📦 Current orders: {len(system.orders)}")
    
    return system


def demo_data_import(system: SearchOrderSystem):
    """Demonstrate importing data from different formats."""
    demo_header("Data Import Capabilities")
    
    # Import from CSV
    print("📥 Importing documents from CSV...")
    try:
        system.import_documents_csv("data/sample_documents.csv")
        print(f"✅ CSV import successful! Now have {len(system.documents)} documents")
    except Exception as e:
        print(f"⚠️  CSV import failed: {e}")
    
    # Import from XML
    print("\n📥 Importing documents from XML...")
    try:
        system.import_documents_xml("data/sample_documents.xml")
        print(f"✅ XML import successful! Now have {len(system.documents)} documents")
    except Exception as e:
        print(f"⚠️  XML import failed: {e}")
    
    # Show sample document
    if system.documents:
        doc_id = list(system.documents.keys())[0]
        doc = system.documents[doc_id]
        print(f"\n📄 Sample document:")
        print(f"   ID: {doc.doc_id}")
        print(f"   Title: {doc.title}")
        print(f"   Content: {doc.content[:100]}...")
        print(f"   Tags: {doc.metadata.get('tags', []) if doc.metadata else []}")


def demo_search_engines(system: SearchOrderSystem):
    """Demonstrate different search engines."""
    demo_header("Search Engine Demonstration")
    
    queries = ["Python programming", "data science", "food safety"]
    engines = ["boolean", "ranked", "semantic"]
    
    for query in queries[:2]:  # Test with first 2 queries
        print(f"\n🔍 Searching for: '{query}'")
        
        for engine in engines:
            print(f"\n   Using {engine.upper()} engine:")
            try:
                results = system.search_documents(query, engine, "demo_user")
                print(f"     Found {len(results)} results")
                
                # Show top 2 results
                for i, doc in enumerate(results[:2], 1):
                    print(f"     {i}. {doc.title} (ID: {doc.doc_id})")
            
            except Exception as e:
                print(f"     ❌ Error: {e}")


def demo_user_management(system: SearchOrderSystem):
    """Demonstrate user management and history tracking."""
    demo_header("User Management & History Tracking")
    
    # Create multiple users with different search patterns
    users = ["alice", "bob", "charlie"]
    
    for user in users:
        print(f"\n👤 User: {user}")
        
        # Perform some searches for each user
        queries = ["Python tutorial", "recipe collection", "machine learning"]
        for query in queries[:2]:  # 2 searches per user
            results = system.search_documents(query, "ranked", user)
            print(f"   Searched '{query}': {len(results)} results")
    
    # Show user activity
    print(f"\n📊 System now has {len(system.users)} users")
    for user_id, user in system.users.items():
        print(f"   {user_id}: {len(user.search_history)} searches")


def demo_order_processing(system: SearchOrderSystem):
    """Demonstrate order processing functionality."""
    demo_header("Order Processing System")
    
    # Place some orders
    orders_data = [
        ("alice", "pizza, soda, salad"),
        ("bob", "burger, fries, shake"),
        ("charlie", "pasta, bread, wine"),
        ("alice", "coffee, sandwich")  # Alice orders again
    ]
    
    for user, order_text in orders_data:
        print(f"\n🍽️  Processing order for {user}: {order_text}")
        order = system.place_order(user, order_text)
        
        if 'error' in order:
            print(f"   ❌ Order failed: {order['error']}")
        else:
            print(f"   ✅ Order {order['order_id']} placed successfully")
            print(f"   📦 Items: {order.get('items', [])}")
    
    print(f"\n📈 Total orders processed: {len(system.orders)}")


def demo_export_functionality(system: SearchOrderSystem):
    """Demonstrate exporting search results."""
    demo_header("Export Functionality")
    
    # Perform a search to get results
    print("🔍 Searching for 'programming' to export results...")
    results = system.search_documents("programming", "ranked")
    print(f"Found {len(results)} results")
    
    # Export in different formats
    export_formats = [
        ("programming_results.json", "json"),
        ("programming_results.csv", "csv"),
        ("programming_results.xml", "xml")
    ]
    
    for filename, format_type in export_formats:
        try:
            system.export_search_results(results, filename, format_type)
            print(f"✅ Exported to {filename} ({format_type.upper()} format)")
        except Exception as e:
            print(f"❌ Export failed for {filename}: {e}")


def demo_reports(system: SearchOrderSystem):
    """Demonstrate report generation."""
    demo_header("Report Generation")
    
    reports = ["summary", "user_activity", "popular_searches"]
    
    for report_type in reports:
        print(f"\n📊 Generating {report_type} report:")
        try:
            report = system.generate_report(report_type)
            
            if report_type == "summary":
                print(f"   Documents: {report.get('documents_count', 0)}")
                print(f"   Users: {report.get('users_count', 0)}")
                print(f"   Orders: {report.get('orders_count', 0)}")
                print(f"   Search Engines: {report.get('search_engines', [])}")
            
            elif report_type == "user_activity":
                print("   User Activity:")
                for user, stats in report.items():
                    if isinstance(stats, dict):
                        searches = stats.get('search_count', 0)
                        orders = stats.get('order_count', 0)
                        print(f"     {user}: {searches} searches, {orders} orders")
            
            elif report_type == "popular_searches":
                print("   Popular Searches:")
                for query, count in list(report.items())[:5]:  # Top 5
                    print(f"     '{query}': {count} times")
            
        except Exception as e:
            print(f"   ❌ Report failed: {e}")


def demo_persistence(system: SearchOrderSystem):
    """Demonstrate data persistence."""
    demo_header("Data Persistence")
    
    print("💾 Saving system state...")
    system.save_system_state()
    print("✅ System state saved to disk")
    
    # Show what was saved
    data_dir = Path(system.data_dir)
    saved_files = list(data_dir.glob("*.json"))
    
    print(f"\n📁 Saved files in {data_dir}:")
    for file in saved_files:
        size = file.stat().st_size
        print(f"   {file.name}: {size:,} bytes")
    
    # Demonstrate loading by creating new system
    print(f"\n🔄 Creating new system instance to test persistence...")
    new_system = SearchOrderSystem(str(data_dir))
    
    print(f"✅ Loaded system state:")
    print(f"   Documents: {len(new_system.documents)}")
    print(f"   Users: {len(new_system.users)}")
    print(f"   Orders: {len(new_system.orders)}")


def demo_error_handling():
    """Demonstrate error handling capabilities."""
    demo_header("Error Handling Demonstration")
    
    system = SearchOrderSystem("demo_data")
    
    # Test missing file import
    print("Testing import of non-existent file...")
    try:
        system.import_documents_csv("nonexistent.csv")
    except FileNotFoundError as e:
        print(f"✅ Properly handled missing file: {e}")
    
    # Test invalid search engine
    print("\nTesting invalid search engine...")
    try:
        system.search_documents("test", "invalid_engine")
    except ValueError as e:
        print(f"✅ Properly handled invalid engine: {e}")
    
    # Test malformed data
    print("\nTesting search with no documents...")
    results = system.search_documents("anything", "ranked")
    print(f"✅ Gracefully handled empty search: {len(results)} results")


def demo_complete_workflow():
    """Demonstrate a complete end-to-end workflow."""
    demo_header("Complete Workflow Demonstration")
    
    print("🚀 Running complete workflow: Import → Search → Order → Export → Report → Save")
    
    # Initialize clean system
    workflow_system = SearchOrderSystem("workflow_demo")
    
    # Step 1: Import data
    print("\n1️⃣ Importing sample data...")
    try:
        workflow_system.import_documents_csv("data/sample_documents.csv")
        print(f"   ✅ Imported {len(workflow_system.documents)} documents")
    except:
        print("   ⚠️  Using existing documents")
    
    # Step 2: Search documents
    print("\n2️⃣ Performing searches...")
    search_queries = ["Python", "food recipes"]
    all_results = []
    
    for query in search_queries:
        results = workflow_system.search_documents(query, "ranked", "workflow_user")
        all_results.extend(results)
        print(f"   🔍 '{query}': {len(results)} results")
    
    # Step 3: Place orders
    print("\n3️⃣ Processing orders...")
    orders = ["pizza, salad", "coffee, sandwich"]
    for order in orders:
        result = workflow_system.place_order("workflow_user", order)
        print(f"   🍽️  Order placed: {result.get('order_id', 'Failed')}")
    
    # Step 4: Export results
    print("\n4️⃣ Exporting search results...")
    if all_results:
        workflow_system.export_search_results(all_results[:3], "workflow_results.json")
        print("   📤 Results exported to workflow_results.json")
    
    # Step 5: Generate report
    print("\n5️⃣ Generating system report...")
    report = workflow_system.generate_report("summary")
    print(f"   📊 Report: {report.get('documents_count')} docs, {report.get('users_count')} users, {report.get('orders_count')} orders")
    
    # Step 6: Save state
    print("\n6️⃣ Saving system state...")
    workflow_system.save_system_state()
    print("   💾 State saved successfully")
    
    print("\n🎉 Complete workflow finished successfully!")


def main():
    """Run the complete demo."""
    print("🎬 Welcome to the Search and Order Management System Demo!")
    print("This demonstration will show all major system capabilities.")
    
    try:
        # Initialize system
        system = demo_basic_functionality()
        
        # Run demonstrations
        demo_data_import(system)
        demo_search_engines(system)
        demo_user_management(system)
        demo_order_processing(system)
        demo_export_functionality(system)
        demo_reports(system)
        demo_persistence(system)
        demo_error_handling()
        demo_complete_workflow()
        
        print("\n" + "="*60)
        print("🎉 Demo completed successfully!")
        print("✨ The Search and Order Management System is ready for use!")
        print("📚 Check README.md for detailed usage instructions")
        print("🧪 Run tests with: python tests/test_project4.py")
        print("🚀 Try interactive mode with: python main.py --interactive")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
