import abc
from typing import Any, Dict, Union

from sqlalchemy import URL, Engine, make_url
from sqlalchemy.orm import Session, sessionmaker

from ..exception import EngineNotInitializedError


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
        """Create the SQLAlchemy engine."""
        pass

    def get_engine(self) -> Engine:
        """Return the SQLAlchemy engine."""
        if self.engine is None:
            raise EngineNotInitializedError
        return self.engine

    def is_async(self) -> bool:
        """Return True if this database instance is asynchronous."""
        return False
