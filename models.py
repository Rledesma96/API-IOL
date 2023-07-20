from sqlalchemy import Boolean, Column, Integer, String, Float
from datetime import datetime 
from database import Base
from pydantic import BaseModel
class Consultas(Base):
    __tablename__ = "Consultas"

    IDConsulta = Column(Integer, primary_key=True, index=True)
    Stock = Column(String, index=True)
    Last = Column(Float, index=True)
    Fecha_consulta = Column(String, index=True)
    Bid = Column(Float, nullable=True, index=True)
    Ask = Column(Float, nullable=True, index=True)
class TradesShort(Base):
    __tablename__ = "TradesShort"

    IDTrade = Column(Integer, primary_key=True, index=True)
    Stock = Column(String, index=True)
    Tipo = Column(String, index=True)
    Precio = Column(Float, index=True)
    TakeProfit = Column(Float, index=True, nullable=True)
    StopLoss = Column(Float, index=True, nullable=True)
    Cantidad = Column(Integer, index=True)
    Costo = Column(Float, index=True)
    Operado = Column(Boolean, index=True)
    Fecha_Trade = Column(String, index=True)
class TradesLong(Base):
    __tablename__ = "TradesLong"

    IDTrade = Column(Integer, primary_key=True, index=True)
    Stock = Column(String, index=True)
    Tipo = Column(String, index=True)
    Precio = Column(Float, index=True)
    TakeProfit = Column(Float, index=True, nullable=True)
    StopLoss = Column(Float, index=True, nullable=True)
    Cantidad = Column(Integer, index=True)
    Costo = Column(Float, index=True)
    Operado = Column(Boolean, index=True)
    Fecha_Trade = Column(String, index=True)
class Long(Base):
    __tablename__ = "OperacionesLong"

    IDLong = Column(String, primary_key=True, index=True)
    Mercado = Column(String, index=True)
    Stock = Column(String, index=True)
    Cantidad = Column(Integer, index=True)
    Precio = Column(Float, index=True)
    Plazo = Column(String, index=True)
    Validez = Column(String, index=True)