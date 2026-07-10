from pydantic import BaseModel

class EstadoSeguimiento(BaseModel):

    nombre: str
    descripcion: str
    completado: bool


class SeguimientoResponse(BaseModel):

    pedido_id: int
    cliente: str
    metodo: str
    fecha: str
    estado_actual: str
    estados: list[EstadoSeguimiento]