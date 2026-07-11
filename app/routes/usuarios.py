from fastapi import APIRouter, HTTPException, status

from app.schemas.usuario import Usuario, UsuarioCrear, UsuarioActualizar
from app.services.usuario_service import (
    listar_usuarios,
    obtener_usuario,
    crear_usuario,
    actualizar_usuario,
    cambiar_estado_usuario,
    buscar_usuario_por_username
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[Usuario])
def get_usuarios():
    return listar_usuarios()


@router.get("/{usuario_id}", response_model=Usuario)
def get_usuario(usuario_id: int):
    usuario = obtener_usuario(usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post("", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def post_usuario(usuario: UsuarioCrear):
    existente = buscar_usuario_por_username(usuario.username)

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese username"
        )

    return crear_usuario(usuario.model_dump())


@router.put("/{usuario_id}", response_model=Usuario)
def put_usuario(usuario_id: int, usuario: UsuarioActualizar):
    usuario_existente = obtener_usuario(usuario_id)

    if not usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    data_actualizada = usuario.model_dump(exclude_unset=True)

    if "username" in data_actualizada:
        otro_usuario = buscar_usuario_por_username(data_actualizada["username"])

        if otro_usuario and otro_usuario["id"] != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro usuario con ese username"
            )

    return actualizar_usuario(usuario_id, data_actualizada)


@router.patch("/{usuario_id}/estado")
def cambiar_estado(usuario_id: int):

    usuario = cambiar_estado_usuario(usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return {
        "mensaje": "Estado actualizado correctamente.",
        "usuario": usuario
    }