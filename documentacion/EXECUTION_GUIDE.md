# Guía de Ejecución y Testing

## Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Instalar dependencias
pip install -r requirements.txt

# O usando un entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```

### 2. Configuración (Opcional)

```bash
# Copiar archivo de configuración de ejemplo
copy .env.example .env

# Editar .env según tus necesidades
# Ejemplo de configuraciones disponibles:
# DEFAULT_SEARCH_STRATEGY=fuzzy
# DEFAULT_RESPONSE_STRATEGY=detailed
# DEBUG=true
```

## Ejecución de la Aplicación

### Modo Servidor Web (Recomendado)

```bash
# Usando la nueva aplicación refactorizada
python main_refactored.py --serve

# Con configuraciones personalizadas
python main_refactored.py --serve --host 0.0.0.0 --port 8000 --debug

# La aplicación estará disponible en:
# http://localhost:5000 (por defecto)
# http://localhost:8000 (si usas --port 8000)
```

### Modo CLI

```bash
# Búsqueda simple
python main_refactored.py "Caffè Latte"

# Con archivo CSV personalizado
python main_refactored.py "Americano" --csv mi_archivo.csv

# Ejemplos de búsquedas
python main_refactored.py "Latte"
python main_refactored.py "Café con leche"
python main_refactored.py "Mocha"
```

### Usando la Aplicación Original (Comparación)

```bash
# Para comparar con la versión original
python main.py --serve
```

## Testing de los Endpoints

### 1. Endpoints de API

#### Búsqueda de Bebidas
```bash
# POST /api/search
curl -X POST "http://localhost:5000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Latte", "lang": "es"}'

# Respuesta esperada:
{
  "ok": true,
  "found": true,
  "lang": "es",
  "data": {
    "name_en": "Caffè Latte",
    "name_es": "Café Latte",
    "method": "Tall with 2% Milk",
    "calories": 190.0,
    "total_fat": 7.0,
    "price": 4.15,
    "image_url": "...",
    "description": "..."
  },
  "text": "Bebida: Café Latte\nTiempo de preparación: ..."
}
```

#### Obtener Sugerencias
```bash
# GET /api/suggestions
curl "http://localhost:5000/api/suggestions?query=coffee&lang=es"

# Sugerencias populares (sin query)
curl "http://localhost:5000/api/suggestions"

# Respuesta esperada:
{
  "ok": true,
  "lang": "es",
  "items": [
    {
      "name_en": "Americano",
      "name_es": "Americano",
      "method": "Grande Hot",
      "calories": 15.0,
      "total_fat": 0.0,
      "price": 2.95,
      "image_url": "...",
      "description": "..."
    }
  ]
}
```

### 2. Vistas HTML

#### Página Principal
```bash
# Abrir en navegador
http://localhost:5000/

# Características:
# - Landing page estilo Starbucks
# - Botón de chat flotante
# - Iframe integrado del chat
```

#### Interfaz de Chat
```bash
# Abrir en navegador
http://localhost:5000/chat

# Características:
# - Widget de chat interactivo
# - Selector de idioma
# - Sugerencias con imágenes
# - Tarjetas de bebidas
```

## Testing con Diferentes Estrategias

### 1. Configurar Estrategias via Código

```python
from app.services.beverage_service import BeverageService
from app.strategies.search_strategy import FuzzySearchStrategy
from app.strategies.response_strategy import DetailedResponseStrategy
from pathlib import Path

# Crear servicio
service = BeverageService(Path("starbucks2.csv"))

# Cambiar a búsqueda difusa
service.set_search_strategy(FuzzySearchStrategy(threshold=0.6))

# Cambiar a respuestas detalladas
service.set_response_strategy(DetailedResponseStrategy())

# Probar búsqueda
result = service.search_beverage("Caffe Latte")  # Sin acento
print(service.format_found_response(result))
```

### 2. Configurar Estrategias via Variables de Entorno

```bash
# Archivo .env
DEFAULT_SEARCH_STRATEGY=fuzzy
DEFAULT_RESPONSE_STRATEGY=detailed
DEFAULT_PRICE_STRATEGY=premium

# Reiniciar aplicación para aplicar cambios
python main_refactored.py --serve
```

### 3. Ejemplos de Testing Manual

#### Test de Búsqueda Exacta
```bash
# Debería encontrar coincidencia exacta
curl -X POST "http://localhost:5000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Americano"}'
```

#### Test de Búsqueda Difusa
```bash
# Debería encontrar a pesar del error tipográfico
curl -X POST "http://localhost:5000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Capuccino"}'  # Mal escrito
```

#### Test de Búsqueda Sin Resultados
```bash
# Debería devolver sugerencias
curl -X POST "http://localhost:5000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Té Verde"}'  # No existe
```

## Testing Unitario

### Ejecutar Tests

```bash
# Instalar pytest si no está instalado
pip install pytest

# Ejecutar todos los tests
pytest tests/

# Ejecutar tests específicos
pytest tests/test_strategies.py

# Con cobertura
pip install pytest-cov
pytest --cov=app tests/

# Con output detallado
pytest -v tests/
```

### Estructura de Tests

```
tests/
├── __init__.py
├── test_strategies.py      # Tests de todas las estrategias
├── test_service.py         # Tests del servicio principal (futuro)
└── test_api.py            # Tests de endpoints (futuro)
```

### Ejemplo de Test Personalizado

```python
# tests/test_custom.py
import pytest
from app.services.beverage_service import BeverageService
from pathlib import Path

def test_custom_search():
    service = BeverageService(Path("starbucks2.csv"))
    
    # Test búsqueda en español
    result = service.search_beverage("Café Latte")
    assert result is not None
    assert "Latte" in result.name_en
    
    # Test sugerencias
    suggestions = service.get_suggestions("Coffee", max_suggestions=3)
    assert len(suggestions) <= 3
    assert all(hasattr(s, 'name_en') for s in suggestions)
```

## Benchmarking y Performance

### 1. Comparar Estrategias de Búsqueda

```python
import time
from app.strategies.search_strategy import ExactMatchStrategy, FuzzySearchStrategy

def benchmark_search_strategies():
    # Cargar datos
    service = BeverageService(Path("starbucks2.csv"))
    beverages = service.beverages
    
    strategies = [
        ("Exact", ExactMatchStrategy()),
        ("Fuzzy", FuzzySearchStrategy()),
    ]
    
    queries = ["Latte", "Americano", "Cappuccino", "Mocha"]
    
    for name, strategy in strategies:
        start_time = time.time()
        for query in queries * 100:  # 400 búsquedas
            strategy.search(beverages, query)
        end_time = time.time()
        print(f"{name}: {end_time - start_time:.4f}s")
```

### 2. Monitorear Memoria

```python
import tracemalloc

def monitor_memory():
    tracemalloc.start()
    
    # Cargar servicio
    service = BeverageService(Path("starbucks2.csv"))
    
    # Realizar operaciones
    for i in range(100):
        service.search_beverage(f"Query {i}")
    
    current, peak = tracemalloc.get_traced_memory()
    print(f"Memoria actual: {current / 1024 / 1024:.1f} MB")
    print(f"Pico de memoria: {peak / 1024 / 1024:.1f} MB")
    tracemalloc.stop()
```

## Troubleshooting

### Problemas Comunes

#### 1. Error de CSV no encontrado
```bash
# Error: FileNotFoundError: No se encontró el archivo CSV
# Solución: Verificar que starbucks2.csv existe en el directorio raíz
ls starbucks2.csv

# O especificar ruta completa
python main_refactored.py --csv "ruta/completa/al/archivo.csv" --serve
```

#### 2. Error de importación
```bash
# Error: ModuleNotFoundError: No module named 'app'
# Solución: Ejecutar desde el directorio raíz del proyecto
cd "c:\Users\RIDUCO\Desktop\proyecto_chatbot V2"
python main_refactored.py --serve
```

#### 3. Puerto ocupado
```bash
# Error: [Errno 10048] Only one usage of each socket address
# Solución: Usar puerto diferente
python main_refactored.py --serve --port 8000
```

#### 4. Problemas de encoding del CSV
```bash
# Si hay problemas con caracteres especiales
# El código maneja automáticamente múltiples encodings:
# utf-8-sig, utf-8, cp1252, latin-1
```

### Logs y Debugging

#### Habilitar Debug Mode
```bash
# Via comando
python main_refactored.py --serve --debug

# Via variable de entorno
set DEBUG=true
python main_refactored.py --serve
```

#### Logs Detallados
```python
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# En el código del servicio
logger = logging.getLogger(__name__)
logger.debug(f"Searching for: {query}")
logger.info(f"Found {len(results)} results")
```

## Extensión y Personalización

### Agregar Nueva Estrategia de Búsqueda

```python
# app/strategies/search_strategy.py
class CustomSearchStrategy(SearchStrategy):
    def search(self, beverages: List[Beverage], query: str) -> Optional[Beverage]:
        # Implementar lógica personalizada
        pass

# Usar la nueva estrategia
service.set_search_strategy(CustomSearchStrategy())
```

### Agregar Nuevo Endpoint

```python
# app/api/routes.py
@api_router.get("/custom-endpoint")
async def custom_endpoint(service: BeverageService = Depends(get_beverage_service)):
    # Implementar funcionalidad personalizada
    return {"message": "Custom endpoint"}
```

### Configuración Avanzada

```python
# app/core/config.py
class Settings(BaseSettings):
    # Agregar nuevas configuraciones
    custom_feature_enabled: bool = False
    max_suggestions: int = 10
    cache_ttl: int = 3600
```

Esta guía proporciona todo lo necesario para ejecutar, probar y extender la aplicación refactorizada con patrón Strategy.
