from sqlalchemy.orm import Session
import models
import schemas
import funcionesIOL
import json

def consulta_precio(stock:str, db:Session):
    datos = funcionesIOL.cotizacion(stock, simple=True)
    consulta = schemas.Consulta(Stock=stock,\
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

    


