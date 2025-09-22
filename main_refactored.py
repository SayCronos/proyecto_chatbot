"""
Aplicación FastAPI refactorizada con patrón Strategy.

Esta es la nueva versión de la aplicación que implementa:
- Patrón Strategy para búsqueda, precios, respuestas y sugerencias
- Arquitectura modular con separación de responsabilidades
- Inyección de dependencias
- Configuración centralizada
"""
import argparse
import sys
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

from app.core.config import settings
from app.core.dependencies import get_beverage_service
from app.api.routes import api_router
from app.api.views import views_router
from app.services.beverage_service import BeverageService


def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Asistente de bebidas Starbucks con patrón Strategy",
        debug=settings.debug
    )
    
    # Incluir routers
    app.include_router(api_router)
    app.include_router(views_router)
    
    return app


def run_cli_mode(args: argparse.Namespace) -> int:
    """Ejecuta la aplicación en modo CLI."""
    if not args.name:
        print("Proporciona el nombre de la bebida. Ejemplo: python main_refactored.py 'Caffè Latte'")
        return 2
    
    query = " ".join(args.name).strip()
    
    try:
        # Crear servicio de bebidas
        csv_path = Path(args.csv_path)
        service = BeverageService(csv_path)
        
        # Buscar bebida
        match = service.search_beverage(query)
        if match:
            print(service.format_found_response(match))
            return 0
        
        # Si no se encuentra, mostrar sugerencias
        suggestions = service.get_suggestions(query)
        print(service.format_not_found_response(query, suggestions))
        return 0
        
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Starbucks beverage assistant with Strategy pattern"
    )
    parser.add_argument(
        "name", 
        nargs="*",
        help="Beverage name in English or Spanish"
    )
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default=settings.csv_file_path,
        help=f"Path to the beverages CSV file (default: {settings.csv_file_path})",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Run a local web server with FastAPI",
    )
    parser.add_argument(
        "--host", 
        default=settings.host,
        help=f"Host for the web server (default: {settings.host})"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=settings.port,
        help=f"Port for the web server (default: {settings.port})"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Función principal de la aplicación."""
    args = parse_args(argv)
    
    # Actualizar configuración con argumentos
    if args.debug:
        settings.debug = True
    
    # Modo servidor web
    if args.serve:
        try:
            app = create_app()
            uvicorn.run(
                app, 
                host=args.host, 
                port=args.port, 
                log_level="debug" if args.debug else "info"
            )
            return 0
        except Exception as exc:
            print(f"Error al iniciar el servidor: {exc}")
            return 1
    
    # Modo CLI
    return run_cli_mode(args)


if __name__ == "__main__":
    sys.exit(main())
