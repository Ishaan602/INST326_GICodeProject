# Search System Architecture Documentation - Team Member 2

## Overview

This document explains the design and implementation of the Search System module, which demonstrates advanced Object-Oriented Programming principles including inheritance hierarchies, polymorphism, abstract base classes, and integration with the existing function library.

## Design Principles Applied

### 1. Abstract Base Classes (ABC Module)

#### AbstractSearchEngine
```python
from abc import ABC, abstractmethod

class AbstractSearchEngine(ABC):
    @abstractmethod
    def process_query(self, query: str) -> Dict[str, Any]:
        """Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def execute_search(self, processed_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def validate_search_capability(self) -> bool:
        """Must be implemented by subclasses."""
        pass
```

**Purpose & Benefits:**
- **Interface Enforcement**: Cannot instantiate incomplete subclasses
- **Contract Definition**: All search engines must implement core methods
- **Polymorphism Foundation**: Enables uniform treatment of different engine types
- **Development Guidance**: Clear indication of required implementation

### 2. Inheritance Hierarchy

#### Class Structure
```
AbstractSearchEngine (ABC)
├── BooleanSearchEngine    (exact matching with inverted indices)
├── RankedSearchEngine     (relevance scoring with term frequency)
└── SemanticSearchEngine   (similarity-based semantic matching)
```

#### Design Rationale

**Why Inheritance Here?**
- True "is-a" relationships: BooleanSearchEngine IS-A AbstractSearchEngine
- Shared common behavior (document management, search orchestration)
- Need for specialized search algorithms while maintaining common interface
- Code reuse for common functionality (history tracking, validation)

**Inherited Functionality:**
- Document collection management (`add_document()`, `get_documents()`)
- Search history tracking (`get_search_history()`, `clear_history()`)
- Basic properties (`engine_id`, `name`, `document_count`)
- Template method pattern in `search()` method

### 3. Polymorphic Behavior

Each engine type implements the same interface but with specialized behavior:

#### BooleanSearchEngine.process_query()
```python
def process_query(self, query: str) -> Dict[str, Any]:
    normalized = normalize_query(query)  # Function library integration
    return {
        'type': 'boolean',
        'normalized': normalized,
        'terms': normalized.split(),
        'operator': 'AND'  # Boolean-specific: exact matching
    }
```

#### RankedSearchEngine.process_query()
```python
def process_query(self, query: str) -> Dict[str, Any]:
    normalized = normalize_query(query)  # Function library integration
    terms = normalized.split()
    return {
        'type': 'ranked',
        'normalized': normalized,
        'terms': terms,
        'term_weights': {term: 1.0 for term in terms},  # Ranked-specific: weighting
        'scoring_method': self._scoring_method
    }
```

#### SemanticSearchEngine.process_query()
```python
def process_query(self, query: str) -> Dict[str, Any]:
    normalized = normalize_query(query)  # Function library integration
    terms = normalized.split()
    return {
        'type': 'semantic',
        'normalized': normalized,
        'terms': terms,
        'semantic_features': {  # Semantic-specific: meaning analysis
            'query_complexity': 'simple' if len(terms) <= 2 else 'complex',
            'has_technical_terms': any(term in ['algorithm', 'data'] for term in terms)
        }
    }
```

### 4. Function Library Integration

Each engine integrates different functions from `library_name.py`:

#### BooleanSearchEngine Functions:
- `normalize_query()` - Query preprocessing
- `build_inverted_index()` - Index construction
- `boolean_retrieval()` - Exact term matching

#### RankedSearchEngine Functions:
- `normalize_query()` - Query preprocessing  
- `rank_documents()` - Relevance scoring
- `filter_sort_paginate_results()` - Result pagination

#### SemanticSearchEngine Functions:
- `normalize_query()` - Query preprocessing
- `semantic_search()` - Similarity matching

## Polymorphism in Action

### Template Method Pattern
The base class `search()` method orchestrates the search process while delegating specialized behavior to subclasses:

```python
def search(self, query: str, **kwargs) -> Dict[str, Any]:
    # Step 1: Validate (polymorphic)
    if not self.validate_search_capability():
        raise RuntimeError("Engine not ready")
    
    # Step 2: Process query (polymorphic)
    processed_query = self.process_query(query)
    
    # Step 3: Execute search (polymorphic)
    raw_results = self.execute_search(processed_query)
    
    # Step 4: Package results (common behavior)
    return self._package_results(processed_query, raw_results)
```

### Uniform Interface Usage
```python
def search_all_engines(engines: List[AbstractSearchEngine], query: str):
    """Demonstrates polymorphic usage - same interface, different behavior"""
    results = []
    for engine in engines:
        if engine.validate_search_capability():  # Polymorphic validation
            result = engine.search(query)  # Polymorphic search execution
            results.append(result)
    return results
```

## Specialized Features

### BooleanSearchEngine Specialization
- **Inverted Index**: Builds and maintains term-to-document mappings
- **Exact Matching**: Binary relevance (match or no match)
- **Index Statistics**: Provides detailed indexing metrics
- **AND Logic**: All terms must be present

### RankedSearchEngine Specialization
- **Relevance Scoring**: Uses term frequency for ranking
- **Pagination Support**: Integrates with pagination functions
- **Configurable Scoring**: Supports different scoring methods
- **Result Ordering**: Sorts by relevance scores

### SemanticSearchEngine Specialization
- **Similarity Thresholds**: Configurable minimum similarity
- **Semantic Analysis**: Query intent and complexity analysis
- **Meaning-based Matching**: Beyond exact term matching
- **Threshold Filtering**: Only returns sufficiently similar results

## Factory Pattern Implementation

```python
class SearchEngineFactory:
    @staticmethod
    def create_engine(engine_type: str, engine_id: str, name: str, **kwargs) -> AbstractSearchEngine:
        if engine_type.lower() == 'boolean':
            return BooleanSearchEngine(engine_id, name)
        elif engine_type.lower() == 'ranked':
            scoring_method = kwargs.get('scoring_method', 'tf')
            return RankedSearchEngine(engine_id, name, scoring_method)
        elif engine_type.lower() == 'semantic':
            threshold = kwargs.get('similarity_threshold', 0.1)
            return SemanticSearchEngine(engine_id, name, threshold)
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")
```

**Benefits:**
- **Centralized Creation**: Single point for engine instantiation
- **Configuration Management**: Handles engine-specific parameters
- **Type Safety**: Validates engine types
- **Extensibility**: Easy to add new engine types

## Testing Strategy

### Abstract Base Class Tests
- Verify cannot instantiate abstract class directly
- Ensure incomplete implementations raise TypeError
- Validate interface contracts are enforced

### Inheritance Tests
- Confirm all engines inherit from AbstractSearchEngine
- Verify proper super() calls in constructors
- Test inherited method availability

### Polymorphism Tests
- Same method calls produce different behavior
- Uniform interface works across all engine types
- Specialized features work correctly

### Integration Tests
- Function library integration works correctly
- Mock testing for external dependencies
- End-to-end search workflow testing

## Performance Considerations

### BooleanSearchEngine
- **Index Building**: O(n*m) where n=documents, m=average document length
- **Search Time**: O(k) where k=number of query terms
- **Memory Usage**: O(vocabulary_size * average_postings_per_term)

### RankedSearchEngine  
- **Ranking Time**: O(n*m) for scoring all documents
- **Sorting Time**: O(n log n) for result ordering
- **Memory Usage**: O(n) for storing scores

### SemanticSearchEngine
- **Similarity Computation**: Depends on semantic model complexity
- **Threshold Filtering**: O(n) for result filtering
- **Memory Usage**: O(n) plus semantic model requirements

## Extension Points

### Adding New Engine Types
1. Create new class inheriting from AbstractSearchEngine
2. Implement all abstract methods with specialized behavior
3. Add to SearchEngineFactory
4. Create corresponding tests
5. Update documentation

### Adding New Search Features
1. Add methods to base class (if common) or specific engines
2. Ensure backward compatibility
3. Update tests and documentation
4. Consider function library integration opportunities

## Conclusion

The Search System module successfully demonstrates:

✅ **Abstract Base Classes**: Enforces interfaces with ABC module  
✅ **Inheritance Hierarchy**: Logical "is-a" relationships with 2-3 levels  
✅ **Polymorphism**: Same methods, different specialized behaviors  
✅ **Function Integration**: All assigned functions properly integrated  
✅ **Method Overriding**: Proper use of super() calls  
✅ **Encapsulation**: Private attributes with controlled access  
✅ **Factory Pattern**: Centralized object creation  
✅ **Comprehensive Testing**: Full test coverage for all OOP concepts  

The design enables easy extension, maintains clean separation of concerns, and provides a solid foundation for building sophisticated search systems.
