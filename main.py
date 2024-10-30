from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

storage = []

class Algo(BaseModel):
    mensagem: str

@app.post("/post", response_model=Algo, status_code=status.HTTP_200_OK)
def postar_aluno(algo: Algo) -> Algo:
    storage.append(algo.dict())
    return algo

@app.get("/get", response_model=list[Algo], status_code=status.HTTP_200_OK)
def get_all():
    return storage

client = TestClient(app)

def test_create_message():
    response = client.post("/post", json={"mensagem": "string"})
    assert response.status_code == 200
    assert response.json() == {"mensagem": "string"}


def test_get_all():
    response = client.get("/get")
    assert response.status_code == 200
    assert response.json() == [{"mensagem": "string"}]