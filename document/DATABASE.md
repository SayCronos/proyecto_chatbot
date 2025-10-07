# 🗄️ Documentación de la Carpeta `app/database/`

## 🎯 **Propósito General**

La carpeta `app/database/` es el **centro de conexión** con la base de datos MySQL. Maneja toda la configuración, conexión y sesiones de base de datos usando SQLAlchemy como ORM (Object-Relational Mapping).

## 📁 **Estructura de Archivos**

```
app/database/
├── __init__.py          # Inicialización del módulo database
└── config.py           # 🗄️ Configuración y conexión a MySQL
```

---

## 📄 **Descripción Detallada de Cada Archivo**

### 1. 🗄️ **`config.py`** - Configuración de Base de Datos

**Propósito**: Establece y configura la conexión con la base de datos MySQL usando SQLAlchemy.

#### **🎯 Funcionalidades:**
- **Conexión a MySQL** (XAMPP)
- **Configuración de SQLAlchemy** (Engine, Session, Base)
- **Pool de conexiones** optimizado
- **Función de prueba** de conexión
- **Inyección de dependencias** para FastAPI

#### **🔧 Configuración de Conexión:**

##### **📡 URL de Conexión:**
```python
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/starbucks?charset=utf8mb4"
```

**Desglose de la URL:**
- **`mysql+pymysql`**: Driver de MySQL con PyMySQL
- **`root`**: Usuario de la base de datos
- **`@`**: Sin contraseña (configuración XAMPP por defecto)
- **`localhost:3306`**: Host y puerto de MySQL
- **`starbucks`**: Nombre de la base de datos
- **`charset=utf8mb4`**: Codificación para caracteres especiales

##### **⚙️ Engine de SQLAlchemy:**
```python
engine = create_engine(
    DATABASE_URL,
    echo=True,              # 📊 Mostrar consultas SQL en logs
    pool_pre_ping=True,     # 🔍 Verificar conexión antes de usar
    pool_recycle=300        # ♻️ Reciclar conexiones cada 5 minutos
)
```

**Parámetros Explicados:**
- **`echo=True`**: Muestra todas las consultas SQL en la consola (útil para debugging)
- **`pool_pre_ping=True`**: Verifica que la conexión esté activa antes de usarla
- **`pool_recycle=300`**: Recicla conexiones cada 5 minutos para evitar timeouts

##### **🔄 Sesión de Base de Datos:**
```python
SessionLocal = sessionmaker(
    autocommit=False,       # 🔒 Transacciones manuales
    autoflush=False,        # 🔄 Flush manual de cambios
    bind=engine            # 🔗 Vinculado al engine
)
```

##### **🏗️ Base para Modelos:**
```python
Base = declarative_base()  # Base para todos los modelos ORM
```

#### **🔌 Funciones Principales:**

##### **1. Inyección de Dependencias:**
```python
def get_db():
    """
    Función para inyección de dependencias en FastAPI.
    Crea una sesión, la usa y la cierra automáticamente.
    """
    db = SessionLocal()
    try:
        yield db          # 🎁 Entrega la sesión
    finally:
        db.close()        # 🔒 Cierra la sesión siempre
```

**Uso en APIs:**
```python
@router.post("/api/pedidos/crear")
async def crear_pedido(
    pedido_data: PedidoRequest,
    db: Session = Depends(get_db)  # 🔌 Inyección automática
):
    # Usar la sesión db para operaciones
    return crear_pedido_en_db(db, pedido_data)
```

##### **2. Prueba de Conexión:**
```python
def test_connection():
    """
    Prueba la conexión a la base de datos.
    Retorna True si exitosa, False si falla.
    """
    try:
        connection = engine.connect()
        result = connection.execute(text("SELECT 1"))
        connection.close()
        print("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False
```

**Uso:**
```python
from app.database.config import test_connection

if test_connection():
    print("Base de datos lista")
else:
    print("Error en base de datos")
```

---

### 2. 📦 **`__init__.py`** - Inicialización del Módulo

**Propósito**: Hace que la carpeta `database` sea un módulo Python importable.

#### **🎯 Funcionalidades:**
- **Módulo Python**: Permite importar desde `app.database`
- **Estructura limpia**: Organización modular

#### **📝 Uso:**
```python
# Importar desde cualquier parte de la aplicación
from app.database.config import get_db, engine, Base
```

---

## 🏗️ **Arquitectura de Base de Datos**

### **📊 Tabla Principal: `pedido`**
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

### **🔗 Relación con la Aplicación:**
```
Frontend (JavaScript) 
    ↓
API (pedidos.py)
    ↓
Services (ServicioPedidos)
    ↓
Database (config.py)
    ↓
MySQL (XAMPP)
```

---

## 🔄 **Flujo de Funcionamiento**

### **1. Inicio de Aplicación:**
```
main.py → database/config.py → Conexión MySQL → Pool de conexiones listo
```

### **2. Request de API:**
```
API Request → Depends(get_db) → Nueva sesión → Operación BD → Sesión cerrada
```

### **3. Ciclo de Vida de Sesión:**
```
get_db() → SessionLocal() → yield db → Operaciones → finally: db.close()
```

---

## 🛠️ **Tecnologías Utilizadas**

### **🔧 SQLAlchemy:**
- **ORM**: Mapeo objeto-relacional
- **Engine**: Motor de base de datos
- **Session**: Manejo de transacciones
- **Base**: Clase base para modelos

### **🐍 PyMySQL:**
- **Driver**: Conector Python-MySQL
- **Compatibilidad**: Funciona con XAMPP
- **Performance**: Optimizado para aplicaciones web

### **🗄️ MySQL:**
- **Base de datos**: Sistema de gestión relacional
- **XAMPP**: Entorno de desarrollo local
- **Puerto 3306**: Puerto estándar de MySQL

---

## ⚙️ **Configuración y Setup**

### **🔧 Requisitos Previos:**

#### **1. XAMPP Instalado:**
- MySQL corriendo en puerto 3306
- Usuario `root` sin contraseña
- Base de datos `starbucks` creada

#### **2. Dependencias Python:**
```bash
pip install sqlalchemy pymysql
```

#### **3. Crear Base de Datos:**
```sql
-- En phpMyAdmin o MySQL CLI
CREATE DATABASE starbucks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### **🚀 Configuración Automática:**
La tabla `pedido` se crea automáticamente cuando se ejecuta la aplicación por primera vez.

---

## 🔧 **Configuración Avanzada**

### **🌍 Variables de Entorno:**
```bash
# .env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=starbucks
```

### **🔄 Configuración Dinámica:**
```python
import os
from urllib.parse import quote_plus

# Construir URL dinámicamente
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "starbucks")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
```

### **🏭 Configuración para Producción:**
```python
# Configuración optimizada para producción
engine = create_engine(
    DATABASE_URL,
    echo=False,              # Sin logs en producción
    pool_size=20,           # Pool más grande
    max_overflow=30,        # Conexiones adicionales
    pool_pre_ping=True,     # Verificación de conexión
    pool_recycle=3600       # Reciclar cada hora
)
```

---

## 🧪 **Testing y Debugging**

### **🔍 Probar Conexión:**
```python
from app.database.config import test_connection

# Verificar conexión
if test_connection():
    print("✅ Base de datos funcionando")
else:
    print("❌ Problema con base de datos")
```

### **📊 Ver Consultas SQL:**
```python
# En config.py, cambiar:
echo=True   # Para ver todas las consultas SQL
```

### **🧪 Base de Datos de Prueba:**
```python
# test_database_config.py
TEST_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/starbucks_test?charset=utf8mb4"

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)
```

---

## 🚀 **Cómo Extender la Base de Datos**

### **1. Agregar Nueva Tabla:**
```python
# En app/models/
from app.database.config import Base
from sqlalchemy import Column, Integer, String

class NuevaTabla(Base):
    __tablename__ = "nueva_tabla"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
```

### **2. Crear Migración:**
```python
# Crear todas las tablas
from app.database.config import engine, Base
Base.metadata.create_all(bind=engine)
```

### **3. Usar en API:**
```python
@router.post("/api/nueva-tabla")
async def crear_registro(
    data: NuevaTablaRequest,
    db: Session = Depends(get_db)
):
    nuevo_registro = NuevaTabla(**data.dict())
    db.add(nuevo_registro)
    db.commit()
    return {"message": "Creado exitosamente"}
```

---

## 📊 **Monitoreo y Performance**

### **🔍 Métricas de Conexión:**
```python
# Ver estado del pool de conexiones
print(f"Conexiones activas: {engine.pool.size()}")
print(f"Conexiones disponibles: {engine.pool.checkedin()}")
```

### **⚡ Optimizaciones:**
- **Pool de conexiones**: Reutilización eficiente
- **Pool pre-ping**: Evita conexiones muertas
- **Pool recycle**: Previene timeouts
- **Autocommit=False**: Control manual de transacciones

---

## 🔒 **Seguridad**

### **🛡️ Mejores Prácticas:**
```python
# 1. Usar variables de entorno para credenciales
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# 2. Validar entrada de usuario
from sqlalchemy import text
result = db.execute(text("SELECT * FROM pedido WHERE id = :id"), {"id": user_id})

# 3. Cerrar sesiones automáticamente
# (Ya implementado en get_db())
```

---

## 🎯 **Puntos Clave para Entender**

### **1. Patrón de Inyección de Dependencias:**
- **FastAPI inyecta** la sesión automáticamente
- **Sesión se cierra** automáticamente después del request
- **Thread-safe**: Cada request tiene su propia sesión

### **2. Pool de Conexiones:**
- **Reutilización**: No crear nueva conexión cada vez
- **Límites**: Controla cuántas conexiones simultáneas
- **Reciclaje**: Evita conexiones obsoletas

### **3. ORM vs SQL Directo:**
- **SQLAlchemy ORM**: Más fácil y seguro
- **SQL directo**: Para consultas complejas específicas
- **Ambos soportados**: Flexibilidad total

---

## 🔧 **Troubleshooting Común**

### **❌ Error: "Can't connect to MySQL server"**
```bash
# Solución:
1. Verificar que XAMPP esté corriendo
2. Verificar puerto 3306 disponible
3. Verificar que MySQL esté iniciado en XAMPP
```

### **❌ Error: "Unknown database 'starbucks'"**
```sql
-- Solución: Crear la base de datos
CREATE DATABASE starbucks;
```

### **❌ Error: "Access denied for user 'root'"**
```python
# Solución: Verificar credenciales en DATABASE_URL
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/starbucks"
```

---

**🎯 Esta carpeta es el puente entre tu aplicación Python y la base de datos MySQL, manejando todas las conexiones de forma segura y eficiente.**
