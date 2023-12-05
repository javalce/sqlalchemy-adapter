import abc
from typing import Generic, List, Type, TypeVar, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..model import Model

T = TypeVar("T", bound=Model)
K = TypeVar("K")


class AbstractRepository(abc.ABC, Generic[T, K]):
    model_class: Type[T]

    @abc.abstractproperty
    def session(self) -> Session:
        ...

    def find_all(self) -> List[T]:
        query = select(self.model_class)
        result = self.session.scalars(query).all()
        return list(result)

    def find_by_id(self, model_id: K) -> Union[T, None]:
        return self.session.get(self.model_class, model_id)

    def save(self, model: T) -> T:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def save_all(self, models: List[T]) -> List[T]:
        self.session.add_all(models)
        self.session.commit()
        for model in models:
            self.session.refresh(model)
        return models

    def delete(self, model: T) -> None:
        self.session.delete(model)
        self.session.commit()

    def delete_by_id(self, model_id: K) -> None:
        model = self.find_by_id(model_id)
        if model:
            self.delete(model)
            self.session.commit()
