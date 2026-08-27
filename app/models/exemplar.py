from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Exemplar(Base):
    __tablename__ = "exemplares"

    id = Column(Integer, primary_key=True, index=True)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    status = Column(String, nullable=False, default="disponivel")
    # valores possíveis: "disponivel", "emprestado", "manutencao"

    livro = relationship("Livro", back_populates="exemplares")
    emprestimos = relationship("Emprestimo", back_populates="exemplar")