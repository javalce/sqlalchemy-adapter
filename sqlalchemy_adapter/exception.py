class SessionNotInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__("Session not initialized")


class DBURLNotInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__("Database URL not set")
