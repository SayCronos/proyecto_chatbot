"""
Search strategies for beverages using the Strategy pattern.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import difflib
import unicodedata
from app.models.beverage import Beverage


class SearchStrategy(ABC):
    """Abstract interface for search strategies."""
    
    @abstractmethod
    def search(self, beverages: List[Beverage], query: str) -> Optional[Beverage]:
        """Search for a beverage using the specific strategy."""
        pass


class ExactMatchStrategy(SearchStrategy):
    """Exact match search strategy."""
    
    def search(self, beverages: List[Beverage], query: str) -> Optional[Beverage]:
        """Search for exact match after normalization."""
        query_normalized = self._normalize_for_match(query)
        if not query_normalized:
            return None
            
        for beverage in beverages:
            # Check both English and Spanish names
            if (self._normalize_for_match(beverage.name_en) == query_normalized or
                self._normalize_for_match(beverage.name_es) == query_normalized):
                return beverage
        return None
    
    def _strip_accents(self, text: str) -> str:
        """Remove accents from text."""
        if text is None:
            return ""
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(ch for ch in normalized if not unicodedata.combining(ch))

    def _normalize_for_match(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text:
            return ""
        text_no_accents = self._strip_accents(text)
        folded = text_no_accents.casefold()
        cleaned = []
        for ch in folded:
            if ch.isalnum():
                cleaned.append(ch)
            else:
                cleaned.append(" ")
        normalized = " ".join("".join(cleaned).split())
        return normalized


class TokenOverlapStrategy(SearchStrategy):
    """Token overlap search strategy."""
    
    def search(self, beverages: List[Beverage], query: str) -> Optional[Beverage]:
        """Search by token overlap if query has 2+ words."""
        query_normalized = self._normalize_for_match(query)
        query_tokens = set(query_normalized.split())
        
        if len(query_tokens) < 2:
            return None
            
        best = None
        best_score = 0
        
        for beverage in beverages:
            # Check both English and Spanish names
            for name in [beverage.name_en, beverage.name_es]:
                if not name:
                    continue
                    
                name_normalized = self._normalize_for_match(name)
                name_tokens = set(name_normalized.split())
                
                if not name_tokens:
                    continue
                    
                overlap = len(query_tokens & name_tokens) / len(query_tokens)
                if overlap < 1.0:
                    continue
                    
                ratio = difflib.SequenceMatcher(None, query_normalized, name_normalized).ratio()
                score = overlap + ratio
                
                if score > best_score:
                    best_score = score
                    best = beverage
                
        return best
    
    def _strip_accents(self, text: str) -> str:
        """Remove accents from text."""
        if text is None:
            return ""
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(ch for ch in normalized if not unicodedata.combining(ch))

    def _normalize_for_match(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text:
            return ""
        text_no_accents = self._strip_accents(text)
        folded = text_no_accents.casefold()
        cleaned = []
        for ch in folded:
            if ch.isalnum():
                cleaned.append(ch)
            else:
                cleaned.append(" ")
        normalized = " ".join("".join(cleaned).split())
        return normalized


class FuzzySearchStrategy(SearchStrategy):
    """Fuzzy search strategy using sequence similarity."""
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
    
    def search(self, beverages: List[Beverage], query: str) -> Optional[Beverage]:
        """Search using fuzzy similarity."""
        q_norm = self._normalize_for_match(query)
        best = None
        best_ratio = 0
        
        for beverage in beverages:
            # Check both English and Spanish names
            for name in [beverage.name_en, beverage.name_es]:
                if not name:
                    continue
                    
                name_norm = self._normalize_for_match(name)
                ratio = difflib.SequenceMatcher(None, q_norm, name_norm).ratio()
                
                if ratio >= self.threshold and ratio > best_ratio:
                    best_ratio = ratio
                    best = beverage
                
        return best
    
    def _strip_accents(self, text: str) -> str:
        """Remove accents from text."""
        if text is None:
            return ""
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(ch for ch in normalized if not unicodedata.combining(ch))

    def _normalize_for_match(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text:
            return ""
        text_no_accents = self._strip_accents(text)
        folded = text_no_accents.casefold()
        cleaned = []
        for ch in folded:
            if ch.isalnum():
                cleaned.append(ch)
            else:
                cleaned.append(" ")
        normalized = " ".join("".join(cleaned).split())
        return normalized


class CompositeSearchStrategy(SearchStrategy):
    """Composite strategy that combines multiple strategies."""
    
    def __init__(self):
        self.strategies = [
            ExactMatchStrategy(),
            TokenOverlapStrategy(),
            FuzzySearchStrategy(threshold=0.7)
        ]
    
    def search(self, beverages: List[Beverage], query: str) -> Optional[Beverage]:
        """Apply strategies in order until finding a match."""
        for strategy in self.strategies:
            result = strategy.search(beverages, query)
            if result:
                return result
        return None
