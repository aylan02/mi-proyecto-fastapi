from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class TipoMovimiento(str, Enum):
    INGRESO = "Ingreso"
    SALIDA = "Salida"
    AJUSTE = "Ajuste"


class MovimientoInventarioBase(BaseModel):
    producto_id: int = Field(
        ...,
        gt=0,
        description="ID del producto"
    )

    tipo: TipoMovimiento

    cantidad: int = Field(
        ...,
        gt=0,
        description="Cantidad del movimiento"
    )

    motivo: str = Field(
        ...,
        min_length=3,
        max_length=150
    )

    usuario: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class MovimientoInventarioCrear(MovimientoInventarioBase):
    pass


class MovimientoInventarioActualizar(BaseModel):
    motivo: Optional[str] = Field(
        None,
        min_length=3,
        max_length=150
    )

    usuario: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )


class MovimientoInventario(MovimientoInventarioBase):
    id: int

    fecha: datetime = Field(
        default_factory=datetime.now
    )

    class Config:
        from_attributes = True