from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from database import engine,SessionLocal
import models
from models import Casas
from utils.scrapping import obtener_casas
from crud import guardar_casas
app=FastAPI()
models.Base.metadata.create_all(bind=engine)

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