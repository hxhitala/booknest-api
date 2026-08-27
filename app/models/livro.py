from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associacoes import livro_autor, livro_categoria


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False, index=True)
    isbn = Column(String, unique=True, index=True, nullable=True)
    ano_publicacao = Column(Integer, nullable=True)
    editora = Column(String, nullable=True)

    autores = relationship("Autor", secondary=livro_autor, back_populates="livros")
    categorias = relationship("Categoria", secondary=livro_categoria, back_populates="livros")
    exemplares = relationship("Exemplar", back_populates="livro")
    reservas = relationship("Reserva", back_populates="livro")