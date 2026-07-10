from pydantic import BaseModel, EmailStr, Field


class ClienteRegistro(BaseModel):

    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str
    correo: EmailStr
    username: str
    password: str = Field(..., min_length=8)
    confirmar_password: str = Field(..., min_length=8)

  