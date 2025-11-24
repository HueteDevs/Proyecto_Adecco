from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, Boolean, select, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

#CONFIGURAR BASE DE DATOS

#crear motor de conexión a base de datos

engine = create_engine(
    "sqlite:///Modulo2/horario.db",
    echo=True,
    connect_args={"check_same_thread":False}
)

#Crear fabrica de sesiones de bases de datos

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

#modelo de base de datos (sqlalchemy)

#clase base para modelos sqlalchemy

class Base (DeclarativeBase):
    pass

#modelo de la tabla horario(se crea un solo modelo
# la cual sera una tabla en la base de datos)


class Horario(Base):
    __tablename__ = "horarios" #nombre de la tabla en bd
    #clave primaria
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pelicula_id: Mapped[int] = mapped_column(Integer,nullable=False)
    sala_id: Mapped[int] = mapped_column(Integer,nullable=False)
    hora: Mapped[str] = mapped_column(String, nullable=False)
    disponible:Mapped[bool] = mapped_column(Boolean, nullable=False)
    

#SCHEMAS (modelos pydantic)
    
#schema para TODAS las respuestas de la API
#lo usamos en GET, POST, PUT, PATCH


class HorarioResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic
    id: int
    pelicula_id: int
    sala_id: int
    hora: str
    disponible: bool


#Schema para crear un horario (POST)
#no incluimos id porque se genera automaticamente

class HorarioCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic
    
    pelicula_id: int
    sala_id:int
    hora: str
    disponible:bool

# schema para Actualizacion completa (PUT)
# todos los campos se tienen que enviar

class HorarioUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic

    pelicula_id: int
    sala_id:int
    hora: str
    disponible:bool

#schema para actualizacion parcial (PATCH)
#solo se envian los campos que quieres actualizar
class HorarioPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Traduce los atributos de SQLAlchemy para Pydantic
    
    pelicula_id: int | None = None
    sala_id:int | None = None
    hora: str | None = None
    disponible: bool | None = None


#inicializacion base de datos

#crear todas las tablas
Base.metadata.create_all(engine)

#metodo inicializar con horarios por defecto

def init_db():
    
    
    """
    Inicializa con canciones por defecto, las creara solo si
    no existen en la base de datos
    """

    db = SessionLocal()
    
    try:
        existing_horario = db.execute(select(Horario)).scalars().all()
        
        if existing_horario:
            return
        
        default_horarios = [
            Horario(pelicula_id=1,sala_id=1, hora = "16:00", disponible = True),
            Horario(pelicula_id=2,sala_id=1, hora = "19:00", disponible = False),
            Horario(pelicula_id=3,sala_id=2, hora = "16:00", disponible = True),
            Horario(pelicula_id=4,sala_id=2, hora = "19:00", disponible = False)
            
        ]
        
        #agregar los horarios
        db.add_all(default_horarios)
        db.commit()
    
    finally:
        db.close()

#inicializa la base de datos con horarios por defecto

init_db()


#dependencia de FastApi

def get_db():
    db = SessionLocal()
    try:
        yield db #entrega la sesion al endpoint
    finally:
        db.close()

#aplicacion fastapi

#crear la instancia de la aplicacion FastApi
app = FastAPI(title="Horarios", version="1.0.0")

#endpoint raiz
@app.get("/")
def home():
    return {"mensaje: Bienvenido a horarios"}


#ENDPOINTS CRUD

#GET-Obtener todas los horarios
@app.get("/api/horarios", response_model=list[HorarioResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Horario)).scalars().all()

#db.execute(): ejecuta la consulta
    #select(Song): crea consulta SELECT * FROM Song
    #.scarlars(): extrae los objetos Song
    #.all(): obtiene los resultados como lista


#GET - Obtener un horario por id

@app.get("/api/horarios/{id}",response_model=HorarioResponse)
def find_by_id(id:int, db: Session = Depends(get_db)):
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
        
    return horario


#POST - Crear un nuev horario
@app.post("/api/horarios", response_model=HorarioResponse, status_code=status.HTTP_201_CREATED)
def create(horario_dto: HorarioCreate, db: Session = Depends(get_db)):
    #Hacemos las validaciones necesarias
    if  horario_dto.pelicula_id is not None and horario_dto.pelicula_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pelicula_id no puede ser negativa"
        )
        
    if horario_dto.sala_id is not None and horario_dto.sala_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sala_id no puede ser negativa"
        )
    
    if not horario_dto.hora.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La hora no puede estar vacia"
        )

    #Crear el objeto horario
    horario = Horario(
        pelicula_id=horario_dto.pelicula_id,
        sala_id=horario_dto.sala_id,
        hora=horario_dto.hora.strip(),
        disponible=horario_dto.disponible
    )
    
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario

#PUT - actualizar completamente un horario
@app.put("/api/horarios/{id}", response_model=HorarioResponse)
def update_full(id: int, horario_dto: HorarioUpdate, db: Session = Depends(get_db)):
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    if  horario_dto.pelicula_id is not None and horario_dto.pelicula_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pelicula_id no puede ser negativa"
        )
        
    if horario_dto.sala_id is not None and horario_dto.sala_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sala_id no puede ser negativa"
        )
    
    if not horario_dto.hora.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La hora no puede estar vacia"
        )
    
    #Actualizar todos los campos
    horario.pelicula_id = horario_dto.pelicula_id
    horario.sala_id = horario_dto.sala_id
    horario.hora = horario_dto.hora.strip()
    horario.disponible = horario_dto.disponible
    
    db.commit()
    db.refresh(horario)
    return horario


@app.patch("/api/horarios/{id}", response_model=HorarioResponse)
def update_parcial(id:int, horario_dto: HorarioPatch, db: Session = Depends(get_db)):
    # buscar el horario por id
    
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    # si no existe, error 404
    
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
    
    #actualizar solo los campos enviados
    
    if horario_dto.pelicula_id is not None:
        if  horario_dto.pelicula_id < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tiene que haber una pelicula y con un numero valido"
            )
    
        horario.pelicula_id = horario_dto.pelicula_id
    
    if horario_dto.sala_id is not None:
        if horario_dto.sala_id < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tiene que haber una sala y con un numero valido"
            )
    
        horario.sala_id = horario_dto.sala_id
    
    if horario_dto.hora is not None:
        if not horario_dto.hora.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora no puede estar vacia"
            )
        horario.hora = horario_dto.hora.strip()
    
    if horario_dto.disponible is not None:
        horario.disponible = horario_dto.disponible
    
    db.commit()
    
    db.refresh(horario)
    return horario

#Delete - eliminar un horario por id

@app.delete("/api/horarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session= Depends(get_db)):
    #busca el horario por id
    horario = db.execute(
        select(Horario).where(Horario.id == id)
    ).scalar_one_or_none()
    
    #si no existe, error 404
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado un horario con la id {id}"
        )
    
    db.delete(horario)
    db.commit()
    return None