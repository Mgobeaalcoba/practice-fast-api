from pydantic import BaseModel, Field


class Item(BaseModel):
    """
    This is the model for the item. If you receive a item object in the request body, it will be validated.
    Using the Field class, you can specify additional validation rules for each field. Directly in the model, you can specify the default value for each field.
    """
    name: str
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300
    )
    price: float = Field(
        gt=0,
        description="The price must be greater than zero"
    )
    tax: float | None = None
