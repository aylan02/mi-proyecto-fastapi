from pydantic import BaseModel, Field
from typing import Optional


class ProductoBase(BaseModel):
    codigo: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Código único del producto"
    )
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100
    )
    marca: str = Field(
        ...,
        min_length=2,
        max_length=100
    )
    categoria: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    precio: float = Field(
        ...,
        gt=0
    )
    stock: int = Field(
        ...,
        ge=0
    )
    descripcion: str = Field(
        ...,
        min_length=3,
        max_length=250
    )


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(BaseModel):
    codigo: Optional[str] = Field(None, min_length=3, max_length=20)
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    marca: Optional[str] = Field(None, min_length=2, max_length=100)
    categoria: Optional[str] = Field(None, min_length=2, max_length=50)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    descripcion: Optional[str] = Field(None, min_length=3, max_length=250)


class Producto(ProductoBase):
    id: int
    estado: str = Field(
        default="Activo",
        description="Activo o Inactivo"
    )

    class Config:
        from_attributes = True