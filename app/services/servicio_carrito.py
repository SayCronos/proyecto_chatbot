"""
Servicio para la gestión del carrito de compras.
Maneja la lógica de negocio relacionada con el carrito de compras de bebidas.
"""
from typing import Optional, Dict, Any
from app.models.beverage import Carrito, Bebida, ItemCarrito
from app.services.servicio_bebidas import ServicioBebidas


class ServicioCarrito:
    """
    Servicio para gestionar operaciones del carrito de compras.
    
    Este servicio maneja:
    - Agregar bebidas al carrito
    - Actualizar cantidades
    - Eliminar items
    - Calcular totales
    - Persistir datos del carrito
    """
    
    def __init__(self, servicio_bebidas: ServicioBebidas):
        """
        Inicializa el servicio del carrito.
        
        Args:
            servicio_bebidas: Servicio de bebidas para obtener información de productos
        """
        self.servicio_bebidas = servicio_bebidas
        self._carritos: Dict[str, Carrito] = {}  # Simulamos storage por sesión
    
    def obtener_carrito(self, sesion_id: str = "default") -> Carrito:
        """
        Obtiene el carrito para una sesión específica.
        
        Args:
            sesion_id: Identificador de la sesión (por defecto "default")
            
        Returns:
            Carrito: El carrito de la sesión
        """
        if sesion_id not in self._carritos:
            self._carritos[sesion_id] = Carrito()
        return self._carritos[sesion_id]
    
    def agregar_al_carrito(self, nombre_bebida: str, cantidad: int = 1, sesion_id: str = "default") -> Dict[str, Any]:
        """
        Agrega una bebida al carrito.
        
        Args:
            nombre_bebida: Nombre de la bebida a agregar
            cantidad: Cantidad a agregar (por defecto 1)
            sesion_id: Identificador de la sesión
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            # Buscar la bebida en el servicio de bebidas
            bebida = self.servicio_bebidas.buscar_bebida(nombre_bebida)
            
            if not bebida:
                return {
                    "ok": False,
                    "mensaje": f"No se encontró la bebida '{nombre_bebida}'",
                    "carrito": self.obtener_carrito(sesion_id)
                }
            
            # Obtener el carrito y agregar el item
            carrito = self.obtener_carrito(sesion_id)
            carrito.agregar_item(bebida, cantidad)
            
            return {
                "ok": True,
                "mensaje": f"Se agregó {cantidad}x {bebida.nombre_es} al carrito",
                "carrito": carrito
            }
            
        except Exception as e:
            return {
                "ok": False,
                "mensaje": f"Error al agregar al carrito: {str(e)}",
                "carrito": self.obtener_carrito(sesion_id)
            }
    
    def actualizar_cantidad(self, nombre_bebida: str, nueva_cantidad: int, sesion_id: str = "default") -> Dict[str, Any]:
        """
        Actualiza la cantidad de un item en el carrito.
        
        Args:
            nombre_bebida: Nombre de la bebida a actualizar
            nueva_cantidad: Nueva cantidad (0 para eliminar)
            sesion_id: Identificador de la sesión
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            carrito = self.obtener_carrito(sesion_id)
            
            if carrito.actualizar_cantidad(nombre_bebida, nueva_cantidad):
                if nueva_cantidad <= 0:
                    mensaje = f"Se eliminó {nombre_bebida} del carrito"
                else:
                    mensaje = f"Se actualizó la cantidad de {nombre_bebida} a {nueva_cantidad}"
                
                return {
                    "ok": True,
                    "mensaje": mensaje,
                    "carrito": carrito
                }
            else:
                return {
                    "ok": False,
                    "mensaje": f"No se encontró {nombre_bebida} en el carrito",
                    "carrito": carrito
                }
                
        except Exception as e:
            return {
                "ok": False,
                "mensaje": f"Error al actualizar cantidad: {str(e)}",
                "carrito": self.obtener_carrito(sesion_id)
            }
    
    def eliminar_del_carrito(self, nombre_bebida: str, sesion_id: str = "default") -> Dict[str, Any]:
        """
        Elimina un item del carrito.
        
        Args:
            nombre_bebida: Nombre de la bebida a eliminar
            sesion_id: Identificador de la sesión
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            carrito = self.obtener_carrito(sesion_id)
            
            if carrito.eliminar_item(nombre_bebida):
                return {
                    "ok": True,
                    "mensaje": f"Se eliminó {nombre_bebida} del carrito",
                    "carrito": carrito
                }
            else:
                return {
                    "ok": False,
                    "mensaje": f"No se encontró {nombre_bebida} en el carrito",
                    "carrito": carrito
                }
                
        except Exception as e:
            return {
                "ok": False,
                "mensaje": f"Error al eliminar del carrito: {str(e)}",
                "carrito": self.obtener_carrito(sesion_id)
            }
    
    def vaciar_carrito(self, sesion_id: str = "default") -> Dict[str, Any]:
        """
        Vacía completamente el carrito.
        
        Args:
            sesion_id: Identificador de la sesión
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            carrito = self.obtener_carrito(sesion_id)
            carrito.vaciar()
            
            return {
                "ok": True,
                "mensaje": "Carrito vaciado exitosamente",
                "carrito": carrito
            }
            
        except Exception as e:
            return {
                "ok": False,
                "mensaje": f"Error al vaciar carrito: {str(e)}",
                "carrito": self.obtener_carrito(sesion_id)
            }
    
    def finalizar_compra(self, sesion_id: str = "default") -> Dict[str, Any]:
        """
        Simula la finalización de una compra.
        
        Args:
            sesion_id: Identificador de la sesión
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            carrito = self.obtener_carrito(sesion_id)
            
            if not carrito.items:
                return {
                    "ok": False,
                    "mensaje": "El carrito está vacío",
                    "carrito": carrito
                }
            
            # Simular procesamiento de compra
            total_items = sum(item.cantidad for item in carrito.items)
            total_precio = carrito.total
            
            # Vaciar el carrito después de la compra
            carrito.vaciar()
            
            return {
                "ok": True,
                "mensaje": f"¡Compra finalizada! {total_items} productos por ${total_precio:.2f}",
                "carrito": carrito,
                "resumen_compra": {
                    "total_items": total_items,
                    "total_precio": total_precio
                }
            }
            
        except Exception as e:
            return {
                "ok": False,
                "mensaje": f"Error al finalizar compra: {str(e)}",
                "carrito": self.obtener_carrito(sesion_id)
            }
