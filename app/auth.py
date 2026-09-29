import time
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import buscar_por_id

SEGREDO_JWT = "segredo-de-teste-nao-usar-em-producao"
ALGORITMO = "HS256"
VALIDADE_TOKEN_SEGUNDOS = 60 * 60  # 1 hora

seguranca = HTTPBearer(auto_error=False)


def gerar_token(usuario_id: int) -> str:
    payload = {"id": usuario_id, "exp": time.time() + VALIDADE_TOKEN_SEGUNDOS}
    return jwt.encode(payload, SEGREDO_JWT, algorithm=ALGORITMO)


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca),
):
    if credenciais is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não fornecido")

    try:
        payload = jwt.decode(credenciais.credentials, SEGREDO_JWT, algorithms=[ALGORITMO])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

    usuario = buscar_por_id(payload["id"])
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

    return usuario
