# API básica com FastAPI

## 🚀 1. Instalando o FastAPI

Você precisa ter o Python instalado (versão 3.7+). Em seguida, instale o FastAPI:

```bash
pip install "fastapi[standard]"
```

---

## 📦 2. Estrutura básica do projeto

Vamos começar com um único arquivo chamado `main.py`:

```
📁 seu_projeto/
 └── main.py
```

---

## 🧱 3. Criando o modelo de dados com Pydantic

FastAPI utiliza **Pydantic** para validar e manipular os dados recebidos via `body`. Então, criamos uma classe `Tarefa` que representa os dados esperados na requisição.

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

# Inicializando o app FastAPI
app = FastAPI()

# Modelo de dados da tarefa
class Tarefa(BaseModel):
    titulo: str
    descricao: str | None = None  # Campo opcional
    concluida: bool = False
```

---

## 🎯 4. Criando o endpoint POST `/tarefas`

Esse endpoint vai receber uma tarefa via `body` da requisição e retornar a mesma tarefa criada como resposta:

```python
# Lista de tarefas (simulando um "banco de dados" na memória)
tarefas = []

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa)
    return {"mensagem": "Tarefa criada com sucesso!", "tarefa": tarefa}
```

> Aqui, o FastAPI entende que o parâmetro `tarefa` (do tipo `Tarefa`) será recebido via `body`, pois é um Pydantic model.

---

## ▶️ 5. Rodando o servidor

No terminal, execute:

```bash
fastapi dev main.py
```

* `main.py`: é o nome do arquivo que contém o app do FastAPI
* `dev`: sinaliza para o FastAPI reiniciar o servidor automaticamente ao salvar alterações (útil no desenvolvimento)

---

## 🧪 6. Testando no navegador ou no Swagger UI

Acesse:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

Você verá uma interface interativa onde pode testar o endpoint `POST /tarefas`. Exemplo de corpo da requisição:

```json
{
  "titulo": "Estudar FastAPI",
  "descricao": "Aprender a criar uma API com FastAPI",
  "concluida": false
}
```

---

## ✅ Resultado esperado

Resposta da API:

```json
{
  "mensagem": "Tarefa criada com sucesso!",
  "tarefa": {
    "titulo": "Estudar FastAPI",
    "descricao": "Aprender a criar uma API com FastAPI",
    "concluida": false
  }
}
```

---

## ✅ 7. Usando `status_code` no retorno das requisições

No **FastAPI**, você pode retornar códigos de status de forma muito simples usando:

1. O parâmetro `status_code` do decorator (`@app.post`, `@app.get`, etc.)
3. O módulo `status` para usar constantes legíveis (`HTTP_201_CREATED`, `HTTP_404_NOT_FOUND`, etc.)

Essa é a forma mais comum e simples:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status

app = FastAPI()

class Tarefa(BaseModel):
    titulo: str
    descricao: str | None = None
    concluida: bool = False

tarefas = []

# definindo o status_code do retorno, em caso de sucesso
@app.post("/tarefas", status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa)
    return {"mensagem": "Tarefa criada com sucesso!", "tarefa": tarefa}
```

### 📝 O que acontece aqui?

* Ao criar uma nova tarefa, o código de resposta será `201 Created` (padrão REST para criação de recurso).
* `status.HTTP_201_CREATED` é mais legível do que usar apenas `201`.

---

## ⚙️ 8. Personalizando a resposta para controle total da informação

Se quiser retornar uma estrutura personalizada **e** um código de status de forma programática, envie como retorno um JSON com o esquema que desejar:

```python
from fastapi.responses import JSONResponse

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa)
    return {
              "status_code": status.HTTP_201_CREATED,
              "content"={"mensagem": "Tarefa criada com sucesso!", "tarefa": tarefa.model_dump()}
            }
```

Nesta resposta aplicamos a função **model_dump()** no modelo **tarefa** (`tarefa.model_dump()`) para permitir o objeto pydantic tarefa seja serializado durante o envio da resposta.

---

## 🚨 9. Lidando com erros usando status HTTP

Você pode usar a exceção `HTTPException` para retornar erros com códigos apropriados:

```python
from fastapi import HTTPException

@app.get("/tarefas/{id}")
def buscar_tarefa(id: int):
    if id < 0 or id >= len(tarefas):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return tarefas[id]
```

---

## 🧠 Dicas úteis de códigos de status

| Código | Constante FastAPI                       | Significado                    |
| ------ | --------------------------------------- | ------------------------------ |
| 200    | `status.HTTP_200_OK`                    | Sucesso (padrão)               |
| 201    | `status.HTTP_201_CREATED`               | Recurso criado                 |
| 204    | `status.HTTP_204_NO_CONTENT`            | Sucesso sem corpo de resposta  |
| 400    | `status.HTTP_400_BAD_REQUEST`           | Erro do cliente                |
| 401    | `status.HTTP_401_UNAUTHORIZED`          | Não autenticado                |
| 403    | `status.HTTP_403_FORBIDDEN`             | Proibido (sem permissão)       |
| 404    | `status.HTTP_404_NOT_FOUND`             | Recurso não encontrado         |
| 422    | `status.HTTP_422_UNPROCESSABLE_ENTITY`  | Erro de validação (automático) |
| 500    | `status.HTTP_500_INTERNAL_SERVER_ERROR` | Erro do servidor               |

---
