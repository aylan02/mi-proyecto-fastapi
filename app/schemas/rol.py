from pydantic import BaseModel, Field


class RolBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=3, max_length=200)
    estado: str = Field(default="Activo")
    permisos: list[str]


class RolCrear(RolBase):
    pass


class RolActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=3, max_length=100)
    descripcion: str | None = Field(default=None, min_length=3, max_length=200)
    estado: str | None = None
    permisos: list[str] | None = None


class Rol(RolBase):
    id: int