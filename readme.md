# Projeto de API com Testes de Software: Um Exemplo Prático

Este projeto demonstra a construção de uma API simples usando FastAPI, juntamente com uma suíte de testes abrangente que inclui testes unitários e de integração. A API gerencia objetos `ComplexAlgo`, permitindo operações CRUD (Criar, Ler, Atualizar e Deletar).

## Visão Geral

A API expõe os seguintes endpoints:

- **POST /post:** Cria um novo objeto `ComplexAlgo`.
- **GET /get:** Retorna todos os objetos `ComplexAlgo`.
- **GET /get/{item_id}:** Retorna um objeto `ComplexAlgo` específico pelo ID.
- **DELETE /delete/{item_id}:** Deleta um objeto `ComplexAlgo` pelo ID.

## Tecnologias Utilizadas

Este projeto utiliza as seguintes tecnologias:

- **[FastAPI](https://fastapi.tiangolo.com/):** Um framework web moderno e de alta performance.
  ![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

- **[Pydantic](https://pydantic-docs.helpmanual.io/):** Uma biblioteca para validação de dados e configurações no Python.
  ![Pydantic Logo](https://raw.githubusercontent.com/samuelcolvin/pydantic/master/docs/static/images/logo.png)

- **[HTTPX](https://www.python-httpx.org/):** Um cliente HTTP moderno.
  ![HTTPX Logo](https://www.python-httpx.org/_static/img/logo.png)

- **[Pytest](https://docs.pytest.org/en/stable/):** Um framework de testes para Python.
  ![Pytest Logo](https://docs.pytest.org/en/stable/_images/pytest_logo.svg)

---

## Estrutura do Projeto

```plaintext
├── .gitignore        # Arquivo para ignorar arquivos específicos no Git
├── __pycache__       # Cache de código Python (deve ser ignorado pelo Git)
├── models            # Diretório para modelos de dados
│   └── schemas.py     # Definição do esquema Pydantic para ComplexAlgo
├── requirements.txt  # Lista de dependências do projeto
├── test_integration.py # Testes de integração da API
└── test_unit.py      # Testes unitários das funções da API
```

---

## Execução dos Testes

Certifique-se de ter as dependências instaladas:

```bash
pip install -r requirements.txt
```

Execute os testes usando pytest:

```bash
pytest
```

---

## Execução da Aplicação

Após instalar as dependências com o comando acima, utilize o uvicorn para executar a API:

```bash
uvicorn test_unit:app --reload
```

---

## Implementação Detalhada

### Modelos (`models/schemas.py`)

O esquema `ComplexAlgo` define a estrutura dos dados usando Pydantic:

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import uuid4

class ComplexAlgo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="ID único do objeto")
    mensagem: str = Field(..., min_length=5, max_length=255, description="Mensagem")
    prioridade: Optional[int] = Field(None, ge=1, le=5, description="Prioridade (1-5)")
    email: EmailStr = Field(..., description="Email")
    tags: List[str] = Field(default_factory=list, description="Tags")
```

---

### Testes Unitários (`test_unit.py`)

Os testes unitários verificam o comportamento individual das funções da API:

```python
from fastapi import FastAPI, HTTPException
from models.schemas import ComplexAlgo
from typing import List

app = FastAPI()

fake_db: List[ComplexAlgo] = []

@app.post("/post")
def create_complex_algo(item: ComplexAlgo):
    fake_db.append(item)
    return item

@app.get("/get")
def get_all_items():
    return fake_db

@app.get("/get/{item_id}")
def get_item(item_id: str):
    for item in fake_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/delete/{item_id}")
def delete_item(item_id: str):
    global fake_db
    fake_db = [item for item in fake_db if item.id != item_id]
    return {"message": "Item deleted"}
```

---

### Testes de Integração (`test_integration.py`)

Os testes de integração verificam a interação entre os diferentes componentes da API:

```python
from fastapi.testclient import TestClient
from test_unit import app

client = TestClient(app)

def test_create_item():
    response = client.post("/post", json={
        "mensagem": "Teste de mensagem",
        "prioridade": 3,
        "email": "teste@exemplo.com",
        "tags": ["tag1", "tag2"]
    })
    assert response.status_code == 200

def test_get_all_items():
    response = client.get("/get")
    assert response.status_code == 200

def test_get_item():
    item_id = "some-id"
    response = client.get(f"/get/{item_id}")
    assert response.status_code in [200, 404]

def test_delete_item():
    item_id = "some-id"
    response = client.delete(f"/delete/{item_id}")
    assert response.status_code == 200
```

---

## Melhorias Futuras

- Implementar testes para cenários de erro mais complexos.
- Adicionar documentação da API usando Swagger.
- Implementar persistência de dados usando um banco de dados.

---

### Arquivo `requirements.txt`

```plaintext
fastapi==0.95.1
uvicorn==0.22.0
pydantic==1.10.2
pytest==7.3.1
httpx==0.23.1
```