#!/usr/bin/env python3
"""
Demo Script for INST326 Information Retrieval Function Library

This script demonstrates the key functions and capabilities of the library
with practical examples and sample data.
"""

import sys
import os

# Add the src directory to the Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from library_name import (
    filter_sort_paginate_results,
    highlight_query_terms,
    normalize_query,
    truncate_snippet,
    count_term_frequency,
    validate_information,
    format_query,
    calculate_user_distance,
    parse_user_order,
    process_multiple_order_data
)


def demo_text_processing():
    """Demonstrate text processing capabilities"""
    print("=" * 60)
    print("TEXT PROCESSING DEMONSTRATION")
    print("=" * 60)
    
    # Query normalization
    print("1. Query Normalization")
    print("-" * 30)
    messy_queries = [
        "  MACHINE    learning   ",
        "Data   Mining    Algorithms",
        "   information     RETRIEVAL  "
    ]
    
    for query in messy_queries:
        normalized = normalize_query(query)
        print(f"Original:   '{query}'")
        print(f"Normalized: '{normalized}'")
        print()
    
    # Term frequency counting
    print("2. Term Frequency Counting")
    print("-" * 30)
    sample_text = "Data mining involves mining data from databases using data mining techniques and data analysis methods"
    terms_to_count = ["data", "mining", "analysis"]
    
    print(f"Text: {sample_text}")
    print()
    for term in terms_to_count:
        count = count_term_frequency(sample_text, term)
        print(f"'{term}' appears {count} times")
    print()
    
    # Text highlighting
    print("3. Text Highlighting")
    print("-" * 30)
    documents = [
        "Introduction to machine learning and data science",
        "Advanced algorithms for data mining applications",
        "Statistical methods in information retrieval systems"
    ]
    
    search_terms = ["data", "machine", "algorithms"]
    
    for i, doc in enumerate(documents, 1):
        highlighted = highlight_query_terms(doc, search_terms)
        print(f"Document {i}: {highlighted}")
    print()
    
    # Text truncation
    print("4. Text Truncation")
    print("-" * 30)
    long_text = "This is a very long document that contains important information about information retrieval systems and their applications in modern computing environments"
    
    for length in [30, 50, 80]:
        truncated = truncate_snippet(long_text, length)
        print(f"Max {length} chars: {truncated}")
    print()


def demo_search_system():
    """Demonstrate search and pagination system"""
    print("=" * 60)
    print("SEARCH SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Sample document collection
    documents = [
        {
            "doc_id": "CS101",
            "title": "Introduction to Computer Science",
            "text": "Computer science fundamentals including programming, algorithms, and data structures",
            "date": "2024-01-15"
        },
        {
            "doc_id": "DS201", 
            "title": "Data Science Fundamentals",
            "text": "Learn data analysis, machine learning, and statistical methods for data science",
            "date": "2024-02-20"
        },
        {
            "doc_id": "ML301",
            "title": "Machine Learning Algorithms",
            "text": "Advanced machine learning techniques including neural networks and deep learning",
            "date": "2024-03-10"
        },
        {
            "doc_id": "DB401",
            "title": "Database Management Systems",
            "text": "Database design, SQL, and data management for large-scale applications",
            "date": "2024-01-30"
        },
        {
            "doc_id": "AI501",
            "title": "Artificial Intelligence Methods",
            "text": "AI algorithms, machine learning, and intelligent system design principles",
            "date": "2024-03-25"
        }
    ]
    
    # Demonstrate different search scenarios
    search_scenarios = [
        {"query": ["data", "science"], "description": "Data Science related courses"},
        {"query": ["machine", "learning"], "description": "Machine Learning courses"},
        {"query": ["algorithms"], "description": "Algorithm-focused courses"},
        {"query": ["database", "management"], "description": "Database courses"}
    ]
    
    for i, scenario in enumerate(search_scenarios, 1):
        print(f"{i}. Searching for: {scenario['description']}")
        print(f"   Query terms: {scenario['query']}")
        print("-" * 50)
        
        results = filter_sort_paginate_results(
            results=documents,
            query_terms=scenario['query'],
            page=1,
            per_page=3,
            sort_by="score",
            min_score=1.0
        )
        
        print(f"Found {results['total_results']} results:")
        
        for doc in results['results']:
            title = highlight_query_terms(doc['title'], scenario['query'])
            text_snippet = truncate_snippet(doc['text'], 60)
            highlighted_text = highlight_query_terms(text_snippet, scenario['query'])
            
            print(f"  📄 {title} (Score: {doc['score']})")
            print(f"     {highlighted_text}")
            print(f"     Course ID: {doc['doc_id']} | Date: {doc['date']}")
            print()
        
        if results['total_results'] == 0:
            print("  No results found matching the criteria.")
            print()


def demo_data_validation():
    """Demonstrate data validation and formatting"""
    print("=" * 60)
    print("DATA VALIDATION DEMONSTRATION")
    print("=" * 60)
    
    # Information validation
    print("1. Information Validation")
    print("-" * 30)
    test_data = [
        ("John   ,  Doe", "123   Main   Street"),
        ("Alice Smith", "456 Oak Avenue"),
        ("Bob  Johnson,", "789 Pine Road"),
        ("", "Invalid Address"),  # This will cause an error
    ]
    
    for name, address in test_data:
        try:
            validated = validate_information(name, address)
            print(f"Input: '{name}' | '{address}'")
            print(f"   Output: {validated}")
        except ValueError as e:
            print(f"Input: '{name}' | '{address}'")
            print(f"   Error: {e}")
        print()
    
    # Query formatting
    print("2. Query Formatting")
    print("-" * 30)
    people = [
        ("  Alice  Johnson  ", 25, "United States"),
        ("Bob Smith", 30, "Canada"),
        ("   Carol   Davis   ", 28, "United Kingdom")
    ]
    
    for name, age, country in people:
        formatted = format_query(name, age, country)
        print(f"Person: {formatted}")
    print()
    
    # Distance calculations
    print("3. Distance Calculations")
    print("-" * 30)
    distance_pairs = [
        (100, 25),
        (200, 150), 
        (75, 30),
        (-10, 50),  # This will cause an error
    ]
    
    for d1, d2 in distance_pairs:
        try:
            distance = calculate_user_distance(d1, d2)
            print(f"Distance between {d1} and {d2}: {distance}")
        except ValueError as e:
            print(f"Distance between {d1} and {d2}: {e}")
    print()


def demo_order_processing():
    """Demonstrate order processing system"""
    print("=" * 60)
    print("ORDER PROCESSING DEMONSTRATION")
    print("=" * 60)
    
    # Restaurant menu
    menu = [
        "cheeseburger", "pizza", "salad", "pasta", "chicken sandwich",
        "fries", "onion rings", "ice cream", "apple pie", "soda"
    ]
    
    print("Restaurant Menu:")
    for i, item in enumerate(menu, 1):
        print(f"  {i}. {item.title()}")
    print()
    
    # Individual order processing
    print("1. Individual Order Processing")
    print("-" * 35)
    
    test_orders = [
        "cheeseburger, fries, soda",
        "pizza, salad, ice cream",
        "pasta, chicken sandwich",
        "cheeseburger, tacos, fries",  # tacos not on menu - will cause error
    ]
    
    for order in test_orders:
        try:
            validated_order = parse_user_order(menu, order)
            print(f"Order: {order}")
            print(f"   Validated: {validated_order}")
        except ValueError as e:
            print(f"Order: {order}")
            print(f"   Error: {e}")
        print()
    
    # Multiple order processing
    print("2. Multiple Order Processing")
    print("-" * 35)
    
    order_data = [
        "Alice, cheeseburger, 2",
        "Bob, pizza, 1",
        "Carol, pasta, 3", 
        "David, salad, 1",
        "Eve, chicken sandwich, 2"
    ]
    
    try:
        processed_orders = process_multiple_order_data(order_data)
        print("Processed Orders:")
        print(processed_orders)
    except ValueError as e:
        print(f"Error processing orders: {e}")
    print()


def demo_integrated_example():
    """Demonstrate integrated use of multiple functions"""
    print("=" * 60)
    print("INTEGRATED EXAMPLE: COURSE SEARCH SYSTEM")
    print("=" * 60)
    
    # Course database
    courses = [
        {
            "doc_id": "INST326",
            "title": "Object Oriented Programming for Information Science", 
            "text": "Learn programming fundamentals, data structures, and object-oriented design for information systems",
            "instructor": "Dr. Smith",
            "credits": 3,
            "date": "2024-01-15"
        },
        {
            "doc_id": "INST327",
            "title": "Database Design and Modeling",
            "text": "Database systems, SQL, data modeling, and information architecture for large applications", 
            "instructor": "Prof. Johnson",
            "credits": 3,
            "date": "2024-02-20"
        },
        {
            "doc_id": "INST414",
            "title": "Data Science Methods",
            "text": "Statistical analysis, machine learning, data mining, and visualization techniques for data science",
            "instructor": "Dr. Davis", 
            "credits": 4,
            "date": "2024-03-10"
        }
    ]
    
    # Simulate user search
    print("Student searches for: '  DATA    science   METHODS  '")
    
    # Step 1: Normalize the query
    user_query = "  DATA    science   METHODS  "
    normalized_query = normalize_query(user_query)
    search_terms = normalized_query.split()
    
    print(f"Normalized query: '{normalized_query}'")
    print(f"Search terms: {search_terms}")
    print()
    
    # Step 2: Search and rank courses
    results = filter_sort_paginate_results(
        results=courses,
        query_terms=search_terms,
        page=1,
        per_page=5,
        sort_by="score",
        min_score=1.0
    )
    
    print(f"Found {results['total_results']} matching courses:")
    print()
    
    # Step 3: Display results with highlighting
    for i, course in enumerate(results['results'], 1):
        # Highlight title and description
        highlighted_title = highlight_query_terms(course['title'], search_terms)
        course_description = truncate_snippet(course['text'], 100)
        highlighted_description = highlight_query_terms(course_description, search_terms)
        
        # Format instructor information
        instructor_info = format_query(course['instructor'].replace('Dr. ', '').replace('Prof. ', ''), 
                                     course['credits'], 'Credits')
        
        print(f"Course {i}: {highlighted_title}")
        print(f"   {highlighted_description}")
        print(f"   Instructor: {course['instructor']} | {course['credits']} credits")
        print(f"   Date: {course['date']} | Relevance Score: {course['score']}")
        print()
    
    print("Search completed successfully!")
    print()


def main():
    """Run all demonstrations"""
    print("INST326 Information Retrieval Function Library Demo")
    print("Demonstrating key features and capabilities")
    print()
    
    try:
        demo_text_processing()
        demo_search_system()
        demo_data_validation()
        demo_order_processing()
        demo_integrated_example()
        
        print("=" * 60)
        print("ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("For more information, see:")
        print("   • docs/function_reference.md - Detailed function documentation")
        print("   • docs/usage_examples.md - More usage examples and tutorials")
        print("   • src/ - Source code for all functions")
        
    except Exception as e:
        print(f"Demo encountered an error: {e}")
        print("Please check your installation and try again.")


if __name__ == "__main__":
    main()
