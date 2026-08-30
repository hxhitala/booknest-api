from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.emprestimo import EmprestimoCreate, EmprestimoResponse, DevolucaoRequest
from app.models.emprestimo import Emprestimo
from app.services import emprestimo_service

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.post("/", response_model=EmprestimoResponse, status_code=201)
def criar_emprestimo(
    dados: EmprestimoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return emprestimo_service.criar_emprestimo(
        db=db, usuario_id=usuario_atual.id, exemplar_id=dados.exemplar_id
    )


@router.post("/devolucao", response_model=EmprestimoResponse)
def devolver_emprestimo(
    dados: DevolucaoRequest,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return emprestimo_service.devolver_emprestimo(db=db, exemplar_id=dados.exemplar_id)


@router.get("/", response_model=List[EmprestimoResponse])
def listar_emprestimos(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return db.query(Emprestimo).all()


@router.get("/usuario/{usuario_id}", response_model=List[EmprestimoResponse])
def listar_emprestimos_do_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return db.query(Emprestimo).filter(Emprestimo.usuario_id == usuario_id).all()