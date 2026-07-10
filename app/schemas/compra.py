from pydantic import BaseModel, Field


class CompraConfirmar(BaseModel):
    cliente_id: int = Field(..., gt=0)
    metodo_pago: str = Field(..., min_length=3, max_length=50)
    observacion: str | None = Field(default="")