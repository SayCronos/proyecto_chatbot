"""
Rutas de vistas HTML para el asistente de bebidas Starbucks.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from functools import lru_cache
from pathlib import Path

from app.services.servicio_bebidas import ServicioBebidas
from app.core.config import configuracion


router = APIRouter(tags=["vistas"])
templates = Jinja2Templates(directory="templates")


@lru_cache()
def obtener_servicio_bebidas() -> ServicioBebidas:
    """Obtiene instancia del servicio de bebidas con caché."""
    ruta_csv = Path(configuracion.ruta_archivo_csv)
    return ServicioBebidas(ruta_csv)


@router.get("/")
async def pagina_inicio(request: Request):
    """Página de inicio del asistente de bebidas."""
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/chat")
async def pagina_chat(request: Request):
    """Página del chat del asistente de bebidas."""
    return templates.TemplateResponse("index.html", {"request": request})
