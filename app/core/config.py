"""
Configuración de la aplicación FastAPI.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # Configuración del servidor
    app_name: str = "Asistente de Bebidas Starbucks"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Ruta del archivo CSV
    csv_file_path: str = "starbucks2.csv"
    
    # Estrategias por defecto
    default_search_strategy: str = "composite"
    default_price_strategy: str = "premium"
    default_response_strategy: str = "standard"
    default_suggestion_strategy: str = "hybrid"
    
    # Configuración del servidor
    host: str = "127.0.0.1"
    port: int = 5000
    
    class Config:
        env_file = ".env"


# Instancia global de configuración
settings = Settings()
