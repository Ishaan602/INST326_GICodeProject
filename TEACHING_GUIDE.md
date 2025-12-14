# Teaching Guide: Search and Order Management System

## Educational Objectives

This project serves as a comprehensive example of software engineering principles and object-oriented programming concepts. It demonstrates the progression from basic functions to a complete integrated system.

## Learning Outcomes

By studying this project, students will understand:

### 1. Object-Oriented Programming Concepts
- **Encapsulation**: Data and methods bundled in classes
- **Inheritance**: Shared functionality through class hierarchies
- **Polymorphism**: Same interface, different implementations
- **Abstraction**: Abstract base classes defining interfaces

### 2. Software Design Patterns
- **Abstract Base Classes**: Interface enforcement
- **Composition**: Building complex objects from simpler ones
- **Factory Pattern**: Creating objects without specifying exact classes
- **Strategy Pattern**: Interchangeable algorithms (search engines)

### 3. System Integration
- **Component Architecture**: How parts work together
- **Data Flow**: Information movement through the system
- **Error Handling**: Graceful failure and recovery
- **State Management**: Persistent data between sessions

### 4. Software Engineering Practices
- **Testing**: Unit, integration, and end-to-end testing
- **Documentation**: Technical and user documentation
- **Code Organization**: Modular structure and clear interfaces
- **Version Control**: Project evolution and collaboration

## Pedagogical Progression

### Stage 1: Functions (Project 1)
**Concepts Introduced:**
- Function definition and calling
- Parameter passing and return values
- String manipulation and text processing
- List operations and data structures

**Key Learning:**
```python
def normalize_query(query: str) -> str:
    """Basic function with clear input/output."""
    return query.lower().strip()
```

### Stage 2: Classes (Project 2) 
**Concepts Introduced:**
- Class definition and instantiation
- Instance methods and attributes
- Encapsulation of related functionality
- Method chaining and object interaction

**Key Learning:**
```python
class Document:
    def __init__(self, doc_id: str, title: str, content: str):
        self.id = doc_id
        self.title = title
        self.content = content
    
    def get_word_count(self) -> int:
        """Method encapsulates functionality."""
        return len(self.content.split())
```

### Stage 3: Advanced OOP (Project 3)
**Concepts Introduced:**
- Abstract base classes and interfaces
- Inheritance hierarchies
- Polymorphic method calls
- Design by contract

**Key Learning:**
```python
class AbstractSearchEngine(ABC):
    @abstractmethod
    def search(self, query: SearchQuery, documents: List[Document]) -> List[Document]:
        """Interface definition enforces implementation."""
        pass

class BooleanSearchEngine(AbstractSearchEngine):
    def search(self, query: SearchQuery, documents: List[Document]) -> List[Document]:
        """Polymorphic implementation."""
        # Boolean search logic
        return results
```

### Stage 4: System Integration (Project 4)
**Concepts Introduced:**
- Application architecture
- Data persistence and I/O
- Error handling strategies
- System testing and validation

**Key Learning:**
```python
class SearchOrderSystem:
    def __init__(self, data_dir: str = "data"):
        """System orchestrates all components."""
        self.search_engines = {
            'boolean': BooleanSearchEngine(),
            'ranked': RankedSearchEngine(),
            'semantic': SemanticSearchEngine()
        }
        self.load_system_state()
```

## Teaching Applications

### 1. Classroom Examples

#### Demonstrating Inheritance
```python
# Show how all search engines share the same interface
engines = [BooleanSearchEngine(), RankedSearchEngine(), SemanticSearchEngine()]

for engine in engines:
    # Polymorphic call - same method, different behavior
    results = engine.search(query, documents)
    print(f"{engine.__class__.__name__}: {len(results)} results")
```

#### Explaining Composition
```python
# System is composed of multiple components
class SearchOrderSystem:
    def __init__(self):
        self.documents = {}  # HAS documents
        self.users = {}      # HAS users  
        self.orders = []     # HAS orders
        self.engines = {}    # HAS search engines
```

### 2. Lab Exercises

#### Exercise 1: Add New Search Engine
Students implement a new search engine by inheriting from `AbstractSearchEngine`:

```python
class ExactMatchEngine(AbstractSearchEngine):
    def search(self, query: SearchQuery, documents: List[Document]) -> List[Document]:
        # Student implements exact string matching
        pass
```

#### Exercise 2: Add New Import Format
Students add support for a new data format:

```python
def import_documents_yaml(self, yaml_file: str) -> None:
    # Student implements YAML import
    pass
```

#### Exercise 3: Extend User Management
Students add new user features:

```python
class UserProfile:
    def add_favorite_document(self, doc_id: str) -> None:
        # Student implements favorites functionality
        pass
```

### 3. Assessment Ideas

#### Code Analysis Questions
1. "Explain how polymorphism is demonstrated in the search engine hierarchy."
2. "Describe the composition relationships in the SearchOrderSystem class."
3. "Analyze the error handling strategy used in the import methods."

#### Design Questions
1. "How would you add support for user authentication?"
2. "Design a caching system for frequently accessed documents."
3. "Propose a solution for handling very large document collections."

#### Implementation Challenges
1. "Add a new report type that shows search trends over time."
2. "Implement a recommendation system based on user search history."
3. "Create a web API interface for the search system."

## Code Quality Examples

### Good Practices Demonstrated

#### 1. Clear Documentation
```python
def search_documents(self, query: str, engine_type: str = 'ranked', 
                    user_id: Optional[str] = None) -> List[Document]:
    """
    Search documents using specified search engine.
    
    Args:
        query: Search terms to find
        engine_type: Type of search engine ('boolean', 'ranked', 'semantic')
        user_id: Optional user ID for tracking search history
        
    Returns:
        List of Document objects ordered by relevance
        
    Raises:
        ValueError: If engine_type is not supported
    """
```

#### 2. Error Handling
```python
try:
    self.import_documents_csv(csv_file)
except FileNotFoundError:
    print(f"CSV file not found: {csv_file}")
    raise
except Exception as e:
    print(f"Error importing CSV: {e}")
    raise
```

#### 3. Type Hints
```python
def export_search_results(self, results: List[Document], 
                         filename: str, format: str = 'json') -> None:
    """Type hints make code self-documenting."""
```

#### 4. Context Managers
```python
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # File automatically closed
```

## Common Student Mistakes

### 1. Inheritance Confusion
**Mistake**: Implementing functionality in abstract base class
```python
class AbstractSearchEngine(ABC):
    def search(self, query, documents):
        # Wrong: implementing in abstract class
        return []
```

**Correction**: Keep abstract classes truly abstract
```python
class AbstractSearchEngine(ABC):
    @abstractmethod
    def search(self, query: SearchQuery, documents: List[Document]) -> List[Document]:
        pass  # Force implementation in subclasses
```

### 2. Poor Error Handling
**Mistake**: Ignoring exceptions
```python
def import_csv(self, filename):
    # Wrong: no error handling
    with open(filename, 'r') as f:
        # Process file
```

**Correction**: Comprehensive error handling
```python
def import_csv(self, filename):
    try:
        with open(filename, 'r') as f:
            # Process file
    except FileNotFoundError:
        print(f"File not found: {filename}")
        raise
    except Exception as e:
        print(f"Error processing file: {e}")
        raise
```

### 3. Missing Type Hints
**Mistake**: No type information
```python
def search(self, query, documents):
    # Unclear what types are expected
```

**Correction**: Clear type hints
```python
def search(self, query: SearchQuery, documents: List[Document]) -> List[Document]:
    # Types make interface clear
```

## Extension Projects

### Beginner Level
1. Add new document fields (author, date, category)
2. Implement simple document tagging system
3. Create basic user preferences storage

### Intermediate Level
1. Add full-text search with highlighting
2. Implement document similarity recommendations
3. Create batch import/export operations

### Advanced Level
1. Add web interface with Flask/Django
2. Implement machine learning document classification
3. Create distributed search across multiple systems

## Assessment Rubric

### Code Quality (40%)
- Clear, readable code with good naming conventions
- Proper use of type hints and documentation
- Appropriate error handling and validation
- Following Python best practices

### OOP Concepts (30%)
- Correct use of inheritance and polymorphism
- Proper abstraction and encapsulation
- Appropriate use of composition
- Understanding of design patterns

### Functionality (20%)
- System works as specified
- All major features implemented
- Edge cases handled appropriately
- Good user experience

### Testing & Documentation (10%)
- Comprehensive test coverage
- Clear documentation
- Good code organization
- Professional presentation

This teaching guide helps instructors use the project effectively to demonstrate key computer science and software engineering concepts while providing students with hands-on experience building real systems.
