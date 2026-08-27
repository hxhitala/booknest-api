from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.autor import Autor
from app.schemas.autor import AutorCreate, AutorResponse

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.post("/", response_model=AutorResponse, status_code=201)
def criar_autor(autor: AutorCreate, db: Session = Depends(get_db)):
    novo_autor = Autor(nome=autor.nome)
    db.add(novo_autor)
    db.commit()
    db.refresh(novo_autor)
    return novo_autor


@router.get("/", response_model=List[AutorResponse])
def listar_autores(db: Session = Depends(get_db)):
    return db.query(Autor).all()


@router.get("/{autor_id}", response_model=AutorResponse)
def obter_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(Autor).filter(Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado.")
    return autor