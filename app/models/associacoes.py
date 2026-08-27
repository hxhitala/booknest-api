from sqlalchemy import Column, Integer, ForeignKey, Table
from app.database import Base

livro_autor = Table(
    "livro_autor",
    Base.metadata,
    Column("livro_id", Integer, ForeignKey("livros.id"), primary_key=True),
    Column("autor_id", Integer, ForeignKey("autores.id"), primary_key=True),
)

livro_categoria = Table(
    "livro_categoria",
    Base.metadata,
    Column("livro_id", Integer, ForeignKey("livros.id"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey("categorias.id"), primary_key=True),
)