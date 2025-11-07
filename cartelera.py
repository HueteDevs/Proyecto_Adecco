from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker
from sqlalchemy import String, Integer, Float, Boolean, create_engine, ForeignKey
app = FastAPI()

class Pelicula(BaseModel):
    titulo: str
    duracion: float
    genero: str
    en_cartelera: bool
    
class Sala(BaseModel):
    nombre: str
    capacidad: int
    tipo: str
    precio: float
    disponible: bool
    
class Horario(BaseModel):
    pelicula_id: int
    sala_id: int
    hora: str
    disponible: bool
    
class Venta(BaseModel):
    pelicula_id: int
    horario_id: int
    sala_id: int
    cantidad_boletos: int
    total: float
    metodo_pago: str
    
class Genero(BaseModel):
    pelicula_id: int
    nombre: str
    descripcion: str
    
DATABAS_URL = "sqlite:///./cartelera.db"

engine = create_engine(DATABAS_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class PeliculaORM(Base):
    __tablename__ = "peliculas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    duracion: Mapped[float] = mapped_column(Float, nullable=False)
    genero: Mapped[str] = mapped_column(String, nullable=False)     
    en_cartelera: Mapped[bool] = mapped_column(Boolean, nullable=False)

class SalaORM(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String, nullable=False)     
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False)

class HorarioORM(Base):
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("peliculas.id"), nullable=False)
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), nullable=False)
    hora: Mapped[str] = mapped_column(String, nullable=False)     
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
class VentaORM(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("peliculas.id"), nullable=False)
    horario_id: Mapped[int] = mapped_column(ForeignKey("horarios.id"), nullable=False)
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), nullable=False)
    cantidad_boletos: Mapped[int] = mapped_column(Integer, nullable=False)     
    total: Mapped[float] = mapped_column(Float, nullable=False)
    metodo_pago: Mapped[str] = mapped_column(String, nullable=False)    
    
class GeneroORM(Base):
    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("peliculas.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[str] = mapped_column(String, nullable=False)    

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    peliculas_existentes = db.query(PeliculaORM).first()
    if not peliculas_existentes:
        peliculas = [
            PeliculaORM(titulo="Pelicula A", duracion=120.0, genero="Accion", en_cartelera=True),
            PeliculaORM(titulo="Pelicula B", duracion=90.0, genero="Comedia", en_cartelera=True),
            PeliculaORM(titulo="Pelicula C", duracion=110.0, genero="Drama", en_cartelera=False)
        ]
        db.add_all(peliculas)
        db.commit() 
    salas_existentes = db.query(SalaORM).first()
    if not salas_existentes:
        salas = [
            SalaORM(nombre="Sala 1", capacidad=100, tipo="2D", precio=8.5, disponible=True),
            SalaORM(nombre="Sala 2", capacidad=80, tipo="3D", precio=10.0, disponible=True),
            SalaORM(nombre="Sala 3", capacidad=50, tipo="IMAX", precio=15.0, disponible=False)
        ]
        db.add_all(salas)
        db.commit()
    horarios_existentes = db.query(HorarioORM).first()
    if not horarios_existentes: 
        horarios = [
            HorarioORM(pelicula_id=1, sala_id=1, hora="14:00", disponible=True),
            HorarioORM(pelicula_id=2, sala_id=2, hora="16:00", disponible=True),
            HorarioORM(pelicula_id=3, sala_id=3, hora="18:00", disponible=False)
        ]
        db.add_all(horarios)
        db.commit() 
    ventas_existentes = db.query(VentaORM).first()
    if not ventas_existentes: 
        ventas = [
            VentaORM(pelicula_id=1, horario_id=1, sala_id=1, cantidad_boletos=2, total=17.0, metodo_pago="Tarjeta"),
            VentaORM(pelicula_id=2, horario_id=2, sala_id=2, cantidad_boletos=3, total=30.0, metodo_pago="Efectivo")
        ]
        db.add_all(ventas)
        db.commit()
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



