from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.livro import Livro
from app.models.autor import Autor
from app.models.categoria import Categoria
from app.schemas.livro import LivroCreate, LivroResponse

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("/", response_model=LivroResponse, status_code=201)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    autores = db.query(Autor).filter(Autor.id.in_(dados.autor_ids)).all()
    categorias = db.query(Categoria).filter(Categoria.id.in_(dados.categoria_ids)).all()

    novo_livro = Livro(
        titulo=dados.titulo,
        isbn=dados.isbn,
        ano_publicacao=dados.ano_publicacao,
        editora=dados.editora,
        autores=autores,
        categorias=categorias,
    )
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@router.get("/", response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(Livro).all()


@router.get("/{livro_id}", response_model=LivroResponse)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro