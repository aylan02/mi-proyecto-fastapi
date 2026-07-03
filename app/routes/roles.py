from fastapi import APIRouter, HTTPException, status

from app.schemas.rol import Rol, RolCrear, RolActualizar
from app.services.rol_service import (
    listar_roles,
    obtener_rol,
    crear_rol,
    actualizar_rol,
    desactivar_rol,
    buscar_rol_por_nombre
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=list[Rol])
def get_roles():
    return listar_roles()


@router.get("/{rol_id}", response_model=Rol)
def get_rol(rol_id: int):
    rol = obtener_rol(rol_id)

    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    return rol


@router.post("", response_model=Rol, status_code=status.HTTP_201_CREATED)
def post_rol(rol: RolCrear):
    existente = buscar_rol_por_nombre(rol.nombre)

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con ese nombre"
        )

    return crear_rol(rol.model_dump())


@router.put("/{rol_id}", response_model=Rol)
def put_rol(rol_id: int, rol: RolActualizar):
    rol_existente = obtener_rol(rol_id)

    if not rol_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    data_actualizada = rol.model_dump(exclude_unset=True)

    if "nombre" in data_actualizada:
        otro_rol = buscar_rol_por_nombre(data_actualizada["nombre"])

        if otro_rol and otro_rol["id"] != rol_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro rol con ese nombre"
            )

    return actualizar_rol(rol_id, data_actualizada)


@router.delete("/{rol_id}")
def delete_rol(rol_id: int):
    rol = desactivar_rol(rol_id)

    if rol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    if rol == "INACTIVO":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol ya se encuentra desactivado"
        )

    return {"mensaje": "Rol desactivado correctamente"}