from abc import ABC

class Default(ABC):

    default_callback: str = f"default_callback"
    none_callback: str = f"none_callback"