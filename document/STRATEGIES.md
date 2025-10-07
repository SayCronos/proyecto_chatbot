# 🧠 Documentación de la Carpeta `app/strategies/`

## 🎯 **Propósito General**

La carpeta `app/strategies/` implementa el **patrón Strategy** para hacer que el chatbot sea inteligente y configurable. Contiene diferentes algoritmos intercambiables para búsqueda, precios, respuestas y sugerencias, permitiendo cambiar el comportamiento sin modificar el código principal.

## 📁 **Estructura de Archivos**

```
app/strategies/
├── __init__.py                    # Exportaciones del módulo
├── estrategias_busqueda.py       # 🔍 Algoritmos de búsqueda (español)
├── estrategias_precio.py         # 💰 Cálculo de precios (español)
├── estrategias_respuesta.py      # 📝 Formateo de respuestas (español)
├── estrategias_sugerencia.py     # 💡 Generación de sugerencias (español)
├── search_strategy.py            # 🔍 Algoritmos de búsqueda (inglés/legacy)
├── price_strategy.py             # 💰 Cálculo de precios (inglés/legacy)
├── response_strategy.py          # 📝 Formateo de respuestas (inglés/legacy)
└── suggestion_strategy.py        # 💡 Generación de sugerencias (inglés/legacy)
```

---

## 📄 **Descripción Detallada de Cada Archivo**

### 1. 🔍 **`estrategias_busqueda.py`** - Algoritmos de Búsqueda

**Propósito**: Implementa diferentes algoritmos para buscar bebidas según la consulta del usuario.

#### **🎯 Interfaz Base:**
```python
class EstrategiaBusqueda(ABC):
    """Interfaz abstracta para estrategias de búsqueda."""
    
    @abstractmethod
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """Busca una bebida usando la estrategia específica."""
        pass
```

#### **🔧 Estrategias Implementadas:**

##### **1. Coincidencia Exacta:**
```python
class EstrategiaCoincidenciaExacta(EstrategiaBusqueda):
    """Estrategia de búsqueda por coincidencia exacta."""
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """
        Busca coincidencia exacta tras normalización.
        - Elimina acentos y espacios extra
        - Convierte a minúsculas
        - Comparación exacta de strings
        """
```

**Características:**
- **Normalización**: Elimina acentos con `unicodedata`
- **Limpieza**: Remueve espacios extra y caracteres especiales
- **Case-insensitive**: Convierte todo a minúsculas
- **Precisión alta**: Solo coincidencias exactas

##### **2. Búsqueda Difusa:**
```python
class EstrategiaBusquedaDifusa(EstrategiaBusqueda):
    """Estrategia de búsqueda difusa tolerante a errores."""
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """
        Busca usando similitud de texto.
        - Usa difflib.SequenceMatcher
        - Umbral de similitud configurable
        - Tolerante a errores de escritura
        """
```

**Características:**
- **Tolerancia a errores**: "latte" encuentra "Latte"
- **Similitud**: Usa ratio de 0.6 como umbral
- **Flexibilidad**: Encuentra coincidencias aproximadas
- **Algoritmo**: difflib.SequenceMatcher de Python

##### **3. Búsqueda Compuesta:**
```python
class EstrategiaBusquedaCompuesta(EstrategiaBusqueda):
    """Estrategia que combina múltiples enfoques de búsqueda."""
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        """
        Combina estrategias en orden de prioridad:
        1. Coincidencia exacta (más precisa)
        2. Búsqueda difusa (más flexible)
        3. Búsqueda por contenido (más amplia)
        """
```

**Características:**
- **Estrategia híbrida**: Combina lo mejor de cada algoritmo
- **Prioridad**: Exacta → Difusa → Contenido
- **Inteligente**: Se adapta al tipo de consulta
- **Por defecto**: Estrategia recomendada

#### **🔧 Métodos Auxiliares:**
```python
def _normalizar_para_comparacion(self, texto: str) -> str:
    """Normaliza texto para comparación consistente."""

def _quitar_acentos(self, texto: str) -> str:
    """Elimina acentos del texto usando unicodedata."""

def _limpiar_texto(self, texto: str) -> str:
    """Limpia espacios y caracteres especiales."""
```

---

### 2. 💰 **`estrategias_precio.py`** - Cálculo de Precios

**Propósito**: Implementa diferentes algoritmos para estimar precios de bebidas cuando no están disponibles en el CSV.

#### **🎯 Interfaz Base:**
```python
class EstrategiaEstimacionPrecio(ABC):
    """Interfaz abstracta para estrategias de estimación de precios."""
    
    @abstractmethod
    def estimar_precio(self, bebida: Bebida) -> float:
        """Estima el precio de una bebida."""
        pass
```

#### **🔧 Estrategias Implementadas:**

##### **1. Precio Básico:**
```python
class EstrategiaPrecioBasico(EstrategiaEstimacionPrecio):
    """Estrategia básica de precios por tamaño."""
    
    def estimar_precio(self, bebida: Bebida) -> float:
        """
        Estima precio basado en tamaño inferido.
        Precios base:
        - Short: $3.20
        - Tall: $3.50  (por defecto)
        - Grande: $4.00
        - Venti: $4.60
        """
```

##### **2. Precio por Familia:**
```python
class EstrategiaPrecioPorFamilia(EstrategiaEstimacionPrecio):
    """Estrategia de precios basada en familia de bebidas."""
    
    def estimar_precio(self, bebida: Bebida) -> float:
        """
        Estima precio por tipo de bebida:
        - Espresso: $3.50-4.50
        - Frappuccino: $4.50-5.50
        - Té: $2.50-3.50
        - Bebidas especiales: $5.00-6.00
        """
```

##### **3. Precio Premium:**
```python
class EstrategiaPrecioPremium(EstrategiaEstimacionPrecio):
    """Estrategia de precios premium con factores múltiples."""
    
    def estimar_precio(self, bebida: Bebida) -> float:
        """
        Cálculo sofisticado considerando:
        - Tamaño base
        - Complejidad de preparación
        - Ingredientes especiales
        - Factor premium de Starbucks
        """
```

#### **🔧 Contexto de Estrategia:**
```python
class ContextoEstrategiaPrecio:
    """Contexto para manejar estrategias de precio."""
    
    def __init__(self, estrategia: EstrategiaEstimacionPrecio):
        self.estrategia = estrategia
    
    def establecer_estrategia(self, estrategia: EstrategiaEstimacionPrecio):
        """Cambia la estrategia de precio dinámicamente."""
        self.estrategia = estrategia
    
    def calcular_precio(self, bebida: Bebida) -> float:
        """Calcula precio usando la estrategia actual."""
        return self.estrategia.estimar_precio(bebida)
```

---

### 3. 📝 **`estrategias_respuesta.py`** - Formateo de Respuestas

**Propósito**: Implementa diferentes formatos para las respuestas del chatbot según el contexto y preferencias.

#### **🎯 Interfaz Base:**
```python
class EstrategiaFormateoRespuesta(ABC):
    """Interfaz abstracta para estrategias de formateo de respuestas."""
    
    @abstractmethod
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """Formatea la respuesta cuando se encuentra una bebida."""
        pass
    
    @abstractmethod
    def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
        """Formatea la respuesta cuando no se encuentra una bebida."""
        pass
```

#### **🔧 Estrategias Implementadas:**

##### **1. Respuesta Estándar:**
```python
class EstrategiaRespuestaEstandar(EstrategiaFormateoRespuesta):
    """Estrategia estándar de formateo de respuestas."""
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """
        Formato estándar:
        Bebida: [Nombre]
        Tiempo de preparación: [Tiempo]
        Calorías: [Calorías] kcal
        Grasa total: [Grasa] g
        Precio: $[Precio]
        [Descripción opcional]
        """
```

##### **2. Respuesta Detallada:**
```python
class EstrategiaRespuestaDetallada(EstrategiaFormateoRespuesta):
    """Estrategia detallada con información completa."""
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """
        Formato detallado:
        ☕ [Nombre] ☕
        📋 Información nutricional completa
        ⏱️ Tiempo de preparación detallado
        💰 Precio con comparación
        📝 Descripción extendida
        🔗 Enlace a imagen
        """
```

##### **3. Respuesta Compacta:**
```python
class EstrategiaRespuestaCompacta(EstrategiaFormateoRespuesta):
    """Estrategia compacta para respuestas breves."""
    
    def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
        """
        Formato compacto:
        [Nombre] - $[Precio] - [Tiempo]
        [Descripción breve]
        """
```

#### **🔧 Contexto de Formateo:**
```python
class ContextoFormateoRespuesta:
    """Contexto para manejar estrategias de formateo."""
    
    def __init__(self, estrategia: EstrategiaFormateoRespuesta):
        self.estrategia = estrategia
    
    def establecer_estrategia(self, estrategia: EstrategiaFormateoRespuesta):
        """Cambia la estrategia de formateo dinámicamente."""
        self.estrategia = estrategia
```

---

### 4. 💡 **`estrategias_sugerencia.py`** - Generación de Sugerencias

**Propósito**: Implementa algoritmos inteligentes para generar sugerencias cuando no se encuentra una bebida exacta.

#### **🎯 Interfaz Base:**
```python
class EstrategiaSugerencia(ABC):
    """Interfaz abstracta para estrategias de generación de sugerencias."""
    
    @abstractmethod
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias basadas en la consulta."""
        pass
```

#### **🔧 Estrategias Implementadas:**

##### **1. Sugerencias por Similitud:**
```python
class EstrategiaSugerenciaPorSimilitud(EstrategiaSugerencia):
    """Estrategia de sugerencias basada en similitud de texto."""
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """
        Genera sugerencias usando:
        - Similitud de texto (difflib)
        - Solapamiento de tokens
        - Puntuación combinada
        - Eliminación de duplicados
        """
```

**Algoritmo:**
1. **Normalización**: Consulta y nombres de bebidas
2. **Tokenización**: División en palabras
3. **Similitud**: Ratio de difflib.SequenceMatcher
4. **Solapamiento**: Tokens comunes entre consulta y nombre
5. **Puntuación**: Combinación ponderada de ambos factores
6. **Ranking**: Ordenamiento por puntuación descendente

##### **2. Sugerencias Híbridas:**
```python
class EstrategiaSugerenciaHibrida(EstrategiaSugerencia):
    """Estrategia híbrida que combina múltiples enfoques."""
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """
        Combina múltiples algoritmos:
        1. Similitud de texto
        2. Búsqueda por contenido
        3. Popularidad de bebidas
        4. Categorización inteligente
        """
```

**Características avanzadas:**
- **Multi-algoritmo**: Combina diferentes enfoques
- **Ponderación inteligente**: Ajusta pesos según contexto
- **Diversidad**: Evita sugerencias muy similares
- **Aprendizaje**: Se adapta a patrones de búsqueda

#### **🔧 Contexto de Sugerencias:**
```python
class ContextoSugerencia:
    """Contexto para manejar estrategias de sugerencias."""
    
    def __init__(self, estrategia: EstrategiaSugerencia):
        self.estrategia = estrategia
    
    def establecer_estrategia(self, estrategia: EstrategiaSugerencia):
        """Cambia la estrategia de sugerencias dinámicamente."""
        self.estrategia = estrategia
    
    def generar_sugerencias(self, bebidas: List[Bebida], consulta: str, max_sugerencias: int = 3) -> List[Bebida]:
        """Genera sugerencias usando la estrategia actual."""
        return self.estrategia.generar_sugerencias(bebidas, consulta, max_sugerencias)
```

---

### 5. 📦 **`__init__.py`** - Exportaciones del Módulo

**Propósito**: Hace que la carpeta `strategies` sea un módulo Python y exporta todas las estrategias.

#### **🎯 Exportaciones:**
```python
# Estrategias de búsqueda
from .estrategias_busqueda import (
    EstrategiaBusqueda, 
    EstrategiaCoincidenciaExacta, 
    EstrategiaBusquedaDifusa, 
    EstrategiaBusquedaCompuesta
)

# Estrategias de precio
from .estrategias_precio import (
    EstrategiaEstimacionPrecio, 
    EstrategiaPrecioBasico, 
    EstrategiaPrecioPorFamilia, 
    EstrategiaPrecioPremium
)

# Estrategias de respuesta
from .estrategias_respuesta import (
    EstrategiaFormateoRespuesta, 
    EstrategiaRespuestaEstandar, 
    EstrategiaRespuestaDetallada, 
    EstrategiaRespuestaCompacta
)

# Estrategias de sugerencia
from .estrategias_sugerencia import (
    EstrategiaSugerencia, 
    EstrategiaSugerenciaPorSimilitud, 
    EstrategiaSugerenciaHibrida
)
```

---

## 🧠 **Patrón Strategy Explicado**

### **🎯 ¿Qué es el Patrón Strategy?**

El patrón Strategy permite definir una familia de algoritmos, encapsularlos y hacerlos intercambiables. El algoritmo puede variar independientemente de los clientes que lo usan.

### **🔧 Componentes del Patrón:**

#### **1. Estrategia (Strategy):**
```python
class EstrategiaBusqueda(ABC):
    @abstractmethod
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        pass
```

#### **2. Estrategia Concreta (Concrete Strategy):**
```python
class EstrategiaCoincidenciaExacta(EstrategiaBusqueda):
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        # Implementación específica
        pass
```

#### **3. Contexto (Context):**
```python
class ServicioBebidas:
    def __init__(self):
        self.estrategia_busqueda = EstrategiaBusquedaCompuesta()
    
    def establecer_estrategia_busqueda(self, estrategia: EstrategiaBusqueda):
        self.estrategia_busqueda = estrategia
    
    def buscar_bebida(self, consulta: str):
        return self.estrategia_busqueda.buscar(self.bebidas, consulta)
```

### **✅ Ventajas del Patrón Strategy:**

1. **Flexibilidad**: Cambiar algoritmos sin modificar código
2. **Extensibilidad**: Agregar nuevas estrategias fácilmente
3. **Mantenibilidad**: Cada algoritmo en su propia clase
4. **Testing**: Probar cada estrategia independientemente
5. **Configuración**: Cambiar comportamiento dinámicamente

---

## 🔄 **Flujo de Funcionamiento**

### **1. Inicialización:**
```
ServicioBebidas → Carga estrategias por defecto → Listo para usar
```

### **2. Búsqueda:**
```
Usuario: "latte" → EstrategiaBusquedaCompuesta → Exacta → Difusa → Resultado
```

### **3. Sugerencias:**
```
No encontrado → EstrategiaSugerenciaHibrida → Similitud + Popularidad → Lista
```

### **4. Formateo:**
```
Resultado → EstrategiaRespuestaEstandar → Texto formateado → Usuario
```

---

## 🚀 **Cómo Extender las Estrategias**

### **1. Crear Nueva Estrategia de Búsqueda:**
```python
class EstrategiaBusquedaPorIngredientes(EstrategiaBusqueda):
    """Búsqueda por ingredientes de la bebida."""
    
    def buscar(self, bebidas: List[Bebida], consulta: str) -> Optional[Bebida]:
        # Buscar en descripción por ingredientes
        for bebida in bebidas:
            if consulta.lower() in (bebida.descripcion or "").lower():
                return bebida
        return None
```

### **2. Usar Nueva Estrategia:**
```python
# En servicio_bebidas.py
servicio.establecer_estrategia_busqueda(EstrategiaBusquedaPorIngredientes())
```

### **3. Configurar en core/config.py:**
```python
# Agregar nueva opción
estrategia_busqueda_default: str = "ingredientes"

# En dependencies.py
if settings.default_search_strategy == "ingredientes":
    service.set_search_strategy(EstrategiaBusquedaPorIngredientes())
```

---

## 🧪 **Testing de Estrategias**

### **📋 Testing Individual:**
```python
def test_estrategia_coincidencia_exacta():
    estrategia = EstrategiaCoincidenciaExacta()
    bebidas = [Bebida(nombre_es="Latte", ...)]
    
    resultado = estrategia.buscar(bebidas, "latte")
    assert resultado is not None
    assert resultado.nombre_es == "Latte"
```

### **🔄 Testing de Contexto:**
```python
def test_cambio_de_estrategia():
    servicio = ServicioBebidas(Path("test.csv"))
    
    # Estrategia inicial
    servicio.establecer_estrategia_busqueda(EstrategiaCoincidenciaExacta())
    resultado1 = servicio.buscar_bebida("late")  # Error de escritura
    assert resultado1 is None
    
    # Cambiar a estrategia difusa
    servicio.establecer_estrategia_busqueda(EstrategiaBusquedaDifusa())
    resultado2 = servicio.buscar_bebida("late")  # Mismo error
    assert resultado2 is not None  # Ahora encuentra "Latte"
```

---

## 📊 **Configuraciones Recomendadas**

### **🔧 Desarrollo:**
```python
estrategia_busqueda = "difusa"      # Más tolerante a errores
estrategia_precio = "basico"        # Cálculos simples
estrategia_respuesta = "detallada"  # Más información para debug
estrategia_sugerencia = "similitud" # Algoritmo predecible
```

### **🚀 Producción:**
```python
estrategia_busqueda = "compuesta"   # Mejor experiencia usuario
estrategia_precio = "premium"       # Cálculos sofisticados
estrategia_respuesta = "estandar"   # Balance información/velocidad
estrategia_sugerencia = "hibrida"   # Recomendaciones inteligentes
```

### **🧪 Testing:**
```python
estrategia_busqueda = "exacta"      # Resultados predecibles
estrategia_precio = "basico"        # Cálculos determinísticos
estrategia_respuesta = "compacta"   # Respuestas simples
estrategia_sugerencia = "similitud" # Algoritmo conocido
```

---

## 🎯 **Puntos Clave para Entender**

### **1. Intercambiabilidad:**
- **Mismo resultado**: Todas las estrategias del mismo tipo devuelven el mismo formato
- **Diferente algoritmo**: Cada una usa un enfoque distinto
- **Configuración dinámica**: Se puede cambiar en runtime

### **2. Extensibilidad:**
- **Nuevas estrategias**: Sin modificar código existente
- **Combinaciones**: Estrategias pueden usar otras estrategias
- **Configuración**: Via archivos de configuración

### **3. Mantenibilidad:**
- **Código separado**: Cada algoritmo en su archivo
- **Responsabilidad única**: Una estrategia, una función
- **Testing independiente**: Cada estrategia se prueba sola

### **4. Performance:**
- **Lazy loading**: Estrategias se cargan cuando se necesitan
- **Cache**: Resultados se pueden cachear por estrategia
- **Optimización**: Cada estrategia optimizada independientemente

---

## 📁 **Estructura Visual:**

```
app/strategies/
├── STRATEGIES.md                  # 📚 NUEVA DOCUMENTACIÓN
├── estrategias_busqueda.py       # 🔍 3 estrategias (170 líneas)
├── estrategias_precio.py         # 💰 3 estrategias (138 líneas)
├── estrategias_respuesta.py      # 📝 3 estrategias (144 líneas)
├── estrategias_sugerencia.py     # 💡 2 estrategias (192 líneas)
├── search_strategy.py            # 🔍 Legacy/inglés
├── price_strategy.py             # 💰 Legacy/inglés
├── response_strategy.py          # 📝 Legacy/inglés
├── suggestion_strategy.py        # 💡 Legacy/inglés
└── __init__.py                   # 📦 Exportaciones (7 líneas)
```

---

**🎯 Esta carpeta implementa la inteligencia artificial de tu chatbot Starbucks, donde cada algoritmo es intercambiable y configurable para diferentes necesidades.**
