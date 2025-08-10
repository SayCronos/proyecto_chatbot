#Chat Bot Asistente de bebidas de Starbucks (CLI + Web)

Proyecto demo que consulta bebidas de Starbucks desde un CSV y ofrece:
- CLI para buscar por nombre (inglés/español)
- Servidor web con landing + chat flotante (widget)
- API JSON para búsqueda y sugerencias

## Características
- Mantiene el idioma de la consulta o lo fuerza vía selector (ES/EN).
- Formato de respuesta: Bebida/Drink, Preparación/Preparation, Calorías/Calories, Grasa total/Total Fat, Precio/Price.
- Sugeriere cuando no hay coincidencia exacta.
- Estimación de precio si el CSV no trae uno (familia + tamaño; recargo por leches alternativas).
- Soporte de imágenes por bebida (columna `Image`/`Imagen`).

## Estructura
```
proyecto/
  main.py                  # CLI + servidor web (Flask)
  starbucks.csv            # CSV de bebidas (tu archivo)
  requirements.txt         # Dependencias (Flask)
  templates/
    home.html              # Landing tipo Starbucks con iframe del chat
    index.html             # Chat (widget flotante)
```

## Requisitos
- Python 3.9+
- Pip/venv

## Instalación
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Uso (CLI)
```powershell
python .\main.py "Caffè Latte" --csv .\starbucks.csv
```
Salida (ES):
```
Bebida: Caffè Latte (Caffè Latte)
Preparación: Tall Nonfat Milk
Calorías: 150 kcal
Grasa total: 0.2 g
Precio: $3.65
```

## Servidor web
```powershell
python .\main.py --serve --csv .\starbucks.csv --host 127.0.0.1 --port 5000
```
- GET `/` → landing tipo Starbucks (Bootstrap) con botón que abre el chat (iframe a `/chat?autopen=1`).
- GET `/chat` → chat completo (widget en esquina inferior derecha). `?autopen=1` lo abre automáticamente.

Abre `http://127.0.0.1:5000` en tu navegador.

### Chat (UI)
- Burbujas, selector de idioma, acciones rápidas (Recomiéndame, Ver populares).
- Sugerencias con miniaturas (si hay `image_url`) y precio.
- Tarjeta con imagen y detalles cuando hay coincidencia.

## API
### POST `/api/search`
Request JSON:
```json
{ "query": "Caffe Latte", "lang": "es" }
```
Respuesta (200) encontrado:
```json
{
  "ok": true,
  "found": true,
  "lang": "es",
  "data": {
    "name_en": "Caffe Latte",
    "name_es": "Caffe Latte",
    "method": "Tall Nonfat Milk",
    "calories": 150,
    "total_fat": 0.2,
    "price": 3.65,
    "image_url": "https://.../latte.jpg"
  },
  "text": "Bebida: ..."
}
```
Respuesta (200) no encontrado (con sugerencias):
```json
{
  "ok": true,
  "found": false,
  "lang": "es",
  "suggestions": [ { "name_en": "Caffè Latte", "price": 3.65, "image_url": "..." } ],
  "text": "La bebida 'X' no está disponible..."
}
```

### GET `/api/suggestions`
- Parámetros opcionales: `?query=latte&lang=es`
- Devuelve sugerencias (o populares si no hay `query`).

## CSV: columnas soportadas
Se detectan equivalencias (normalización sin acentos, guiones y guiones bajos):
- Nombre EN: `Beverage`, `Name EN`, `English Name`.
- Nombre ES (opcional): `Name ES`, `Nombre Español`.
- Método: `Beverage_prep`, `Method`, `Preparation`, `Método de preparación`.
- Calorías: `Calories`, `Calorías (kcal)`.
- Grasa total: `Total Fat (g)`, `Total Fat`, `Grasa total`.
- Categoría (opcional): `Beverage_category`, `Category`.
- Precio (opcional): `Price`, `Precio`, `Price USD`.
- Imagen (opcional): `Image`, `Image URL`, `Imagen`.

### Estimación de precio
- Familias: Brewed Coffee, Americano, Latte, Cappuccino, Mocha.
- Tamaños: Short/Tall/Grande/Venti inferidos desde `method`.
- Recargo por leches alternativas (soya/almendra/avena).

## Personalización
- Color del chat: `--accent: #006241` en `templates/index.html` y `templates/home.html`.
- Autoapertura del chat: `/chat?autopen=1` (la home ya lo usa).

## Problemas comunes
- "Failed to load the CSV": revisa ruta `--csv` y que el CSV tenga encabezados.
- No detecta columnas: confirma encabezados; se soportan `Beverage`, `Beverage_prep`, `Total Fat (g)`, etc.
- Imágenes no se ven: URLs públicas HTTP/HTTPS.
- Puerto ocupado: cambia `--port` (p. ej., `--port 5001`).

## Licencia
Uso educativo/demostrativo.