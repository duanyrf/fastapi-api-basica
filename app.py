from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    titulo: str
    descricao: str | None = None
    valor: float


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/item/{item_id}")
def get_item_by_id(item_id: int):
    return {"ID": item_id}


@app.get("/item")
def get_item_by_name(nome: str):
    return {"Nome": nome}


@app.post("/item", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return {
        "status_code": status.HTTP_201_CREATED,
        "content": {"mensagem": "Item criado com sucesso!", "item": item.model_dump()},
    }
