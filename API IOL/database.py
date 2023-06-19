from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

#Todo ORM requiere una conexion, una session y una base de la cual heredar para generar los modelos, este
#archivo lo que hace es crear esas cosas 

sql_database_url = "sqlite:///./API-IOL.db"

engine = create_engine(sql_database_url, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
Base = declarative_base() 