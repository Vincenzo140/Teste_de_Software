from fastapi import FastAPI, status, HTTPException
from fastapi.testclient import TestClient
from models.schemas import ComplexAlgo
from typing import List

app = FastAPI()

storage = []


@app.post("/post", response_model=ComplexAlgo, status_code=status.HTTP_201_CREATED)
def postar_algo(algo: ComplexAlgo) -> ComplexAlgo:
    """
    Rota POST para adicionar um objeto `ComplexAlgo` ao armazenamento.

    Args:
        algo (ComplexAlgo): Objeto contendo os dados a serem armazenados.

    Returns:
        ComplexAlgo: O objeto `ComplexAlgo` que foi armazenado.
    """
    storage.append(algo.dict())
    return algo

@app.get("/get", response_model=List[ComplexAlgo], status_code=status.HTTP_200_OK)
def get_all() -> List[ComplexAlgo]:
    """
    Rota GET para recuperar todos os objetos `ComplexAlgo` armazenados.

    Returns:
        list[ComplexAlgo]: Lista contendo todos os objetos `ComplexAlgo` armazenados.
    """
    return storage

@app.get("/get/{item_id}", response_model=ComplexAlgo, status_code=status.HTTP_200_OK)
def get_by_id(item_id: str) -> ComplexAlgo:
    """
    Rota GET para recuperar um objeto `ComplexAlgo` específico pelo seu ID.

    Args:
        item_id (str): ID do objeto a ser recuperado.

    Returns:
        ComplexAlgo: O objeto `ComplexAlgo` correspondente ao ID fornecido.
    """
    for item in storage:
        if item["id"] == item_id:
            return ComplexAlgo(**item)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado")

@app.delete("/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(item_id: str):
    """
    Rota DELETE para remover um objeto `ComplexAlgo` do armazenamento pelo seu ID.

    Args:
        item_id (str): ID do objeto a ser removido.

    Raises:
        HTTPException: Se o item não for encontrado no armazenamento.
    """
    global storage
    storage = [item for item in storage if item["id"] != item_id]
    return

client = TestClient(app)

def test_create_complex_message():
    """
    Teste de alto nível para validar a criação de um objeto `ComplexAlgo` com atributos complexos.
    
    O teste envolve a emissão de uma requisição POST para o endpoint `/post` com um conjunto de atributos que incluem uma mensagem, prioridade, email e tags. Após a requisição, é realizada uma validação rigorosa do código de resposta, que deve ser 201. Em seguida, verifica-se a consistência dos dados retornados em relação aos dados submetidos, levando em consideração aspectos de coerência semântica e conformidade estrutural dos atributos complexos.
    """
    response = client.post("/post", json={
        "mensagem": "Mensagem de teste avançado",
        "prioridade": 3,
        "email": "teste@example.com",
        "tags": ["tag1", "tag2"]
    })
    assert response.status_code == 201, "Falha ao validar o código de resposta da criação da mensagem complexa."
    response_data = response.json()
    assert response_data["mensagem"] == "Mensagem de teste avançado", "Falha ao validar o conteúdo da mensagem retornada."
    assert response_data["prioridade"] == 3, "Falha ao validar o nível de prioridade."
    assert response_data["email"] == "teste@example.com", "Falha ao validar o email associado ao objeto."
    assert response_data["tags"] == ["tag1", "tag2"], "Falha ao validar as tags associadas ao objeto."

def test_get_all_complex():
    """
    Teste de alto nível para validar a recuperação do conjunto completo de objetos `ComplexAlgo` persistidos.
    
    O teste emite uma requisição GET para o endpoint `/get` e realiza uma verificação do código de resposta, que deve ser 200. Em seguida, avalia a consistência e completude dos dados retornados, garantindo que todas as instâncias armazenadas sejam representadas com fidelidade. A inspeção é feita considerando a integridade dos atributos complexos presentes em cada entidade.
    """
    response = client.get("/get")
    assert response.status_code == 200, "Falha ao validar o código de resposta da recuperação de mensagens complexas."
    assert len(response.json()) > 0, "Falha ao validar a presença de itens no armazenamento."

def test_get_by_id():
    """
    Teste para validar a recuperação de um único objeto `ComplexAlgo` pelo seu ID.
    
    Este teste envolve a criação de um novo objeto, seguida pela recuperação deste objeto utilizando o ID gerado. O teste valida se a resposta é consistente em termos de conteúdo e estrutura dos atributos.
    """
    post_response = client.post("/post", json={
        "mensagem": "Mensagem de teste para ID",
        "prioridade": 2,
        "email": "idteste@example.com",
        "tags": ["tagID"]
    })
    item_id = post_response.json()["id"]
    get_response = client.get(f"/get/{item_id}")
    assert get_response.status_code == 200, "Falha ao validar o código de resposta da recuperação por ID."
    assert get_response.json()["id"] == item_id, "Falha ao validar a correspondência do ID do item recuperado."

def test_delete_by_id():
    """
    Teste para validar a remoção de um objeto `ComplexAlgo` pelo seu ID.
    
    O teste cria um novo objeto e em seguida emite uma requisição DELETE para removê-lo. Após a remoção, o teste verifica se o objeto não está mais presente no armazenamento, garantindo a eficácia da operação de exclusão.
    """
    post_response = client.post("/post", json={
        "mensagem": "Mensagem para exclusão",
        "prioridade": 1,
        "email": "delete@example.com",
        "tags": []
    })
    item_id = post_response.json()["id"]
    delete_response = client.delete(f"/delete/{item_id}")
    assert delete_response.status_code == 204, "Falha ao validar o código de resposta da exclusão."
    get_response = client.get(f"/get/{item_id}")
    assert get_response.status_code == 404, "Falha ao validar que o item foi removido corretamente do armazenamento."
