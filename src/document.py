"""
Document Class Module

This module contains the Document class for representing and managing individual
documents in an information retrieval system. The class encapsulates document
data and provides methods for text processing and analysis.
"""

import re
from typing import List, Optional


class Document:
    """Represents a document in an information retrieval system.
    
    This class encapsulates document data and provides methods for text processing,
    analysis, and manipulation. It integrates functionality for cleaning text,
    creating snippets, counting term frequencies, and highlighting query terms.
    
    Attributes:
        _doc_id (str): Unique identifier for the document
        _title (str): Document title
        _content (str): Full document content/text
        _metadata (dict): Additional document metadata
    
    Examples:
        >>> doc = Document("1", "Data Mining Guide", "Introduction to data mining techniques")
        >>> doc.title
        'Data Mining Guide'
        >>> doc.clean_content()
        'introduction to data mining techniques'
    """
    
    def __init__(self, doc_id: str, title: str, content: str, metadata: Optional[dict] = None):
        """Initialize a Document instance.
        
        Args:
            doc_id (str): Unique identifier for the document
            title (str): Document title
            content (str): Full document content/text
            metadata (dict, optional): Additional document metadata. Defaults to None.
            
        Raises:
            ValueError: If doc_id, title, or content are empty strings
            TypeError: If doc_id, title, or content are not strings
            
        Examples:
            >>> doc = Document("1", "AI Guide", "Machine learning basics")
            >>> doc.doc_id
            '1'
            >>> doc = Document("2", "Python Tutorial", "Learn Python", {"author": "Jane"})
            >>> doc.metadata["author"]
            'Jane'
        """
        # Parameter validation
        if not isinstance(doc_id, str):
            raise TypeError("doc_id must be a string")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not isinstance(content, str):
            raise TypeError("content must be a string")
            
        if not doc_id.strip():
            raise ValueError("doc_id cannot be empty")
        if not title.strip():
            raise ValueError("title cannot be empty")
        if not content.strip():
            raise ValueError("content cannot be empty")
            
        # Initialize private attributes
        self._doc_id = doc_id.strip()
        self._title = title.strip()
        self._content = content.strip()
        self._metadata = metadata if metadata is not None else {}
    
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
            raise TypeError("title must be a string")
        if not value.strip():
            raise ValueError("title cannot be empty")
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
        return self._metadata.copy()  # Return copy to prevent external modification
    
    def clean_content(self) -> str:
        """Clean and normalize the document content by converting to lowercase.
        
        Integrates the clean_text() function to provide standardized text processing
        for search and analysis operations.
        
        Returns:
            str: Lowercase version of the document content
            
        Examples:
            >>> doc = Document("1", "Title", "Hello WORLD!")
            >>> doc.clean_content()
            'hello world!'
        """
        return self._content.lower()
    
    def create_snippet(self, max_chars: int = 160) -> str:
        """Create a truncated snippet of the document content.
        
        Integrates the truncate_snippet() function to create preview text that
        respects word boundaries and adds ellipsis when truncated.
        
        Args:
            max_chars (int, optional): Maximum characters in snippet. Defaults to 160.
            
        Returns:
            str: Truncated content snippet with ellipsis if needed
            
        Examples:
            >>> doc = Document("1", "Title", "This is a very long document content")
            >>> doc.create_snippet(20)
            'This is a very long…'
        """
        if len(self._content) <= max_chars:
            return self._content
        
        # Find the last space within the character limit
        truncated = self._content[:max_chars]
        
        # Find the last word boundary
        last_space = truncated.rfind(' ')
        
        if last_space == -1:
            # No space found, truncate at character limit
            return truncated + "…"
        else:
            # Truncate at last word boundary
            return truncated[:last_space] + "…"
    
    def count_term_occurrences(self, term: str) -> int:
        """Count occurrences of a specific term in the document content.
        
        Integrates the count_term_frequency() function to perform case-insensitive
        whole-word matching for term frequency analysis.
        
        Args:
            term (str): The term to count occurrences of
            
        Returns:
            int: Number of times the term appears as a complete word
            
        Examples:
            >>> doc = Document("1", "Mining Guide", "Data mining is about mining data")
            >>> doc.count_term_occurrences("mining")
            2
            >>> doc.count_term_occurrences("data")
            2
        """
        # Split text into words and count matches
        words = self._content.lower().split()
        count = 0
        
        for word in words:
            # Remove punctuation from word for comparison
            clean_word = word.strip('.,!?;:"()[]{}')
            if clean_word == term.lower():
                count += 1
        
        return count
    
    def highlight_terms(self, terms: List[str], pre: str = "<b>", post: str = "</b>") -> str:
        """Highlight query terms in the document content.
        
        Integrates the highlight_query_terms() function to wrap matching terms
        with specified tags for display purposes.
        
        Args:
            terms (List[str]): List of terms to highlight
            pre (str, optional): Opening tag/text. Defaults to "<b>".
            post (str, optional): Closing tag/text. Defaults to "</b>".
            
        Returns:
            str: Content with matching terms highlighted
            
        Examples:
            >>> doc = Document("1", "Guide", "Learn data mining techniques")
            >>> doc.highlight_terms(["data", "mining"])
            'Learn <b>data</b> <b>mining</b> techniques'
        """
        # Create a copy of the content to modify
        result_text = self._content
        
        # Sort terms by length (longest first) to avoid partial replacements
        sorted_terms = sorted(terms, key=len, reverse=True)
        
        for term in sorted_terms:
            # Simple case-insensitive replacement
            # Split text into words, check each word, and replace if it matches
            words = result_text.split()
            new_words = []
            
            for word in words:
                # Remove punctuation for comparison but keep original word
                clean_word = word.strip('.,!?;:"()[]{}').lower()
                if clean_word == term.lower():
                    # Replace the original word with highlighted version
                    highlighted = word.replace(clean_word.title(), f"{pre}{clean_word.title()}{post}")
                    highlighted = highlighted.replace(clean_word.upper(), f"{pre}{clean_word.upper()}{post}")
                    highlighted = highlighted.replace(clean_word, f"{pre}{clean_word}{post}")
                    new_words.append(highlighted)
                else:
                    new_words.append(word)
            
            result_text = ' '.join(new_words)
        
        return result_text
    
    def get_word_count(self) -> int:
        """Get the total word count of the document content.
        
        Returns:
            int: Number of words in the document content
            
        Examples:
            >>> doc = Document("1", "Title", "Hello world test")
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
            >>> doc.add_metadata("author", "John Doe")
            >>> doc.metadata["author"]
            'John Doe'
        """
        self._metadata[key] = value
    
    def __str__(self) -> str:
        """Return a human-readable string representation of the document.
        
        Returns:
            str: Formatted string showing document title and snippet
            
        Examples:
            >>> doc = Document("1", "Data Mining", "Introduction to data mining")
            >>> str(doc)
            'Document: Data Mining\\nContent: Introduction to data mining'
        """
        snippet = self.create_snippet(100)
        return f"Document: {self._title}\nContent: {snippet}"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging.
        
        Returns:
            str: Detailed representation with all key attributes
            
        Examples:
            >>> doc = Document("1", "Title", "Content")
            >>> repr(doc)
            'Document(doc_id="1", title="Title", content_length=7)'
        """
        return f'Document(doc_id="{self._doc_id}", title="{self._title}", content_length={len(self._content)})'
