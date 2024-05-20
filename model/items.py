from pydantic import BaseModel


class Item(BaseModel):
    """
    This is the model for the item. If you receive a item object in the request body, it will be validated
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
