# 🍵 Asistente de Bebidas Starbucks

Aplicación FastAPI refactorizada con patrón Strategy para búsqueda y recomendación de bebidas Starbucks.

## ✨ Características

- 🔍 **Búsqueda inteligente**: Búsqueda tolerante a acentos y variaciones
- 💰 **Estimación de precios**: Cálculo automático cuando no hay datos disponibles
- 🎯 **Sugerencias**: Recomendaciones basadas en similitud y categorías
- 🛒 **Carrito de compras**: Sistema completo con persistencia localStorage
- 🌐 **API REST**: Endpoints completos con FastAPI
- 🖥️ **Interfaz web**: Chat interactivo y páginas HTML
- 📱 **Acceso de red**: Configurable para acceso desde dispositivos móviles

## 🚀 Inicio Rápido

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
# Servidor web (acceso local)
python main_refactorizado.py

# Servidor web (acceso de red local)
# Edita app/core/config.py y cambia host a "0.0.0.0"
python main_refactorizado.py
```

### URLs de acceso
- **Página principal**: http://localhost:8000
- **Chat**: http://localhost:8000/chat
- **API Docs**: http://localhost:8000/docs
- **API Interactiva**: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
proyecto_chatbot V2/
├── main_refactorizado.py          # Aplicación principal
├── starbucks2.csv                 # Base de datos de bebidas
├── requirements.txt               # Dependencias
├── app/
│   ├── api/
│   │   ├── routes.py             # Rutas API (incluye endpoints del carrito)
│   │   └── vistas.py             # Vistas HTML
│   ├── core/
│   │   └── config.py             # Configuración
│   ├── models/
│   │   └── beverage.py           # Modelos de datos (incluye carrito)
│   ├── services/
│   │   ├── servicio_bebidas.py   # Lógica de negocio de bebidas
│   │   └── servicio_carrito.py   # Lógica de negocio del carrito
│   └── strategies/
│       ├── estrategias_busqueda.py    # Estrategias de búsqueda
│       ├── estrategias_precio.py      # Estrategias de precio
│       ├── estrategias_respuesta.py   # Estrategias de respuesta
│       └── estrategias_sugerencia.py  # Estrategias de sugerencia
├── templates/
│   ├── index.html                # Chat interactivo
│   └── home.html                 # Página de inicio
└── tests/                        # Pruebas unitarias
```

## 🔧 Configuración

### Variables de entorno (.env)
```env
HOST=0.0.0.0                     # Para acceso de red local
PUERTO=8000
DEBUG=false
RUTA_ARCHIVO_CSV=starbucks2.csv
```

### Configuración de red local
Para acceder desde otros dispositivos:

1. **Edita** `app/core/config.py`:
   ```python
   host: str = "0.0.0.0"  # Cambiar de "127.0.0.1"
   ```

2. **Configura el firewall** (Windows):
   ```powershell
   New-NetFirewallRule -DisplayName "FastAPI Port 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
   ```

3. **Obtén tu IP local**:
   ```cmd
   ipconfig | findstr "IPv4"
   ```

4. **Accede desde otros dispositivos**: `http://[TU_IP]:8000`

## 🎯 API Endpoints

### Búsqueda de bebidas
```http
POST /api/buscar
Content-Type: application/json

{
  "consulta": "latte",
  "idioma": "es"
}
```

### Sugerencias
```http
GET /api/sugerencias?consulta=cafe&limite=5
```

### Listar bebidas
```http
GET /api/bebidas?categoria=espresso&limite=10
```

### Estado de la API
```http
GET /api/salud
```

### Carrito de compras
```http
GET    /api/carrito                    # Obtener carrito actual
POST   /api/carrito/agregar            # Agregar bebida al carrito
PUT    /api/carrito/actualizar         # Actualizar cantidad
DELETE /api/carrito/eliminar/{bebida}  # Eliminar item específico
DELETE /api/carrito/vaciar             # Vaciar carrito
POST   /api/carrito/finalizar          # Finalizar compra
```

## 🏗️ Arquitectura - Patrón Strategy

La aplicación utiliza el patrón Strategy para:

- **🔍 Búsqueda**: Exacta, difusa, compuesta
- **💰 Precios**: Básico, por familia, premium  
- **📝 Respuestas**: Estándar, detallada, compacta
- **💡 Sugerencias**: Por similitud, por categoría, híbrida

## 📱 Acceso desde Dispositivos Móviles

1. Conecta el dispositivo a la misma red Wi-Fi
2. Configura `host: "0.0.0.0"` en la configuración
3. Abre el navegador y ve a `http://[IP_LOCAL]:8000`

## 🛠️ Desarrollo

### Ejecutar en modo desarrollo
```bash
python main_refactorizado.py  # Con recarga automática si debug=True
```

### Ejecutar pruebas
```bash
python -m pytest tests/
```

## 📚 Documentación Adicional

- **README_NETWORK.md**: Guía completa de configuración de red
- **MIGRATION_DOCUMENTATION.md**: Documentación de migración del código
- **CARRITO_DOCUMENTATION.md**: Documentación completa del sistema de carrito

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.
