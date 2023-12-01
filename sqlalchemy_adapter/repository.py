from typing import Generic, List, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from .core import get_session
from .model import Model

T = TypeVar("T", bound=Model)
K = TypeVar("K")


class Repository(Generic[T, K]):
    model_class: Type[T]

    @property
    def session(self) -> Session:
        return get_session()

    def find_all(self) -> List[T]:
        query = select(self.model_class)
        result = self.session.scalars(query).all()
        return list(result)
