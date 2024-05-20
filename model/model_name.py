from enum import Enum


class ModelName(str, Enum):
    """Model name enum."""
    telecentro = "telecentro"
    movistar = "movistar"
    claro = "claro"
    fibertel = "fibertel"
