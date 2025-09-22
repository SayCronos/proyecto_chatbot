"""
Servicio principal para manejo de bebidas con patrón Strategy integrado.
"""
import csv
from pathlib import Path
from typing import Dict, List, Optional
from app.models.beverage import Beverage
from app.strategies.search_strategy import CompositeSearchStrategy, SearchStrategy
from app.strategies.price_strategy import PriceStrategyContext, PremiumPriceStrategy
from app.strategies.response_strategy import ResponseFormattingContext, StandardResponseStrategy
from app.strategies.suggestion_strategy import SuggestionContext, HybridSuggestionStrategy


class BeverageService:
    """Servicio principal para manejo de bebidas con estrategias configurables."""
    
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.beverages: List[Beverage] = []
        
        # Inicializar contextos de estrategias
        self.search_strategy = CompositeSearchStrategy()
        self.price_context = PriceStrategyContext(PremiumPriceStrategy())
        self.response_context = ResponseFormattingContext(StandardResponseStrategy())
        self.suggestion_context = SuggestionContext(HybridSuggestionStrategy())
        
        # Cargar bebidas al inicializar
        self.load_beverages()
    
    def set_search_strategy(self, strategy: SearchStrategy):
        """Configura la estrategia de búsqueda."""
        self.search_strategy = strategy
    
    def set_price_strategy(self, strategy):
        """Configura la estrategia de estimación de precios."""
        self.price_context.set_strategy(strategy)
    
    def set_response_strategy(self, strategy):
        """Configura la estrategia de formateo de respuestas."""
        self.response_context.set_strategy(strategy)
    
    def set_suggestion_strategy(self, strategy):
        """Configura la estrategia de sugerencias."""
        self.suggestion_context.set_strategy(strategy)
    
    def load_beverages(self) -> None:
        """Carga las bebidas desde el archivo CSV."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo CSV en: {self.csv_path}")
        
        last_error: Optional[Exception] = None
        for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                with self.csv_path.open("r", encoding=encoding, newline="") as f:
                    # Detectar el separador del CSV
                    sample = f.read(1024)
                    f.seek(0)
                    sniffer = csv.Sniffer()
                    delimiter = sniffer.sniff(sample).delimiter
                    reader = csv.DictReader(f, delimiter=delimiter)
                    
                    if reader.fieldnames is None:
                        raise ValueError("El CSV no contiene encabezados (fila de columnas)")
                    
                    mapping = self._guess_column_mapping(reader.fieldnames)
                    required = ["name_en", "method", "calories", "total_fat"]
                    missing = [k for k in required if k not in mapping]
                    
                    if missing:
                        raise ValueError(
                            "No se pudieron identificar las columnas requeridas en el CSV. "
                            f"Faltan: {', '.join(missing)}. Encabezados detectados: {reader.fieldnames}"
                        )
                    
                    self.beverages = []
                    for row in reader:
                        beverage = self._create_beverage_from_row(row, mapping)
                        if beverage:
                            # Estimar precio si no existe
                            if beverage.price is None:
                                beverage.price = self.price_context.estimate_price(beverage)
                            self.beverages.append(beverage)
                    
                    return
            except Exception as exc:
                last_error = exc
                continue
        
        if last_error:
            raise last_error
    
    def search_beverage(self, query: str) -> Optional[Beverage]:
        """Busca una bebida usando la estrategia de búsqueda configurada."""
        return self.search_strategy.search(self.beverages, query)
    
    def get_suggestions(self, query: str = "", max_suggestions: int = 10) -> List[Beverage]:
        """Obtiene sugerencias de bebidas."""
        if query:
            return self.suggestion_context.generate_suggestions(
                self.beverages, query, max_suggestions
            )
        else:
            # Devolver las más populares (por frecuencia)
            return self._get_top_suggestions(max_suggestions)
    
    def format_found_response(self, beverage: Beverage, lang: str = "es") -> str:
        """Formatea la respuesta para una bebida encontrada."""
        return self.response_context.format_found_response(beverage, lang)
    
    def format_not_found_response(self, query: str, suggestions: List[Beverage], lang: str = "es") -> str:
        """Formatea la respuesta para una bebida no encontrada."""
        return self.response_context.format_not_found_response(query, suggestions, lang)
    
    def _guess_column_mapping(self, headers) -> Dict[str, str]:
        """Adivina el mapeo de columnas del CSV."""
        normalized = {h: self._normalize_header(h) for h in headers}
        
        def find(candidates: List[str]) -> Optional[str]:
            best_choice: Optional[tuple] = None
            for original, norm in normalized.items():
                for cand in candidates:
                    if norm == cand:
                        score = 3
                    elif norm.startswith(cand + " ") or norm.endswith(" " + cand) or (" " + cand + " ") in norm:
                        score = 2
                    elif cand in norm:
                        score = 1
                    else:
                        continue
                    key = (score, -len(norm), original)
                    if best_choice is None or key > best_choice:
                        best_choice = key
            return best_choice[2] if best_choice else None
        
        # Mapeo para starbucks2.csv (formato español)
        name_es_col = find([
            "nombre bebida", "nombre de la bebida", "bebida", "nombre", "name es", "spanish name",
            "nombre espanol", "nombre en espanol", "nombre español", "nombre en español",
            "beverage es", "drink es", "nombre de la bebida en espanol", "nombre de la bebida en español",
        ])
        method_col = find([
            "tiempo de preparacion", "tiempo preparacion", "tiempo", "preparacion", "tiempo de preparación",
            "method", "preparation", "metodo de preparacion", "metodo", "preparacion",
            "metodo de preparación", "método de preparación", "beverage prep",
        ])
        calories_col = find(["calories", "calorias", "calorias kcal", "calorias (kcal)", "caloria"])
        fat_col = find(["grasa total", "total fat", "fat", "grasa", "total fat g"])
        price_col = find(["price", "precio", "price usd", "precio usd", "precio (usd)", "price ($)"])
        description_col = find(["descripcion", "description", "descripción"])
        image_col = find(["imagen", "image", "image url", "url imagen", "imagen url"])
        
        name_en_col = name_es_col  # Usar el mismo nombre para ambos idiomas
        
        mapping = {}
        if name_en_col:
            mapping["name_en"] = name_en_col
        if name_es_col:
            mapping["name_es"] = name_es_col
        if method_col:
            mapping["method"] = method_col
        if calories_col:
            mapping["calories"] = calories_col
        if fat_col:
            mapping["total_fat"] = fat_col
        if price_col:
            mapping["price"] = price_col
        if description_col:
            mapping["description"] = description_col
        if image_col:
            mapping["image_url"] = image_col
        
        return mapping
    
    def _normalize_header(self, header: str) -> str:
        """Normaliza encabezados de CSV."""
        key = header.strip().lower()
        replacements = {
            "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n",
        }
        for src, dst in replacements.items():
            key = key.replace(src, dst)
        key = key.replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ")
        key = key.replace("-", " ").replace("/", " ").replace(".", " ").replace("_", " ")
        key = " ".join(key.split())
        return key
    
    def _create_beverage_from_row(self, row: dict, mapping: dict) -> Optional[Beverage]:
        """Crea una bebida desde una fila del CSV."""
        name_en = (row.get(mapping["name_en"], "") or "").strip()
        name_es_key = mapping.get("name_es")
        name_es = (row.get(name_es_key, "") or "").strip() if name_es_key else name_en
        method = (row.get(mapping["method"], "") or "").strip()
        calories = self._to_float(row.get(mapping["calories"]))
        total_fat = self._to_float(row.get(mapping["total_fat"]))
        category = (row.get(mapping.get("category", ""), "") or "").strip() if mapping.get("category") else None
        price_val = self._to_float(row.get(mapping.get("price", ""))) if mapping.get("price") else None
        image_url = (row.get(mapping.get("image_url", ""), "") or "").strip() if mapping.get("image_url") else None
        description = (row.get(mapping.get("description", ""), "") or "").strip() if mapping.get("description") else None
        
        if not name_en and not name_es:
            return None
        
        return Beverage(
            name_en=name_en,
            name_es=name_es,
            method=method,
            calories=calories,
            total_fat=total_fat,
            category=category,
            price=price_val,
            image_url=image_url or None,
            description=description,
        )
    
    def _to_float(self, value: str) -> Optional[float]:
        """Convierte string a float manejando diferentes formatos."""
        if value is None:
            return None
        text = str(value).strip().lower()
        if not text:
            return None
        
        # Remover unidades y símbolos de moneda
        for suffix in ["kcal", "g", "cal", "grams", "gramos", "usd", "$"]:
            if text.endswith(suffix):
                text = text[: -len(suffix)].strip()
        
        # Manejar formato decimal europeo
        if "," in text and "." not in text:
            text = text.replace(",", ".")
        elif "," in text and "." in text:
            comma_pos = text.rfind(",")
            dot_pos = text.rfind(".")
            if comma_pos > dot_pos:
                text = text.replace(".", "").replace(",", ".")
            else:
                text = text.replace(",", "")
        
        # Filtrar caracteres no numéricos
        filtered = "".join(ch for ch in text if (ch.isdigit() or ch == "." or ch == "-"))
        
        try:
            return float(filtered) if filtered else None
        except ValueError:
            return None
    
    def _get_top_suggestions(self, limit: int = 12) -> List[Beverage]:
        """Obtiene las sugerencias más populares."""
        counts: Dict[tuple, int] = {}
        first_seen: Dict[tuple, Beverage] = {}
        
        for beverage in self.beverages:
            key = (beverage.name_en, beverage.name_es)
            counts[key] = counts.get(key, 0) + 1
            if key not in first_seen:
                first_seen[key] = beverage
        
        sorted_keys = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
        top: List[Beverage] = []
        
        for (name_pair, _count) in sorted_keys[:limit]:
            top.append(first_seen[name_pair])
        
        return top
