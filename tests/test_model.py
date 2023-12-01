from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy_adapter.model import Model


def test_model_default_tablename():
    class TestModel(Model):
        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    assert issubclass(TestModel, DeclarativeBase)
    assert getattr(TestModel, "__tablename__", None) == "test_model"

    Model.metadata.clear()


def test_model_tablename_custom():
    class TestModel(Model):
        __tablename__ = "test"

        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    assert issubclass(TestModel, DeclarativeBase)
    assert getattr(TestModel, "__tablename__", None) == "test"

    Model.metadata.clear()
