from typing import Union
from pydantic import BaseModel, Field

class Consulta(BaseModel):
    IDConsulta: int = Field(default=None, primary_key=True)
    Stock : str
    Last : float
    Fecha_consulta : str
    Bid : float
    Ask : float
    class Config:
        orm_mode = True
    pass

class TradesShort(BaseModel):
    idtrade : int
    stock : str
    tipo : str
    precio : float
    takeprofit : float
    stoploss : float
    cantidad : int
    costo : float
    operado : bool
    fecha_trade : str
    class Config:
        orm_mode = True
    pass

class TradesLong(BaseModel):
    idtrade : int
    stock : str
    tipo : str
    precio : float
    takeprofit : float
    stoploss : float
    cantidad : int
    costo : float
    operado : bool
    fecha_trade : str
    class Config:
        orm_mode = True
    pass
    
class Operacion(BaseModel):
    estado: str = 'todas'
    desde: str
    hasta: str
    pais: str = 'argentina'

class ConsultaMep(BaseModel):
    simbolo:str = None

class Orden(BaseModel):
    mercado: str = "bCBA" #Las opciones son bCBA o estados_Unidos
    simbolo: str
    cantidad: int
    precio: Union[float, int]
    plazo: str #t0, t1, t2
    validez: str #Ejemplo: 2023-05-31