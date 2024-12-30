from typing import Generic, Sequence, TypeVar, Optional
from pydantic.generics import GenericModel

# Tipo genérico para el contenido de la respuesta
T = TypeVar("T")

class ResponseSchema(GenericModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    error: Optional[Sequence] = None
    status_code: int = 201