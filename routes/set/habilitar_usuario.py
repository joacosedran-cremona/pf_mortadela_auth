from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import TypedDict, Optional
from database import get_connection

router = APIRouter(tags=["usuarios"])

class ApiResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class UsuarioRow(TypedDict):
    rol: str
    habilitado: int

class HabilitarUsuario(BaseModel):
  username: str

@router.post("/habilitar_usuario", response_model=ApiResponse)
def habilitar_usuario(data: HabilitarUsuario) -> ApiResponse:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verificar usuario
    cursor.execute(
        "SELECT rol, habilitado FROM Usuarios WHERE username = %s",
        (data.username,)
    )
    usuario: UsuarioRow = cursor.fetchone()  # type: ignore

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario["rol"] == "superadmin":
        raise HTTPException(
            status_code=403,
            detail="No se puede deshabilitar un superadmin"
        )

    if usuario["habilitado"] == 1:
        return ApiResponse(success=True, message="Usuario ya estaba habilitado")

    cursor.execute(
        "UPDATE Usuarios SET habilitado = 1 WHERE username = %s",
        (data.username,)
    )
  
    conn.commit()
    cursor.close()
    conn.close()

    return ApiResponse(success=True, message="Usuario habilitado exitosamente")
