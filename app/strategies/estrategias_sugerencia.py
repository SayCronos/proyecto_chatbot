"""
Estrategias de generación de sugerencias usando el patrón Strategy.
"""
from abc import ABC, abstractmethod
from typing import List, Set, Tuple
import difflib
import unicodedata
from app.models.beverage import Bebida


class EstrategiaSugerencia(ABC):
    """Interfaz abstracta para estrategias de generación de sugerencias."""
    
    @abstractmethod
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias basadas en la consulta."""
        pass


class EstrategiaSugerenciaPorSimilitud(EstrategiaSugerencia):
    """Estrategia de sugerencias basada en similitud de texto."""
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias usando similitud de texto y solapamiento de tokens."""
        consulta_normalizada = self._normalizar_para_comparacion(consulta)
        tokens_consulta = set(self._tokenizar(consulta))
        
        candidatos: List[Tuple[float, Bebida]] = []
        claves_vistas: Set[str] = set()
        
        for bebida in bebidas:
            nombre_normalizado = self._normalizar_para_comparacion(bebida.nombre_es)
            tokens_nombre = set(nombre_normalizado.split())
            clave = bebida.nombre_es
            
            if clave in claves_vistas:
                continue
            claves_vistas.add(clave)
            
            ratio = difflib.SequenceMatcher(None, consulta_normalizada, nombre_normalizado).ratio()
            solapamiento_tokens = 0.0
            if tokens_consulta:
                solapamiento_tokens = len(tokens_consulta & tokens_nombre) / len(tokens_consulta)
            
            puntuacion = 0.6 * solapamiento_tokens + 0.4 * ratio
            candidatos.append((puntuacion, bebida))
        
        candidatos.sort(key=lambda x: x[0], reverse=True)
        sugerencias: List[Bebida] = []
        
        for puntuacion, bebida in candidatos:
            if puntuacion <= 0.30:
                continue
            sugerencias.append(bebida)
            if len(sugerencias) >= max_sugerencias:
                break
        
        return sugerencias
    
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
    
    def _tokenizar(self, texto: str) -> List[str]:
        """Tokeniza el texto."""
        return self._normalizar_para_comparacion(texto).split()


class EstrategiaSugerenciaPorCategoria(EstrategiaSugerencia):
    """Estrategia de sugerencias basada en categorías."""
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias basadas en categorías similares."""
        # Primero intentar encontrar bebidas de la misma categoría
        consulta_minuscula = consulta.lower()
        coincidencias_categoria = []
        
        # Identificar posible categoría de la consulta
        categoria_objetivo = None
        for bebida in bebidas:
            if bebida.categoria and bebida.categoria.lower() in consulta_minuscula:
                categoria_objetivo = bebida.categoria
                break
        
        if categoria_objetivo:
            # Buscar bebidas de la misma categoría
            for bebida in bebidas:
                if bebida.categoria == categoria_objetivo:
                    coincidencias_categoria.append(bebida)
        
        # Si no hay suficientes, usar estrategia de similitud
        if len(coincidencias_categoria) < max_sugerencias:
            estrategia_similitud = EstrategiaSugerenciaPorSimilitud()
            coincidencias_similitud = estrategia_similitud.generar_sugerencias(
                bebidas, consulta, max_sugerencias - len(coincidencias_categoria)
            )
            coincidencias_categoria.extend(coincidencias_similitud)
        
        return coincidencias_categoria[:max_sugerencias]


class EstrategiaSugerenciaPorPopularidad(EstrategiaSugerencia):
    """Estrategia de sugerencias basada en popularidad (frecuencia en datos)."""
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias basadas en popularidad y similitud."""
        # Calcular popularidad por frecuencia de aparición
        conteos_popularidad = {}
        for bebida in bebidas:
            clave = bebida.nombre_es
            conteos_popularidad[clave] = conteos_popularidad.get(clave, 0) + 1
        
        # Obtener sugerencias por similitud
        estrategia_similitud = EstrategiaSugerenciaPorSimilitud()
        bebidas_similares = estrategia_similitud.generar_sugerencias(bebidas, consulta, max_sugerencias * 2)
        
        # Ordenar por popularidad
        sugerencias_populares = []
        claves_vistas = set()
        
        for bebida in bebidas_similares:
            clave = bebida.nombre_es
            if clave not in claves_vistas:
                popularidad = conteos_popularidad.get(clave, 1)
                sugerencias_populares.append((popularidad, bebida))
                claves_vistas.add(clave)
        
        sugerencias_populares.sort(key=lambda x: x[0], reverse=True)
        return [bebida for _, bebida in sugerencias_populares[:max_sugerencias]]


class EstrategiaSugerenciaHibrida(EstrategiaSugerencia):
    """Estrategia híbrida que combina múltiples enfoques."""
    
    def __init__(self):
        self.estrategia_similitud = EstrategiaSugerenciaPorSimilitud()
        self.estrategia_categoria = EstrategiaSugerenciaPorCategoria()
        self.estrategia_popularidad = EstrategiaSugerenciaPorPopularidad()
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias combinando múltiples estrategias."""
        todas_sugerencias = []
        claves_vistas = set()
        
        # Obtener sugerencias de cada estrategia
        resultados_estrategias = [
            self.estrategia_similitud.generar_sugerencias(bebidas, consulta, max_sugerencias),
            self.estrategia_categoria.generar_sugerencias(bebidas, consulta, max_sugerencias),
            self.estrategia_popularidad.generar_sugerencias(bebidas, consulta, max_sugerencias)
        ]
        
        # Combinar resultados priorizando diversidad
        for resultados_estrategia in resultados_estrategias:
            for bebida in resultados_estrategia:
                clave = bebida.nombre_es
                if clave not in claves_vistas and len(todas_sugerencias) < max_sugerencias:
                    todas_sugerencias.append(bebida)
                    claves_vistas.add(clave)
        
        return todas_sugerencias


class ContextoSugerencia:
    """Contexto para las estrategias de sugerencias."""
    
    def __init__(self, estrategia: EstrategiaSugerencia = None):
        self._estrategia = estrategia or EstrategiaSugerenciaHibrida()
    
    def establecer_estrategia(self, estrategia: EstrategiaSugerencia):
        """Cambia la estrategia de sugerencias."""
        self._estrategia = estrategia
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias usando la estrategia actual."""
        return self._estrategia.generar_sugerencias(bebidas, consulta, max_sugerencias)
