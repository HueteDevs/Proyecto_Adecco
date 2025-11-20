from fastapi import FastAPI, Depends, HTTPException, status 
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker, Session
from sqlalchemy import Integer, Float, Enum, create_engine, select

app = FastAPI()

# Conexión a la base de datos
DATABASE_URL = "sqlite:///./sala.db"

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

# Modelo Sala de la base de datos
class SalaORM(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(Enum("2D", "3D", "IMAX", "2d", "3d", "imax", name="tipo_enum"), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    
# Modelo Pydantic para la Sala (schema)
class SalaResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    nombre: str
    capacidad: int
    tipo: str
    precio: float
        
class SalaCreate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    nombre: str
    capacidad: int
    tipo: str
    precio: float

class SalaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    nombre: str | None = None
    capacidad: int | None = None
    tipo: str | None = None
    precio: float | None = None 
    
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)   

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
        
@app.get("/salas", response_model=list[SalaResponse])
def obtener_salas(db: Session = Depends(get_db)):
    salas = db.execute(select(SalaORM)).scalars().all()
    return salas

@app.get("/salas/{sala_id}", response_model=SalaResponse)
def obtener_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.execute(
        select(SalaORM).where(SalaORM.id == sala_id)
        ).scalar_one_or_none()
    if sala is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="Sala no encontrada")
    return sala 

@app.post("/salas", response_model=SalaResponse, status_code=status.HTTP_201_CREATED)
def crear_sala(sala: SalaCreate, db: Session = Depends(get_db)):
    if not sala.nombre:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de la sala es obligatorio")
    if sala.capacidad <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La capacidad debe ser un número positivo")
    if sala.tipo not in ["2D", "3D", "IMAX", "2d", "3d", "imax"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de sala inválido")
    if sala.precio < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El precio no puede ser negativo")  
    nueva_sala = SalaORM(
        nombre=sala.nombre,
        capacidad=sala.capacidad,
        tipo=sala.tipo,
        precio=sala.precio
    )
    db.add(nueva_sala)
    db.commit()
    db.refresh(nueva_sala)
    return nueva_sala

@app.patch("/salas/{sala_id}", response_model=SalaResponse)
def actualizar_sala(sala_id: int, sala: SalaUpdate, db: Session =  Depends(get_db)):
    sala_existente = db.execute(
        select(SalaORM).where(SalaORM.id == sala_id)
        ).scalar_one_or_none()
    if sala_existente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada")
    if sala.nombre is not None:
        sala_existente.nombre = sala.nombre
    if sala.capacidad is not None:
        if sala.capacidad <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La capacidad debe ser un número positivo")
        sala_existente.capacidad = sala.capacidad
    if sala.tipo is not None:
        if sala.tipo not in ["2D", "3D", "IMAX"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de sala inválido")
        sala_existente.tipo = sala.tipo
    if sala.precio is not None:
        if sala.precio < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El precio no puede ser negativo")
        sala_existente.precio = sala.precio
    db.commit()
    db.refresh(sala_existente)
    return sala_existente

@app.delete("/salas/{sala_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sala(sala_id: int, db: Session = Depends(get_db)):
    sala_existente = db.execute(
        select(SalaORM).where(SalaORM.id == sala_id)
        ).scalar_one_or_none()
    if sala_existente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada")
    db.delete(sala_existente)
    db.commit()
    return None
