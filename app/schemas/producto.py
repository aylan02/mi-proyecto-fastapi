from pydantic import BaseModel, Field

class Producto(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    marca: str = Field(..., min_length=2, max_length=100)
    categoria: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    descripcion: str = Field(..., min_length=3, max_length=200)

class ProductoCrear(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    marca: str = Field(..., min_length=2, max_length=100)
    categoria: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    descripcion: str = Field(..., min_length=3, max_length=200)

class ProductoActualizar(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    marca: str = Field(..., min_length=2, max_length=100)
    categoria: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    descripcion: str = Field(..., min_length=3, max_length=200)