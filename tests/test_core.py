import pytest

from sqlalchemy_adapter.core import Database
from sqlalchemy_adapter.exception import (
    DBURLNotInitializedError,
    SessionNotInitializedError,
)


def test_database_without_url():
    db = Database()
    assert db.db_url is None
    assert db.engine is None
    assert db.session_factory is None


def test_database_with_url():
    db = Database("sqlite:///:memory:")
    assert db.db_url is not None
    assert db.engine is not None
    assert db.session_factory is not None


def test_initialize():
    db = Database()
    db.initialize("sqlite:///:memory:")
    assert db.db_url is not None
    assert db.engine_options is not None
    assert db.session_options is not None


def test_is_not_async():
    db = Database()
    assert not db.is_async()


def test_create_engine_without_url():
    db = Database()
    with pytest.raises(DBURLNotInitializedError) as excinfo:
        db.create_engine()
    assert "Database URL not set" in str(excinfo.value)


def test_create_engine():
    db = Database("sqlite:///:memory:")
    db.create_engine()
    assert db.engine is not None


def test_session_not_initialized_error():
    db = Database()
    with pytest.raises(SessionNotInitializedError) as excinfo:
        db.session  # noqa: B018
    assert "Session not initialized" in str(excinfo.value)


def test_session_ctx_sesssion_not_initialized_error():
    db = Database()
    with pytest.raises(SessionNotInitializedError) as excinfo:
        with db.session_ctx():
            pass
    assert "Session not initialized" in str(excinfo.value)


def test_session_ctx():
    db = Database("sqlite:///:memory:")
    with db.session_ctx() as session:
        assert session is not None
        assert db.session is not None
        assert db.session is session
    with pytest.raises(SessionNotInitializedError) as excinfo:
        db.session  # noqa: B018
    assert "Session not initialized" in str(excinfo.value)
