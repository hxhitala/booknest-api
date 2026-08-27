from pydantic import BaseModel
from typing import Optional, List
from app.schemas.autor import AutorResponse
from app.schemas.categoria import CategoriaResponse


class LivroBase(BaseModel):
    titulo: str
    isbn: Optional[str] = None
    ano_publicacao: Optional[int] = None
    editora: Optional[str] = None


class LivroCreate(LivroBase):
    autor_ids: List[int] = []
    categoria_ids: List[int] = []


class LivroResponse(LivroBase):
    id: int
    autores: List[AutorResponse] = []
    categorias: List[CategoriaResponse] = []

    class Config:
        from_attributes = True