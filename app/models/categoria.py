from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associacoes import livro_categoria


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True, index=True)

    livros = relationship("Livro", secondary=livro_categoria, back_populates="categorias")