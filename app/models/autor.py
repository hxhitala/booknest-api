from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associacoes import livro_autor


class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)

    livros = relationship("Livro", secondary=livro_autor, back_populates="autores")