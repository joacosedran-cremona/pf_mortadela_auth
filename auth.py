from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import TypedDict, Optional

SECRET_KEY = "CAMBIA_ESTE_SECRET_POR_EL_REAL"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class TokenUser(TypedDict):
    username: str
    rol: Optional[str]

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenUser:
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    username = payload.get("sub")
    if not username:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido"
      )

    return {
        "username": username,
        "rol": payload.get("rol"),
    }

  except JWTError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token inválido"
    )
