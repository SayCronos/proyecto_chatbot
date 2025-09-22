"""
Dependencias de FastAPI para inyección de dependencias.
"""
from functools import lru_cache
from pathlib import Path
from app.core.config import settings
from app.services.beverage_service import BeverageService
from app.strategies.search_strategy import CompositeSearchStrategy, ExactMatchStrategy, FuzzySearchStrategy
from app.strategies.price_strategy import PremiumPriceStrategy, FamilyBasedPriceStrategy, BasicPriceStrategy
from app.strategies.response_strategy import StandardResponseStrategy, DetailedResponseStrategy, CompactResponseStrategy
from app.strategies.suggestion_strategy import HybridSuggestionStrategy, SimilarityBasedSuggestionStrategy


@lru_cache()
def get_beverage_service() -> BeverageService:
    """
    Dependency injection para el servicio de bebidas.
    Usa cache para evitar recargar el CSV en cada request.
    """
    csv_path = Path(settings.csv_file_path)
    service = BeverageService(csv_path)
    
    # Configurar estrategias por defecto según configuración
    if settings.default_search_strategy == "exact":
        service.set_search_strategy(ExactMatchStrategy())
    elif settings.default_search_strategy == "fuzzy":
        service.set_search_strategy(FuzzySearchStrategy())
    else:  # composite (default)
        service.set_search_strategy(CompositeSearchStrategy())
    
    if settings.default_price_strategy == "basic":
        service.set_price_strategy(BasicPriceStrategy())
    elif settings.default_price_strategy == "family":
        service.set_price_strategy(FamilyBasedPriceStrategy())
    else:  # premium (default)
        service.set_price_strategy(PremiumPriceStrategy())
    
    if settings.default_response_strategy == "detailed":
        service.set_response_strategy(DetailedResponseStrategy())
    elif settings.default_response_strategy == "compact":
        service.set_response_strategy(CompactResponseStrategy())
    else:  # standard (default)
        service.set_response_strategy(StandardResponseStrategy())
    
    if settings.default_suggestion_strategy == "similarity":
        service.set_suggestion_strategy(SimilarityBasedSuggestionStrategy())
    else:  # hybrid (default)
        service.set_suggestion_strategy(HybridSuggestionStrategy())
    
    return service


def get_settings():
    """Dependency injection para la configuración."""
    return settings
