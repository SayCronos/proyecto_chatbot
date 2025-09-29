"""
Estrategias de formateo de respuestas usando el patrón Strategy.
"""
from abc import ABC, abstractmethod
from typing import List
from app.models.beverage import Bebida


class EstrategiaFormateoRespuesta(ABC):
    """Interfaz abstracta para estrategias de formateo de respuestas."""
    
    @abstractmethod
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """Formatea la respuesta cuando se encuentra una bebida."""
        pass
    
    @abstractmethod
    def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
        """Formatea la respuesta cuando no se encuentra una bebida."""
        pass


class EstrategiaRespuestaEstandar(EstrategiaFormateoRespuesta):
    """Estrategia estándar de formateo de respuestas."""
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """Formatea respuesta estándar para bebida encontrada."""
        calorias = self._formatear_numero(bebida.calorias)
        grasa = self._formatear_numero(bebida.grasa_total)
        precio = f"${bebida.precio:.2f}" if bebida.precio is not None else "N/D"
        
        respuesta = (
            f"Bebida: {bebida.nombre_es}\n"
            f"Tiempo de preparación: {bebida.metodo}\n"
            f"Calorías: {calorias} kcal\n"
            f"Grasa total: {grasa} g\n"
            f"Precio: {precio}"
        )
        
        if bebida.descripcion:
            respuesta += f"\nDescripción: {bebida.descripcion}"
        
        return respuesta
    
    def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
        """Formatea respuesta estándar para bebida no encontrada."""
        base = f"La bebida '{consulta}' no está disponible en el menú."
        if sugerencias:
            sug = ", ".join(f"{s.nombre_es}" for s in sugerencias)
            return f"{base} Quizá te interesen: {sug}."
        
        return base
    
    def _formatear_numero(self, valor: float) -> str:
        """Formatea números para mostrar enteros sin decimales."""
        if valor is None:
            return "N/D"
        return f"{int(valor)}" if valor.is_integer() else f"{valor}"


class EstrategiaRespuestaDetallada(EstrategiaFormateoRespuesta):
    """Estrategia detallada de formateo con información adicional."""
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """Formatea respuesta detallada para bebida encontrada."""
        calorias = self._formatear_numero(bebida.calorias)
        grasa = self._formatear_numero(bebida.grasa_total)
        precio = f"${bebida.precio:.2f}" if bebida.precio is not None else "N/D"
        
        respuesta = (
            f"🍵 **{bebida.nombre_es}**\n"
            f"⏱️ Preparación: {bebida.metodo}\n"
            f"🔥 Calorías: {calorias} kcal\n"
            f"🧈 Grasa total: {grasa} g\n"
            f"💰 Precio: {precio}"
        )
        
        if bebida.categoria:
            respuesta += f"\n📂 Categoría: {bebida.categoria}"
        if bebida.descripcion:
            respuesta += f"\n📝 Descripción: {bebida.descripcion}"
        
        return respuesta
    
    def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
        """Formatea respuesta detallada para bebida no encontrada."""
        base = f"❌ La bebida '{consulta}' no está disponible en nuestro menú."
        if sugerencias:
            sug = ", ".join(f"**{s.nombre_es}**" for s in sugerencias)
            return f"{base}\n\n💡 Quizá te interesen: {sug}."
        
        return base
    
    def _formatear_numero(self, valor: float) -> str:
        """Formatea números para mostrar enteros sin decimales."""
        if valor is None:
            return "N/D"
        return f"{int(valor)}" if valor.is_integer() else f"{valor}"


class EstrategiaRespuestaCompacta(EstrategiaFormateoRespuesta):
    """Estrategia compacta de formateo para respuestas breves."""
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """Formatea respuesta compacta para bebida encontrada."""
        precio = f"${bebida.precio:.2f}" if bebida.precio is not None else "N/D"
        calorias = self._formatear_numero(bebida.calorias)
        
        return f"{bebida.nombre_es} - {precio} | {calorias} kcal | {bebida.metodo}"
    
    def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
        """Formatea respuesta compacta para bebida no encontrada."""
        base = f"'{consulta}' no encontrada."
        if sugerencias:
            sug = ", ".join(f"{s.nombre_es}" for s in sugerencias[:2])
            return f"{base} Prueba: {sug}."
        
        return base
    
    def _formatear_numero(self, valor: float) -> str:
        """Formatea números para mostrar enteros sin decimales."""
        if valor is None:
            return "N/D"
        return f"{int(valor)}" if valor.is_integer() else f"{valor}"


class ContextoFormateoRespuesta:
    """Contexto para las estrategias de formateo de respuestas."""
    
    def __init__(self, estrategia: EstrategiaFormateoRespuesta = None):
        self._estrategia = estrategia or EstrategiaRespuestaEstandar()
    
    def establecer_estrategia(self, estrategia: EstrategiaFormateoRespuesta):
        """Cambia la estrategia de formateo."""
        self._estrategia = estrategia
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """Formatea respuesta para bebida encontrada usando la estrategia actual."""
        return self._estrategia.formatear_respuesta_encontrada(bebida)
    
    def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
        """Formatea respuesta para bebida no encontrada usando la estrategia actual."""
        return self._estrategia.formatear_respuesta_no_encontrada(consulta, sugerencias)
