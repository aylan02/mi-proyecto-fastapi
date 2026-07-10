from pydantic import BaseModel, Field
from typing import Optional


class ProductoEnvio(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)


class Envio(BaseModel):
    productos: list[ProductoEnvio]

    destinatario: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)

    observacion: Optional[str] = Field(default=None, max_length=200)

    ruta: Optional[str] = None
    vehiculo: Optional[str] = None
    fecha_programada: Optional[str] = None

    venta_id: Optional[int] = None


class EnvioActualizar(Envio):
    pass


class EstadoEnvioActualizar(BaseModel):
    estado: str = Field(..., min_length=2, max_length=30)