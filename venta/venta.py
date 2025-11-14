from fastapi import FastAPI, HTTPException,status,Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Float,Integer,create_engine, select
from sqlalchemy import Enum as SQLEnum 
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column,sessionmaker,Session
from enum import Enum

# Configuración Base de datos para Ventas
# Motor de conexión a BBDD
engine  = create_engine('sqlite:///venta.db', 
          echo=True, # echo True para mostrar SQL solo en desarrollo
          connect_args={"check_same_thread": False}  # Puedes utilizar la conexión desde varios hilos
          )
# Creamos la fábrica de sesiones de base de datos
SessionLocal = sessionmaker(bind= engine, # Esto conecta las sesiones al motor de la conexión
               autocommit= False, # Controla los cambios, es decir en este caso no se actualiza automáticamente
               autoflush= True, # Sincroniza los cambios realizados temporalmente para que las consultas posteriores vean los datos actualizados
               expire_on_commit= False  # Sirve para que podamos seguir accediendo a los objetos después del commit
               )
# MODELO BASE DE DATOS (sqlalchemy)

# clase método de pago para que el usuario escoja como quiere pagar mediante un Enum
class MetodoPago(str, Enum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"

#Crear clase Base para los modelos SQLAlchemy
class Base(DeclarativeBase):
    pass

#modelo de la tabla venta

class Venta(Base):
    __tablename__ = 'ventas'
    
    # Clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requierido, RELACION CON IDs de horario
    horario_id:Mapped[int] = mapped_column(Integer,nullable=False)
    # requierido, Precio total (haremos el cálculo con el precio base de las sales y la cantidad)
    precio_total: Mapped[float] = mapped_column(Float, nullable=False)
    # requerido.
    cantidad: Mapped[int]= mapped_column(Integer, nullable=False)
    # requerido
    metodo_pago: Mapped[MetodoPago] = mapped_column(SQLEnum(MetodoPago, name="metodo_pago_enum"),
    nullable=False)
    
 # Modelos Pydantic (schema.py)
 # modelos que validan los datos que llegan y salen de la API
 
 # Schema para TODAS las respuestas de la API
 # Usos:
 # GET, POST, PUT, PATCH
class VentaResponse(BaseModel):
    
# ConfigDict hace que Pydantic pueda crear los modelos a partir de instancias 
# de SQLAlchemy (valida objetos ORM)
    model_config = ConfigDict(from_attributes=True)
     
    id: int
    horario_id: int
    precio_total: float
    cantidad: int
    metodo_pago: MetodoPago
    
# Equema para CREAR una venta
# No se incluye id porque se genera automáticamente
class VentaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int #RELACION (preguntar a María)
    cantidad: int
    metodo_pago: MetodoPago

# Esquema para actualización completa (PUT)
# Todos los campos son obligarorios
class VentaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int #RELACION
    cantidad: int
    metodo_pago: MetodoPago

# Esquema actualualización parcial (PATCH)
# Todos los campos son opcionales.
class VentaPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    horario_id: int | None #RELACION
    cantidad: int | None
    metodo_pago: MetodoPago | None

# Inicializar base de datos

# Crear todas las tablas
Base.metadata.create_all(engine)

# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()
# APLICACIÓN FASTAPI

# crea la instancia de la aplicación FastAPI
app = FastAPI(title="ventas", version="1.0.0")

# endpoint raíz
@app.get("/")
def home():
    return {'mensaje': 'VENTAS'}

# ENDPOINTS CRUD

# GET - obtener TODAS las ventas
@app.get("/api/ventas", response_model=list[VentaResponse])
def find_all(db: Session = Depends(get_db)):
    # db.execute(): ejecuta la consulta
    # select(Venta): crea consulta SELECT * FROM venta
    # .scarlars(): extrae los objetos Venta
    # .all(): obtiene los resultados como lista
    return db.execute(select(Venta)).scalars().all()
# GET - obtener UNA venta por id
@app.get("/api/ventas/{id}", response_model=VentaResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    # busca la venta con el id de la ruta
    # .scalar_one_or_none(): devuelve el objeto o None si no existe
    venta = db.execute(
        select(Venta).where(Venta.id == id)
    ).scalar_one_or_none()
    
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la venta con id {id}"
        )
    return venta

# POST - crear una nueva venta
@app.post("/api/ventas", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def create(venta_dto: VentaCreate, db: Session = Depends(get_db)):
    # TODO: obtener precio_unitario a partir de horario_id
    precio_total = 8 * venta_dto.cantidad
    
    #Validaciones
    if not venta_dto.horario_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo id horario no puede estar vacío"
        )
    
    
    if not venta_dto.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo cantidad no puede estar vacío"
            )
    if not venta_dto.metodo_pago:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo método de pago no puede estar vacío"
            )
    
    # Crea objeto venta con datos validados
    venta= Venta(
        horario_id=venta_dto.horario_id,
        precio_total=precio_total,
        cantidad=venta_dto.cantidad,
        metodo_pago=venta_dto.metodo_pago
    )
# Agrega el objeto a la base de datos
    db.add(venta) # Agrega el objeto a la sesion
    db.commit() # confirma la creación en base de datos
    db.refresh(venta) # refresca el objeto para obtener el id generado
    return venta # devuelve la venta creada

# PUT -actualizar COMPLETAMENTE una venta
@app.put("/api/ventas/{id}", response_model=VentaResponse)
def update_full(id: int, venta_dto: VentaUpdate, db: Session = Depends(get_db)):
    
    # Busca la venta por id
    venta=db.execute(
        select(Venta).where(Venta.id==id)
    ).scalar_one_or_none()
    

    # Si no existe
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la venta con id {id}"
        )
    
    #Validaciones
    if not venta_dto.horario_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo id horario no puede estar vacío"
        )
        
    
    if not venta_dto.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo cantidad no puede estar vacío"
            )
    if not venta_dto.metodo_pago:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo método de pago no puede estar vacío"
            )
    
    
    # Crea objeto venta con datos validados
    
    venta.horario_id=venta_dto.horario_id
    venta.cantidad=venta_dto.cantidad
    venta.metodo_pago=venta_dto.metodo_pago
    
    # Recalcular precio_total porque PUT cambia todo
    # TODO: calcular precio REAL según base de datos de horarios
    venta.precio_total = 8 * venta.cantidad  
    db.commit() # confirma la creación en base de datos
    db.refresh(venta) # refresca el objeto para obtener el id generado
    return venta # devuelve la venta creada

# PATCH -actualizar parcialmente una venta
@app.patch("/api/ventas/{id}", response_model=VentaResponse)
def update_venta(id: int, venta_dto: VentaPatch, db: Session = Depends(get_db)):
    # Busca la venta por id
    venta=db.execute(
        select(Venta).where(Venta.id==id)
    ).scalar_one_or_none()

# Si no existe
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la venta con id {id}"
        )
# 2. Extraer solo los campos enviados en el PATCH
    data = venta_dto.model_dump(exclude_unset=True)

    # 3. Actualizar SOLO esos campos
    for attr, value in data.items():
        setattr(venta, attr, value)
        
    if "horario_id" in data or "cantidad" in data:
    # TODO: obtener precio_unitario real a partir de horario_id
        venta.precio_total = 8 * venta.cantidad    
     
    db.commit() # confirma la creación en base de datos
    db.refresh(venta) # refresca el objeto para obtener el id generado
    return venta # devuelve la venta creada

# DELETE -borrar una venta por id
@app.delete("/api/ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_venta(id: int, db: Session = Depends(get_db)):
    # busca la venta con el id de la ruta
    # .scalar_one_or_none(): devuelve el objeto o None si no existe
    venta = db.execute(
        select(Venta).where(Venta.id == id)
    ).scalar_one_or_none()
    
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la venta con id {id}"
        )
    db.delete(venta) # Borra la venta por id
    db.commit() # confirma que hemos borrado la venta
    return None # No devuelve nada porque está borrado  

