from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.exemplar import Exemplar
from app.models.livro import Livro
from app.schemas.exemplar import ExemplarCreate, ExemplarResponse

router = APIRouter(prefix="/exemplares", tags=["Exemplares"])


@router.post("/", response_model=ExemplarResponse, status_code=201)
def criar_exemplar(dados: ExemplarCreate, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == dados.livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    novo_exemplar = Exemplar(livro_id=dados.livro_id, status="disponivel")
    db.add(novo_exemplar)
    db.commit()
    db.refresh(novo_exemplar)
    return novo_exemplar


@router.get("/", response_model=List[ExemplarResponse])
def listar_exemplares(db: Session = Depends(get_db)):
    return db.query(Exemplar).all()