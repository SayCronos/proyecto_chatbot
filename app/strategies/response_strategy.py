"""
Estrategias de formateo de respuestas usando el patrón Strategy.
"""
from abc import ABC, abstractmethod
from typing import List
from app.models.beverage import Beverage


class ResponseFormattingStrategy(ABC):
    """Interfaz abstracta para estrategias de formateo de respuestas."""
    
    @abstractmethod
    def format_found_response(self, beverage: Beverage, lang: str = "es") -> str:
        """Formatea la respuesta cuando se encuentra una bebida."""
        pass
    
    @abstractmethod
    def format_not_found_response(self, query: str, suggestions: List[Beverage], lang: str = "es") -> str:
        """Formatea la respuesta cuando no se encuentra una bebida."""
        pass


class StandardResponseStrategy(ResponseFormattingStrategy):
    """Estrategia estándar de formateo de respuestas."""
    
    def format_found_response(self, beverage: Beverage, lang: str = "es") -> str:
        """Formatea respuesta estándar para bebida encontrada."""
        calories = self._format_number(beverage.calories)
        fat = self._format_number(beverage.total_fat)
        price = f"${beverage.price:.2f}" if beverage.price is not None else "N/D"
        
        if lang == "en":
            response = (
                f"Beverage: {beverage.name_en}\n"
                f"Preparation time: {beverage.method}\n"
                f"Calories: {calories} kcal\n"
                f"Total fat: {fat} g\n"
                f"Price: {price}"
            )
            if beverage.description:
                response += f"\nDescription: {beverage.description}"
        else:
            response = (
                f"Bebida: {beverage.name_es}\n"
                f"Tiempo de preparación: {beverage.method}\n"
                f"Calorías: {calories} kcal\n"
                f"Grasa total: {fat} g\n"
                f"Precio: {price}"
            )
            if beverage.description:
                response += f"\nDescripción: {beverage.description}"
        
        return response
    
    def format_not_found_response(self, query: str, suggestions: List[Beverage], lang: str = "es") -> str:
        """Formatea respuesta estándar para bebida no encontrada."""
        if lang == "en":
            base = f"The beverage '{query}' is not available on the menu."
            if suggestions:
                sug = ", ".join(f"{s.name_en}" for s in suggestions)
                return f"{base} You might be interested in: {sug}."
        else:
            base = f"La bebida '{query}' no está disponible en el menú."
            if suggestions:
                sug = ", ".join(f"{s.name_es}" for s in suggestions)
                return f"{base} Quizá te interesen: {sug}."
        
        return base
    
    def _format_number(self, value: float) -> str:
        """Formatea números para mostrar enteros sin decimales."""
        if value is None:
            return "N/D"
        return f"{int(value)}" if value.is_integer() else f"{value}"


class DetailedResponseStrategy(ResponseFormattingStrategy):
    """Estrategia detallada de formateo con información adicional."""
    
    def format_found_response(self, beverage: Beverage, lang: str = "es") -> str:
        """Formatea respuesta detallada para bebida encontrada."""
        calories = self._format_number(beverage.calories)
        fat = self._format_number(beverage.total_fat)
        price = f"${beverage.price:.2f}" if beverage.price is not None else "N/D"
        
        if lang == "en":
            response = (
                f"🍵 **{beverage.name_en}**\n"
                f"⏱️ Preparation: {beverage.method}\n"
                f"🔥 Calories: {calories} kcal\n"
                f"🧈 Total fat: {fat} g\n"
                f"💰 Price: {price}"
            )
            if beverage.category:
                response += f"\n📂 Category: {beverage.category}"
            if beverage.description:
                response += f"\n📝 Description: {beverage.description}"
        else:
            response = (
                f"🍵 **{beverage.name_es}**\n"
                f"⏱️ Preparación: {beverage.method}\n"
                f"🔥 Calorías: {calories} kcal\n"
                f"🧈 Grasa total: {fat} g\n"
                f"💰 Precio: {price}"
            )
            if beverage.category:
                response += f"\n📂 Categoría: {beverage.category}"
            if beverage.description:
                response += f"\n📝 Descripción: {beverage.description}"
        
        return response
    
    def format_not_found_response(self, query: str, suggestions: List[Beverage], lang: str = "es") -> str:
        """Formatea respuesta detallada para bebida no encontrada."""
        if lang == "en":
            base = f"❌ The beverage '{query}' is not available on our menu."
            if suggestions:
                sug = ", ".join(f"**{s.name_en}**" for s in suggestions)
                return f"{base}\n\n💡 You might be interested in: {sug}."
        else:
            base = f"❌ La bebida '{query}' no está disponible en nuestro menú."
            if suggestions:
                sug = ", ".join(f"**{s.name_es}**" for s in suggestions)
                return f"{base}\n\n💡 Quizá te interesen: {sug}."
        
        return base
    
    def _format_number(self, value: float) -> str:
        """Formatea números para mostrar enteros sin decimales."""
        if value is None:
            return "N/D"
        return f"{int(value)}" if value.is_integer() else f"{value}"


class CompactResponseStrategy(ResponseFormattingStrategy):
    """Estrategia compacta de formateo para respuestas breves."""
    
    def format_found_response(self, beverage: Beverage, lang: str = "es") -> str:
        """Formatea respuesta compacta para bebida encontrada."""
        price = f"${beverage.price:.2f}" if beverage.price is not None else "N/D"
        calories = self._format_number(beverage.calories)
        
        if lang == "en":
            return f"{beverage.name_en} - {price} | {calories} kcal | {beverage.method}"
        else:
            return f"{beverage.name_es} - {price} | {calories} kcal | {beverage.method}"
    
    def format_not_found_response(self, query: str, suggestions: List[Beverage], lang: str = "es") -> str:
        """Formatea respuesta compacta para bebida no encontrada."""
        if lang == "en":
            base = f"'{query}' not found."
            if suggestions:
                sug = ", ".join(f"{s.name_en}" for s in suggestions[:2])
                return f"{base} Try: {sug}."
        else:
            base = f"'{query}' no encontrada."
            if suggestions:
                sug = ", ".join(f"{s.name_es}" for s in suggestions[:2])
                return f"{base} Prueba: {sug}."
        
        return base
    
    def _format_number(self, value: float) -> str:
        """Formatea números para mostrar enteros sin decimales."""
        if value is None:
            return "N/D"
        return f"{int(value)}" if value.is_integer() else f"{value}"


class ResponseFormattingContext:
    """Contexto para las estrategias de formateo de respuestas."""
    
    def __init__(self, strategy: ResponseFormattingStrategy = None):
        self._strategy = strategy or StandardResponseStrategy()
    
    def set_strategy(self, strategy: ResponseFormattingStrategy):
        """Cambia la estrategia de formateo."""
        self._strategy = strategy
    
    def format_found_response(self, beverage: Beverage, lang: str = "es") -> str:
        """Formatea respuesta para bebida encontrada usando la estrategia actual."""
        return self._strategy.format_found_response(beverage, lang)
    
    def format_not_found_response(self, query: str, suggestions: List[Beverage], lang: str = "es") -> str:
        """Formatea respuesta para bebida no encontrada usando la estrategia actual."""
        return self._strategy.format_not_found_response(query, suggestions, lang)
