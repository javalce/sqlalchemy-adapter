from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from sqlalchemy_adapter.database import Database


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, db: Database):
        super().__init__(app)
        self.db = db

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        with self.db.session_ctx():
            return await call_next(request)
