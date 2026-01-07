from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.get.usuarios import router as usuarios_router
from routes.set.deshabilitar_usuario import router as deshabilitar_usuario_router
from routes.set.habilitar_usuario import router as habilitar_usuario_router
from routes.delete.eliminar_usuario import router as eliminar_usuario_router
from routes.create.crear_usuario import router as crear_usuario_router

app = FastAPI()

origins = [
    "http://localhost:3000",  # o la URL de tu frontend
    # "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # en dev: ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(usuarios_router)
app.include_router(deshabilitar_usuario_router)
app.include_router(habilitar_usuario_router)
app.include_router(eliminar_usuario_router)
app.include_router(crear_usuario_router)

@app.get("/")
def hola():
    return {"mensaje": "Hola, mundo!"}