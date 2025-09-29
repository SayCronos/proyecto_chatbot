"""
Modelos de datos para la aplicación de bebidas Starbucks.
"""
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel


@dataclass
class Bebida:
    """Modelo de datos para una bebida."""
    nombre_en: str
    nombre_es: str
    metodo: str
    calorias: Optional[float]
    grasa_total: Optional[float]
    categoria: Optional[str] = None
    precio: Optional[float] = None
    url_imagen: Optional[str] = None
    descripcion: Optional[str] = None


class SolicitudBusqueda(BaseModel):
    """Modelo de solicitud para búsqueda de bebidas."""
    consulta: str
    idioma: str = "es"


class RespuestaBusqueda(BaseModel):
    """Modelo de respuesta para búsqueda de bebidas."""
    ok: bool = True
    encontrado: bool
    idioma: str = "es"
    datos: Optional[Bebida] = None
    texto: str
    sugerencias: list[Bebida] = []


class RespuestaSugerencias(BaseModel):
    """Modelo de respuesta para sugerencias de bebidas."""
    ok: bool = True
    idioma: str = "es"
    elementos: list[Bebida]
