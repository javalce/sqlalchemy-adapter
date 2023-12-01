import re
from typing import Any, Dict

from sqlalchemy.orm import DeclarativeBase


class Tablename:
    def __get__(self, _: Any, cls: Any) -> Any:
        if cls.__dict__.get("__tablename__") is None and cls.__dict__.get("__table__") is None:
            name = re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", cls.__name__)
            cls.__tablename__ = name.lower().lstrip("_")
        return getattr(cls, "__tablename__", None)


class ModelMixin:
    __metadatas__: Dict[str, Any] = {}
    __tablename__: Any = Tablename()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)


class Model(ModelMixin, DeclarativeBase):
    __abstract__ = True
