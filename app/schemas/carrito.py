from pydantic import BaseModel, Field


class AgregarProductoCarrito(BaseModel):
    cliente_id: int = Field(..., gt=0)
    producto_id: int = Field(..., gt=0)
    cantidad: int = Field(..., gt=0)


class ActualizarCantidadCarrito(BaseModel):
    cantidad: int = Field(..., gt=0)


class ItemCarrito(BaseModel):
    producto_id: int
    cantidad: int


class ItemCarritoResponse(BaseModel):
    producto_id: int
    nombre: str
    marca: str
    categoria: str
    imagen: str
    precio: float
    cantidad: int
    subtotal: float


class Carrito(BaseModel):
    cliente_id: int
    items: list[ItemCarrito]


class CarritoResponse(BaseModel):
    cliente_id: int
    items: list[ItemCarritoResponse]
    total_productos: int
    total: float