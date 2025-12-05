from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import SalaORM


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/salas", tags=["web"])

# listar salas (http://localhost:8000/salas)
@router.get("", response_class=HTMLResponse)
def list_salas(request: Request, db: Session = Depends(get_db)):
    salas = db.execute(select(SalaORM)).scalars().all()
    
    return templates.TemplateResponse(
        "salas/list.html",
        {"request": request, "salas": salas}
    )
    
# detalle de sala (http://localhost:8000/salas/3)
@router.get("/{sala_id}", response_class=HTMLResponse)
def salas_detail(request: Request, sala_id: int, db: Session = Depends(get_db)):
    sala= db.execute(select(SalaORM).where(SalaORM.id == sala_id)).scalar_one_or_none()
    
    if sala is None:
        raise HTTPException(status_code=404, detail="404 - Sala no encontrada")
    
    return templates.TemplateResponse(
        "salas/detail.html",
        {"request": request, "sala": sala}
    )