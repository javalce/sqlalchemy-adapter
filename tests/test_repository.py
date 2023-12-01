import pytest
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy_adapter.core import Database
from sqlalchemy_adapter.model import Model
from sqlalchemy_adapter.repository import Repository


class MockModel(Model):
    __tablename__ = "mock_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MockRepository(Repository[MockModel, int]):
    model_class = MockModel


@pytest.fixture(scope="module")
def db() -> Database:
    return Database("sqlite:///:memory:")


@pytest.fixture(scope="function")
def init_db(db: Database) -> None:
    with db.session_ctx():
        Model.metadata.create_all(db.engine)  # type: ignore


@pytest.mark.usefixtures("init_db")
def test_repository_find_all(db):
    with db.session_ctx() as session:
        session.add(MockModel(id=1))
        session.add(MockModel(id=2))
        session.add(MockModel(id=3))
        session.commit()

    repository = MockRepository()

    with db.session_ctx():
        result = repository.find_all()

    assert isinstance(result, list)
    assert len(result) == 3
