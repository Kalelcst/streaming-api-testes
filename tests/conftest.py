import copy

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app

EMAIL_PADRAO = "cliente1@streamteste.com"
EMAIL_BASICO = "cliente2@streamteste.com"
SENHA_PADRAO = "Senha@123"

_USUARIOS_INICIAIS = copy.deepcopy(database.usuarios)
_CATALOGO_INICIAL = copy.deepcopy(database.catalogo)


@pytest.fixture(autouse=True)
def resetar_banco_de_dados():
    """Restaura o "banco de dados" em memória antes de cada teste.

    Sem isso, um teste que altera o plano, os perfis ou as sessões de um
    usuário afetaria os testes seguintes — o mesmo problema de isolamento
    que corrigimos no projeto do banco, aqui resolvido de forma preventiva.
    """
    database.usuarios.clear()
    database.usuarios.extend(copy.deepcopy(_USUARIOS_INICIAIS))
    database.catalogo.clear()
    database.catalogo.extend(copy.deepcopy(_CATALOGO_INICIAL))
    database.codigos_reset.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token(client):
    resposta = client.post("/api/auth/login", json={"email": EMAIL_PADRAO, "senha": SENHA_PADRAO})
    return resposta.json()["token"]


@pytest.fixture
def token_basico(client):
    resposta = client.post("/api/auth/login", json={"email": EMAIL_BASICO, "senha": SENHA_PADRAO})
    return resposta.json()["token"]


@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_basico(token_basico):
    return {"Authorization": f"Bearer {token_basico}"}
