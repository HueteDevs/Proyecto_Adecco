## DOCUMENTACIÓN MÓDULO DE VENTAS - API REST

## 1. DESCRIPCIÓN GENERAL
Este módulo implementa un servicio API REST para vestionar las ventas dentro del proyecto de cartelera de cine.

Permite:
1. Registrar nuevas ventas
2. Consultar ventas existentes
3. Actualizar ventas (Completas y parciales)
4. Eliminar ventas

Se ha usado:
* FastAPI para la API REST
* SQLAlchemy 2.0 como ORM
* SQLite como bsae de datos local
* Pydantic v2 para la validación y la serialización

El cálculo del campo **precio_total** se realiza siempre en el servidor, garantizando la integridad de la venta.


--------------------------------------------------------------------------------

## 2. CONFIGURACIÓN DE LA BASE DE DATOS

La conexión se realiza mediante **SQLAlchemy**:

```bash
engine=create_engine(
    'sqlite://ventas.db',
    echo=True,
    connect_args={"check_same_thread":False}
)

```
Las sesiones se gestionan con:
```bash
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)
```
Utilizamos un método de dependencias para abrir y cerrar sesiones dentro de los endpoints:

```bash
def get_db()
db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
--------------------------------------------------------------------------------

## 3. MODELO SQLALCHEMY

La entidad principal es **Venta**, que representa una venta realizada para un horario concreto.

```bash
class Venta(Base):
    __tablename__="ventas"

    id=mapped_column(Integer,primary_key=True,autoincrement=True)
    horario_id=mapped_column(Integer,nullable=False)
    precio_total=mapped_column(FLoat,nullable=False)
    cantidad=mapped_column(Integer,nullable=False)
    metodo_pago=mapped_column(SQLEnum(MetodoPago,name="metodo_pago_enum"),nullable=False)
    MetodoPago(Enum)
    #Define los valores permitidos para el método de pago:
    class MetodoPago(str,Enum):
    EFECTIVO="efectivo"
    TARJETA="tarjeta"
```
--------------------------------------------------------------------------------

## 4. Esquemas Pydantic (DTOs)

Los modelos Pydantic se utilizan para validar datos entrantes y estructurar respuestas JSON.

## 4.1 VentasResponse (salidas de la API)

Incluye todos los campos, incluso **id** y **precio_total**:

```bash
class VentaResponse(BaseModel):
    model_config=ConfigDigit(from_attributes=True)
    
    id:int
    horario_id:int
    precio_total:float
    cantidad:int
    metodo_pago:MetodoPago
```
## 4.2 VentaCreate(POST)

No incluye **id** ni **precio_total**:

```bash
class VentaCreate(BaseModel):
    model_config=ConfigDigit(from_attributes=True)

    horario_id:int
    cantidad:int
    metodo_pago:MetodoPago
```
## 4.3 VentaUpdate(PUT)

Actualización total, todos los campos son **obligatorios**:

```bash
class VentaUpdate(BassModel):
    model_config=ConfigDigit(from_attributes=True)

    horario_id:int
    cantidad:int
    metodo_pago:MetodoPago
```
## 4.4 VentaPatch(patch)

Actualización parcial, todos los campos son **opcionales**:

```bash
class VentaPatch(BaseModel):
    model_config=ConfigDigit(from_attributes=True)

    horario_id: int | None
    cantidad: int | None
    metodo_pago: MetodoPago | None
```
## 5. Endpoints del CRUD

## 5.1 GET/api/ventas

Devuelve la lista completa de ventas.

```bash
@app.get("/api/ventas", response_model=list[VentaResponse])
```

## 5.2 GET/api/ventas/{id}

Devuelve una venta concreta a partir del id

```bash
@app.get("/api/ventas/{id}", response_model=VentaResponse)
```
Si no existe, genera **HTTP 404**.

## 5.3 POST/api/ventas

Crea una nueva venta.
El **precio_total** se calcula dentro del servidor:

```bash
# Se hace con un valor predefinido para pruebas a falta de poder generar la relación con horario.db
precio_total=8*venta_dto.cantidad
```
Valida:
* horario_id no vacío
* cantidad no vacía
* metodo_pago válido

Devuelve la venta creada con su **id**.

## 5.4 PUT/api/ventas

Actualiza completamente una venta.
Todos los campos son **obligatorios**.
El precio se recalcula:

```bash
venta.precio_total= 8 * venta.cantidad
```
Devuelve la venta actualizada

## 5.5 PATCH/api/ventas/{id}

Actualiza todos los campos enviados.

Uso de:

```bash
data=venta_dto.model_dump(exclude_unset=True)
```
Si cambia **horario_id** o **cantidad**, recalcula el precio:

```bash
if horario_id in data or cantidad in data:
    venta.precio_total=8 * venta.cantidad
```
## 5.6 DELETE/api/ventas/{id}

Elimina una venta a partir del **id**.
Si no existe -> **404**.
Retorna **204 NO CONTENT**.

## 6. Cálculo de precios

Actualmente el precio se calcula de forma **fija**:

```bash
precio_total = 8 * cantidad
```

## P.S: Se ha dejado preparado para integrarlo con el módulo horarios:

```bash
# TODO: precio_unitario = obtener_precio_de_horarios(horario_id)
# venta.precio_total = precio_unitario * venta.cantidad
```
