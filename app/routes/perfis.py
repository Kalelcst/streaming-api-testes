from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import obter_usuario_atual
from app.database import PLANOS

router = APIRouter(prefix="/api/perfis", tags=["perfis"])


class CriarPerfilRequest(BaseModel):
    nome: str


@router.get("")
def listar_perfis(usuario=Depends(obter_usuario_atual)):
    return {"perfis": usuario["perfis"]}


@router.post("")
def criar_perfil(dados: CriarPerfilRequest, usuario=Depends(obter_usuario_atual)):
    limite = PLANOS[usuario["plano"]]["limite_perfis"]

    if len(usuario["perfis"]) >= limite:
        raise HTTPException(
            status_code=400,
            detail=f"Limite de {limite} perfis atingido para o plano '{usuario['plano']}'",
        )

    if not dados.nome.strip():
        raise HTTPException(status_code=400, detail="Nome do perfil é obrigatório")

    novo_perfil = {"id": usuario["proximo_id_perfil"], "nome": dados.nome}
    usuario["perfis"].append(novo_perfil)
    usuario["proximo_id_perfil"] += 1

    return novo_perfil


@router.delete("/{perfil_id}")
def remover_perfil(perfil_id: int, usuario=Depends(obter_usuario_atual)):
    perfil = next((p for p in usuario["perfis"] if p["id"] == perfil_id), None)

    if perfil is None:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    if len(usuario["perfis"]) == 1:
        raise HTTPException(status_code=400, detail="A conta deve ter pelo menos um perfil")

    usuario["perfis"].remove(perfil)
    return {"mensagem": "Perfil removido com sucesso"}
