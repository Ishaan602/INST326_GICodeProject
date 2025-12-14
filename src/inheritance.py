"""
Search System Module

This module implements the document system using advanced OOP principles:
- Abstract Base Classes for documents
- Inheritance hierarchy for different types of documents
- Polymorphic behavior for text processing
- Integration with Project 1 function library

Author: Team Member 1
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Set, Any, Optional
from collections import defaultdict, Counter
import re
import math

class AbstractDocument(ABC):
    """Abstract base class for all documents.
    
    Defines the common interface that all document types have to implement.
    Uses polymorphism to allow different documents.
    
    This class enforces the contract that all documents must:
    - Prepare for text to be cleaned and processed
    - Make sure a snippet of text is created and truncated
    - Provides key information about how many times a word appears
    """
    def __init__(self, doc_id, title, content, metadata: Optional[dict] = None):
        """Initialize the abstract search engine.
        
        Args:
            doc_id (str): Unique identifier for the document
            title (str): Human-readable title for the document
            content (str): Shows full document content/text
            metadata (dict, optional): Additional document metadata. Defaults to None.
            
        Raises:
            ValueError: If doc_id, title is empty
        """
        if not doc_id.strip():
            raise ValueError("doc_id has to be a non-empty string.")
        
        if not title.strip():
            raise ValueError("Title has to be a non-empty string.")
        
        if not content.strip():
            raise ValueError("Content has to be a non-empty string.")
        
        self._doc_id = doc_id
        self._title = title
        self._content = content
        self._metadata = metadata if metadata is not None else {}
        self._processed = False

    @property
    def doc_id(self) -> str:
        """Get the document ID.
        
        Returns:
            str: Document unique identifier
        """
        return self._doc_id
    
    @property 
    def title(self) -> str:
        """Get the document title.
        
        Returns:
            str: Document title
        """
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        """Set the document title.
        
        Args:
            value (str): New title for the document
            
        Raises:
            ValueError: If title is empty
            TypeError: If title is not a string
        """
        if not isinstance(value, str):
            raise TypeError("Title has to be a string")
        if not value.strip():
            raise ValueError("Title has to be a non-empty string")
        self._title = value.strip()
    
    @property
    def content(self) -> str:
        """Get the document content.
        
        Returns:
            str: Document content/text
        """
        return self._content
    
    @content.setter
    def content(self, value: str) -> None:
        """Set the document content.
        
        Args:
            value (str): New content for the document
            
        Raises:
            ValueError: If content is empty
            TypeError: If content is not a string
        """
        if not isinstance(value, str):
            raise TypeError("content must be a string")
        if not value.strip():
            raise ValueError("content cannot be empty")
        self._content = value.strip()
    
    @property
    def metadata(self) -> dict:
        """Get the document metadata.
        
        Returns:
            dict: Document metadata dictionary
        """
        return self._metadata.copy()

    @abstractmethod
    def prepare_text(self, text: str) -> str:
        """Prepare/clean text for processing document.

        Args:
            text (str): Raw text
        
        Returns:
            str: Shows prepared text
        """
        pass

    @abstractmethod
    def create_snippet(self, text: str, max_chars: int = 160) -> str:
        """Create a snippet from text.
        
        Args:
            text (str): Raw text
            max_chars (int): Maximum number of characters. Set to 160.
            
        Returns:
            str: Shows snippet of text.
        """
        pass

    @abstractmethod
    def compute_statistics(self) -> Dict[str, Any]:
        """Compute main information of document.
            
        Returns:
            Dict[str, Any]: Shows computed information.
        """
        pass

    def get_word_count(self) -> int:
        """Get the total word count of the document content.
        
        Returns:
            int: Number of words in the document content
            
        Examples:
            >>> doc = Document("1", "Title", "Introduction to Algorithms")
            >>> doc.get_word_count()
            3
        """
        return len(self._content.split())
    
    def add_metadata(self, key: str, value) -> None:
        """Add or update metadata for the document.
        
        Args:
            key (str): Metadata key
            value: Metadata value
            
        Examples:
            >>> doc = Document("1", "Title", "Content")
            >>> doc.add_metadata("author", "Rick Riordan")
            >>> doc.metadata["author"]
            'Rick Riordan'
        """
        self._metadata[key] = value
    
    def __str__(self) -> str:
        content_snippet = self.create_snippet(self._content, 100)
        return f"Document: {self._title}\nContent: {content_snippet}"
    
    def __repr__(self) -> str:
        return f'Document(doc_id="{self._doc_id}", title="{self._title}", content_length={len(self._content)})'


class TextDocument(AbstractDocument):
    """Text document implementation.
    
    Implements text cleaning and shortening text into snippets.
    """
    def __init__(self, doc_id, title, content, metadata: Optional[Dict] = None):
        super().__init__(doc_id, title, content, metadata)
        
    def prepare_text(self, text: str) -> str:
        """Prepare text by converting to lowercase.
        
        Args:
            text (str): Text to prepare
            
        Returns:
            str: Cleaned text in lowercase
        """
        return text.lower()
        
    def create_snippet(self, text: str, max_chars: int = 160) -> str:
        """Create a snippet by truncating text to max_chars.
        
        Args:
            text (str): Text to truncate
            max_chars (int): Maximum characters in snippet
            
        Returns:
            str: Truncated text with ellipsis if needed
        """
        if len(text) <= max_chars:
            return text
        return text[:max_chars].rsplit(' ', 1)[0] + "..."
    
    def count_term_frequency(self, text: str, term: str) -> int:
        """Counts occurrences of a term in the text.
        
        Args:
            text (str): Text to search
            term (str): Term to count
            
        Returns:
            int: Number of occurrences
        """
        clean_text = self.prepare_text(text)
        clean_term = term.lower()
        return clean_text.split().count(clean_term)
    
    def highlight_query_terms(self, text: str, terms: List[str], pre: str = "<b>", post: str = "</b>") -> str:
        """Highlight main query terms in the text.
        
        Args:
            text (str): Text to highlight
            terms (List[str]): Terms to highlight
            pre (str): Opening tag
            post (str): Closing tag
            
        Returns:
            str: Text with highlighted terms
        """
        result = text
        for term in terms:
            pattern = re.compile(re.escape(term))
            result = pattern.sub(f"{pre}{term}{post}", result)
        return result
    
    def compute_statistics(self) -> Dict[str, Any]:
        """Compute statistics for text document.
        
        Returns:
            Dict[str, Any]: Shows statistics including word count, character count, unique words
        """
        words = self._content.split()
        return {
            "word_count": len(words),
            "char_count": len(self._content),
            "unique_words": len(set(w.lower() for w in words)),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0
        }


class IndexedDocument(AbstractDocument):
    """Indexed document with term frequency indexing."""
    
    def __init__(self, doc_id, title, content, metadata: Optional[Dict] = None):
        super().__init__(doc_id, title, content, metadata)
        self._term_index = self._build_index()
    
    def _build_index(self) -> Dict[str, int]:
        """Build term frequency index.
        
        Returns:
            Dict[str, int]: Shows a dictionary 
        """
        words = self.prepare_text(self._content).split()
        return Counter(words)
    
    def prepare_text(self, text: str) -> str:
        """Clean text by converting to lowercase, then splitting it into multiple parts
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Shows cleaned text
        """
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return ' '.join(text.split())
    
    def create_snippet(self, text: str, max_chars: int = 160) -> str:
        """Create snippet with word boundary awareness.
        
        Args:
            text (str): Text to truncate
            max_chars (int): Maximum characters
            
        Returns:
            str: Shows truncated snippet
        """
        if len(text) <= max_chars:
            return text
        truncated = text[:max_chars]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + "..."
    
    def count_term_frequency(self, text: str, term: str) -> int:
        """Count term frequency using the index.
        
        Args:
            text (str): Text to search (ignored, uses index)
            term (str): Term to count
            
        Returns:
            int: Frequency of term
        """
        clean_term = self.prepare_text(term).split()[0] if term else ""
        return self._term_index.get(clean_term, 0)
    
    def highlight_query_terms(self, text: str, terms: List[str], pre: str = "<b>", post: str = "</b>") -> str:
        """Highlight query terms with word boundary matching.
        
        Args:
            text (str): Text to highlight
            terms (List[str]): Terms to highlight
            pre (str): Opening tag
            post (str): Closing tag
            
        Returns:
            str: Highlighted text
        """
        result = text
        for term in terms:
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            result = pattern.sub(f"{pre}\\g<0>{post}", result)
        return result
    
    def compute_statistics(self) -> Dict[str, Any]:
        """Compute statistics including index information.
        
        Returns:
            dict: Statistics with term index info
        """
        return {
            "word_count": sum(self._term_index.values()),
            "unique_terms": len(self._term_index),
            "most_common": self._term_index.most_common(5),
            "index_size": len(self._term_index)
        }


class ProcessedDocument(AbstractDocument):
    """Advanced document with stemming and stopword removal."""
    
    STOPWORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'is', 'was', 'are', 'were', 'be', 'been', 'being'}
    
    def __init__(self, doc_id, title, content, metadata: Optional[Dict] = None):
        super().__init__(doc_id, title, content, metadata)
        self._processed_content = self.prepare_text(self._content)
        self._term_frequencies = Counter(self._processed_content.split())
    
    def prepare_text(self, text: str) -> str:
        """Advanced text cleaning with stopword removal.
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Processed text
        """
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        filtered = [w for w in words if w not in self.STOPWORDS and len(w) > 2]
        return ' '.join(filtered)
    
    def create_snippet(self, text: str, max_chars: int = 160) -> str:
        """Create intelligent snippet with sentence awareness.
        
        Args:
            text (str): Text to truncate
            max_chars (int): Maximum characters
            
        Returns:
            str: Snippet with complete sentences when possible
        """
        if len(text) <= max_chars:
            return text
        
        truncated = text[:max_chars]
        sentence_end = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
        
        if sentence_end > max_chars * 0.5:
            return truncated[:sentence_end + 1]
        
        last_space = truncated.rfind(' ')
        if last_space > 0:
            return truncated[:last_space] + "..."
        return truncated + "..."
    
    def count_term_frequency(self, text: str, term: str) -> int:
        """Count term frequency in processed content.
        
        Args:
            text (str): Text to search
            term (str): Term to count
            
        Returns:
            int: Frequency of processed term
        """
        processed_term = self.prepare_text(term).split()
        if not processed_term:
            return 0
        return self._term_frequencies.get(processed_term[0], 0)
    
    def highlight_query_terms(self, text: str, terms: List[str], pre: str = "<b>", post: str = "</b>") -> str:
        """Highlight terms with context preservation.
        
        Args:
            text (str): Text to highlight
            terms (List[str]): Terms to highlight
            pre (str): Opening tag
            post (str): Closing tag
            
        Returns:
            str: Highlighted text
        """
        result = text
        for term in terms:
            if term.lower() not in self.STOPWORDS:
                pattern = re.compile(r'\b' + re.escape(term) + r'\b')
                result = pattern.sub(f"{pre}\\g<0>{post}", result)
        return result
    
    def compute_statistics(self) -> Dict[str, Any]:
        """Compute advanced statistics.
        
        Returns:
            Dict[str, Any]: Comprehensive document statistics
        """
        original_words = self._content.split()
        processed_words = self._processed_content.split()
        
        return {
            "original_word_count": len(original_words),
            "processed_word_count": len(processed_words),
            "unique_terms": len(self._term_frequencies),
            "stopwords_removed": len(original_words) - len(processed_words),
            "top_terms": self._term_frequencies.most_common(10),
            "avg_term_length": sum(len(w) for w in processed_words) / len(processed_words) if processed_words else 0
        }

# Tests
if __name__ == "__main__":
    print("=== Document System Module Demo ===\n")
    
    # Test data
    test_documents = [
        {
            "doc_id": "1",
            "title": "Algorithms Guide",
            "text": "Guide to learning all about algorithms"
        },
        {
            "doc_id": "2", 
            "title": "Networks Guide",
            "text": "Guide to learning all about networks"
        },
        {
            "doc_id": "3",
            "title": "Python Guide",
            "text": "Guide to learning all about the inner workings of Python"
        },
        {
            "doc_id": "4",
            "title": "Information Technology Guide",
            "text": "Guide to learning all about information technology"
        }
    ]
    
    # 1. Test Abstract Base Class enforcement
    print("1. Testing Abstract Base Class Enforcement:")
    try:
        # Trying to instantiate the abstract base class directly will fail
        abstract_document = AbstractDocument(doc_id="12", title="Title", content="Content")
    except TypeError as e:
        print(f"✓ Cannot instantiate abstract class: {type(e).__name__}")
    
    print()
    
    # 2. Test Polymorphic Behavior with different document types
    print("2. Testing Polymorphic Document Behavior:")

    # Create instances of different document types
    text_doc = TextDocument(doc_id="1", title="Text Document Example", content="This is an example of a text document.")
    indexed_doc = IndexedDocument(doc_id="2", title="Indexed Document Example", content="This is an example of an indexed document.")
    processed_doc = ProcessedDocument(doc_id="3", title="Processed Document Example", content="This is an example of a processed document with stopwords removed.")

    documents = [text_doc, indexed_doc, processed_doc]
    
    # Test polymorphic behavior of each document type
    for doc in documents:
        print(f"{doc.__class__.__name__} - Title: {doc.title}")
        
        # Get word count
        print(f"  Word Count: {doc.get_word_count()}")
        
        # Create snippet
        snippet = doc.create_snippet(doc.content, max_chars=50)
        print(f"  Snippet: {snippet}")
        
        # Compute statistics
        stats = doc.compute_statistics()
        print(f"  Statistics: {stats}")
        
        print()
    
    # 3. Test Inheritance Hierarchy
    print("3. Testing Inheritance Hierarchy:")
    
    # Test if all document types are instances of AbstractDocument
    for doc in documents:
        is_abstract_subclass = isinstance(doc, AbstractDocument)
        print(f"{doc.__class__.__name__} IS-A AbstractDocument: {is_abstract_subclass}")
    
    print()
    
    # 4. Test Metadata Integration
    print("4. Testing Metadata Integration:")

    # Add and retrieve metadata
    processed_doc.add_metadata("author", "J.D. Salinger")
    processed_doc.add_metadata("published_date", "2023-10-21")
    print(f"Processed Document Metadata: {processed_doc.metadata}")
    
    # Update metadata
    processed_doc.add_metadata("author", "Suzanne Collins")
    print(f"Updated Metadata: {processed_doc.metadata}")
    
    print()
    
    # 5. Demonstrate Document Snippet Customization
    print("5. Demonstrating Document Snippet Customization:")

    # Customize snippet length for different documents
    for doc in documents:
        custom_snippet = doc.create_snippet(doc.content, max_chars=30)
        print(f"{doc.__class__.__name__} - Custom Snippet: {custom_snippet}")
    
    print()
    
    # 6. Test Term Frequency Counting
    print("6. Testing Term Frequency Counting:")

    # Test term frequency counting for IndexedDocument and ProcessedDocument
    indexed_term_freq = indexed_doc.count_term_frequency(indexed_doc.content, "example")
    print(f"Term Frequency ('example') in IndexedDocument: {indexed_term_freq}")
    
    processed_term_freq = processed_doc.count_term_frequency(processed_doc.content, "processed")
    print(f"Term Frequency ('processed') in ProcessedDocument: {processed_term_freq}")
    
    print()
    
    print("=== Document System Module Demo Complete ===")
    print("\nFeatures Implemented:")
    print("✓ Abstract Base Class (AbstractDocument) using ABC module")
    print("✓ Inheritance Hierarchy: AbstractDocument → TextDocument / IndexedDocument / ProcessedDocument")
    print("✓ Polymorphic Methods: get_word_count(), create_snippet(), compute_statistics()")
    print("✓ Metadata Management: Add/Update metadata using add_metadata()")
    print("✓ Advanced Text Processing: Stopwords removal and term frequency counting")
    print("✓ Customizable snippet generation based on character limits")
    print("✓ Functionality tested on different document types with varied behavior")

