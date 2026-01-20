from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.database import get_db
from app.models import Pelicula

# Configurar jinja2
templates = Jinja2Templates(directory = "app/templates")

# Crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    # Obtener las últimas 5 películas ordenadas por ID descendente
    peliculas = db.execute(
        select(Pelicula)
        .options(joinedload(Pelicula.genero))
        .order_by(Pelicula.id.desc())
        .limit(5)
    ).scalars().all()
    
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "peliculas": peliculas}
    )
