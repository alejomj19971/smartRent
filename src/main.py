from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from src.database import engine,SessionLocal
import src.models
from src.models import Casas
from src.utils.scrapping import obtener_casas
from src.utils.filtrar import filtrar
from src.utils.agruparPorLugar import agrupar
from src.crud import guardar_casas
from src.chat_service import chat_with_agent

app=FastAPI()

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

src.models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]

@app.get("/casas")
async def read_all(db:db_dependency):
    return db.query(Casas).all()


@app.post("/actualizar")
async def actualizar_datos():
    df = obtener_casas()
    guardar_casas(df)
    return {"mensaje": "Datos guardados correctamente"}

@app.get("/casas/filtrar/")
async def filtrar_casas(precioMin:int =0,precioMax:int=200000000,db: db_dependency=True):
        casas=db.query(Casas).all()
        resultado=list(filter(lambda casa:filtrar(casa,precioMin,precioMax),casas))
        return resultado

@app.get("/casas/agrupar/")
async def agrupar_casas(db: db_dependency=True):
    casas=db.query(Casas).all()
    return agrupar(casas)

# Modelo para el request de chat
class ChatRequest(BaseModel):
    message: str

# Endpoint para el chat
@app.post("/chat")
async def chat(request: ChatRequest):
    """Endpoint para procesar mensajes del chat"""
    response = chat_with_agent(request.message)
    return {"response": response}

# Servir archivos estáticos del frontend
frontend_path = Path(__file__).parent.parent / "front"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Servir el archivo HTML del frontend
@app.get("/")
async def read_root():
    frontend_file = Path(__file__).parent.parent / "front" / "index.html"
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    return {"message": "Frontend no encontrado. Por favor, crea el archivo front/index.html"}