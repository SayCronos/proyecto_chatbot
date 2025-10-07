# API endpoints para pedidos
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.pedido import PedidoCreate, PedidoResponse, UsuarioRegistro
from app.services.servicio_pedidos import ServicioPedidos
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pedidos", tags=["pedidos"])

@router.post("/registrar-usuario", response_model=PedidoResponse)
async def registrar_usuario(
    usuario_data: UsuarioRegistro,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario en la base de datos
    Crea un registro inicial para el usuario
    """
    try:
        pedido = ServicioPedidos.registrar_usuario(db, usuario_data)
        return pedido
    except Exception as e:
        logger.error(f"Error en registro de usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registrando usuario: {str(e)}"
        )

@router.post("/crear-pedido", response_model=PedidoResponse)
async def crear_pedido(
    pedido_data: PedidoCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un pedido completo con bebida y precio
    """
    try:
        pedido = ServicioPedidos.crear_pedido_completo(db, pedido_data)
        return pedido
    except Exception as e:
        logger.error(f"Error creando pedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creando pedido: {str(e)}"
        )

@router.put("/actualizar-pedido/{usuario_nombre}")
async def actualizar_pedido_con_bebida(
    usuario_nombre: str,
    nombre_bebida: str,
    precio: float,
    db: Session = Depends(get_db)
):
    """
    Actualiza un pedido existente agregando bebida y precio
    """
    try:
        pedido = ServicioPedidos.actualizar_pedido_con_bebida(
            db, usuario_nombre, nombre_bebida, precio
        )
        
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró pedido pendiente para el usuario"
            )
        
        return {"message": "Pedido actualizado exitosamente", "pedido": pedido}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando pedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando pedido: {str(e)}"
        )

@router.get("/usuario/{nombre_usuario}", response_model=List[PedidoResponse])
async def obtener_pedidos_usuario(
    nombre_usuario: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los pedidos de un usuario específico
    """
    try:
        pedidos = ServicioPedidos.obtener_pedidos_usuario(db, nombre_usuario)
        return pedidos
    except Exception as e:
        logger.error(f"Error obteniendo pedidos del usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo pedidos: {str(e)}"
        )

@router.get("/todos", response_model=List[PedidoResponse])
async def obtener_todos_pedidos(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los pedidos (para administración)
    """
    try:
        pedidos = ServicioPedidos.obtener_todos_pedidos(db, limit)
        return pedidos
    except Exception as e:
        logger.error(f"Error obteniendo todos los pedidos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo pedidos: {str(e)}"
        )

@router.get("/test-conexion")
async def test_conexion_db():
    """
    Endpoint para probar la conexión a la base de datos
    """
    try:
        from app.database.config import test_connection
        if test_connection():
            return {"status": "success", "message": "Conexión a base de datos exitosa"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error conectando a la base de datos"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de conexión: {str(e)}"
        )
