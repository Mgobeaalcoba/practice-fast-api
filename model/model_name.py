from enum import Enum


class ModelName(str, Enum):
    """
    Model name enum. Can be used in Path & Query parameters
    """
    telecentro = "telecentro"
    movistar = "movistar"
    claro = "claro"
    fibertel = "fibertel"
