# 📚 Índice de Documentación - Chatbot Starbucks

## 📋 Documentación Principal

### 📖 **[README.md](README.md)**
Documentación técnica completa del proyecto original con detalles de implementación, arquitectura y configuración.

### 🛒 **[CARRITO_DOCUMENTATION.md](CARRITO_DOCUMENTATION.md)**
Documentación específica del sistema de carrito de compras:
- Funcionalidades implementadas
- APIs del carrito
- Componentes visuales
- Persistencia de datos

### 🚀 **[EXECUTION_GUIDE.md](EXECUTION_GUIDE.md)**
Guía paso a paso para ejecutar la aplicación:
- Configuración del entorno
- Instalación de dependencias
- Ejecución local y en red

### 🔄 **[MIGRATION_DOCUMENTATION.md](MIGRATION_DOCUMENTATION.md)**
Documentación del proceso de migración del chatbot:
- Cambios realizados
- Integración en home.html
- Eliminación del iframe

### 🌐 **[README_NETWORK.md](README_NETWORK.md)**
Configuración para acceso desde la red:
- Configuración de IP
- Acceso desde dispositivos móviles
- Troubleshooting de red

### 🏗️ **[UML_STRATEGY_DIAGRAM_ES.md](UML_STRATEGY_DIAGRAM_ES.md)**
Diagramas UML y documentación del patrón Strategy:
- Arquitectura del sistema
- Diagramas de clases
- Patrones de diseño implementados

## 🧪 Scripts de Prueba

### 🤖 **[test_chatbot.py](test_chatbot.py)**
Pruebas completas del sistema:
- Verificación de APIs
- Prueba de homepage
- Test de base de datos
- Validación completa del chatbot

### 🔌 **[test_api.py](test_api.py)**
Pruebas específicas de las APIs:
- Test de registro de usuario
- Prueba de creación de pedidos
- Validación de endpoints

### 🗄️ **[test_db.py](test_db.py)**
Pruebas de conexión a base de datos:
- Conexión directa MySQL
- Validación SQLAlchemy
- Verificación de tablas

## 📁 Organización de Archivos

```
documentacion/
├── INDEX.md                      # 📋 Este archivo (índice)
├── README.md                     # 📖 Documentación principal
├── CARRITO_DOCUMENTATION.md      # 🛒 Sistema de carrito
├── EXECUTION_GUIDE.md            # 🚀 Guía de ejecución
├── MIGRATION_DOCUMENTATION.md    # 🔄 Proceso de migración
├── README_NETWORK.md             # 🌐 Configuración de red
├── UML_STRATEGY_DIAGRAM_ES.md    # 🏗️ Diagramas UML
├── test_chatbot.py              # 🧪 Pruebas del chatbot
├── test_api.py                  # 🔌 Pruebas de API
└── test_db.py                   # 🗄️ Pruebas de base de datos
```

## 🎯 Guía de Uso

### Para Desarrolladores
1. **Empezar con**: [README.md](README.md) para entender la arquitectura
2. **Configurar**: [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) para setup inicial
3. **Probar**: Ejecutar scripts `test_*.py` para validar funcionamiento

### Para Administradores
1. **Despliegue**: [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) y [README_NETWORK.md](README_NETWORK.md)
2. **Monitoreo**: Usar [test_chatbot.py](test_chatbot.py) para health checks

### Para Mantenimiento
1. **Carrito**: [CARRITO_DOCUMENTATION.md](CARRITO_DOCUMENTATION.md) para modificaciones
2. **Base de datos**: [test_db.py](test_db.py) para diagnósticos
3. **APIs**: [test_api.py](test_api.py) para validar endpoints

## 🔧 Comandos Útiles

### Ejecutar Pruebas
```bash
# Desde la raíz del proyecto
python documentacion/test_chatbot.py    # Pruebas completas
python documentacion/test_api.py        # Solo APIs
python documentacion/test_db.py         # Solo base de datos
```

### Ver Documentación
```bash
# Abrir archivos con cualquier editor de markdown
code documentacion/README.md
```

---

**📝 Nota**: Toda la documentación está organizada aquí para mantener el proyecto principal limpio y facilitar el mantenimiento.
