"""
Modelos de datos para la aplicación de bebidas Starbucks.
"""
from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel


@dataclass
class Bebida:
    """Modelo de datos para una bebida."""
    nombre_en: str
    nombre_es: str
    metodo: str
    calorias: Optional[float]
    grasa_total: Optional[float]
    categoria: Optional[str] = None
    precio: Optional[float] = None
    url_imagen: Optional[str] = None
    descripcion: Optional[str] = None


class SolicitudBusqueda(BaseModel):
    """Modelo de solicitud para búsqueda de bebidas."""
    consulta: str
    idioma: str = "es"


class RespuestaBusqueda(BaseModel):
    """Modelo de respuesta para búsqueda de bebidas."""
    ok: bool = True
    encontrado: bool
    idioma: str = "es"
    datos: Optional[Bebida] = None
    texto: str
    sugerencias: list[Bebida] = []


class RespuestaSugerencias(BaseModel):
    """Modelo de respuesta para sugerencias de bebidas."""
    ok: bool = True
    idioma: str = "es"
    elementos: list[Bebida]


# Modelos para el carrito de compras
class ItemCarrito(BaseModel):
    """Modelo para un item del carrito de compras."""
    bebida: Bebida
    cantidad: int = 1
    subtotal: float
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal del item basado en cantidad y precio."""
        precio = self.bebida.precio or 0.0
        return precio * self.cantidad


class Carrito(BaseModel):
    """Modelo para el carrito de compras completo."""
    items: List[ItemCarrito] = []
    total: float = 0.0
    
    def calcular_total(self) -> float:
        """Calcula el total del carrito sumando todos los subtotales."""
        return sum(item.subtotal for item in self.items)
    
    def agregar_item(self, bebida: Bebida, cantidad: int = 1) -> None:
        """Agrega un item al carrito o incrementa la cantidad si ya existe."""
        # Buscar si la bebida ya está en el carrito
        for item in self.items:
            if item.bebida.nombre_es == bebida.nombre_es:
                item.cantidad += cantidad
                item.subtotal = item.calcular_subtotal()
                self.total = self.calcular_total()
                return
        
        # Si no existe, crear nuevo item
        precio = bebida.precio or 0.0
        nuevo_item = ItemCarrito(
            bebida=bebida,
            cantidad=cantidad,
            subtotal=precio * cantidad
        )
        self.items.append(nuevo_item)
        self.total = self.calcular_total()
    
    def actualizar_cantidad(self, nombre_bebida: str, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un item específico."""
        for item in self.items:
            if item.bebida.nombre_es == nombre_bebida:
                if nueva_cantidad <= 0:
                    self.items.remove(item)
                else:
                    item.cantidad = nueva_cantidad
                    item.subtotal = item.calcular_subtotal()
                self.total = self.calcular_total()
                return True
        return False
    
    def eliminar_item(self, nombre_bebida: str) -> bool:
        """Elimina un item del carrito."""
        for item in self.items:
            if item.bebida.nombre_es == nombre_bebida:
                self.items.remove(item)
                self.total = self.calcular_total()
                return True
        return False
    
    def vaciar(self) -> None:
        """Vacía completamente el carrito."""
        self.items = []
        self.total = 0.0


# Modelos para las operaciones del carrito
class SolicitudAgregarCarrito(BaseModel):
    """Modelo de solicitud para agregar item al carrito."""
    nombre_bebida: str
    cantidad: int = 1


class SolicitudActualizarCarrito(BaseModel):
    """Modelo de solicitud para actualizar cantidad en el carrito."""
    nombre_bebida: str
    cantidad: int


class RespuestaCarrito(BaseModel):
    """Modelo de respuesta para operaciones del carrito."""
    ok: bool = True
    mensaje: str
    carrito: Carrito
