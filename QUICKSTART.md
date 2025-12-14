# Quick Start Guide

Welcome to the Search and Order Management System! This guide will get you up and running in minutes.

## Prerequisites
- Python 3.8 or higher
- No additional packages required (uses standard library only)

## 🚀 Quick Setup (30 seconds)

1. **Download and navigate to the project**:
```bash
cd INST326_GICodeProject
```

2. **Import sample data**:
```bash
python main.py --import-csv data/sample_documents.csv
```

3. **Run your first search**:
```bash
python main.py --search "Python programming" --engine ranked
```

## 🎯 Try These Examples

### Search Examples
```bash
# Boolean search with exact terms
python main.py --search "data science" --engine boolean

# Ranked search with relevance scoring  
python main.py --search "machine learning" --engine ranked

# Semantic search for similar concepts
python main.py --search "programming tutorial" --engine semantic
```

### User Tracking
```bash
# Search with user history tracking
python main.py --search "Python" --user-id "student123" --engine ranked
```

### Export Results
```bash
# Search and export to JSON
python main.py --search "food" --export food_results.json

# Export to CSV
python main.py --search "programming" --export prog_results.csv --export-format csv
```

### System Reports
```bash
# Get system summary
python main.py --report summary

# View user activity
python main.py --report user_activity

# See popular searches
python main.py --report popular_searches
```

### Interactive Mode
```bash
# Launch interactive session
python main.py --interactive
```

## 🧪 Run Tests
```bash
# Run comprehensive test suite
python tests/test_project4.py

# Test search system
python tests/test_search_system.py
```

## 📁 Sample Data Included
- `data/sample_documents.csv`: Programming and food-related documents
- `data/sample_documents.xml`: Additional sample documents

## 🆘 Need Help?
- Check `README.md` for complete documentation
- See `docs/TECHNICAL_DOCUMENTATION.md` for architecture details
- Review test files for usage examples

## Next Steps
1. Try the interactive mode: `python main.py --interactive`
2. Import your own data (CSV or XML format)
3. Explore the different search engines
4. Check out the API usage in the main README

Happy searching! 🔍
