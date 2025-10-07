# 🛒 Sistema de Carrito de Compras - Starbucks Chatbot

## Descripción General

El sistema de carrito de compras permite a los usuarios agregar bebidas encontradas a través del chatbot a un carrito persistente, gestionar cantidades, y simular el proceso de compra. **Tanto el carrito como el chatbot están completamente integrados en la página principal (`home.html`).**

## ✨ Características Principales

- **🛒 Carrito Flotante**: Sidebar deslizable con diseño Starbucks
- **💾 Persistencia**: Los datos se guardan en localStorage
- **🔢 Gestión de Cantidades**: Botones +/- para ajustar cantidades
- **💰 Cálculos Automáticos**: Subtotales y total se actualizan en tiempo real
- **🗑️ Eliminación de Items**: Botón para remover productos individuales
- **✅ Finalizar Compra**: Proceso de checkout simulado
- **🏷️ Badge Contador**: Indicador visual del número de items
- **🎨 Modal Personalizado**: Notificaciones elegantes con diseño Starbucks

## 🏗️ Arquitectura del Sistema

### Backend (Python/FastAPI)

#### Modelos de Datos
```python
# app/models/beverage.py

class ItemCarrito(BaseModel):
    """Item individual del carrito"""
    cantidad: int = 1
    subtotal: float

class Carrito(BaseModel):
    """Carrito completo con métodos de gestión"""
    items: List[ItemCarrito]
    total: float = 0.0
```
GET    /api/carrito                 # Obtener carrito actual
POST   /api/carrito/agregar         # Agregar bebida al carrito
PUT    /api/carrito/actualizar      # Actualizar cantidad
DELETE /api/carrito/eliminar/{item} # Eliminar item específico
DELETE /api/carrito/vaciar          # Vaciar carrito completo
POST   /api/carrito/finalizar       # Finalizar compra
```

### Frontend (JavaScript/HTML/CSS)

#### Componentes Visuales

1. **Botón Flotante del Carrito**
   - Posición fija en esquina inferior derecha
   - Badge con contador de items
   - Icono de carrito 🛒

2. **Sidebar del Carrito**
   - Panel deslizable desde la derecha
   - Overlay semitransparente
   - Header con título y botón cerrar

3. **Lista de Items**
   - Imagen de la bebida
   - Nombre y precio unitario
   - Controles de cantidad (+/-)
   - Botón eliminar
   - Subtotal por item

4. **Resumen de Compra**
   - Total general
   - Botón "Finalizar Compra"

#### Funciones JavaScript Principales

```javascript
// Gestión de datos
cargarCarrito()           // Carga desde localStorage
guardarCarrito()          // Guarda en localStorage
actualizarVisualizacion() // Actualiza UI

// Operaciones del carrito
agregarAlCarrito(bebida)  // Agrega nueva bebida
cambiarCantidad(nombre, cantidad) // Modifica cantidad
eliminarDelCarrito(nombre) // Elimina item
finalizarCompra()         // Procesa compra

// Control de UI
abrirCarrito()           // Muestra sidebar
cerrarCarrito()          // Oculta sidebar
renderizarItemsCarrito() // Actualiza lista visual
```

## 🎨 Diseño y Estilos

### Modal Personalizado Starbucks
El sistema incluye un modal completamente personalizado que reemplaza las alertas nativas del navegador:

**Características del Modal:**
- **Gradiente de fondo**: Verde Starbucks con efectos de profundidad
- **Animaciones suaves**: Slide-in y efectos de escala
- **Backdrop blur**: Efecto de desenfoque en el fondo
- **Iconos contextuales**: 🎉 para éxito, ❌ para errores, 🗑️ para eliminaciones
- **Auto-cierre**: Se cierra automáticamente después de 5 segundos
- **Interactividad**: Cierre con Escape, clic en overlay, o botones
- **Responsive**: Se adapta a diferentes tamaños de pantalla

**Tipos de Modal:**
```javascript
// Compra finalizada con detalles de productos
mostrarModalCompraFinalizada(totalItems, totalPrecio, itemsComprados);

// Error
mostrarModalError('Mensaje de error');

// Eliminación
mostrarModalEliminacion(nombreBebida);
```

**Ejemplo de Modal de Compra Finalizada:**
```
🎉 ¡Compra Finalizada!
Tu pedido ha sido procesado exitosamente

Resumen de tu pedido:
[🖼️] 2x Latte
     $4.50 c/u = $9.00

[🖼️] 1x Cappuccino  
     $4.00 c/u = $4.00

─────────────────────
Total: $13.00

[Seguir Comprando] [¡Perfecto!]
```

**Nota:** [🖼️] representa la imagen real del producto (50x50px) que se muestra en el modal.

### Paleta de Colores Starbucks
```css
:root {
  --accent: #006241;     /* Verde Starbucks */
  --fg: #fff;            /* Blanco */
  --bg1: #e8f3ee;        /* Verde claro */
  --bg2: #f6fbf9;        /* Verde muy claro */
  --text: #142021;       /* Texto oscuro */
  --muted: #6b7a7a;      /* Texto secundario */
}
```

### Componentes CSS Clave
- `.cart-sidebar`: Panel principal del carrito
- `.cart-item`: Item individual con controles
- `.cart-button`: Botón flotante con badge
- `.qty-btn`: Botones de cantidad
- `.btn-add-cart`: Botón agregar en tarjetas de bebida

## 💾 Persistencia de Datos

### localStorage Schema
```javascript
{
  "starbucks_carrito": {
    "items": [
      {
        "bebida": {
          "nombre_es": "Latte",
          "precio": 4.50,
          "url_imagen": "...",
          // ... otros campos de bebida
        },
        "cantidad": 2,
        "subtotal": 9.00
      }
    ],
    "total": 9.00
  }
}
```

### Sincronización
- **Carga inicial**: `cargarCarrito()` al iniciar la página
- **Guardado automático**: Cada operación guarda inmediatamente
- **Persistencia**: Los datos sobreviven recargas de página

## 🔄 Flujo de Usuario

1. **Búsqueda de Bebida**
   - Usuario busca bebida en el chat (integrado en home.html)
   - Se muestra tarjeta con información detallada
   - Aparece botón "🛒 Añadir al carrito"

2. **Agregar al Carrito**
   - Click en botón agregar
   - Item se agrega al localStorage
   - Badge se actualiza automáticamente
   - Mensaje de confirmación en chat

3. **Gestión del Carrito**
   - Click en botón flotante del carrito (en `home.html`)
   - Se abre sidebar con items
   - Usuario puede modificar cantidades
   - Eliminar items individuales
   - Ver total actualizado

4. **Finalizar Compra**
   - Click en "Finalizar Compra"
   - Simulación de procesamiento
   - Carrito se vacía
   - Mensaje de confirmación
   - Sidebar se cierra automáticamente

5. **Cerrar Chat**
   - Botón "×" cierra completamente el widget del chat
   - Botón "–" minimiza el chat

## 🛠️ Integración con el Chat

### Modificaciones en `drinkCard()`
```javascript
// Se agregó botón "Añadir al carrito" a cada tarjeta de bebida
const addButton = document.createElement('button');
addButton.className = 'btn-add-cart';
addButton.textContent = '🛒 Añadir al carrito';
addButton.onclick = () => agregarAlCarrito(d);
```

### Mensajes del Sistema (Modal Personalizado)
- **Compra finalizada**: Modal elegante con gradiente verde, icono 🎉 y **lista detallada de productos comprados**
  - **Imágenes de productos** (50x50px) con bordes redondeados
  - Muestra cada producto con cantidad, nombre y subtotal
  - Precio unitario y total por item
  - Layout tipo card con imagen a la izquierda
  - Total general con separador visual
- **Eliminación**: Modal con icono 🗑️ y confirmación de eliminación
- **Errores**: Modal con icono ❌ y mensaje de error personalizado
- **Confirmación de agregado**: Mensaje en el chat integrado

## 🚀 Instalación y Uso

### Requisitos
- El sistema funciona con la estructura existente del chatbot
- No requiere dependencias adicionales
- Compatible con navegadores modernos

### Activación
1. El carrito se inicializa automáticamente al cargar la página
2. Los datos se cargan desde localStorage si existen
3. Todos los event listeners se configuran automáticamente

### Testing
```javascript
// Probar funcionalidades en consola del navegador
agregarAlCarrito({nombre_es: "Test Latte", precio: 5.0});
abrirCarrito();
cambiarCantidad("Test Latte", 3);
finalizarCompra();
```

## 🔧 Configuración Avanzada

### Personalización de Estilos
Los estilos del carrito pueden modificarse editando las clases CSS:
- Cambiar colores en las variables CSS `:root`
- Ajustar tamaños en `.cart-sidebar`
- Modificar animaciones en `transition` properties

### Extensiones Futuras
- Integración con API de pagos real
- Descuentos y cupones
- Historial de compras
- Favoritos y listas de deseos
- Notificaciones push

## 📱 Responsividad

El carrito está optimizado para:
- **Desktop**: Sidebar de 400px de ancho
- **Tablet**: Se adapta al ancho disponible
- **Mobile**: Ocupa pantalla completa en dispositivos pequeños

## 🐛 Solución de Problemas

### Problemas Comunes
1. **Carrito no se guarda**: Verificar que localStorage esté habilitado
2. **Badge no se actualiza**: Revisar llamadas a `actualizarVisualizacionCarrito()`
3. **Botones no funcionan**: Verificar event listeners en consola
4. **Estilos rotos**: Verificar que CSS del carrito esté cargado

### Debug
```javascript
// Verificar estado del carrito
console.log('Carrito actual:', carritoLocal);

// Verificar localStorage
console.log('Carrito guardado:', localStorage.getItem('starbucks_carrito'));

// Limpiar carrito para testing
localStorage.removeItem('starbucks_carrito');
location.reload();
```

## 📊 Métricas y Analytics

### Eventos Trackeable
- `carrito_item_agregado`: Cuando se agrega un item
- `carrito_cantidad_cambiada`: Modificación de cantidades
- `carrito_item_eliminado`: Eliminación de items
- `carrito_compra_finalizada`: Checkout completado
- `carrito_abierto`: Apertura del sidebar
- `carrito_cerrado`: Cierre del sidebar

### KPIs Sugeridos
- Tasa de conversión (búsquedas → items agregados)
- Valor promedio del carrito
- Items más agregados
- Abandono del carrito
- Tiempo en carrito abierto
