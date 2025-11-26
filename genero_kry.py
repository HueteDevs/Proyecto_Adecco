from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker
from sqlalchemy import String, Integer, Float, Boolean, create_engine, ForeignKey
from pylance import Optional

app = FastAPI()

class Genero(BaseModel):
    nombre: str
    descripcion: Optional[str]

DATABASE_URL = "sqlite:///./cartelera.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class GeneroORM(Base):
    __tablename__= "genero"
    
    Id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion:Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    generos_existentes = db.query(GeneroORM).first()
    if not generos_existentes:  
        generos = [
            GeneroORM(pelicula_id=1, nombre="Accion", descripcion="Peliculas llenas de emocion y aventura."),
            GeneroORM(pelicula_id=2, nombre="Comedia", descripcion="Peliculas para reir y disfrutar."),
            GeneroORM(pelicula_id=3, nombre="Drama", descripcion="Peliculas con historias profundas y emotivas.")
        ]
        db.add_all(generos)
        db.commit() 
finally:
    db.close()



   
