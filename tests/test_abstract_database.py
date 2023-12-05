import pytest

from sqlalchemy_adapter.core.database import AbstractDatabase


def test_abstract_database_cannot_be_instantiated():
    with pytest.raises(TypeError) as excinfo:
        AbstractDatabase()  # type: ignore
    assert "Can't instantiate abstract class AbstractDatabase" in str(excinfo.value)
