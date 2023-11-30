from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, Union

from sqlalchemy.orm import Session, sessionmaker

from .exception import SessionNotInitializedError

_session: ContextVar[Union[Session, None]] = ContextVar("_session", default=None)


def get_session() -> Session:
    session = _session.get()
    if session is None:
        raise SessionNotInitializedError
    return session


@contextmanager
def session_ctx(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    with session_factory() as session:
        token = _session.set(session)
        yield session
        _session.reset(token)
