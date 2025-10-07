# 📋 Documentación de la Carpeta `app/models/`

## 🎯 **Propósito General**

La carpeta `app/models/` contiene todas las **estructuras de datos** de la aplicación. Define cómo se organizan y validan los datos que fluyen entre el frontend, las APIs, los servicios y la base de datos.

## 📁 **Estructura de Archivos**

```
app/models/
├── __init__.py          # Inicialización y exportaciones del módulo
├── beverage.py         # 🍹 Modelos de bebidas y carrito de compras
└── pedido.py           # 🗄️ Modelos de base de datos (pedidos y usuarios)
```

---

## 📄 **Descripción Detallada de Cada Archivo**

### 1. 🍹 **`beverage.py`** - Modelos de Bebidas y Carrito

**Propósito**: Define todas las estructuras de datos relacionadas con bebidas, búsquedas, sugerencias y el carrito de compras.

#### **🎯 Modelos Principales:**

##### **🍹 Modelo `Bebida` (Dataclass):**
```python
@dataclass
class Bebida:
    """Modelo de datos para una bebida."""
    nombre_en: str                    # Nombre en inglés
    nombre_es: str                    # Nombre en español
    metodo: str                       # Método de preparación
    calorias: Optional[float]         # Calorías
    grasa_total: Optional[float]      # Grasa total
    categoria: Optional[str] = None   # Categoría de bebida
    precio: Optional[float] = None    # Precio
    url_imagen: Optional[str] = None  # URL de imagen
    descripcion: Optional[str] = None # Descripción
```

**Uso:**
```python
latte = Bebida(
    nombre_en="Latte",
    nombre_es="Latte",
    metodo="4 min",
    calorias=190.0,
    grasa_total=6.0,
    precio=4.5,
    descripcion="Espresso con leche al vapor"
)
```

##### **🔍 Modelos de Búsqueda:**

###### **Solicitud de Búsqueda:**
```python
class SolicitudBusqueda(BaseModel):
    """Modelo de solicitud para búsqueda de bebidas."""
    consulta: str           # Término de búsqueda
    idioma: str = "es"      # Idioma por defecto español
```

###### **Respuesta de Búsqueda:**
```python
class RespuestaBusqueda(BaseModel):
    """Modelo de respuesta para búsqueda de bebidas."""
    ok: bool = True                    # Estado de la operación
    encontrado: bool                   # Si se encontró la bebida
    idioma: str = "es"                 # Idioma de respuesta
    datos: Optional[Bebida] = None     # Datos de la bebida encontrada
    texto: str                         # Mensaje de respuesta
    sugerencias: list[Bebida] = []     # Sugerencias alternativas
```

###### **Respuesta de Sugerencias:**
```python
class RespuestaSugerencias(BaseModel):
    """Modelo de respuesta para sugerencias de bebidas."""
    ok: bool = True                    # Estado de la operación
    idioma: str = "es"                 # Idioma de respuesta
    elementos: list[Bebida]            # Lista de bebidas sugeridas
```

##### **🛒 Modelos del Carrito de Compras:**

###### **Item del Carrito:**
```python
class ItemCarrito(BaseModel):
    """Modelo para un item del carrito de compras."""
    bebida: Bebida          # Bebida seleccionada
    cantidad: int = 1       # Cantidad de items
    subtotal: float         # Subtotal calculado
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal del item basado en cantidad y precio."""
        precio = self.bebida.precio or 0.0
        return precio * self.cantidad
```

###### **Carrito Completo:**
```python
class Carrito(BaseModel):
    """Modelo para el carrito de compras completo."""
    items: List[ItemCarrito] = []    # Lista de items
    total: float = 0.0               # Total del carrito
    
    # Métodos principales:
    def calcular_total(self) -> float
    def agregar_item(self, bebida: Bebida, cantidad: int = 1) -> None
    def actualizar_cantidad(self, nombre_bebida: str, nueva_cantidad: int) -> bool
    def eliminar_item(self, nombre_bebida: str) -> bool
    def vaciar(self) -> None
```

**Funcionalidades del Carrito:**
- **Agregar items**: Detecta duplicados y suma cantidades
- **Actualizar cantidades**: Modifica cantidad de items existentes
- **Eliminar items**: Remueve productos específicos
- **Calcular totales**: Automático en cada operación
- **Vaciar carrito**: Limpia completamente

##### **📡 Modelos de API del Carrito:**

###### **Solicitudes:**
```python
class SolicitudAgregarCarrito(BaseModel):
    """Modelo de solicitud para agregar item al carrito."""
    nombre_bebida: str
    cantidad: int = 1

class SolicitudActualizarCarrito(BaseModel):
    """Modelo de solicitud para actualizar cantidad en el carrito."""
    nombre_bebida: str
    cantidad: int
```

###### **Respuesta:**
```python
class RespuestaCarrito(BaseModel):
    """Modelo de respuesta para operaciones del carrito."""
    ok: bool = True         # Estado de la operación
    mensaje: str            # Mensaje descriptivo
    carrito: Carrito        # Estado actual del carrito
```

---

### 2. 🗄️ **`pedido.py`** - Modelos de Base de Datos

**Propósito**: Define los modelos para interactuar con la base de datos MySQL, incluyendo pedidos y registro de usuarios.

#### **🎯 Modelos Principales:**

##### **🗄️ Modelo SQLAlchemy `Pedido`:**
```python
class Pedido(Base):
    """Modelo SQLAlchemy para la tabla pedido."""
    __tablename__ = "pedido"
    
    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_usuario = Column(String(100), nullable=False)
    direccion = Column(String(100), nullable=False)
    telefono = Column(Integer, nullable=False)
    nombre_bebida = Column(String(100), nullable=True)
    precio = Column(Float, nullable=True)
```

**Correspondencia con tabla MySQL:**
```sql
CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono INT NOT NULL,
    nombre_bebida VARCHAR(100),
    precio FLOAT
);
```

##### **📡 Modelos Pydantic para APIs:**

###### **Crear Pedido:**
```python
class PedidoCreate(BaseModel):
    """Modelo para crear un nuevo pedido."""
    nombre_usuario: str
    direccion: str
    telefono: str
    nombre_bebida: Optional[str] = None
    precio: Optional[float] = None
```

###### **Respuesta de Pedido:**
```python
class PedidoResponse(BaseModel):
    """Modelo de respuesta para pedidos."""
    id_pedido: int
    nombre_usuario: str
    direccion: str
    telefono: int
    nombre_bebida: Optional[str]
    precio: Optional[float]
    
    class Config:
        from_attributes = True  # Para convertir desde SQLAlchemy
```

###### **Registro de Usuario:**
```python
class UsuarioRegistro(BaseModel):
    """Modelo para registro de usuario."""
    nombre: str
    direccion: str
    celular: str
```

---

### 3. 📦 **`__init__.py`** - Exportaciones del Módulo

**Propósito**: Hace que la carpeta `models` sea un módulo Python y exporta los modelos principales.

#### **🎯 Exportaciones:**
```python
from .beverage import Bebida, SolicitudBusqueda, RespuestaBusqueda, RespuestaSugerencias
```

#### **📝 Uso:**
```python
# Importar desde cualquier parte de la aplicación
from app.models import Bebida, SolicitudBusqueda
```

---

## 🔄 **Flujo de Datos**

### **1. Búsqueda de Bebidas:**
```
Frontend → SolicitudBusqueda → API → Servicio → RespuestaBusqueda → Frontend
```

### **2. Carrito de Compras:**
```
Frontend → SolicitudAgregarCarrito → API → Carrito → RespuestaCarrito → Frontend
```

### **3. Pedidos en Base de Datos:**
```
Frontend → UsuarioRegistro → API → Pedido (SQLAlchemy) → MySQL → PedidoResponse
```

---

## 🛠️ **Tecnologías Utilizadas**

### **📋 Pydantic:**
- **Validación automática**: Tipos y valores
- **Serialización JSON**: Automática
- **Documentación**: Auto-generada para APIs
- **Type hints**: Tipado estático

### **🗄️ SQLAlchemy:**
- **ORM**: Mapeo objeto-relacional
- **Modelos de tabla**: Definición de esquemas
- **Relaciones**: Entre tablas (futuro)

### **📊 Dataclasses:**
- **Estructuras simples**: Para datos inmutables
- **Performance**: Más rápido que clases normales
- **Legibilidad**: Código más limpio

---

## 🎯 **Validaciones Automáticas**

### **🔍 Pydantic Validations:**
```python
class SolicitudBusqueda(BaseModel):
    consulta: str           # Debe ser string, no puede ser None
    idioma: str = "es"      # Valor por defecto si no se proporciona

# Uso:
solicitud = SolicitudBusqueda(consulta="latte")  # ✅ Válido
solicitud = SolicitudBusqueda(consulta=123)      # ❌ Error de validación
```

### **🛒 Validaciones del Carrito:**
```python
# El carrito valida automáticamente:
- Cantidad debe ser entero positivo
- Bebida debe tener estructura válida
- Subtotal se calcula automáticamente
- Total se actualiza en cada operación
```

---

## 🚀 **Cómo Extender los Modelos**

### **1. Agregar Nuevo Campo a Bebida:**
```python
@dataclass
class Bebida:
    # ... campos existentes ...
    disponible: bool = True        # Nuevo campo
    descuento: Optional[float] = None  # Otro campo opcional
```

### **2. Crear Nuevo Modelo de API:**
```python
class SolicitudFiltros(BaseModel):
    """Modelo para filtrar bebidas."""
    categoria: Optional[str] = None
    precio_min: Optional[float] = None
    precio_max: Optional[float] = None
    calorias_max: Optional[int] = None
```

### **3. Agregar Nuevo Modelo de Base de Datos:**
```python
class Categoria(Base):
    """Modelo para categorías de bebidas."""
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(200))
```

---

## 🔧 **Configuración Avanzada**

### **📋 Validadores Personalizados:**
```python
from pydantic import validator

class PedidoCreate(BaseModel):
    telefono: str
    
    @validator('telefono')
    def validar_telefono(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Teléfono debe tener 10 dígitos')
        return v
```

### **🔄 Conversiones Automáticas:**
```python
class PedidoResponse(BaseModel):
    class Config:
        from_attributes = True      # Convierte desde SQLAlchemy
        json_encoders = {           # Encoders personalizados
            datetime: lambda v: v.isoformat()
        }
```

---

## 🧪 **Testing de Modelos**

### **📋 Validación de Pydantic:**
```python
def test_solicitud_busqueda():
    # Test válido
    solicitud = SolicitudBusqueda(consulta="latte")
    assert solicitud.consulta == "latte"
    assert solicitud.idioma == "es"
    
    # Test inválido
    with pytest.raises(ValidationError):
        SolicitudBusqueda(consulta=None)
```

### **🛒 Testing del Carrito:**
```python
def test_carrito_agregar_item():
    carrito = Carrito()
    bebida = Bebida(nombre_es="Latte", precio=4.5)
    
    carrito.agregar_item(bebida, 2)
    
    assert len(carrito.items) == 1
    assert carrito.items[0].cantidad == 2
    assert carrito.total == 9.0
```

---

## 📊 **Relaciones Entre Modelos**

### **🔗 Flujo de Datos:**
```
CSV (starbucks2.csv) → Bebida → SolicitudBusqueda → RespuestaBusqueda
                         ↓
                    ItemCarrito → Carrito → SolicitudAgregarCarrito
                         ↓
                    UsuarioRegistro → PedidoCreate → Pedido (SQLAlchemy)
```

### **📋 Jerarquía de Modelos:**
```
Modelos Base:
├── Bebida (Dataclass)          # Estructura principal
├── Carrito (Pydantic)          # Lógica de negocio
└── Pedido (SQLAlchemy)         # Persistencia

Modelos de API:
├── Solicitud* (Pydantic)       # Input de APIs
└── Respuesta* (Pydantic)       # Output de APIs
```

---

## 🎯 **Puntos Clave para Entender**

### **1. Separación de Responsabilidades:**
- **Bebida**: Estructura de datos pura
- **Carrito**: Lógica de negocio
- **Pedido**: Persistencia en base de datos
- **API Models**: Comunicación HTTP

### **2. Validación Automática:**
- **Pydantic**: Valida tipos y valores automáticamente
- **SQLAlchemy**: Valida esquema de base de datos
- **Type hints**: Ayuda al IDE y debugging

### **3. Flexibilidad:**
- **Optional fields**: Campos opcionales para diferentes casos
- **Default values**: Valores por defecto sensatos
- **Extensibilidad**: Fácil agregar nuevos campos

### **4. Performance:**
- **Dataclass**: Más rápido para estructuras simples
- **Pydantic**: Validación eficiente
- **SQLAlchemy**: ORM optimizado

---

## 🔍 **Debugging y Monitoreo**

### **📊 Ver Estructura de Modelos:**
```python
from app.models import Bebida, Carrito

# Ver campos de un modelo
print(Bebida.__annotations__)
print(Carrito.__fields__)
```

### **🔧 Validar Datos:**
```python
# Validar JSON de entrada
try:
    solicitud = SolicitudBusqueda.parse_obj(json_data)
except ValidationError as e:
    print(f"Error de validación: {e}")
```

---

**🎯 Esta carpeta define la estructura de todos los datos que fluyen por tu aplicación Starbucks, desde bebidas hasta pedidos en base de datos.**
