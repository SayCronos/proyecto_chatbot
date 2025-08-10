"""
Asistente de bebidas de Starbucks

Este módulo implementa:
- Carga/normalización de un CSV con bebidas (EN/ES, método, kcal, grasa, categoría, precio, imagen)
- Búsqueda tolerante a acentos/variaciones y sugerencias basadas en similitud/token overlap
- Estimación de precio cuando no hay dato en el CSV
- Servidor Flask con APIs (/api/search, /api/suggestions) y vistas (/ y /chat)
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

# Flask es opcional; el modo CLI funciona sin él
try:
    from flask import Flask, jsonify, render_template, request
except Exception:  # noqa: BLE001 - import opcional
    Flask = None  # type: ignore


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
    key = key.replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ")
    key = key.replace("-", " ").replace("/", " ").replace(".", " ")
    # Normalizar guion bajo a espacio para soportar encabezados como 'beverage_prep'
    key = key.replace("_", " ")
    key = " ".join(key.split())
    return key


def _guess_column_mapping(headers: Iterable[str]) -> Dict[str, str]:
    normalized = {h: _normalize_header(h) for h in headers}

    def find(candidates: List[str]) -> Optional[str]:
        best_choice: Optional[Tuple[int, int, str]] = None  # (score, length, original)
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

    name_en_col = find([
        "name en", "english name", "nombre ingles", "nombre en ingles", "beverage en", "drink en",
        "nombre de la bebida en ingles", "beverage",
    ])
    name_es_col = find([
        "name es", "spanish name", "nombre espanol", "nombre en espanol", "nombre español", "nombre en español",
        "beverage es", "drink es", "nombre de la bebida en espanol", "nombre de la bebida en español",
    ])
    method_col = find([
        "method", "preparation", "metodo de preparacion", "metodo", "preparacion",
        "metodo de preparación", "método de preparación", "beverage prep",
    ])
    calories_col = find(["calories", "calorias", "calorias kcal", "calorias (kcal)", "caloria"])
    fat_col = find(["total fat", "grasa total", "fat", "grasa", "total fat g"])
    category_col = find(["category", "beverage category", "categoria", "categoria de la bebida"])
    price_col = find(["price", "precio", "price usd", "precio usd", "precio (usd)", "price ($)"])
    image_col = find(["image", "image url", "imagen", "url imagen", "imagen url"])

    mapping = {}
    if name_en_col: mapping["name_en"] = name_en_col
    if name_es_col: mapping["name_es"] = name_es_col
    if method_col: mapping["method"] = method_col
    if calories_col: mapping["calories"] = calories_col
    if fat_col: mapping["total_fat"] = fat_col
    if category_col: mapping["category"] = category_col
    if price_col: mapping["price"] = price_col
    if image_col: mapping["image_url"] = image_col
    return mapping


def _to_float(value: str) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip().lower().replace(",", ".")
    if not text:
        return None
    # Remove potential units like "kcal" or "g" and currency symbols
    for suffix in ["kcal", "g", "cal", "grams", "gramos", "usd", "$"]:
        if text.endswith(suffix):
            text = text[: -len(suffix)].strip()
    # Remove any stray characters
    filtered = "".join(ch for ch in text if (ch.isdigit() or ch == "." or ch == "-"))
    try:
        return float(filtered)
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

    base_table = base_by_family.get(family) or {"Short": 3.20, "Tall": 3.50, "Grande": 4.00, "Venti": 4.60}
    price = base_table.get(size, base_table["Tall"])

    # Recargos por leche alternativa según method
    m = (method or "").lower()
    if "soymilk" in m or "soy milk" in m or "almond" in m or "oat" in m:
        price += 0.50

    return round(price, 2)


def load_beverages(csv_path: Path) -> List[Beverage]:
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV en: {csv_path}")

    last_error: Optional[Exception] = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with csv_path.open("r", encoding=encoding, newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise ValueError("El CSV no contiene encabezados (fila de columnas)")
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
                    name_es = (row.get(name_es_key, "") or "").strip() if name_es_key else name_en
                    method = (row.get(mapping["method"], "") or "").strip()
                    calories = _to_float(row.get(mapping["calories"]))
                    total_fat = _to_float(row.get(mapping["total_fat"]))
                    category = (row.get(mapping.get("category", ""), "") or "").strip() if mapping.get("category") else None
                    price_val = _to_float(row.get(mapping.get("price", ""))) if mapping.get("price") else None
                    image_url = (row.get(mapping.get("image_url", ""), "") or "").strip() if mapping.get("image_url") else None

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
                    )
                    if beverage.price is None:
                        beverage.price = derive_price_estimate(beverage.name_en, beverage.method, beverage.category)

                    beverages.append(beverage)
                return beverages
        except Exception as exc:  # noqa: BLE001 - collect and try next encoding
            last_error = exc
            continue

    assert last_error is not None
    raise last_error


def _casefold(text: str) -> str:
    return (text or "").casefold().strip()


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
        best: Optional[Tuple[float, float, Beverage]] = None  # (overlap, ratio, bev)
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


def detect_language(user_input: str) -> str:
    text = user_input.strip().lower()
    # Heuristics: accented characters or common Spanish stopwords
    if any(ch in text for ch in "áéíóúüñ"):
        return "es"
    tokens = {t for t in text.replace(",", " ").replace(".", " ").split() if t}
    spanish_markers = {"el", "la", "los", "las", "un", "una", "unos", "unas", "de", "con", "y"}
    if tokens & spanish_markers:
        return "es"
    return "en"


def format_response(bev: Beverage, lang: str) -> str:
    calories = f"{int(bev.calories)}" if bev.calories is not None and bev.calories.is_integer() else f"{bev.calories}" if bev.calories is not None else "N/D"
    fat = f"{int(bev.total_fat)}" if bev.total_fat is not None and bev.total_fat.is_integer() else f"{bev.total_fat}" if bev.total_fat is not None else "N/D"
    price = f"${bev.price:.2f}" if bev.price is not None else "N/D"

    if lang == "es":
        return (
            f"Bebida: {bev.name_es} ({bev.name_en})\n"
            f"Preparación: {bev.method}\n"
            f"Calorías: {calories} kcal\n"
            f"Grasa total: {fat} g\n"
            f"Precio: {price}"
        )
    else:
        return (
            f"Drink: {bev.name_en} ({bev.name_es})\n"
            f"Preparation: {bev.method}\n"
            f"Calories: {calories} kcal\n"
            f"Total Fat: {fat} g\n"
            f"Price: {price}"
        )


def format_not_found(query: str, lang: str, suggestions: List[Beverage]) -> str:
    if lang == "es":
        base = f"La bebida '{query}' no está disponible en el menú."
        if suggestions:
            sug = ", ".join(f"{s.name_es} ({s.name_en})" for s in suggestions)
            return f"{base} Quizá te interesen: {sug}."
        return base
    else:
        base = f"The drink '{query}' is not available on the menu."
        if suggestions:
            sug = ", ".join(f"{s.name_en} ({s.name_es})" for s in suggestions)
            return f"{base} You might like: {sug}."
        return base


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Starbucks beverage assistant")
    parser.add_argument("name", nargs="*", help="Beverage name in English or Spanish")
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default=str(Path.cwd() / "beverages.csv"),
        help="Path to the beverages CSV file (default: ./beverages.csv)",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Run a local web server with a simple HTML UI",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for the web server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port for the web server (default: 5000)")
    return parser.parse_args(argv)


def create_app(beverages: List[Beverage], csv_filename: str) -> "Flask":
    if Flask is None:
        raise RuntimeError(
            "Flask no está instalado. Instala con: pip install flask"
        )

    app = Flask(__name__)

    # Precalcular sugerencias populares por nombre (deduplicado)
    def build_top_suggestions(items: List[Beverage], limit: int = 12) -> List[Beverage]:
        counts: Dict[Tuple[str, str], int] = {}
        first_seen: Dict[Tuple[str, str], Beverage] = {}
        for b in items:
            key = (b.name_en, b.name_es)
            counts[key] = counts.get(key, 0) + 1
            if key not in first_seen:
                first_seen[key] = b
        sorted_keys = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
        top: List[Beverage] = []
        for (name_pair, _count) in sorted_keys[:limit]:
            top.append(first_seen[name_pair])
        return top

    top_suggestions: List[Beverage] = build_top_suggestions(beverages)

    @app.get("/")
    def home():
        return render_template("home.html", csv_filename=csv_filename)

    @app.get("/chat")
    def index():
        return render_template("index.html", csv_filename=csv_filename)

    @app.get("/api/suggestions")
    def api_suggestions():
        query = (request.args.get("query") or "").strip()
        lang = (request.args.get("lang") or "").strip().lower()
        if query:
            items = suggest_similar(beverages, query, max_suggestions=10)
        else:
            items = top_suggestions
        return jsonify({
            "ok": True,
            "lang": lang or None,
            "items": [
                {
                    "name_en": b.name_en,
                    "name_es": b.name_es,
                    "method": b.method,
                    "calories": b.calories,
                    "total_fat": b.total_fat,
                    "price": b.price,
                    "image_url": b.image_url,
                }
                for b in items
            ],
        })

    @app.post("/api/search")
    def api_search():
        payload = request.get_json(silent=True) or {}
        query = str(payload.get("query", "")).strip()
        user_lang = str(payload.get("lang", "")).strip().lower()
        if not query:
            return jsonify({"ok": False, "error": "empty_query"}), 400
        lang = user_lang if user_lang in ("es", "en") else detect_language(query)
        match = find_exact_match(beverages, query)
        if match:
            text = format_response(match, lang)
            return jsonify({
                "ok": True,
                "found": True,
                "lang": lang,
                "data": {
                    "name_en": match.name_en,
                    "name_es": match.name_es,
                    "method": match.method,
                    "calories": match.calories,
                    "total_fat": match.total_fat,
                    "price": match.price,
                    "image_url": match.image_url,
                },
                "text": text,
            })
        suggestions = suggest_similar(beverages, query)
        text = format_not_found(query, lang, suggestions)
        return jsonify({
            "ok": True,
            "found": False,
            "lang": lang,
            "suggestions": [
                {
                    "name_en": s.name_en,
                    "name_es": s.name_es,
                    "method": s.method,
                    "calories": s.calories,
                    "total_fat": s.total_fat,
                    "price": s.price,
                    "image_url": s.image_url,
                }
                for s in suggestions
            ],
            "text": text,
        })

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
        # Modo CLI conserva idioma en función de la consulta
        lang = "es" if any(ch in "".join(args.name).lower() for ch in "áéíóúüñ") else "en"
        msg_es = f"No se pudo cargar el CSV: {exc}"
        msg_en = f"Failed to load the CSV: {exc}"
        print(msg_es if lang == "es" else msg_en)
        return 1

    # Modo servidor web
    if args.serve:
        app = create_app(beverages, csv_filename=csv_path.name)
        # Evitar recarga automática en algunos entornos
        app.run(host=args.host, port=args.port, debug=False)
        return 0

    # Modo CLI tradicional
    if not args.name:
        print("Proporciona el nombre de la bebida. Ejemplo: python main.py 'Caffè Latte' --csv ruta\\a\\bebidas.csv")
        return 2

    query = " ".join(args.name).strip()
    lang = detect_language(query)

    match = find_exact_match(beverages, query)
    if match:
        print(format_response(match, lang))
        return 0

    suggestions = suggest_similar(beverages, query)
    print(format_not_found(query, lang, suggestions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
