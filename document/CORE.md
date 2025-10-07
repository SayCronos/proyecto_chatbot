# ⚙️ Documentación de la Carpeta `app/core/`

## 🎯 **Propósito General**

La carpeta `app/core/` es el **centro de configuración** de toda la aplicación. Contiene la configuración global, las dependencias centralizadas y los parámetros que controlan cómo funciona todo el sistema.

## 📁 **Estructura de Archivos**

```
app/core/
├── __init__.py          # Inicialización del módulo core
├── config.py           # ⚙️ Configuración global de la aplicación
└── dependencies.py     # 🔌 Inyección de dependencias centralizadas
```

---

## 📄 **Descripción Detallada de Cada Archivo**

### 1. ⚙️ **`config.py`** - Configuración Global

**Propósito**: Define todos los parámetros de configuración de la aplicación en un lugar centralizado.

#### **🎯 Funcionalidades:**
- **Configuración del servidor** (host, puerto, debug)
- **Rutas de archivos** (CSV de productos)
- **Estrategias por defecto** (búsqueda, precios, respuestas)
- **Metadatos de la aplicación** (nombre, versión)

#### **📋 Parámetros de Configuración:**

##### **🖥️ Configuración del Servidor:**
```python
nombre_app: str = "Asistente de Bebidas Starbucks"
version_app: str = "2.0.0"
debug: bool = False
host: str = "127.0.0.1"        # IP del servidor
puerto: int = 8000             # Puerto de la aplicación
```

##### **📂 Archivos y Rutas:**
```python
ruta_archivo_csv: str = "starbucks2.csv"  # Archivo de productos
```

##### **🧠 Estrategias por Defecto:**
```python
estrategia_busqueda_default: str = "compuesta"    # Tipo de búsqueda
estrategia_precio_default: str = "premium"        # Cálculo de precios
estrategia_respuesta_default: str = "estandar"    # Formato de respuestas
estrategia_sugerencia_default: str = "hibrida"    # Algoritmo de sugerencias
```

#### **🔧 Características Técnicas:**
- **BaseSettings de Pydantic**: Validación automática de tipos
- **Archivo .env**: Soporte para variables de entorno
- **Instancia global**: `configuracion = Configuracion()`

#### **📝 Ejemplo de Uso:**
```python
from app.core.config import configuracion

# Acceder a configuración
print(f"Aplicación: {configuracion.nombre_app}")
print(f"Puerto: {configuracion.puerto}")
print(f"CSV: {configuracion.ruta_archivo_csv}")
```

#### **🌍 Variables de Entorno (.env):**
```bash
# Archivo .env (opcional)
DEBUG=true
HOST=0.0.0.0
PUERTO=8080
RUTA_ARCHIVO_CSV=productos.csv
```

---

### 2. 🔌 **`dependencies.py`** - Inyección de Dependencias

**Propósito**: Centraliza la creación y configuración de todos los servicios y estrategias de la aplicación.

#### **🎯 Funcionalidades:**
- **Inyección de dependencias** para FastAPI
- **Configuración automática** de estrategias
- **Cache de servicios** para optimización
- **Patrón Strategy** implementado

#### **🏭 Servicios Creados:**

##### **🔍 Servicio de Bebidas:**
```python
@lru_cache()
def get_beverage_service() -> BeverageService:
    """
    Crea y configura el servicio principal de bebidas
    con todas las estrategias según configuración.
    """
```

##### **⚙️ Servicio de Configuración:**
```python
def get_settings():
    """Inyecta la configuración global."""
    return settings
```

#### **🧠 Estrategias Configuradas Automáticamente:**

##### **🔍 Estrategias de Búsqueda:**
- **`exact`**: Búsqueda exacta (`ExactMatchStrategy`)
- **`fuzzy`**: Búsqueda difusa (`FuzzySearchStrategy`) 
- **`composite`**: Búsqueda compuesta (`CompositeSearchStrategy`) ⭐ *Por defecto*

##### **💰 Estrategias de Precio:**
- **`basic`**: Precios básicos (`BasicPriceStrategy`)
- **`family`**: Precios por familia (`FamilyBasedPriceStrategy`)
- **`premium`**: Precios premium (`PremiumPriceStrategy`) ⭐ *Por defecto*

##### **📝 Estrategias de Respuesta:**
- **`detailed`**: Respuestas detalladas (`DetailedResponseStrategy`)
- **`compact`**: Respuestas compactas (`CompactResponseStrategy`)
- **`standard`**: Respuestas estándar (`StandardResponseStrategy`) ⭐ *Por defecto*

##### **💡 Estrategias de Sugerencias:**
- **`similarity`**: Por similitud (`SimilarityBasedSuggestionStrategy`)
- **`hybrid`**: Híbrida (`HybridSuggestionStrategy`) ⭐ *Por defecto*

#### **🔧 Flujo de Configuración:**
```python
# 1. Lee configuración de config.py
# 2. Crea BeverageService con CSV
# 3. Configura estrategias según configuración
# 4. Aplica cache con @lru_cache()
# 5. Retorna servicio configurado
```

#### **📝 Ejemplo de Uso en API:**
```python
from app.core.dependencies import get_beverage_service

@router.post("/api/buscar")
async def buscar(
    consulta: str,
    servicio: BeverageService = Depends(get_beverage_service)
):
    # El servicio ya viene configurado con todas las estrategias
    return servicio.buscar_bebida(consulta)
```

---

### 3. 📦 **`__init__.py`** - Inicialización del Módulo

**Propósito**: Hace que la carpeta `core` sea un módulo Python y expone la configuración.

#### **🎯 Funcionalidades:**
- **Exporta configuración**: `from .config import configuracion`
- **Módulo Python**: Permite importar desde `app.core`

#### **📝 Uso:**
```python
# Importar configuración desde cualquier parte
from app.core import configuracion
```

---

## 🔄 **Flujo de Funcionamiento**

### **1. Inicio de la Aplicación:**
```
main.py → app.core.config → Carga configuración → Aplica settings
```

### **2. Creación de Servicios:**
```
API Request → Depends(get_beverage_service) → dependencies.py → Servicio configurado
```

### **3. Configuración de Estrategias:**
```
config.py (estrategia_default) → dependencies.py → Strategy Pattern → Servicio listo
```

---

## 🎯 **Patrón de Diseño: Dependency Injection**

### **🔧 Cómo Funciona:**
```python
# 1. Definir dependencia
@lru_cache()
def get_beverage_service() -> BeverageService:
    return BeverageService(configuracion.ruta_archivo_csv)

# 2. Inyectar en endpoint
@router.post("/api/endpoint")
async def endpoint(servicio: BeverageService = Depends(get_beverage_service)):
    return servicio.hacer_algo()

# 3. FastAPI inyecta automáticamente
```

### **✅ Ventajas:**
- **Reutilización**: Un servicio para toda la app
- **Testing**: Fácil de mockear para pruebas
- **Performance**: Cache con `@lru_cache()`
- **Configuración**: Centralizada y consistente

---

## 🔧 **Configuración Avanzada**

### **🌍 Variables de Entorno:**
```bash
# .env
DEBUG=true
HOST=0.0.0.0
PUERTO=8080
ESTRATEGIA_BUSQUEDA_DEFAULT=fuzzy
ESTRATEGIA_PRECIO_DEFAULT=family
```

### **🔄 Cambiar Configuración en Runtime:**
```python
# Cambiar estrategia dinámicamente
servicio = get_beverage_service()
servicio.set_search_strategy(FuzzySearchStrategy())
```

### **🧪 Configuración para Testing:**
```python
# test_config.py
class TestConfig(Configuracion):
    debug = True
    ruta_archivo_csv = "test_data.csv"
```

---

## 🚀 **Cómo Extender la Configuración**

### **1. Agregar Nueva Configuración:**
```python
# En config.py
class Configuracion(BaseSettings):
    # ... configuración existente ...
    
    # Nueva configuración
    max_resultados: int = 10
    timeout_api: int = 30
    cache_ttl: int = 3600
```

### **2. Crear Nueva Dependencia:**
```python
# En dependencies.py
@lru_cache()
def get_cache_service() -> CacheService:
    return CacheService(
        ttl=configuracion.cache_ttl,
        max_size=configuracion.max_resultados
    )
```

### **3. Usar en API:**
```python
@router.get("/api/cached-data")
async def get_cached_data(
    cache: CacheService = Depends(get_cache_service)
):
    return cache.get_data()
```

---

## 📊 **Configuraciones por Entorno**

### **🔧 Desarrollo:**
```python
debug = True
host = "127.0.0.1"
estrategia_busqueda_default = "fuzzy"  # Más flexible
```

### **🚀 Producción:**
```python
debug = False
host = "0.0.0.0"
estrategia_busqueda_default = "compuesta"  # Más precisa
```

### **🧪 Testing:**
```python
debug = True
ruta_archivo_csv = "test_starbucks.csv"
estrategia_busqueda_default = "exact"  # Predecible
```

---

## 🎯 **Puntos Clave para Entender**

### **1. Centralización:**
- **Una sola fuente** de configuración
- **Consistencia** en toda la aplicación
- **Fácil mantenimiento** y cambios

### **2. Flexibilidad:**
- **Variables de entorno** para diferentes despliegues
- **Estrategias intercambiables** según necesidades
- **Configuración dinámica** posible

### **3. Performance:**
- **Cache de servicios** con `@lru_cache()`
- **Instancia única** de configuración
- **Lazy loading** de dependencias

### **4. Testing:**
- **Dependencias mockeables**
- **Configuración de prueba** separada
- **Inyección controlada** para tests

---

## 🔍 **Debugging y Monitoreo**

### **📊 Ver Configuración Actual:**
```python
from app.core.config import configuracion
print(configuracion.dict())  # Muestra toda la configuración
```

### **🔧 Validar Dependencias:**
```python
servicio = get_beverage_service()
print(f"Estrategia actual: {type(servicio.search_strategy).__name__}")
```

---

**🎯 Esta carpeta es el cerebro de configuración que controla cómo se comporta toda tu aplicación Starbucks.**
