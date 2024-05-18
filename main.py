from fastapi import FastAPI

from typing import Union

from model.model_name import ModelName

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Example of a path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# Example of a path parameter with a type validation with enum
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {
        "model_name": model_name
    }


# Example of a query parameter
@app.get("/items/")
async def read_item2(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit] # Example of path for this endpoint:
    # http://127.0.0.1:8000/items/?skip=0&limit=10


# Example of a optional query parameter
@app.get("/items2/{item_id}")
async def read_item3(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Example of a boolean conversion
@app.get("/items3/{item_id}")
async def read_item4(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Example of a required query parameter
@app.get("/items4/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
    # If you try to access this endpoint without the needy parameter, you will get a 422 error
