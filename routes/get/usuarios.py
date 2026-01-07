from fastapi import APIRouter
from database import get_connection

router = APIRouter(tags=["usuarios"])

@router.get("/usuarios")
def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT email, username, nombre, apellido, rol, habilitado, reporte FROM Usuarios
    """
    cursor.execute(query)
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios
