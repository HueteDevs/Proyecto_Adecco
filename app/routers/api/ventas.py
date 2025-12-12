from app.schemas.venta import VentaResponse, VentaCreate, VentaUpdate, VentaPatch
from fastapi import HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.venta import Venta
from app.database import get_db

router = APIRouter(
    prefix="/api/ventas",
    tags=["ventas"]
    )

# ENDPOINTS CRUD

# GET - obtener TODAS las ventas
@router.get("", response_model=list[VentaResponse])
def find_all(db: Session = Depends(get_db)):
    # db.execute(): ejecuta la consulta
    # select(Venta): crea consulta SELECT * FROM venta
    # .scarlars(): extrae los objetos Venta
    # .all(): obtiene los resultados como lista
    return db.execute(select(Venta).options(joinedload(Venta.horario))).scalars().unique().all()
# GET - obtener UNA venta por id
@router.get("/{id}", response_model=VentaResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    # busca la venta con el id de la ruta
    # .scalar_one_or_none(): devuelve el objeto o None si no existe
    venta = db.execute(
        select(Venta).where(Venta.id == id)
        .options(joinedload(Venta.horario))
    ).scalar_one_or_none()
    
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la venta con id {id}"
        )
    return venta

# POST - crear una nueva venta
@router.post("", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def create(venta_dto: VentaCreate, db: Session = Depends(get_db)):
    # TODO: obtener precio_unitario a partir de horario_id
    precio_total = 8 * venta_dto.cantidad
    
    # Crea objeto venta con datos validados
    venta= Venta(
        horario_id=venta_dto.horario_id,
        precio_total=precio_total,
        cantidad=venta_dto.cantidad,
        metodo_pago=venta_dto.metodo_pago
    )
    
    db.add(venta) # Agrega el objeto a la sesion
    db.commit() # confirma la creación en base de datos
    db.refresh(venta) # refresca el objeto para obtener el id generado
    
    venta_with_horario = db.execute(
        select(Venta)
        .where(Venta.id == venta.id)
        .options(joinedload(Venta.horario))
    ).scalar_one()
    
    return venta_with_horario

# PUT -actualizar COMPLETAMENTE una venta
@router.put("/{id}", response_model=VentaResponse)
def update_full(id: int, venta_dto: VentaUpdate, db: Session = Depends(get_db)):
    
    # Busca la venta por id
    venta=db.execute(
        select(Venta).where(Venta.id==id).options(joinedload(Venta.horario))
    ).scalar_one_or_none()
    

    # Si no existe
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la venta con id {id}"
        )
    
    # guarda el diccionario sacado de song_dto
    update_data = venta_dto.model_dump()
    
    # bucle para asignar el valor del diccionario a cada atributo
    for field, value in update_data.items():
        setattr(venta, field, value)
    # Crea objeto venta con datos validados
    # TODO: calcular precio REAL según base de datos de horarios
    venta.precio_total = 8 * venta.cantidad  
    db.commit() # confirma la creación en base de datos
    db.refresh(venta) # refresca el objeto para obtener el id generado
    return venta # devuelve la venta creada    

# PATCH -actualizar parcialmente una venta
@router.patch("/{id}", response_model=VentaResponse)
def update_venta(id: int, venta_dto: VentaPatch, db: Session = Depends(get_db)):
    # Busca la venta por id
    venta=db.execute(
        select(Venta).where(Venta.id==id)
        .options(joinedload(Venta.horario))
    ).scalar_one_or_none()

# Si no existe
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la venta con id {id}"
        )
# 2. Extraer solo los campos enviados en el PATCH
    update_data = venta_dto.model_dump(exclude_unset=True)

    # 3. Actualizar SOLO esos campos
    for attr, value in update_data.items():
        setattr(venta, attr, value)
        
    if "horario_id" in update_data or "cantidad" in update_data:
    # TODO: obtener precio_unitario real a partir de horario_id
        venta.precio_total = 8 * venta.cantidad    
     
    db.commit() # confirma la creación en base de datos
    db.refresh(venta) # refresca el objeto para obtener el id generado
    return venta # devuelve la venta creada

# DELETE -borrar una venta por id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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