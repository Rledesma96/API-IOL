from sqlalchemy.orm import Session
import models
import schemas
import funcionesIOL
import json

def consulta_precio(db:Session):
    try:
        datos = funcionesIOL.cotizacion("COME", simple=True)
    except ValueError as error:
        raise ValueError ("El usuario o contraseña no son válidos") from error
    
    consulta = schemas.Consulta(Stock="COME",\
                                Last = float(json.loads(datos)['ultimoPrecio']),\
                                Fecha_consulta = str(json.loads(datos)['date']),\
                                Bid = float((json.loads(datos)['Bid'])),\
                                Ask = float(json.loads(datos)['Ask']),\
                                )

    dbconsulta = models.Consultas(**consulta.dict())
    db.add(dbconsulta)
    db.commit()
    db.refresh(dbconsulta)
    return consulta

    

