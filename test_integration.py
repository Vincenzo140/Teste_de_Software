import pytest
from fastapi.testclient import TestClient
from test_unit import app  # Supondo que seu arquivo principal se chame main.py, onde a app é instanciada

client = TestClient(app)


@pytest.fixture
def create_multiple_items():
    # Cria um conjunto de itens no sistema para testes subsequentes
    items = []
    for i in range(5):
        prioridade_valida = i + 1  # Agora as prioridades serão 1, 2, 3, 4, 5
        response = client.post("/post", json={
            "mensagem": f"Mensagem {i}",
            "prioridade": prioridade_valida,
            "email": f"email{i}@example.com",
            "tags": [f"tag{i}"]
        })
        assert response.status_code == 201
        items.append(response.json())

    return items


def test_create_with_invalid_data():
    """
    Testa o envio de dados inválidos para verificar se o sistema 
    retorna erros adequados de validação ou HTTP.
    """
    # Falta atributo obrigatório "mensagem"
    response = client.post("/post", json={
        "prioridade": 5,
        "email": "invalid@example.com",
        "tags": ["tagX"]
    })
    # Espera-se um erro de validação (422 Unprocessable Entity do FastAPI)
    assert response.status_code == 422, "Deveria falhar na validação por ausência do campo mensagem."


def test_get_non_existent_item():
    """
    Testa a tentativa de recuperar um item que não existe,
    garantindo que o sistema retorne o status code 404.
    """
    response = client.get("/get/nao_existe_id")
    assert response.status_code == 404, "Deveria retornar 404 para item inexistente."


def test_get_after_creations(create_multiple_items):
    """
    Testa a recuperação de todos os itens após a criação de múltiplos elementos,
    garantindo que todos foram persistidos adequadamente.
    """
    response = client.get("/get")
    assert response.status_code == 200
    data = response.json()
    # Confere se pelo menos 5 foram criados (considerando que o storage não é limpo entre testes)
    assert len(data) >= 5, "Deveria haver pelo menos 5 itens armazenados."


def test_delete_multiple_items(create_multiple_items):
    """
    Testa a exclusão de vários itens em sequência, garantindo que o 
    armazenamento reflita corretamente essas remoções.
    """
    # Seleciona 3 itens para deletar
    itens_para_deletar = create_multiple_items[:3]
    for item in itens_para_deletar:
        delete_response = client.delete(f"/delete/{item['id']}")
        assert delete_response.status_code == 204, f"Falha ao deletar o item {item['id']}"

    # Agora recupera a lista novamente e verifica se os itens foram realmente removidos
    final_response = client.get("/get")
    assert final_response.status_code == 200
    remaining_data = final_response.json()

    # IDs deletados não devem estar presentes
    deleted_ids = {item['id'] for item in itens_para_deletar}
    for item in remaining_data:
        assert item["id"] not in deleted_ids, "Um item deletado ainda está presente no armazenamento."


# def test_complex_scenario():
#     """
#     Teste de cenário mais complexo:
#     1. Cria dois itens
#     2. Deleta um deles
#     3. Verifica se o outro ainda existe
#     """
#     # Criação de itens
#     item1 = client.post("/post", json={
#         "mensagem": "Scenario Item 1",
#         "prioridade": 10,
#         "email": "scenario1@example.com",
#         "tags": ["scenario"]
#     }).json()

#     item2 = client.post("/post", json={
#         "mensagem": "Scenario Item 2",
#         "prioridade": 20,
#         "email": "scenario2@example.com",
#         "tags": ["scenario"]
#     }).json()

#     # Deleta o primeiro
#     delete_response = client.delete(f"/delete/{item1['id']}")
#     assert delete_response.status_code == 204, "Falha ao deletar o item no cenário complexo."

#     # Verifica se o segundo ainda existe
#     get_response = client.get(f"/get/{item2['id']}")
#     assert get_response.status_code == 200, "O segundo item deveria continuar existindo após a deleção do primeiro."
#     returned_item = get_response.json()
#     assert returned_item["id"] == item2["id"], "O ID do item retornado não corresponde ao esperado."
#     assert returned_item["mensagem"] == "Scenario Item 2", "A mensagem do segundo item não é a esperada."
