from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy_adapter.model import Model


def test_model_default_tablename():
    class TestModelWithoutTablename(Model):
        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    assert issubclass(TestModelWithoutTablename, DeclarativeBase)
    assert getattr(TestModelWithoutTablename, "__tablename__", None) == "test_model_without_tablename"


def test_model_tablename_custom():
    class TestModelWithTablename(Model):
        __tablename__ = "test"

        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    assert issubclass(TestModelWithTablename, DeclarativeBase)
    assert getattr(TestModelWithTablename, "__tablename__", None) == "test"
