# atividade_01

Repositório: https://github.com/Lucas-BRT/CG-UFC

Requer Python >= 3.8.

## Instalação e execução

### Usando UV

```
uv sync
uv run src/atividade_01/__init__.py
```

Ou, sem instalar nada explicitamente:

```
uv run src/atividade_01/__init__.py
```

O UV resolve as dependências a partir do `pyproject.toml`/`uv.lock` automaticamente.

### Usando pip

Precisa de um Python >= 3.8 já instalado (`python3 --version`).

Crie e ative um ambiente virtual (recomendado):

```
python3 -m venv .venv
source .venv/bin/activate   # Windows sei que não usa, mas vai que né: .venv\Scripts\activate
```

Instale o projeto direto do `pyproject.toml`:

```
pip install .
```

Ou só as dependências:

```
pip install glfw "numpy>=1.24.4" pyopengl
```

Execute:

```
python src/atividade_01/__init__.py
```
