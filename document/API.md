# 📡 Documentación de la Carpeta `app/api/`

## 🎯 **Propósito General**

La carpeta `app/api/` contiene todos los **endpoints** y **rutas** de la aplicación FastAPI. Es el punto de entrada para todas las comunicaciones HTTP entre el frontend (JavaScript) y el backend (Python).

## 📁 **Estructura de Archivos**

```
app/api/
├── __init__.py          # Archivo de inicialización del módulo
├── routes.py           # 🔍 APIs principales (búsqueda, sugerencias, carrito)
├── pedidos.py          # 🗄️ APIs de base de datos (pedidos y usuarios)
├── vistas.py           # 🌐 Rutas HTML (páginas web)
└── views.py            # 🌐 Rutas HTML alternativas (legacy)
```

---

## 📄 **Descripción Detallada de Cada Archivo**

### 1. 🔍 **`routes.py`** - APIs Principales del Chatbot

**Propósito**: Maneja toda la lógica principal del chatbot y carrito de compras.

#### **🎯 Funcionalidades:**
- **Búsqueda de bebidas** por nombre
- **Sugerencias inteligentes** basadas en consultas
- **Gestión del carrito** (agregar, actualizar, eliminar)
- **Listado de bebidas** disponibles

#### **📡 Endpoints Disponibles:**
```python
POST   /api/buscar              # Buscar bebidas por nombre
GET    /api/sugerencias         # Obtener sugerencias de bebidas
GET    /api/bebidas             # Listar todas las bebidas
POST   /api/carrito/agregar     # Agregar producto al carrito
PUT    /api/carrito/actualizar  # Actualizar cantidad en carrito
DELETE /api/carrito/eliminar    # Eliminar producto del carrito
GET    /api/carrito/obtener     # Obtener contenido del carrito
DELETE /api/carrito/vaciar      # Vaciar carrito completo
POST   /api/carrito/finalizar   # Finalizar compra
GET    /api/salud               # Health check de la API
```

#### **🔧 Servicios Utilizados:**
- `ServicioBebidas`: Para búsqueda y sugerencias
- `ServicioCarrito`: Para gestión del carrito
- `@lru_cache()`: Para optimización de rendimiento

#### **📝 Ejemplo de Uso:**
```javascript
// Desde el frontend (JavaScript)
const response = await fetch('/api/buscar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ consulta: 'latte', idioma: 'es' })
});
```

---

### 2. 🗄️ **`pedidos.py`** - APIs de Base de Datos

**Propósito**: Maneja toda la comunicación con la base de datos MySQL para pedidos y usuarios.

#### **🎯 Funcionalidades:**
- **Registro de usuarios** en la base de datos
- **Creación de pedidos** completos
- **Actualización de pedidos** existentes
- **Consulta de pedidos** por usuario
- **Gestión de historial** de compras

#### **📡 Endpoints Disponibles:**
```python
POST   /api/pedidos/registrar-usuario    # Registrar nuevo usuario
POST   /api/pedidos/crear-pedido          # Crear pedido completo
PUT    /api/pedidos/actualizar-pedido     # Actualizar pedido existente
GET    /api/pedidos/usuario/{nombre}      # Obtener pedidos de usuario
GET    /api/pedidos/todos                 # Obtener todos los pedidos (admin)
GET    /api/pedidos/test-conexion         # Probar conexión a BD
```

#### **🗄️ Tabla de Base de Datos:**
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

#### **🔧 Servicios Utilizados:**
- `ServicioPedidos`: Lógica de negocio para pedidos
- `get_db()`: Inyección de dependencia para sesión de BD
- `SQLAlchemy`: ORM para interacción con MySQL

#### **📝 Ejemplo de Uso:**
```javascript
// Registrar usuario desde el frontend
const userData = {
    nombre: "Juan Pérez",
    direccion: "Calle 123 #45-67",
    celular: "3001234567"
};

const response = await fetch('/api/pedidos/registrar-usuario', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
});
```

---

### 3. 🌐 **`vistas.py`** - Rutas HTML (Actual)

**Propósito**: Sirve las páginas HTML de la aplicación web.

#### **🎯 Funcionalidades:**
- **Página principal** (`/`) - Renderiza `home.html`
- **Integración con templates** Jinja2
- **Inyección de dependencias** para servicios

#### **📡 Endpoints Disponibles:**
```python
GET    /                        # Página principal (home.html)
```

#### **🔧 Características:**
- Usa `Jinja2Templates` para renderizar HTML
- Integrado con `ServicioBebidas` para datos dinámicos
- Optimizado con `@lru_cache()` para performance

#### **📝 Flujo de Funcionamiento:**
```
Usuario accede a "/" → vistas.py → templates/home.html → Página mostrada
```

---

### 4. 🌐 **`views.py`** - Rutas HTML (Legacy)

**Propósito**: Archivo alternativo/legacy para rutas HTML (similar a `vistas.py`).

#### **🎯 Estado Actual:**
- **Funcionalidad duplicada** con `vistas.py`
- **Posible archivo legacy** de versiones anteriores
- **No se usa actualmente** en la aplicación principal

#### **⚠️ Nota:**
Este archivo parece ser una versión anterior o alternativa de `vistas.py`. En un proyecto limpio, se debería mantener solo uno de los dos.

---

## 🔄 **Flujo de Comunicación**

### **Frontend → Backend**
```
JavaScript (home.html) 
    ↓
FastAPI Router (routes.py / pedidos.py)
    ↓
Services (ServicioBebidas / ServicioPedidos)
    ↓
Database / CSV Files
```

### **Ejemplo de Flujo Completo:**
1. **Usuario busca "latte"** en el chat
2. **JavaScript** envía POST a `/api/buscar`
3. **routes.py** recibe la petición
4. **ServicioBebidas** busca en `starbucks2.csv`
5. **Respuesta JSON** se envía al frontend
6. **JavaScript** muestra resultados en el chat

---

## 🛠️ **Tecnologías Utilizadas**

### **FastAPI Features:**
- `APIRouter`: Para organizar rutas
- `Depends`: Inyección de dependencias
- `HTTPException`: Manejo de errores
- `Jinja2Templates`: Renderizado de HTML

### **Optimizaciones:**
- `@lru_cache()`: Cache de servicios
- `async/await`: Programación asíncrona
- Type hints: Tipado estático

### **Integración:**
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **CSV**: Lectura de archivos de productos

---

## 🎯 **Puntos Clave para Entender**

### **1. Separación de Responsabilidades:**
- `routes.py`: Lógica del chatbot y carrito
- `pedidos.py`: Persistencia en base de datos
- `vistas.py`: Renderizado de páginas web

### **2. Patrón de Inyección de Dependencias:**
```python
def endpoint(servicio: ServicioBebidas = Depends(obtener_servicio_bebidas)):
    # El servicio se inyecta automáticamente
    return servicio.buscar_bebida(consulta)
```

### **3. Manejo de Errores:**
```python
try:
    resultado = servicio.operacion()
    return resultado
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

### **4. Validación con Pydantic:**
```python
class SolicitudBusqueda(BaseModel):
    consulta: str
    idioma: str = "es"
```

---

## 🚀 **Cómo Extender la API**

### **Para agregar un nuevo endpoint:**

1. **Definir el modelo** en `app/models/`
2. **Crear la lógica** en `app/services/`
3. **Agregar el endpoint** en el archivo correspondiente:

```python
@router.post("/api/nuevo-endpoint")
async def nuevo_endpoint(
    datos: MiModelo,
    servicio: MiServicio = Depends(obtener_mi_servicio)
):
    resultado = servicio.procesar(datos)
    return resultado
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Salud:**
- `/api/salud`: Estado general de la API
- `/api/pedidos/test-conexion`: Estado de la base de datos

### **Logging:**
Todos los archivos incluyen logging para debugging y monitoreo.

---

**🎯 Esta carpeta es el corazón de la comunicación entre el frontend y backend de tu aplicación Starbucks.**
