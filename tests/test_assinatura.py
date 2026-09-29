def test_consultar_assinatura_atual(client, auth_headers):
    resposta = client.get("/api/assinatura", headers=auth_headers)

    assert resposta.status_code == 200
    assert resposta.json()["plano"] == "padrao"


def test_upgrade_de_plano_com_sucesso(client, auth_headers_basico):
    resposta = client.post(
        "/api/assinatura/alterar", json={"novo_plano": "premium"}, headers=auth_headers_basico
    )

    assert resposta.status_code == 200
    assert resposta.json()["plano"] == "premium"


def test_downgrade_para_plano_invalido_retorna_erro(client, auth_headers):
    resposta = client.post(
        "/api/assinatura/alterar", json={"novo_plano": "inexistente"}, headers=auth_headers
    )

    assert resposta.status_code == 400


def test_downgrade_bloqueado_quando_excede_limite_de_perfis_do_novo_plano(client, auth_headers):
    # cliente1 tem 2 perfis e está no plano "padrao"; o plano "basico" só permite 1
    resposta = client.post(
        "/api/assinatura/alterar", json={"novo_plano": "basico"}, headers=auth_headers
    )

    assert resposta.status_code == 400
    assert "Remova perfis" in resposta.json()["detail"]


def test_downgrade_permitido_quando_dentro_do_limite_do_novo_plano(client, auth_headers_basico):
    # cliente2 tem 1 perfil só — pode ficar em "basico" sem problema, mesmo já estando nele
    resposta = client.post(
        "/api/assinatura/alterar", json={"novo_plano": "basico"}, headers=auth_headers_basico
    )

    assert resposta.status_code == 200
