from passlib.hash import bcrypt

# Senha de todos os usuários de seed: "Senha@123"
# (rounds=4 deixa o hash rápido; é só um dado fictício de teste)
_SENHA_HASH = bcrypt.using(rounds=4).hash("Senha@123")

PLANOS = {
    "basico": {"preco": 19.90, "limite_perfis": 1, "limite_dispositivos": 1},
    "padrao": {"preco": 29.90, "limite_perfis": 3, "limite_dispositivos": 2},
    "premium": {"preco": 44.90, "limite_perfis": 5, "limite_dispositivos": 4},
}

# "Banco de dados" em memória (fictício, apenas para testes/portfólio).
usuarios = [
    {
        "id": 1,
        "nome": "Cliente Um",
        "email": "cliente1@streamteste.com",
        "senha": _SENHA_HASH,
        "plano": "padrao",
        "perfis": [{"id": 1, "nome": "Principal"}, {"id": 2, "nome": "Crianças"}],
        "proximo_id_perfil": 3,
        "dispositivos_ativos": [],
        "proximo_id_dispositivo": 1,
    },
    {
        "id": 2,
        "nome": "Cliente Dois",
        "email": "cliente2@streamteste.com",
        "senha": _SENHA_HASH,
        "plano": "basico",
        "perfis": [{"id": 1, "nome": "Principal"}],
        "proximo_id_perfil": 2,
        "dispositivos_ativos": [],
        "proximo_id_dispositivo": 1,
    },
]

catalogo = [
    {"id": 1, "titulo": "O Enigma da Ilha", "tipo": "filme", "genero": "suspense", "ano": 2022},
    {"id": 2, "titulo": "Risos no Escritório", "tipo": "serie", "genero": "comedia", "ano": 2020},
    {"id": 3, "titulo": "Fronteira Final", "tipo": "serie", "genero": "ficcao", "ano": 2023},
    {"id": 4, "titulo": "Sabores do Mundo", "tipo": "serie", "genero": "documentario", "ano": 2019},
    {"id": 5, "titulo": "Código Vermelho", "tipo": "filme", "genero": "acao", "ano": 2021},
    {"id": 6, "titulo": "Detetives do Bairro", "tipo": "serie", "genero": "comedia", "ano": 2022},
]

# Códigos temporários de reset de senha: { email: {"codigo": str, "expira_em": float} }
codigos_reset = {}


def buscar_por_email(email: str):
    return next((u for u in usuarios if u["email"] == email), None)


def buscar_por_id(usuario_id: int):
    return next((u for u in usuarios if u["id"] == usuario_id), None)
