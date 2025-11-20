
  <p align="center">
  <img src="banner_adecco.png" alt="HueteDevs banner" width="750" />
  </p>
   
# 🎥 Cartelera de Cine en Python
La magia del cine… programada en Python 🐍🍿

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" />
  <img src="https://img.shields.io/badge/FastAPI-ASGI%20Framework-009688" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-orange" />
  <img src="https://img.shields.io/badge/SQLite-Database-lightgrey" />
  <img src="https://img.shields.io/badge/Status-En%20desarrollo-yellow" />
</p>

## Introducción al proyecto
Bienvenido al repositorio oficial de **Cartelera de Cine**, una aplicación desarrollada en **Python** cuyo objetivo es gestionar de forma eficiente la cartelera digital de un cine. Este proyecto forma parte del aprendizaje del curso **Python + Inteligencia Artificial**, combinando conceptos de programación estructurada, POO, bases de datos, APIs y arquitectura web moderna.

---

## 🎯 Finalidad del Proyecto
El propósito de este proyecto es diseñar un sistema backend capaz de:
- 📌 Mostrar información de **películas** disponibles en cartelera.
- 🕒 Gestionar **horarios** y **salas**.
- 🎫 Administrar **ventas de entradas** y **precios**.
- 🎭 Organizar **géneros** y **clasificaciones**.
- 👥 Gestionar **usuarios, autenticación** y **socios**.
- 📚 Aplicar **POO**, estructuras de datos y buenas prácticas de desarrollo.
- 🚀 Integrar tecnologías modernas como **FastAPI** y **SQLAlchemy**.

---

## 👥 Equipo de Desarrollo
El proyecto ha sido diseñado y desarrollado por el siguiente equipo:
- **Javier Cachón Garrido**
- **Kary Haro Pérez**
- **Manuel Jesús Marín García**
- **Reyes Delestal Barrios**
- **Iñaki Huete Montes**

---

## 🛠️ Tecnologías utilizadas
- Python 3
- SQLAlchemy (ORM)
- SQLite
- Programación Orientada a Objetos
- FastAPI
- Jinja2
- Bootstrap 4/5
- HTML5
- CSS3
- JavaScript
- SQL
- Visual Studio Code

---

## 🏛️ Arquitectura del sistema
El proyecto está basado en una arquitectura modular que separa claramente las **entidades de dominio**, la **lógica de negocio** y los **servicios** (endpoints, vistas, etc.).

A continuación se detallan todas las entidades con sus campos, sus responsabilidades dentro del sistema y las **relaciones entre ellas**, así como cómo se pueden modelar en la base de datos y, cuando procede, en el ORM.

---

## 📁 Estructura del proyecto
A continuación se detalla la estructura recomendada del proyecto Cartelera de Cine en Python:

```text
.
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── pelicula.py      # Entidad Pelicula
│   │   ├── genero.py        # Entidad Genero
│   │   ├── sala.py          # Entidad Sala
│   │   ├── horario.py       # Entidad Horario
│   │   ├── venta.py         # Entidad Venta
│   │   ├── socio.py         # Entidad Socio
│   │   └── login.py         # Entidad Login / Usuario
│   ├── routes/
│   │   ├── peliculas.py     # Rutas CRUD Peliculas
│   │   ├── generos.py       # Rutas CRUD Generos
│   │   ├── salas.py         # Rutas CRUD Salas
│   │   ├── horarios.py      # Rutas CRUD Horarios
│   │   ├── ventas.py        # Rutas CRUD Ventas
│   │   
│   ├── database/
│   │   ├── db.py            # Motor de conexión SQLAlchemy
│   │   ├── db.sql           # Schema y seed de la base de datos
│   │   └── cartelera_cine.db    # Base de datos SQLite
│   ├── templates/
│   │   ├── base.html        # Layout común
│   │   ├── peliculas/       # Vistas HTML de peliculas
│   │   ├── generos/         # Vistas HTML de generos
│   │   ├── salas/           # Vistas HTML de salas
│   │   ├── horarios/        # Vistas HTML de horarios
│   │   ├── ventas/          # Vistas HTML de ventas
│   │   
├── requirements.txt
├── README.html

🎬 Entidades del sistema
🎞️ Pelicula
Responsable: JAVIER CACHÓN Representa una película disponible (o no) en la cartelera.

Campos
id: int — PK (clave primaria)

titulo: string

genero_id: int — FK → generos.id

duracion: int

director: string

descripcion: string

trailer: string (URL)

productora: string

idioma: string

VOSE: boolean

actores: lista (strings)

disponible: boolean

Relaciones (modelo y ORM)
Pelicula ↔ Género

A nivel de base de datos:

La FK está en peliculas.genero_id apuntando a generos.id.

A nivel lógico/ORM:

Cada Pelicula está asociada a un único Genero (lado N:1).

Cada Genero puede exponer una colección de peliculas (lado 1:N).

Navegación típica en ORM:

Desde una película: pelicula.genero

Desde un género (si se implementa la colección): genero.peliculas

Pelicula ↔ Horario

A nivel de base de datos (modelo relacional):

La FK está en horarios.pelicula_id apuntando a peliculas.id.

Conceptualmente: una Pelicula puede tener muchos Horarios (1:N).

Navegación ORM implementada:

Se navega desde Horario hacia Pelicula mediante horario.pelicula.

No se implementa en el ORM la colección pelicula.horarios (no hay atributo en la entidad Pelicula).

Es decir, la relación es 1:N en la base de datos, pero la navegación en código se ha definido solo en el sentido Horario → Pelicula.

Servicios — Películas 🎬
Añadir película

Ver películas disponibles

Ver detalle de una película

Editar película

Eliminar o desactivar película

Extra (futuro)
Filtrar por género, duración, clasificación, etc.

Búsquedas avanzadas (título, director, actor, etc.)

Exportar catálogo a CSV/JSON

🏟️ Sala
Responsable: REYES Representa una sala física del cine.

Campos
id: int — PK

numero: int

capacidad: int (número de butacas)

tipo: enum (normal, 3D, IMAX, premium)

precio_base: float

Relaciones (modelo y ORM)
Sala ↔ Horario

A nivel de base de datos:

La FK está en horarios.sala_id apuntando a salas.id.

A nivel lógico/ORM:

Una Sala puede tener muchos Horarios (1:N).

Un Horario se proyecta en una sola Sala (N:1).

Dependiendo de la configuración del ORM se puede navegar:

Desde el horario: horario.sala

Desde la sala (si se define colección): sala.horarios

Servicios — Salas 🏟️
Añadir sala

Listar salas

Editar sala (capacidad, tipo, precio_base)

Activar/desactivar sala (si se implementa este campo)

Extra (futuro)
Gestión de mantenimiento (salas fuera de servicio)

Suplementos por tipo de sala (3D, IMAX, etc.)

🕒 Horario
Responsable: MANUEL Representa una sesión concreta de una película en una sala y hora determinada.

Campos
id: int — PK

pelicula_id: int — FK → peliculas.id

sala_id: int — FK → salas.id

hora: datetime/string

disponible: boolean

Relaciones (modelo y ORM)
Horario ↔ Pelicula

Modelo relacional:

Cada Horario referencia una única Pelicula mediante pelicula_id.

Una Pelicula puede tener muchos Horarios asociados (1:N, a nivel de tabla).

Navegación ORM implementada:

Desde Horario hacia Pelicula: horario.pelicula.

No se ha definido en el ORM la colección inversa pelicula.horarios; la navegación se mantiene intencionadamente unidireccional.

Horario ↔ Sala

Cada Horario referencia una única Sala mediante sala_id.

Una Sala puede tener múltiples Horarios (1:N, a nivel de modelo lógico).

Horario ↔ Venta

A nivel de base de datos:

La FK está en ventas.horario_id apuntando a horarios.id.

A nivel lógico/ORM:

Un Horario puede tener muchas Ventas (1:N).

Cada Venta corresponde a un único Horario (N:1).

Servicios — Horarios
Crear horario para una película en una sala

Listar horarios por película

Listar horarios por fecha

Listar horarios por sala

Editar horario (cambiar hora, sala, película)

Cancelar horario (marcar como no disponible)

Extra (futuro)
Comprobar solapamientos de horarios en la misma sala

Mostrar solo sesiones futuras

Control de aforo basado en ventas

💳 Venta
Responsable: IÑAKI Representa la compra de entradas para un determinado horario.

Campos
id: int — PK

horario_id: int — FK → horarios.id

precio_total: float

cantidad: int (número de entradas)

metodo_pago: enum (efectivo, tarjeta, cripto…)

socio_id: int (opcional) — FK → socios.id

Relaciones (modelo y ORM)
Venta ↔ Horario

Cada Venta está asociada a un único Horario mediante horario_id.

Un Horario puede tener múltiples Ventas asociadas.

Venta ↔ Socio (opcional / futuro)

Cada Venta puede opcionalmente estar asociada a un Socio mediante socio_id.

Un Socio puede acumular muchas Ventas a su nombre.

Servicios — Ventas 💳
Registrar venta

Calcular precio total

Listar ventas (por día, película, horario…)

Consultar recaudación en un rango de fechas

Extra (futuro)
Cupones de descuento

Asignar venta a usuario o socio

Generar ticket (PDF / código QR)

🏷️ Género
Responsable: KARY Catálogo de géneros cinematográficos asociados a las películas.

Campos
id: int — PK

nombre: string

descripcion: string

Relaciones (modelo y ORM)
Género ↔ Pelicula

Cada Pelicula referencia un Genero mediante genero_id.

Cada Genero puede agrupar muchas Peliculas asociadas.

Servicios — Géneros 🏷️
Crear género

Listar géneros

Editar género

Eliminar género (según política de negocio)

Extra (futuro)
Permitir múltiples géneros por película (tabla intermedia)

Estadísticas por género (películas, ventas, horarios, etc.)


🔗 Modelo de datos y relaciones (Cardinalidad)
A continuación se resumen las relaciones entre las entidades, indicando claves foráneas, dirección, cardinalidad y, cuando aplica, cómo se navega en el ORM.

2.1. Pelicula ↔ Género
FK: peliculas.genero_id → generos.id

Cardinalidad (modelo lógico):

Una Pelicula pertenece a un único Genero.

Un Genero puede tener muchas Peliculas.

Tipo:

Pelicula → Genero: ManyToOne (N:1)

Genero → Pelicula: OneToMany (1:N)

Navegación ORM típica: pelicula.genero y, si se define, genero.peliculas

2.2. Horario ↔ Pelicula
FK: horarios.pelicula_id → peliculas.id

Cardinalidad (modelo lógico):

Un Horario corresponde a una Pelicula concreta.

Una Pelicula puede tener muchos Horarios (1:N).

Tipo:

Horario → Pelicula: ManyToOne (N:1)

Pelicula → Horario: OneToMany (1:N) (a nivel de diseño de datos)

Navegación ORM implementada: solo horario.pelicula (no se implementa pelicula.horarios en el modelo actual).

2.3. Horario ↔ Sala
FK: horarios.sala_id → salas.id

Cardinalidad:

Un Horario se proyecta en una sola Sala.

Una Sala puede tener muchos Horarios.

Tipo:

Horario → Sala: ManyToOne (N:1)

Sala → Horario: OneToMany (1:N)

2.4. Venta ↔ Horario
FK: ventas.horario_id → horarios.id

Cardinalidad:

Una Venta está asociada a un solo Horario.

Un Horario puede tener muchas Ventas.

Tipo:

Venta → Horario: ManyToOne (N:1)

Horario → Venta: OneToMany (1:N)


📦 Instalación de dependencias
Antes de ejecutar el proyecto se recomienda utilizar un entorno virtual de Python y cargar todas las dependencias desde requirements.txt.

1. Clonar el repositorio
bash
git clone https://github.com/HueteDevs/Proyecto_Adecco
cd Proyecto_Adecco
2. Crear y activar entorno virtual (opcional, pero recomendado)
bash
# Linux y MacOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
3. Instalar dependencias del proyecto
Con el entorno virtual activado:

bash
pip install -r requirements.txt
Entre las dependencias típicas se incluyen paquetes como fastapi, uvicorn, sqlalchemy, pydantic, jinja2 y el driver de sqlite ya incorporado en la librería estándar de Python.

▶️ Ejecución paso a paso
Una vez instaladas las dependencias y creada la base de datos, la ejecución del proyecto se realiza normalmente a través de FastAPI y un servidor ASGI como Uvicorn.

1. Comprobar variables de entorno (opcional)
Si se utilizan variables de entorno (por ejemplo, para el modo debug o la URL de la base de datos), configúralas antes de lanzar la aplicación.

2. Ejecutar el servidor de desarrollo
bash
# Desde la raíz del proyecto
uvicorn app.main:app --reload
Por defecto, la API estará disponible en: http://127.0.0.1:8000 y la documentación interactiva en:

http://127.0.0.1:8000/docs (Swagger UI)

http://127.0.0.1:8000/redoc (ReDoc)

3. Ejecución desde run.py (alternativa)
bash
python run.py
Este script puede actuar como punto de entrada unificado para entornos de desarrollo o despliegue.

🗄️ Scripts de inicialización de la base de datos
La base de datos principal del proyecto es un fichero SQLite llamado cartelera_cine.db, ubicado en app/database/.

1. Módulos de base de datos
app/database/db.py — configuración de la conexión SQLAlchemy.

app/database/db.sql — creación de tablas y carga inicial de datos (seed).

2. Crear o recrear la base de datos
Desde la raíz del proyecto:

bash
python -m app.cartelera_cine.db
Este script se encarga de:

Crear el fichero cartelera_cine.db si no existe.

Generar las tablas correspondientes a las entidades: peliculas, generos, salas, horarios, ventas, logins y socios.

Cargar datos de ejemplo (películas, horarios, etc.) para pruebas.

3. Regenerar la base de datos (entornos de desarrollo)
En desarrollo es habitual borrar el fichero cartelera_cine.db y volver a ejecutar python -m app.cartelera_cine.db para partir de un estado limpio.

🌐 Definición de endpoints con FastAPI
La API se estructura en módulos de rutas dentro del paquete app/routes/, separando por dominio funcional (películas, géneros, salas, horarios, ventas, socios y login).

1. Punto de entrada de la API: app/main.py
python
from fastapi import FastAPI
from app.routes import peliculas, generos, salas, horarios, ventas, socios, login

app = FastAPI(title="Cartelera de Cine en Python")

app.include_router(peliculas.router, prefix="/peliculas", tags=["Películas"])
app.include_router(generos.router,   prefix="/generos",   tags=["Géneros"])
app.include_router(salas.router,     prefix="/salas",     tags=["Salas"])
app.include_router(horarios.router,  prefix="/horarios",  tags=["Horarios"])
app.include_router(ventas.router,    prefix="/ventas",    tags=["Ventas"])
2. Ejemplo de endpoints: app/routes/peliculas.py
python
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.pelicula import PeliculaCreate, PeliculaRead
from app.services.peliculas import PeliculaService

router = APIRouter()

@router.get("/", response_model=List[PeliculaRead])
def listar_peliculas():
    return PeliculaService.listar()

@router.get("/{pelicula_id}", response_model=PeliculaRead)
def obtener_pelicula(pelicula_id: int):
    pelicula = PeliculaService.obtener(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula

@router.post("/", response_model=PeliculaRead, status_code=201)
def crear_pelicula(datos: PeliculaCreate):
    return PeliculaService.crear(datos)

@router.delete("/{pelicula_id}", status_code=204)
def eliminar_pelicula(pelicula_id: int):
    PeliculaService.eliminar(pelicula_id)
3. Endpoints habituales por módulo
/peliculas: CRUD de películas y filtros por género, disponibilidad, etc.

/generos: mantenimiento del catálogo de géneros.

/salas: gestión de salas y capacidades.

/horarios: gestión de sesiones (película + sala + hora).

/ventas: registro de ventas y consultas de recaudación.

Esta organización facilita el mantenimiento, la escalabilidad del proyecto y la integración posterior con un frontend (por ejemplo, una SPA o plantillas Jinja2).

🚀 Futuras mejoras del proyecto
Sistema completo de compra de entradas (frontend + backend).

Diseño gráfico tipo cine (UI/UX más cinematográfica).

Panel de administración web (gestión de contenidos y usuarios).

Estadísticas avanzadas (ventas, ocupación, popularidad de películas).

Machine Learning para recomendaciones personalizadas de películas.

📦 Próximas actualizaciones
Se incorporará documentación detallada y ejemplos adicionales sobre:

Estructura de carpetas del proyecto.

Instalación de dependencias en distintos entornos.

Ejecución paso a paso con distintos perfiles (desarrollo / producción).

Scripts de inicialización y migraciones de la base de datos.

Definición avanzada de endpoints y seguridad en FastAPI.

✨ Proyecto en constante evolución con licencia GPL3. Cada aportación suma. Este repositorio seguirá creciendo con nuevas funcionalidades, mejoras y buenas prácticas de programación.
