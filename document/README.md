# 🤖 **Chatbot Starbucks - Documentación Técnica Completa**

<div align="center">

![Starbucks](https://img.shields.io/badge/Starbucks-00704A?style=for-the-badge&logo=starbucks&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**Sistema completo de chatbot inteligente con carrito de compras y base de datos**

</div>

---

## 🎯 **Visión General del Sistema**

Este proyecto implementa un **chatbot inteligente para Starbucks** con funcionalidades avanzadas de búsqueda, carrito de compras y persistencia de datos. Utiliza el **patrón Strategy** para algoritmos intercambiables y está optimizado para dispositivos móviles.

### **🏗️ Arquitectura del Proyecto**

```
📁 proyecto_chatbot V2/
├── 🌐 app/                    # Código principal de la aplicación
│   ├── 📡 api/               # Endpoints y rutas HTTP
│   ├── ⚙️ core/              # Configuración central
│   ├── 🗄️ database/          # Conexión a MySQL
│   ├── 📋 models/            # Estructuras de datos
│   ├── ⚙️ services/          # Lógica de negocio
│   └── 🧠 strategies/        # Algoritmos IA intercambiables
├── 🎨 templates/             # Páginas HTML
├── 📚 document/              # Documentación técnica
└── 📊 starbucks2.csv         # Base de datos de productos
```

---

## 📚 **Guía de Documentación**

### **📡 [API.md](API.md) - El Corazón de la Comunicación**

> **¿Qué hace?** Maneja toda la comunicación entre el frontend y backend

#### **🎯 Componentes Principales:**
- **`routes.py`** - 35+ endpoints para chatbot y carrito
- **`pedidos.py`** - 6 endpoints para base de datos MySQL
- **`vistas.py`** - Renderizado de páginas HTML
- **`views.py`** - Archivo legacy/alternativo

#### **🔗 APIs Disponibles:**
```http
POST   /api/buscar              # Búsqueda inteligente de bebidas
GET    /api/sugerencias         # Sugerencias con IA
POST   /api/carrito/agregar     # Gestión del carrito
POST   /api/pedidos/registrar-usuario  # Registro en MySQL
GET    /api/pedidos/test-conexion      # Health check BD
```

#### **💡 Punto Clave:**
*Todas las APIs usan **inyección de dependencias** y **validación automática** con Pydantic*

---

### **⚙️ [CORE.md](CORE.md) - El Centro de Control**

> **¿Qué hace?** Configura y controla el comportamiento de toda la aplicación

#### **🎯 Componentes Principales:**
- **`config.py`** - Configuración global (servidor, estrategias, archivos)
- **`dependencies.py`** - Inyección de dependencias con FastAPI

#### **🔧 Configuraciones Clave:**
```python
# Estrategias por defecto
estrategia_busqueda_default = "compuesta"    # Búsqueda híbrida
estrategia_precio_default = "premium"        # Cálculos sofisticados
estrategia_respuesta_default = "estandar"    # Balance perfecto
estrategia_sugerencia_default = "hibrida"    # IA avanzada
```

#### **💡 Punto Clave:**
*Usa el **patrón Dependency Injection** para servicios configurables y **variables de entorno** para diferentes despliegues*

---

### **🗄️ [DATABASE.md](DATABASE.md) - La Persistencia**

> **¿Qué hace?** Maneja toda la conexión y operaciones con MySQL

#### **🎯 Componentes Principales:**
- **`config.py`** - Configuración SQLAlchemy + MySQL (XAMPP)

#### **🗄️ Configuración de Base de Datos:**
```python
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/starbucks"

# Tabla principal
CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono INT NOT NULL,
    nombre_bebida VARCHAR(100),
    precio FLOAT
);
```

#### **💡 Punto Clave:**
*Usa **pool de conexiones** optimizado y **inyección automática** de sesiones de BD en FastAPI*

---

### **📋 [MODELS.md](MODELS.md) - Las Estructuras de Datos**

> **¿Qué hace?** Define cómo se organizan y validan todos los datos

#### **🎯 Componentes Principales:**
- **`beverage.py`** - Modelos de bebidas + carrito completo (134 líneas)
- **`pedido.py`** - Modelos de base de datos + APIs (44 líneas)

#### **📊 Modelos Principales:**
```python
@dataclass
class Bebida:                    # Estructura principal
    nombre_es: str
    precio: float
    descripcion: str
    # ... 9 campos total

class Carrito(BaseModel):        # Lógica de carrito
    items: List[ItemCarrito]
    total: float
    # Métodos: agregar, actualizar, eliminar, calcular

class Pedido(Base):              # Tabla MySQL
    __tablename__ = "pedido"
    id_pedido = Column(Integer, primary_key=True)
    # ... mapeo directo con BD
```

#### **💡 Punto Clave:**
*Combina **Dataclass** (velocidad), **Pydantic** (validación) y **SQLAlchemy** (persistencia) según necesidades*

---

### **⚙️ [SERVICES.md](SERVICES.md) - La Lógica de Negocio**

> **¿Qué hace?** Implementa toda la funcionalidad inteligente del chatbot

#### **🎯 Componentes Principales:**
- **`servicio_bebidas.py`** - Cerebro del chatbot (259 líneas)
- **`servicio_carrito.py`** - Gestión del carrito (230 líneas)
- **`servicio_pedidos.py`** - Operaciones de BD (139 líneas)

#### **🧠 Funcionalidades Inteligentes:**
```python
class ServicioBebidas:
    def buscar_bebida(consulta)           # Búsqueda con IA
    def obtener_sugerencias(consulta)     # Recomendaciones
    def cargar_bebidas()                  # Mapeo automático CSV
    
class ServicioCarrito:
    def agregar_al_carrito()              # Detecta duplicados
    def actualizar_cantidad()             # Validaciones
    def finalizar_compra()                # Simulación completa

class ServicioPedidos:
    def registrar_usuario()               # Limpieza de datos
    def crear_pedido_completo()           # Transacciones seguras
```

#### **💡 Punto Clave:**
*Usa **patrón Strategy** para algoritmos intercambiables y **separación de responsabilidades** clara*

---

### **🧠 [STRATEGIES.md](STRATEGIES.md) - Los Algoritmos IA**

> **¿Qué hace?** Implementa la inteligencia artificial con algoritmos intercambiables

#### **🎯 Componentes Principales:**
- **`estrategias_busqueda.py`** - 3 algoritmos de búsqueda (170 líneas)
- **`estrategias_precio.py`** - 3 estrategias de precios (138 líneas)
- **`estrategias_respuesta.py`** - 3 formatos de respuesta (144 líneas)
- **`estrategias_sugerencia.py`** - 2 algoritmos de IA (192 líneas)

#### **🤖 Algoritmos de IA:**

##### **🔍 Búsqueda Inteligente:**
```python
class EstrategiaCoincidenciaExacta:     # 100% precisión
class EstrategiaBusquedaDifusa:         # Tolerante a errores
class EstrategiaBusquedaCompuesta:      # Híbrida (recomendada)
```

##### **💰 Cálculo de Precios:**
```python
class EstrategiaPrecioBasico:           # Por tamaño
class EstrategiaPrecioPorFamilia:       # Por tipo de bebida
class EstrategiaPrecioPremium:          # Factores múltiples
```

##### **💡 Sugerencias IA:**
```python
class EstrategiaSugerenciaPorSimilitud: # difflib + tokens
class EstrategiaSugerenciaHibrida:      # Multi-algoritmo
```

#### **💡 Punto Clave:**
*Implementa **patrón Strategy** perfecto con **11 algoritmos intercambiables** y **IA de recomendación** avanzada*

---

## 🔄 **Flujo Completo del Sistema**

### **1. 🚀 Inicialización**
```
main.py → core/config.py → core/dependencies.py → services/ → strategies/
```

### **2. 💬 Interacción del Usuario**
```
Frontend → api/routes.py → services/servicio_bebidas.py → strategies/busqueda → CSV
```

### **3. 🛒 Carrito de Compras**
```
Usuario agrega → api/routes.py → services/servicio_carrito.py → models/Carrito → localStorage
```

### **4. 🗄️ Persistencia de Datos**
```
Registro → api/pedidos.py → services/servicio_pedidos.py → database/config.py → MySQL
```

---

## 🎯 **Patrones de Diseño Implementados**

### **🧠 Strategy Pattern**
- **Ubicación**: `app/strategies/`
- **Propósito**: Algoritmos intercambiables
- **Beneficio**: Extensibilidad sin modificar código

### **🔌 Dependency Injection**
- **Ubicación**: `app/core/dependencies.py`
- **Propósito**: Servicios configurables
- **Beneficio**: Testing y flexibilidad

### **📋 Repository Pattern**
- **Ubicación**: `app/services/`
- **Propósito**: Abstracción de datos
- **Beneficio**: Separación de responsabilidades

### **🏭 Factory Pattern**
- **Ubicación**: `app/core/dependencies.py`
- **Propósito**: Creación de servicios
- **Beneficio**: Configuración centralizada

---

## 🛠️ **Stack Tecnológico**

### **🐍 Backend**
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para MySQL
- **Pydantic** - Validación de datos
- **PyMySQL** - Conector de base de datos

### **🌐 Frontend**
- **JavaScript Vanilla** - Sin frameworks
- **HTML5 + CSS3** - Diseño responsive
- **Bootstrap** - Componentes UI
- **LocalStorage** - Persistencia local

### **🗄️ Base de Datos**
- **MySQL** - Base de datos relacional
- **XAMPP** - Entorno de desarrollo
- **CSV** - Base de datos de productos

### **🧠 Inteligencia Artificial**
- **difflib** - Similitud de texto
- **unicodedata** - Normalización
- **Algoritmos personalizados** - Recomendaciones

---

## 📊 **Métricas del Proyecto**

### **📈 Líneas de Código**
```
📁 app/api/        →  4 archivos  →  ~400 líneas
📁 app/core/       →  2 archivos  →  ~100 líneas
📁 app/database/   →  1 archivo   →   ~50 líneas
📁 app/models/     →  2 archivos  →  ~180 líneas
📁 app/services/   →  4 archivos  →  ~900 líneas
📁 app/strategies/ →  8 archivos  → ~1200 líneas
```

### **🎯 Funcionalidades**
- **35+ endpoints** de API
- **11 algoritmos** de IA intercambiables
- **6 modelos** de datos principales
- **4 servicios** de lógica de negocio
- **1 base de datos** MySQL integrada

---

## 🚀 **Cómo Usar Esta Documentación**

### **👨‍💻 Para Desarrolladores**
1. **Empezar con**: [SERVICES.md](SERVICES.md) para entender la lógica
2. **Luego**: [STRATEGIES.md](STRATEGIES.md) para los algoritmos IA
3. **Después**: [API.md](API.md) para los endpoints
4. **Finalmente**: [MODELS.md](MODELS.md) para las estructuras

### **🔧 Para Administradores**
1. **Configuración**: [CORE.md](CORE.md) y [DATABASE.md](DATABASE.md)
2. **Despliegue**: [API.md](API.md) para endpoints de salud
3. **Monitoreo**: [SERVICES.md](SERVICES.md) para métricas

### **🧪 Para Testing**
1. **Modelos**: [MODELS.md](MODELS.md) para validaciones
2. **Servicios**: [SERVICES.md](SERVICES.md) para lógica
3. **Estrategias**: [STRATEGIES.md](STRATEGIES.md) para algoritmos
4. **APIs**: [API.md](API.md) para endpoints

---

## 🎉 **Características Destacadas**

### **🤖 Inteligencia Artificial**
- **Búsqueda tolerante a errores** - "late" encuentra "Latte"
- **Sugerencias inteligentes** - Algoritmo híbrido de recomendación
- **Normalización avanzada** - Elimina acentos y espacios
- **Cálculo de precios** - Estimación automática sofisticada

### **🛒 Carrito Inteligente**
- **Detección de duplicados** - Suma cantidades automáticamente
- **Cálculos automáticos** - Subtotales y totales en tiempo real
- **Persistencia dual** - localStorage + MySQL
- **Validaciones** - Productos existentes y cantidades

### **📱 Diseño Responsive**
- **Móvil optimizado** - Chat compacto (55vh) y carrito (65vh)
- **Navbar oculto** - Logo flotante en móviles
- **Botones táctiles** - 44px mínimo para accesibilidad
- **Breakpoints** - 768px (tablet) y 480px (móvil)

### **🗄️ Base de Datos Robusta**
- **Pool de conexiones** - Optimizado para performance
- **Transacciones seguras** - Manejo de errores completo
- **Validación de datos** - Limpieza automática de teléfonos
- **Health checks** - Monitoreo de conexión

---

## 🔧 **Configuración Rápida**

### **1. Requisitos**
```bash
pip install fastapi sqlalchemy pymysql pydantic-settings
```

### **2. Base de Datos**
```sql
CREATE DATABASE starbucks;
-- La tabla se crea automáticamente
```

### **3. Ejecutar**
```bash
python main_refactorizado.py
# Aplicación en: http://127.0.0.1:8000
```

---

<div align="center">

## 🎯 **Sistema Completo y Documentado**

**Este chatbot Starbucks implementa las mejores prácticas de desarrollo:**
- ✅ **Arquitectura limpia** con separación de responsabilidades
- ✅ **Patrones de diseño** modernos y escalables  
- ✅ **Inteligencia artificial** con algoritmos intercambiables
- ✅ **Base de datos** robusta y optimizada
- ✅ **Diseño responsive** para todos los dispositivos
- ✅ **Documentación completa** para mantenimiento

---

**🚀 ¡Listo para producción y fácil de mantener!**

</div>
