from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Iterator, Union

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .abstract_database import AbstractDatabase
from .exception import DBURLNotInitializedError, SessionNotInitializedError

_session: ContextVar[Union[Session, None]] = ContextVar("_session", default=None)


def get_session() -> Session:
    session = _session.get()
    if session is None:
        raise SessionNotInitializedError
    return session


class Database(AbstractDatabase):
    """Initialize the database instance.

    :param url: the database URL.
    :param engine_options: a dictionary with additional engine options to pass to SQLAlchemy.
    :param session_options: a dictionary with additional session options to use when creating a new session.
    """

    def __init__(
        self,
        url: Union[str, None] = None,
        engine_options: Union[Dict[str, Any], None] = None,
        session_options: Union[Dict[str, Any], None] = None,
    ) -> None:
        super().__init__(url, engine_options, session_options)

    def initialize(
        self,
        url: str,
        engine_options: Union[Dict[str, Any], None] = None,
        session_options: Union[Dict[str, Any], None] = None,
    ) -> None:
        super().initialize(url, engine_options, session_options)
        self.create_engine()
        self.session_factory = sessionmaker(bind=self.engine, **self.session_options)

    def _create_engine(self) -> Engine:
        if self.db_url is None:
            raise DBURLNotInitializedError
        return create_engine(self.db_url, **self.engine_options)

    @property
    def session(self) -> Session:
        """Return a new session."""
        return get_session()

    @contextmanager
    def session_ctx(self) -> Iterator[Session]:
        """Return a context manager that yields a new session."""
        try:
            assert self.session_factory is not None
            with self.session_factory() as session:
                token = _session.set(session)
                yield session
                _session.reset(token)
        except Exception as e:
            raise SessionNotInitializedError from e
