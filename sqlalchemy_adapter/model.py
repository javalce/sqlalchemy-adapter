import re
from typing import Any, Dict

from sqlalchemy.orm import DeclarativeBase


def camel_to_snake_case(name: str) -> str:
    name = re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", name)
    return name.lower().lstrip("_")


class Tablename:
    def __get__(self, _: Any, cls: Any) -> Any:
        if cls.__dict__.get("__tablename__") is None and cls.__dict__.get("__table__") is None:
            cls.__tablename__ = camel_to_snake_case(cls.__name__)
        return getattr(cls, "__tablename__", None)


class ModelMixin:
    __metadatas__: Dict[str, Any] = {}
    __tablename__: Any = Tablename()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)


class Model(ModelMixin, DeclarativeBase):
    __abstract__ = True
