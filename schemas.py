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
    

    

