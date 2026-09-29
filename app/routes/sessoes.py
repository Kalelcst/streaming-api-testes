from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import obter_usuario_atual
from app.database import PLANOS

router = APIRouter(prefix="/api/sessoes", tags=["sessoes"])


class AbrirSessaoRequest(BaseModel):
    dispositivo: str


@router.get("")
def listar_sessoes(usuario=Depends(obter_usuario_atual)):
    return {"dispositivos_ativos": usuario["dispositivos_ativos"]}


@router.post("")
def abrir_sessao(dados: AbrirSessaoRequest, usuario=Depends(obter_usuario_atual)):
    limite = PLANOS[usuario["plano"]]["limite_dispositivos"]

    if len(usuario["dispositivos_ativos"]) >= limite:
        raise HTTPException(
            status_code=400,
            detail=f"Limite de {limite} dispositivos simultâneos atingido para o plano '{usuario['plano']}'",
        )

    nova_sessao = {"id": usuario["proximo_id_dispositivo"], "dispositivo": dados.dispositivo}
    usuario["dispositivos_ativos"].append(nova_sessao)
    usuario["proximo_id_dispositivo"] += 1

    return nova_sessao


@router.delete("/{sessao_id}")
def encerrar_sessao(sessao_id: int, usuario=Depends(obter_usuario_atual)):
    sessao = next((s for s in usuario["dispositivos_ativos"] if s["id"] == sessao_id), None)

    if sessao is None:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    usuario["dispositivos_ativos"].remove(sessao)
    return {"mensagem": "Sessão encerrada com sucesso"}
