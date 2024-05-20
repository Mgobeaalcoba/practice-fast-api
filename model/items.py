from pydantic import BaseModel, Field, HttpUrl
from typing import List


# Submodel for the item
class Image(BaseModel):
    url: HttpUrl # This is a URL that must start with http or https. It's a special type of string that is used to represent URLs.
    name: str


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
    tags: List[str] = []
    set_tags: set[str] = set(tags)
    image: Image | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                    "tags": ["tag1", "tag2"],
                    "set_tags": ["tag1", "tag2"],
                    "image": {
                        "url": "https://example.com/image.jpg",
                        "name": "image.jpg"
                    }
                }
            ]
        }
    }


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: List[Item]
