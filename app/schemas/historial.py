from pydantic import BaseModel


class HistorialCompra(BaseModel):
    id: int
    fecha: str
    total: float
    metodo_pago: str
    estado: str