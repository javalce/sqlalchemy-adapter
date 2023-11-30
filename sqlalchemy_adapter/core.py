from typing import Any, Dict, Union

from sqlalchemy import URL, Engine, make_url


class AbstractDatabase:
    def __init__(
        self,
        url: Union[str, None] = None,
        engine_options: Union[Dict[str, Any], None] = None,
        session_options: Union[Dict[str, Any], None] = None,
    ) -> None:
        self.db_url: URL
        self.engine_options = engine_options or {}
        self.session_options = session_options or {}
        self.engine: Engine

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

    def is_async(self) -> bool:
        """Return True if this database instance is asynchronous."""
        return False
