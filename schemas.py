from enum import Enum
from typing import Union
from pydantic import BaseModel, Field


class Consulta(BaseModel):
    IDConsulta: int = Field(default=None, primary_key=True)
    Stock: str
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
class OperacionEstado (str, Enum):
    todas = "todas"
    pendientes = "pendientes"
    terminadas = "terminadas"
    canceladas = "canceladas"
class OperacionPais(str, Enum):
    argentina = "argentina"
    usa = "estados_Unidos"
class Operacion(BaseModel):
    estado: OperacionEstado = OperacionEstado.todas
    desde: str
    hasta: str
    pais: OperacionPais = OperacionPais.argentina
class ConsultaMep(BaseModel):
    simbolo:str = None
class OrdenMercado(str, Enum):
    bcba = "bCBA"
    usa = "estados_Unidos"
class OrdenPlazo(str, Enum):
    t0 = "t0"
    t1 = "t1"
    t2 = "t2"
class Orden(BaseModel):
    mercado: OrdenMercado = OrdenMercado.bcba #Las opciones son bCBA o estados_Unidos
    simbolo: str
    cantidad: int
    precio: Union[float, int]
    plazo: OrdenPlazo = OrdenPlazo.t2   
    validez: str #Ejemplo: 2023-05-31
class PortafolioPais(str, Enum):
    argentina = "argentina"
    usa = "estados_Unidos"