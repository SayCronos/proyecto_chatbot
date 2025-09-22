"""
Estrategias de generación de sugerencias usando el patrón Strategy.
"""
from abc import ABC, abstractmethod
from typing import List, Set, Tuple
import difflib
import unicodedata
from app.models.beverage import Beverage


class SuggestionStrategy(ABC):
    """Interfaz abstracta para estrategias de generación de sugerencias."""
    
    @abstractmethod
    def generate_suggestions(self, beverages: List[Beverage], query: str, max_suggestions: int = 3) -> List[Beverage]:
        """Genera sugerencias basadas en la consulta."""
        pass


class SimilarityBasedSuggestionStrategy(SuggestionStrategy):
    """Estrategia de sugerencias basada en similitud de texto."""
    
    def generate_suggestions(self, beverages: List[Beverage], query: str, max_suggestions: int = 3) -> List[Beverage]:
        """Genera sugerencias usando similitud de texto y solapamiento de tokens."""
        q_norm = self._normalize_for_match(query)
        q_tokens = set(self._tokenize(query))
        
        candidates: List[Tuple[float, Beverage]] = []
        seen_keys: Set[Tuple[str, str]] = set()
        
        for beverage in beverages:
            name_norm = self._normalize_for_match(beverage.name_en)
            name_tokens = set(name_norm.split())
            key = (beverage.name_en, beverage.name_es)
            
            if key in seen_keys:
                continue
            seen_keys.add(key)
            
            ratio = difflib.SequenceMatcher(None, q_norm, name_norm).ratio()
            token_overlap = 0.0
            if q_tokens:
                token_overlap = len(q_tokens & name_tokens) / len(q_tokens)
            
            score = 0.6 * token_overlap + 0.4 * ratio
            candidates.append((score, beverage))
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        suggestions: List[Beverage] = []
        
        for score, beverage in candidates:
            if score <= 0.30:
                continue
            suggestions.append(beverage)
            if len(suggestions) >= max_suggestions:
                break
        
        return suggestions
    
    def _strip_accents(self, text: str) -> str:
        """Elimina acentos del texto."""
        if text is None:
            return ""
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(ch for ch in normalized if not unicodedata.combining(ch))

    def _normalize_for_match(self, text: str) -> str:
        """Normaliza texto para comparación."""
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
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokeniza el texto."""
        return self._normalize_for_match(text).split()


class CategoryBasedSuggestionStrategy(SuggestionStrategy):
    """Estrategia de sugerencias basada en categorías."""
    
    def generate_suggestions(self, beverages: List[Beverage], query: str, max_suggestions: int = 3) -> List[Beverage]:
        """Genera sugerencias basadas en categorías similares."""
        # Primero intentar encontrar bebidas de la misma categoría
        query_lower = query.lower()
        category_matches = []
        
        # Identificar posible categoría de la consulta
        target_category = None
        for beverage in beverages:
            if beverage.category and beverage.category.lower() in query_lower:
                target_category = beverage.category
                break
        
        if target_category:
            # Buscar bebidas de la misma categoría
            for beverage in beverages:
                if beverage.category == target_category:
                    category_matches.append(beverage)
        
        # Si no hay suficientes, usar estrategia de similitud
        if len(category_matches) < max_suggestions:
            similarity_strategy = SimilarityBasedSuggestionStrategy()
            similarity_matches = similarity_strategy.generate_suggestions(
                beverages, query, max_suggestions - len(category_matches)
            )
            category_matches.extend(similarity_matches)
        
        return category_matches[:max_suggestions]


class PopularityBasedSuggestionStrategy(SuggestionStrategy):
    """Estrategia de sugerencias basada en popularidad (frecuencia en datos)."""
    
    def generate_suggestions(self, beverages: List[Beverage], query: str, max_suggestions: int = 3) -> List[Beverage]:
        """Genera sugerencias basadas en popularidad y similitud."""
        # Calcular popularidad por frecuencia de aparición
        popularity_counts = {}
        for beverage in beverages:
            key = (beverage.name_en, beverage.name_es)
            popularity_counts[key] = popularity_counts.get(key, 0) + 1
        
        # Obtener sugerencias por similitud
        similarity_strategy = SimilarityBasedSuggestionStrategy()
        similar_beverages = similarity_strategy.generate_suggestions(beverages, query, max_suggestions * 2)
        
        # Ordenar por popularidad
        popular_suggestions = []
        seen_keys = set()
        
        for beverage in similar_beverages:
            key = (beverage.name_en, beverage.name_es)
            if key not in seen_keys:
                popularity = popularity_counts.get(key, 1)
                popular_suggestions.append((popularity, beverage))
                seen_keys.add(key)
        
        popular_suggestions.sort(key=lambda x: x[0], reverse=True)
        return [beverage for _, beverage in popular_suggestions[:max_suggestions]]


class HybridSuggestionStrategy(SuggestionStrategy):
    """Estrategia híbrida que combina múltiples enfoques."""
    
    def __init__(self):
        self.similarity_strategy = SimilarityBasedSuggestionStrategy()
        self.category_strategy = CategoryBasedSuggestionStrategy()
        self.popularity_strategy = PopularityBasedSuggestionStrategy()
    
    def generate_suggestions(self, beverages: List[Beverage], query: str, max_suggestions: int = 3) -> List[Beverage]:
        """Genera sugerencias combinando múltiples estrategias."""
        all_suggestions = []
        seen_keys = set()
        
        # Obtener sugerencias de cada estrategia
        strategies_results = [
            self.similarity_strategy.generate_suggestions(beverages, query, max_suggestions),
            self.category_strategy.generate_suggestions(beverages, query, max_suggestions),
            self.popularity_strategy.generate_suggestions(beverages, query, max_suggestions)
        ]
        
        # Combinar resultados priorizando diversidad
        for strategy_results in strategies_results:
            for beverage in strategy_results:
                key = (beverage.name_en, beverage.name_es)
                if key not in seen_keys and len(all_suggestions) < max_suggestions:
                    all_suggestions.append(beverage)
                    seen_keys.add(key)
        
        return all_suggestions


class SuggestionContext:
    """Contexto para las estrategias de sugerencias."""
    
    def __init__(self, strategy: SuggestionStrategy = None):
        self._strategy = strategy or HybridSuggestionStrategy()
    
    def set_strategy(self, strategy: SuggestionStrategy):
        """Cambia la estrategia de sugerencias."""
        self._strategy = strategy
    
    def generate_suggestions(self, beverages: List[Beverage], query: str, max_suggestions: int = 3) -> List[Beverage]:
        """Genera sugerencias usando la estrategia actual."""
        return self._strategy.generate_suggestions(beverages, query, max_suggestions)
