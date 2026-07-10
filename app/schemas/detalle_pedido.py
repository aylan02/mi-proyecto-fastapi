from pydantic import BaseModel


class ProductoDetalle(BaseModel):
    producto_id: int
    producto_nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class DetallePedido(BaseModel):
    id: int
    cliente_id: int
    cliente_nombre: str
    fecha: str
    metodo_pago: str
    estado: str
    total: float
    observacion: str
    detalles: list[ProductoDetalle]