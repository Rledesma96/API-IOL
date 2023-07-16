from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address, get_ipaddr
from slowapi.errors import RateLimitExceeded
from enum import Enum
import crud
import json
import funcionesIOL
import models
import schemas

def crear_database():
    return models.Base.metadata.create_all(bind=engine)

crear_database()

limiter = Limiter(key_func=get_ipaddr, default_limits=['5minute'])
app = FastAPI(title="API-IOL")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
@limiter.exempt
def home(request: Request):
    """ Endpoint para dar la bienvenida
    """
    response_data = {"messagge":"Bienvenidos a la API",
                     }
    
    return response_data

@app.get("/DatosPerfil", summary="Consulta Datos del Perfil", description="Consulta los datos del perfil seleccionado", tags=['Consulta de datos del Perfil'])
@limiter.exempt
def datos_perfil(request: Request):
    """Solcitar datos del pefil de IOL
    """
    response_data = funcionesIOL.datos_perfil()

    return Response(content=response_data, media_type="application/json")

@app.post("/operaciones",tags=['Consulta Operaciones'])
@limiter.limit("20/minute")
def operaciones(item: schemas.Operacion, request: Request):
    """Solcitar datos del pefil de IOL
    """
    response_data = funcionesIOL.consulta_operaciones(item.estado, item.desde, item.hasta, item.pais)
    #response_data.headers["X-Cat-Dog"] = "alone in the world" Primero se debe instanciar la clase Response

    return Response(content=response_data, media_type="application/json")

@app.post("/mep", 
          tags=['Cotizacion Mep'],
          description="Obtiene los valores del MEP del ticker asignado en caso de existir")
@limiter.limit("20/minute")
def mep(simbolo:str, request:Request):
    response_data = funcionesIOL.mep(simbolo)
    if response_data is None:
        raise HTTPException(status_code=422, detail="Ticker Nulo")
    elif isinstance(response_data, dict) | isinstance(response_data, float) :
        return Response(content=json.dumps(response_data), media_type="application/json")
    else:
        raise HTTPException(status_code=400, detail="Ticker sin mep")


@app.post("/consultas/", response_model=schemas.Consulta, tags=['Nueva alta en tabla Consultas'])
@limiter.limit("1/minute")
def crear_consulta(request : Request, consulta: schemas.Consulta, db: Session = Depends(get_db)):
    """Este enpoint permite agregar un nuevo registro a la tabla Consultas
    
    """
    db_proveedor = crud.consulta_precio(stock = consulta.Stock, db=db)
    
    return db_proveedor