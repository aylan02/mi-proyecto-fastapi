from pydantic import BaseModel, Field


class DetalleVentaCrear(BaseModel):
    producto_id: int = Field(..., gt=0)
    cantidad: int = Field(..., gt=0)


class DetalleVenta(BaseModel):
    producto_id: int
    producto_nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class VentaCrear(BaseModel):
    cliente_id: int = Field(..., gt=0)
    detalles: list[DetalleVentaCrear] = Field(..., min_length=1)
    metodo_pago: str = Field(..., min_length=3, max_length=50)
    observacion: str | None = Field(default="")


class Venta(BaseModel):
    id: int
    cliente_id: int
    cliente_nombre: str
    detalles: list[DetalleVenta]
    metodo_pago: str
    observacion: str | None = ""
    fecha: str
    total: float
    estado: str