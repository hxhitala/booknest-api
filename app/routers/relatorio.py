from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import obter_usuario_atual
from app.models.usuario import Usuario
from app.services import relatorio_service

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/livros-mais-emprestados")
def livros_mais_emprestados(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return relatorio_service.livros_mais_emprestados(db)


@router.get("/usuarios-com-pendencias")
def usuarios_com_pendencias(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return relatorio_service.usuarios_com_pendencias(db)


@router.get("/emprestimos-em-atraso")
def emprestimos_em_atraso(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    return relatorio_service.emprestimos_em_atraso(db)