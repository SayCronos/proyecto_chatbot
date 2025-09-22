"""
Rutas API para el asistente de bebidas Starbucks.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.models.beverage import Beverage
from app.core.dependencies import get_beverage_service
from app.services.beverage_service import BeverageService


# Modelos de request/response
class SearchRequest(BaseModel):
    query: str
    lang: str = "es"


class SearchResponse(BaseModel):
    ok: bool = True
    found: bool
    lang: str = "es"
    data: Optional[Beverage] = None
    text: str
    suggestions: List[Beverage] = []


class SuggestionsResponse(BaseModel):
    ok: bool = True
    lang: str = "es"
    items: List[Beverage]


api_router = APIRouter(prefix="/api", tags=["beverages"])


@api_router.post("/search", response_model=SearchResponse)
async def search_beverages(
    request: SearchRequest,
    service: BeverageService = Depends(get_beverage_service)
) -> SearchResponse:
    """Busca bebidas basándose en la consulta."""
    try:
        # Buscar bebida
        beverage = service.search_beverage(request.query)
        
        if beverage:
            # Formatear respuesta encontrada
            text_response = service.format_found_response(beverage, request.lang)
            return SearchResponse(
                found=True,
                lang=request.lang,
                data=beverage,
                text=text_response,
                suggestions=[]
            )
        else:
            # Obtener sugerencias y formatear respuesta no encontrada
            suggestions = service.get_suggestions(request.query, max_suggestions=5)
            text_response = service.format_not_found_response(request.query, suggestions, request.lang)
            return SearchResponse(
                found=False,
                lang=request.lang,
                data=None,
                text=text_response,
                suggestions=suggestions
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching beverages: {str(e)}")


@api_router.get("/suggestions", response_model=SuggestionsResponse)
async def get_suggestions(
    query: Optional[str] = None,
    lang: str = "es",
    max_suggestions: int = 10,
    service: BeverageService = Depends(get_beverage_service)
) -> SuggestionsResponse:
    """Obtiene sugerencias de bebidas."""
    try:
        suggestions = service.get_suggestions(query or "", max_suggestions)
        return SuggestionsResponse(
            lang=lang,
            items=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting suggestions: {str(e)}")
