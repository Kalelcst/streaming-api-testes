def test_buscar_catalogo_sem_filtros_retorna_todos_os_titulos(client, auth_headers):
    resposta = client.get("/api/catalogo", headers=auth_headers)

    assert resposta.status_code == 200
    assert resposta.json()["total"] == 6  # tamanho do catálogo de seed


def test_filtrar_catalogo_por_tipo(client, auth_headers):
    resposta = client.get("/api/catalogo?tipo=serie", headers=auth_headers)

    corpo = resposta.json()
    assert all(item["tipo"] == "serie" for item in corpo["resultados"])


def test_filtrar_catalogo_por_genero(client, auth_headers):
    resposta = client.get("/api/catalogo?genero=comedia", headers=auth_headers)

    corpo = resposta.json()
    assert all(item["genero"] == "comedia" for item in corpo["resultados"])


def test_buscar_catalogo_por_termo_no_titulo(client, auth_headers):
    resposta = client.get("/api/catalogo?busca=enigma", headers=auth_headers)

    corpo = resposta.json()
    assert corpo["total"] == 1
    assert "Enigma" in corpo["resultados"][0]["titulo"]


def test_paginacao_do_catalogo(client, auth_headers):
    resposta = client.get("/api/catalogo?pagina=1&limite=2", headers=auth_headers)

    corpo = resposta.json()
    assert len(corpo["resultados"]) == 2
    assert corpo["pagina"] == 1


def test_buscar_catalogo_exige_autenticacao(client):
    resposta = client.get("/api/catalogo")

    assert resposta.status_code == 401
