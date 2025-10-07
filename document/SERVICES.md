# ⚙️ Documentación de la Carpeta `app/services/`

## 🎯 **Propósito General**

La carpeta `app/services/` contiene toda la **lógica de negocio** de la aplicación. Es donde se implementan las funcionalidades principales del chatbot, carrito de compras y gestión de pedidos. Los servicios actúan como intermediarios entre las APIs y los datos.

## 📁 **Estructura de Archivos**

```
app/services/
├── __init__.py              # Inicialización y exportaciones del módulo
├── servicio_bebidas.py     # 🍹 Lógica principal del chatbot (búsqueda, sugerencias)
├── servicio_carrito.py     # 🛒 Gestión del carrito de compras
├── servicio_pedidos.py     # 🗄️ Operaciones de base de datos (pedidos, usuarios)
└── beverage_service.py     # 🍹 Servicio alternativo/legacy (inglés)
```

---

## 📄 **Descripción Detallada de Cada Archivo**

### 1. 🍹 **`servicio_bebidas.py`** - El Cerebro del Chatbot

**Propósito**: Implementa toda la lógica inteligente del chatbot usando el patrón Strategy para búsquedas, precios, respuestas y sugerencias.

#### **🎯 Funcionalidades Principales:**
- **Carga de datos CSV** con mapeo automático de columnas
- **Búsqueda inteligente** con múltiples estrategias
- **Generación de sugerencias** basadas en similitud
- **Formateo de respuestas** personalizables
- **Estimación de precios** con diferentes algoritmos

#### **🧠 Estrategias Integradas:**
```python
class ServicioBebidas:
    def __init__(self, ruta_csv: Path):
        # Estrategias configurables
        self.estrategia_busqueda = EstrategiaBusquedaCompuesta()
        self.contexto_precio = ContextoEstrategiaPrecio(EstrategiaPrecioPremium())
        self.contexto_respuesta = ContextoFormateoRespuesta(EstrategiaRespuestaEstandar())
        self.contexto_sugerencia = ContextoSugerencia(EstrategiaSugerenciaHibrida())
```

#### **🔧 Métodos Principales:**

##### **📊 Carga de Datos:**
```python
def cargar_bebidas(self) -> None:
    """
    Carga las bebidas desde el archivo CSV.
    - Mapeo automático de columnas
    - Normalización de encabezados
    - Validación de datos
    - Manejo de errores
    """
```

##### **🔍 Búsqueda Inteligente:**
```python
def buscar_bebida(self, consulta: str) -> Optional[Bebida]:
    """
    Busca una bebida usando la estrategia de búsqueda configurada.
    - Búsqueda exacta, difusa o compuesta
    - Tolerancia a errores de escritura
    - Búsqueda en múltiples idiomas
    """
```

##### **💡 Sugerencias:**
```python
def obtener_sugerencias(self, consulta: str = "", max_sugerencias: int = 10) -> List[Bebida]:
    """
    Obtiene sugerencias de bebidas.
    - Con consulta: Sugerencias similares
    - Sin consulta: Bebidas más populares
    - Algoritmo híbrido de recomendación
    """
```

##### **📝 Formateo de Respuestas:**
```python
def formatear_respuesta_encontrada(self, bebida: Bebida) -> str:
    """Formatea la respuesta para una bebida encontrada."""

def formatear_respuesta_no_encontrada(self, consulta: str, sugerencias: List[Bebida]) -> str:
    """Formatea la respuesta para una bebida no encontrada."""
```

#### **🔧 Configuración Dinámica:**
```python
# Cambiar estrategias en runtime
servicio.establecer_estrategia_busqueda(EstrategiaBusquedaExacta())
servicio.establecer_estrategia_precio(EstrategiaPrecioBasico())
servicio.establecer_estrategia_respuesta(EstrategiaRespuestaDetallada())
```

#### **📊 Mapeo Automático de CSV:**
El servicio detecta automáticamente la estructura del CSV:
```python
def _adivinar_mapeo_columnas(self, encabezados) -> Dict[str, str]:
    """
    Mapea automáticamente columnas del CSV a campos del modelo.
    Reconoce variaciones como:
    - "nombre_bebida" → "nombre"
    - "tiempo_preparacion" → "metodo"
    - "grasa_total" → "grasa"
    """
```

---

### 2. 🛒 **`servicio_carrito.py`** - Gestión del Carrito

**Propósito**: Maneja toda la lógica del carrito de compras, incluyendo agregar, actualizar, eliminar productos y calcular totales.

#### **🎯 Funcionalidades Principales:**
- **Gestión de sesiones** de carrito
- **Operaciones CRUD** en el carrito
- **Cálculo automático** de totales
- **Validación de productos** existentes
- **Simulación de compra**

#### **🔧 Métodos Principales:**

##### **🛒 Gestión Básica:**
```python
def obtener_carrito(self, sesion_id: str = "default") -> Carrito:
    """
    Obtiene el carrito para una sesión específica.
    - Crea carrito si no existe
    - Manejo de múltiples sesiones
    """
```

##### **➕ Agregar Productos:**
```python
def agregar_al_carrito(self, nombre_bebida: str, cantidad: int = 1, sesion_id: str = "default") -> Dict[str, Any]:
    """
    Agrega una bebida al carrito.
    - Valida que la bebida exista
    - Detecta duplicados y suma cantidades
    - Calcula subtotales automáticamente
    - Actualiza total del carrito
    """
```

##### **🔄 Actualizar Cantidades:**
```python
def actualizar_cantidad(self, nombre_bebida: str, nueva_cantidad: int, sesion_id: str = "default") -> Dict[str, Any]:
    """
    Actualiza la cantidad de un item en el carrito.
    - Valida cantidad positiva
    - Elimina item si cantidad es 0
    - Recalcula totales
    """
```

##### **🗑️ Eliminar Productos:**
```python
def eliminar_del_carrito(self, nombre_bebida: str, sesion_id: str = "default") -> Dict[str, Any]:
    """
    Elimina un item del carrito.
    - Busca item por nombre
    - Actualiza total automáticamente
    - Retorna estado actualizado
    """
```

##### **🧹 Vaciar Carrito:**
```python
def vaciar_carrito(self, sesion_id: str = "default") -> Dict[str, Any]:
    """
    Vacía completamente el carrito.
    - Remueve todos los items
    - Resetea total a 0
    - Mantiene estructura del carrito
    """
```

##### **💳 Finalizar Compra:**
```python
def finalizar_compra(self, sesion_id: str = "default") -> Dict[str, Any]:
    """
    Simula la finalización de una compra.
    - Valida carrito no vacío
    - Genera resumen de compra
    - Vacía carrito después de compra
    """
```

#### **🔄 Flujo de Operaciones:**
```
1. Usuario agrega producto → Validar existencia → Agregar/Actualizar → Calcular total
2. Usuario modifica cantidad → Validar cantidad → Actualizar item → Recalcular
3. Usuario elimina producto → Buscar item → Remover → Actualizar total
4. Usuario finaliza compra → Validar carrito → Procesar → Vaciar carrito
```

---

### 3. 🗄️ **`servicio_pedidos.py`** - Operaciones de Base de Datos

**Propósito**: Maneja todas las operaciones relacionadas con la persistencia de datos en MySQL, incluyendo registro de usuarios y gestión de pedidos.

#### **🎯 Funcionalidades Principales:**
- **Registro de usuarios** en base de datos
- **Creación de pedidos** completos
- **Actualización de pedidos** existentes
- **Consulta de historial** de pedidos
- **Validación y limpieza** de datos

#### **🔧 Métodos Principales:**

##### **👤 Registro de Usuarios:**
```python
@staticmethod
def registrar_usuario(db: Session, usuario_data: UsuarioRegistro) -> Pedido:
    """
    Registra un nuevo usuario en la base de datos.
    - Limpia y valida número de teléfono
    - Crea registro inicial sin bebida
    - Manejo de errores de base de datos
    - Logging de operaciones
    """
```

**Características especiales:**
- **Limpieza de teléfono**: Remueve caracteres no numéricos
- **Validación de longitud**: Limita a 10 dígitos
- **Manejo de overflow**: Previene errores de int(11)

##### **📝 Creación de Pedidos:**
```python
@staticmethod
def crear_pedido_completo(db: Session, pedido_data: PedidoCreate) -> Pedido:
    """
    Crea un pedido completo con bebida y precio.
    - Validación de datos de entrada
    - Inserción en tabla pedido
    - Commit automático de transacción
    - Logging de operaciones
    """
```

##### **🔄 Actualización de Pedidos:**
```python
@staticmethod
def actualizar_pedido_con_bebida(db: Session, usuario_nombre: str, nombre_bebida: str, precio: float) -> Optional[Pedido]:
    """
    Actualiza un pedido existente agregando la bebida y precio.
    - Busca pedido pendiente por usuario
    - Actualiza campos de bebida y precio
    - Retorna pedido actualizado o None
    """
```

##### **📊 Consultas de Pedidos:**
```python
@staticmethod
def obtener_pedidos_usuario(db: Session, nombre_usuario: str) -> List[Pedido]:
    """Obtiene todos los pedidos de un usuario específico."""

@staticmethod
def obtener_todos_pedidos(db: Session, limit: int = 100) -> List[Pedido]:
    """Obtiene todos los pedidos (para administración)."""
```

#### **🔒 Características de Seguridad:**
- **Métodos estáticos**: No mantienen estado
- **Manejo de excepciones**: Try-catch en todas las operaciones
- **Logging**: Registro de todas las operaciones
- **Validación de entrada**: Limpieza de datos antes de insertar

---

### 4. 🍹 **`beverage_service.py`** - Servicio Legacy/Alternativo

**Propósito**: Versión alternativa del servicio de bebidas con nombres en inglés. Posiblemente una versión anterior o para internacionalización.

#### **🎯 Estado Actual:**
- **Funcionalidad similar** a `servicio_bebidas.py`
- **Nombres en inglés**: `BeverageService`, `load_beverages`, etc.
- **Posible versión legacy**: No se usa en la aplicación principal
- **Patrón Strategy**: Implementado de forma similar

#### **⚠️ Recomendación:**
En un proyecto limpio, se debería mantener solo una versión del servicio de bebidas.

---

### 5. 📦 **`__init__.py`** - Exportaciones del Módulo

**Propósito**: Hace que la carpeta `services` sea un módulo Python y exporta los servicios principales.

#### **🎯 Exportaciones:**
```python
from .servicio_bebidas import ServicioBebidas
```

#### **📝 Uso:**
```python
# Importar desde cualquier parte de la aplicación
from app.services import ServicioBebidas
```

---

## 🔄 **Flujo de Funcionamiento**

### **1. Inicialización de la Aplicación:**
```
main.py → core/dependencies.py → services/servicio_bebidas.py → Carga CSV → Servicios listos
```

### **2. Request de Búsqueda:**
```
API Request → servicio_bebidas.buscar_bebida() → estrategia_busqueda.buscar() → Respuesta
```

### **3. Operación de Carrito:**
```
API Request → servicio_carrito.agregar_al_carrito() → Validar bebida → Actualizar carrito → Respuesta
```

### **4. Operación de Base de Datos:**
```
API Request → servicio_pedidos.registrar_usuario() → SQLAlchemy → MySQL → Respuesta
```

---

## 🛠️ **Tecnologías y Patrones Utilizados**

### **🧠 Patrón Strategy:**
- **Estrategias intercambiables**: Búsqueda, precio, respuesta, sugerencia
- **Configuración dinámica**: Cambiar comportamiento en runtime
- **Extensibilidad**: Fácil agregar nuevas estrategias

### **📋 Dependency Injection:**
- **Servicios inyectados**: En APIs via FastAPI Depends
- **Desacoplamiento**: Servicios independientes
- **Testing**: Fácil mockear para pruebas

### **🗄️ ORM SQLAlchemy:**
- **Operaciones de base de datos**: Via modelos SQLAlchemy
- **Transacciones**: Manejo automático
- **Seguridad**: Prevención de SQL injection

### **📊 Procesamiento de CSV:**
- **Mapeo automático**: Detección de estructura
- **Normalización**: Limpieza de encabezados
- **Validación**: Datos consistentes

---

## 🎯 **Principios de Diseño**

### **1. Separación de Responsabilidades:**
- **ServicioBebidas**: Lógica del chatbot
- **ServicioCarrito**: Gestión del carrito
- **ServicioPedidos**: Persistencia de datos

### **2. Single Responsibility Principle:**
- **Cada servicio**: Una responsabilidad específica
- **Métodos cohesivos**: Funcionalidad relacionada agrupada
- **Interfaces claras**: Métodos bien definidos

### **3. Open/Closed Principle:**
- **Extensible**: Nuevas estrategias sin modificar código
- **Cerrado para modificación**: Funcionalidad base estable
- **Configuración**: Via inyección de estrategias

### **4. Dependency Inversion:**
- **Abstracciones**: Servicios dependen de interfaces
- **Inversión**: Detalles dependen de abstracciones
- **Flexibilidad**: Fácil cambiar implementaciones

---

## 🚀 **Cómo Extender los Servicios**

### **1. Agregar Nueva Funcionalidad a ServicioBebidas:**
```python
def buscar_por_categoria(self, categoria: str) -> List[Bebida]:
    """Nueva funcionalidad de búsqueda por categoría."""
    return [b for b in self.bebidas if b.categoria == categoria]
```

### **2. Crear Nuevo Servicio:**
```python
class ServicioRecomendaciones:
    """Nuevo servicio para recomendaciones personalizadas."""
    
    def __init__(self, servicio_bebidas: ServicioBebidas):
        self.servicio_bebidas = servicio_bebidas
    
    def recomendar_para_usuario(self, historial_usuario: List[str]) -> List[Bebida]:
        """Genera recomendaciones basadas en historial."""
        pass
```

### **3. Agregar Nueva Estrategia:**
```python
# En strategies/
class EstrategiaBusquedaPorIngredientes(EstrategiaBusqueda):
    """Nueva estrategia de búsqueda por ingredientes."""
    pass

# En servicio_bebidas.py
servicio.establecer_estrategia_busqueda(EstrategiaBusquedaPorIngredientes())
```

---

## 🧪 **Testing de Servicios**

### **📋 Testing de ServicioBebidas:**
```python
def test_buscar_bebida():
    servicio = ServicioBebidas(Path("test_data.csv"))
    resultado = servicio.buscar_bebida("latte")
    assert resultado is not None
    assert "latte" in resultado.nombre_es.lower()
```

### **🛒 Testing de ServicioCarrito:**
```python
def test_agregar_al_carrito():
    mock_servicio_bebidas = Mock()
    servicio_carrito = ServicioCarrito(mock_servicio_bebidas)
    
    resultado = servicio_carrito.agregar_al_carrito("Latte", 2)
    
    assert resultado["ok"] is True
    assert len(resultado["carrito"].items) == 1
```

### **🗄️ Testing de ServicioPedidos:**
```python
def test_registrar_usuario():
    mock_db = Mock()
    usuario_data = UsuarioRegistro(
        nombre="Test User",
        direccion="Test Address",
        celular="1234567890"
    )
    
    resultado = ServicioPedidos.registrar_usuario(mock_db, usuario_data)
    
    assert resultado.nombre_usuario == "Test User"
```

---

## 🔍 **Debugging y Monitoreo**

### **📊 Logging:**
```python
import logging
logger = logging.getLogger(__name__)

# En métodos de servicio
logger.info(f"Buscando bebida: {consulta}")
logger.error(f"Error en base de datos: {e}")
```

### **🔧 Métricas:**
```python
# Contar operaciones
def buscar_bebida(self, consulta: str):
    self.contador_busquedas += 1
    # ... lógica de búsqueda
```

---

## 📊 **Performance y Optimización**

### **⚡ Optimizaciones Implementadas:**
- **Cache de CSV**: Carga una sola vez al inicializar
- **Mapeo eficiente**: Diccionarios para búsquedas rápidas
- **Lazy loading**: Servicios se crean solo cuando se necesitan
- **Pool de conexiones**: Para base de datos (via SQLAlchemy)

### **🔧 Mejoras Posibles:**
- **Cache de búsquedas**: Resultados frecuentes en memoria
- **Índices de base de datos**: Para consultas más rápidas
- **Paginación**: Para listas grandes de resultados
- **Compresión**: Para respuestas grandes

---

**🎯 Esta carpeta es el motor de toda la lógica de negocio de tu chatbot Starbucks, donde se implementan todas las funcionalidades inteligentes.**
