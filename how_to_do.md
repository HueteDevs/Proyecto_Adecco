## CARTELERA

### Pelicula
- titulo: string
- genero_id: int
- duracion: int
- director (opcional): string
- descripcion (opcional): string
- trailer (opcional): string
- productora (opcional): string
- idioma (opcional): string
- VOSE (opcional): boolean
- actores: list
- disponible: boolean

### Sala
- numero: int
- capacidad: int (cantidad de butacas)
- tipo: string/enum tipo sala (normal, 3d, imax, premium)
- precio_base: float

### Horario
- pelicula_id: int
- sala_id: int
- hora: datetime/string
- disponible: bool

### Venta
- horario_id: int
- precio_total: float
- cantidad: int
- metodo_pago: string/enum (efectivo, tarjeta, cripto)

### Genero
- nombre: string (historica, accion, romance, fantasia, drama...)
- descripcion (opcional): string