"""
INST326 Information Retrieval Function Library
"""
# Import main functions for easy access
from .library_name import (
    filter_sort_paginate_results,
    highlight_query_terms,
    normalize_query,
    truncate_snippet,
    count_term_frequency,
    clean_text,
    build_inverted_index,
    boolean_retrieval,
    rank_documents,
    semantic_search
)

from .utils import (
    validate_information,
    format_query,
    calculate_user_distance,
    parse_user_order,
    process_multiple_order_data
)

__all__ = [
    'filter_sort_paginate_results',
    'highlight_query_terms', 
    'normalize_query',
    'truncate_snippet',
    'count_term_frequency',
    'clean_text',
    'build_inverted_index',
    'boolean_retrieval',
    'rank_documents',
    'semantic_search',
    'validate_information',
    'format_query',
    'calculate_user_distance',
    'parse_user_order',
    'process_multiple_order_data'
]
