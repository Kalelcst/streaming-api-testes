def test_solicitar_reset_para_email_existente_gera_codigo(client):
    resposta = client.post(
        "/api/senha/reset/solicitar", json={"email": "cliente2@streamteste.com"}
    )

    assert resposta.status_code == 200
    assert "codigo_debug" in resposta.json()
    assert len(resposta.json()["codigo_debug"]) == 6


def test_solicitar_reset_para_email_inexistente_nao_revela_a_base(client):
    resposta = client.post(
        "/api/senha/reset/solicitar", json={"email": "naoexiste@streamteste.com"}
    )

    assert resposta.status_code == 200
    assert "codigo_debug" not in resposta.json()


def test_confirmar_reset_sem_solicitacao_previa_retorna_erro(client):
    resposta = client.post(
        "/api/senha/reset/confirmar",
        json={"email": "cliente1@streamteste.com", "codigo": "123456", "nova_senha": "NovaSenha123"},
    )

    assert resposta.status_code == 400


def test_confirmar_reset_com_codigo_incorreto_retorna_erro(client):
    email = "cliente2@streamteste.com"
    client.post("/api/senha/reset/solicitar", json={"email": email})

    resposta = client.post(
        "/api/senha/reset/confirmar",
        json={"email": email, "codigo": "000000", "nova_senha": "NovaSenha123"},
    )

    assert resposta.status_code == 400
    assert "inválido" in resposta.json()["detail"]


def test_confirmar_reset_com_nova_senha_curta_retorna_erro(client):
    email = "cliente2@streamteste.com"
    solicitar = client.post("/api/senha/reset/solicitar", json={"email": email})
    codigo = solicitar.json()["codigo_debug"]

    resposta = client.post(
        "/api/senha/reset/confirmar",
        json={"email": email, "codigo": codigo, "nova_senha": "123"},
    )

    assert resposta.status_code == 400


def test_fluxo_completo_de_reset_permite_login_com_nova_senha(client):
    email = "cliente2@streamteste.com"
    solicitar = client.post("/api/senha/reset/solicitar", json={"email": email})
    codigo = solicitar.json()["codigo_debug"]

    confirmar = client.post(
        "/api/senha/reset/confirmar",
        json={"email": email, "codigo": codigo, "nova_senha": "SenhaNova@2024"},
    )
    assert confirmar.status_code == 200

    login = client.post("/api/auth/login", json={"email": email, "senha": "SenhaNova@2024"})
    assert login.status_code == 200
    assert "token" in login.json()
