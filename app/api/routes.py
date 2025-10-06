"""
Rutas API para el asistente de bebidas Starbucks.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from functools import lru_cache
from pathlib import Path

from app.models.beverage import (
    Bebida, SolicitudBusqueda, RespuestaBusqueda, RespuestaSugerencias,
    SolicitudAgregarCarrito, SolicitudActualizarCarrito, RespuestaCarrito, Carrito
)
from app.services.servicio_bebidas import ServicioBebidas
from app.services.servicio_carrito import ServicioCarrito
from app.core.config import configuracion


router = APIRouter(prefix="/api", tags=["api"])


@lru_cache()
def obtener_servicio_bebidas() -> ServicioBebidas:
    """Obtiene instancia del servicio de bebidas con caché."""
    ruta_csv = Path(configuracion.ruta_archivo_csv)
    return ServicioBebidas(ruta_csv)


@lru_cache()
def obtener_servicio_carrito() -> ServicioCarrito:
    """Obtiene instancia del servicio de carrito con caché."""
    servicio_bebidas = obtener_servicio_bebidas()
    return ServicioCarrito(servicio_bebidas)


@router.post("/buscar", response_model=RespuestaBusqueda)
async def buscar_bebida(
    solicitud: SolicitudBusqueda,
    servicio: ServicioBebidas = Depends(obtener_servicio_bebidas)
):
    """Busca una bebida por nombre."""
    try:
        resultado = servicio.buscar_bebida(solicitud.consulta)
        
        if resultado:
            return RespuestaBusqueda(
                encontrado=True,
                datos=resultado,
                texto=servicio.formatear_respuesta_encontrada(resultado),
                sugerencias=[]
            )
        else:
            sugerencias = servicio.obtener_sugerencias(solicitud.consulta)
            return RespuestaBusqueda(
                encontrado=False,
                datos=None,
                texto=servicio.formatear_respuesta_no_encontrada(solicitud.consulta, sugerencias),
                sugerencias=sugerencias
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")


@router.get("/sugerencias", response_model=RespuestaSugerencias)
async def obtener_sugerencias_bebidas(
    consulta: str,
    limite: int = 5,
    servicio: ServicioBebidas = Depends(obtener_servicio_bebidas)
):
    """Obtiene sugerencias de bebidas basadas en una consulta."""
    try:
        sugerencias = servicio.obtener_sugerencias(consulta, limite)
        return RespuestaSugerencias(elementos=sugerencias)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo sugerencias: {str(e)}")


@router.get("/bebidas", response_model=List[Bebida])
async def listar_bebidas(
    categoria: Optional[str] = None,
    limite: int = 50,
    servicio: ServicioBebidas = Depends(obtener_servicio_bebidas)
):
    """Lista todas las bebidas disponibles."""
    try:
        bebidas = servicio.obtener_todas_bebidas(categoria, limite)
        return bebidas
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando bebidas: {str(e)}")


@router.get("/salud")
async def verificar_salud():
    """Endpoint de verificación de salud de la API."""
    return {
        "estado": "ok",
        "mensaje": "API del asistente de bebidas funcionando correctamente",
        "version": configuracion.version_app
    }


# ========== ENDPOINTS DEL CARRITO DE COMPRAS ==========

@router.get("/carrito", response_model=Carrito)
async def obtener_carrito(
    sesion_id: str = "default",
    servicio: ServicioCarrito = Depends(obtener_servicio_carrito)
):
    """Obtiene el carrito actual de una sesión."""
    try:
        carrito = servicio.obtener_carrito(sesion_id)
        return carrito
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo carrito: {str(e)}")


@router.post("/carrito/agregar", response_model=RespuestaCarrito)
async def agregar_al_carrito(
    solicitud: SolicitudAgregarCarrito,
    sesion_id: str = "default",
    servicio: ServicioCarrito = Depends(obtener_servicio_carrito)
):
    """Agrega una bebida al carrito."""
    try:
        resultado = servicio.agregar_al_carrito(
            solicitud.nombre_bebida, 
            solicitud.cantidad, 
            sesion_id
        )
        
        if not resultado["ok"]:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        
        return RespuestaCarrito(**resultado)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error agregando al carrito: {str(e)}")


@router.put("/carrito/actualizar", response_model=RespuestaCarrito)
async def actualizar_cantidad_carrito(
    solicitud: SolicitudActualizarCarrito,
    sesion_id: str = "default",
    servicio: ServicioCarrito = Depends(obtener_servicio_carrito)
):
    """Actualiza la cantidad de un item en el carrito."""
    try:
        resultado = servicio.actualizar_cantidad(
            solicitud.nombre_bebida,
            solicitud.cantidad,
            sesion_id
        )
        
        if not resultado["ok"]:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        
        return RespuestaCarrito(**resultado)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando carrito: {str(e)}")


@router.delete("/carrito/eliminar/{nombre_bebida}")
async def eliminar_del_carrito(
    nombre_bebida: str,
    sesion_id: str = "default",
    servicio: ServicioCarrito = Depends(obtener_servicio_carrito)
):
    """Elimina un item específico del carrito."""
    try:
        resultado = servicio.eliminar_del_carrito(nombre_bebida, sesion_id)
        
        if not resultado["ok"]:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        
        return RespuestaCarrito(**resultado)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando del carrito: {str(e)}")


@router.delete("/carrito/vaciar")
async def vaciar_carrito(
    sesion_id: str = "default",
    servicio: ServicioCarrito = Depends(obtener_servicio_carrito)
):
    """Vacía completamente el carrito."""
    try:
        resultado = servicio.vaciar_carrito(sesion_id)
        return RespuestaCarrito(**resultado)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error vaciando carrito: {str(e)}")


@router.post("/carrito/finalizar")
async def finalizar_compra(
    sesion_id: str = "default",
    servicio: ServicioCarrito = Depends(obtener_servicio_carrito)
):
    """Finaliza la compra y vacía el carrito."""
    try:
        resultado = servicio.finalizar_compra(sesion_id)
        
        if not resultado["ok"]:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finalizando compra: {str(e)}")
