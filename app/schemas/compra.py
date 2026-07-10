from pydantic import BaseModel, Field


class CompraConfirmar(BaseModel):

    cliente_id: int = Field(..., gt=0)

    destinatario: str = Field(..., min_length=3, max_length=100)

    direccion: str = Field(..., min_length=5, max_length=200)

    metodo_pago: str = Field(..., min_length=3, max_length=50)

    observacion: str | None = Field(default="")