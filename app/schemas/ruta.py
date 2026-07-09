from pydantic import BaseModel, Field


class RutaBase(BaseModel):
    origen: str = Field(..., min_length=3, max_length=100)
    destino: str = Field(..., min_length=3, max_length=100)
    distancia: str = Field(..., min_length=1, max_length=50)
    estado: str = Field(default="Activa")


class RutaCrear(RutaBase):
    pass


class RutaActualizar(BaseModel):
    origen: str | None = Field(default=None, min_length=3, max_length=100)
    destino: str | None = Field(default=None, min_length=3, max_length=100)
    distancia: str | None = Field(default=None, min_length=1, max_length=50)
    estado: str | None = None


class Ruta(RutaBase):
    id: int