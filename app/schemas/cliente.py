from pydantic import BaseModel, Field


class ClienteBase(BaseModel):
    rut: str | None = None
    nombre: str = Field(..., min_length=3, max_length=100)
    direccion: str = ""
    correo: str = Field(..., min_length=5, max_length=120)
    telefono: str = ""
    estado: str = "Activo"


class ClienteCrear(ClienteBase):
    pass


class ClienteActualizar(BaseModel):
    rut: str | None = None
    nombre: str | None = None
    direccion: str | None = None
    correo: str | None = None
    telefono: str | None = None
    estado: str | None = None


class Cliente(ClienteBase):
    id: int

class ClientePerfilActualizar(BaseModel):
    nombre: str
    apellido: str
    correo: str
    telefono: str
    direccion: str