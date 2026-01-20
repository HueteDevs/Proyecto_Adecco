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
    
    from app.models import Pelicula, SalaORM, Horario, Genre, Venta, MetodoPago
    
    #crear todas las tablas
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    try:
        existing_peliculas = db.execute(select(Pelicula)).scalars().all()
        
        
        if existing_peliculas:
            return
        
        
        default_peliculas = [
            Pelicula(titulo="Regreso al Futuro", genero_id=2, duracion=103, disponible=False, imagen="https://pics.filmaffinity.com/back_to_the_future-100822308-large.jpg"),
            Pelicula(titulo="Frankenstein", genero_id=4, duracion=122, disponible=True, imagen="https://m.media-amazon.com/images/M/MV5BYzYzNDYxMTQtMTU4OS00MTdlLThhMTQtZjI4NGJmMTZmNmRiXkEyXkFqcGc@._V1_.jpg"),
            Pelicula(titulo="Dragon ball Super: Broly", genero_id=5, duracion=102, disponible=True, imagen ="https://pics.filmaffinity.com/doragon_boru_cho_burori-949664812-large.jpg"),
            Pelicula(titulo="Atrapalo como Puedas", genero_id=2, duracion=98, disponible=True, imagen = "https://es.web.img2.acsta.net/img/56/dd/56dd4ecedfc32ef070bb4cc723ff01c1.jpg")
            
        ]
        db.add_all(default_peliculas)
        db.commit() 
    
        
    
    
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
            Genre(id=1, name_genre="Acción"),
            Genre(id=2, name_genre="Comedia"),
            Genre(id=3, name_genre="Drama"),
            Genre(id=4, name_genre="Terror"),
            Genre(id=5, name_genre="Anime"),
            Genre(id=6, name_genre="Animación"),
            Genre(id=7, name_genre="Comedia Negra")
]
        
        
    
        db.add_all(default_genres)
        db.commit()
        
        
        default_ventas = [
            Venta(horario_id=1, precio_total=20.60,cantidad=2, metodo_pago=MetodoPago.EFECTIVO),
            Venta(horario_id=2, precio_total=30.60,cantidad=5, metodo_pago=MetodoPago.TARJETA),
            Venta(horario_id=3, precio_total=40.60,cantidad=4, metodo_pago=MetodoPago.EFECTIVO)           
        ]
        
        db.add_all(default_ventas)
        db.commit()
    finally:
         db.close()



