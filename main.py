from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas

def crear_database():
    return models.Base.metadata.create_all(bind=engine)

crear_database()

app = FastAPI(title="API-IOL")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    """ Endpoint para dar la bienvenida
    """
    
    return {"Bienvenidos a la API"}

@app.post("/consultas/", response_model=schemas.Consulta, tags=['Nueva alta en tabla Consultas'])
def crear_consulta(consulta: schemas.Consulta, db: Session = Depends(get_db)):
    """Este enpoint permite agregar un nuevo registro a la tabla Consultas
    
    """
    db_proveedor = crud.consulta_precio(db=db)
    
    return db_proveedor