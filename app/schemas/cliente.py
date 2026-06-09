from pydantic import BaseModel, Field


class ClienteBase(BaseModel):
    rut: str = Field(..., min_length=3, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)
    correo: str = Field(..., min_length=5, max_length=120)
    telefono: str = Field(..., min_length=6, max_length=30)
    estado: str = Field(default="Activo")


class ClienteCrear(ClienteBase):
    pass


class ClienteActualizar(BaseModel):
    rut: str | None = Field(default=None, min_length=3, max_length=20)
    nombre: str | None = Field(default=None, min_length=3, max_length=100)
    direccion: str | None = Field(default=None, min_length=5, max_length=200)
    correo: str | None = Field(default=None, min_length=5, max_length=120)
    telefono: str | None = Field(default=None, min_length=6, max_length=30)
    estado: str | None = None


class Cliente(ClienteBase):
    id: int