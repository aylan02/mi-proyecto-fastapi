from pydantic import BaseModel, Field
from typing import Optional

class Envio(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    destinatario: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)
    observacion: Optional[str] = Field(default=None, max_length=200)

class EnvioActualizar(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    destinatario: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)
    observacion: Optional[str] = Field(default=None, max_length=200)

class EstadoEnvioActualizar(BaseModel):
    estado: str = Field(..., min_length=2, max_length=30)