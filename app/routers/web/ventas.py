from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.venta import Venta


# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/ventas", tags=["web"])

#Listar ventas

@router.get("", response_class=HTMLResponse)
def list_artists(request: Request, db: Session = Depends(get_db)):
    ventas = db.execute(select(Venta)).scalars().all()

    return templates.TemplateResponse(
        "ventas/list.html",
        {"request": request, "ventas": ventas}
    )
