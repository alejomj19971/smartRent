from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from src.database import engine,SessionLocal
import src.models
from src.models import Casas
from src.utils.scrapping import obtener_casas
from src.utils.filtrar import filtrar
from src.utils.agruparPorLugar import agrupar
from src.crud import guardar_casas

app=FastAPI()
src.models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]

@app.get("/")
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