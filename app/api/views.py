"""
Rutas de vistas HTML para la aplicación FastAPI.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.beverage_service import BeverageService


# Router para las vistas HTML
views_router = APIRouter(tags=["views"])

# Configurar templates
templates = Jinja2Templates(directory="templates")


def get_beverage_service() -> BeverageService:
    """Dependency injection para el servicio de bebidas."""
    csv_path = Path("starbucks2.csv")
    return BeverageService(csv_path)


@views_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con landing de Starbucks."""
    return templates.TemplateResponse("home.html", {
        "request": request,
        "csv_filename": "starbucks2.csv"
    })


@views_router.get("/chat", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Interfaz de chat para interactuar con el chatbot."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "csv_filename": "starbucks2.csv"
    })
