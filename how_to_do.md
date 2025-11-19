## CARTELERA DE CINE

### Pelicula (JAVIER CACHÓN)
- titulo: string
- genero_id: int **RELACION Pelicula a Genero ManyToOne**
- duracion: int
- director (opcional): string
- descripcion (opcional): string
- trailer (opcional): string
- productora (opcional): string
- idioma (opcional): string
- VOSE (opcional): boolean
- actores: lista
- disponible: boolean

Servicios — Películas 🎬
    • Añadir película
    • Ver películas disponibles
    • Eliminar/editar película
    
Extra (futuro si hay tiempo)
    • Ordenar por género / clasificación / duración
    • Guardar en archivo externo (JSON o CSV)
    
- base de datos SQLite
- Visual Studio Code

### Sala (REYES)
- numero: int
- capacidad: int (cantidad de butacas)
- tipo: string/enum tipo sala (normal, 3d, imax, premium)
- precio_base: float

### Horario (MANUEL)
- pelicula_id: int **RELACION**
- sala_id: int **RELACION**
- hora: datetime/string
- disponible: bool

### Venta (IÑAKI)
- horario_id: int **RELACION**
- precio_total: float
- cantidad: int
- metodo_pago: string/enum (efectivo, tarjeta, cripto)

### Genero(KARY) **RELACION Bidireccional Pelicula a Genero ManyToOne**
- nombre: string (historica, accion, romance, fantasia, drama...)
- descripcion (opcional): string
