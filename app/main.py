from fastapi import FastAPI

from app.routes import assinatura, auth, catalogo, perfis, senha, sessoes

app = FastAPI(title="Streaming API Teste", version="1.0.0")

app.include_router(auth.router)
app.include_router(senha.router)
app.include_router(perfis.router)
app.include_router(catalogo.router)
app.include_router(sessoes.router)
app.include_router(assinatura.router)


@app.get("/")
def raiz():
    return {"mensagem": "API Streaming Teste está no ar"}
