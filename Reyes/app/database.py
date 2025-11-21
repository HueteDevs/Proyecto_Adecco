
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine


# Conexión a la base de datos
DATABASE_URL = "sqlite:///./proyectoReyes/sala.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
    )

# Crear las sesiones
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False      
    )

# Clase Base para modelos sqlalchemy
class Base(DeclarativeBase):
    pass    

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()