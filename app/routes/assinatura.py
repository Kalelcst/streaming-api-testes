from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import obter_usuario_atual
from app.database import PLANOS

router = APIRouter(prefix="/api/assinatura", tags=["assinatura"])


class AlterarPlanoRequest(BaseModel):
    novo_plano: str


@router.get("")
def consultar_assinatura(usuario=Depends(obter_usuario_atual)):
    return {"plano": usuario["plano"], "detalhes": PLANOS[usuario["plano"]]}


@router.post("/alterar")
def alterar_plano(dados: AlterarPlanoRequest, usuario=Depends(obter_usuario_atual)):
    if dados.novo_plano not in PLANOS:
        raise HTTPException(status_code=400, detail="Plano inválido")

    novo_limite_perfis = PLANOS[dados.novo_plano]["limite_perfis"]

    if len(usuario["perfis"]) > novo_limite_perfis:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Não é possível migrar para o plano '{dados.novo_plano}': "
                f"você tem {len(usuario['perfis'])} perfis, mas o limite desse plano é {novo_limite_perfis}. "
                "Remova perfis antes de continuar."
            ),
        )

    usuario["plano"] = dados.novo_plano

    return {"mensagem": "Plano alterado com sucesso", "plano": usuario["plano"]}
