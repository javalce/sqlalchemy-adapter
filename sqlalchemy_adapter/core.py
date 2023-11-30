import abc
from typing import Any, ContextManager, Dict, Union

from sqlalchemy import URL, Engine, create_engine, make_url
from sqlalchemy.orm import Session, sessionmaker

from .context import get_session, session_ctx
from .exception import DBURLNotInitializedError, SessionNotInitializedError


class AbstractDatabase(abc.ABC):
    def __init__(
        self,
        url: Union[str, None] = None,
        engine_options: Union[Dict[str, Any], None] = None,
        session_options: Union[Dict[str, Any], None] = None,
    ) -> None:
        self.db_url: Union[URL, None] = None
        self.engine_options = engine_options or {}
        self.session_options = session_options or {}
        self.engine: Union[Engine, None] = None
        self.session_factory: Union[sessionmaker[Session], None] = None

        if url is not None:
            self.initialize(url, engine_options)

    def initialize(
        self,
        url: str,
        engine_options: Union[Dict[str, Any], None] = None,
        session_options: Union[Dict[str, Any], None] = None,
    ) -> None:
        """Initialize the database instance.

        :param url: the database URL.
        :param engine_options: a dictionary with additional engine options to pass to SQLAlchemy.
        :param session_options: a dictionary with additional session options to use when creating a new session.

        This method must be called explicitly to complete the database initialization of the instance if the two-phase initialization method is used.
        """
        self.db_url = make_url(url)
        self.engine_options = engine_options or self.engine_options
        self.session_options = session_options or self.session_options

    def create_engine(self) -> None:
        """Create the SQLAlchemy engine."""
        self.engine = self._create_engine()

    @abc.abstractmethod
    def _create_engine(self) -> Engine:
        pass

    def is_async(self) -> bool:
        """Return True if this database instance is asynchronous."""
        return False


class Database(AbstractDatabase):
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

    def session_ctx(self) -> ContextManager[Session]:
        """Return a context manager that yields a new session."""
        try:
            assert self.session_factory is not None
            return session_ctx(self.session_factory)
        except Exception as e:
            raise SessionNotInitializedError from e
