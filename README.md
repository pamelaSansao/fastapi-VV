### **Guia: Iniciando um Projeto FastAPI com Qualidade de Código**

Este guia irá nos ajudar a criar a estrutura base para nossa aula de Qualidade e Teste de Software. Vamos configurar um ambiente local com as ferramentas essenciais de formatação, linting e teste.

#### **Passo 1: Estrutura do Projeto**

Primeiro, vamos criar uma estrutura de pastas simples e organizada.

Bash

```
# Crie a pasta principal do projeto
mkdir projeto_qts_fastapi
cd projeto_qts_fastapi

# Crie as pastas da aplicação e dos testes
mkdir app
mkdir tests
```


A estrutura final será esta:

```
projeto_qts_fastapi/
├── app/
│   ├── __init__.py      # Torna 'app' um módulo Python
│   └── main.py          # Onde nosso código FastAPI viverá
├── tests/
│   ├── __init__.py      # Torna 'tests' um módulo Python
│   └── test_main.py     # Onde nossos testes viverão
└── requirements.txt     # Nossas dependências
```

Crie os arquivos vazios `__init__.py` dentro de `app` e `tests`.

#### **Passo 2: Configuração do Ambiente e Instalação**

É uma boa prática usar um ambiente virtual para cada projeto.

Bash

```
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
# venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```



Agora, crie o arquivo `requirements.txt` na raiz do projeto (`projeto_qts_fastapi/`) com o seguinte conteúdo:

**requirements.txt**

```
# Framework principal
fastapi[standard]

# Ferramentas de Qualidade e Teste
pytest
black
flake8
```

Com o arquivo criado, instale todas as dependências de uma vez:

Bash

```
pip install -r requirements.txt
```

#### **Passo 3: Criando a Aplicação FastAPI (O "Antes")**

Agora, vamos escrever o código inicial em `app/main.py`. **Vamos escrevê-lo intencionalmente com má formatação e alguns erros de lint** para vermos as ferramentas em ação.

**app/main.py (Versão inicial, com problemas)**

Python

```
from fastapi import FastAPI
import os # import não utilizado

# esta é uma aplicação de exemplo
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Olá Mundo"}

@app.get("/user/{user_id}")
def read_user(user_id: int, q:str | None=None):
    return {'user_id': user_id, 'q': q}


def uma_funcao_muito_longa_para_demonstrar_o_poder_do_black_em_quebrar_linhas_automaticamente(param1, param2, param3, param4, param5):
    print("Esta função tem uma assinatura muito longa!")
    return param1+param2+param3+param4+param5
```

**Problemas neste código:**

1. Importação de `os` que não é utilizada.
    
2. Espaçamento inconsistente (ex: 2 linhas em branco após o import).
    
3. Aspas duplas em `"Olá Mundo"`. O Black padroniza para aspas simples se for mais comum no arquivo.
    
4. A assinatura da função `uma_funcao_muito_longa_para_demonstrar_o_poder_do_black...` é excessivamente longa e viola a recomendação de 79/88 caracteres por linha do PEP 8.
    
5. A declaração de tipo `q:str | None=None` usa `|` que é moderno, mas o Black pode padronizá-lo dependendo da configuração.
    

#### **Passo 4: Formatando com Black (A Mágica da Formatação)**

O **Black** é um formatador de código "opinativo". Ele não dá opções, apenas reformata seu código para um padrão consistente.

Execute o seguinte comando na raiz do projeto:

Bash

```
black .
```

Você verá uma saída parecida com esta:

```
reformatted app/main.py
All done! ✨ 🍰 ✨
1 file reformatted.
```

Agora, veja o arquivo `app/main.py`. Ele foi magicamente transformado:

**app/main.py (Após o `black`)**

Python

```
from fastapi import FastAPI
import os  # import não utilizado

# esta é uma aplicação de exemplo
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Olá Mundo"}


@app.get("/user/{user_id}")
def read_user(user_id: int, q: str | None = None):
    return {"user_id": user_id, "q": q}


def uma_funcao_muito_longa_para_demonstrar_o_poder_do_black_em_quebrar_linhas_automaticamente(
    param1, param2, param3, param4, param5
):
    print("Esta função tem uma assinatura muito longa!")
    return param1 + param2 + param3 + param4 + param5
```

**O que o Black fez?**

- Ajustou os espaços em branco.
    
- Quebrou a linha da função longa de forma legível.
    
- Padronizou o espaçamento na declaração do parâmetro `q`.
    

#### **Passo 5: Encontrando Erros com Flake8 (O Inspetor de Código)**

A formatação está bonita, mas o código ainda tem problemas que não são de estilo. O **Flake8** é um "linter", ele inspeciona o código em busca de erros e violações do guia de estilo PEP 8.

Execute o seguinte comando na raiz do projeto:

Bash

```
flake8 .
```

O `flake8` irá apontar o problema:

```
./app/main.py:2:1: F401 'os' imported but unused
```

Ele está nos dizendo exatamente o que está errado: no arquivo `app/main.py`, linha 2, coluna 1, o erro `F401` significa que o módulo `os` foi importado, mas nunca usado.

Vamos corrigir isso removendo a linha `import os` de `app/main.py`.

**app/main.py (Versão final e corrigida)**

Python

```
from fastapi import FastAPI

# esta é uma aplicação de exemplo
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Olá Mundo"}


@app.get("/user/{user_id}")
def read_user(user_id: int, q: str | None = None):
    return {"user_id": user_id, "q": q}


def uma_funcao_muito_longa_para_demonstrar_o_poder_do_black_em_quebrar_linhas_automaticamente(
    param1, param2, param3, param4, param5
):
    print("Esta função tem uma assinatura muito longa!")
    return param1 + param2 + param3 + param4 + param5
```

Se você rodar `flake8 .` novamente, não haverá nenhuma saída. Silêncio significa sucesso!

#### **Passo 6: Escrevendo Testes Unitários com Pytest**

Agora vamos criar os testes para nossos endpoints no arquivo `tests/test_main.py`. O `pytest` usa o `TestClient` do FastAPI para fazer requisições à nossa aplicação em memória, sem precisar de um servidor rodando.

**tests/test_main.py**

Python

```
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    """Testa se a rota raiz ('/') retorna status 200 e a mensagem correta."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Olá Mundo"}


def test_read_user():
    """Testa a rota de usuário com um ID específico."""
    user_id = 42
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "q": None}


def test_read_user_with_query_param():
    """Testa a rota de usuário com um parâmetro de query."""
    user_id = 10
    query_param = "test_query"
    response = client.get(f"/user/{user_id}?q={query_param}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "q": query_param}
```

**Nota:** As ferramentas de qualidade também se aplicam aos testes! Rode `black .` e `flake8 .` novamente para garantir que seu código de teste também está limpo e bem formatado.

#### **Passo 7: Executando os Testes**

Com os testes escritos, vamos executá-los usando o `pytest`.

Bash

```
pytest -v
```

A opção `-v` é para o modo "verbose", que nos dá mais detalhes. A saída deve ser:

```
============================= test session starts ==============================
...
tests/test_main.py::test_read_root PASSED                                  [ 33%]
tests/test_main.py::test_read_user PASSED                                  [ 66%]
tests/test_main.py::test_read_user_with_query_param PASSED                 [100%]

============================== 3 passed in ...s ================================
```

#### **Passo 8: Rodando a Aplicação Localmente**

Finalmente, para ver a aplicação funcionando no seu navegador, execute:

Bash

```
fastapi dev
```


#### Passo 9: Conflito entre black extension e black formater

- Ao salvar automatico no VS code o black tem configuração de line-lenght de 88 por padrão
- Isso gera conflito entre o flake8 que fala que precisa ser 79 e o black.

Inserir/ criar arquivo `pyproject.toml`


```
[tool.black]

line-length = 79
```


#### Passo 10: Adicionar arquivos de exclusão

- Crie o arquivo `.flake8` na raiz do projeto 
- Adicione o código 

```
[flake8]
exclude =
    .git,
    __pycache__,
    venv
```

#### Passo 11: Adicionar Pipiline de CI

- Crie o arquivo `ci.yml` em `.github\workflows`

```
name: CI Pipeline

# Quando executar: a cada push ou pull request
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
    ci:
        runs-on: ubuntu-latest
        steps:
            # Fazer checkout do código
            - name: Fazer checkout do código
              uses: actions/checkout@v4

            # Configurar Python
            - name: Set up Python
              uses: actions/setup-python@v4
              with:
                  python-version: '3.12.2'
            
            - name: Instalar dependências
              run: pip install -r requirements.txt

            - name: Verificar formatação com Black
              run: black --check .

            - name: Verificar linting com Flake8
              run: flake8 .

            - name: Executar testes com pytest
              run: pytest
```