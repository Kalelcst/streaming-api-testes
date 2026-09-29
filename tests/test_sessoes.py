def test_abrir_sessao_dentro_do_limite_de_dispositivos(client, auth_headers):
    # cliente1 está no plano "padrao" (limite de 2 dispositivos)
    resposta = client.post("/api/sessoes", json={"dispositivo": "TV Sala"}, headers=auth_headers)

    assert resposta.status_code == 200
    assert resposta.json()["dispositivo"] == "TV Sala"


def test_abrir_sessao_alem_do_limite_retorna_erro(client, auth_headers_basico):
    # cliente2 está no plano "basico" (limite de 1 dispositivo)
    client.post("/api/sessoes", json={"dispositivo": "Celular"}, headers=auth_headers_basico)

    resposta = client.post("/api/sessoes", json={"dispositivo": "Notebook"}, headers=auth_headers_basico)

    assert resposta.status_code == 400
    assert "Limite" in resposta.json()["detail"]


def test_listar_sessoes_ativas(client, auth_headers):
    client.post("/api/sessoes", json={"dispositivo": "TV Sala"}, headers=auth_headers)

    resposta = client.get("/api/sessoes", headers=auth_headers)

    assert resposta.status_code == 200
    assert len(resposta.json()["dispositivos_ativos"]) == 1


def test_encerrar_sessao_existente(client, auth_headers):
    abrir = client.post("/api/sessoes", json={"dispositivo": "TV Sala"}, headers=auth_headers)
    sessao_id = abrir.json()["id"]

    resposta = client.delete(f"/api/sessoes/{sessao_id}", headers=auth_headers)

    assert resposta.status_code == 200


def test_encerrar_sessao_inexistente_retorna_404(client, auth_headers):
    resposta = client.delete("/api/sessoes/999", headers=auth_headers)

    assert resposta.status_code == 404
