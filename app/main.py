from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import autor, categoria, emprestimo, usuario, livro, exemplar, reserva

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookNest API")

app.include_router(usuario.router)
app.include_router(autor.router)
app.include_router(categoria.router)
app.include_router(livro.router)
app.include_router(exemplar.router)
app.include_router(emprestimo.router)
app.include_router(reserva.router)


@app.get("/")
def raiz():
    return {"mensagem": "BookNest API rodando"}