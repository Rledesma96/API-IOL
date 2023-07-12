from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address, get_ipaddr
from slowapi.errors import RateLimitExceeded
import crud
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


@app.post("/consultas/", response_model=schemas.Consulta, tags=['Nueva alta en tabla Consultas'])
@limiter.limit("1/minute")
def crear_consulta(request : Request, consulta: schemas.Consulta, db: Session = Depends(get_db)):
    """Este enpoint permite agregar un nuevo registro a la tabla Consultas
    
    """
    db_proveedor = crud.consulta_precio(db=db)
    
    return db_proveedor