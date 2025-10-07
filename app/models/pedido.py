# Modelo para la tabla pedido
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database.config import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo SQLAlchemy para la tabla pedido (coincide exactamente con tu tabla)
class Pedido(Base):
    __tablename__ = "pedido"
    
    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_usuario = Column(String(100), nullable=False)
    direccion = Column(String(100), nullable=False)
    telefono = Column(Integer, nullable=False)
    nombre_bebida = Column(String(100), nullable=True)
    precio = Column(Float, nullable=True)
    # Nota: No incluimos fecha_pedido ya que no existe en tu tabla actual

# Modelos Pydantic para las APIs
class PedidoCreate(BaseModel):
    nombre_usuario: str
    direccion: str
    telefono: str
    nombre_bebida: Optional[str] = None
    precio: Optional[float] = None

class PedidoResponse(BaseModel):
    id_pedido: int
    nombre_usuario: str
    direccion: str
    telefono: int  # Cambiado a int para coincidir con la base de datos
    nombre_bebida: Optional[str]
    precio: Optional[float]
    
    class Config:
        from_attributes = True

class UsuarioRegistro(BaseModel):
    nombre: str
    direccion: str
    celular: str
