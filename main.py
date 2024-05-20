from fastapi import FastAPI

from typing import Union

from model.model_name import ModelName
from model.items import Item

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
    return fake_items_db[skip: skip + limit]  # Example of path for this endpoint:
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


# Example of a request body in a POST method
@app.post("/items5/")
async def create_item(item: Item):
    item_dict = item.dict() # Convert the item to a dictionary. It's possible by pydantic
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# Example of a request body in a POST method with path parameters
@app.put("/items6/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# Example of a request body in a POST method with path parameters and query parameters
@app.put("/items7/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    """
    The function parameters will be recognized as follows:

    If the parameter is also declared in the path, it will be used as a path parameter.
    If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
    If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
    """
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

