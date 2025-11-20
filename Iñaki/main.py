from fastapi import FastAPI
from database import Base,engine
from routers.venta import router as venta_router

# crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="Cartelera de cine", 
    description="Proyecto con 5 entidades (Película, sala, horario, género y venta)",
    version="1.0.0")

Base.metadata.create_all(bind = engine)

app.include_router(venta_router)

@app.get("/")
def home():
    return {"mensaje": "API Cartelera de Cine funcionando"}
