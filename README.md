# Streaming API Testes

![CI](https://github.com/SEU-USUARIO/streaming-api-testes/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Pytest](https://img.shields.io/badge/tested%20with-Pytest-0A9EDC)

Projeto de portfólio de **automação de testes de API** simulando uma plataforma de
streaming fictícia: autenticação, reset de senha, perfis, catálogo, sessões
simultâneas e assinatura de planos.

> ⚠️ Projeto educacional/fictício. Não representa nenhuma empresa real.

## Cenário simulado

- **Login** com JWT e **reset de senha** em duas etapas (solicitar código, confirmar)
- **Perfis** por conta, com limite que depende do plano
- **Catálogo** com busca por título, filtros (tipo, gênero) e paginação
- **Sessões simultâneas**, com limite de dispositivos por plano
- **Assinatura**: consulta, upgrade e downgrade (bloqueado se a conta tiver mais perfis do que o novo plano permite)

| Plano   | Perfis | Dispositivos simultâneos |
|---------|--------|--------------------------|
| basico  | 1      | 1                        |
| padrao  | 3      | 2                        |
| premium | 5      | 4                        |

Os dados ficam em memória, sem banco real.

## Tecnologias

FastAPI, PyJWT, passlib (bcrypt), Pytest, pytest-cov, GitHub Actions.

## Como rodar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

pytest                                   # roda a suíte de testes
pytest --cov=app --cov-report=term-missing   # com cobertura
uvicorn app.main:app --reload            # sobe a API (docs em /docs)
```

## Usuários de teste (seed)

| E-mail                     | Senha     | Plano  |
|----------------------------|-----------|--------|
| cliente1@streamteste.com   | Senha@123 | padrao |
| cliente2@streamteste.com   | Senha@123 | basico |

## Casos de teste cobertos (35)

- **Login** (`test_login.py`): credenciais válidas/inválidas, e-mail inexistente, validação automática do Pydantic, rotas protegidas sem token e com token inválido
- **Reset de senha** (`test_reset_senha.py`): geração de código, resposta genérica para e-mail inexistente, código incorreto, senha curta, fluxo completo até o novo login
- **Perfis** (`test_perfis.py`): listar, criar dentro/fora do limite do plano, nome vazio, remover, impedir remoção do último perfil
- **Catálogo** (`test_catalogo.py`): sem filtros, por tipo, por gênero, por termo, paginação, exigência de autenticação
- **Sessões** (`test_sessoes.py`): abrir dentro/fora do limite, listar, encerrar, sessão inexistente
- **Assinatura** (`test_assinatura.py`): consulta, upgrade, plano inválido, downgrade bloqueado por excesso de perfis, downgrade permitido

> **Isolamento de testes:** a fixture `resetar_banco_de_dados` (em `tests/conftest.py`,
> `autouse=True`) restaura o estado em memória antes de cada teste, então nenhum teste
> depende da ordem de execução.

## Estrutura

```
streaming-api-testes/
├── app/
│   ├── main.py, auth.py, database.py
│   └── routes/ (auth, senha, perfis, catalogo, sessoes, assinatura)
├── tests/ (conftest.py + 6 arquivos de teste)
├── requirements.txt, pytest.ini
└── .github/workflows/ci.yml
```
