from typing import Optional

from fastapi import APIRouter, Depends

from app.auth import obter_usuario_atual
from app.database import catalogo

router = APIRouter(prefix="/api/catalogo", tags=["catalogo"])


@router.get("")
def buscar_catalogo(
    tipo: Optional[str] = None,
    genero: Optional[str] = None,
    busca: Optional[str] = None,
    pagina: int = 1,
    limite: int = 10,
    usuario=Depends(obter_usuario_atual),
):
    resultado = catalogo

    if tipo:
        resultado = [item for item in resultado if item["tipo"] == tipo]

    if genero:
        resultado = [item for item in resultado if item["genero"] == genero]

    if busca:
        termo = busca.lower()
        resultado = [item for item in resultado if termo in item["titulo"].lower()]

    total = len(resultado)
    inicio = (pagina - 1) * limite
    fim = inicio + limite
    pagina_atual = resultado[inicio:fim]

    return {
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "resultados": pagina_atual,
    }
