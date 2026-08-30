from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.emprestimo import Emprestimo
from app.models.livro import Livro
from app.models.exemplar import Exemplar
from app.models.usuario import Usuario
from app.models.multa import Multa


def livros_mais_emprestados(db: Session, limite: int = 10):
    resultado = (
        db.query(
            Livro.id,
            Livro.titulo,
            func.count(Emprestimo.id).label("total_emprestimos"),
        )
        .join(Exemplar, Exemplar.livro_id == Livro.id)
        .join(Emprestimo, Emprestimo.exemplar_id == Exemplar.id)
        .group_by(Livro.id, Livro.titulo)
        .order_by(func.count(Emprestimo.id).desc())
        .limit(limite)
        .all()
    )
    return [
        {"livro_id": r.id, "titulo": r.titulo, "total_emprestimos": r.total_emprestimos}
        for r in resultado
    ]


def usuarios_com_pendencias(db: Session):
    resultado = (
        db.query(
            Usuario.id,
            Usuario.nome,
            Usuario.email,
            func.sum(Multa.valor).label("total_pendente"),
        )
        .join(Emprestimo, Emprestimo.usuario_id == Usuario.id)
        .join(Multa, Multa.emprestimo_id == Emprestimo.id)
        .filter(Multa.paga == False)
        .group_by(Usuario.id, Usuario.nome, Usuario.email)
        .all()
    )
    return [
        {
            "usuario_id": r.id,
            "nome": r.nome,
            "email": r.email,
            "total_pendente": float(r.total_pendente),
        }
        for r in resultado
    ]


def emprestimos_em_atraso(db: Session):
    hoje = date.today()
    resultado = (
        db.query(Emprestimo)
        .filter(Emprestimo.status == "ativo", Emprestimo.data_prevista < hoje)
        .all()
    )
    return [
        {
            "emprestimo_id": e.id,
            "usuario_id": e.usuario_id,
            "exemplar_id": e.exemplar_id,
            "data_prevista": e.data_prevista,
            "dias_atraso": (hoje - e.data_prevista).days,
        }
        for e in resultado
    ]