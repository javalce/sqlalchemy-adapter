import pytest
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, clear_mappers, mapped_column

from sqlalchemy_adapter.core import Database
from sqlalchemy_adapter.model import Model
from sqlalchemy_adapter.repository import BaseRepository


@pytest.fixture
def MockModel():
    class MockModel(Model):
        __tablename__ = "mock_model"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    return MockModel


@pytest.fixture
def repository(MockModel):
    class MockRepository(BaseRepository[MockModel, int]):  # type: ignore
        model_class = MockModel

    return MockRepository()


@pytest.fixture
def db():
    return Database("sqlite:///:memory:")


@pytest.fixture(autouse=True)
def init_db_tables(db, MockModel):
    with db.session_ctx():
        Model.metadata.create_all(db.get_engine())
    yield
    with db.session_ctx():
        Model.metadata.drop_all(db.get_engine())
    Model.metadata.clear()
    clear_mappers()


def test_repository_find_all(db, MockModel, repository):
    with db.session_ctx() as session:
        session.add(MockModel(id=1))
        session.add(MockModel(id=2))
        session.add(MockModel(id=3))
        session.commit()

    with db.session_ctx():
        result = repository.find_all()

    assert isinstance(result, list)
    assert len(result) == 3


def test_repository_find_by_id(db, MockModel, repository):
    with db.session_ctx() as session:
        session.add(MockModel(id=1))
        session.commit()

    model_id = 1

    with db.session_ctx():
        result = repository.find_by_id(model_id)

    assert isinstance(result, MockModel)
    assert result.id == model_id


def test_repository_find_by_id_not_found(db, MockModel, repository):
    model_id = 2
    with db.session_ctx():
        result = repository.find_by_id(model_id)

    assert result is None


def test_repository_save(db, MockModel, repository):
    model = MockModel()

    with db.session_ctx():
        result = repository.save(model)

    assert isinstance(result, MockModel)
    assert result.id == 1


def test_repository_save_all(db, MockModel, repository):
    models = [MockModel(), MockModel(), MockModel()]

    with db.session_ctx():
        result = repository.save_all(models)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[2].id == 3


def test_repository_update_model(db, MockModel, repository):
    model = MockModel()
    with db.session_ctx():
        repository.save(model)
    model.id = 2
    with db.session_ctx():
        result = repository.save(model)
    assert result.id == 2


def test_repository_delete(db, MockModel, repository):
    model = MockModel()
    with db.session_ctx():
        repository.save(model)
    with db.session_ctx():
        repository.delete(model)
    with db.session_ctx():
        result = repository.find_by_id(model.id)
    assert result is None


def test_repository_delete_by_id(db, MockModel, repository):
    model = MockModel()
    with db.session_ctx():
        repository.save(model)
    with db.session_ctx():
        repository.delete_by_id(model.id)
    with db.session_ctx():
        result = repository.find_by_id(model.id)
    assert result is None


def test_repository_delete_by_id_not_found(db, MockModel, repository):
    model_id = 2
    with db.session_ctx():
        repository.delete_by_id(model_id)
    with db.session_ctx():
        result = repository.find_by_id(model_id)
    assert result is None
