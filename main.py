"""
Asistente de bebidas de Starbucks

Este módulo implementa:
- Carga/normalización de un CSV con bebidas (EN/ES, método, kcal, grasa, categoría, precio, imagen)
- Búsqueda tolerante a acentos/variaciones y sugerencias basadas en similitud/token overlap
- Estimación de precio cuando no hay dato en el CSV
- Servidor FastAPI con APIs (/api/search, /api/suggestions) y vistas (/ y /chat)
- CLI para consultas rápidas desde terminal
"""

import argparse
import csv
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import unicodedata


@dataclass
class Beverage:
    name_en: str
    name_es: str
    method: str
    calories: Optional[float]
    total_fat: Optional[float]
    category: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


# FastAPI es opcional; el modo CLI funciona sin él
try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
    import uvicorn

    # Modelos Pydantic para FastAPI
    class SearchRequest(BaseModel):
        query: str
        lang: Optional[str] = None

    class SearchResponse(BaseModel):
        ok: bool
        found: bool
        lang: str
        data: Optional[Dict] = None
        suggestions: Optional[List[Dict]] = None
        text: str

    class SuggestionsResponse(BaseModel):
        ok: bool
        lang: Optional[str] = None
        items: List[Dict]

except Exception:  # noqa: BLE001 - import opcional
    FastAPI = None  # type: ignore
    BaseModel = None  # type: ignore


def _normalize_header(header: str) -> str:
    key = header.strip().lower()
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
    }
    for src, dst in replacements.items():
        key = key.replace(src, dst)
    key = key.replace("(", " ").replace(")", " ").replace(
        "[", " ").replace("]", " ")
    key = key.replace("-", " ").replace("/", " ").replace(".", " ")
    # Normalizar guion bajo a espacio para soportar encabezados como 'beverage_prep'
    key = key.replace("_", " ")
    key = " ".join(key.split())
    return key


def _guess_column_mapping(headers: Iterable[str]) -> Dict[str, str]:
    normalized = {h: _normalize_header(h) for h in headers}

    def find(candidates: List[str]) -> Optional[str]:
        best_choice: Optional[Tuple[int, int, str]
                              ] = None  # (score, length, original)
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
                # Prefer higher score, then shorter norm to avoid picking 'beverage category' over 'beverage'
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
    calories_col = find(
        ["calories", "calorias", "calorias kcal", "calorias (kcal)", "caloria"])
    fat_col = find(["grasa total", "total fat", "fat", "grasa", "total fat g"])
    price_col = find(["price", "precio", "price usd",
                     "precio usd", "precio (usd)", "price ($)"])
    description_col = find(["descripcion", "description", "descripción"])
    image_col = find(["imagen", "image", "image url",
                     "url imagen", "imagen url"])

    # Para starbucks2.csv, usamos el nombre en español como nombre principal
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


def _to_float(value: str) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip().lower()
    if not text:
        return None

    # Remove potential units like "kcal" or "g" and currency symbols
    for suffix in ["kcal", "g", "cal", "grams", "gramos", "usd", "$"]:
        if text.endswith(suffix):
            text = text[: -len(suffix)].strip()

    # Handle European decimal format (comma as decimal separator)
    if "," in text and "." not in text:
        # European format: 4,5 -> 4.5
        text = text.replace(",", ".")
    elif "," in text and "." in text:
        # Mixed format: determine which is decimal separator
        comma_pos = text.rfind(",")
        dot_pos = text.rfind(".")
        if comma_pos > dot_pos:
            # Comma is decimal separator: 1.234,5 -> 1234.5
            text = text.replace(".", "").replace(",", ".")
        else:
            # Dot is decimal separator: 1,234.5 -> 1234.5
            text = text.replace(",", "")

    # Remove any stray characters except digits, dots, and minus
    filtered = "".join(ch for ch in text if (
        ch.isdigit() or ch == "." or ch == "-"))

    try:
        return float(filtered) if filtered else None
    except ValueError:
        return None


def _infer_size_from_method(method: str) -> Optional[str]:
    m = (method or "").lower()
    if "short" in m:
        return "Short"
    if "tall" in m:
        return "Tall"
    if "grande" in m:
        return "Grande"
    if "venti" in m:
        return "Venti"
    return None


def _infer_family_from_name(name_en: str) -> str:
    n = (name_en or "").lower()
    if "americano" in n:
        return "Americano"
    if "mocha" in n:
        return "Mocha"
    if "cappuccino" in n:
        return "Cappuccino"
    if "latte" in n:
        return "Latte"
    if "brewed coffee" in n or "coffee" in n:
        return "Brewed Coffee"
    return "Other"


def derive_price_estimate(name_en: str, method: str, category: Optional[str]) -> float:
    size = _infer_size_from_method(method) or "Tall"
    family = _infer_family_from_name(name_en)
    cat = (category or "").lower()

    # Base prices (USD) por tamaño para familias comunes
    base_by_family = {
        "Brewed Coffee": {"Short": 2.25, "Tall": 2.45, "Grande": 2.65, "Venti": 2.85},
        "Americano": {"Short": 2.45, "Tall": 2.65, "Grande": 2.95, "Venti": 3.25},
        "Latte": {"Short": 3.35, "Tall": 3.65, "Grande": 4.15, "Venti": 4.65},
        "Cappuccino": {"Short": 3.35, "Tall": 3.65, "Grande": 4.15, "Venti": 4.65},
        "Mocha": {"Short": 3.85, "Tall": 4.15, "Grande": 4.65, "Venti": 5.15},
    }
    # Si hay categoría de espresso, aproximar como Latte si no está clasificado
    if family == "Other" and ("espresso" in cat or "classic espresso" in cat):
        family = "Latte"

    base_table = base_by_family.get(
        family) or {"Short": 3.20, "Tall": 3.50, "Grande": 4.00, "Venti": 4.60}
    price = base_table.get(size, base_table["Tall"])

    # Recargos por leche alternativa según method
    m = (method or "").lower()
    if "soymilk" in m or "soy milk" in m or "almond" in m or "oat" in m:
        price += 0.50

    return round(price, 2)


def load_beverages(csv_path: Path) -> List[Beverage]:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo CSV en: {csv_path}")

    last_error: Optional[Exception] = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with csv_path.open("r", encoding=encoding, newline="") as f:
                # Detectar el separador del CSV
                sample = f.read(1024)
                f.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                reader = csv.DictReader(f, delimiter=delimiter)
                if reader.fieldnames is None:
                    raise ValueError(
                        "El CSV no contiene encabezados (fila de columnas)")
                mapping = _guess_column_mapping(reader.fieldnames)
                # Hacemos opcional name_es; si falta, se usará name_en como fallback
                required = ["name_en", "method", "calories", "total_fat"]
                missing = [k for k in required if k not in mapping]
                if missing:
                    raise ValueError(
                        "No se pudieron identificar las columnas requeridas en el CSV. "
                        f"Faltan: {', '.join(missing)}. Encabezados detectados: {reader.fieldnames}"
                    )

                beverages: List[Beverage] = []
                for row in reader:
                    name_en = (row.get(mapping["name_en"], "") or "").strip()
                    # Fallback: si no hay columna de español, usamos el nombre en inglés
                    name_es_key = mapping.get("name_es")
                    name_es = (row.get(name_es_key, "")
                               or "").strip() if name_es_key else name_en
                    method = (row.get(mapping["method"], "") or "").strip()
                    calories = _to_float(row.get(mapping["calories"]))
                    total_fat = _to_float(row.get(mapping["total_fat"]))
                    category = (row.get(mapping.get("category", ""), "") or "").strip(
                    ) if mapping.get("category") else None
                    price_val = _to_float(
                        row.get(mapping.get("price", ""))) if mapping.get("price") else None
                    image_url = (row.get(mapping.get("image_url", ""), "") or "").strip(
                    ) if mapping.get("image_url") else None
                    description = (row.get(mapping.get("description", ""), "") or "").strip(
                    ) if mapping.get("description") else None

                    if not name_en and not name_es:
                        continue

                    beverage = Beverage(
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
                    if beverage.price is None:
                        beverage.price = derive_price_estimate(
                            beverage.name_en, beverage.method, beverage.category)

                    beverages.append(beverage)
                return beverages
        except Exception as exc:  # noqa: BLE001 - collect and try next encoding
            last_error = exc
            continue

    assert last_error is not None
    raise last_error


def _strip_accents(text: str) -> str:
    if text is None:
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def _normalize_for_match(text: str) -> str:
    # Quitar acentos, bajar a minúsculas, mantener alfanumérico y espacios
    text_no_accents = _strip_accents(text)
    folded = text_no_accents.casefold()
    cleaned = []
    for ch in folded:
        if ch.isalnum():
            cleaned.append(ch)
        else:
            cleaned.append(" ")
    normalized = " ".join("".join(cleaned).split())
    return normalized


def _tokenize(text: str) -> List[str]:
    return _normalize_for_match(text).split()


def find_exact_match(beverages: List[Beverage], query: str) -> Optional[Beverage]:
    q_norm = _normalize_for_match(query)
    if not q_norm:
        return None
    # 1) Igualdad exacta tras normalización
    for b in beverages:
        if _normalize_for_match(b.name_en) == q_norm or _normalize_for_match(b.name_es) == q_norm:
            return b
    # 2) Coincidencia por tokens si la consulta tiene 2+ palabras
    q_tokens = set(q_norm.split())
    if len(q_tokens) >= 2:
        best: Optional[Tuple[float, float, Beverage]
                       ] = None  # (overlap, ratio, bev)
        for b in beverages:
            name_norm = _normalize_for_match(b.name_en)
            name_tokens = set(name_norm.split())
            if not name_tokens:
                continue
            overlap = len(q_tokens & name_tokens) / len(q_tokens)
            if overlap < 1.0:
                continue
            ratio = difflib.SequenceMatcher(None, q_norm, name_norm).ratio()
            key = (overlap, ratio, b)
            if best is None or (key[0] > best[0] or (key[0] == best[0] and key[1] > best[1])):
                best = key
        if best is not None:
            return best[2]
    return None


def suggest_similar(beverages: List[Beverage], query: str, max_suggestions: int = 3) -> List[Beverage]:
    q_norm = _normalize_for_match(query)
    q_tokens = set(_tokenize(query))

    candidates: List[Tuple[float, Beverage]] = []
    seen_keys: set = set()

    for b in beverages:
        name_norm = _normalize_for_match(b.name_en)
        name_tokens = set(name_norm.split())
        key = (b.name_en, b.name_es)
        if key in seen_keys:
            continue
        seen_keys.add(key)

        ratio = difflib.SequenceMatcher(None, q_norm, name_norm).ratio()
        token_overlap = 0.0
        if q_tokens:
            token_overlap = len(q_tokens & name_tokens) / len(q_tokens)
        score = 0.6 * token_overlap + 0.4 * ratio
        candidates.append((score, b))

    candidates.sort(key=lambda x: x[0], reverse=True)
    suggestions: List[Beverage] = []
    for score, bev in candidates:
        if score <= 0.30:
            continue
        suggestions.append(bev)
        if len(suggestions) >= max_suggestions:
            break
    return suggestions


def format_response(bev: Beverage, lang: str = "es") -> str:
    calories = f"{int(bev.calories)}" if bev.calories is not None and bev.calories.is_integer(
    ) else f"{bev.calories}" if bev.calories is not None else "N/D"
    fat = f"{int(bev.total_fat)}" if bev.total_fat is not None and bev.total_fat.is_integer(
    ) else f"{bev.total_fat}" if bev.total_fat is not None else "N/D"
    price = f"${bev.price:.2f}" if bev.price is not None else "N/D"

    response = (
        f"Bebida: {bev.name_es}\n"
        f"Tiempo de preparación: {bev.method}\n"
        f"Calorías: {calories} kcal\n"
        f"Grasa total: {fat} g\n"
        f"Precio: {price}"
    )

    if bev.description:
        response += f"\nDescripción: {bev.description}"

    return response


def format_not_found(query: str, suggestions: List[Beverage]) -> str:
    base = f"La bebida '{query}' no está disponible en el menú."
    if suggestions:
        sug = ", ".join(f"{s.name_es}" for s in suggestions)
        return f"{base} Quizá te interesen: {sug}."
    return base


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Starbucks beverage assistant")
    parser.add_argument("name", nargs="*",
                        help="Beverage name in English or Spanish")
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default=str(Path.cwd() / "starbucks2.csv"),
        help="Path to the beverages CSV file (default: ./starbucks2.csv)",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Run a local web server with a simple HTML UI",
    )
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host for the web server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000,
                        help="Port for the web server (default: 5000)")
    return parser.parse_args(argv)


def create_app(beverages: List[Beverage], csv_filename: str) -> "FastAPI":
    if FastAPI is None:
        raise RuntimeError(
            "FastAPI no está instalado. Instala con: pip install fastapi uvicorn jinja2"
        )

    app = FastAPI(title="Starbucks Beverage Assistant", version="1.0.0")

    # Configurar templates
    templates = Jinja2Templates(directory="templates")

    # Precalcular sugerencias populares por nombre (deduplicado)
    def build_top_suggestions(items: List[Beverage], limit: int = 12) -> List[Beverage]:
        counts: Dict[Tuple[str, str], int] = {}
        first_seen: Dict[Tuple[str, str], Beverage] = {}
        for b in items:
            key = (b.name_en, b.name_es)
            counts[key] = counts.get(key, 0) + 1
            if key not in first_seen:
                first_seen[key] = b
        sorted_keys = sorted(
            counts.items(), key=lambda kv: kv[1], reverse=True)
        top: List[Beverage] = []
        for (name_pair, _count) in sorted_keys[:limit]:
            top.append(first_seen[name_pair])
        return top

    top_suggestions: List[Beverage] = build_top_suggestions(beverages)

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        return templates.TemplateResponse("home.html", {
            "request": request,
            "csv_filename": csv_filename
        })

    @app.get("/chat", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "csv_filename": csv_filename
        })

    @app.get("/api/suggestions", response_model=SuggestionsResponse)
    async def api_suggestions(query: str = "", lang: str = ""):
        query = query.strip()
        lang = lang.strip().lower()
        if query:
            items = suggest_similar(beverages, query, max_suggestions=10)
        else:
            items = top_suggestions

        return SuggestionsResponse(
            ok=True,
            lang=lang or None,
            items=[
                {
                    "name_en": b.name_en,
                    "name_es": b.name_es,
                    "method": b.method,
                    "calories": b.calories,
                    "total_fat": b.total_fat,
                    "price": b.price,
                    "image_url": b.image_url,
                    "description": b.description,
                }
                for b in items
            ]
        )

    @app.post("/api/search", response_model=SearchResponse)
    async def api_search(request_data: SearchRequest):
        query = request_data.query.strip()
        user_lang = (request_data.lang or "").strip().lower()

        if not query:
            raise HTTPException(status_code=400, detail="empty_query")

        lang = "es"  # Siempre español para starbucks2.csv
        match = find_exact_match(beverages, query)

        if match:
            text = format_response(match)
            return SearchResponse(
                ok=True,
                found=True,
                lang=lang,
                data={
                    "name_en": match.name_en,
                    "name_es": match.name_es,
                    "method": match.method,
                    "calories": match.calories,
                    "total_fat": match.total_fat,
                    "price": match.price,
                    "image_url": match.image_url,
                    "description": match.description,
                },
                text=text,
            )

        suggestions = suggest_similar(beverages, query)
        text = format_not_found(query, suggestions)
        return SearchResponse(
            ok=True,
            found=False,
            lang=lang,
            suggestions=[
                {
                    "name_en": s.name_en,
                    "name_es": s.name_es,
                    "method": s.method,
                    "calories": s.calories,
                    "total_fat": s.total_fat,
                    "price": s.price,
                    "image_url": s.image_url,
                    "description": s.description,
                }
                for s in suggestions
            ],
            text=text,
        )

    return app


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    csv_path = Path(args.csv_path)
    try:
        beverages = load_beverages(csv_path)
    except Exception as exc:
        # Si estamos en modo servidor, informamos claramente y salimos
        if args.serve:
            print(f"No se pudo cargar el CSV: {exc}")
            return 1
        # Modo CLI siempre en español para starbucks2.csv
        print(f"No se pudo cargar el CSV: {exc}")
        return 1

    # Modo servidor web
    if args.serve:
        app = create_app(beverages, csv_filename=csv_path.name)
        # Usar uvicorn para servir la aplicación FastAPI
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
        return 0

    # Modo CLI tradicional
    if not args.name:
        print("Proporciona el nombre de la bebida. Ejemplo: python main.py 'Caffè Latte' --csv ruta\\a\\bebidas.csv")
        return 2

    query = " ".join(args.name).strip()

    match = find_exact_match(beverages, query)
    if match:
        print(format_response(match))
        return 0

    suggestions = suggest_similar(beverages, query)
    print(format_not_found(query, suggestions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
