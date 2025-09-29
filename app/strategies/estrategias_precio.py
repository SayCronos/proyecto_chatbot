"""
Estrategias de estimación de precios usando el patrón Strategy.
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.models.beverage import Bebida


class EstrategiaEstimacionPrecio(ABC):
    """Interfaz abstracta para estrategias de estimación de precios."""
    
    @abstractmethod
    def estimar_precio(self, bebida: Bebida) -> float:
        """Estima el precio de una bebida."""
        pass


class EstrategiaPrecioBasico(EstrategiaEstimacionPrecio):
    """Estrategia básica de precios por tamaño."""
    
    def estimar_precio(self, bebida: Bebida) -> float:
        """Estima precio basado en tamaño inferido del método."""
        tamaño = self._inferir_tamaño_del_metodo(bebida.metodo_preparacion) or "Tall"
        
        precios_base = {
            "Short": 3.20,
            "Tall": 3.50,
            "Grande": 4.00,
            "Venti": 4.60
        }
        
        return precios_base.get(tamaño, precios_base["Tall"])
    
    def _inferir_tamaño_del_metodo(self, metodo: str) -> Optional[str]:
        """Infiere el tamaño del método de preparación."""
        m = (metodo or "").lower()
        if "short" in m:
            return "Short"
        if "tall" in m:
            return "Tall"
        if "grande" in m:
            return "Grande"
        if "venti" in m:
            return "Venti"
        return None


class EstrategiaPrecioPorFamilia(EstrategiaEstimacionPrecio):
    """Estrategia de precios basada en familia de bebidas."""
    
    def estimar_precio(self, bebida: Bebida) -> float:
        """Estima precio basado en familia y tamaño de bebida."""
        tamaño = self._inferir_tamaño_del_metodo(bebida.metodo) or "Tall"
        familia = self._inferir_familia_del_nombre(bebida.nombre_es)
        
        precios_por_familia = {
            "Café Preparado": {"Short": 2.25, "Tall": 2.45, "Grande": 2.65, "Venti": 2.85},
            "Americano": {"Short": 2.45, "Tall": 2.65, "Grande": 2.95, "Venti": 3.25},
            "Latte": {"Short": 3.35, "Tall": 3.65, "Grande": 4.15, "Venti": 4.65},
            "Cappuccino": {"Short": 3.35, "Tall": 3.65, "Grande": 4.15, "Venti": 4.65},
            "Mocha": {"Short": 3.85, "Tall": 4.15, "Grande": 4.65, "Venti": 5.15},
        }
        
        # Si hay categoría de espresso, aproximar como Latte si no está clasificado
        cat = (bebida.categoria or "").lower()
        if familia == "Otro" and ("espresso" in cat or "espresso clásico" in cat):
            familia = "Latte"
        
        tabla_precios = precios_por_familia.get(familia) or {
            "Short": 3.20, "Tall": 3.50, "Grande": 4.00, "Venti": 4.60
        }
        
        return tabla_precios.get(tamaño, tabla_precios["Tall"])
    
    def _inferir_tamaño_del_metodo(self, metodo: str) -> Optional[str]:
        """Infiere el tamaño del método de preparación."""
        m = (metodo or "").lower()
        if "short" in m:
            return "Short"
        if "tall" in m:
            return "Tall"
        if "grande" in m:
            return "Grande"
        if "venti" in m:
            return "Venti"
        return None
    
    def _inferir_familia_del_nombre(self, nombre: str) -> str:
        """Infiere la familia de bebida del nombre."""
        n = (nombre or "").lower()
        if "americano" in n:
            return "Americano"
        if "mocha" in n:
            return "Mocha"
        if "cappuccino" in n or "capuchino" in n:
            return "Cappuccino"
        if "latte" in n or "café con leche" in n:
            return "Latte"
        if "café preparado" in n or "coffee" in n:
            return "Café Preparado"
        return "Otro"


class EstrategiaPrecioPremium(EstrategiaEstimacionPrecio):
    """Estrategia de precios premium con recargos por ingredientes especiales."""
    
    def estimar_precio(self, bebida: Bebida) -> float:
        """Estima precio con recargos por leche alternativa y otros ingredientes."""
        # Usar estrategia base de familia
        estrategia_base = EstrategiaPrecioPorFamilia()
        precio = estrategia_base.estimar_precio(bebida)
        
        # Recargos por leche alternativa según método
        metodo = (bebida.metodo_preparacion or "").lower()
        if any(leche_alt in metodo for leche_alt in ["leche de soja", "soy milk", "almendra", "avena", "oat"]):
            precio += 0.50
        
        # Recargo por ingredientes premium
        if any(premium in metodo for premium in ["vainilla", "caramelo", "avellana"]):
            precio += 0.25
        
        return round(precio, 2)


class ContextoEstrategiaPrecio:
    """Contexto para las estrategias de precios."""
    
    def __init__(self, estrategia: EstrategiaEstimacionPrecio = None):
        self._estrategia = estrategia or EstrategiaPrecioPremium()
    
    def establecer_estrategia(self, estrategia: EstrategiaEstimacionPrecio):
        """Cambia la estrategia de estimación de precios."""
        self._estrategia = estrategia
    
    def estimar_precio(self, bebida: Bebida) -> float:
        """Estima el precio usando la estrategia actual."""
        return self._estrategia.estimar_precio(bebida)
