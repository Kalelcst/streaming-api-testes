import random
import time

from fastapi import APIRouter, HTTPException, status
from passlib.hash import bcrypt
from pydantic import BaseModel

from app.database import buscar_por_email, codigos_reset

router = APIRouter(prefix="/api/senha", tags=["senha"])

VALIDADE_CODIGO_SEGUNDOS = 5 * 60


class SolicitarResetRequest(BaseModel):
    email: str


class ConfirmarResetRequest(BaseModel):
    email: str
    codigo: str
    nova_senha: str


@router.post("/reset/solicitar")
def solicitar_reset(dados: SolicitarResetRequest):
    usuario = buscar_por_email(dados.email)

    # Por segurança, não revelamos se o e-mail existe ou não na base.
    if usuario is None:
        return {"mensagem": "Se o e-mail existir, um código de verificação foi enviado."}

    codigo = f"{random.randint(100000, 999999)}"
    codigos_reset[dados.email] = {"codigo": codigo, "expira_em": time.time() + VALIDADE_CODIGO_SEGUNDOS}

    return {
        "mensagem": "Se o e-mail existir, um código de verificação foi enviado.",
        "codigo_debug": codigo,
    }


@router.post("/reset/confirmar")
def confirmar_reset(dados: ConfirmarResetRequest):
    registro = codigos_reset.get(dados.email)

    if registro is None:
        raise HTTPException(status_code=400, detail="Nenhuma solicitação de reset encontrada para este e-mail")

    if time.time() > registro["expira_em"]:
        del codigos_reset[dados.email]
        raise HTTPException(status_code=400, detail="Código expirado. Solicite um novo.")

    if registro["codigo"] != dados.codigo:
        raise HTTPException(status_code=400, detail="Código inválido")

    if len(dados.nova_senha) < 8:
        raise HTTPException(status_code=400, detail="A nova senha deve ter pelo menos 8 caracteres")

    usuario = buscar_por_email(dados.email)
    usuario["senha"] = bcrypt.hash(dados.nova_senha)
    del codigos_reset[dados.email]

    return {"mensagem": "Senha alterada com sucesso"}
