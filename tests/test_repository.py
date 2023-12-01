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
def db():
    return Database("sqlite:///:memory:")


@pytest.fixture(scope="function")
def init_db(db: Database):  # type: ignore
    with db.session_ctx():
        Model.metadata.create_all(db.get_engine())
    yield
    with db.session_ctx():
        Model.metadata.drop_all(db.get_engine())


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


@pytest.mark.usefixtures("init_db")
def test_repository_find_by_id(db):
    with db.session_ctx() as session:
        session.add(MockModel(id=1))
        session.commit()

    repository = MockRepository()
    model_id = 1

    with db.session_ctx():
        result = repository.find_by_id(model_id)

    assert isinstance(result, MockModel)
    assert result.id == model_id


@pytest.mark.usefixtures("init_db")
def test_repository_find_by_id_not_found(db):
    repository = MockRepository()

    model_id = 2
    with db.session_ctx():
        result = repository.find_by_id(model_id)

    assert result is None
