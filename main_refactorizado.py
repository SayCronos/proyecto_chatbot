"""
Aplicación principal FastAPI refactorizada con patrón Strategy.
Asistente de bebidas Starbucks completamente en español.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as api_router
from app.api.vistas import router as vistas_router
from app.core.config import configuracion


def crear_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""
    app = FastAPI(
        title=configuracion.nombre_app,
        version=configuracion.version_app,
        description="Asistente de bebidas Starbucks con patrón Strategy",
        debug=configuracion.debug
    )
    
    # Incluir routers
    app.include_router(api_router)
    app.include_router(vistas_router)
    
    return app


# Crear instancia de la aplicación
app = crear_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_refactorizado:app",
        host=configuracion.host,
        port=configuracion.puerto,
        reload=configuracion.debug
    )
