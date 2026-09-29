def test_listar_perfis_da_conta(client, auth_headers):
    resposta = client.get("/api/perfis", headers=auth_headers)

    assert resposta.status_code == 200
    assert len(resposta.json()["perfis"]) == 2  # seed do cliente1: 2 perfis


def test_criar_perfil_dentro_do_limite_do_plano(client, auth_headers):
    # cliente1 está no plano "padrao" (limite de 3 perfis) e já tem 2
    resposta = client.post("/api/perfis", json={"nome": "Perfil Trabalho"}, headers=auth_headers)

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Perfil Trabalho"


def test_criar_perfil_alem_do_limite_do_plano_retorna_erro(client, auth_headers_basico):
    # cliente2 está no plano "basico" (limite de 1 perfil) e já tem 1
    resposta = client.post("/api/perfis", json={"nome": "Segundo Perfil"}, headers=auth_headers_basico)

    assert resposta.status_code == 400
    assert "Limite" in resposta.json()["detail"]


def test_criar_perfil_com_nome_vazio_retorna_erro(client, auth_headers):
    resposta = client.post("/api/perfis", json={"nome": "   "}, headers=auth_headers)

    assert resposta.status_code == 400


def test_remover_perfil_existente(client, auth_headers):
    criar = client.post("/api/perfis", json={"nome": "Perfil Temporário"}, headers=auth_headers)
    perfil_id = criar.json()["id"]

    resposta = client.delete(f"/api/perfis/{perfil_id}", headers=auth_headers)

    assert resposta.status_code == 200


def test_remover_ultimo_perfil_restante_retorna_erro(client, auth_headers_basico):
    # cliente2 só tem 1 perfil — não pode ficar sem nenhum
    resposta = client.delete("/api/perfis/1", headers=auth_headers_basico)

    assert resposta.status_code == 400
