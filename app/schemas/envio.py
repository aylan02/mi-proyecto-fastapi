from pydantic import BaseModel, Field

class Envio(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    destinatario: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)