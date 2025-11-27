# app/services/pelicula_service.py
# Lógica de negocio (CRUD) para el módulo de Películas

from sqlalchemy.orm import Session, joinedload
from app.models.pelicula import PeliculaORM
from app.models.genero import GeneroORM 
from app.schemas.pelicula import PeliculaCreate, PeliculaUpdate, PeliculaReadWithGenero, PeliculaImport
from typing import List, Optional, Dict, Any, Tuple 
from sqlalchemy import or_, func, cast, String

# --- Importaciones para Exportación (CSV/JSON) ---
import io
import csv
import json
from pydantic import ValidationError 


# ==============================================================================
# I. FUNCIONES DE EXPORTACIÓN 
# ==============================================================================

def _format_pelicula_for_csv_export(pelicula: PeliculaORM) -> Dict[str, Any]:
    """
    Formatea un objeto PeliculaORM a un diccionario aplanado para el exportación CSV.
    """
    data = {
        "id": pelicula.id,
        "titulo": pelicula.titulo,
        # Navegación eager-loaded
        "genero_nombre": pelicula.genero.nombre if pelicula.genero else "N/A",
        "duracion": pelicula.duracion,
        "disponible": "Sí" if pelicula.disponible else "No",
        
        # <-- INICIO FIX REGRESIÓN CSV -->
        "director": str(pelicula.director) if pelicula.director is not None else "",
        "descripcion": str(pelicula.descripcion) if pelicula.descripcion is not None else "",
        "trailer": str(pelicula.trailer) if pelicula.trailer is not None else "",
        "productora": str(pelicula.productora) if pelicula.productora is not None else "",
        "idioma": str(pelicula.idioma) if pelicula.idioma is not None else "",
        # <-- FIN FIX REGRESIÓN CSV -->
        
        "vose": "Sí" if pelicula.vose else "No",
        # Aplanar la lista de actores
        "actores": ", ".join(pelicula.actores) if pelicula.actores else "",
    }
    return data

def export_peliculas_to_csv(
    db: Session,
    query: Optional[str] = None,
    genero_id: Optional[int] = None,
    duracion_max: Optional[int] = None,
    disponible: Optional[bool] = None,
) -> io.StringIO:
    """
    Exporta el catálogo de películas filtradas a un formato CSV.
    Retorna un objeto StringIO (buffer en memoria) que contiene el CSV.
    """
    # 1. Obtener datos (la función get_peliculas_filtradas ya hace eager load del género)
    peliculas_orm = get_peliculas_filtradas(
        db=db,
        query=query,
        genero_id=genero_id,
        duracion_max=duracion_max,
        disponible=disponible,
    )
    
    # 2. Formatear datos y preparar cabeceras
    data = [_format_pelicula_for_csv_export(p) for p in peliculas_orm]
    
    # 3. Crear buffer y escribir CSV
    output = io.StringIO()
    # Definir el orden de las columnas del CSV
    fieldnames = [
        "id", "titulo", "genero_nombre", "duracion", "disponible", "director", 
        "productora", "idioma", "vose", "actores", "descripcion", "trailer"
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    
    writer.writeheader()
    writer.writerows(data)
    
    output.seek(0)
    return output

def export_peliculas_to_json(
    db: Session,
    query: Optional[str] = None,
    genero_id: Optional[int] = None,
    duracion_max: Optional[int] = None,
    disponible: Optional[bool] = None,
) -> str:
    """
    Exporta el catálogo de películas filtradas a un formato JSON.
    Retorna una cadena JSON serializada.
    """
    # 1. Obtener datos (se asegura el eager load del género)
    peliculas_orm = get_peliculas_filtradas(
        db=db,
        query=query,
        genero_id=genero_id,
        duracion_max=duracion_max,
        disponible=disponible,
    )
    
    # 2. Convertir los objetos ORM a schemas Pydantic (con el género anidado)
    # Nota de Seguridad: Usamos model_validate para la conversión de datos.
    peliculas_schema = [PeliculaReadWithGenero.model_validate(p) for p in peliculas_orm]
    
    # 3. Serializar la lista de objetos Pydantic a JSON
    return json.dumps([p.model_dump() for p in peliculas_schema], indent=4, ensure_ascii=False)

# ==============================================================================
# II. FUNCIONES DE IMPORTACIÓN 
# ==============================================================================

def _get_or_create_genero_id(db: Session, genero_nombre: str) -> Optional[int]:
    """
    Busca el ID de un género por su nombre. Si no existe, lo crea y retorna su ID.
    
    Nota: Se utiliza 'nombre' para la importación ya que es más legible que el 'id'.
    """
    genero_nombre = genero_nombre.strip()
    db_genero = db.query(GeneroORM).filter(
        func.lower(GeneroORM.nombre) == func.lower(genero_nombre)
    ).first()
    
    if db_genero:
        return db_genero.id
    
    # Si no existe, lo creamos para evitar fallos de FK
    print(f"INFO: Creando nuevo género '{genero_nombre}' durante la importación.")
    new_genero = GeneroORM(nombre=genero_nombre)
    db.add(new_genero)
    db.flush() # Forzar la inserción para obtener el ID
    return new_genero.id

def import_peliculas_from_data(
    db: Session, data: List[Dict[str, Any]]
) -> Tuple[int, List[Dict[str, Any]]]:
    """
    Procesa una lista de diccionarios (de JSON o CSV) e inserta/actualiza las películas.

    Retorna una tupla: (conteo de inserciones/actualizaciones exitosas, lista de errores).
    """
    success_count = 0
    errors: List[Dict[str, Any]] = []
    
    for row_index, row_data in enumerate(data):
        try:
            # 1. Validar y normalizar con el esquema Pydantic
            pelicula_data = PeliculaImport(**row_data)
            
            # 2. Obtener/Crear el ID del género
            genero_id = _get_or_create_genero_id(db, pelicula_data.genero_nombre)
            
            if not genero_id:
                 raise ValueError(f"No se pudo resolver el género: {pelicula_data.genero_nombre}")

            # 3. Construir el objeto PeliculaCreate para la inserción
            pelicula_create = PeliculaCreate(
                titulo=pelicula_data.titulo,
                duracion=pelicula_data.duracion,
                genero_id=genero_id,
                disponible=pelicula_data.disponible,
                director=pelicula_data.director,
                descripcion=pelicula_data.descripcion,
                trailer=pelicula_data.trailer,
                productora=pelicula_data.productora,
                idioma=pelicula_data.idioma,
                vose=pelicula_data.vose,
                actores=pelicula_data.actores,
            )
            
            # 4. Comprobar si existe (simplemente por título para simplificar)
            # En un sistema real, se usaría un ID externo o un slug para evitar duplicados.
            db_pelicula = db.query(PeliculaORM).filter(
                func.lower(PeliculaORM.titulo) == func.lower(pelicula_data.titulo)
            ).first()
            
            if db_pelicula:
                # Actualizar (Reutilizamos la lógica de update_pelicula)
                pelicula_update = PeliculaUpdate(**pelicula_create.model_dump())
                update_pelicula(db, db_pelicula.id, pelicula_update)
            else:
                # Insertar
                add_pelicula(db, pelicula_create)
            
            success_count += 1

        except ValidationError as e:
            errors.append({
                "row": row_index + 1, 
                "data": row_data, 
                "error": f"Error de Validación de Pydantic: {e.errors()}"
            })
            db.rollback() # Deshacer si hubo un flush previo
        except Exception as e:
            errors.append({
                "row": row_index + 1, 
                "data": row_data, 
                "error": f"Error de Base de Datos: {e}"
            })
            db.rollback()
            
    db.commit() # Commit final de todas las operaciones exitosas
    return success_count, errors


# ==============================================================================
# II. FUNCIONES CRUD/BÚSQUEDA 
# ==============================================================================

# --- Servicio 1: Añadir película ---
def add_pelicula(db: Session, pelicula: PeliculaCreate) -> PeliculaORM:
    """
    Añade una nueva película a la base de datos.
    """
    # Convertimos el schema Pydantic a un objeto ORM
    db_pelicula = PeliculaORM(**pelicula.model_dump())
    
    db.add(db_pelicula)
    db.commit()
    db.refresh(db_pelicula) # Refrescamos para obtener el ID asignado
    return db_pelicula

# --- Servicio 2: Ver películas disponibles ---
def get_peliculas_disponibles(db: Session) -> List[PeliculaORM]:
    """
    Devuelve una lista de todas las películas marcadas como 'disponible'.
    """
    return db.query(PeliculaORM).filter(PeliculaORM.disponible == True).all()

# --- Servicio 3 (Implícito): Ver todas las películas ---
def get_all_peliculas(db: Session) -> List[PeliculaORM]:
    """
    Devuelve todas las películas, disponibles o no.
    """
    return db.query(PeliculaORM).all()

# --- Servicio 4 (Implícito): Ver una película por ID ---
def get_pelicula_by_id(db: Session, pelicula_id: int) -> Optional[PeliculaORM]:
    """
    Busca una película por su ID.
    """
    return db.query(PeliculaORM).filter(PeliculaORM.id == pelicula_id).first()

# --- Servicio 5: Editar película ---
def update_pelicula(db: Session, pelicula_id: int, pelicula_update: PeliculaUpdate) -> Optional[PeliculaORM]:
    """
    Actualiza una película existente en la BBDD.
    """
    db_pelicula = get_pelicula_by_id(db, pelicula_id)
    
    if not db_pelicula:
        return None # Película no encontrada
        
    # Obtenemos los datos del update, excluyendo los que no se pasaron (None)
    update_data = pelicula_update.model_dump(exclude_unset=True)
    
    # Aplicamos las actualizaciones
    for key, value in update_data.items():
        setattr(db_pelicula, key, value)
        
    db.commit()
    db.refresh(db_pelicula)
    return db_pelicula

# --- Servicio 6: Eliminar película ---
def delete_pelicula(db: Session, pelicula_id: int) -> bool:
    """
    Elimina una película de la BBDD. Devuelve True si se eliminó.
    """
    db_pelicula = get_pelicula_by_id(db, pelicula_id)
    
    if db_pelicula:
        db.delete(db_pelicula)
        db.commit()
        return True
    return False

# ESTA FUNCIÓN ES UN SERVICIO PURO, SIN DECORADORES DE FASTAPI
def get_pelicula_detalle(db: Session, pelicula_id: int) -> Optional[PeliculaORM]:
    """
    Obtiene una película por ID y carga eagerly el género asociado.
    """
    return db.query(PeliculaORM).options(
        joinedload(PeliculaORM.genero)
    ).filter(PeliculaORM.id == pelicula_id).first()


# Función para aplicar los filtros dinámicos en buscador y genero
def get_peliculas_filtradas(
    db: Session,
    query: Optional[str] = None,
    genero_id: Optional[int] = None,
    duracion_max: Optional[int] = None,
    disponible: Optional[bool] = None,
) -> List[PeliculaORM]:
    """
    Obtiene películas aplicando de forma combinada.
    """
    # 1. Consulta base con eager loading del género
    query_stmt = db.query(PeliculaORM).options(
        joinedload(PeliculaORM.genero)
    )

    filtros = []

    # A) BÚSQUEDA GLOBAL (OR lógico)
    if query:
        term = f"%{query.lower()}%"

        filtros.append(
            or_(
                func.lower(PeliculaORM.titulo).like(term),
                func.lower(PeliculaORM.director).like(term),
                func.lower(PeliculaORM.descripcion).like(term),
                # Actores: la columna JSON se castea a texto y se busca ahí
                func.lower(cast(PeliculaORM.actores, String)).like(term),
            )
        )

    # B) FILTROS PARAMÉTRICOS (AND lógico)
    if genero_id is not None:
        filtros.append(PeliculaORM.genero_id == genero_id)

    if duracion_max is not None and duracion_max > 0:
        filtros.append(PeliculaORM.duracion <= duracion_max)

    # Si disponible es True, filtramos solo las disponibles; si es None/False, no filtramos
    if disponible:
        filtros.append(PeliculaORM.disponible == True)

    # 3) Aplicar filtros y ordenar
    return query_stmt.filter(*filtros).order_by(PeliculaORM.titulo).all()