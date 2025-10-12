import re
import math
from collections import defaultdict, Counter
from typing import List, Dict, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text: str) -> str:
    text = text.lower()
    return text


def build_inverted_index(documents: List[str]) -> Dict[str, Set[int]]:
    index = defaultdict(set)
    for doc_id, text in enumerate(documents):
        tokens = clean_text(text).split()
        for token in set(tokens):
            index[token].add(doc_id)
    return dict(index)


def boolean_retrieval(query: str, inverted_index: Dict[str, Set[int]]) -> Set[int]:
    tokens = clean_text(query).split()
    if not tokens:
        return set()

    result = inverted_index.get(tokens[0], set())
    for token in tokens[1:]:
        result = result.intersection(inverted_index.get(token, set()))
    return result


def rank_documents(query: str, documents: List[str], top_k: int = 5) -> List[tuple]:
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([query] + documents)
    query_vec = tfidf_matrix[0:1]
    doc_vecs = tfidf_matrix[1:]
    scores = cosine_similarity(query_vec, doc_vecs).flatten()
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


def semantic_search(query: str, documents: List[str], model=None, top_k: int = 5) -> List[tuple]:
    if model is None:
        return rank_documents(query, documents, top_k)

    query_emb = model.encode([query])
    doc_embs = model.encode(documents)
    similarities = cosine_similarity(query_emb, doc_embs).flatten()
    ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
