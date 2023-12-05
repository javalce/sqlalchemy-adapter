from sqlalchemy.orm import Session

from .core.repository import AbstractRepository, K, T
from .database import get_session


class BaseRepository(AbstractRepository[T, K]):
    @property
    def session(self) -> Session:
        return get_session()
