from fastapi import FastAPI, Query, Path, Body

from typing import Union, Annotated

from model.model_name import ModelName
from model.items import Item, Offer
from model.users import User

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
    item_dict = item.dict()  # Convert the item to a dictionary. It's possible by pydantic
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


# Example of a validated query parameter
@app.get("/items8/")
async def read_items8(q: Annotated[str | None, Query(max_length=50)] = None):
    """
    The Query class is used to add validation to the query parameters.
    :param q: A optional query parameter with a max length of 50 characters
    :return: results with the query parameter if it exists
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example of other form of validated query parameter
@app.get("/items9/")
async def read_items9(q: str | None = Query(default=None, min_length=3, max_length=50)):
    """
    The Query class is used to add validation to the query parameters.
    It's highly recommended to use the Query class instead of the Annotated class for query parameters.
    :param q:
    :return:
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example of query validation with regex patterns:
@app.get("/items10/")
async def read_items10(
        q: str | None = Query(
            default=None, min_length=3, max_length=50, pattern="^fixedquery$"
            # The query parameter must be "fixedquery"
        ),
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example one of a required query parameter
@app.get("/items11/")
async def read_items11(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example two of a required query parameter with ellipsis (...)
@app.get("/items12/")
async def read_items12(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example of a query parameter list
@app.get("/items13/")
async def read_items13(q: Annotated[Union[list[str], None], Query()] = None):
    """
    To declare a query parameter with a type of list, like in the example above, you need to explicitly use Query, otherwise it would be interpreted as a request body.
    :param q:
    :return:
    """
    query_items = {"q": q}
    return query_items


# Example of a query parameter list with a default value
@app.get("/items14/")
async def read_items14(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


# Example add more metadata to the query parameter
@app.get("/items15/")
async def read_items15(
    q: Annotated[
        Union[str, None],
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example of query parameters with alias
@app.get("/items16/")
async def read_items16(q: Annotated[Union[str, None], Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example of deprecated query parameters
@app.get("/items17/")
async def read_items17(
    q: Annotated[
        Union[str, None],
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Example of query parameter exclude from docs
@app.get("/items18/")
async def read_items18(
    hidden_query: Annotated[Union[str, None], Query(include_in_schema=False)] = None,
):
    """
    The include_in_schema parameter is used to exclude the query parameter from the generated OpenAPI documentation.
    :param hidden_query:
    :return:
    """
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}


# Example of a path parameter with a path parameter validation
@app.get("/items19/{item_id}")
async def read_items19(
    item_id: Annotated[int, Path(
        title="The ID of the item to get",
        description="The ID must be a positive integer",
    )], # The title parameter is used to add a title to the parameter in the generated OpenAPI documentation.
    q: Annotated[str | None, Query(alias="item-query")] = None, # The alias parameter is used to add an alias to the parameter in the generated OpenAPI documentation.
):
    """
    In the Path Class you can declare all the same parameters as for Query.
    :param item_id:
    :param q:
    :return:
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Example of a path parameter with a path parameter number validation
@app.get("/items20/{item_id}")
async def read_items20(
    item_id: Annotated[int, Path(
        title="The ID of the item to get",
        gt=0,
        le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Example of a path, query and body parameters
@app.put("/items21/{item_id}")
async def update_item21(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# Example of multiple body parameters
@app.put("/items22/{item_id}")
async def update_item22(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# Example of use singular values in a body parameter
@app.put("/items23/{item_id}")
async def update_item23(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    """
    If you declare a parameter with the Body class, it will be interpreted as a request body.
    """
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# Example of use a BaseModel embedded in a body parameter
@app.put("/items24/{item_id}")
async def update_item24(item_id: int, item: Annotated[Item, Body(embed=True)]):
    """
    The embed parameter is used to indicate that the parameter is a Pydantic model that should be embedded in the request body.
    """
    results = {"item_id": item_id, "item": item}
    return results


# Example of use a BaseModel with a submodel in a body parameter
@app.put("/items25/{item_id}")
async def update_item25(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# Example of endpoint of nested models
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


# Example of bodies of arbitrary dict
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights