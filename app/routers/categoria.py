from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/", response_model=CategoriaResponse, status_code=201)
def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    nova_categoria = Categoria(nome=categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return categoria