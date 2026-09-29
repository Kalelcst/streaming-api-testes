from fastapi import APIRouter, HTTPException, status
from passlib.hash import bcrypt
from pydantic import BaseModel

from app.database import buscar_por_email
from app.auth import gerar_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/login")
def login(dados: LoginRequest):
    usuario = buscar_por_email(dados.email)

    if usuario is None or not bcrypt.verify(dados.senha, usuario["senha"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = gerar_token(usuario["id"])

    return {
        "token": token,
        "usuario": {"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]},
    }
