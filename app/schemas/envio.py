from pydantic import BaseModel, Field
from typing import Optional

class Envio(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    destinatario: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)
    observacion: Optional[str] = Field(default=None, max_length=200)
    ruta: Optional[str] = None
    vehiculo: Optional[str] = None
    fecha_programada: Optional[str] = None
    venta_id: Optional[int] = None

class EnvioActualizar(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    destinatario: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)
    observacion: Optional[str] = Field(default=None, max_length=200)
    ruta: Optional[str] = None
    vehiculo: Optional[str] = None
    fecha_programada: Optional[str] = None
    venta_id: Optional[int] = None
    
class EstadoEnvioActualizar(BaseModel):
    estado: str = Field(..., min_length=2, max_length=30)