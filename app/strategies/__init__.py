"""
Estrategias de la aplicación usando patrón Strategy.
"""
from .search_strategy import SearchStrategy, ExactMatchStrategy, FuzzySearchStrategy, CompositeSearchStrategy
from .price_strategy import PriceEstimationStrategy, BasicPriceStrategy, FamilyBasedPriceStrategy, PremiumPriceStrategy
from .response_strategy import ResponseFormattingStrategy, StandardResponseStrategy, DetailedResponseStrategy, CompactResponseStrategy
from .suggestion_strategy import SuggestionStrategy, SimilarityBasedSuggestionStrategy, HybridSuggestionStrategy