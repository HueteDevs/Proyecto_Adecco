"""
Configuración de la base de datos
"""
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Configuración Base de datos para Ventas
# Motor de conexión a BBDD
engine  = create_engine('sqlite:///cartelera.db', 
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
    
    from app.models import SalaORM, Horario, Genre
    
    #crear todas las tablas
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    try:
        existing_horarios = db.execute(select(Horario)).scalars().all()
        
        
        if existing_horarios:
            return
    
        
    
    
        default_salas = [
            SalaORM(nombre="Sala1",capacidad=20,tipo="2d",precio=8.90),
            SalaORM(nombre="Sala2",capacidad=40,tipo="IMAX",precio=11.90),
            SalaORM(nombre="Sala3",capacidad=25,tipo="3D",precio=9.00),
            SalaORM(nombre="Sala4",capacidad=20,tipo="2d",precio=8.90),
        ]
        db.add_all(default_salas)
        db.commit() 
    
    
        default_horarios = [
         Horario(pelicula_id=1, sala_id=1, hora = "22:00", disponible=True ),
         Horario(pelicula_id=2, sala_id=2, hora = "16:00", disponible=False ),
         Horario(pelicula_id=3, sala_id=3, hora = "18:30", disponible=True ),
         Horario(pelicula_id=4, sala_id=4, hora = "19:50", disponible=False ),
        ]
        db.add_all(default_horarios)
        db.commit() 
    
    
    
        default_genres = [
            Genre(genre_id=1, name_genre="Acción"),
            Genre(genre_id=2, name_genre="Comedia"),
            Genre(genre_id=3, name_genre="Drama"),
            Genre(genre_id=4, name_genre="Terror"),
            Genre(genre_id=5, name_genre="Anime"),
            Genre(genre_id=6, name_genre="Animación"),
            Genre(genre_id=7, name_genre="Comedia Negra")
        
        ]
    
        db.add_all(default_genres)
        db.commit() 
    finally:
         db.close()



