"""
Configuración de la aplicación FastAPI.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Configuracion(BaseSettings):
    """Configuración de la aplicación."""
    
    # Configuración del servidor
    nombre_app: str = "Asistente de Bebidas Starbucks"
    version_app: str = "2.0.0"
    debug: bool = False
    
    # Ruta del archivo CSV
    ruta_archivo_csv: str = "starbucks2.csv"
    
    # Estrategias por defecto
    estrategia_busqueda_default: str = "compuesta"
    estrategia_precio_default: str = "premium"
    estrategia_respuesta_default: str = "estandar"
    estrategia_sugerencia_default: str = "hibrida"
    
    # Configuración del servidor
    host: str = "127.0.0.1"  # Cambiar a "0.0.0.0" para acceso de red local
    puerto: int = 8000  # Puerto estándar para desarrollo web
    
    class Config:
        env_file = ".env"


# Instancia global de configuración
configuracion = Configuracion()
