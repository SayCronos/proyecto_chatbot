# Servicio para manejar pedidos en la base de datos
from sqlalchemy.orm import Session
from app.models.pedido import Pedido, PedidoCreate, UsuarioRegistro
from app.database.config import get_db
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class ServicioPedidos:
    """Servicio para gestionar pedidos en la base de datos MySQL"""
    
    @staticmethod
    def registrar_usuario(db: Session, usuario_data: UsuarioRegistro) -> Pedido:
        """
        Registra un nuevo usuario en la base de datos
        Crea un registro inicial sin bebida ni precio
        """
        try:
            # Convertir celular a int (remover caracteres no numéricos)
            telefono_limpio = ''.join(filter(str.isdigit, usuario_data.celular))
            # Limitar a los últimos 10 dígitos para evitar overflow de int(11)
            if len(telefono_limpio) > 10:
                telefono_limpio = telefono_limpio[-10:]
            telefono_int = int(telefono_limpio) if telefono_limpio else 0
            
            nuevo_pedido = Pedido(
                nombre_usuario=usuario_data.nombre,
                direccion=usuario_data.direccion,
                telefono=telefono_int,
                nombre_bebida=None,
                precio=None
            )
            
            db.add(nuevo_pedido)
            db.commit()
            db.refresh(nuevo_pedido)
            
            logger.info(f"Usuario registrado: {usuario_data.nombre} - ID: {nuevo_pedido.id_pedido}")
            return nuevo_pedido
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error registrando usuario: {e}")
            raise e
    
    @staticmethod
    def crear_pedido_completo(db: Session, pedido_data: PedidoCreate) -> Pedido:
        """
        Crea un pedido completo con bebida y precio
        """
        try:
            # Convertir teléfono a int
            telefono_limpio = ''.join(filter(str.isdigit, str(pedido_data.telefono)))
            # Limitar a los últimos 10 dígitos para evitar overflow de int(11)
            if len(telefono_limpio) > 10:
                telefono_limpio = telefono_limpio[-10:]
            telefono_int = int(telefono_limpio) if telefono_limpio else 0
            
            nuevo_pedido = Pedido(
                nombre_usuario=pedido_data.nombre_usuario,
                direccion=pedido_data.direccion,
                telefono=telefono_int,
                nombre_bebida=pedido_data.nombre_bebida,
                precio=pedido_data.precio
            )
            
            db.add(nuevo_pedido)
            db.commit()
            db.refresh(nuevo_pedido)
            
            logger.info(f"Pedido creado: {pedido_data.nombre_bebida} - ID: {nuevo_pedido.id_pedido}")
            return nuevo_pedido
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creando pedido: {e}")
            raise e
    
    @staticmethod
    def actualizar_pedido_con_bebida(db: Session, usuario_nombre: str, nombre_bebida: str, precio: float) -> Optional[Pedido]:
        """
        Actualiza un pedido existente agregando la bebida y precio
        """
        try:
            # Buscar el pedido más reciente del usuario sin bebida
            pedido = db.query(Pedido).filter(
                Pedido.nombre_usuario == usuario_nombre,
                Pedido.nombre_bebida.is_(None)
            ).order_by(Pedido.id_pedido.desc()).first()
            
            if pedido:
                pedido.nombre_bebida = nombre_bebida
                pedido.precio = precio
                db.commit()
                db.refresh(pedido)
                logger.info(f"Pedido actualizado: {nombre_bebida} - ID: {pedido.id_pedido}")
                return pedido
            else:
                logger.warning(f"No se encontró pedido pendiente para usuario: {usuario_nombre}")
                return None
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error actualizando pedido: {e}")
            raise e
    
    @staticmethod
    def obtener_pedidos_usuario(db: Session, nombre_usuario: str) -> List[Pedido]:
        """
        Obtiene todos los pedidos de un usuario
        """
        try:
            pedidos = db.query(Pedido).filter(
                Pedido.nombre_usuario == nombre_usuario
            ).order_by(Pedido.fecha_pedido.desc()).all()
            
            return pedidos
            
        except Exception as e:
            logger.error(f"Error obteniendo pedidos: {e}")
            raise e
    
    @staticmethod
    def obtener_todos_pedidos(db: Session, limit: int = 100) -> List[Pedido]:
        """
        Obtiene todos los pedidos (para administración)
        """
        try:
            pedidos = db.query(Pedido).order_by(
                Pedido.fecha_pedido.desc()
            ).limit(limit).all()
            
            return pedidos
            
        except Exception as e:
            logger.error(f"Error obteniendo todos los pedidos: {e}")
            raise e
