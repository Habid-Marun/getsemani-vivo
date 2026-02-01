# database.py
# Configuracion de la base de datos - Getsemani Vivo

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# URL de la base de datos desde .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./getsemani.db")

# Crear el motor de base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Crear la sesion local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """Generador que proporciona una sesion de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()