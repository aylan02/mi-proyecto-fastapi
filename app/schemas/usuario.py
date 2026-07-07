from pydantic import BaseModel, Field


class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: str = Field(..., min_length=5, max_length=100)
    rol: str = Field(..., min_length=3, max_length=100)
    estado: str = Field(default="Activo")


class UsuarioCrear(UsuarioBase):
    pass


class UsuarioActualizar(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    password: str | None = Field(default=None, min_length=4, max_length=100)
    nombre: str | None = Field(default=None, min_length=3, max_length=100)
    rol: str | None = Field(default=None, min_length=3, max_length=100)
    estado: str | None = None


class Usuario(UsuarioBase):
    id: int