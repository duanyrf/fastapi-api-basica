from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


# Modelo de dados da tarefa
class Tarefa(BaseModel):
    titulo: str
    descricao: str | None = None  # Campo opcional
    concluida: bool = False


# Lista de tarefas (simulando um "banco de dados" na memória)
tarefas = []


@app.get("/")
def root():
    return {"mensagem": "Olá Mundo"}


@app.post("/tarefas", status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa)
    return {
        "mensagem": "Tarefa criada com sucesso!",
        "tarefa": tarefa.model_dump(),
    }


# Simula a busca de uma tarefa por seu ID, através de parâmetros da requisição
# Exemplo de URL: http://localhost:8000/tarefas/123
@app.get("/tarefas/{tarefa_id}")
def get_item_by_id(tarefa_id: int):
    return {"ID": tarefa_id}


# Simula a busca de uma tarefa por seu ID, através de Query Parameters
# Exemplo de URL: http://localhost:8000/tarefas?tarefa_id=123
@app.get("/tarefas")
def get_item_by_name(tarefa_id: int):
    return {"ID da Tarefa": tarefa_id}
