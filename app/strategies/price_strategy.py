"""
Estrategias de estimación de precios usando el patrón Strategy.
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.models.beverage import Beverage


class PriceEstimationStrategy(ABC):
    """Interfaz abstracta para estrategias de estimación de precios."""
    
    @abstractmethod
    def estimate_price(self, beverage: Beverage) -> float:
        """Estima el precio de una bebida."""
        pass


class BasicPriceStrategy(PriceEstimationStrategy):
    """Estrategia básica de precios por tamaño."""
    
    def estimate_price(self, beverage: Beverage) -> float:
        """Estima precio basado en tamaño inferido del método."""
        size = self._infer_size_from_method(beverage.method) or "Tall"
        
        base_prices = {
            "Short": 3.20,
            "Tall": 3.50,
            "Grande": 4.00,
            "Venti": 4.60
        }
        
        return base_prices.get(size, base_prices["Tall"])
    
    def _infer_size_from_method(self, method: str) -> Optional[str]:
        """Infiere el tamaño del método de preparación."""
        m = (method or "").lower()
        if "short" in m:
            return "Short"
        if "tall" in m:
            return "Tall"
        if "grande" in m:
            return "Grande"
        if "venti" in m:
            return "Venti"
        return None


class FamilyBasedPriceStrategy(PriceEstimationStrategy):
    """Estrategia de precios basada en familia de bebidas."""
    
    def estimate_price(self, beverage: Beverage) -> float:
        """Estima precio basado en familia y tamaño de bebida."""
        size = self._infer_size_from_method(beverage.method) or "Tall"
        family = self._infer_family_from_name(beverage.name_en)
        
        base_by_family = {
            "Brewed Coffee": {"Short": 2.25, "Tall": 2.45, "Grande": 2.65, "Venti": 2.85},
            "Americano": {"Short": 2.45, "Tall": 2.65, "Grande": 2.95, "Venti": 3.25},
            "Latte": {"Short": 3.35, "Tall": 3.65, "Grande": 4.15, "Venti": 4.65},
            "Cappuccino": {"Short": 3.35, "Tall": 3.65, "Grande": 4.15, "Venti": 4.65},
            "Mocha": {"Short": 3.85, "Tall": 4.15, "Grande": 4.65, "Venti": 5.15},
        }
        
        # Si hay categoría de espresso, aproximar como Latte si no está clasificado
        cat = (beverage.category or "").lower()
        if family == "Other" and ("espresso" in cat or "classic espresso" in cat):
            family = "Latte"
        
        base_table = base_by_family.get(family) or {
            "Short": 3.20, "Tall": 3.50, "Grande": 4.00, "Venti": 4.60
        }
        
        return base_table.get(size, base_table["Tall"])
    
    def _infer_size_from_method(self, method: str) -> Optional[str]:
        """Infiere el tamaño del método de preparación."""
        m = (method or "").lower()
        if "short" in m:
            return "Short"
        if "tall" in m:
            return "Tall"
        if "grande" in m:
            return "Grande"
        if "venti" in m:
            return "Venti"
        return None
    
    def _infer_family_from_name(self, name_en: str) -> str:
        """Infiere la familia de bebida del nombre."""
        n = (name_en or "").lower()
        if "americano" in n:
            return "Americano"
        if "mocha" in n:
            return "Mocha"
        if "cappuccino" in n:
            return "Cappuccino"
        if "latte" in n:
            return "Latte"
        if "brewed coffee" in n or "coffee" in n:
            return "Brewed Coffee"
        return "Other"


class PremiumPriceStrategy(PriceEstimationStrategy):
    """Estrategia de precios premium con recargos por ingredientes especiales."""
    
    def estimate_price(self, beverage: Beverage) -> float:
        """Estima precio con recargos por leche alternativa y otros ingredientes."""
        # Usar estrategia base de familia
        base_strategy = FamilyBasedPriceStrategy()
        price = base_strategy.estimate_price(beverage)
        
        # Recargos por leche alternativa según method
        method = (beverage.method or "").lower()
        if any(alt_milk in method for alt_milk in ["soymilk", "soy milk", "almond", "oat"]):
            price += 0.50
        
        # Recargo por ingredientes premium
        if any(premium in method for premium in ["vanilla", "caramel", "hazelnut"]):
            price += 0.25
        
        return round(price, 2)


class PriceStrategyContext:
    """Contexto para las estrategias de precios."""
    
    def __init__(self, strategy: PriceEstimationStrategy = None):
        self._strategy = strategy or PremiumPriceStrategy()
    
    def set_strategy(self, strategy: PriceEstimationStrategy):
        """Cambia la estrategia de estimación de precios."""
        self._strategy = strategy
    
    def estimate_price(self, beverage: Beverage) -> float:
        """Estima el precio usando la estrategia actual."""
        return self._strategy.estimate_price(beverage)
