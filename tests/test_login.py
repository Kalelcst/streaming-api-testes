def test_login_com_credenciais_validas_retorna_token(client):
    resposta = client.post(
        "/api/auth/login", json={"email": "cliente1@streamteste.com", "senha": "Senha@123"}
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert "token" in corpo
    assert corpo["usuario"]["email"] == "cliente1@streamteste.com"


def test_login_com_senha_incorreta_retorna_401(client):
    resposta = client.post(
        "/api/auth/login", json={"email": "cliente1@streamteste.com", "senha": "senhaErrada"}
    )

    assert resposta.status_code == 401


def test_login_com_email_nao_cadastrado_retorna_401(client):
    resposta = client.post(
        "/api/auth/login", json={"email": "naoexiste@streamteste.com", "senha": "Senha@123"}
    )

    assert resposta.status_code == 401


def test_login_sem_senha_retorna_erro_de_validacao(client):
    resposta = client.post("/api/auth/login", json={"email": "cliente1@streamteste.com"})

    assert resposta.status_code == 422  # validação automática do FastAPI/Pydantic


def test_rota_protegida_bloqueia_acesso_sem_token(client):
    resposta = client.get("/api/perfis")

    assert resposta.status_code == 401


def test_rota_protegida_bloqueia_acesso_com_token_invalido(client):
    resposta = client.get("/api/perfis", headers={"Authorization": "Bearer token-invalido"})

    assert resposta.status_code == 401


def test_rota_protegida_permite_acesso_com_token_valido(client, auth_headers):
    resposta = client.get("/api/perfis", headers=auth_headers)

    assert resposta.status_code == 200
