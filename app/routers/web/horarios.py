from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.horario import Horario

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/horarios", tags=["web"])

@router.get("", response_class=HTMLResponse)
def list_artists(request: Request, db: Session = Depends(get_db)):
    horarios = db.execute(select(Horario)).scalars().all()

    return templates.TemplateResponse(
        "horarios/list.html",
        {"request": request, "horarios": horarios}
    )
