"""
Estrategias de búsqueda para bebidas usando el patrón Strategy.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import difflib
import unicodedata
from app.models.beverage import Bebida


class EstrategiaBusqueda(ABC):
    """Interfaz abstracta para estrategias de búsqueda."""
    
    @abstractmethod
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """Busca una bebida usando la estrategia específica."""
        pass


class EstrategiaCoincidenciaExacta(EstrategiaBusqueda):
    """Estrategia de búsqueda por coincidencia exacta."""
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """Busca coincidencia exacta tras normalización."""
        consulta_normalizada = self._normalizar_para_comparacion(consulta)
        if not consulta_normalizada:
            return None
            
        for bebida in bebidas:
            if self._normalizar_para_comparacion(bebida.nombre) == consulta_normalizada:
                return bebida
        return None
    
    def _quitar_acentos(self, texto: str) -> str:
        """Elimina acentos del texto."""
        if texto is None:
            return ""
        normalizado = unicodedata.normalize("NFKD", texto)
        return "".join(ch for ch in normalizado if not unicodedata.combining(ch))

    def _normalizar_para_comparacion(self, texto: str) -> str:
        """Normaliza texto para comparación."""
        texto_sin_acentos = self._quitar_acentos(texto)
        minusculas = texto_sin_acentos.casefold()
        limpio = []
        for ch in minusculas:
            if ch.isalnum():
                limpio.append(ch)
            else:
                limpio.append(" ")
        normalizado = " ".join("".join(limpio).split())
        return normalizado


class EstrategiaSolapamientoTokens(EstrategiaBusqueda):
    """Estrategia de búsqueda por solapamiento de tokens."""
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """Busca por solapamiento de tokens si la consulta tiene 2+ palabras."""
        consulta_normalizada = self._normalizar_para_comparacion(consulta)
        tokens_consulta = set(consulta_normalizada.split())
        
        if len(tokens_consulta) < 2:
            return None
            
        mejor = None
        mejor_puntuacion = 0
        
        for bebida in bebidas:
            nombre_normalizado = self._normalizar_para_comparacion(bebida.nombre)
            tokens_nombre = set(nombre_normalizado.split())
            
            if not tokens_nombre:
                continue
                
            solapamiento = len(tokens_consulta & tokens_nombre) / len(tokens_consulta)
            if solapamiento < 1.0:
                continue
                
            ratio = difflib.SequenceMatcher(None, consulta_normalizada, nombre_normalizado).ratio()
            puntuacion = solapamiento + ratio
            
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor = bebida
                
        return mejor
    
    def _quitar_acentos(self, texto: str) -> str:
        """Elimina acentos del texto."""
        if texto is None:
            return ""
        normalizado = unicodedata.normalize("NFKD", texto)
        return "".join(ch for ch in normalizado if not unicodedata.combining(ch))

    def _normalizar_para_comparacion(self, texto: str) -> str:
        """Normaliza texto para comparación."""
        texto_sin_acentos = self._quitar_acentos(texto)
        minusculas = texto_sin_acentos.casefold()
        limpio = []
        for ch in minusculas:
            if ch.isalnum():
                limpio.append(ch)
            else:
                limpio.append(" ")
        normalizado = " ".join("".join(limpio).split())
        return normalizado


class EstrategiaBusquedaDifusa(EstrategiaBusqueda):
    """Estrategia de búsqueda difusa usando similitud de secuencias."""
    
    def __init__(self, umbral: float = 0.8):
        self.umbral = umbral
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """Busca usando similitud difusa."""
        consulta_normalizada = self._normalizar_para_comparacion(consulta)
        mejor = None
        mejor_ratio = 0
        
        for bebida in bebidas:
            nombre_normalizado = self._normalizar_para_comparacion(bebida.nombre)
            ratio = difflib.SequenceMatcher(None, consulta_normalizada, nombre_normalizado).ratio()
            
            if ratio >= self.umbral and ratio > mejor_ratio:
                mejor_ratio = ratio
                mejor = bebida
                
        return mejor
    
    def _quitar_acentos(self, texto: str) -> str:
        """Elimina acentos del texto."""
        if texto is None:
            return ""
        normalizado = unicodedata.normalize("NFKD", texto)
        return "".join(ch for ch in normalizado if not unicodedata.combining(ch))

    def _normalizar_para_comparacion(self, texto: str) -> str:
        """Normaliza texto para comparación."""
        texto_sin_acentos = self._quitar_acentos(texto)
        minusculas = texto_sin_acentos.casefold()
        limpio = []
        for ch in minusculas:
            if ch.isalnum():
                limpio.append(ch)
            else:
                limpio.append(" ")
        normalizado = " ".join("".join(limpio).split())
        return normalizado


class EstrategiaBusquedaCompuesta(EstrategiaBusqueda):
    """Estrategia compuesta que combina múltiples estrategias."""
    
    def __init__(self):
        self.estrategias = [
            EstrategiaCoincidenciaExacta(),
            EstrategiaSolapamientoTokens(),
            EstrategiaBusquedaDifusa(umbral=0.7)
        ]
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """Aplica estrategias en orden hasta encontrar una coincidencia."""
        for estrategia in self.estrategias:
            resultado = estrategia.buscar(bebidas, consulta)
            if resultado:
                return resultado
        return None
