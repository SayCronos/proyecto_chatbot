"""
Data models for the Starbucks beverages application.
"""
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel


@dataclass
class Beverage:
    """Data model for a beverage."""
    name_en: str
    name_es: str
    method: str
    calories: Optional[float]
    total_fat: Optional[float]
    category: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


class SearchRequest(BaseModel):
    """Request model for beverage search."""
    query: str
    lang: str = "es"


class SearchResponse(BaseModel):
    """Response model for beverage search."""
    ok: bool = True
    found: bool
    lang: str = "es"
    data: Optional[Beverage] = None
    text: str
    suggestions: list[Beverage] = []


class SuggestionsResponse(BaseModel):
    """Response model for beverage suggestions."""
    ok: bool = True
    lang: str = "es"
    items: list[Beverage]
