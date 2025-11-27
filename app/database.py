from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

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

#Crear clase Base para los modelos SQLAlchemy
class Base(DeclarativeBase):
    pass

# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()

def init_db():
    """
    Inicializa la base de datos con nuestras entidades por defecto si está vacía.
    Sólo crea las cosas si no existen ya en la base de datos.
    """
    
    from app.models import Pelicula, Sala, Horario, Venta, Genero
    
    #crear todas las tablas
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    #try:
    #    existing_peliculas = 
    
    # if existing_peliculas:
    #        return
    
    #default_peliculas = [
        
    #]
    
    
    #default_salas = [
        
    #]
    
    
    
    #default_horarios = [
        
    #]
    
    
    
    #default_ventas = [
        
    #]
    
    #default_generos = [
        
    #]
    
    



